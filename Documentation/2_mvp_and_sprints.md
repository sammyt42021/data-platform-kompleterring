# MVP and Sprint Plan

## MVP Definition
For me, MVP means the core ETL works end-to-end:
- generate raw data (`data/raw/products_dirty.csv`)
- clean and split data (`data/processed/*.csv` + `eda_summary.json`)
- load clean and summary outputs into PostgreSQL
- query the stored results (SQL and API)

## Sprint Plan

### Sprint 1: ETL Core
- Build raw data generator.
- Build transform logic with validation and rejection reasons.
- Save clean/rejected/statistical outputs to files.

### Sprint 2: Database Integration
- Create SQL schema.
- Load ETL outputs into PostgreSQL tables.
- Validate table contents in pgAdmin.

### Sprint 3: Streaming and API
- Publish top-5 expensive products to Kafka.
- Consume Kafka events into PostgreSQL.
- Expose data through FastAPI endpoints.

## Done Definition
- `scripts/run_all.py` works without manual data edits.
- PostgreSQL tables are populated as expected.
- API endpoints return correct data format.
- Documentation is clear enough for another student to run.
