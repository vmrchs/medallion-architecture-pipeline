# test_brewery_pipeline.py
import os
import unittest
import json
from unittest.mock import patch, MagicMock
import pandas as pd
import brewery_pipeline

class TestBreweryPipeline(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para testes
        self.sample_data = [
            {
                "id": "brewery-1",
                "name": "Test Brewery 1",
                "brewery_type": "micro",
                "city": "Test City",
                "state": "Test State"
            },
            {
                "id": "brewery-2",
                "name": "Test Brewery 2",
                "brewery_type": "brewpub",
                "city": "Another City",
                "state": "Another State"
            }
        ]
        
        # Configurar diretórios de teste
        self.test_dir = "test_data"
        os.makedirs(f"{self.test_dir}/bronze", exist_ok=True)
        os.makedirs(f"{self.test_dir}/silver", exist_ok=True)
        os.makedirs(f"{self.test_dir}/gold", exist_ok=True)
    
    def tearDown(self):
        # Limpar diretórios de teste após os testes
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    @patch('brewery_pipeline.requests.get')
    def test_extract_to_bronze(self, mock_get):
        # Configurar o mock da API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response
        
        # Redirecionar o caminho de saída para os diretórios de teste
        with patch('brewery_pipeline.BRONZE_PATH', f"{self.test_dir}/bronze"):
            result = brewery_pipeline.extract_to_bronze()
        
        # Verificar se o arquivo foi criado
        self.assertTrue(os.path.exists(result))
        
        # Verificar o conteúdo do arquivo
        with open(result, 'r') as f:
            data = json.load(f)
        self.assertEqual(data, self.sample_data)
    
    def test_transform_to_silver(self):
        # Criar arquivo bronze de teste
        bronze_file = f"{self.test_dir}/bronze/test_breweries.json"
        with open(bronze_file, 'w') as f:
            json.dump(self.sample_data, f)
        
        # Redirecionar caminhos para diretórios de teste
        with patch('brewery_pipeline.SILVER_PATH', f"{self.test_dir}/silver"):
            result = brewery_pipeline.transform_to_silver(bronze_file)
        
        # Verificar se os diretórios de estado foram criados
        self.assertTrue(os.path.exists(f"{self.test_dir}/silver/Test State"))
        self.assertTrue(os.path.exists(f"{self.test_dir}/silver/Another State"))
        
        # Verificar se os arquivos parquet contêm os dados corretos
        state_files = os.listdir(f"{self.test_dir}/silver/Test State")
        self.assertTrue(len(state_files) > 0)
        
        df = pd.read_parquet(f"{self.test_dir}/silver/Test State/{state_files[0]}")
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['name'], 'Test Brewery 1')
    
    def test_transform_to_gold(self):
        # Criar arquivos silver de teste
        os.makedirs(f"{self.test_dir}/silver/Test State", exist_ok=True)
        os.makedirs(f"{self.test_dir}/silver/Another State", exist_ok=True)
        
        pd.DataFrame([self.sample_data[0]]).to_parquet(
            f"{self.test_dir}/silver/Test State/test_breweries.parquet"
        )
        pd.DataFrame([self.sample_data[1]]).to_parquet(
            f"{self.test_dir}/silver/Another State/test_breweries.parquet"
        )
        
        # Redirecionar caminhos para diretórios de teste
        with patch('brewery_pipeline.GOLD_PATH', f"{self.test_dir}/gold"):
            result = brewery_pipeline.transform_to_gold(f"{self.test_dir}/silver")
        
        # Verificar se o arquivo gold foi criado
        self.assertTrue(os.path.exists(result))
        
        # Verificar o conteúdo do arquivo gold
        df = pd.read_parquet(result)
        self.assertEqual(df.shape[0], 2)  # Duas combinações de tipo/estado
        self.assertEqual(
            df[(df['brewery_type'] == 'micro') & (df['state'] == 'Test State')]['count'].iloc[0], 
            1
        )

if __name__ == '__main__':
    unittest.main()
