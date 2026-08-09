# Course Map: Skills, Evidence, and Learning Progression

## Course-Level Outcomes

By the end of the course, a student can:

1. Build and explain a small relational or document data model that matches a
   stated workload.
2. Write and verify basic SQL and MongoDB queries using managed cloud interfaces.
3. Protect data with constraints, roles, grants, row-level policies, validation,
   and safe secret handling.
4. Investigate transactions, locks, query plans, indexes, and common performance
   problems using evidence rather than guesses.
5. Create a logical backup, perform or rehearse a restore, and document how the
   result was verified.
6. Explain replication, consistency, availability, sharding, and polyglot design
   as tradeoffs rather than product slogans.
7. Package database work so another person can reproduce, review, and discuss it
   in a workplace setting.

## The Learning Progression

The course follows one recurring scenario: Metro Support operates a help desk for
public services. It has users, tickets, ticket events, changing metadata, access
boundaries, reporting needs, and reliability risks. Students first represent the
system relationally, then reconsider parts of it as documents. Reusing one domain
reduces setup time and makes the changing technical decisions visible.

| Stage | Weeks | Central shift |
|---|---:|---|
| Rebuild the foundation and enter the profession | 1-2 | From half-remembered SQL to relational reasoning, verified queries, and operational responsibility |
| Build and change safely | 3-4 | From tables that merely accept rows to schemas that protect meaning |
| Operate PostgreSQL | 5-8 | From writing SQL to diagnosing concurrency, access, performance, and recovery |
| Move from tables to documents | 9-12 | From copying relational shapes to modeling around document access patterns and reliability |
| Reason across systems | 13-15 | From isolated features to capacity, architecture, incidents, projects, and career evidence |

## Weekly Alignment

| Week | Student can... | In-class evidence | Course outcome |
|---:|---|---|---:|
| 1 | distinguish data-system responsibilities and express a question using selection, projection, and join | responsibility map and relational-reasoning artifact | 1, 7 |
| 2 | translate relational operations into selection, filtering, joins, grouping, subqueries, and safe data changes | verified SQL review portfolio with result-grain notes | 1, 2, 7 |
| 3 | retrieve cumulative SQL skills, then create a schema with keys, constraints, and a justified index | SQL clinic evidence, schema audit, and build script | 1, 2, 3 |
| 4 | use views and metadata to make a safe, reversible change | change plan, migration, and verification query | 3, 7 |
| 5 | predict commit/rollback behavior and diagnose blocking | two-session incident record | 4 |
| 6 | apply least privilege and test an RLS policy | access matrix and allow/deny evidence | 3 |
| 7 | read an `EXPLAIN` plan and test an index hypothesis | before/after plan analysis | 4 |
| 8 | create and verify a logical recovery artifact | restore rehearsal and midterm package | 5, 7 |
| 9 | explain NoSQL's evolution and represent CSV relationships as JSON | two valid JSON designs with tradeoff | 1, 2 |
| 10 | perform basic MQL and choose embedding or referencing | query evidence and model decision | 1, 2 |
| 11 | build an aggregation, add validation, and evaluate an index | workload evidence packet | 3, 4 |
| 12 | connect reliability promises to recovery evidence | Atlas export/restore rehearsal and runbook | 5, 6 |
| 13 | explain a shard-key or capacity decision and connect with Python | capacity note and executable notebook | 2, 6, 7 |
| 14 | triage an incident spanning relational and document stores | individual incident report | 4, 6, 7 |
| 15 | demonstrate, explain, and reflect on course skills | final project and career story | 1-7 |

## Class Design Pattern

Most class meetings use the same sequence:

1. Retrieve: answer three short questions without notes.
2. Model: inspect one complete worked example and explain why it works.
3. Fade: complete a partially worked example with fewer prompts.
4. Build: complete an individual lab that produces one small artifact.
5. Check: answer one exit question that identifies evidence and a tradeoff.

No lab requires group work. Conversation is welcome, but every student creates
and submits their own evidence.

## Assessment Map

| Category | Weight | Evidence |
|---|---:|---|
| Midterm operations case | 30% | reproducible PostgreSQL/Supabase build, transaction/lock diagnosis, access or performance improvement, and recovery plan |
| Final cloud database project | 40% | model, seed data, meaningful queries, operational evidence, explanation, and short presentation |
| Engagement and skill evidence | 30% | in-class labs, retrieval/exit checks, notebooks, and eight short critical/career responses |

## Career Connection

The title "database administrator" is only one destination. The course produces
evidence relevant to database support, cloud operations, backend development,
data engineering, application support, cybersecurity operations, and technical
business analysis. Students practice the workplace verbs that recur across those
roles: reproduce, verify, restrict, monitor, diagnose, recover, document, and
explain.
