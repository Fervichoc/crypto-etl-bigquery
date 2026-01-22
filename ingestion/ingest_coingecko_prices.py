import os
from datetime import datetime, timezone
from pathlib import Path

import requests
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Cargar .env desde la raíz
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.raw_coingecko_prices"

COINS = ["bitcoin", "ethereum", "solana"]
VS_CURRENCIES = ["usd", "chf"]

def main():
    now = datetime.now(timezone.utc)

    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": ",".join(COINS),
            "vs_currencies": ",".join(VS_CURRENCIES),
            "include_last_updated_at": "true"
        },
        timeout=20
    )
    r.raise_for_status()
    payload = r.json()

    rows = []
    for coin, values in payload.items():
        source_ts = datetime.fromtimestamp(values["last_updated_at"], tz=timezone.utc)
        for ccy in VS_CURRENCIES:
            rows.append({
                "coin_id": coin,
                "vs_currency": ccy,
                "price": float(values[ccy]),
                "source_timestamp_utc": source_ts.isoformat(),
                "ingestion_timestamp_utc": now.isoformat(),
                "ingestion_date": now.date().isoformat()
            })

    df = pd.DataFrame(rows)

    client = bigquery.Client(project=PROJECT_ID)
    client.load_table_from_dataframe(
        df,
        TABLE_ID,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    ).result()

    print(f"Loaded {len(df)} rows into {TABLE_ID}")

if __name__ == "__main__":
    main()
