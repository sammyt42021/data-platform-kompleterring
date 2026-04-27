"""Run the full ETL flow in one command."""

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
    print("[next] Optional: validate Kafka with docker compose CLI smoke-test commands")


if __name__ == "__main__":
    main()
