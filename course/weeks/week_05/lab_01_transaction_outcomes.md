# Lab 1: Assign a Ticket and Record Its History Together

Assigning a ticket changes its current state and creates a history event. If one
change persists without the other, the current record and history disagree.
Use a transaction to make the pair one unit of work.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Make an Isolated Practice Copy

Use your personal PostgreSQL/Supabase course database. If Metro Support is missing,
run its [setup](../../datasets/metro_support/postgres_setup.sql) first.

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
     'Assigned to Priya for follow-up', now());

SELECT ticket_id, assignee_id, status
FROM transaction_lab.tickets WHERE ticket_id = 1004;
SELECT event_id, ticket_id, new_status
FROM transaction_lab.ticket_events WHERE event_id = 5999;
ROLLBACK;
```

Before running the whole block together, predict what the two SELECTs inside it
will show. After it finishes, run those SELECTs again. The ticket should be back
to its starting state and event 5999 should be absent.

## 3. Keep the Approved Assignment

Run the same block with COMMIT in place of ROLLBACK. Query both tables again and
record the persistent assignee, status, and event ID.

Now test a failed pair. Ticket 1004's original priority is `low`. Run this block
only after the approved event 5999 exists:

```sql
BEGIN;
UPDATE transaction_lab.tickets
SET priority = 'urgent' WHERE ticket_id = 1004;
INSERT INTO transaction_lab.ticket_events (event_id, ticket_id)
VALUES (5999, 1004);
```

Expect a duplicate-primary-key error. Run `ROLLBACK;` separately after the error,
then query the ticket's priority and event 5999. The priority should still be
`low`, and the earlier approved event should still exist. This failure does not
undo a transaction that already committed.

Explain why the failed pair kept neither new change, and what could go wrong if
the UPDATE had committed separately before the failed insert. An UPDATE that
matches zero rows is different: it is valid SQL, so an application must check the
affected-row result before claiming that a requested assignment happened.

**Submit:** `week_05_transaction_outcomes.sql` with the isolated setup, rehearsal,
committed version, failed-pair test, and short explanation. Put observed results
in SQL comments. Keep the expected-error test and its separate rollback labeled
so a reader knows where execution pauses.

If rerunning your entire file, start with the disposable setup. If rerunning only
the committed block, the duplicate event ID will be rejected and the transaction
must be rolled back. A production retry policy needs more care; we return to
idempotency later in the course.
