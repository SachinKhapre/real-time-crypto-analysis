# Real-Time Ethereum Analytics Pipeline

A fully containerized, end-to-end real-time analytics pipeline for tracking Ethereum (ETH) price every 15 seconds using the Binance API. It covers ingestion, processing, transformation, orchestration, and visualization.

---

## 🚀 Stack Overview

| Layer             | Tool/Tech                  |
| ----------------- | -------------------------- |
| Ingestion         | Python + Kafka             |
| Stream Processing | Spark Structured Streaming |
| Storage           | PostgreSQL, Amazon S3      |
| Transformation    | dbt                        |
| Orchestration     | Dagster                    |
| Visualization     | Metabase                   |

---

## 📦 Project Structure

```
real-time-crypto-analysis/
├── docker-compose.yml
├── .env
├── kafka_producer/
│   └── kafka_producer.py
├── spark_job/
│   ├── stream_eth_prices.py
│   └── spark-submit.sh
├── dbt_eth_pipeline/
│   └── dbt project (models, profiles.yml, etc)
├── dagster_project/
│   └── Dagster definitions
├── docker/
│   └── Dockerfile
```

---

## 🛠️ Setup Instructions

### 1. Clone Repo & Create .env

```bash
git clone https://github.com/SachinKhapre/real-time-crypto-analysis.git
cd real-time-crypto-analysis
```

### 2. Start Services

```bash
docker-compose up --build
```

### 3. Create Kafka Topic

```bash
docker-compose run kafka-init
```

### 4. Run Spark 

```bash
docker-compose run spark
```

### 5. Run Producer

```bash
python3 kafka_producer/kafka_producer.py
```

### 5. DBT Models

```bash
cd dbt_eth_pipeline/dbt_cryptodata
# Run transformations
dbt run
```

### 6. Dagster

```bash
cd dagster_project
dagster dev -p 3001
```

### 7. Metabase (Dashboard)

Access Metabase at: [http://localhost:3000](http://localhost:3000)

* Connect to Postgres
* Build dashboards from dbt models

---

## 📈 DBT Models

* `stg_eth_prices`: Raw data
* `price_change_last_hour`: % change in price
* `eth_price_5min_avg`: 5-minute average
* `eth_price_daily_avg`: Daily average
* `price_volatility`: Price volatility

---

## ✅ To-Do

* Add dbt tests & snapshots
* Add alerts/sensors in Dagster
* (Optional) Deploy on AWS

---

## 📄 License

Apache License
