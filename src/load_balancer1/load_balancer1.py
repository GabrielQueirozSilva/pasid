from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

SERVICES = [
    "http://lb2:5201/process"
]

@app.route("/process", methods=["POST"])
def process():
    t1 = time.time()
    data = request.json or {}
    t1 = data.get("timestamp", t1)

    target = random.choice(SERVICES)
    try:
        r = requests.post(target, json={"t1": t1}, timeout=10)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101)