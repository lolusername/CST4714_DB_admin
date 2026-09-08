# Lab 1: Count Requests Without Counting Them Twice

A summary says there are three active requests. That sounds correct, but the
pipeline counted one request twice and lost another. Find out how a plausible
total can hide an incorrect result.

Work individually in class. Submit one completed notebook in Brightspace.

## 1. Build and Check the Summary

Download [From Tickets to a Reliable Summary](../../notebooks/07_aggregation_validation.ipynb),
open [Colab](https://colab.research.google.com/), and choose **File > Upload
notebook**. Run the notebook in order. It supplies its own four-ticket case;
nothing from Week 10 needs to be retained.

Keep local mode on, or use your personal Atlas practice project with the notebook's
hidden credential prompt and temporary runtime-IP instructions.

The worked pipeline counts active tickets by category. Add **urgent count** and
**newest opening date**, using the supplied expressions. Inspect the actual ticket
IDs to check the streetlight result. Then run the `$unwind` example and explain
why its rows answer a different question. A matching grand total is insufficient.

## 2. Add One Rule and Explain the Result

The supplied validator allows optional fields but requires a valid ticket ID,
status, and subject. Add a required BSON `opened_at` date and rerun the validator
cell. Run the tests: accept an allowed date, reject an invalid status, reject a
date stored as text, and reject a missing date. Use Atlas or interpret the
explicitly labeled trace in local mode. Do not report the trace as a live server
test. The date cases appear only after you add the rule.

Complete the notebook's one explanation cell: your streetlight result and its
source IDs, the counting error, and what your date rule does and does not check.
Run cleanup when finished.

**Submit:** the notebook with your modified pipeline, validator, outputs, and
short explanation. No JavaScript file, repository, screenshot, or extra report
is required. Assignee sets and event analytics are optional extensions.
