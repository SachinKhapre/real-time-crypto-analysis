{{ config(materialized='table') }}

WITH base AS (
    SELECT
        ts,
        price
    FROM {{ ref('stg_eth_prices') }}
    WHERE ts >= now() - interval '1 hour'
),
ordered AS (
    SELECT
        ts,
        price,
        ROW_NUMBER() OVER (ORDER BY ts ASC) AS rn_asc,
        ROW_NUMBER() OVER (ORDER BY ts DESC) AS rn_desc
    FROM base
),
first_price AS (
    SELECT price AS first_price, ts AS start_time
    FROM ordered
    WHERE rn_asc = 1
),
last_price AS (
    SELECT price AS last_price, ts AS end_time
    FROM ordered
    WHERE rn_desc = 1
)
SELECT
    f.start_time,
    l.end_time,
    f.first_price,
    l.last_price,
    l.last_price - f.first_price AS price_change,
    ROUND(((l.last_price - f.first_price) / f.first_price)::numeric * 100, 2) AS percent_change
FROM first_price f
CROSS JOIN last_price l
