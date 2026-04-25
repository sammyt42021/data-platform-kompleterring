from pathlib import Path
import json

import pandas as pd


RAW_FILE = Path("data/raw/products_dirty.csv")
CLEAN_FILE = Path("data/processed/products_clean.csv")
REJECTED_FILE = Path("data/processed/products_rejected.csv")
CATEGORY_SUMMARY_FILE = Path("data/processed/category_summary.csv")
TOP5_FILE = Path("data/processed/top_5_expensive.csv")
EDA_FILE = Path("data/processed/eda_summary.json")


REQUIRED_COLUMNS = ["product_id", "product_name", "category", "brand", "price", "quantity"]


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def collect_rejection_reasons(row: pd.Series) -> str:
    row_reasons: list[str] = []
    if pd.isna(row["product_id_num"]) or row["product_id_num"] <= 0:
        row_reasons.append("invalid_product_id")
    if row["product_name"] == "":
        row_reasons.append("empty_product_name")
    if row["category"] == "":
        row_reasons.append("empty_category")
    if row["brand"] == "":
        row_reasons.append("empty_brand")
    if pd.isna(row["price_num"]) or row["price_num"] <= 0:
        row_reasons.append("invalid_price")
    if pd.isna(row["quantity_num"]) or row["quantity_num"] < 0:
        row_reasons.append("invalid_quantity")
    return "|".join(row_reasons)


def validate_and_split(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    working_df = df.copy()

    # Basic normalize first.
    for col in ["product_name", "category", "brand"]:
        working_df[col] = working_df[col].apply(normalize_text)

    working_df["product_id_num"] = pd.to_numeric(working_df["product_id"], errors="coerce")
    working_df["price_num"] = pd.to_numeric(working_df["price"], errors="coerce")
    working_df["quantity_num"] = pd.to_numeric(working_df["quantity"], errors="coerce")

    working_df["rejection_reason"] = [
        collect_rejection_reasons(row) for _, row in working_df.iterrows()
    ]
    rejected = working_df[working_df["rejection_reason"] != ""].copy()
    clean = working_df[working_df["rejection_reason"] == ""].copy()

    clean = clean.assign(
        product_id=clean["product_id_num"].astype(int),
        price=clean["price_num"].round(2),
        quantity=clean["quantity_num"].astype(int),
    )
    clean["inventory_value"] = (clean["price"] * clean["quantity"]).round(2)

    clean = clean[
        ["product_id", "product_name", "category", "brand", "price", "quantity", "inventory_value"]
    ].sort_values(by="inventory_value", ascending=False)

    rejected = rejected[
        ["product_id", "product_name", "category", "brand", "price", "quantity", "rejection_reason"]
    ]

    return clean, rejected


def build_category_summary(clean_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        clean_df.groupby("category", as_index=False)
        .agg(
            products_count=("product_id", "count"),
            total_quantity=("quantity", "sum"),
            average_price=("price", "mean"),
            total_inventory_value=("inventory_value", "sum"),
        )
        .sort_values("total_inventory_value", ascending=False)
    )

    summary["average_price"] = summary["average_price"].round(2)
    summary["total_inventory_value"] = summary["total_inventory_value"].round(2)
    return summary


def build_eda_summary(raw_df: pd.DataFrame, clean_df: pd.DataFrame, rejected_df: pd.DataFrame) -> dict[str, object]:
    return {
        "rows_raw": int(len(raw_df)),
        "rows_clean": int(len(clean_df)),
        "rows_rejected": int(len(rejected_df)),
        "rejection_rate_percent": round((len(rejected_df) / len(raw_df)) * 100, 2) if len(raw_df) else 0.0,
        "price_stats_clean": {
            "min": float(clean_df["price"].min()) if len(clean_df) else 0.0,
            "max": float(clean_df["price"].max()) if len(clean_df) else 0.0,
            "mean": round(float(clean_df["price"].mean()), 2) if len(clean_df) else 0.0,
        },
        "top_categories_by_inventory_value": clean_df.groupby("category")["inventory_value"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .round(2)
        .to_dict(),
    }


def main() -> None:
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw file not found: {RAW_FILE}. Run `python scripts/generate_dirty_csv.py` first."
        )

    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(RAW_FILE)
    missing = [c for c in REQUIRED_COLUMNS if c not in raw_df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    clean_df, rejected_df = validate_and_split(raw_df)
    category_summary = build_category_summary(clean_df)
    top5 = clean_df.sort_values(by="price", ascending=False).head(5)
    eda_summary = build_eda_summary(raw_df, clean_df, rejected_df)

    clean_df.to_csv(CLEAN_FILE, index=False)
    rejected_df.to_csv(REJECTED_FILE, index=False)
    category_summary.to_csv(CATEGORY_SUMMARY_FILE, index=False)
    top5.to_csv(TOP5_FILE, index=False)
    EDA_FILE.write_text(json.dumps(eda_summary, indent=2), encoding="utf-8")

    print(f"[ok] Clean rows: {len(clean_df)} -> {CLEAN_FILE}")
    print(f"[ok] Rejected rows: {len(rejected_df)} -> {REJECTED_FILE}")
    print(f"[ok] Category summary -> {CATEGORY_SUMMARY_FILE}")
    print(f"[ok] Top 5 expensive -> {TOP5_FILE}")
    print(f"[ok] EDA summary -> {EDA_FILE}")


if __name__ == "__main__":
    main()
