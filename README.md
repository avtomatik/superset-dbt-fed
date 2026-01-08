# FRED Data Pipeline with Superset & dbt (Dockerized)

An end-to-end, fully containerized data pipeline for **Federal Reserve Economic Data (FRED)** using:

* **PostgreSQL** as the warehouse
* **Python ingestion** for FRED data
* **dbt** for transformations & tests
* **Apache Superset** for analytics & dashboards

All orchestration is handled via **Docker Compose**.

---

## Architecture Overview

```text
FRED API
   │
   ▼
Python Ingestion (container)
   │
   ▼
Postgres Warehouse
   │
   ▼
dbt (run → test → build)
   │
   ▼
Superset (Dashboards & SQL Lab)
```

---

## Prerequisites

You only need:

* Docker ≥ 24
* Docker Compose (v2 plugin)
* A FRED API key

No Python, dbt, or Superset installed locally.

---

## Quick Start

### 1. Create your `.env` file

Copy the example environment file:

```bash
cp .env.example .env
```

---

### 2. Required configuration

Open `.env` and **update only the following values**.

#### 🔑 FRED configuration (required)

```env
FRED_API_KEY=your_fred_api_key_here
FRED_SERIES_ID=GDPC1
```

You can change `FRED_SERIES_ID` to any valid FRED series.

---

#### 🔐 Superset secret key (required)

Generate a secure secret key:

```bash
openssl rand -base64 48
```

Paste it into:

```env
SUPERSET_SECRET_KEY=your_generated_secret_key
```

---

#### 👤 Superset admin user (optional)

Change these if you want custom credentials:

```env
SUPERSET_USERNAME=admin
SUPERSET_FIRSTNAME=Admin
SUPERSET_LASTNAME=User
SUPERSET_EMAIL=admin@superset.com
SUPERSET_PASSWORD=admin
```

---

### 3. Start the pipeline

From the project root:

```bash
docker compose up --build
```

That’s it.

Docker Compose will:

1. Start PostgreSQL
2. Run the FRED ingestion container
3. Execute dbt:

   * `dbt run`
   * `dbt test`
   * `dbt build`
4. Initialize Superset (DB migrations, admin user, permissions)
5. Start Superset on port **8088**

---

## Accessing Superset

Once all containers are healthy:

* URL: [http://localhost:8088](http://localhost:8088)
* Username: `SUPERSET_USERNAME`
* Password: `SUPERSET_PASSWORD`

---

## What Happens Automatically

### Data ingestion

* Pulls data from the FRED API
* Loads raw data into PostgreSQL

### dbt

* Builds models
* Runs tests
* Creates analytics-ready tables

### Superset

* Initializes metadata DB
* Creates admin user (if missing)
* Connects to the warehouse
* Serves dashboards & SQL Lab

No manual intervention required.

---

## Environment Variables Reference

All services (ingestion, dbt, Superset) share the same warehouse configuration:

```env
WAREHOUSE_DIALECT_DRIVER=postgresql+psycopg2
WAREHOUSE_HOST=postgres
WAREHOUSE_PORT=5432
WAREHOUSE_DBNAME=warehouse
WAREHOUSE_USER=analytics
WAREHOUSE_PASSWORD=analytics

SQLALCHEMY_DATABASE_URI=${WAREHOUSE_DIALECT_DRIVER}://${WAREHOUSE_USER}:${WAREHOUSE_PASSWORD}@${WAREHOUSE_HOST}:${WAREHOUSE_PORT}/${WAREHOUSE_DBNAME}
```

These values typically **do not need to be changed**.

---

## Stopping & Resetting

Stop all services:

```bash
docker compose down
```

Remove all data (⚠️ destructive):

```bash
docker compose down -v
```

---
