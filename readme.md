# Pipeline de Dados de Cervejarias

Este projeto implementa um pipeline de dados que consome a API Open Brewery DB e armazena os dados em uma arquitetura de medalhão de três camadas.

## Arquitetura

- **Bronze**: Dados brutos da API em formato JSON
- **Silver**: Dados transformados e particionados por estado em formato Parquet
- **Gold**: Dados agregados por tipo e localização

## Requisitos

- Docker
- Docker Compose

## Como executar

1. Clone o repositório
2. Execute o pipeline:

```bash
docker-compose up
```

Os dados processados serão armazenados na pasta `data/` com a seguinte estrutura:
- `data/bronze/`: Dados brutos da API
- `data/silver/`: Dados transformados e particionados por estado
- `data/gold/`: Agregações por tipo e localização

## Estrutura do projeto

```
brewery-pipeline/
│
├── brewery_pipeline.py    # Script principal do pipeline
├── Dockerfile             # Configuração do container
├── docker-compose.yml     # Configuração do Docker Compose
├── requirements.txt       # Dependências Python
└── data/                  # Diretório onde os dados serão armazenados
    ├── bronze/            # Camada bronze (dados brutos)
    ├── silver/            # Camada silver (dados tratados por estado)
    └── gold/              # Camada gold (dados agregados)
```

## Monitoramento e Alertas

Para um ambiente de produção, recomenda-se implementar:

1. **Monitoramento do Pipeline**:
   - Integração com ferramentas como Prometheus/Grafana
   - Logs centralizados com ELK Stack ou CloudWatch

2. **Qualidade de Dados**:
   - Validações de schema e integridade
   - Monitoramento de valores nulos ou inválidos

3. **Alertas**:
   - Notificações por e-mail, Slack ou outros canais
   - Alertas para falhas no pipeline e problemas de qualidade de dados

## Extensões Futuras

1. **Agendamento**: Integrar com Airflow ou outras ferramentas de orquestração
2. **Escalabilidade**: Migrar para processamento distribuído com Spark
3. **Cloud**: Implementar usando serviços em nuvem como AWS S3/Glue, Azure Data Lake/Databricks
