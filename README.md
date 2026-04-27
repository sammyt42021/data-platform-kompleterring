# Product ETL Project (Komplettering)

This is my ETL project for the data platform komplettering.  
I built it as a clear pipeline with small scripts so each step is easy to run and explain.

Pipeline flow:
1. Extract: generate a raw CSV dataset.
2. Transform: validate rows, separate rejected records, and calculate statistics.
3. Load: store clean and summary data in PostgreSQL.
4. Stream (optional): validate Kafka with a produce/consume smoke test.

## Tech Stack
- Python (`pandas`, `FastAPI`)
- PostgreSQL
- pgAdmin
- Kafka + Zookeeper
- Docker Compose

## Project Structure

```text
.
├── app/
├── consumer/
├── data/
│   ├── raw/
│   └── processed/
├── documentation/
├── scripts/
├── schema/
├── sql/
├── tests/
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Start Services

```bash
docker compose up -d
```

- PostgreSQL: `localhost:55432`
- pgAdmin: `http://localhost:5050`
- pgAdmin login: `admin@example.com` / `admin123`
- Kafka: `localhost:9092`

## Quick Start

Run these commands in order:

```bash
cd /Users/tobisamuel/data-platform-kompleterring
source .venv/bin/activate
docker compose up -d
python -m pytest -q
python scripts/run_all.py
```

Verify loaded row counts in PostgreSQL:

```bash
docker compose exec -T postgres psql -U etl_user -d etl_db -c "select count(*) from staging.products_clean;"
docker compose exec -T postgres psql -U etl_user -d etl_db -c "select count(*) from staging.products_rejected;"
docker compose exec -T postgres psql -U etl_user -d etl_db -c "select count(*) from analytics.category_summary;"
```

Expected counts after a normal run:
- `staging.products_clean`: `60`
- `staging.products_rejected`: `5`
- `analytics.category_summary`: `5`

## Run ETL

```bash
python3 scripts/run_all.py
```

This executes:
- `scripts/generate_dirty_csv.py`
- `scripts/transform.py`
- `scripts/load_products.py`

Generated outputs:
- `data/raw/products_dirty.csv`
- `data/processed/products_clean.csv`
- `data/processed/products_rejected.csv`
- `data/processed/category_summary.csv`
- `data/processed/top_5_expensive.csv`
- `data/processed/eda_summary.json`

## Kafka (Optional)

Simple smoke test (create topic, produce one message, consume one message):

```bash
docker compose exec kafka kafka-topics --bootstrap-server kafka:29092 --create --topic etl-test --partitions 1 --replication-factor 1
echo "hello-etl" | docker compose exec -T kafka kafka-console-producer --bootstrap-server kafka:29092 --topic etl-test
docker compose exec -T kafka kafka-console-consumer --bootstrap-server kafka:29092 --topic etl-test --from-beginning --max-messages 1
```

## Useful SQL Checks

```sql
SELECT COUNT(*) FROM staging.products_clean;
SELECT * FROM analytics.category_summary ORDER BY total_inventory_value DESC;
```

## Stop Services

```bash
docker compose down
```

## Troubleshooting

pgAdmin exits immediately with an email error:
- Symptom: container shows `Exited (1)` and logs mention invalid `PGADMIN_DEFAULT_EMAIL`.
- Fix: use a valid email in `docker-compose.yml`, for example:
  - `PGADMIN_DEFAULT_EMAIL: admin@example.com`
  - `PGADMIN_DEFAULT_PASSWORD: admin123`
- Restart pgAdmin:

```bash
docker compose up -d --force-recreate pgadmin
docker compose ps -a
```

Common Docker restart steps:

```bash
docker compose down
docker compose up -d
docker compose ps
```

## Scope Notes
- I used PostgreSQL + pgAdmin as requested.
- I focused on an understandable ETL flow with clear scripts and documentation.
