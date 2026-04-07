"""
Descarga rápida de datos SIMEM usando threads concurrentes.
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import time

BASE_URL = "https://www.simem.co/backend-files/api/PublicData"
START_DATE = "2023-01-01"
END_DATE = "2026-04-03"
OUTPUT_DIR = "/home/user/workspace/ml-proyecto/data/raw"

DATASETS = {
    "precio_bolsa_ponderado": "96D56E",
    "max_precio_ofertado": "03ba47",
    "precio_escasez": "43D616",
    "demanda_comercial": "d55202",
    "generacion_real": "055A4D",
    "aportes_hidricos": "BA1C55",
    "nivel_embalses": "BD26DC",
}

def date_chunks(start, end, days=30):
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    chunks = []
    c = s
    while c < e:
        ce = min(c + timedelta(days=days), e)
        chunks.append((c.strftime("%Y-%m-%d"), ce.strftime("%Y-%m-%d")))
        c = ce + timedelta(days=1)
    return chunks

def fetch_chunk(dataset_id, start, end):
    try:
        r = requests.get(BASE_URL, params={
            "datasetId": dataset_id, "startDate": start, "endDate": end
        }, timeout=45)
        r.raise_for_status()
        data = r.json()
        if data.get("success") and data.get("result", {}).get("records"):
            return data["result"]["records"]
        if isinstance(data.get("result"), dict):
            for k in ["records", "data"]:
                if k in data["result"] and isinstance(data["result"][k], list):
                    return data["result"][k]
        return []
    except Exception as e:
        print(f"    Error {dataset_id} [{start}→{end}]: {e}")
        return []

def download_one(name, dataset_id):
    print(f"\n  Descargando {name} ({dataset_id})...")
    chunks = date_chunks(START_DATE, END_DATE, 30)
    all_records = []
    
    for i, (s, e) in enumerate(chunks):
        records = fetch_chunk(dataset_id, s, e)
        if records:
            all_records.extend(records)
        if (i + 1) % 10 == 0:
            print(f"    {name}: {i+1}/{len(chunks)} chunks, {len(all_records)} records...")
        time.sleep(0.3)
    
    if all_records:
        df = pd.DataFrame(all_records)
        path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"  ✓ {name}: {len(df)} registros, cols={list(df.columns)[:5]}")
        return name, len(df)
    else:
        print(f"  ✗ {name}: sin datos")
        return name, 0

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Descargar secuencialmente pero con menor sleep
results = {}
for name, did in DATASETS.items():
    n, count = download_one(name, did)
    results[n] = count

print("\n" + "="*50)
print("RESUMEN:")
for n, c in results.items():
    print(f"  {n}: {c} registros")
