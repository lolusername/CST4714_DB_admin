# Week 5: Transactions and Concurrency

## The Week's Question

What happens when two sessions act at the same time, and how can evidence reveal
who is waiting on whom?

## What You Will Be Able to Do

- predict and verify commit and rollback outcomes;
- connect ACID to observable database behavior;
- explain MVCC snapshots and row versions at a beginner level;
- distinguish waiting, blocking, and deadlock; and
- diagnose and resolve a controlled block using session evidence.

## Read and Use

- [Module 5: Transactions coordinate competing work](../textbook/module_05_transactions.md)
- [Transactions and locks notebook](../notebooks/02_postgres_transactions_locks.ipynb)
- [Open the notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/02_postgres_transactions_locks.ipynb)
- [Week 5 student deck](week_05_transactions_mvcc_locks.pptx)
- [Week 5 PDF handout](week_05_transactions_mvcc_locks.pdf)
- [Week 5 transcript](week_05_transactions_mvcc_locks_transcript.md)

## Day 1: Transaction Outcomes

Complete [Lab 1: Predict, commit, and roll back](lab_01_transaction_outcomes.md).

Submit only `week_05_transaction_outcomes.sql`.

## Day 2: Controlled Blocking Incident

Complete [Lab 2: Diagnose one blocking relationship](lab_02_blocking_incident.md).

Submit only the completed `02_postgres_transactions_locks.ipynb` notebook. The
credential prompt does not save your connection string in the file.

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
