# FRED Data Pipeline with Superset and DBT
An end-to-end data pipeline for Federal Reserve Economic Data (FRED).

## Project Setup and Instructions

Follow these steps to get started with the project:

### Step 1: Copy Environment Variables
First, copy the example environment file to create your own `.env` file.

```bash
$ cp .env.example .env
```

### Step 2: Paste Your API Key

Open the `.env` file and paste your `FRED_API_KEY` to authenticate with the external API.

```bash
# .env
FRED_API_KEY=your_fred_api_key_here
```

### Step 3: Set Up, Activate & Synchronize Virtual Environment

Set up and activate your virtual environment, then synchronize it.

```bash
$ uv venv --python 3.12
$ source .venv/bin/activate
$ uv sync
```

### Step 4: Run the Data Ingestion Script

To fetch the data from the external API, run the `fred_downloader.py` script. This will download the necessary data before running any transformations.

```bash
$ uv run python -m data_ingestion.fred_downloader
```

### Step 5: Running the DBT Project

Now that your data is ingested, you can run your DBT project and execute a transformation:

```bash
$ export WAREHOUSE_HOST=localhost
$ export WAREHOUSE_PORT=5432
$ export WAREHOUSE_DBNAME=warehouse
$ export WAREHOUSE_USER=analytics
$ export WAREHOUSE_PASSWORD=analytics
$ uv run dbt run --profiles-dir dbt_project --project-dir dbt_project
$ uv run dbt test --profiles-dir dbt_project --project-dir dbt_project
$ uv run dbt build --profiles-dir dbt_project --project-dir dbt_project
```

---
