# Lab 1: Build a Plan-Reading Record

## Purpose

Read estimated and actual plan evidence before adding an index or changing the
query.

This is individual work completed in class. Submit one SQL file.

## 1. Establish the Workload

Run [`performance_lab_setup.sql`](performance_lab_setup.sql). Create
`week_07_plan_reading.sql` and verify that the fixture contains 100,000 rows and
2,000 open rows.

The workload is:

> Return the twenty newest open tickets with ticket ID, subject, and opening time.

Write the query and add comments naming its result grain, expected maximum result
count, filter, order, and limit.

## 2. Compare Estimate and Execution

Run plain `EXPLAIN`, then `EXPLAIN (ANALYZE, BUFFERS)` on the identical `SELECT`.
In comments, record:

- scan node;
- estimated and actual rows at the scan;
- whether a sort appears and its method;
- rows returned by the top node;
- planning and execution time; and
- buffer evidence you can interpret safely.

Then run an analyzed plan for `SELECT count(*) FROM performance_lab.tickets;` and
explain why a sequential scan can be reasonable when the query needs every row.

## 3. State One Hypothesis

Without creating an index, propose one composite index for the newest-open-ticket
workload. Predict which scan or sort work it might change and name one cost.

## Submit One Thing

Submit `week_07_plan_reading.sql`. Keep plan observations as concise SQL comments;
do not paste an unreadable full-screen screenshot.
