#!/usr/bin/env bash
set -euo pipefail

echo "Running data ingestion"
python data_ingestion/fred_downloader.py

echo "Running dbt transformations"
dbt run --project-dir dbt_project
dbt test --project-dir dbt_project

echo "Pipeline complete"
