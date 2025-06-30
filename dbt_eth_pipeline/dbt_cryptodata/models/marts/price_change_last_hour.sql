WITH hourly AS (
  SELECT
    DATE_TRUNC('hour', ts) AS hour,
    FIRST_VALUE(price) OVER (PARTITION BY DATE_TRUNC('hour', ts) ORDER BY ts) AS price_start,
    LAST_VALUE(price) OVER (PARTITION BY DATE_TRUNC('hour', ts) ORDER BY ts ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS price_end
  FROM {{ ref('stg_eth_prices') }}
)

SELECT
  hour,
  price_start,
  price_end,
  ROUND(((price_end - price_start) / price_start)::numeric * 100, 2) AS pct_change
FROM hourly
GROUP BY hour, price_start, price_end