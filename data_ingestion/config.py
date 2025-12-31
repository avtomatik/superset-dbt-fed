import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
WAREHOUSE = BASE_DIR / "data" / "processed" / "warehouse.duckdb"


FRED_API_BASE = "https://api.stlouisfed.org/fred/"
FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_SERIES_ID = os.getenv("FRED_SERIES_ID")
