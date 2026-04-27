# Commit Walkthrough (11 Steps)

This file explains what each commit should contain and why.
Use it as a checklist when rebuilding in the GitHub-connected folder.

## Commit 1 - Project Scaffold
Files:
- `app/__init__.py`
- `consumer/__init__.py`
- `schema/__init__.py`
- `scripts/__init__.py`
- `data/raw/.gitkeep`
- `data/processed/.gitkeep`

Why:
- Creates clean package structure and keeps empty data folders tracked by Git.

## Commit 2 - Environment and Infrastructure
Files:
- `.gitignore`
- `.env.example`
- `requirements.txt`
- `pyproject.toml`
- `docker-compose.yml`

Why:
- Defines dependencies and local services (PostgreSQL, pgAdmin, Kafka, Zookeeper).

## Commit 3 - Domain Schema
Files:
- `schema/product.py`

Why:
- Adds typed models for cleaned products and Kafka events.

## Commit 4 - Raw Data Generator
Files:
- `scripts/generate_dirty_csv.py`
- `data/products_100.csv`

Why:
- Makes the project independent by generating sample data with controlled dirty rows.

## Commit 5 - Transform and Unit Tests
Files:
- `scripts/transform.py`
- `tests/conftest.py`
- `tests/test_transform.py`

Why:
- Core cleaning and EDA logic.
- Tests verify split and summary behavior.

## Commit 6 - SQL and DB Helpers
Files:
- `sql/01_create_tables.sql`
- `scripts/db_utils.py`

Why:
- Defines schemas/tables and shared DB connection utilities.

## Commit 7 - Load Step and End-to-End Runner
Files:
- `scripts/load_products.py`
- `scripts/run_all.py`

Why:
- Loads transformed outputs to PostgreSQL.
- Provides one command for the ETL batch flow.

## Commit 8 - Kafka Producer
Files:
- `scripts/publish_top5_to_kafka.py`

Why:
- Sends top expensive products as JSON events to Kafka.

## Commit 9 - Kafka Consumer
Files:
- `consumer/db_consumer.py`

Why:
- Reads events from Kafka and stores them in PostgreSQL.

## Commit 10 - API Layer
Files:
- `app/main.py`

Why:
- Exposes health, products, category stats, and stream queries.

## Commit 11 - Documentation and Final Notes
Files:
- `README.md`
- `docs/assignment_notes.md`
- `documentation/1_user_stories.md`
- `documentation/2_mvp_and_sprints.md`
- `documentation/3_reflection_agile.md`
- `documentation/4_eda_steps.md`
- `documentation/5_pgadmin_guide.md`
- `documentation/6_commit_walkthrough.md`
- `documentation/7_viva_prep.md`

Why:
- Makes the project explainable and auditable for review.
