AUDIT (
  name not_null_prices
);

SELECT *
FROM dm_daily_prices
WHERE price_date IS NULL OR symbol IS NULL OR close IS NULL;
