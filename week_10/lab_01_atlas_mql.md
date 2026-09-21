# Lab 1: Find and Change the Right Document

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_10/lab_01_atlas_mql.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/04_atlas_mql_modeling.ipynb)

A support tool must update one request without changing everybody else's data.
Practice the filters and write operators that make that possible.

Work individually in class. Submit one completed notebook.

## 1. Query the Supplied Tickets

Click **Open in Colab** above and save a working copy in Drive. The
[downloadable notebook](materials/notebooks/04_atlas_mql_modeling.ipynb) also supports local Jupyter.

The local path works without an account. The Atlas path uses your own Free cluster,
a hidden connection-URI prompt, a temporary runtime-IP rule, and a unique practice
database. Keep certificate verification enabled.

Run the SQL-to-MongoDB comparison in Section 2. Both queries ask for active
high/urgent tickets and return the same ticket ID and status. The SQL example
uses a temporary SQLite table made from these six documents, so it needs no
second account. Notice how WHERE, selected columns, and ORDER BY become a filter,
a projection, and a sort.

Then complete **Your Turn: The Crew's Work Queue**. The lighting and sanitation
crews need **active streetlight or sanitation tickets, newest first**, with each
ticket's priority displayed. Add the active-status condition and priority field
to the working starter. Medium-priority work belongs in this queue too.

Predict the ticket IDs from the six documents before running your query. Compare
the output with that prediction, and explain why ticket 1005 should be absent
even though it is a high-priority sanitation request. Continue with the worked
nested-field and array queries.

Compare the separate array conditions with `$elemMatch`. Use the actual event
objects to explain why one query can match conditions in different elements and
the other cannot.

## 2. Update, Repeat, and Read Back

Run the test-ticket setup once, then run the same `$set` update cell twice without
rerunning the setup between updates. Compare the matched and modified counts,
then inspect the saved document. Continue through the expected-state and event
examples. Run the narrowly targeted test deletion and its verification.

Complete the notebook's one explanation cell, using your results. Then run
cleanup. Later weeks supply fresh fixtures, so you do not need to retain this
database or pay for a service.

**Submit:** the notebook with your query changes, output, and short explanation.
No additional model report or Atlas screenshot is required. Day 2 develops the
embedding/referencing design.
