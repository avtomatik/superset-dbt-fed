import os
from dataclasses import dataclass
from urllib.parse import urljoin

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine


@dataclass
class DBWriteRequest:
    df: pd.DataFrame
    table_name: str
    db_path: str


@dataclass
class SeriesRequest:
    api_base: str
    api_key: str
    series_id: str
    start_date: str | None = None
    end_date: str | None = None
    file_type: str = "json"


load_dotenv()

FRED_API_BASE = "https://api.stlouisfed.org/fred/"
FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_SERIES_ID = os.getenv("FRED_SERIES_ID")
DB_PATH = os.getenv("DB_PATH", "duckdb:///data/warehouse.duckdb")


def fetch_series_observations(req: SeriesRequest) -> pd.DataFrame:
    """
    Fetch observations for a FRED series and return as DataFrame.
    params:
      - req.series_id: e.g. 'GDP', 'CPIAUCSL'
      - req.start_date, req.end_date: 'YYYY-MM-DD' or leave None to get whole history
    """
    endpoint = urljoin(req.api_base, "series/observations")
    params = {
        "series_id": req.series_id,
        "api_key": req.api_key,
        "file_type": req.file_type,
    }
    if req.start_date:
        params["observation_start"] = req.start_date
    if req.end_date:
        params["observation_end"] = req.end_date

    resp = requests.get(endpoint, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # observations is a list of {date, value, ...}
    obs = data.get("observations", [])
    df = pd.DataFrame(obs)
    # Clean: convert date, numeric value (note: "." sometimes used for missing)
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"].replace(".", pd.NA))
    return df


def write_df_to_db(req: DBWriteRequest) -> None:
    """
    Write df to SQL DB. req.db_path is a SQLAlchemy URL, e.g. duckdb:///data/my.db or postgresql://user:pass@host/db
    """
    engine = create_engine(req.db_path)
    req.df.to_sql(req.table_name, engine, if_exists="replace", index=False)


if __name__ == "__main__":
    series_req = SeriesRequest(
        series_id=FRED_SERIES_ID, api_base=FRED_API_BASE, api_key=FRED_API_KEY
    )
    df = fetch_series_observations(series_req)

    db_req = DBWriteRequest(
        df=df,
        table_name=f"fred_{series_req.series_id.lower()}",
        db_path=DB_PATH,
    )

    write_df_to_db(db_req)
