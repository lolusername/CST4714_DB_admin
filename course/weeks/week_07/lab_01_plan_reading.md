# Lab 1: Why Does a Twenty-Row Result Read So Much Data?

The support queue displays only twenty tickets. That does not mean PostgreSQL
needs to examine only twenty rows. Use a query plan to find out what it does.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Run the Workload

Run [performance_lab_setup.sql](performance_lab_setup.sql) in your personal
PostgreSQL/Supabase practice database. It recreates only `performance_lab`, with
**100,000 tickets and 2,000 open tickets**. The larger table makes the access
method worth investigating.

```sql
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

The question is precise: the twenty newest open tickets, one row per ticket.
Before viewing a plan, predict whether the server can stop after reading the
first twenty physical rows. Explain what the filter and ordering require.

## 2. Read the Plan From Its Inputs

Run plain EXPLAIN on that SELECT, then run:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

Plain EXPLAIN estimates work. ANALYZE actually executes the statement; here it is
a read-only SELECT. BUFFERS reports page activity.

Use the [Chapter 7 plan explanation](../../textbook/module_07_performance.md) to
identify the scan, any sort, and the final limit. Write short comments answering:

- How does PostgreSQL find qualifying tickets? Name the actual scan node.
- Is it sorting qualifying rows before returning twenty? Name the sort node if present.
- How much work is hidden by the small final result? Use actual rows and any
  `Rows Removed by Filter` measurement, not just the final output count.

Estimated `rows=` and `actual rows=` are different measurements. Where a node
runs more than once, consider `loops`; a node's per-loop count is not necessarily
its total work. Your plan can differ with version, settings, and hardware.

## 3. Predict One Useful Change

Change only `LIMIT 20` to `LIMIT 5` and run the analyzed plan again. Compare the
final output with the scan's qualifying and rejected rows. Did a smaller result
also make the scan smaller? Explain the difference using your actual plan, then
restore `LIMIT 20`. This is a separate comparison, not the baseline for Day 2.

Without creating an index yet, explain why an ordered access path on
`(status, opened_at DESC)` might help this query. Identify which scan or sort work
you expect to change. The next lab tests that prediction.

**Submit:** `week_07_plan_reading.sql` with the query, its EXPLAIN forms, the
five-row comparison, and your observations as comments. Copy only the relevant plan lines. No screenshots
or separate report are required.
