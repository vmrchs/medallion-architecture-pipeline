# Brewery Data Pipeline

A modern data pipeline that extracts, transforms, and loads brewery data following the medallion architecture pattern (Bronze, Silver, Gold layers).

![Medallion Architecture](https://img.shields.io/badge/Architecture-Medallion-blue)
![Python](https://img.shields.io/badge/Python-3.9-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

## 🏗️ Architecture

This project implements a data pipeline following the Medallion Architecture (also known as Delta/Lakehouse Architecture):

- **Bronze Layer**: Raw data stored as JSON, exactly as received from the API
- **Silver Layer**: Cleaned and transformed data, partitioned by state, stored as Parquet files
- **Gold Layer**: Business-level aggregations and metrics for analysis, stored as Parquet files

## 🚀 Features

- **API Integration**: Fetches brewery data from the Open Brewery DB API
- **Data Partitioning**: Organizes data by state for efficient access
- **Automated Aggregations**: Creates business-ready datasets with brewery counts by type and state
- **Containerized**: Fully dockerized for environment consistency
- **Unit Tested**: Includes comprehensive tests for all pipeline stages

## 📋 Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🛠️ Installation

1. Clone this repository

   ```bash
   git clone https://github.com/vmrchs/medallion-architecture-pipeline.git
   cd brewery-data-pipeline
   ```

2. Build and run the pipeline
   ```bash
   docker-compose up --build
   ```

## 📊 Data Visualization with DBeaver

The pipeline stores data in Parquet format. To visualize it:

1. Install [DBeaver](https://dbeaver.io/download/)
2. Connect to your data:
   - Use "File" connection type for Parquet files
   - Browse to the `./data` directory to access the processed data
   - Explore Silver layer data (by state) or Gold layer aggregations

## 📁 Project Structure

```
medallion-architecture-pipeline/
│
├── brewery_pipeline.py     # Main pipeline implementation
├── test_brewery_pipeline.py # Unit tests
├── Dockerfile              # Container configuration
├── docker-compose.yaml     # Service orchestration
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── data/                   # Data storage (mounted volume)
    ├── bronze/             # Raw JSON data from API
    ├── silver/             # Cleaned data partitioned by state
    └── gold/               # Aggregated business metrics
```

## 🧪 Testing

Run the tests with:

```bash
docker-compose run brewery_pipeline python test_brewery_pipeline.py
```

## 🔄 Data Flow

1. **Extract**: Data is pulled from the Open Brewery DB API and stored as raw JSON in the Bronze layer
2. **Transform - Silver**: Raw data is cleaned, validated, and partitioned by state
3. **Transform - Gold**: Silver data is aggregated to create business metrics by brewery type and state

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
