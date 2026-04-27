"""Kafka consumer: save top expensive product events into PostgreSQL."""

import json
import os
from pathlib import Path
import sys

from kafka import KafkaConsumer

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.db_utils import get_connection, run_sql_file


KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "products.top5")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "products-top5-consumer")
SCHEMA_FILE = "sql/01_create_tables.sql"


def save_event(conn, event: dict[str, object]) -> None:
    payload = event["payload"]
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO analytics.top_expensive_stream
            (event_id, event_type, emitted_at, product_id, product_name, category, brand, price, quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (event_id) DO NOTHING
            """,
            (
                event["event_id"],
                event["event_type"],
                event["emitted_at"],
                int(payload["product_id"]),
                str(payload["product_name"]),
                str(payload["category"]),
                str(payload["brand"]),
                float(payload["price"]),
                int(payload["quantity"]),
            ),
        )
    conn.commit()


def main() -> None:
    with get_connection() as conn:
        run_sql_file(conn, Path(SCHEMA_FILE))

        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            group_id=GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

        print(f"[listen] topic={KAFKA_TOPIC} bootstrap={KAFKA_BOOTSTRAP}")
        try:
            for message in consumer:
                event = message.value
                save_event(conn, event)
                print(f"[saved] event_id={event['event_id']} product={event['payload']['product_name']}")
        except KeyboardInterrupt:
            print("\n[stop] Consumer stopped by user.")
        finally:
            consumer.close()


if __name__ == "__main__":
    main()
