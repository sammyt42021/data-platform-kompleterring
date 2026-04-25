import pandas as pd

from scripts.transform import build_category_summary, validate_and_split


def test_validate_and_split() -> None:
    df = pd.DataFrame(
        [
            {
                "product_id": 1,
                "product_name": "A",
                "category": "Sports",
                "brand": "Peak",
                "price": 20,
                "quantity": 2,
            },
            {
                "product_id": "bad",
                "product_name": "B",
                "category": "Sports",
                "brand": "Peak",
                "price": 20,
                "quantity": 2,
            },
        ]
    )

    clean, rejected = validate_and_split(df)

    assert len(clean) == 1
    assert len(rejected) == 1
    assert clean.iloc[0]["inventory_value"] == 40


def test_category_summary() -> None:
    clean_df = pd.DataFrame(
        [
            {
                "product_id": 1,
                "product_name": "A",
                "category": "Sports",
                "brand": "Peak",
                "price": 20,
                "quantity": 2,
                "inventory_value": 40,
            },
            {
                "product_id": 2,
                "product_name": "B",
                "category": "Sports",
                "brand": "Nova",
                "price": 10,
                "quantity": 1,
                "inventory_value": 10,
            },
        ]
    )

    summary = build_category_summary(clean_df)
    row = summary.iloc[0]

    assert row["category"] == "Sports"
    assert row["products_count"] == 2
    assert row["total_quantity"] == 3
