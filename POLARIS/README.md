# POLARIS | Insurance Data & AI Mission Control

I built POLARIS to explore the engineering work behind reliable insurance analytics and AI: clean ingestion, traceable transformations, quality gates, repeatable pipelines, and answers grounded in validated data.

## Quick start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** and click **Run pipeline**. Run `pytest -q` to check the engine.

## Explore

1. Run the pipeline and watch 180 valid claims load while three deliberately invalid rows enter quarantine.
2. Explore the portfolio exposure by product and inspect the modeled claims.
3. Open Data lineage to follow the flow from source to evidence.
4. Ask the evidence assistant about open Boat claims and inspect the claim IDs supporting its answer.
5. Review the audit log and export a CSV.

## Engineering contents

- `app/`: FastAPI endpoints, SQL-backed pipeline and validation engine.
- `static/`: custom responsive front end.
- `data/`: synthetic source claims.
- `tests/`: automated validation, idempotency, evidence, and API tests.
- `dbt/`: Snowflake-oriented illustrative dbt staging model and schema tests.
- `dagster_project/`: optional Dagster asset example (requires Dagster installation).
- `.github/workflows/`: CI quality gate example.
- `Dockerfile`: container build.
- `docs/`: architecture and production gap analysis.

**Scope:** Everything uses invented claim and policy records. The running demo uses SQLite, not Snowflake. dbt and Dagster assets are examples and are not connected to a live warehouse. The assistant performs deterministic evidence retrieval, not live LLM inference. This is a portfolio demonstration, not a production insurance system or a Svedea product.
