# brewery_pipeline.py
import os
import json
import requests
import pandas as pd
from datetime import datetime

# Caminhos para as camadas do data lake
DATA_PATH = "data"
BRONZE_PATH = f"{DATA_PATH}/bronze"
SILVER_PATH = f"{DATA_PATH}/silver"
GOLD_PATH = f"{DATA_PATH}/gold"

# Criar diretórios se não existirem
for path in [BRONZE_PATH, SILVER_PATH, GOLD_PATH]:
    os.makedirs(path, exist_ok=True)

def extract_to_bronze():
    """Extrai dados da API e salva na camada Bronze"""
    print("Extraindo dados para a camada Bronze...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    bronze_file = f"{BRONZE_PATH}/breweries_{date_str}.json"
    
    response = requests.get('https://api.openbrewerydb.org/breweries')
    if response.status_code == 200:
        with open(bronze_file, 'w') as f:
            json.dump(response.json(), f)
        print(f"Dados salvos em {bronze_file}")
        return bronze_file
    else:
        raise Exception(f"Falha ao buscar dados: {response.status_code}")

def transform_to_silver(bronze_file):
    """Transforma dados da Bronze para Silver (particionado por estado)"""
    print("Transformando dados para a camada Silver...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Carregar dados da camada Bronze
    with open(bronze_file, 'r') as f:
        data = json.load(f)
    
    # Converter para DataFrame
    df = pd.DataFrame(data)
    
    # Particionar por estado
    for state, group in df.groupby('state'):
        if state and not pd.isna(state):
            # Criar diretório para o estado
            state_dir = f"{SILVER_PATH}/{state}"
            os.makedirs(state_dir, exist_ok=True)
            
            # Salvar como Parquet
            state_file = f"{state_dir}/breweries_{date_str}.parquet"
            group.to_parquet(state_file, index=False)
            print(f"Dados salvos em {state_file}")
    
    return SILVER_PATH

def transform_to_gold(silver_path):
    """Cria agregações na camada Gold"""
    print("Transformando dados para a camada Gold...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    all_data = []
    # Carregar dados de todos os estados da camada Silver
    for state in os.listdir(silver_path):
        state_dir = f"{silver_path}/{state}"
        if os.path.isdir(state_dir):
            state_files = [f for f in os.listdir(state_dir) if f.endswith('.parquet')]
            if state_files:
                latest_file = sorted(state_files)[-1]
                df = pd.read_parquet(f"{state_dir}/{latest_file}")
                all_data.append(df)
    
    if all_data:
        # Combinar todos os DataFrames
        combined_df = pd.concat(all_data)
        
        # Agregação por tipo e localização
        agg_by_type = combined_df.groupby(['brewery_type', 'state']).size().reset_index(name='count')
        
        # Salvar como Parquet na camada Gold
        gold_file = f"{GOLD_PATH}/brewery_aggregation_{date_str}.parquet"
        agg_by_type.to_parquet(gold_file, index=False)
        print(f"Dados agregados salvos em {gold_file}")
        return gold_file
    
    return None

def run_pipeline():
    """Executa o pipeline completo"""
    try:
        bronze_file = extract_to_bronze()
        silver_path = transform_to_silver(bronze_file)
        gold_file = transform_to_gold(silver_path)
        print("Pipeline executado com sucesso!")
    except Exception as e:
        print(f"Erro no pipeline: {str(e)}")

if __name__ == "__main__":
    run_pipeline()
