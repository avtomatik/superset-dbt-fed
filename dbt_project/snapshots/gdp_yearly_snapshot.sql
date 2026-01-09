{% snapshot gdp_yearly_snapshot %}

{{ config(
    target_schema = 'snapshots',
    unique_key = 'year',
    strategy = 'check',
    check_cols = ['gdp_value']
) }}

SELECT
    year,
    gdp_value
FROM
    {{ ref('gdp_yearly') }}

{% endsnapshot %}