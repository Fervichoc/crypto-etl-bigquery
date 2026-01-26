import os
from pathlib import Path
from google.cloud import bigquery
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")

def run_sql_file(sql_path: Path) -> None:
    sql = sql_path.read_text(encoding="utf-8")
    client = bigquery.Client(project=PROJECT_ID)
    client.query(sql).result()
    print(f"Applied: {sql_path}")

def main():
    root = Path(__file__).resolve().parents[0]
    # Ejecuta staging primero, luego marts
    run_sql_file(root / "staging" / "stg_coingecko_prices.sql")
    run_sql_file(root / "marts" / "mart_daily_prices.sql")

if __name__ == "__main__":
    main()
