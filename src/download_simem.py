"""
Script para descargar datos históricos de la API SIMEM (XM Colombia).
Maneja automáticamente el límite de 31 días por request.
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import os

# Configuración
BASE_URL = "https://www.simem.co/backend-files/api/PublicData"
START_DATE = "2023-01-01"
END_DATE = "2026-04-03"
OUTPUT_DIR = "/home/user/workspace/ml-proyecto/data/raw"
MAX_DAYS_PER_REQUEST = 30  # conservador para no exceder el límite de 31

# Datasets a descargar
DATASETS = {
    # Variable objetivo
    "precio_bolsa_horario": {
        "id": "EC6945",
        "description": "Precio de Bolsa Horario (COP/kWh)",
        "granularity": "hourly"
    },
    "precio_bolsa_ponderado": {
        "id": "96D56E", 
        "description": "Precio de Bolsa Ponderado Diario",
        "granularity": "daily"
    },
    # Predictores de precio
    "max_precio_ofertado": {
        "id": "03ba47",
        "description": "Máximo Precio Ofertado",
        "granularity": "daily"
    },
    "precio_escasez": {
        "id": "43D616",
        "description": "Precio de Escasez Ponderado",
        "granularity": "daily"
    },
    # Demanda
    "demanda_comercial": {
        "id": "d55202",
        "description": "Demanda Comercial de Energía",
        "granularity": "hourly"
    },
    # Generación
    "generacion_real": {
        "id": "055A4D",
        "description": "Generación Real por tipo",
        "granularity": "hourly"
    },
    # Hidrología
    "aportes_hidricos": {
        "id": "BA1C55",
        "description": "Aportes Hídricos en Energía",
        "granularity": "daily"
    },
    "nivel_embalses": {
        "id": "BD26DC",
        "description": "Nivel de Embalse Declarado",
        "granularity": "daily"
    },
}

def generate_date_chunks(start_date: str, end_date: str, max_days: int = 30):
    """Genera pares de fechas en chunks de max_days."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    chunks = []
    current = start
    while current < end:
        chunk_end = min(current + timedelta(days=max_days), end)
        chunks.append((current.strftime("%Y-%m-%d"), chunk_end.strftime("%Y-%m-%d")))
        current = chunk_end + timedelta(days=1)
    
    return chunks

def fetch_simem_data(dataset_id: str, start_date: str, end_date: str):
    """Consulta un dataset de SIMEM para un rango de fechas."""
    params = {
        "datasetId": dataset_id,
        "startDate": start_date,
        "endDate": end_date
    }
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        if data.get("success") and data.get("result", {}).get("records"):
            return data["result"]["records"]
        
        # Intentar estructura alternativa
        if isinstance(data, dict) and "result" in data:
            result = data["result"]
            if isinstance(result, list):
                return result
            if isinstance(result, dict):
                for key in ["records", "data", "datos"]:
                    if key in result and isinstance(result[key], list):
                        return result[key]
        
        return []
    except Exception as e:
        print(f"  Error: {e}")
        return []

def download_dataset(name: str, config: dict):
    """Descarga un dataset completo dividiendo en chunks."""
    dataset_id = config["id"]
    description = config["description"]
    
    print(f"\n{'='*60}")
    print(f"Descargando: {description}")
    print(f"Dataset ID: {dataset_id}")
    print(f"Rango: {START_DATE} → {END_DATE}")
    print(f"{'='*60}")
    
    chunks = generate_date_chunks(START_DATE, END_DATE, MAX_DAYS_PER_REQUEST)
    all_records = []
    
    for i, (chunk_start, chunk_end) in enumerate(chunks):
        print(f"  Chunk {i+1}/{len(chunks)}: {chunk_start} → {chunk_end} ... ", end="", flush=True)
        
        records = fetch_simem_data(dataset_id, chunk_start, chunk_end)
        
        if records:
            all_records.extend(records)
            print(f"✓ {len(records)} registros")
        else:
            print("✗ sin datos")
        
        # Rate limiting
        time.sleep(0.5)
    
    if all_records:
        df = pd.DataFrame(all_records)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(output_path, index=False)
        print(f"\n  TOTAL: {len(df)} registros → {output_path}")
        print(f"  Columnas: {list(df.columns)}")
        return df
    else:
        print(f"\n  ⚠ No se obtuvieron datos para {name}")
        return None

def main():
    """Descarga todos los datasets configurados."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    results = {}
    for name, config in DATASETS.items():
        df = download_dataset(name, config)
        if df is not None:
            results[name] = df
    
    # Resumen final
    print(f"\n{'='*60}")
    print("RESUMEN DE DESCARGA")
    print(f"{'='*60}")
    for name, df in results.items():
        print(f"  {name}: {len(df)} registros, {len(df.columns)} columnas")
    
    return results

if __name__ == "__main__":
    main()
