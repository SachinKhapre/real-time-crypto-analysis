{{ config(
    alias='stg_eth_prices',
    materialized='view',
    schema='staging'
) }}

select
    timestamp::timestamp as ts,
    symbol,
    price::float
from {{ source('public', 'crypto_prices')}}