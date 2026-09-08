# Lab 2: Make Misspelled Statuses Impossible

A ticket marked `IN PROGRESS` can disappear from a report that searches for
`in_progress`. Add rules that prevent this problem at every database write path.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Inspect and Add the Rules

Use a fresh [Metro Support setup](../../datasets/metro_support/postgres_setup.sql)
in your personal practice database. Do not reset a project used for other work.

Inspect existing status and priority values before adding a rule:

```sql
SELECT status, count(*)
FROM metro_support.tickets
GROUP BY status ORDER BY status;
```

Repeat the query for `priority`. Here is a complete example for the priority rule:

```sql
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_priority_allowed
CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
```

Write the matching status constraint, named `tickets_status_allowed`, allowing
`new`, `open`, `in_progress`, `resolved`, and `closed`.

If a constraint already exists, inspect it before running ADD again. Keep the
setup reset separate from your submitted solution.

## 2. Test Rejection and Acceptance

Run each of these statements **separately**. Each should fail without changing
the row:

```sql
UPDATE metro_support.tickets
SET priority = 'extreme' WHERE ticket_id = 1004;
```

```sql
UPDATE metro_support.tickets
SET status = 'IN PROGRESS' WHERE ticket_id = 1004;
```

In your submitted file, leave these expected-failure statements commented out and
record the constraint name from each error. If your editor reports an aborted
transaction, run `ROLLBACK;` before continuing.

Now run this valid change and rollback together:

```sql
BEGIN;
UPDATE metro_support.tickets
SET priority = 'high', status = 'in_progress'
WHERE ticket_id = 1004
RETURNING ticket_id, priority, status;
ROLLBACK;

SELECT ticket_id, priority, status
FROM metro_support.tickets WHERE ticket_id = 1004;
```

The final state should still be `low` and `new`. A useful rule must accept valid
values as well as reject invalid ones.

## 3. Explain What You Protected

Inspect the saved definitions:

```sql
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'metro_support.tickets'::regclass
  AND conname IN ('tickets_priority_allowed', 'tickets_status_allowed');
```

Add two or three sentences explaining why this protects imports and scripts as
well as the web form, and name one rule it does not enforce. For example, a list
of valid statuses alone does not establish who may close a ticket.

**Submit:** `week_03_integrity_build.sql` containing your constraints, test
statements, short error records, and explanation. No index experiment or separate
report is required. Week 7 will test index performance.
