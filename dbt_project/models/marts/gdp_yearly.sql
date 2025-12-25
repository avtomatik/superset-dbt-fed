{{ config(materialized = 'table') }} WITH quarterly AS (
    SELECT
        date,
        value :: DOUBLE PRECISION AS gdp_value
    FROM
        {{ ref('stg_fred_gdpc1') }}
),
yearly AS (
    SELECT
        EXTRACT(
            year
            FROM
                date
        ) :: INT AS year,
        EXP(SUM(LN(gdp_value)) / COUNT(*)) AS gdp_geom_mean
    FROM
        quarterly
    GROUP BY
        year
)
SELECT
    year,
    gdp_geom_mean AS gdp_value
FROM
    yearly
ORDER BY
    year