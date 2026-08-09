# Module 7: Performance Work Begins With Evidence

## Operating Question

When a query feels slow, what evidence can distinguish a scan, a bad estimate, an
expensive join, an avoidable sort, blocking, or simply more work than expected?

## Learning Outcomes

After this module, you can:

- turn a vague complaint into a reproducible query and workload statement;
- distinguish estimated plans from plans with actual execution evidence;
- recognize common scan, join, sort, and aggregate plan nodes;
- connect selectivity and statistics to planner choices;
- design and test a basic single-column, composite, or partial index; and
- decide whether an improvement justifies its write, storage, and maintenance cost.

## 1. "Slow" Is a Symptom, Not a Diagnosis

Begin with a reproducible statement:

- Which exact query and parameter values?
- Which database, schema, and data volume?
- What result grain and row count?
- What elapsed time or service objective?
- Is the time spent executing, waiting for a lock, transferring many rows, or
  rendering in a client?
- Is the behavior repeatable, and what changed?

A query returning a million rows may be fast for the database and slow for the
network or browser. A query waiting on a lock may have a simple plan. Measure the
right layer.

## 2. `EXPLAIN` Shows the Planner's Strategy

```sql
EXPLAIN
SELECT ticket_id, subject, opened_at
FROM metro_support.tickets
WHERE status = 'open'
ORDER BY opened_at DESC;
```

Plain `EXPLAIN` estimates a plan without running the query. It is safe for
understanding a potentially mutating statement because it does not execute it.

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM metro_support.tickets
WHERE status = 'open'
ORDER BY opened_at DESC;
```

`ANALYZE` executes the statement and reports actual timing and rows. On `UPDATE`,
`DELETE`, or function calls, that means real side effects unless protected and
rolled back. Use it only when execution is safe. `BUFFERS` reports cache and I/O
activity available to the statement.

## 3. Read a Plan From the Inside Out

A plan is a tree. Child nodes produce rows for parent nodes.

Common nodes include:

- **Seq Scan:** inspect table pages and test rows. Often correct for a small table
  or a query returning much of the table.
- **Index Scan:** use an index to find row locations, then access table rows.
- **Index Only Scan:** answer from index entries when required columns and
  visibility information permit it.
- **Bitmap Index/Heap Scan:** collect many index matches and visit table pages in
  batches.
- **Nested Loop:** for each row from one input, scan or probe the other input.
- **Hash Join:** build a hash table for one input and match the other, commonly for
  equality joins.
- **Merge Join:** consume sorted inputs and merge matching keys.
- **Sort:** order rows; may use memory or spill to temporary storage.
- **Aggregate/GroupAggregate/HashAggregate:** reduce input rows into summaries.

Node names are not grades. A sequential scan is not automatically bad, and an
index scan is not automatically good.

## 4. Estimates Drive Choices

The planner estimates row counts and costs using table statistics, data type
information, constraints, and configurable assumptions. Compare estimated rows
with actual rows in an analyzed plan.

Large mismatches may come from:

- stale statistics;
- correlated columns that basic statistics treat as independent;
- unusual parameter values;
- skewed data;
- expressions without useful statistics; or
- a model that hides important relationships.

`ANALYZE` refreshes statistics:

```sql
ANALYZE metro_support.tickets;
```

Do not run maintenance blindly as a ritual. Identify the mismatch and verify the
effect.

## 5. Selectivity Explains Many Scan Decisions

Selectivity is the fraction of rows expected to satisfy a condition. An index is
often attractive when a query needs a small, identifiable fraction of a large
table. If nearly every row has `status = 'open'`, using an index may still require
visiting most table pages, making a sequential scan reasonable.

The twelve-row class dataset is too small to demonstrate realistic planner
tradeoffs. Performance labs create a larger, disposable table with a skewed status
distribution. Small examples teach correctness; larger fixtures reveal access
paths.

## 6. B-Tree Indexes Support Ordered Comparisons

PostgreSQL's default B-tree index supports equality and range comparisons and can
also help ordered retrieval.

```sql
CREATE INDEX perf_tickets_status_opened_idx
ON performance_lab.tickets (status, opened_at DESC);
```

A composite index is ordered first by `status`, then by `opened_at` within each
status. It may efficiently support:

```sql
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20
```

It is less directly suited to a query that filters only `opened_at` without the
leading column. Column order should follow real predicates and ordering needs,
not a rule such as "most unique first" applied without context.

## 7. Partial Indexes Cover a Deliberate Subset

If most tickets are closed but the operational queue reads only active rows, a
partial index may be smaller:

```sql
CREATE INDEX perf_tickets_active_opened_idx
ON performance_lab.tickets (opened_at DESC)
WHERE status IN ('new', 'open', 'in_progress');
```

The query predicate must imply the index predicate for the planner to use it.
Partial indexes add design specificity: if the application's definition of active
changes, the index and queries may need coordinated revision.

## 8. Indexes Have Costs

Each useful index can add:

- storage;
- write work on inserts, updates, and deletes;
- write-ahead log volume;
- backup size or duration;
- cache competition; and
- maintenance and cognitive overhead.

Duplicate, unused, or speculative indexes are not free. Start with a workload and
evidence.

## Worked Example: Test an Index Hypothesis

**Workload:** list the 20 newest open tickets in a large operational table.

### Baseline

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

Record:

- scan node;
- estimated and actual rows at the scan;
- whether a sort occurs;
- planning and execution time; and
- buffer evidence.

### Hypothesis

An index on `(status, opened_at DESC)` can locate open rows in requested order and
may avoid scanning and sorting unrelated rows.

### Change and Refresh

```sql
CREATE INDEX perf_tickets_status_opened_idx
ON performance_lab.tickets (status, opened_at DESC);

