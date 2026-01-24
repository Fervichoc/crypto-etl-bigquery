AUDIT (
  name positive_close
);

SELECT *
FROM dm_daily_prices
WHERE close <= 0;
