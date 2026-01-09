import os

# =============================================================================
# St. Louis Fed Web Services API
# =============================================================================
FRED_BASE_URL = os.getenv("FRED_BASE_URL")
FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_SERIES_ID = os.getenv("FRED_SERIES_ID")


# =============================================================================
# Warehouse (used by ingestion, dbt, superset)
# =============================================================================
WAREHOUSE_HOST = os.getenv("WAREHOUSE_HOST")
WAREHOUSE_PORT = os.getenv("WAREHOUSE_PORT")
WAREHOUSE_DBNAME = os.getenv("WAREHOUSE_DBNAME")
WAREHOUSE_USER = os.getenv("WAREHOUSE_USER")
WAREHOUSE_PASSWORD = os.getenv("WAREHOUSE_PASSWORD")
