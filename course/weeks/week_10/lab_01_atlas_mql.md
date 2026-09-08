# Lab 1: Find and Change the Right Document

A support tool must update one request without changing everybody else's data.
Practice the filters and write operators that make that possible.

Work individually in class. Submit one completed notebook.

## 1. Query the Supplied Tickets

Download [Atlas MQL and Modeling](../../notebooks/04_atlas_mql_modeling.ipynb),
open [Colab](https://colab.research.google.com/), and choose **File > Upload notebook**.

The local path works without an account. The Atlas path uses your own Free cluster,
a hidden connection-URI prompt, a temporary runtime-IP rule, and a unique practice
database. Keep certificate verification enabled.

Run the worked filters, projections, nested-field queries, and array
counterexample. Change one filter and one projection so the result answers a
different question. Name one returned ticket and explain why it belongs.

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
