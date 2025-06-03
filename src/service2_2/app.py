from flask import Flask, request, jsonify
import time
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__)

# Define o dispositivo
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Carrega o modelo treinado e o tokenizer
tokenizer = BertTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model = BertForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
model.to(device)
model.eval()

@app.route("/process", methods=["POST"])
def process():
    texto = request.json.get("texto", "This is a test sentence.")

    start_time = time.time()

    # Tokeniza e envia para o device
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Inferência sem gradientes
    with torch.no_grad():
        outputs = model(**inputs)

    elapsed = time.time() - start_time

    return jsonify({
        "status": "success",
        "elapsed_time": elapsed,
        "logits": outputs.logits.tolist()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5302)
