# EDA Steps

## Goal
Check data quality before loading to PostgreSQL.

## Step 1: Generate Raw Data
```bash
python3 scripts/generate_dirty_csv.py
```

Output: `data/raw/products_dirty.csv`

## Step 2: Transform and Validate
```bash
python3 scripts/transform.py
```

What happens:
- required column check
- type conversion for `product_id`, `price`, `quantity`
- invalid-row tagging with `rejection_reason`
- clean/rejected split
- category-level aggregation
- top-5 expensive extraction

## Step 3: Inspect EDA Outputs
- `data/processed/eda_summary.json`
- `data/processed/category_summary.csv`
- `data/processed/top_5_expensive.csv`

## Key Values to Comment On
- `rows_raw`
- `rows_clean`
- `rows_rejected`
- `rejection_rate_percent`
- clean price min/max/mean
- categories with highest inventory value

## Example Interpretation
- High rejection rate means low source quality.
- One dominant category means concentration risk.
- If max price is much higher than mean, prices are right-skewed.
