# Crypto Finance Data MVP

This repository contains a **data engineering & analytics MVP** focused on ingesting cryptocurrency market data and producing **analytics-ready data marts** using modern, production-oriented practices.

The project demonstrates:
- clean separation between ingestion, orchestration, and analytics
- SQL-based business logic managed as code
- explicit data quality validation
- auditable and reproducible transformations

---

## High-Level Architecture



```
External APIs
↓
Python ingestion
↓
Dagster (orchestration)
↓
BigQuery (raw & staging)
↓
SQLMesh models
↓
Analytics-ready data marts
```

---

## Orchestration (Dagster)

All workflows are orchestrated using **Dagster**, which acts as the single entrypoint for the pipeline.

Dagster is responsible for:
- triggering daily ingestion jobs
- enforcing execution order (ingestion → analytics)
- running SQLMesh deployments non-interactively
- surfacing logs and failures in a single UI

The pipeline is defined as a Dagster job and can be executed manually or scheduled.

---

## Ingestion & Staging

- Data is ingested from external APIs using **Python**.
- Ingestion writes raw data into **BigQuery raw tables**.
- Staging logic (type casting, timestamp normalization) is implemented as **SQLMesh staging models**.

Responsibilities of this layer:
- extract data
- normalize types
- prepare clean staging datasets for analytics

---

## Analytics Engineering with SQLMesh

All analytics logic is managed using **SQLMesh**, treating SQL transformations as production code.

### Models

- Each analytics table or view is defined as a **SQLMesh model**.
- Models encapsulate business logic such as:
  - deduplication
  - window functions
  - derived metrics

Example:
- `stg_coingecko_prices`: normalized staging view
- `dm_daily_prices`: daily close prices with daily returns

### Audits

- **SQLMesh audits** are used to enforce data quality rules.
- Audits are SQL queries that return invalid rows.
- If an audit returns rows, it fails.

Typical checks:
- non-null critical fields
- uniqueness constraints
- valid numeric ranges

### State & History

- SQLMesh automatically tracks:
  - model versions
  - applied plans
  - deployment metadata
- State is persisted in a dedicated **BigQuery dataset**.
- Changes are reviewed before execution via `sqlmesh plan`.

---

## Repository Structure

```
├── ingestion/ # Python ingestion scripts
│
├── warehouse/
│ └── raw/ # raw BigQuery tables
│
├── orchestration/
│ └── dagster_job.py # Dagster job definition
│
├── sqlmesh/
│ ├── models/ # SQLMesh models (staging + marts)
│ ├── audits/ # SQLMesh audits
│ └── .cache/ # local SQLMesh cache (ignored)
│
├── config.yaml # SQLMesh configuration (no secrets)
├── README.md
└── .gitignore
```

---

## Configuration

SQLMesh is configured via `config.yaml`, which is versioned as infrastructure code.

Key points:
- BigQuery is used as the execution engine
- SQL dialect is explicitly set to BigQuery
- No credentials are stored in the repository

Authentication is handled via environment variables
(e.g. `GOOGLE_APPLICATION_CREDENTIALS`).

---

## Workflow

### Orchestrated execution (recommended)

Dagster runs the full pipeline:

1. Ingest raw data into BigQuery
2. Execute SQLMesh deployment
3. Validate data quality

Internally, Dagster executes:

```bash
sqlmesh plan --auto-apply
sqlmesh audit
```

plan --auto-apply:

- computes the deployment plan

- applies changes non-interactively (required for orchestration)

audit:

- validates data quality after materialization

## Current Scope

- Single environment (no dev/prod separation yet)

- Daily execution via Dagster

- SQLMesh-managed staging and analytics layers

- Designed to be easily extended with environments and scheduling

## Key Takeaway

This MVP demonstrates how to:

- orchestrate data pipelines using Dagster

- manage SQL-based analytics with SQLMesh

- treat transformations as auditable, versioned code

- enforce data quality explicitly

- build reliable reporting foundations on BigQuery