"""FastAPI app for reading ETL outputs from PostgreSQL."""

from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row


DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "55432"),
    "dbname": os.getenv("POSTGRES_DB", "etl_db"),
    "user": os.getenv("POSTGRES_USER", "etl_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "etl_password"),
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
    yield
    app.state.conn.close()


app = FastAPI(title="ETL API", lifespan=lifespan)


def normalized_limit(value: int, default: int = 20, max_limit: int = 200) -> int:
    """Keep API query limits in a sensible range."""
    if value <= 0:
        return default
    return min(value, max_limit)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products")
def list_products(limit: int = 20) -> list[dict]:
    safe_limit = normalized_limit(limit)
    with app.state.conn.cursor() as cur:
        cur.execute(
            """
            SELECT product_id, product_name, category, brand, price, quantity, inventory_value
            FROM staging.products_clean
            ORDER BY inventory_value DESC
            LIMIT %s
            """,
            (safe_limit,),
        )
        return cur.fetchall()


@app.get("/stats/categories")
def category_stats() -> list[dict]:
    with app.state.conn.cursor() as cur:
        cur.execute(
            """
            SELECT category, products_count, total_quantity, average_price, total_inventory_value
            FROM analytics.category_summary
            ORDER BY total_inventory_value DESC
            """
        )
        return cur.fetchall()


@app.get("/stream/top-expensive")
def top_expensive_stream(limit: int = 20) -> list[dict]:
    safe_limit = normalized_limit(limit)
    with app.state.conn.cursor() as cur:
        cur.execute(
            """
            SELECT event_id, emitted_at, product_id, product_name, category, brand, price, quantity, consumed_at
            FROM analytics.top_expensive_stream
            ORDER BY consumed_at DESC
            LIMIT %s
            """,
            (safe_limit,),
        )
        return cur.fetchall()
