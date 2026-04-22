# MVP and Sprint Plan

## MVP Definition
A minimum valid ETL product should:
- generate data (`data/raw/products_dirty.csv`)
- clean and transform data (`data/processed/*.csv` + `eda_summary`)
- load cleaned results to PostgreSQL
- expose category summary in FastAPI

## Sprint Goals

### Sprint 1: Base ETL
- Generate raw CSV
- Transform and validate rows
- Produce cleaned and rejected output files

### Sprint 2: Database Load
- Create PostgreSQL tables with SQL scripts
- Load clean/rejected/summary files into database
- Verify tables in pgAdmin

### Sprint 3: Streaming + API
- Publish top-5 products to Kafka
- Consume Kafka events and store in DB
- Add FastAPI endpoints for products and statistics

## Done Definition
- Script runs end-to-end.
- PostgreSQL contains expected rows.
- API endpoints return data.

