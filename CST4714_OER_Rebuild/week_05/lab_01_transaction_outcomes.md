# Lab 1: Predict, Commit, and Roll Back

## Purpose

Make transaction boundaries visible by predicting each state, observing it inside
the transaction, and checking it again from a new statement after the decision.

This is individual work completed in class. Submit one SQL file.

## 1. Create an Isolated Copy

Create `week_05_transaction_outcomes.sql`. Build a disposable schema and copy the
ticket data:

```sql
DROP SCHEMA IF EXISTS transaction_lab CASCADE;
CREATE SCHEMA transaction_lab;

CREATE TABLE transaction_lab.tickets AS
SELECT * FROM metro_support.tickets;

ALTER TABLE transaction_lab.tickets
ADD PRIMARY KEY (ticket_id);
```

Verify the copy's row count and ticket 1004's starting assignee and status.

## 2. Roll Back One Unit of Work

Write an explicit transaction that assigns ticket 1004 and changes it to
`in_progress`. Before running, add a comment predicting what a query inside the
transaction will show and what a query after `ROLLBACK` will show.

Use `UPDATE ... RETURNING`, verify inside the transaction, roll back, and verify
the original state returned.

## 3. Commit One Unit of Work

Create `transaction_lab.ticket_events` as a copy of the event table. In one
transaction:

- update ticket 1004 to the approved assignee and status;
- insert one matching event with a new event ID; and
- verify both changes before committing.

After `COMMIT`, run fresh queries proving that both changes remain. Add a comment
explaining which ACID properties are visible and which cannot be completely proved
by this small exercise.

## Submit One Thing

Submit `week_05_transaction_outcomes.sql`. It should create an isolated copy,
demonstrate one rollback and one commit, include predictions, and verify each final
state.
