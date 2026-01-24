AUDIT (
  name unique_symbol_date
);

SELECT symbol, price_date, COUNT(*) AS n
FROM dm_daily_prices
GROUP BY 1,2
HAVING COUNT(*) > 1;
