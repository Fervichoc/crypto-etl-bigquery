# Crypto Finance Data MVP

This repository contains a data engineering & analytics MVP focused on ingesting cryptocurrency market data and producing analytics-ready data marts using modern, production-oriented practices.

The goal of the project is to demonstrate:

clean separation between ingestion and analytics

SQL-based business logic

data quality validation

auditable and reproducible transformations
## Architecture

```
External APIs
     ↓
Python Ingestion
     ↓
BigQuery (staging tables)
     ↓
SQLMesh models
     ↓
Analytics-ready data marts
```

---

## Ingestion & Staging

- Data is ingested from external APIs using **Python**.
- Raw data is written into **BigQuery staging tables**.
- Staging tables are intentionally kept close to the source structure, with minimal transformations.

This layer is responsible only for:
- data extraction
- basic typing / normalization
- reliable loading into BigQuery

---

## Analytics Engineering with SQLMesh

All analytics logic is managed using **SQLMesh**, treating SQL transformations as production code.

### Models

- Data marts are defined as **SQLMesh models**.
- Each model represents a business-ready table or view.
- Models encapsulate all business logic (deduplication, aggregations, window functions, derived metrics).

Example:
- `dm_daily_prices`: daily close prices per asset and currency, including derived daily returns.

### Audits

- **SQLMesh audits** are used to enforce data quality rules.
- Audits express invalid data conditions in SQL (e.g. nulls, duplicates, invalid values).
- An audit fails if it returns rows.

Typical checks include:
- non-null critical fields
- uniqueness constraints
- valid numeric ranges

### State & History

- SQLMesh automatically manages:
  - model versions
  - applied plans
  - deployment metadata
- State is persisted in a dedicated **BigQuery dataset**.
- Changes are reviewed via `sqlmesh plan` before execution.

---

---

## Configuration

SQLMesh is configured via `config.yaml`, which is versioned as infrastructure code.

Key points:
- BigQuery is used as the execution engine.
- SQL dialect is explicitly set to BigQuery.
- No credentials are stored in the repository.

Authentication is handled externally via environment variables
(e.g. `GOOGLE_APPLICATION_CREDENTIALS`).

---

## Workflow

Typical local workflow:

```bash
sqlmesh plan
sqlmesh apply
sqlmesh audit
```

- plan shows the impact of changes before execution

- apply materializes or updates models

- audit validates data quality explicitly

This ensures transformations are reviewed, reproducible, and auditable.

##Current Scope

- Single environment (no dev/prod separation yet)

- Focus on correctness, clarity, and production-ready patterns

- Designed to be easily extended with multiple environments and orchestration

Key Takeaway

This MVP demonstrates how to:

- separate ingestion from analytics

- manage SQL transformations as code

- enforce data quality at the analytics layer

- build reliable reporting foundations on BigQuery