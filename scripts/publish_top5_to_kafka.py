"""Publish top 5 expensive products to Kafka."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import uuid

import pandas as pd
from kafka import KafkaProducer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from schema.product import ProductSchema, TopProductEvent


TOP5_FILE = "data/processed/top_5_expensive.csv"
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "products.top5")


def main() -> None:
    df = pd.read_csv(TOP5_FILE)

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        value_serializer=lambda payload: json.dumps(payload).encode("utf-8"),
    )

    sent = 0
    for row in df.to_dict(orient="records"):
        payload = ProductSchema(
            product_id=int(row["product_id"]),
            product_name=str(row["product_name"]),
            category=str(row["category"]),
            brand=str(row["brand"]),
            price=float(row["price"]),
            quantity=int(row["quantity"]),
        )
        event = TopProductEvent(
            event_id=str(uuid.uuid4()),
            emitted_at=datetime.now(timezone.utc),
            payload=payload,
        )
        producer.send(KAFKA_TOPIC, value=event.model_dump(mode="json"))
        sent += 1

    producer.flush()
    producer.close()

    print(f"[ok] Sent {sent} events to Kafka topic '{KAFKA_TOPIC}' on {KAFKA_BOOTSTRAP}")


if __name__ == "__main__":
    main()
