# CryptoStream-AI

A real-time cryptocurrency data pipeline and forecasting system that leverages Coinbase API, Apache Kafka, Apache Spark, and Cassandra to enable efficient data ingestion, processing, storage, and visualization. This system is designed to process live cryptocurrency price data for popular coins such as Bitcoin (BTC), Ethereum (ETH), and others, providing real-time insights and predictions.

### Architecture Diagram:
![alt text](<Architecture Diagram.png>)

### Key features include:
- Real-time Data Ingestion: Seamlessly fetches cryptocurrency price data from the Coinbase API and streams it into Kafka topics for downstream processing.
- Distributed Data Processing: Uses Apache Spark to handle high-velocity streaming data, transform it into a structured format, and store it in Cassandra for scalable and low-latency querying.
- Machine Learning Forecasting: Implements cutting-edge forecasting models such as ARIMA, VAR, Moving Averages, and LSTM neural networks to predict future price trends for individual cryptocurrencies or relationships between coin pairs.
- Data Visualization: Combines the power of Grafana for real-time monitoring of cryptocurrency metrics and Streamlit for intuitive dashboards, enabling users to explore predictions and perform trend analysis.
- CSV Export for Offline Analysis: Exports processed data to CSV files for further offline analysis or integration with other tools.
- Modular and Scalable Design: Built using a microservices approach with Dockerized components for scalability, ease of deployment, and adaptability to new data sources or models.

This robust data pipeline serves as a comprehensive tool for crypto enthusiasts, data scientists, and traders looking to analyze live cryptocurrency trends, monitor key metrics, and make informed decisions using machine learning-based forecasts. Whether for casual users or professionals, CryptoStream-AI provides both deep insights and actionable intelligence into the ever-changing cryptocurrency market.


## Project Architecture 

### Data Ingestion
- Pulls real-time cryptocurrency prices from Coinbase API
- Publishes data to Kafka topics using Python

### Data Processing
- Spark processes data from Kafka topics
- Transforms data into structured formats
- Stores processed data in Cassandra and CSV files

### Storage
- Cassandra stores processed cryptocurrency data
- Data exported to CSV for additional analysis

### Machine Learning Models
- ARIMA, LSTM, VAR, and Moving Averages for forecasting
- Pre-trained LSTM models stored in saved_models/

### Visualization
- Grafana: Provides real-time dashboards for monitoring cryptocurrency data stored in Cassandra.
- Streamlit: Offers interactive dashboards for selecting coins, forecasting models, and visualizing predictions.

## Folder Structure
```
├── .gitignore
├── README.md
├── Architechture Diagram.png
├── data_ingestion/            # Code for data ingestion from Coinbase API
├── data_processing/           # Apache Spark data processing scripts
├── frontend/                  # Streamlit application for visualization
├── kafka/                     # Kafka Docker configuration
├── raw_data_storage/          # Raw data scripts and files
├── processed_data_storage/    # Cassandra schema and processed data
├── saved_models/             # Pre-trained LSTM models and scalers
├── coinbase_data/            # CSV files exported from Spark
└── export_cassandra_to_csv.py # Export Cassandra data to CSV
```
## Installation and Setup

### Prerequisites
- Python 3.9+
- Java 8+
- Apache Kafka
- Apache Spark
- Cassandra
- Docker
- Streamlit

### Clone the Repository
```
git clone https://github.com/isiddharthsingh/CryptoStream-AI.git
cd CryptoStream-AI
```

### Setup Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r data_ingestion/requirements.txt
pip install -r data_processing/requirements.txt
pip install -r frontend/requirements.txt
```

### Start Kafka and Cassandra
```
docker-compose -f kafka/docker-compose.yml up
```

### Run the Data Pipeline

Start the Kafka producer:
```
python data_ingestion/producer.py
```
Run the Spark job:
```
spark-submit --packages com.datastax.spark:spark-cassandra-connector_2.12:3.1.0 data_processing/spark_job.py
```
### Start the Frontend
```
streamlit run frontend/app.py
```
## Features

### Real-time Data Ingestion
- Collects cryptocurrency price data for 11 popular coins (BTC, ETH, ADA, etc.)

### Real-time Data Processing
- Kafka as streaming platform
- Spark processes real-time data streams

### Machine Learning Forecasting
- Pre-trained models (ARIMA, LSTM, VAR, Moving Averages)
- Future cryptocurrency price predictions

### Visualization
- Streamlit dashboard for model and coin selection
- Grafana for real-time data visualization

## Usage

### Run Forecasts
- Select coins and forecasting models via Streamlit dashboard
- Visualize cryptocurrency trends and predictions

### Real-time Data Monitoring
- Monitor live cryptocurrency data in Grafana

## Technologies Used

| Category | Technologies |
|----------|-------------|
| Languages | Python, Go |
| Data Pipeline | Kafka, Spark, Cassandra |
| Machine Learning | TensorFlow, ARIMA, VAR, Moving Averages |
| Visualization | Streamlit, Grafana |
| Containerization | Docker |

## Contributors
- Siddharth Singh

## License
This project is licensed under the MIT License.
