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

Use [Chapter 5: Transactions Coordinate Competing Work](../../textbook/module_05_transactions.md).

- **Before Day 1:** read from **A Transaction Is a Unit of Decision** through **ACID Describes Guarantees, Not a Product Label**, including the state/history pair and zero-row UPDATE discussion.
- **Before Day 2:** read from **Concurrency Creates Useful Work and New Questions** through **Safe Incident Communication**. Follow the visible row versions, blocker, waiter, and final state. The on-call/write-skew example is enrichment; the lab does not require implementing isolation protocols.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Transactions and locks notebook](../../notebooks/02_postgres_transactions_locks.ipynb)
- [Open Colab](https://colab.research.google.com/), then **File > Upload notebook** using the downloaded file above.
- [Week 5 student deck](week_05_transactions_mvcc_locks.pptx)
- [Week 5 PDF handout](week_05_transactions_mvcc_locks.pdf)
- [Week 5 transcript](week_05_transactions_mvcc_locks_transcript.md)

## Day 1: Transaction Outcomes

Slides 1-9 teach the complete assignment rehearsal, its stored outcomes, a failed
pair, and the distinction between an error and an UPDATE that matches no rows.
The instructor's example assigns Noah and ends with rollback in the source
schema. Your lab uses Priya and separate disposable tables.

Complete [Lab 1: Assign a ticket and record its history together](lab_01_transaction_outcomes.md).

Submit only `week_05_transaction_outcomes.sql`.

## Day 2: Controlled Blocking Incident

Slides 10-23 introduce sessions, MVCC, isolation, activity diagnostics, and the
consequences of ending a blocking transaction. The instructor demonstrates the
notebook's rollback case. You predict and test the commit alternative, keeping
the fixture and competing update unchanged.

Complete [Lab 2: The query finished, but which change survived?](lab_02_blocking_incident.md).

Submit only the completed `02_postgres_transactions_locks.ipynb` notebook. The
credential prompt does not save your connection string in the file.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

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
