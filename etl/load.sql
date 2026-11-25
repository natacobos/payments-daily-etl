-- Load: write the day's result into daily_totals.
-- Before this file runs, the job puts the output of daily_totals.sql for :day in the table `staging`
-- (columns user_id, total_cents, payment_count). Separate statements with a semicolon.
INSERT INTO daily_totals (day, user_id, total_cents, payment_count)
SELECT :day, user_id, total_cents, payment_count
FROM staging;
