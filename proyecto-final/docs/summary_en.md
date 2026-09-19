# NYC TLC Data Pipeline — Project Summary

**Author:** Alan Miguel Crispín Rivera
**Context:** Individual capstone project ("Proyecto Integrador") for the Xideral capacitation.

---

## Overview

An end-to-end, AWS-based data pipeline for New York City's TLC (Taxi & Limousine
Commission) trip records. It covers all four trip types the TLC publishes —
`yellow`, `green`, `fhv` (for-hire vehicle), and `fhvhv` (high-volume for-hire
vehicle) — from raw ingestion to an interactive dashboard, using a medallion
(Bronze → Silver → Gold) architecture.

## Architecture

```
NYC TLC (public data)
        │
        ▼
   raw_data/     <- Bronze: raw parquet, as published by the TLC
        │  (notebook 03 - PySpark: cleaning, typing, derived columns, sentinel value)
        ▼
   clean_data/   <- Silver: 4 taxi types, normalized schema
        │  (notebook 04 - PySpark: incremental joins/aggregations per type)
        ▼
   gold_data/    <- Gold: 7 aggregated KPI results
        │  (notebooks 05 + 06 - pandas/boto3, no Spark)
        ▼
   RDS (MySQL)   <- gold_* tables + metadata + pipeline run log
        │
        ▼
   Streamlit Dashboard  <- 5 tabs, 8 charts
```

All raw, cleaned, and aggregated data lives in S3. RDS is used **only** for the
final aggregates (hundreds/thousands of rows) and control metadata — never for
the full dataset.

## Datasets as complementary sources

The 4 taxi types (`yellow`, `green`, `fhv`, `fhvhv`) are used as **complementary sources**: demand, duration, and cost are compared across them. This involved manually normalizing 4 distinct schemas and addressing the different data gaps in each one — for example, `fhv` does not report fare or tip, and ~82% of its trips lack a pickup location. These rows were not discarded (which would have resulted in losing the majority of `fhv` data); instead, they were retained using a **sentinel value (`-1`)** and are excluded only in the analyses that strictly require that data (such as geographic demand).

## Pipeline stages

| Notebook | Engine | Purpose |
|---|---|---|
| `01_ingesta_datos_crudos_s3` | Python | Downloads raw TLC parquet files and uploads them to `raw_data/` |
| `02_perfilamiento_esquemas` | Python | Profiles schema and data quality across the 4 taxi types |
| `03_etl_limpieza_spark` | PySpark | Cleaning, typing, derived columns, sentinel handling → `clean_data/` |
| `04_joins_agregaciones_spark` | PySpark | Incremental joins/aggregations per type → `gold_data/` |
| `05_export_rds` | Python | Exports the 7 Gold KPIs to RDS (idempotent, `if_exists="replace"`); trip duration median computed via memory-bounded sampling directly from Silver |
| `06_sync_metadatos_rds` | Python | Syncs the S3 metadata catalog to RDS (`pipeline_metadata`, upsert) |
| `00_orquestador` | Python | Automates `06 → 05` and logs every run to `pipeline_runs` |

**Why 03/04 are excluded from automation:** they are computationally heavy
Spark jobs (JVM, S3 connectivity JARs, shuffles). On the course's shared
t2.medium instance (~4GB RAM), repeatedly re-running them automatically proved
unreliable due to memory and disk-quota limits of that specific instance — not
a flaw in the pipeline design. They are run deliberately, on demand.

## How the pipeline is triggered

The pipeline is split into **two stages**, based on how expensive each part is
to recompute:

- **Stage 1 — heavy transformation (manual / on demand):** `01 → 02 → 03 → 04`.
  Triggered by hand when new TLC data arrives. There is no reason to recompute
  Gold automatically if Silver hasn't changed, and this is where Spark competes
  for the instance's limited RAM.
- **Stage 2 — lightweight sync (automated by `00_orquestador.ipynb`):**
  `06 → 05`. Neither step uses Spark, both are idempotent, and both simply
  sync what's already computed in S3 into RDS. This is the part that makes
  sense to re-trigger often, and it's what the orchestrator runs — logging
  every run to `pipeline_runs`, which feeds the dashboard's "Pipeline health" tab.

In a production environment, Stage 2 would be the natural candidate for a
schedule (cron, EventBridge + Lambda, an Airflow DAG) with no manual step.

## Database (RDS)

Dedicated MySQL database on the course's RDS instance:

- **`gold_*` tables** (7 total): the final KPIs, fully recomputed on every run.
- **`pipeline_metadata`**: a catalog of every file in `raw_data/` (bucket, key,
  type, year, month, size, row count), upserted from notebook `06`.
- **`pipeline_runs`**: a log of every orchestrator run (notebook, status,
  duration, error if any).

No credentials are ever hardcoded — notebooks read them from environment
variables or interactive/`getpass` prompts.

## Lambda + backfill

Two paths feed the same S3 metadata catalog, which `06` then syncs to RDS:

- **`lambda_function.py`** — triggered by an S3 `ObjectCreated` event every
  time a new parquet file lands in `raw_data/`; writes a metadata JSON per file.
- **`backfill_metadata.py`** (with a notebook version) — a one-time batch
  script covering the 117 files that already existed before the Lambda was
  active (S3 triggers only fire on new objects). It reuses the Lambda's exact
  parsing logic and is idempotent via a deterministic S3 key.

## Dashboard (Streamlit)

5 tabs, 8 charts, first-person narrative explaining the reasoning behind each
analysis: daily/hourly demand patterns, trip duration & cost, geographic
demand, cross-service correlation, and pipeline health. Deployed via Docker
Compose, redeployed automatically by a self-hosted GitHub Actions runner on
every push to `main`.


## Key design decisions

- **Sentinel value (`-1`)** for structurally missing locations, instead of
  dropping rows.
- **Median, not average**, for duration/fare/tip — less sensitive to outliers.
- **Incremental per-type processing** in Spark to stay within the t2.medium's
  memory limits.
- **RDS holds only KPIs and metadata**, never the full dataset.
- **Two-stage orchestration**: automate only the idempotent, lightweight sync
  (`06 → 05`); run heavy Spark transformations deliberately.
- **No hardcoded credentials** anywhere in the codebase.
