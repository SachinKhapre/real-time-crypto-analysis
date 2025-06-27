{{ config(materialized='table', alias='eth_price_5min_avg') }}

WITH base AS (
    SELECT
        date_trunc('minute', ts) AS minute_bucket,
        price
    FROM {{ ref('stg_eth_prices') }}
),
grouped AS (
    SELECT
        minute_bucket,
        avg(price) AS avg_price
    FROM base
    GROUP BY minute_bucket
    ORDER BY minute_bucket
)
SELECT * FROM grouped