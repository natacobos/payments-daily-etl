# Daily payments report: rules

1. **A payment counts once.** It counts when its status is `completed` and the processor has sent its
   `settled` event. The processor sometimes sends the same event twice; that must not change the totals.
2. **Only that day.** A run for day D includes only payments created on day D (UTC date of
   `payments.created_at`). Failed and refunded payments never count.
3. **Safe to run again.** If the job runs again for a day (for example, a retry after a timeout),
   `daily_totals` must end up the same as after one run. Rows of other days are never changed.
