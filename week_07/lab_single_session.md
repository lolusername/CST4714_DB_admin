# Optional Practice Reading a Plan and Testing an Index

**Optional reference for the instructor demonstration or extra practice. No separate graded submission. The required work is in the [Week 7 guide](README.md).**

Use this optional exercise to repeat the instructor's larger index demonstration. Compare the same query before and after adding one index. You may save your SQL and observations in a local practice file.

## 1 Load the fixture and record the baseline

Run [performance_lab_setup.sql](performance_lab_setup.sql) once in your personal PostgreSQL or Supabase practice database. It resets only the disposable performance_lab schema and creates **100,000 synthetic tickets**, including **2,000 open tickets**. Save any previous work you need before resetting it. The setup already runs ANALYZE to collect planner statistics.

If your cloud connection is unavailable, use the [disposable PostgreSQL notebook setup](../week_06/README.md#postgresql-without-a-cloud-database-account). Run the setup SQL and each query with its run_sql helper. Save your SQL file before the notebook's final cleanup. There is no extra notebook submission.

Run the queue query and save all twenty ticket IDs in order:

```sql
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

The first five IDs should be 100000, 99901, 99900, 99801, 99800. Every timestamp in this fixture is unique. A real queue with tied times would need a tie-breaker for a fully deterministic order.

First put EXPLAIN before the SELECT to see estimates. Then run this analyzed plan twice:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

EXPLAIN ANALYZE executes the statement. This exercise uses a read-only SELECT. Copy the relevant scan, sort, and limit lines into SQL comments. Record the estimated and actual rows, loops, rows removed by the filter if shown, top-level buffer counters, and execution times. Keep parent and child buffer counts separate instead of adding them together.

Explain why returning twenty rows can still require examining many more. Your exact plan, estimates, and timings may differ from the lecture.

## 2 Add one index and repeat the same query

Before running the statement, predict which scan or sort work it could avoid:

```sql
CREATE INDEX tickets_status_opened_idx
ON performance_lab.tickets (status, opened_at DESC);
```

This index orders entries by status and then by opening time within each status. The open entries can therefore be read newest first. Keep the SQL query and data unchanged. Do not reset the schema or refresh statistics between the before and after runs.

Run the original SELECT again and compare all twenty ordered IDs. Then run the analyzed plan twice again. Record whether the scan changes, whether a separate Sort remains, the top-level buffer activity, and both execution times. A faster result is useful only if it still answers the same query.

Measure the index's storage:

```sql
SELECT pg_relation_size(
    'performance_lab.tickets_status_opened_idx'
) AS index_bytes;
```

One quick run does not establish production performance. This experiment measures index storage and read behavior. It does not measure the additional work of maintaining the index during writes.

## 3 Recommend and finish

In one short SQL comment, recommend **keep**, **remove**, or **test further** for this query. State whether the ordered IDs stayed the same, explain one change in the plan, and give one cost or remaining question. Distinguish the storage you measured from write overhead you have not measured.

Save your SQL and observations before cleanup:

```sql
DROP SCHEMA IF EXISTS performance_lab CASCADE;
```

Save your practice file locally. This optional exercise has no submission. If you used supplied output because your connection failed, identify it as supplied output and tell the instructor which steps you could not run.

## Optional practice

If time remains, predict whether LIMIT 5 reduces the baseline scan's work. Reset only after saving the required comparison, then test the prediction. Partial indexes, join operators, and machine-readable plan analysis are optional follow-up reading for this shortened week.
