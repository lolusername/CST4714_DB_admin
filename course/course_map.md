# Course Map: Skills and Learning Progression

## Course-Level Outcomes

By the end of the course, a student can:

1. build and explain a small relational or document data model that matches a
   stated workload;
2. write basic SQL and MongoDB queries using managed cloud interfaces;
3. protect data with constraints, roles, grants, row-level policies, validation,
   and safe secret handling;
4. investigate transactions, locks, query plans, indexes, and common performance
   problems;
5. create a logical backup and complete or rehearse a restore;
6. explain replication, consistency, availability, sharding, and polyglot design
   as engineering tradeoffs; and
7. present database work clearly in documentation, demonstrations, portfolios,
   and interviews.

## Learning Progression

The course follows Metro Support, a fictional public-service help desk with
users, tickets, ticket events, changing metadata, access boundaries, reporting
needs, and reliability risks. Students first represent the system relationally,
then reconsider parts of it as documents. Reusing one case keeps setup small and
makes the technical differences easier to see.

| Stage | Weeks | Main development |
|---|---:|---|
| Rebuild the foundation | 1-3 | Refresh relational thinking and SQL before administration work assumes fluency |
| Build and operate PostgreSQL | 4-8 | Change schemas, coordinate transactions, control access, tune queries, and rehearse recovery |
| Move from tables to documents | 9-12 | Learn JSON, MQL, document modeling, aggregation, indexing, and MongoDB reliability |
| Connect systems and careers | 13-15 | Work with public data, scaling choices, multi-database incidents, projects, and interview explanations |

## Weekly Alignment

| Week | Main skill | In-class work | Course outcomes |
|---:|---|---|---:|
| 1 | trace a database-backed request and use relational-model vocabulary | application/data map and relational reasoning | 1, 7 |
| 2 | translate relational operations into working SQL | SQL query ladder and join/aggregate practice | 1, 2 |
| 3 | create and inspect schemas, keys, and constraints | schema inspection and integrity-rule lab | 1, 2, 3 |
| 4 | create a stable view and make a reversible schema change | view exercise and migration | 3, 7 |
| 5 | predict transaction behavior and diagnose blocking | two-session transaction and lock labs | 4 |
| 6 | apply least privilege and test row-level security | role/privilege and RLS labs | 3 |
| 7 | read an `EXPLAIN` plan and test an index | plan-reading and index experiments | 4 |
| 8 | create a logical backup and restore it separately | recovery notebook and midterm work | 5, 7 |
| 9 | compare NoSQL models and represent CSV relationships as JSON | JSON design lab | 1, 2 |
| 10 | perform basic MQL and choose embedding or referencing | MQL notebook and modeling lab | 1, 2 |
| 11 | build an aggregation, add validation, and evaluate an index | pipeline, validation, and sort lab | 3, 4 |
| 12 | connect replica behavior to consistency and recovery choices | reliability decision and restore labs | 5, 6 |
| 13 | evaluate a shard-key candidate and load public data with Python | capacity and integration notebook | 2, 6, 7 |
| 14 | diagnose an incident spanning relational and document stores | individual incident analysis | 4, 6, 7 |
| 15 | review, demonstrate, and explain course skills | final project and career translation | 1-7 |

## Typical Class Rhythm

Most meetings combine four elements:

1. a short review question;
2. a worked example or live demonstration;
3. guided practice with the class; and
4. an individual lab or project work period.

The sequence is flexible. A difficult example can take more time, and a class
may move directly into a notebook or lab when practice is more useful than more
slides. There is no required group work.

## Assessment Map

| Category | Weight | Main work |
|---|---:|---|
| In-class work and skill practice | 30% | individual labs, notebooks, short responses, and brief checks |
| Midterm PostgreSQL/Supabase project | 30% | schema and query work, one operational problem, one improvement, and a recovery plan |
| Final cloud database project | 40% | model, sample data, useful queries, one index, access control, recovery, and a short demonstration |

## Career Connection

The skills apply to database administration, backend development, cloud support,
data engineering, application support, cybersecurity operations, and technical
business analysis. Students practice explaining what they built, how they
debugged it, what tradeoff they made, and what they would improve next.
