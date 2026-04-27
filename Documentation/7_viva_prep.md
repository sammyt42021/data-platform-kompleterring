# Viva / Demo Prep Notes

## 1-minute Project Summary
"I built an ETL pipeline for product data. The flow is: generate raw CSV, clean and validate rows, create category statistics, load to PostgreSQL, then optionally stream top products through Kafka and consume them back into PostgreSQL. I also added a small FastAPI service for read endpoints and documented each step." 

## Why this architecture?
- CSV generation gives reproducible local input data.
- Transform is separated from load so data quality is visible before DB insert.
- PostgreSQL stores both clean and rejected outputs for traceability.
- Kafka demonstrates continuation from batch to stream.
- FastAPI gives quick read access without opening SQL every time.

## Key files to explain quickly
- `scripts/generate_dirty_csv.py`: creates valid + invalid sample rows.
- `scripts/transform.py`: validation, clean/rejected split, category summary, EDA JSON.
- `scripts/load_products.py`: inserts ETL outputs into PostgreSQL tables.
- `sql/01_create_tables.sql`: target table definitions.
- `scripts/publish_top5_to_kafka.py` + `consumer/db_consumer.py`: stream flow.
- `app/main.py`: API endpoints for health, products, stats, stream.

## Typical lecturer questions and short answers
1. Why do you keep rejected rows?
- "To keep a clear audit trail and understand data quality issues instead of silently dropping bad records."

2. Why separate scripts instead of one large script?
- "It is easier to test, debug, and explain each ETL phase independently."

3. What proves transformation happened?
- "Generated artifacts: `products_clean.csv`, `products_rejected.csv`, `category_summary.csv`, and `eda_summary.json`."

4. How do you verify load worked?
- "I query `staging.products_clean` and `analytics.category_summary` in pgAdmin/psql."

5. Why use Kafka here?
- "To show pipeline continuation from batch processing to event-driven flow."

## Demo sequence (safe and short)
1. `docker compose up -d`
2. `python3 scripts/run_all.py`
3. Show one SQL check in pgAdmin or psql.
4. `python3 scripts/publish_top5_to_kafka.py`
5. `python3 consumer/db_consumer.py` (brief run)
6. `uvicorn app.main:app --reload` and open `/health` + one data endpoint.

## If something fails during demo
- "The project is modular, so I can run each script independently and isolate the failing stage quickly."
