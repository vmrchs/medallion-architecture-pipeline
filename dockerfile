FROM python:3.9-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY brewery_pipeline.py .
COPY test_brewery_pipeline.py .
# Criar diretórios de dados
RUN mkdir -p data/bronze data/silver data/gold

# Comando para executar o pipeline
CMD ["python", "brewery_pipeline.py"]