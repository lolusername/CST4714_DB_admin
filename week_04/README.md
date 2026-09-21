# Week 4: Reliable SQL Reports

The view and migration lesson is now Week 3. This week extends it: count the
right records, select a latest event without losing requests, and test the
result before another person depends on it.

## Before Class: Assigned Reading

In [Operating Cloud Databases](../Operating_Cloud_Databases.pdf):

- **Before Day 1:** Chapter 2, **Diagnose Duplicate Rows**, **Group and Aggregate**,
  **Subqueries and CTEs Name Intermediate Relations**, and **Verification Is a
  Second Query or Reasoning Path**.
- **Before Day 2:** Chapter 4, **Views Create a Query Interface**. Then read the
  Day 2 explanations in the notebook. They introduce `ROW_NUMBER` from scratch;
  window functions are not assumed knowledge from the textbook.

Reading prepares the examples; no separate reading report is required.

## Class Materials

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_04/04_reliable_reporting.ipynb)

- [Guided notebook](04_reliable_reporting.ipynb)
- [PowerPoint with spoken script in its notes](week_04_reliable_sql_reports.pptx)
- [PDF handout](week_04_reliable_sql_reports.pdf)
- [Slide transcript](week_04_reliable_sql_reports_transcript.md)
- [Dataset and setup help](materials/datasets/metro_support/README.md)

The Colab notebook runs a disposable PostgreSQL database without a cloud account.
Supabase SQL Editor or PGlite can run the same SQL. Use one route. Save your SQL
outside the temporary runtime; the labs each require one SQL file, not another
notebook submission.

## Day 1: Count Requests, Not Ticket-Event Pairs

Use **slides 1-12** and the notebook's Day 1 sections. Introduce the data before
the first query: **8 users, 12 tickets, 21 events**. Ticket 1003 has three history
rows but is still one request. Read that example before grouping anything.

The worked examples explain `COUNT`, conditional counts with `FILTER`, CTEs,
pre-aggregation, `LEFT JOIN`, and meaningful checks. Complete
[Lab 1: Category workload report](lab_01_category_report.md) after the worked
category example. Submit `week_04_category_report.sql` in Brightspace.

## Day 2: Select One Latest Event Per Ticket

Use **slides 13-24** and the notebook's Day 2 sections. Inspect all ranked rows
before filtering `rn = 1`. We explain `PARTITION BY`, the ordering rule, the
outer-query filter, and why the last join must preserve the ticket population.

Complete [Lab 2: Latest-event queue](lab_02_latest_event.md). Submit
`week_04_latest_event.sql` in Brightspace. The two labs are individual.

The queries use the original fixture and do not depend on Week 3's new channel
column. An existing correct fixture is fine; a fresh isolated copy is also fine.
Never reset a project just to start a new week if it contains work you need.

## Reference and Reuse

PostgreSQL's [window-function tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
and [CTE documentation](https://www.postgresql.org/docs/current/queries-with.html)
provide further explanation. These are references, not additional assignments.

See [licenses](materials/LICENSE.md) and [attributions](materials/ATTRIBUTIONS.md).
