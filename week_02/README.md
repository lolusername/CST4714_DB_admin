# Week 2: Major SQL Review Studio

[Course home](../README.md) | [Previous: Week 1](../week_01/README.md)

## The Week's Question

How do relational operations become SQL that another person can run, verify, and
trust?

This week is a substantial prerequisite review. It does not assume that you
remember SQL from an earlier course.

## What You Will Be Able to Do

- translate selection, projection, join, union, and difference into SQL;
- state and preserve the intended result grain;
- filter, sort, calculate, and reason about `NULL`;
- choose inner or outer joins based on the question;
- group and aggregate without accidental duplication;
- use subqueries and CTEs to name intermediate results;
- perform a small `INSERT`, `UPDATE`, or `DELETE` inside a controlled transaction;
  and
- verify a result through an independent query or boundary case.

## Before Class: Assigned Reading

Read these free sections of the PostgreSQL tutorial. Its weather tables are
examples; our class uses the Metro Support data supplied below.

- **Before Day 1:** read [Querying a Table](https://www.postgresql.org/docs/current/tutorial-select.html) and [Joins Between Tables](https://www.postgresql.org/docs/current/tutorial-join.html), through the left outer join example. Focus on choosing rows and columns, ordering results, and matching identifiers.
- **Before Day 2:** read [Aggregate Functions](https://www.postgresql.org/docs/current/tutorial-agg.html) and [Transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html). Focus on what one grouped row represents and what `ROLLBACK` does.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Exercises on the linked documentation pages
are optional unless the weekly lab assigns them.

## Class Materials

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_02/01_relational_sql_review.ipynb)

Open the notebook, save a copy in Drive, and run the cells through
**Use the Complete Week 2 Lab Dataset** before starting either lab.

- [Metro Support PostgreSQL setup](data/postgres_setup.sql)
- [Dataset and CSV files](data/README.md)
- [SQL and relational review notebook](01_relational_sql_review.ipynb)
- [Week 2 student deck](week_02_relational_algebra_sql_review.pptx)
- [Week 2 PDF handout](week_02_relational_algebra_sql_review.pdf)

The notebook includes the data and runs DuckDB inside Colab. You do not need a
Supabase account or a database password. Before either lab, run **Use the Complete
Week 2 Lab Dataset** to load 8 users, 12 tickets, and 21 events. The earlier
worked demonstrations use a smaller instance.

If you already have a personal Supabase practice project, you can instead run
the setup file in its SQL Editor. It resets the `metro_support` practice schema.
Both paths support the same lab questions.

Use the notebook to run your queries. In each submitted `.sql` file, include
the SQL statements and `--` comments, leaving out Python wrappers such as
`con.sql(...).show()`. The notebook itself is practice material, not an extra
submission.

## Day 1: Query Ladder

We translate relational operations into `SELECT`, `FROM`, `WHERE`, `ORDER BY`,
expressions, and null-aware predicates, then match a ticket to its requester with
a join. Slides 1-10 cover this meeting. You will predict output before execution
and check one answer against the source data.

Complete [Lab 1: SQL query ladder](lab_01_sql_query_ladder.md).

The only submission is `week_02_sql_review.sql`.

## Day 2: Relationships, Summaries, and Safe Changes

We rebuild joins, grouping, aggregates, set operators, subqueries, CTEs, and safe
data changes. Slides 11-21 cover this meeting. The worked example counts resolved
tickets for every staff member, including a person with zero. You will adapt that
pattern to active work. The repeated question is: what does one output row
represent, and which independent check would reveal a mistake?

Complete [Lab 2: Join, summarize, and change safely](lab_02_joins_aggregates_dml.md).

The only submission is `week_02_relational_sql_studio.sql`.

## Optional Industry Extension: Equivalent-Query Detective

This activity is optional, ungraded, and does not add a submission.

Using Metro Support, answer one question twice with intentionally different SQL,
such as a join-and-group query and a correlated subquery. Before running either
query, predict the result grain and row count. Then compare stable identifiers,
not only the number of rows. If the answers differ, identify whether the cause is
`NULL`, duplicate multiplication, filter placement, or a genuinely different
question. Finish with one sentence naming which version would be easier for a
teammate to verify in a code review.

## End-of-Week Readiness Check

You are ready for schema administration when you can:

1. predict whether a query returns one row per ticket, event, user, or group;
2. explain why a left join preserves an unmatched row;
3. distinguish `count(*)` from `count(column)`;
4. verify a grouped result with a simpler query; and
5. protect an update with a target preview, transaction, `RETURNING`, and
   verification.

Week 3 begins with a cumulative SQL clinic. It is another chance to repair gaps
before new schema-management material begins.
