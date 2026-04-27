"""Generate a raw CSV with some intentional dirty rows."""

from pathlib import Path
import random

import pandas as pd


RAW_DIR = Path("data/raw")
RAW_FILE = RAW_DIR / "products_dirty.csv"


def build_rows(total_rows: int = 60) -> list[dict[str, object]]:
    random.seed(42)

    categories = ["Electronics", "Sports", "Home", "Beauty", "Fashion"]
    brands = ["Nova", "Peak", "Urban", "Astra", "Pulse"]

    rows: list[dict[str, object]] = []
    for i in range(1, total_rows + 1):
        rows.append(
            {
                "product_id": i,
                "product_name": f"Product {i}",
                "category": random.choice(categories),
                "brand": random.choice(brands),
                "price": round(random.uniform(5, 200), 2),
                "quantity": random.randint(0, 25),
            }
        )

    # Add dirty rows to make transform step meaningful.
    rows.extend(
        [
            {
                "product_id": "x-101",
                "product_name": "Broken Id",
                "category": "Sports",
                "brand": "Peak",
                "price": 40.0,
                "quantity": 2,
            },
            {
                "product_id": 9991,
                "product_name": "Negative Price",
                "category": "Electronics",
                "brand": "Nova",
                "price": -20,
                "quantity": 4,
            },
            {
                "product_id": 9992,
                "product_name": "No Quantity",
                "category": "Home",
                "brand": "Urban",
                "price": 55,
                "quantity": "",
            },
            {
                "product_id": 9993,
                "product_name": "",
                "category": "Beauty",
                "brand": "Astra",
                "price": 30,
                "quantity": 3,
            },
            {
                "product_id": 9994,
                "product_name": "No Category",
                "category": "",
                "brand": "Pulse",
                "price": 15,
                "quantity": 7,
            },
        ]
    )
    return rows


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(build_rows())
    df.to_csv(RAW_FILE, index=False)
    print(f"[ok] Raw CSV generated: {RAW_FILE} ({len(df)} rows)")


if __name__ == "__main__":
    main()
