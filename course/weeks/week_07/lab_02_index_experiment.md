# Lab 2: Does This Index Earn Its Space?

Test whether an index helps the twenty-newest-open-tickets query. A useful
conclusion explains the mechanism and the cost, even when timing is noisy.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Record the Same Query Before the Change

The instructor demonstrates a partial index for `in_progress` tickets in
`performance_demo`. Your experiment uses a composite index for `open` tickets
in `performance_lab`. Keep these queries and index definitions distinct.

Reset the disposable data with
[performance_lab_setup.sql](performance_lab_setup.sql). Run:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT ticket_id, subject, opened_at
FROM performance_lab.tickets
WHERE status = 'open'
ORDER BY opened_at DESC
LIMIT 20;
```

Keep the scan type, whether a sort appears, and the amount of row/page work in a
SQL comment. Run the baseline plan twice. Run the SELECT without EXPLAIN and save its twenty ticket IDs for
comparison. An optimization must preserve the answer.

The setup already runs `ANALYZE`, which refreshes planner statistics. Record
the scan's estimated rows once so you can notice any large change in the
estimate later. Do not add another statistics refresh while testing the index.

## 2. Add the Index and Rerun

```sql
CREATE INDEX tickets_status_opened_idx
ON performance_lab.tickets (status, opened_at DESC);
```

Run the **identical** query and analyzed plan again. Repeat the plan a second time.
Compare:

- the twenty result IDs, which should be unchanged;
- the scan and sort work before and after; and
- execution times across runs, without treating one fast measurement as a guarantee.

Measure storage with:

```sql
SELECT pg_size_pretty(
    pg_relation_size('performance_lab.tickets_status_opened_idx')
) AS index_size;
```

Read the index as tickets ordered by status, then by opening time within a
status. Restricting to `open` can make the newest matching entries directly
accessible. The plan decides whether PostgreSQL uses that path.

## 3. Make a Recommendation

Write a short update to the application developer in a SQL comment recommending
**keep**, **remove**, or **test further**.
Use one observation about preserved results, one about the query plan, and one
cost such as storage or additional work when indexed values change. Distinguish
the space you measured from write overhead you have not measured.

If you recommend removing it, run
`DROP INDEX performance_lab.tickets_status_opened_idx;` after saving your
observations. Keeping it in this disposable schema is also fine; the next fixture
reset removes it. Do not create a second identical index if you repeat the lab.

**Submit:** `week_07_index_decision.sql` with your before/after experiment and
recommendation. No separate benchmark report is required.

**If you finish early:** remove the status predicate and inspect that plan too.
Column order still matters, but do not claim that a multicolumn index can
*never* help a query on a later column. PostgreSQL version and selectivity affect
the choice, including skip-scan behavior in versions that support it.
[Official multicolumn-index documentation](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
explains that distinction. This extension is ungraded.
