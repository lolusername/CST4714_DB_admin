# Week 10: MQL and Document Modeling

## The Week's Question

How do we query MongoDB documents safely and decide which related facts belong
together?

## What You Will Be Able to Do

- connect to Atlas through a credential-safe notebook or use the offline fallback;
- insert, find, project, sort, update, and delete test documents;
- query nested fields and arrays;
- interpret matched, modified, and deleted counts;
- choose embedding or referencing from access patterns and growth; and
- document one model's benefit and cost.

## Course OER

- [Module 10: MongoDB models the way an application reads](../textbook/module_10_mql_modeling.md)
- [Atlas MQL and modeling notebook](../notebooks/04_atlas_mql_modeling.ipynb)
- [Open the notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/04_atlas_mql_modeling.ipynb)
- [Week 10 student deck](week_10_mql_document_modeling.pptx)
- [Week 10 PDF handout](week_10_mql_document_modeling.pdf)
- [Week 10 transcript](week_10_mql_document_modeling_transcript.md)

## Free External Resources With Distinct Roles

- **Instructor live demonstration:** [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)
- **Student individual activity:** [Relational (SQL) to Document Model](https://learn.mongodb.com/courses/relational-to-document-model)

The instructor demonstration and student activity are intentionally different.
Students are not assigned the same MongoDB University activity used for live
coding.

## Day 1: Basic MQL in a Safe Collection

The instructor models filter, projection, nested fields, array queries, update
operators, write-result evidence, and exact cleanup.

Complete [Lab 1: Query and change documents safely](lab_01_atlas_mql.md).

Submit only the completed `04_atlas_mql_modeling.ipynb` notebook.

## Day 2: Model From Access Patterns

The instructor works through the separate **Modeling Data Relationships** free
resource as a live example. Students then complete the **Relational (SQL) to
Document Model** activity individually and apply it to Metro Support.

Complete [Lab 2: Translate one workload into a document model](lab_02_document_model.md).

Submit one Brightspace text response containing the required completion evidence,
JSON model, and explanation. Do not create an extra Markdown assignment file.

## Optional Industry Extension: Live-Service Game Inventory Model

This activity is optional, ungraded, and does not add a submission.

Design documents for a game that must load a player's equipped items in one read,
grant one item atomically, preserve an unbounded acquisition history, and maintain
one shared catalog description per item type. Sketch an embedded, referenced, or
hybrid design and mark every bounded and potentially unbounded array. Explain one
atomicity benefit, one duplication risk, and one query that would force you to
reconsider the boundary.

## End-of-Week Self-Check

Given one-to-many related data, explain when ownership, atomic update, shared
identity, independent queries, and unbounded growth point toward embedding or
referencing.
