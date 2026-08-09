# Week 9: From Tables to Documents

## The Week's Question

If we designed a database system around today's workload, which relational ideas
would we keep, what might we change, and why?

## What You Will Be Able to Do

- explain the evolution of NoSQL as a response to varied workloads;
- compare key-value, wide-column, document, graph, and vector models;
- write strict JSON with objects, arrays, strings, numbers, booleans, and null;
- compare referenced, embedded, and hybrid document shapes; and
- create a free Atlas environment without exposing a database credential.

## Course OER

- [Module 9: Documents emerged from changing workloads](../textbook/module_09_nosql_json.md)
- [Metro Support CSV dataset](../datasets/metro_support/)
- [Week 9 student deck](week_09_nosql_models_json.pptx)
- [Week 9 PDF handout](week_09_nosql_models_json.pdf)
- [Week 9 transcript](week_09_nosql_models_json_transcript.md)

## Free External Resources

- [Getting Started with MongoDB Atlas](https://learn.mongodb.com/courses/getting-started-with-mongodb-atlas-smartbridge)
- [MongoDB and the Document Model](https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge)
- [GitHub online file editor documentation](https://docs.github.com/repositories/working-with-files/managing-files/editing-files)

These resources cost students nothing but are linked external resources, not
claimed as course-created OER.

## Day 1: Why Multiple Data Models Exist

We move from relational history to the workload pressures behind key-value,
wide-column, document, graph, and vector systems. The goal is not to rank models.
The goal is to match an abstraction to a question and name the operational cost.

The class ends by comparing graph paths, vector similarity, and a relational join
as three different meanings of "related."

## Day 2: JSON, Atlas, and Multiple Valid Designs

The instructor demonstrates free Atlas project setup and database-user/network
boundaries. Students then work individually with the three Metro Support CSVs.
No SQL or MQL is required this week.

Complete [Lab: Turn related CSV tables into two JSON designs](lab_01_csv_to_json.md).

Submit only `week_09_json_models.md`.

## Optional Industry Extension: JSON Interoperability Escape Room

This activity is optional, ungraded, and does not add a submission.

Classify each case as invalid JSON, valid but interoperability-dangerous, or valid
with application-defined meaning: single quotes, a trailing comma, `NaN`, the
number `01`, duplicate object names, and an ISO timestamp stored as a string.
Verify syntax with a standard parser, but explain why successful parsing does not
settle duplicate-name behavior, numeric precision, date semantics, or schema
quality. The goal is to separate grammar from a reliable data contract.

## End-of-Week Self-Check

Explain why "valid JSON," "good document model," and "stored BSON document" are
three different claims.
