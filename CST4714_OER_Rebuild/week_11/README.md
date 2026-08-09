# Week 11: Aggregation, Validation, and MongoDB Index Evidence

## The Week's Question

How can a MongoDB workload transform documents, reject invalid states, and prove
whether an index supports a filter and sort?

## What You Will Be Able to Do

- trace the document grain after every aggregation stage;
- use `$match`, `$unwind`, `$group`, `$project`, `$sort`, and `$limit`;
- add focused BSON schema validation;
- read `nReturned`, documents examined, keys examined, and plan stages; and
- connect a real case-study design decision to course evidence.

## Course OER

- [Module 11: MongoDB operations connect pipelines, rules, and indexes](../textbook/module_11_mongodb_operations.md)
- [Week 11 student deck](week_11_aggregation_validation_indexes.pptx)
- [Week 11 PDF handout](week_11_aggregation_validation_indexes.pdf)
- [Week 11 transcript](week_11_aggregation_validation_indexes_transcript.md)

## Free External Resources

- [Improving Performance of Sort Stages - Lab Only](https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only)
- [Building an Event-Driven Inventory Platform: A Case Study](https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13)

The case-study response appears only in Week 11.

## Day 1: Pipeline and Validation Studio

Complete [Lab 1: Trace a pipeline and reject one invalid document](lab_01_pipeline_validation.md).

Submit only `week_11_pipeline_validation.mongodb.js`.

## Day 2: Sort Performance and Career-Connected Case Writing

The instructor first demonstrates an index decision on a course dataset. Students
then complete a different guided performance lab and watch the inventory case.

Complete [Lab 2: Sort evidence and inventory case response](lab_02_sort_and_case_response.md).

Submit one Brightspace text response containing the completion image and writing.

## Optional Industry Extension: Leaderboard Pipeline Challenge

This activity is optional, ungraded, and does not add a submission.

Assume one MongoDB document per completed game with `player_id`, `mode`, `score`,
and `finished_at`. Write or sketch a pipeline that returns the top ten scores for
one mode and day. Add a unique tie-break field so repeated runs have deterministic
order, propose an index for the opening filter and sort, and name the evidence you
would inspect in `explain("executionStats")`. State why a fast leaderboard query
does not validate the score values themselves.

## End-of-Week Self-Check

Explain why aggregation, validation, and indexing answer three different questions
about the same workload.
