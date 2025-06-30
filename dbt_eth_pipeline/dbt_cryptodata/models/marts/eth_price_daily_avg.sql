SELECT
    DATE(ts) AS date,
    ROUND(AVG(price)::numeric, 2) AS avg_price
FROM {{ ref('stg_eth_prices') }}
GROUP BY date
ORDER BY date DESC