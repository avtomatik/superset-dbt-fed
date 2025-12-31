import json
import tempfile
from dataclasses import dataclass
from urllib.parse import urljoin

import duckdb
import requests
from config import FRED_API_BASE, FRED_API_KEY, FRED_SERIES_ID, WAREHOUSE


@dataclass
class SeriesRequest:
    """
    Represents a request for fetching time series data from FRED API.

    Attributes:
        api_base (str): The base URL for the FRED API.
        api_key (str): The API key for authenticating requests to FRED.
        series_id (str): The unique identifier for the series to fetch.
        start_date (str | None): Optional start date in 'YYYY-MM-DD' format.
        end_date (str | None): Optional end date in 'YYYY-MM-DD' format.
        file_type (str): The format for the data file ('json' by default).
    """

    api_base: str
    api_key: str
    series_id: str
    start_date: str | None = None
    end_date: str | None = None
    file_type: str = "json"


@dataclass
class DBWriteRequest:
    """
    Represents a request to write data into a DuckDB table.

    Attributes:
        data (list): The data to be inserted into the database as a list of
            dictionaries.
        table_name (str): The name of the table to write the data to.
        db_path (str): The connection path to the DuckDB database.
    """

    data: list
    table_name: str
    db_path: str


def fetch_series_observations(req: SeriesRequest) -> list:
    """
    Fetch observations for a FRED series and return as a list of dictionaries.

    Args:
        req (SeriesRequest): A SeriesRequest object containing API
            configuration.

    Returns:
        list: A list of dictionaries, where each dictionary represents an
            observation with 'date' and 'value' keys.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the
            API request.
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
    return data.get("observations", [])


def create_raw_schema_if_not_exists(con: duckdb.DuckDBPyConnection) -> None:
    """
    Create the 'raw' schema in DuckDB if it does not already exist.

    Args:
        con (duckdb.DuckDBPyConnection): A DuckDB connection object.
    """
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")


if __name__ == "__main__":
    series_req = SeriesRequest(
        series_id=FRED_SERIES_ID, api_base=FRED_API_BASE, api_key=FRED_API_KEY
    )

    observations = fetch_series_observations(series_req)

    with tempfile.NamedTemporaryFile(
        delete=False, mode="w", encoding="utf-8"
    ) as temp_file:
        json.dump(observations, temp_file)
        temp_file_path = temp_file.name

    con = duckdb.connect(WAREHOUSE)
    create_raw_schema_if_not_exists(con)

    query = f"""
    CREATE OR REPLACE TABLE raw.{series_req.series_id.lower()} AS
    SELECT * FROM read_json_auto('{temp_file_path}')
    """
    con.execute(query)

    con.close()

    print(f"Ingestion of {series_req.series_id} complete.")
