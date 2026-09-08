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

## Before Class: Assigned Reading

Use [Chapter 10: MongoDB Models the Way an Application Reads](../../textbook/module_10_mql_modeling.md).

- **Before Day 1:** read the connection, BSON, CRUD, and nested/array-query sections. Pay attention to whether a listing is shell JavaScript or notebook Python.
- **Before Day 2:** read from **Single-Document Atomicity Shapes Modeling** through **More Than One Model Can Be Valid**. Use the workload to explain embedding and referencing.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Atlas MQL and modeling notebook](../../notebooks/04_atlas_mql_modeling.ipynb)
- [Open Colab](https://colab.research.google.com/), then **File > Upload notebook** using the downloaded file above.
- [Week 10 student deck](week_10_mql_document_modeling.pptx)
- [Week 10 PDF handout](week_10_mql_document_modeling.pdf)
- [Week 10 transcript](week_10_mql_document_modeling_transcript.md)

## Free External Resources With Distinct Roles

- **Instructor live demonstration:** [Modeling Data Relationships: Lesson 3, Modeling One-to-One](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-3-modeling-one-to-one/learn). The instructor works the one-to-one example and its Practice activity, not Lesson 4.
- **Student individual activity:** [Modeling Data Relationships: Lesson 4, Modeling One-to-Many](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn), followed by [Lesson 4: Practice](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1).
- **Optional workload support:** [Identifying Reads and Writes](https://learn.mongodb.com/learn/course/relational-to-document-model/relational-to-document-model/model-for-workloads?page=3), a video within Relational (SQL) to Document Model. It is not an interactive lab or an extra submission.

These are different lessons and practice activities within one free course.
Students do not repeat the instructor's one-to-one activity. Some MongoDB
University courses reuse videos under different course names, so this week's
boundary is the specific lesson, not a claim that different titles mean new work.

## Day 1: Basic MQL in a Safe Collection

Use **slides 1-17**. The instructor models filter, projection, nested fields, array queries, update
operators, write-result counts, and exact cleanup.

Complete [Lab 1: Query and change documents safely](lab_01_atlas_mql.md).

Submit only the completed `04_atlas_mql_modeling.ipynb` notebook.

## Day 2: Model From Access Patterns

Use **slides 18-28**. The instructor demonstrates **Lesson 3: Modeling One-to-One** and a ticket-page
read. Students complete **Lesson 4: Modeling One-to-Many**, including its
interactive **Practice**, then revise their Week 9 ticket design for a new
requirement: the page needs only the latest two events, but the system must retain
all history and update contact information in one place. No complete course badge
or validation unit is required this week.

Complete [Lab 2: Translate one workload into a document model](lab_02_document_model.md).

Submit the JSON, explanation, and Lesson 4 Practice progress image in one Brightspace
text response. The lab describes the fallback if the external platform is down.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

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
