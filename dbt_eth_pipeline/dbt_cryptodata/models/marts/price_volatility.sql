SELECT
    DATE(ts) AS date,
    ROUND(STDDEV(price)::numeric, 4) AS price_stddev
FROM {{ ref('stg_eth_prices') }}
GROUP BY date
ORDER BY date DESC