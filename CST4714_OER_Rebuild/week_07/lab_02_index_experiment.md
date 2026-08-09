# Lab 2: Measure, Change, Remeasure, Decide

## Purpose

Test one index hypothesis against an unchanged workload and make an evidence-based
keep or remove recommendation.

This is individual work completed in class. Submit one SQL file.

## 1. Capture the Baseline

Reset the fixture with [`performance_lab_setup.sql`](performance_lab_setup.sql).
Create `week_07_index_decision.sql` and run:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

Record scan, sort, estimated and actual rows, execution time, and buffer evidence.

## 2. Test the Hypothesis

Create a B-tree index on `(status, opened_at DESC)` and run `ANALYZE`. Rerun the
identical query at least twice without changing its columns, predicate, order, or
limit.

Record:

- which node changed;
- whether the explicit sort remained;
- actual rows read or returned by important nodes;
- repeated execution observations; and
- index size from `pg_relation_size` or `pg_size_pretty`.

Run one additional query that filters only by `opened_at`. Explain why the
composite index's leading column matters.

## 3. Decide

End the file with a claim-evidence-tradeoff comment recommending `KEEP`, `REMOVE`,
or `TEST FURTHER`. The decision must cite at least two plan observations and one
write, storage, backup, or maintenance cost.

## Submit One Thing

Submit `week_07_index_decision.sql`. A different plan or timing from a classmate
is not automatically wrong; your evidence and interpretation must match your run.
