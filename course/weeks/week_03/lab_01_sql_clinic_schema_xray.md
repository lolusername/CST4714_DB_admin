# Lab 1: Inspect a Database Before Changing It

A new developer asks whether a ticket can reference a missing person and whether
the database rejects misspelled statuses. Answer by inspecting the actual schema.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Check the Starting Data

Run the [Metro Support setup](../../datasets/metro_support/postgres_setup.sql) in
your personal Supabase or PostgreSQL practice database. It resets that practice
schema. Confirm **8 users, 12 tickets, and 21 events**.

Write a query returning one row per category with total tickets and active tickets
(`new`, `open`, or `in_progress`). Start from:

```sql
SELECT category, count(*) AS total_tickets
FROM metro_support.tickets
GROUP BY category
ORDER BY category;
```

Use the worked resolved-ticket report on slide 2 of the
[Week 3 deck](week_03_schemas_constraints_integrity.pptx) as your model.
`FILTER` limits the rows counted by that one aggregate; it does not remove the
category from the result. Add
`count(*) FILTER (WHERE status IN (...)) AS active_tickets`, replacing `...` with
the three quoted active-status values above. The totals across
the report should add to 12 tickets and 7 active tickets. This is a quick SQL review,
not a second submission.

## 2. Ask the Database About Its Structure

Run this worked metadata query:

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'metro_support' AND table_name = 'users'
ORDER BY ordinal_position;
```

`information_schema` contains descriptions of database objects. The result
describes columns, not users. Change the table filter to inspect `tickets`.

Then inspect its rules and indexes:

```sql
SELECT conname AS constraint_name, contype AS kind,
       pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'metro_support.tickets'::regclass
ORDER BY conname;

SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'metro_support' AND tablename = 'tickets';
```

Constraint kinds include `p` (primary key), `f` (foreign key), and `c` (check).
The `::regclass` expression identifies the named table in PostgreSQL's catalog.

Keep these queries in your file. Use their actual output to answer:

- What stops a ticket from naming a nonexistent requester?
- How can you tell that an unassigned ticket is allowed?
- Does a rule currently restrict status to the approved words?

## 3. Recommend One Change

Write a short SQL comment naming one invalid state the baseline still permits and
the database rule you would add. Include the relevant current definition or
missing rule from your inspection. You will implement the change in the next lab.

**Submit:** `week_03_schema_xray.sql`, containing your category report, metadata
queries, and answers as comments. A few relevant output values are enough; do not
paste entire screens or every catalog row.
