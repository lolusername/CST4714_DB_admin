# Week 11: Aggregation, Validation, and MongoDB Index Design

## The Week's Question

How can a MongoDB workload transform documents, reject invalid states, and show
whether an index supports a filter and sort?

## What You Will Be Able to Do

- trace the document grain after every aggregation stage;
- use `$match`, `$unwind`, `$group`, `$project`, `$sort`, and `$limit`;
- define focused BSON validation and distinguish a server test from a local trace;
- read `nReturned`, documents examined, keys examined, and plan stages; and
- connect a real case-study design decision to the workload and its results.

## Before Class: Assigned Reading

Use [Chapter 11: MongoDB Operations Connect Pipelines, Rules, and Indexes](../../textbook/module_11_mongodb_operations.md).

- **Before Day 1:** read the pipeline and validation sections. Trace the four-ticket case and the misleading equal totals after unwind.
- **Before Day 2:** read from **An Index Is an Ordered Access Path for a Workload** through **Validation and Indexing Solve Different Problems**. Use these ideas in the performance lab and case-study response.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Aggregation and validation notebook](../../notebooks/07_aggregation_validation.ipynb)
- [Open Colab](https://colab.research.google.com/), then **File > Upload notebook**
- [Week 11 student deck](week_11_aggregation_validation_indexes.pptx)
- [Week 11 PDF handout](week_11_aggregation_validation_indexes.pdf)
- [Week 11 transcript](week_11_aggregation_validation_indexes_transcript.md)

## Free External Resources

- [Improving Performance of $sort stages (Lab Only)](https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only)
- [Building an Event-Driven Inventory Platform: A Case Study](https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13)

The case-study response appears only in Week 11.

## Day 1: Pipeline and Validation Studio

Use **slides 1-16**. The worked example begins with four tickets and shows the
actual output after filtering, grouping, and projection. The second example
expands events and exposes why equal totals can still count different tickets.
The validation section distinguishes presence, BSON type, and allowed values.

Complete [Lab 1: Count Requests Without Counting Them Twice](lab_01_pipeline_validation.md).

Submit only the completed `07_aggregation_validation.ipynb` notebook. It includes
a fresh fixture, worked pipeline, array-counting trap, and one validation change
tested with an allowed date, text date, and missing date.

## Day 2: Sort Performance and Career-Connected Case Writing

Use **slides 17-28**. The instructor first demonstrates an index decision on a
separate 10,000-ticket synthetic dataset. Compare the same ordered result before
and after the index, including documents examined and the remaining fetch work.
Students then complete a different guided performance lab and watch the inventory
case. Slides 26 and 27 also link directly to those resources.

Complete [Lab 2: Sort performance and inventory case response](lab_02_sort_and_case_response.md).

Submit one Brightspace text response containing the completion image and writing.

## Optional Industry Extension: Leaderboard Pipeline Challenge

This activity is optional, ungraded, and does not add a submission.

Assume one MongoDB document per completed game with `player_id`, `mode`, `score`,
and `finished_at`. Write or sketch a pipeline that returns the top ten scores for
one mode and day. Add a unique tie-break field so repeated runs have deterministic
order, propose an index for the opening filter and sort, and name the measurements you
would inspect in `explain("executionStats")`. State why a fast leaderboard query
does not validate the score values themselves.

## End-of-Week Self-Check

Explain why aggregation, validation, and indexing answer three different questions
about the same workload.
