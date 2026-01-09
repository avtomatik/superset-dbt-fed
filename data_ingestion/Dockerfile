FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir dbt-core>=1.11.2 \
    dbt-postgres>=1.10.0 \
    "psycopg[binary]">=3.3.2

COPY . .

CMD [ "python", "-m", "data_ingestion.fred_downloader" ]
