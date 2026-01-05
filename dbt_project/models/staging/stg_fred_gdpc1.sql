{{ config(materialized = 'table', schema = 'staging') }}

WITH raw AS (
  SELECT
    date,
    value :: DOUBLE PRECISION AS gdp_value
  FROM
    {{ source('fred', 'gdpc1') }}
)

SELECT
  date :: DATE AS date,
  gdp_value
FROM
  raw
WHERE
  gdp_value IS NOT NULL
