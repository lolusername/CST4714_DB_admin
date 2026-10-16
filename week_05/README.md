# Week 5: Transactions and Concurrency

## The Week's Question

What happens when two sessions act at the same time, and how can PostgreSQL's
session and lock views reveal who is waiting on whom?

## What You Will Be Able to Do

- predict and verify commit and rollback outcomes;
- connect ACID to observable database behavior;
- explain MVCC snapshots and row versions at a beginner level;
- distinguish waiting, blocking, and deadlock; and
- diagnose and resolve a controlled block using session and lock state.

## Before Class: Assigned Reading

Read the [textbook corrections](../COURSE_CORRECTIONS.md) with the assigned sections.

Use [Chapter 5: Transactions Coordinate Competing Work](../Operating_Cloud_Databases.pdf).

supasbase password encoding: https://supabase.com/docs/guides/database/connecting-to-postgres

- **Before Day 1:** read from **A Transaction Is a Unit of Decision** through **ACID Describes Guarantees, Not a Product Label**, including the state/history pair and zero-row UPDATE discussion.
- **Before Day 2:** read from **Concurrency Creates Useful Work and New Questions** through **Safe Incident Communication**. Follow the visible row versions, blocker, waiter, and final state. The on-call/write-skew example is enrichment; the lab does not require implementing isolation protocols.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Transactions and locks notebook](materials/notebooks/02_postgres_transactions_locks.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_05/materials/notebooks/02_postgres_transactions_locks.ipynb) for Lab 2; save a working copy in Drive.
- [Week 5 student deck](week_05_transactions_mvcc_locks.pptx)
- [Week 5 PDF handout](week_05_transactions_mvcc_locks.pdf)
- [Week 5 transcript](week_05_transactions_mvcc_locks_transcript.md)

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 5 videos](videos/README.md).

- [One assignment, one transaction](videos/01_transaction_boundary.mp4) (1:28): Assigning ticket 1004 changes the ticket and writes event 5998, so both belong in one transaction. Watch ROLLBACK and COMMIT end it, a duplicate-key error fail the pair, and an UPDATE match zero rows without any error.
- [Row versions and snapshots](videos/02_mvcc_row_versions.mp4) (1:22): An UPDATE to ticket 1004 writes a new row version stamped with transaction IDs. See which version each session reads before and after the commit, and why VACUUM can reclaim the old version only when no snapshot needs it.
- [Who is waiting on whom?](videos/03_blocking_and_deadlock.mp4) (1:28): Session A updates ticket 1004 and leaves its transaction open, so Session B waits. A third session uses pg_blocking_pids to find the blocker, and ending A decides which data survives. A deadlock is different: it is a cycle that PostgreSQL breaks by aborting one transaction.

<!-- videos:end -->

## Day 1: Transaction Outcomes

Slides 1-9 teach the complete assignment rehearsal, its stored outcomes, a failed
pair, and the distinction between an error and an UPDATE that matches no rows.
The instructor's example assigns Agent 202 and ends with rollback in the source
schema. Your lab uses Agent 201 and separate disposable tables. After committing
that assignment, you test an outdated request to assign the same ticket to Agent 202.
Read both the empty UPDATE result and the unchanged current record before
deciding what an application should tell its caller.

Complete [Lab 1: Assign a ticket and record its history together](lab_01_transaction_outcomes.md).

Submit only `week_05_transaction_outcomes.sql`.

## Day 2: Controlled Blocking Incident

Slides 10-25 introduce sessions, MVCC, isolation, activity diagnostics, and the
consequences of ending a blocking transaction. The instructor demonstrates the
notebook's rollback case. You predict and test the commit alternative, keeping
the fixture and competing update unchanged.

**Before the diagnostic query:** a PostgreSQL session uses a server process
called a backend. Its **PID** is that process identifier, not a user or ticket
ID. `SELECT pg_backend_pid();` identifies the backend for the connection running
the query. In slides **15-16**, read the waiting session's `pg_blocking_pids`
list to find its blockers. The notebook captures these IDs from its own open
connections; a later SQL Editor request may use a different backend.

**First-time connection:** slides **20-22** and the notebook's **First-Time Setup:
Colab and Supabase** explain how the tools fit together, how to prepare the
Session pooler URL, and what confirms the connection and starting row.

Complete [Lab 2: The query finished, but which change survived?](lab_02_blocking_incident.md).

Submit the sharing link to your completed Colab notebook in Brightspace, as
stated in Lab 2. The credential prompt does not save your connection string
in the file.

For support with the lab's explanation, use [Writing About Database Decisions](materials/assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

## Optional Industry Extension: Deadlock Detective

This activity is optional, ungraded, and does not add a submission.

Draw a wait-for graph for this incident: Transaction A locks ticket 1001 and then
requests ticket 1002; Transaction B locks ticket 1002 and then requests ticket
1001. Mark every held and requested resource, identify the cycle, and predict why
PostgreSQL must abort one transaction rather than wait forever. Then write one
application-level prevention rule and one retry requirement. This is a paper or
text-editor exercise; do not create the deadlock in a shared database.

## End-of-Week Self-Check

Given a blocked PID, explain how you would identify the blocking PID, determine
the transaction's owner and age, resolve the controlled lab safely, and verify the
final row state.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
