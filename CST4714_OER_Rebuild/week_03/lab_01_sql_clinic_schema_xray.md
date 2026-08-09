# Lab 1: SQL Clinic and Schema X-Ray

## Purpose

Prove that the SQL foundation is usable, then inspect the database as data instead
of relying on a dashboard or memory.

This is individual work completed in class. Submit one SQL file.

## 1. Rebuild and Query

Run the [Metro Support setup](../datasets/metro_support/postgres_setup.sql) in your
course database. Create `week_03_schema_xray.sql` and complete these three queries:

1. Return one row per resident, including residents with zero requested tickets,
   with resident name and request count.
2. Return one row per category with total tickets and unresolved tickets. Keep
   only categories with at least two total tickets.
3. Use `EXCEPT` to identify user IDs that requested a ticket but were never
   assigned one.

Before each query, add comments naming its relational operations and result grain.
After each query, add the expected row count.

## 2. Inspect the Actual Schema

Add metadata queries that answer:

1. Which columns, data types, nullability rules, and defaults exist on `tickets`?
2. Which named constraints exist on `tickets`, and what type is each?
3. Which indexes exist on `tickets`, including those created for keys?
4. Which columns in `tickets` participate in foreign keys, and which table and
   column does each reference?

Use `information_schema` for columns and constraints and `pg_indexes` for indexes.
Do not use screenshots as the primary evidence.

## 3. Record One Finding

End the file with a SQL comment containing:

- one integrity strength the schema already has;
- one invalid state it still permits; and
- one candidate query that might later justify an index.

Do not create the new constraint or index in this lab.

## Submit One Thing

Submit `week_03_schema_xray.sql`. It should run after the setup file and contain
three cumulative SQL queries, four metadata queries, and one evidence-based audit
comment.
