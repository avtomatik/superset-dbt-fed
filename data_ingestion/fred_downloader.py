from urllib.parse import urljoin

import psycopg
import requests

from .config import (FRED_API_KEY, FRED_BASE_URL, FRED_SERIES_ID,
                     WAREHOUSE_DBNAME, WAREHOUSE_HOST, WAREHOUSE_PASSWORD,
                     WAREHOUSE_PORT, WAREHOUSE_USER)


def fetch_series_observations() -> list[dict]:
    resp = requests.get(
        urljoin(FRED_BASE_URL, "series/observations"),
        params={
            "series_id": FRED_SERIES_ID,
            "api_key": FRED_API_KEY,
            "file_type": "json",
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["observations"]


def load_to_postgres(conn, series_id: str, observations: list[dict]) -> None:
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")

        cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS raw.{series_id.lower()} (
                date DATE PRIMARY KEY,
                value DOUBLE PRECISION
            );
            """
        )

        cur.execute(f"TRUNCATE TABLE raw.{series_id.lower()};")

        cur.executemany(
            f"""
            INSERT INTO raw.{series_id.lower()} (date, value)
            VALUES (%(date)s, %(value)s);
            """,
            observations,
        )
    conn.commit()


def main():
    observations = fetch_series_observations()
    dsn = (
        f"postgresql://{WAREHOUSE_USER}:{WAREHOUSE_PASSWORD}"
        f"@{WAREHOUSE_HOST}:{WAREHOUSE_PORT}/{WAREHOUSE_DBNAME}"
    )

    with psycopg.connect(dsn) as conn:
        load_to_postgres(conn, FRED_SERIES_ID, observations)

    print("FRED ingestion complete.")


if __name__ == "__main__":
    main()
