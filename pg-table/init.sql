-- Create schema if does not exist
CREATE SCHEMA IF NOT EXISTS public;

-- Create crypto_prices table
CREATE TABLE IF NOT EXISTS public.crypto_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    price NUMERIC(20,8) NOT NULL,
    timestamp TIMESTAMP NOT NULL
);

-- Create index on symbol for faster lookups
CREATE INDEX IF NOT EXISTS idx_crypto_prices_symbol 
ON public.crypto_prices (symbol);

-- Create index on timestamp for faster time-based queries
CREATE INDEX IF NOT EXISTS idx_crypto_prices_timestamp
ON public.crypto_prices (timestamp);