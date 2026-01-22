from dagster import op, job
import subprocess
import sys

@op
def ingest_raw():
    subprocess.check_call([sys.executable, "ingestion/ingest_coingecko_prices.py"])

@op
def apply_sql():
    subprocess.check_call([sys.executable, "warehouse/apply_sql.py"])

@job
def crypto_mvp_job():
    # Firstly we ingest data and then we apply the transformations (views)
    ingest_raw()
    apply_sql()
