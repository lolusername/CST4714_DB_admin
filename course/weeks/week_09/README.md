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

## Before Class: Assigned Reading

Use [Chapter 9: Documents Emerged From Changing Workloads](../../textbook/module_09_nosql_json.md).

- **Before Day 1:** read the history and model comparisons through **Specialized Models Trade Generality for Directness**. Work through the small graph and vector examples; no graph/vector deployment is required.
- **Before Day 2:** read from **JSON Became a Common Interchange Format** through **Worked Example: Compare Two Ticket Shapes**. No SQL, MQL, or Python execution is required for the JSON design lab.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Metro Support CSV dataset](../../datasets/metro_support/)
- [Week 9 student deck](week_09_nosql_models_json.pptx)
- [Week 9 PDF handout](week_09_nosql_models_json.pdf)
- [Week 9 transcript](week_09_nosql_models_json_transcript.md)

## Free External Resources

- [Getting Started with MongoDB Atlas](https://learn.mongodb.com/courses/getting-started-with-mongodb-atlas): orientation, especially the Atlas overview, deployment, and interface lessons. No completion screenshot is required this week.
- [MongoDB and the Document Model](https://learn.mongodb.com/courses/overview-of-mongodb-and-the-document-model): optional reinforcement of documents, types, and relationships. The full unit includes database operations that we begin in Week 10; completing the entire unit is not a Week 9 requirement.
- [Atlas Free cluster setup](https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/): the official setup reference. Use Free / M0 only; no payment card is needed for the course path.
- [GitHub online file editor documentation](https://docs.github.com/repositories/working-with-files/managing-files/editing-files)

These resources cost students nothing but are linked external resources, not
claimed as course-created OER.

Links and published lesson outlines checked September 8, 2026. A free learning
account may be required. The required lab works without these services.

## Day 1: Why Multiple Data Models Exist

We move from relational history to the workload pressures behind key-value,
wide-column, document, graph, and vector systems. The goal is not to rank models.
The goal is to match an abstraction to a question and name the operational cost.

**Slides 1-16:** recover the meaning of keys, follow a four-vertex dependency
graph, calculate cosine and Euclidean rankings for the same small vectors, and
compare models against specific reads. The closing individual design exercise
goes in your notes and adds no submission.

## Day 2: JSON, Atlas, and Multiple Valid Designs

**Slides 17-32:** learn JSON value kinds and punctuation, repair an invalid
example, and compare complete referenced and embedded versions of ticket 1001.
The instructor demonstrates GitHub's browser editor and free Atlas setup,
including the distinction between account access, database credentials, and the
client's source IP. Students then apply the worked method to ticket 1003 in the
three Metro Support CSVs. No SQL or MQL is required this week.

Complete [Lab: Turn related CSV tables into two JSON designs](lab_01_csv_to_json.md).

Submit only `week_09_json_models.md`.

## Optional Practice: JSON Interoperability

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
