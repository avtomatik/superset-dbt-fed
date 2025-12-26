# superset-dbt-fed

# Project Setup and Instructions

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

### Step 3: Set Up & Activate & Synchronize Virtual Environment

```bash
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

---

### Running the DBT Project

To run your DBT project and execute a transformation, use the following command:

```bash
$ uv run dbt run --project-dir dbt_project --select stg_fred_gdpc1 gdp_yearly  # Expected to Fail: to Be Continued...
```
---
