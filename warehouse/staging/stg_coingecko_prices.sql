CREATE OR REPLACE VIEW `crypto-data-485108.cf_mvp.stg_coingecko_prices` AS
SELECT
  coin_id,
  vs_currency,
  CAST(price AS FLOAT64) AS price,
  TIMESTAMP(source_timestamp_utc) AS source_ts,
  TIMESTAMP(ingestion_timestamp_utc) AS ingestion_ts,
  ingestion_date
FROM `crypto-data-485108.cf_mvp.raw_coingecko_prices`;
