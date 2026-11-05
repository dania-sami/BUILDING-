"""Optional Dagster asset sketch; install dagster to run in an orchestrated environment."""
from dagster import asset
from app.engine import ingest, ROOT
import csv
@asset
def validated_claims():
    with (ROOT/'data/claims.csv').open(newline='') as f:
        return ingest(list(csv.DictReader(f)))
