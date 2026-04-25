"""Run the full beginner ETL flow in one command."""

import subprocess
import sys


STEPS = [
    [sys.executable, "scripts/generate_dirty_csv.py"],
    [sys.executable, "scripts/transform.py"],
    [sys.executable, "scripts/load_products.py"],
]


def main() -> None:
    total_steps = len(STEPS)
    for index, step in enumerate(STEPS, start=1):
        print(f"[run {index}/{total_steps}] {' '.join(step)}")
        subprocess.run(step, check=True)

    print("[done] ETL completed: raw -> clean/rejected + EDA -> postgres")
    print("[next] Optional Kafka producer: python3 scripts/publish_top5_to_kafka.py")
    print("[next] Optional Kafka consumer: python3 consumer/db_consumer.py")


if __name__ == "__main__":
    main()
