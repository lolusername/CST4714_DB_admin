# Lab 1: Assign a Ticket and Record Its History Together

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_05/lab_01_transaction_outcomes.md)

Assigning a ticket changes its current state and creates a history event. If one
change persists without the other, the current record and history disagree.
Use a transaction to make the pair one unit of work.

Work individually in class. Submit one SQL file in Brightspace.

In the Supabase SQL editor, select and run **one complete SQL block at a time**.
Run the dataset setup and practice-copy setup separately from the experiments.
Keep each transaction together in one run. The expected-error block stops at its
failing INSERT; run its cleanup block next. Do not run the entire lab as one batch.

## 1. Make an Isolated Practice Copy

Use your personal PostgreSQL/Supabase course database. If Metro Support is missing,
run its [setup](materials/datasets/metro_support/postgres_setup.sql) first.

```sql
DROP SCHEMA IF EXISTS transaction_lab CASCADE;
CREATE SCHEMA transaction_lab;
CREATE TABLE transaction_lab.tickets AS
SELECT * FROM metro_support.tickets;
CREATE TABLE transaction_lab.ticket_events AS
SELECT * FROM metro_support.ticket_events;
ALTER TABLE transaction_lab.tickets ADD PRIMARY KEY (ticket_id);
ALTER TABLE transaction_lab.ticket_events ADD PRIMARY KEY (event_id);

SELECT ticket_id, assignee_id, status
FROM transaction_lab.tickets WHERE ticket_id = 1004;
```

Expect ticket 1004 to be unassigned and `new`. CREATE TABLE AS copies query
results, not all source constraints; the two primary keys above are explicit.
These disposable tables are separate from the source data.

## 2. Rehearse One Assignment

The proposed assignee is agent **201**. Here is the complete state change:

```sql
BEGIN;
UPDATE transaction_lab.tickets
SET assignee_id = 201, status = 'in_progress'
WHERE ticket_id = 1004 AND status = 'new'
RETURNING ticket_id, assignee_id, status;

INSERT INTO transaction_lab.ticket_events
    (event_id, ticket_id, actor_id, event_type, old_status, new_status, note, event_at)
VALUES
    (5999, 1004, 201, 'status_changed', 'new', 'in_progress',
     'Assigned to Agent 201 for follow-up', now());

SELECT ticket_id, assignee_id, status
FROM transaction_lab.tickets WHERE ticket_id = 1004;
SELECT event_id, ticket_id, new_status
FROM transaction_lab.ticket_events WHERE event_id = 5999;
ROLLBACK;
```

Before running the whole block together, predict what the two SELECTs inside it
will show: ticket 1004 assigned to 201 and event 5999 present. Those are observations
inside the transaction. After it finishes, run these queries separately:

```sql
SELECT ticket_id, assignee_id, status
FROM transaction_lab.tickets WHERE ticket_id = 1004;
SELECT event_id, ticket_id, new_status
FROM transaction_lab.ticket_events WHERE event_id = 5999;
```

The ticket should be back to its starting state and event 5999 should be absent.

## 3. Keep the Approved Assignment

Run this complete transaction to keep the assignment:

```sql
BEGIN;
UPDATE transaction_lab.tickets
SET assignee_id = 201, status = 'in_progress'
WHERE ticket_id = 1004 AND status = 'new'
RETURNING ticket_id, assignee_id, status;

INSERT INTO transaction_lab.ticket_events
    (event_id, ticket_id, actor_id, event_type, old_status, new_status, note, event_at)
VALUES
    (5999, 1004, 201, 'status_changed', 'new', 'in_progress',
     'Assigned to Agent 201 for follow-up', now());
COMMIT;
```

Run the two verification queries from step 2 again. Expect ticket 1004 assigned
to **201**, status **in_progress**, and event **5999** present. A COMMIT issued
after a completed ROLLBACK cannot recover the discarded changes; the UPDATE and
INSERT must run again in the new transaction above.

## 4. Observe a Failed Pair

Ticket 1004's original priority is `low`. Event **5001** already exists in the
copied setup data. This test attempts to insert that entire existing row again,
so the duplicate-key error does not depend on whether event 5999 was committed.

```sql
BEGIN;
UPDATE transaction_lab.tickets
SET priority = 'urgent' WHERE ticket_id = 1004;
INSERT INTO transaction_lab.ticket_events
SELECT * FROM transaction_lab.ticket_events WHERE event_id = 5001;
```

Expect a duplicate-primary-key error naming **5001** (SQLSTATE `23505`).
After the error, run this cleanup and verification block separately:

```sql
ROLLBACK;
SELECT ticket_id, assignee_id, status, priority
FROM transaction_lab.tickets WHERE ticket_id = 1004;
SELECT event_id, ticket_id, new_status
FROM transaction_lab.ticket_events
WHERE event_id IN (5001, 5999)
ORDER BY event_id;
```

After completing step 3, expect **201, in_progress, low** for ticket 1004 and
one row each for events **5001** and **5999**. The failed transaction keeps neither
the new priority nor a duplicate event. It does not undo the assignment or event
that already committed. If testing this block before step 3, the duplicate error
still occurs, but event 5999 remains absent and the ticket remains unassigned.

## 5. Compare an Outdated Assignment Request

Complete step 3 before this test and verify its stored results. Agent 201 already
has the ticket, but another request still assumes its status is `new`. Predict
the two results, then run this whole block:

```sql
BEGIN;
UPDATE transaction_lab.tickets
SET assignee_id = 202, status = 'in_progress'
WHERE ticket_id = 1004 AND status = 'new'
RETURNING ticket_id, assignee_id, status;

SELECT ticket_id, assignee_id, status
FROM transaction_lab.tickets WHERE ticket_id = 1004;
ROLLBACK;
```

The UPDATE should return **no rows**, without an SQL error. The SELECT should
still show **201, in_progress**. We deliberately do not insert an event in this
probe. A program that announced an assignment to Agent 202 merely because no exception
occurred would report a change that never happened.

In your SQL comments, explain why the failed pair kept neither new change and
what could go wrong if its UPDATE committed separately. Then write one sentence
to the application developer: which result must the assignment code check before
it records history or tells the caller that the assignment succeeded? A zero-row
result calls for examining the current record; by itself it cannot distinguish
an outdated status from a missing ticket.

**Submit:** `week_05_transaction_outcomes.sql` with the isolated setup, rehearsal,
committed version, failed-pair and zero-row tests, and short explanation. Put observed results
in SQL comments. Keep the expected-error test and its separate rollback labeled
so a reader knows where execution pauses.

To restart the lab, run the disposable setup separately, then run the blocks in
order again. If rerunning only the committed block, the duplicate event 5999
will be rejected and the transaction must be rolled back. A production retry
policy needs more care; we return to idempotency later in the course.
