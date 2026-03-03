import os
from datetime import datetime, timezone
from pathlib import Path

import requests
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.raw_coingecko_prices"

COINS = ["bitcoin", "ethereum", "solana"]
VS_CURRENCIES = ["usd", "chf"]

def already_ingested_today(client: bigquery.Client, ingestion_date: str) -> bool:
    q = f"""
    SELECT 1
    FROM `{TABLE_ID}`
    WHERE ingestion_date = @ingestion_date
    LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("ingestion_date", "STRING", ingestion_date)]
    )
    rows = list(client.query(q, job_config=job_config).result())
    return len(rows) > 0

def main():
    now = datetime.now(timezone.utc)
    today = now.date().isoformat()

    client = bigquery.Client(project=PROJECT_ID)

    # Idempotency by day: ingest at most once per ingestion_date
    if already_ingested_today(client, today):
        print(f"Already ingested for {today}. Nothing to do.")
        return

    r = requests.get(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": ",".join(COINS),
            "vs_currencies": ",".join(VS_CURRENCIES),
            "include_last_updated_at": "true",
        },
        timeout=20,
    )
    r.raise_for_status()
    payload = r.json()

    rows = []
    for coin, values in payload.items():
        source_ts = datetime.fromtimestamp(values["last_updated_at"], tz=timezone.utc)
        for ccy in VS_CURRENCIES:
            rows.append(
                {
                    "coin_id": coin,
                    "vs_currency": ccy,
                    "price": float(values[ccy]),
                    "source_timestamp_utc": source_ts.isoformat(),
                    "ingestion_timestamp_utc": now.isoformat(),
                    "ingestion_date": today,
                }
            )

    df = pd.DataFrame(rows)

    client.load_table_from_dataframe(
        df,
        TABLE_ID,
        job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"),
    ).result()

    print(f"Loaded {len(df)} rows into {TABLE_ID} for ingestion_date={today}")

if __name__ == "__main__":
    main()