"""Load ETL outputs into PostgreSQL tables."""

from pathlib import Path

import pandas as pd

from db_utils import get_connection, run_sql_file


CLEAN_FILE = Path("data/processed/products_clean.csv")
REJECTED_FILE = Path("data/processed/products_rejected.csv")
CATEGORY_SUMMARY_FILE = Path("data/processed/category_summary.csv")
SCHEMA_FILE = Path("sql/01_create_tables.sql")


def load_clean_products(conn, df: pd.DataFrame) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE staging.products_clean")
        for row in df.to_dict(orient="records"):
            cur.execute(
                """
                INSERT INTO staging.products_clean
                (product_id, product_name, category, brand, price, quantity, inventory_value)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_id)
                DO UPDATE SET
                    product_name = EXCLUDED.product_name,
                    category = EXCLUDED.category,
                    brand = EXCLUDED.brand,
                    price = EXCLUDED.price,
                    quantity = EXCLUDED.quantity,
                    inventory_value = EXCLUDED.inventory_value,
                    loaded_at = NOW()
                """,
                (
                    row["product_id"],
                    row["product_name"],
                    row["category"],
                    row["brand"],
                    row["price"],
                    row["quantity"],
                    row["inventory_value"],
                ),
            )
    conn.commit()


def load_rejected_rows(conn, df: pd.DataFrame) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE staging.products_rejected")
        for row in df.to_dict(orient="records"):
            cur.execute(
                """
                INSERT INTO staging.products_rejected
                (product_id, product_name, category, brand, price, quantity, rejection_reason)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    str(row.get("product_id", "")),
                    str(row.get("product_name", "")),
                    str(row.get("category", "")),
                    str(row.get("brand", "")),
                    str(row.get("price", "")),
                    str(row.get("quantity", "")),
                    str(row.get("rejection_reason", "")),
                ),
            )
    conn.commit()


def load_category_summary(conn, df: pd.DataFrame) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE analytics.category_summary")
        for row in df.to_dict(orient="records"):
            cur.execute(
                """
                INSERT INTO analytics.category_summary
                (category, products_count, total_quantity, average_price, total_inventory_value)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (category)
                DO UPDATE SET
                    products_count = EXCLUDED.products_count,
                    total_quantity = EXCLUDED.total_quantity,
                    average_price = EXCLUDED.average_price,
                    total_inventory_value = EXCLUDED.total_inventory_value,
                    loaded_at = NOW()
                """,
                (
                    row["category"],
                    int(row["products_count"]),
                    int(row["total_quantity"]),
                    float(row["average_price"]),
                    float(row["total_inventory_value"]),
                ),
            )
    conn.commit()


def main() -> None:
    if not CLEAN_FILE.exists() or not REJECTED_FILE.exists() or not CATEGORY_SUMMARY_FILE.exists():
        raise FileNotFoundError(
            "Processed files missing. Run `python scripts/transform.py` first."
        )

    clean_df = pd.read_csv(CLEAN_FILE)
    rejected_df = pd.read_csv(REJECTED_FILE)
    summary_df = pd.read_csv(CATEGORY_SUMMARY_FILE)

    with get_connection() as conn:
        run_sql_file(conn, SCHEMA_FILE)
        load_clean_products(conn, clean_df)
        load_rejected_rows(conn, rejected_df)
        load_category_summary(conn, summary_df)

    print(f"[ok] Loaded clean rows: {len(clean_df)}")
    print(f"[ok] Loaded rejected rows: {len(rejected_df)}")
    print(f"[ok] Loaded category summary rows: {len(summary_df)}")


if __name__ == "__main__":
    main()