ANALYZE performance_lab.tickets;
```

### Remeasure

Run the identical analyzed query. Do not change the selected columns, predicate,
order, or limit while comparing.

### Decide

Keep the index only if the workload benefit is meaningful relative to its cost.
A changed node name alone is not enough. On a warm cache and small class fixture,
timing can vary; plan shape, rows, sort removal, and buffers may be more stable
evidence.

## 9. Separate Query Tuning From Lock Diagnosis

An analyzed plan reports execution after the statement can proceed. If the query
waits on another transaction, `pg_stat_activity`, wait events, and
`pg_blocking_pids` may be the first useful evidence. Do not add an index to solve a
transaction left open in a client.

## Common Misconceptions

### "Sequential scan means the index is missing"

The table may be small, the condition unselective, the statistics reasonable, or
the available index mismatched to the query.

### "Lower estimated cost is milliseconds"

Planner cost units are relative estimates, not elapsed-time units.

### "`EXPLAIN ANALYZE DELETE` is only an explanation"

`ANALYZE` executes the statement. Use a safe copy and transaction or avoid it.

### "One fast run proves the change"

Caching, concurrent load, and measurement noise affect timing. Repeat carefully
and compare multiple kinds of evidence.

## Practice

For a query that filters `assignee_id`, selects active statuses, orders newest
first, and returns 25 rows:

1. state the result grain and workload;
2. propose a composite or partial index;
3. predict which plan work it may remove;
4. name three before/after observations; and
5. state one write or maintenance cost.

## Retrieval and Transfer

1. How does `EXPLAIN` differ from `EXPLAIN ANALYZE`?
2. Why might PostgreSQL choose a sequential scan when an index exists?
3. What does a large estimated-versus-actual row mismatch suggest?
4. Why does composite-index column order matter?
5. When can a partial index be useful?
6. Which evidence would tell you the query is waiting rather than scanning slowly?

## Further Reading

- PostgreSQL `EXPLAIN`: <https://www.postgresql.org/docs/current/using-explain.html>
- PostgreSQL planner statistics: <https://www.postgresql.org/docs/current/planner-stats.html>
- PostgreSQL index types: <https://www.postgresql.org/docs/current/indexes-types.html>
- PostgreSQL multicolumn indexes: <https://www.postgresql.org/docs/current/indexes-multicolumn.html>
- PostgreSQL partial indexes: <https://www.postgresql.org/docs/current/indexes-partial.html>
