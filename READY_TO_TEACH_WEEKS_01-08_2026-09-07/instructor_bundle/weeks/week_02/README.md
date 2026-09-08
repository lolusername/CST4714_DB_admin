# Week 2: Major SQL Review Studio

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

Use [Chapter 2: Relational Operations Become Testable SQL](../../textbook/module_02_sql.md).

- **Before Day 1:** read from **A Relation Represents One Kind of Fact** through **Join Related Facts**, plus **NULL Means Missing or Inapplicable**. Concentrate on filtering, choosing columns, ordering, missing values, and matching requester IDs. The join derivation and duplicate diagnosis are revisited on Day 2.
- **Before Day 2:** read **A Join Is a Filtered Product**, **Diagnose Duplicate Rows**, **Group and Aggregate**, **Worked Example: Staff Workload Including Zero Counts**, **Subqueries and CTEs Name Intermediate Relations**, and **Review Safe Data Changes**. Return to the NULL section when explaining unmatched rows.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Metro Support PostgreSQL setup](../../datasets/metro_support/postgres_setup.sql)
- [SQL and relational review notebook](../../notebooks/01_relational_sql_review.ipynb)
- [Open Colab](https://colab.research.google.com/), then **File > Upload notebook** using the downloaded file above.
- [Week 2 student deck](week_02_relational_algebra_sql_review.pptx)
- [Week 2 PDF handout](week_02_relational_algebra_sql_review.pdf)
- [Week 2 transcript](week_02_relational_algebra_sql_review_transcript.md)

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
