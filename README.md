📊 Crypto Data ELT MVP
Overview

This project is a minimal end-to-end ELT pipeline built to demonstrate how external financial data can be ingested, transformed, and exposed for analytics in a production-style setup.

The pipeline is designed with clear data layers, version-controlled SQL, and orchestration, closely mirroring a real analytics engineering workflow.

Architecture
External API (CoinGecko)
        |
        v
Python Ingestion (ELT)
        |
        v
BigQuery RAW tables
        |
        v
BigQuery STAGING views
        |
        v
BigQuery MART views
        |
        v
Analytics / BI

Data Layers
RAW

Stored directly in BigQuery

Data is persisted as received, with minimal normalization

Acts as an immutable source of truth

Example:

raw_coingecko_prices

STAGING

SQL views

Type casting and basic normalization

No business logic

Example:

stg_coingecko_prices

MART

Business-facing analytics layer

Contains derived metrics (e.g. daily close prices, returns)

Designed to be consumed directly by BI tools or analysts

Example:

mart_daily_prices

Orchestration

The pipeline is orchestrated using Dagster:

ingest_raw → ingests external API data into BigQuery

apply_sql → applies staging and mart SQL definitions

Executed sequentially as a single job

The job can be run locally via the Dagster UI.

Scheduling (Design Only)

In a production environment, this pipeline would be executed once per day using a Dagster schedule.

Example (not deployed in this MVP):

from dagster import schedule

@schedule(cron_schedule="0 22 * * *", job=crypto_mvp_job)
def daily_crypto_pipeline():
    return {}


This ensures:

daily data refresh

reproducible execution

no manual intervention

Tech Stack

Python (API ingestion, orchestration)

BigQuery (data warehouse)

SQL (analytics modeling)

Dagster (orchestration)

Git (version control)

How to Run (Local)

Activate virtual environment

Start Dagster:

dagster dev -f orchestration/dagster_job.py


Run the job from the Dagster UI

Notes

This project is intentionally scoped as an MVP:

focuses on clarity over complexity

prioritizes production-style structure

avoids over-engineering