import os
from pathlib import Path

import psycopg


def get_db_config() -> dict[str, str]:
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "55432"),
        "dbname": os.getenv("POSTGRES_DB", "etl_db"),
        "user": os.getenv("POSTGRES_USER", "etl_user"),
        "password": os.getenv("POSTGRES_PASSWORD", "etl_password"),
    }


def get_connection() -> psycopg.Connection:
    return psycopg.connect(**get_db_config())


def run_sql_file(conn: psycopg.Connection, sql_path: Path) -> None:
    script = sql_path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(script)
    conn.commit()
