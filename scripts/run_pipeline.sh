#!/usr/bin/env bash
set -euo pipefail

echo "Running data ingestion..."
python -m data_ingestion.fred_downloader

echo "Running dbt transformations"
$ export WAREHOUSE_HOST=localhost
$ export WAREHOUSE_PORT=5432
$ export WAREHOUSE_DBNAME=warehouse
$ export WAREHOUSE_USER=analytics
$ export WAREHOUSE_PASSWORD=analytics
dbt run --profiles-dir dbt_project --project-dir dbt_project
dbt test --profiles-dir dbt_project --project-dir dbt_project
dbt build --profiles-dir dbt_project --project-dir dbt_project

echo "Pipeline complete."
