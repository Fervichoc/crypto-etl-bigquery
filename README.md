# 📊 Crypto Data ELT MVP

## Overview

This project is a **minimal end-to-end ELT pipeline** designed to demonstrate how external financial data can be ingested, transformed, and exposed for analytics using production-style practices.

The goal is to showcase:
- clear data layering (RAW → STAGING → MART)
- version-controlled SQL
- orchestration with a modern data orchestrator

The implementation closely mirrors a real-world **analytics engineering** workflow.

---

## Architecture

```
┌──────────────────────────┐
│  External API (CoinGecko)│
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Python Ingestion (ELT)   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ BigQuery RAW Tables      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ BigQuery STAGING Views   │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ BigQuery MART Views      │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────┐
│ Analytics / BI           │
└──────────────────────────┘
```


---

## Data Layers

### RAW

- Stored directly in **:contentReference[oaicite:0]{index=0}**
- Data is persisted **as received**, with minimal processing
- Acts as an immutable source of truth for auditing and replay

Example:
- `raw_coingecko_prices`

---

### STAGING

- Implemented as SQL **views**
- Responsible for:
  - type casting
  - timestamp normalization
  - basic data cleanup
- Contains **no business logic**

Example:
- `stg_coingecko_prices`

---

### MART

- Business-facing analytics layer
- Contains derived metrics and aggregations
- Designed to be consumed directly by BI tools or analysts

Example:
- `mart_daily_prices`
  - daily close prices
  - previous close
  - daily returns (window functions)

---

## Orchestration

The pipeline is orchestrated using **:contentReference[oaicite:1]{index=1}**.

### Pipeline steps
1. **Ingest RAW data**  
   - Fetches data from the **:contentReference[oaicite:2]{index=2}** API  
   - Loads it into BigQuery RAW tables

2. **Apply SQL transformations**  
   - Executes versioned SQL files
   - Creates or updates STAGING and MART views in BigQuery

Both steps are executed sequentially as part of a single Dagster job.

---

## Scheduling (Design Only)

In a production setup, this pipeline would be executed **once per day** using a Dagster schedule.

> ⚠️ The schedule is documented here for design completeness but is not deployed as part of this MVP.

Example:

```python
from dagster import schedule

@schedule(cron_schedule="0 22 * * *", job=crypto_mvp_job)
def daily_crypto_pipeline():
    return {}
```


## This ensures:

- daily data refresh

- reproducible execution

- no manual intervention

## Tech Stack

- Python (API ingestion, orchestration)

- BigQuery (data warehouse)

- SQL (analytics modeling)

- Dagster (orchestration)

- Git (version control)

## How to Run (Local)

Activate virtual environment

Start Dagster:

dagster dev -f orchestration/dagster_job.py


Run the job from the Dagster UI

## Notes

This project is intentionally scoped as an MVP:

- focuses on clarity over complexity

- prioritizes production-style structure

- avoids over-engineering