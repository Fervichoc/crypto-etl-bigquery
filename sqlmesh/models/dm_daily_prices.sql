MODEL (
  name dm_daily_prices,
  kind VIEW
);

WITH daily_last AS (
  SELECT
    coin_id,
    vs_currency,
    DATE(source_ts) AS price_date,
    price,
    source_ts,
    ROW_NUMBER() OVER (
      PARTITION BY coin_id, vs_currency, DATE(source_ts)
      ORDER BY source_ts DESC
    ) AS rn
  FROM `crypto-data-485108.cf_mvp.stg_coingecko_prices`
),
daily AS (
  SELECT
    coin_id,
    vs_currency,
    price_date,
    price AS close_price
  FROM daily_last
  WHERE rn = 1
),
with_prev AS (
  SELECT
    *,
    LAG(close_price) OVER (PARTITION BY coin_id, vs_currency ORDER BY price_date) AS prev_close_price
  FROM daily
)
SELECT
  coin_id,
  vs_currency,
  price_date,
  close_price,
  prev_close_price,
  SAFE_DIVIDE(close_price - prev_close_price, prev_close_price) AS daily_return
FROM with_prev
ORDER BY coin_id, vs_currency, price_date;
