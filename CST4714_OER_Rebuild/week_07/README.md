# Week 7: Query Plans, Evidence, and Index Design

## The Week's Question

How can we explain a query plan, test one index hypothesis, and decide whether the
benefit is worth the cost?

## What You Will Be Able to Do

- convert a slow-query complaint into a reproducible workload statement;
- distinguish estimated and actual plan evidence;
- recognize scan, sort, join, and aggregate nodes;
- compare estimated and actual row counts;
- test a composite index on a deterministic larger fixture; and
- write a keep/remove recommendation with a real tradeoff.

## Read and Use

- [Module 7: Performance work begins with evidence](../textbook/module_07_performance.md)
- [Performance fixture setup](performance_lab_setup.sql)
- [Week 7 student deck](week_07_query_plans_index_design.pptx)
- [Week 7 PDF handout](week_07_query_plans_index_design.pdf)
- [Week 7 transcript](week_07_query_plans_index_design_transcript.md)

## Day 1: Read the Plan Before Changing Anything

Complete [Lab 1: Build a plan-reading record](lab_01_plan_reading.md).

Submit only `week_07_plan_reading.sql`.

## Day 2: Test One Index Hypothesis

Complete [Lab 2: Measure, change, remeasure, decide](lab_02_index_experiment.md).

Submit only `week_07_index_decision.sql`.

## Optional Industry Extension: Machine-Readable Plan Detective

This activity is optional, ungraded, and does not add a submission.

Run one safe `SELECT` from the performance fixture with
`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`. Locate the top node, actual and
estimated rows, loops, shared-buffer evidence, planning time, and execution time.
Write a tiny SQL or Python expression that extracts one field, or simply annotate
the JSON in a text editor. Explain why a machine-readable plan helps regression
testing but still cannot decide by itself whether an index should remain.

## End-of-Week Self-Check

Explain why neither "sequential scan" nor "index scan" is automatically a good or
bad result.
