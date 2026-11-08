# VAULT360 | Finance & Risk Data Architecture Lab

A hands-on Python + SQL + Data Vault 2.0 inspired proof of concept for the emagine Data Modeller vacancy (#327003). Entirely fictional banking records.

## Run locally

```bash
python3 app/pipeline.py
python3 app/build_site.py
python3 -m unittest discover -s tests -v
```

Open `index.html` in any browser. No package installation required. The site is static and does not run the Python pipeline inside the browser; regenerate it after data changes.

## Contents

- `app/pipeline.py`: synthetic source generator, validation, hashed hubs, links, historized satellite, quarantine, lineage, audit, and monthly aggregation.
- `app/build_site.py`: renders an interactive read-only explorer from the SQLite database.
- `sql/bigquery_reference.sql`: illustrative BigQuery DDL, not deployed.
- `docs/ARCHITECTURE.md`: architectural choices, controls, and limitations.
- `tests/`: automated unit tests.

**Security:** Use only synthetic data. Do not import banking records into this demo.
