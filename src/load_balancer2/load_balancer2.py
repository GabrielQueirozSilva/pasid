from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

SERVICES = [
    "http://service2_1:5301/process",
    "http://service2_2:5302/process"
]

@app.route("/process", methods=["POST"])
def process():
    t1 = float(request.json.get("t1", time.time()))
    t2 = time.time()

    service_url = random.choice(SERVICES)

    try:
        r = requests.post(service_url, json={}, timeout=20)
        t4 = time.time()
        result = r.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    t5 = time.time()

    return jsonify({
        "t1": t1,
        "t2": t2,
        "t3": t2,      
        "t4": t4,
        "t5": t5
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5201)
