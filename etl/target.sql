-- Target table of the job (the report reads it).
CREATE TABLE daily_totals (
    day           TEXT    NOT NULL,
    user_id       TEXT    NOT NULL,
    total_cents   INTEGER NOT NULL,
    payment_count INTEGER NOT NULL
);
