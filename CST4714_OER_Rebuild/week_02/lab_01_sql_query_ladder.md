# Lab 1: SQL Query Ladder

## Purpose

Rebuild basic SQL through prediction, execution, and verification. Every step uses
the same Metro Support data, so you can focus on reasoning instead of setup.

This is individual work completed in class. Submit one SQL file.

## 1. Set Up and Prove the Starting State

Open Supabase SQL Editor in a personal course project. Run
[`postgres_setup.sql`](../datasets/metro_support/postgres_setup.sql).

Create a new editor tab and save your work as `week_02_sql_review.sql`. Begin with
the following comment block and fill it in after setup:

```sql
/*
Environment: [Supabase project or approved PostgreSQL environment]
Expected counts: users = 8, tickets = 12, ticket_events = 21
Observed counts: [write the three counts]
Setup verified because: [one sentence]
*/
```

If the cloud editor is unavailable, use the course notebook and identify DuckDB
as the environment in your comment.

## 2. Complete the Query Ladder

For every query, add two comments before the SQL:

```sql
-- Grain: one row per ...
-- Prediction: ...
```

Write and run these five queries:

1. Return `ticket_id`, `subject`, `priority`, and `opened_at` for high or urgent
   tickets, newest first.
2. Return unassigned tickets. Use the correct null predicate and explain in a
   comment why `= NULL` is wrong.
3. Return active tickets opened by residents in the `Harbor` neighborhood. The
   result requires a relationship between tickets and users.
4. Return each ticket's age in days relative to the latest `opened_at` in this
   dataset. Use the dataset's maximum date rather than the current date so the
   result is reproducible.
5. Return the distinct categories that have at least one unresolved ticket. State
   why duplicate removal is or is not part of the question.

Use explicit column names rather than `SELECT *`.

## 3. Verify One Result Independently

Choose Query 3 or Query 5. Add a simpler verification query that checks one known
neighborhood or category. Then add this comment:

```sql
-- Verification conclusion: ...
-- This check does not prove: ...
```

The verification must reason independently; do not merely paste the same query a
second time.

## Submit One Thing

Download or copy the completed SQL into your course repository as
`week_02/week_02_sql_review.sql`. Submit that one file in Brightspace.

Your file should run from top to bottom after the setup script, contain five
queries, name each result grain, and include one independent verification.
