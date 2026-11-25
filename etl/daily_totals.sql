-- Extract: total paid per user for one day.
-- :day is the day being processed, 'YYYY-MM-DD' (UTC).
-- Output columns: user_id, total_cents, payment_count.
SELECT
    p.user_id,
    SUM(p.amount_cents) AS total_cents,
    COUNT(*)            AS payment_count
FROM payments p
JOIN payment_events e
    ON e.payment_id = p.payment_id
   AND e.event_type = 'settled'
WHERE date(p.created_at) BETWEEN :day AND date(:day, '+1 day')
GROUP BY p.user_id
ORDER BY p.user_id
