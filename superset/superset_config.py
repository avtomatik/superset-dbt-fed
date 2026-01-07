import os

# =============================================================================
# Core Superset settings
# =============================================================================
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")


# =============================================================================
# Database (Superset metadata DB)
# =============================================================================
WAREHOUSE_HOST = os.getenv("WAREHOUSE_HOST")
WAREHOUSE_PORT = os.getenv("WAREHOUSE_PORT")
WAREHOUSE_DBNAME = os.getenv("WAREHOUSE_DBNAME")
WAREHOUSE_USER = os.getenv("WAREHOUSE_USER")
WAREHOUSE_PASSWORD = os.getenv("WAREHOUSE_PASSWORD")


# =============================================================================
# Feature flags
# =============================================================================
FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}


# =============================================================================
# Misc sane defaults
# =============================================================================
ROW_LIMIT = 10000
SUPERSET_WEBSERVER_TIMEOUT = 60
