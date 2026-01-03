from urllib.parse import urljoin

import psycopg
import requests

from config.database import WarehouseDBConfig
from config.fred import FredConfig


def fetch_series_observations(fred: FredConfig) -> list[dict]:
    resp = requests.get(
        urljoin(fred.FRED_BASE_URL, "series/observations"),
        params={
            "series_id": fred.FRED_SERIES_ID,
            "api_key": fred.FRED_API_KEY,
            "file_type": "json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["observations"]


def load_to_postgres(conn, series_id: str, observations: list[dict]) -> None:
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")

        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS raw.{series_id.lower()} (
                date DATE PRIMARY KEY,
                value DOUBLE PRECISION
            )
        """
        )

        cur.execute(f"TRUNCATE TABLE raw.{series_id.lower()}")

        cur.executemany(
            f"""
            INSERT INTO raw.{series_id.lower()} (date, value)
            VALUES (%(date)s, %(value)s)
            """,
            observations,
        )
    conn.commit()


def main():
    fred = FredConfig()
    db = WarehouseDBConfig()

    observations = fetch_series_observations(fred)

    with psycopg.connect(db.psycopg_dsn) as conn:
        load_to_postgres(conn, fred.FRED_SERIES_ID, observations)

    print("FRED ingestion complete.")


if __name__ == "__main__":
    main()
