# Fix a daily payments ETL job

Every night a job reads the payments database and writes each user's total for the day into the
table `daily_totals`, which a report reads. The finance team says the totals are wrong, and a retry
last week duplicated a whole day. Your job is to fix the SQL. It runs on SQLite, which comes with
Python 3, so there is nothing to install.

You may use your usual AI tool; we will watch how you use it. Please think out loud.

## Files

- `RULES.md`: the three rules of the report. Read it first.
- `etl/daily_totals.sql`: extract, the total per user for one day (`:day`).
- `etl/load.sql`: load, writes that result into `daily_totals`.
- `etl/target.sql`: the `daily_totals` table.
- `data/seed.sql`: the source tables and data. Do not edit it.

To see what the extract returns for a day:

```
python3 run.py 2026-11-10
```

## Tasks: 7 minutes in total (any order)

1. **Counted twice (about 2 minutes).** Some payments are counted more than once. Make each payment count once (rule 1).
2. **Wrong payments and wrong days (about 2 minutes).** Refunded payments and payments from another day are included
   (rule 2).
3. **Retry (about 3 minutes).** Running the job twice for the same day duplicates its rows. Make it safe to run again
   without touching other days (rule 3). You may change `etl/load.sql` and `etl/target.sql`.

At 7 minutes we stop. Then run:

```
python3 check/check.py
```

Do not edit the `check` or `data` folders.
