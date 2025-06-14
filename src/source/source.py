import requests
import time
import csv
import socket
import matplotlib.pyplot as plt
import pandas as pd
import os

taxas = [1, 5, 10, 20]  # Requisições por segundo
duracao = 10  # Segundos
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
                dados["t_envio"] = t_envio
                dados["t_recebido"] = time.time()
                tempos.append(dados)
        except Exception as e:
            print("Erro:", e)
        time.sleep(intervalo)
    return tempos

def salvar_csv(taxa, dados):
    os.makedirs("resultados", exist_ok=True)
    path = f"resultados/tempos_taxa_{taxa}.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["taxa", "mrt", "t_envio", "t_recebido"])
        for d in dados:
            mrt = d["t_recebido"] - d["t_envio"]
            writer.writerow([taxa, mrt, d["t_envio"], d["t_recebido"]])
    return path

def gerar_grafico_individual(path_csv, taxa):
    df = pd.read_csv(path_csv)
    plt.figure(figsize=(8, 5))
    plt.plot(df.index, df["mrt"], marker="o", label=f"{taxa} req/s")
    plt.title(f"MRT - Taxa {taxa} req/s")
    plt.xlabel("Requisição #")
    plt.ylabel("Tempo de Resposta (s)")
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("graficos", exist_ok=True)
    plt.savefig(f"graficos/grafico_taxa_{taxa}.png")
    plt.close()

def gerar_grafico_comparativo(mrts_por_taxa):
    taxas = list(mrts_por_taxa.keys())
    mrts = list(mrts_por_taxa.values())

    plt.figure(figsize=(8, 5))
    plt.plot(taxas, mrts, marker='o', color='blue', linestyle='-')
    plt.title("Tempo Médio de Resposta (MRT) por Taxa de Requisição")
    plt.xlabel("Taxa de Requisições por Segundo")
    plt.ylabel("MRT Médio (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficos/mrt_mensagens.png")
    plt.close()
    print("Gráfico comparativo salvo em: graficos/mrt_mensagens.png")

if __name__ == "__main__":
    esperar_lb1()
    mrts_por_taxa = {}

    for taxa in taxas:
        print(f"\nExecutando experimento para taxa {taxa} req/s...")
        dados = coletar_tempos(taxa)
        csv_path = salvar_csv(taxa, dados)
        gerar_grafico_individual(csv_path, taxa)

        # Calcular MRT médio para gráfico comparativo
        df = pd.read_csv(csv_path)
        mrt_medio = df["mrt"].mean()
        mrts_por_taxa[taxa] = mrt_medio
        print(f"MRT médio para {taxa} req/s: {mrt_medio:.4f}s")

    gerar_grafico_comparativo(mrts_por_taxa)
    print("\nExperimentos concluídos! Gráficos salvos na pasta 'graficos'.")