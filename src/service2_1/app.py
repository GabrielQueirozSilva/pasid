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

# Endpoint de health check
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

@app.route("/process", methods=["POST"])
def process():
    texto = request.json.get("texto", "This is a test sentence.")
    t1 = float(request.json.get("t1", time.time()))
    t3 = time.time()  

   
    inputs = tokenizer(texto, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    t4 = time.time()  # Após inferência
    t5 = time.time()  # Pronto para resposta

    return jsonify({
        "t1": t1,
        "t3": t3,
        "t4": t4,
        "t5": t5,
        "status": "success",
        "logits": outputs.logits.tolist()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5301)
