CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS staging.products_clean (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    inventory_value NUMERIC(12, 2) NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS staging.products_rejected (
    rejected_id BIGSERIAL PRIMARY KEY,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price TEXT,
    quantity TEXT,
    rejection_reason TEXT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.category_summary (
    category TEXT PRIMARY KEY,
    products_count INTEGER NOT NULL,
    total_quantity INTEGER NOT NULL,
    average_price NUMERIC(10, 2) NOT NULL,
    total_inventory_value NUMERIC(12, 2) NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.top_expensive_stream (
    event_id TEXT PRIMARY KEY,
    event_type TEXT NOT NULL,
    emitted_at TIMESTAMPTZ NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    brand TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    consumed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
