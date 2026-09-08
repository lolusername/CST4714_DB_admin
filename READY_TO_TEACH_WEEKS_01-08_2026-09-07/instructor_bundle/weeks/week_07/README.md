# Week 7: Query Plans and Index Design

## The Week's Question

How can we explain a query plan, test one index hypothesis, and decide whether the
benefit is worth the cost?

## What You Will Be Able to Do

- convert a slow-query complaint into a reproducible workload statement;
- distinguish estimated and actual plan rows;
- recognize scan, sort, join, and aggregate nodes;
- interpret loops and buffer counters without double-counting work;
- test a composite index on a deterministic larger fixture; and
- write a keep/remove/test-further recommendation with a real tradeoff.

## Before Class: Assigned Reading

Use [Chapter 7: Performance Work Begins With Measurement](../../textbook/module_07_performance.md).

- **Before Day 1:** read through **Selectivity Explains Many Scan Decisions**, including the actual plan excerpt and row-flow diagram.
- **Before Day 2:** read the B-tree, partial-index, cost, and worked-experiment sections. An improvement must preserve the returned ticket IDs.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Performance fixture setup](performance_lab_setup.sql)
- [Week 7 student deck](week_07_query_plans_index_design.pptx)
- [Week 7 PDF handout](week_07_query_plans_index_design.pdf)
- [Week 7 transcript](week_07_query_plans_index_design_transcript.md)

## Day 1: Read the Plan Before Changing Anything

Slides 1-12 teach the workload, actual row flow, plan measurements, and selectivity.
The demonstration uses twenty newest `in_progress` tickets in `performance_demo`.
Your lab uses `open` tickets in `performance_lab`, then changes the limit to test
whether fewer returned rows necessarily mean less scanning.

Complete [Lab 1: Why Does a Twenty-Row Result Read So Much Data?](lab_01_plan_reading.md).

Submit only `week_07_plan_reading.sql`.

## Day 2: Test One Index Hypothesis

Slides 13-24 explain B-tree ordering, composite and partial indexes, and a complete
before/after demonstration. The instructor tests a partial index for the
in-progress queue. You test a composite index for the open queue and write a
short recommendation from your own results.

Complete [Lab 2: Does This Index Earn Its Space?](lab_02_index_experiment.md).

Submit only `week_07_index_decision.sql`.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

## Optional Industry Extension: Machine-Readable Plan Detective

This activity is optional, ungraded, and does not add a submission.

Run one safe `SELECT` from the performance fixture with
`EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)`. Locate the top node, actual and
estimated rows, loops, shared-buffer activity, planning time, and execution time.
Write a tiny SQL or Python expression that extracts one field, or simply annotate
the JSON in a text editor. Explain why a machine-readable plan helps regression
testing but still cannot decide by itself whether an index should remain.

## End-of-Week Self-Check

Explain why neither "sequential scan" nor "index scan" is automatically a good or
bad result.
