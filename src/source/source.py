import requests
import time
import csv
import socket

taxas = [1, 5, 10, 20]  
duracao = 10  
url = "http://lb1:5101/process"

def esperar_lb1(host="lb1", port=5101, timeout=30):
    inicio = time.time()
    while time.time() - inicio < timeout:
        try:
            with socket.create_connection((host, port), timeout=2):
                print(f"[source] Conexão com {host}:{port} estabelecida.")
                return
        except OSError:
            print(f"[source] Aguardando {host}:{port} estar disponível...")
            time.sleep(1)
    raise RuntimeError(f"[source] {host}:{port} não respondeu após {timeout} segundos.")


def coletar_tempos(taxa):
    tempos = []
    intervalo = 1 / taxa
    inicio = time.time()
    while time.time() - inicio < duracao:
        t_envio = time.time()
        try:
            r = requests.post(url, json={"timestamp": t_envio, "texto": "This is a test input to stress NLP inference."})
            if r.status_code == 200:
                dados = r.json()
                tempos.append(dados)
        except Exception as e:
            print("Erro:", e)
        time.sleep(intervalo)
    return tempos

def salvar_csv(taxa, dados):
    with open(f"/app/tempos_taxa_{taxa}.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["taxa", "mrt", "t1", "t2", "t3", "t4", "t5"])
        for d in dados:
            mrt = d["t5"] - d["t1"]
            writer.writerow([
                taxa,
                mrt,
                d["t1"], d["t2"], d["t3"], d["t4"], d["t5"]
            ])

if __name__ == "__main__":
    esperar_lb1()  
    for taxa in taxas:
        print(f"Executando experimento para taxa {taxa} req/s...")
        dados = coletar_tempos(taxa)
        salvar_csv(taxa, dados)