SELECT
  DATE_TRUNC('minute', ts) - INTERVAL '1 minute' * (EXTRACT(MINUTE FROM ts)::int % 5) AS window_start,
  ROUND(AVG(price)::numeric, 4) AS avg_price
FROM {{ ref('stg_eth_prices') }}
GROUP BY window_start
ORDER BY window_start DESC