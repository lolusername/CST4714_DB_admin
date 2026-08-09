# Course Implementation Guide

## Scope and Use

This public guide supports a two-meeting-per-week implementation of *Operating
Cloud Databases*. It is not a private answer key. It identifies outcomes,
prerequisites, demonstrations, likely misconceptions, equivalent paths, and the
evidence an instructor can use to decide what comes next.

Most class time belongs to individual technical work. Whole-class explanation is
used to establish a model, inspect evidence, and resolve common errors. Students
may ask and answer questions publicly, but every lab artifact is produced and
submitted individually.

## Stable Meeting Pattern

Use the same five phases often enough that students can spend attention on the
database problem rather than the class procedure.

1. **Retrieve:** three no-notes prompts from the public
   [retrieval bank](../assessments/retrieval_exit_bank.md).
2. **Model:** inspect one complete example and predict its evidence before running
   it.
3. **Fade:** remove selected steps or labels while retaining the same small case.
4. **Build:** students complete the individual lab and create one checkable
   artifact.
5. **Check:** one exit response names evidence and a limitation or tradeoff.

Early modules provide complete commands and emphasize prediction and
interpretation. Middle modules provide partial procedures. Late modules provide a
symptom, workload, or operating promise and require students to select evidence.

Each weekly guide contains one optional industry extension. It is ungraded, adds
no submission, and must never become an unstated prerequisite. Offer it only when
time and interest permit; a student who uses the standard lab or equivalent
fallback receives no penalty or reduced access to later work. The
[currentness, pedagogy, and QA audit](../fellowship/CURRENTNESS_PEDAGOGY_QA_AUDIT.md)
records the research basis and extension inventory.

## Week 1: Responsibility, Evidence, and Relational Re-entry

**Student materials:** [Week 1 guide](../week_01/README.md),
[Module 1](../textbook/module_01_responsibility.md),
[responsibility lab](../week_01/lab_01_responsibility_evidence.md), and
[relational reasoning lab](../week_01/lab_02_relational_reasoning.md).

**Prerequisite:** no current SQL fluency is assumed. Use the beginning diagnostic
to locate remembered vocabulary without grading it.

### Day 1 Arc

- Retrieve distinctions among data, database, DBMS, and managed service.
- Model one failed application request as layers: client, network, managed
  platform, database engine, schema/query, and data.
- Show a complete evidence record with environment, action, observed result, and
  interpretation. Contrast it with an unexplained screenshot.
- Students complete the responsibility lab individually, using either Supabase or
  Atlas documentation or the supplied static path.
- Exit with one provider responsibility, one customer responsibility, and one
  piece of evidence that can locate the boundary.

### Day 2 Arc

- Retrieve tuple, attribute, key, selection, projection, and join without starting
  from SQL syntax.
- Model a four-row `users` relation and a six-row `tickets` relation. State the
  grain of each before matching identifiers.
- Fade the example by giving a plain-language question and asking students to mark
  rows kept, attributes kept, and matching pairs.
- Students complete the relational reasoning lab individually.
- Exit with a plain-language operation and the expected result grain.

**Live demonstration:** open one official architecture page and label only facts
that the source actually supports. Then manipulate a tiny printed or projected
relation before showing SQL vocabulary.

**Likely misconceptions:** “cloud provider owns every failure,” “a database is the
same as the provider dashboard,” and “a join simply adds columns without changing
row count.”

**Equivalent path:** no account is needed. Use the official-page excerpt already
recorded in the module and the synthetic relation tables.

**Evidence decision:** if students cannot state row grain or distinguish selection
from projection, Week 2 begins with relation marking rather than a longer SQL
lecture.

## Week 2: Relational Algebra and Major SQL Review

**Student materials:** [Week 2 guide](../week_02/README.md),
[Module 2](../textbook/module_02_sql.md),
[SQL review notebook](../notebooks/01_relational_sql_review.ipynb),
[query ladder](../week_02/lab_01_sql_query_ladder.md), and
[joins, aggregates, and DML lab](../week_02/lab_02_joins_aggregates_dml.md).

**Prerequisite:** Week 1 row/attribute/key vocabulary. Assume students have seen
SQL previously but cannot retrieve it reliably.

### Day 1 Arc

- Retrieve selection, projection, join, and result grain.
- Model one question through four representations: plain language, relational
  algebra, predicted tuples, and SQL.
- Run the first half of Notebook 1. Pause before each result so students commit to
  row count, columns, and one sample value.
- Fade by changing predicates and projections while retaining the Metro Support
  tables.
- Students complete the query ladder individually and annotate what one result row
  means.

### Day 2 Arc

- Retrieve one-to-many row multiplication, `NULL`, and duplicate behavior.
- Model inner versus left join with an unassigned ticket; then group events per
  ticket and identify when `WHERE` versus `HAVING` applies.
- Continue Notebook 1 through subqueries/CTEs, set operations, and transaction-
  guarded DML.
- Students complete the second lab and verify one result through a second query or
  hand calculation.
- Exit by explaining why a query can run successfully and still answer the wrong
  question.

**Live demonstration:** deliberately run a plausible but wrong join, compare row
counts, and repair it from the intended relationship. Roll back a test update.

**Likely misconceptions:** `DISTINCT` repairs a wrong join, `NULL` behaves like an
empty string, every selected column can accompany an aggregate, and successful
execution proves correctness.

**Equivalent path:** Notebook 1 runs in Colab or local Jupyter with DuckDB and no
cloud account. The labs can use any approved PostgreSQL environment.

**Evidence decision:** do not advance to schema administration if most students
cannot explain a one-to-many join result. Use the same relations and a different
visual representation before adding syntax.

## Week 3: Schema X-Ray, Keys, Constraints, and Index Vocabulary

**Student materials:** [Week 3 guide](../week_03/README.md),
[Module 3](../textbook/module_03_schema.md),
[SQL clinic](../week_03/lab_01_sql_clinic_schema_xray.md), and
[integrity lab](../week_03/lab_02_integrity_constraints.md).

**Prerequisite:** basic `SELECT`, joins, grouping, and safe DML from Week 2.

### Day 1 Arc

- Retrieve SQL with a cumulative clinic rather than assuming Week 2 is retained.
- Model a schema x-ray: list tables, columns, types, nullability, keys,
  constraints, and indexes before changing anything.
- Ask students to connect each metadata item to a possible bad state or operating
  question.
- Students complete the schema x-ray individually and submit one compact audit.

### Day 2 Arc

- Retrieve primary key, foreign key, `NOT NULL`, `UNIQUE`, and `CHECK` by the bad
  state each prevents.
- Model one expected success and one expected failure inside a transaction.
- Fade the example by giving a business rule and requiring students to choose the
  database mechanism and test.
- Students build and test the integrity lab individually.
- Exit by stating what the successful DDL proves and what the expected failure
  proves.

**Live demonstration:** insert an orphan, invalid status, and duplicate identifier
into an intentionally weak table; then add rules and rerun the same tests.

**Likely misconceptions:** foreign keys automatically create all useful indexes,
application validation replaces database integrity, and a declared constraint is
proven without a rejection test.

**Equivalent path:** use the provided PostgreSQL setup SQL locally when Supabase
is unavailable. Metadata screenshots may be replaced by copied catalog-query
results.

**Evidence decision:** if constraint names are remembered but bad-state reasoning
is weak, reteach from invalid rows and expected failures rather than definitions.

## Week 4: Views, Identity, Introspection, and Safe Migration

**Student materials:** [Week 4 guide](../week_04/README.md),
[Module 4](../textbook/module_04_change.md),
[views lab](../week_04/lab_01_views_identity.md), and
[safe migration lab](../week_04/lab_02_safe_migration.md).

**Prerequisite:** schema metadata, constraints, and transaction-guarded tests.

### Day 1 Arc

- Retrieve schema inspection and result grain.
- Model a view as a stable named query and identify current database, user,
  schema, and search path.
- Compare an administrator context with an application-facing interface without
  claiming they have the same permissions.
- Students create and verify one view individually.

### Day 2 Arc

- Retrieve precondition, postcondition, rollback, and dependency.
- Model expand-migrate-verify-contract on a small status-label change.
- Fade by supplying the desired final state but not the verification and rollback
  steps.
- Students complete one reversible migration and change record individually.
- Exit with a remaining risk outside the database command itself.

**Live demonstration:** query metadata before and after a change, keep old and new
interfaces compatible, and intentionally test a stale client query.

**Likely misconceptions:** a view stores an independent copy by default, DDL
success proves every client still works, and rollback means only writing the
opposite command.

**Equivalent path:** run against local PostgreSQL. If no server is available, use
the supplied before/after metadata and query transcript while students write and
defend the change plan.

**Evidence decision:** if students omit preconditions or verification, require the
five-part change record again in Week 6 before any access-policy change.

## Week 5: Transactions, MVCC, Locks, and Incident Communication

**Student materials:** [Week 5 guide](../week_05/README.md),
[Module 5](../textbook/module_05_transactions.md),
[transaction lab](../week_05/lab_01_transaction_outcomes.md),
[blocking lab](../week_05/lab_02_blocking_incident.md), and
[transactions/locks notebook](../notebooks/02_postgres_transactions_locks.ipynb).

**Prerequisite:** transactions as a safe test boundary; basic update syntax.

### Day 1 Arc

- Retrieve commit, rollback, and atomicity.
- Model two sessions as separate state machines. Students predict what each can
  observe before any command runs.
- Execute commit and rollback cases and connect observed rows to transaction
  boundaries.
- Students complete the transaction-outcomes lab individually.

### Day 2 Arc

- Retrieve open transactions and evidence records.
- Model a controlled blocker and waiter. Identify symptom, waiting evidence,
  blocking evidence, safe mitigation, and verification.
- Fade by removing the blocker label from the second case.
- Students complete the blocking incident notebook/lab individually and write a
  neutral incident update.

**Live demonstration:** use two visibly labeled sessions. Never create blocking in
a shared production table or terminate a session without identifying ownership.

**Likely misconceptions:** MVCC removes all locks, every delay is blocking, commit
and close-window are equivalent, and terminating a blocker explains the root
cause.

**Equivalent path:** the notebook contains a complete static incident transcript
when two live cloud sessions are unavailable.

**Evidence decision:** if students name the blocker but cannot explain evidence or
verification, return to the four-part evidence record before introducing security.

## Week 6: Roles, Grants, RLS, and Secret Boundaries

**Student materials:** [Week 6 guide](../week_06/README.md),
[Module 6](../textbook/module_06_security.md),
[least-privilege lab](../week_06/lab_01_least_privilege.md), and
[RLS lab](../week_06/lab_02_rls_test_harness.md).

**Prerequisite:** database identity from Week 4 and allow/rollback testing from
earlier labs.

### Day 1 Arc

- Retrieve authentication versus authorization and actor-action-resource scope.
- Model an access matrix before writing `GRANT` statements.
- Test one expected allow and one expected deny from the intended role.
- Students create and test a minimum role individually.

### Day 2 Arc

- Retrieve table grants versus row restrictions.
- Model RLS with two resident identities and an administrator observation,
  explicitly distinguishing Supabase Auth, token claims, PostgreSQL roles, and
  policy expressions.
- Fade by supplying the ownership rule while students write the test matrix.
- Students complete the RLS harness individually and map the local PostgreSQL
  concept to Supabase.

**Live demonstration:** show that SQL Editor success under a privileged context
does not prove an application user's access. Use a disposable schema and no real
user data.

**Likely misconceptions:** login equals authorization, RLS replaces all grants,
service-role credentials belong in frontend code, and one successful query proves
least privilege.

**Equivalent path:** PostgreSQL no-login roles and session settings can demonstrate
the concept without Supabase Auth. Static allow/deny evidence is acceptable during
a platform outage.

**Evidence decision:** if expected-deny evidence is missing, do not accept a broad
administrator screenshot as equivalent. Reteach from the access matrix and test
pair.

## Week 7: Explain Plans, Measurements, and Index Design

**Student materials:** [Week 7 guide](../week_07/README.md),
[Module 7](../textbook/module_07_performance.md),
[plan-reading lab](../week_07/lab_01_plan_reading.md),
[index experiment](../week_07/lab_02_index_experiment.md), and
[performance fixture](../week_07/performance_lab_setup.sql).

**Prerequisite:** cumulative SQL, indexes as structures with costs, and controlled
change evidence.

### Day 1 Arc

- Retrieve query grain, selectivity, and index costs.
- Model a plan from the leaves upward. Separate estimate from actual measurement
  and plan node from judgment.
- Compare a small-table sequential scan with a larger selective query so students
  do not treat node names as grades.
- Students complete the plan-reading lab individually before changing any index.

### Day 2 Arc

- Retrieve baseline, hypothesis, and single-variable experiment.
- Model question-plan-hypothesis-change-remeasure on the 100,000-row deterministic
  fixture.
- Fade by giving a query and baseline while students select one candidate index
  and predict the change.
- Students complete the index experiment individually and recommend keep or drop
  using evidence and cost.

**Live demonstration:** run `EXPLAIN (ANALYZE, BUFFERS)` only on the safe teaching
fixture. Show one index that helps and one plausible index that the planner does
not need.

**Likely misconceptions:** sequential scan is always bad, index scan is always
good, lower one-time runtime proves a lasting improvement, and indexes have no
write or storage cost.

**Equivalent path:** distribute saved text plans from the deterministic fixture.
Students can annotate nodes and make the same evidence decision without a live
server.

**Evidence decision:** if students recommend from node name alone, compare two
plans with different table sizes/selectivities before recovery work.

## Week 8: Logical Backup, Verified Restore, and Midterm Integration

**Student materials:** [Week 8 guide](../week_08/README.md),
[Module 8](../textbook/module_08_recovery.md),
[backup/restore notebook](../notebooks/03_postgres_backup_restore.ipynb),
[recovery lab](../week_08/lab_01_backup_restore.md), and the canonical
[midterm operations case](../midterm_project.md).

**Prerequisite:** schema, transactions, security, performance, and evidence.

### Day 1 Arc

- Retrieve RPO, RTO, backup, restore, and verification.
- Model a real logical dump, artifact checksum, separate restore database, and
  five different checks.
- Run Notebook 3 from the top, including its tool/server compatibility selection.
- Students complete the recovery lab individually and identify what the artifact
  does not include.

### Day 2 Arc

- Retrieve one concept from each PostgreSQL operations week.
- Model how a concise evidence record can connect schema, incident, access or
  performance, and recovery without producing many unrelated screenshots.
- Students work individually on the canonical midterm. Use public checkpoints but
  do not create alternate deliverable lists in the weekly guide.
- Exit with the strongest evidence, weakest evidence, and next repair.

**Live demonstration:** intentionally show a nonzero file before restoring it, so
students can distinguish artifact existence from recovery.

**Likely misconceptions:** sync/replication equals backup, restore into the source
is the safest test, command success proves behavioral correctness, and free cloud
tiers guarantee native backups.

**Equivalent path:** Notebook 3 creates a disposable local PostgreSQL service and
requires no cloud secret. A supplied dump and restore transcript can support the
reasoning if runtime startup fails.

**Evidence decision:** if restore verification is weak, require an additional
meaningful query or expected constraint failure rather than another screenshot.

## Week 9: NoSQL Evolution, Model Families, JSON, and Atlas Orientation

**Student materials:** [Week 9 guide](../week_09/README.md),
[Module 9](../textbook/module_09_nosql_json.md),
[CSV-to-JSON lab](../week_09/lab_01_csv_to_json.md), and the
[Mini Inventory data](../datasets/mini_inventory/README.md).

**Prerequisite:** relational model, keys, relationships, and access questions.

### Day 1 Arc

- Retrieve relational strengths before introducing alternatives.
- Present NoSQL history as workload and distribution responses, not a winner-
  versus-loser story.
- Model key-value, document, graph, and vector questions. Include basic graph
  vertices/edges/path vocabulary and a small cosine-similarity comparison.
- Students individually classify four workloads and defend one model with a
  tradeoff.

### Day 2 Arc

- Retrieve JSON value types and relationship cardinality.
- Model strict JSON syntax, then create two valid representations of the same
  small CSV relations: embedded and referenced.
- Demonstrate the GitHub web editor and Atlas setup as tools, not separate
  submissions.
- Students complete the CSV-to-JSON lab individually in a text editor and explain
  why multiple answers can be valid.

**Live demonstration:** parse intentionally invalid JSON, repair one error at a
time, and compare read/update behavior across two valid shapes.

**Likely misconceptions:** NoSQL means no schema or no queries, JSON allows single
  quotes/comments/trailing commas, vectors store only images, and one model family
  replaces all others.

**Equivalent path:** the entire required lab uses CSV and JSON text; no Atlas query
or MongoDB University completion is required for the core evidence.

**Evidence decision:** if students copy tables directly without a workload
explanation, ask one read and one update question before MQL begins.

## Week 10: Basic MQL and Access-Pattern Modeling

**Student materials:** [Week 10 guide](../week_10/README.md),
[Module 10](../textbook/module_10_mql_modeling.md),
[MQL notebook](../notebooks/04_atlas_mql_modeling.ipynb),
[MQL lab](../week_10/lab_01_atlas_mql.md), and
[document-model lab](../week_10/lab_02_document_model.md).

**Prerequisite:** valid JSON, document/collection vocabulary, and relationship
cardinality.

### Day 1 Arc

- Retrieve filters, projections, nested fields, and arrays by connecting them to
  familiar SQL concepts without claiming identical semantics.
- Model direct `find`, projection, sort, update, and delete in a disposable course
  collection. Predict matched and modified counts.
- Run the MQL notebook on its offline path or Atlas.
- Students complete the MQL lab individually and record one query result, update
  result, verification query, and safety control.

### Day 2 Arc

- Retrieve boundedness, read-together patterns, and source of truth.
- The instructor live-codes the external **Modeling Data Relationships** activity.
- Fade the reasoning with one Metro Support relationship.
- Students complete the distinct external **Relational (SQL) to Document Model**
  activity and the course-authored model decision individually.

**Live demonstration boundary:** do not assign students the same MongoDB
University activity used for live coding. The instructor activity demonstrates;
the student activity practices a distinct translation.

**Likely misconceptions:** MongoDB filters are SQL strings, all related data should
be embedded, referencing recreates every relational join, and modified count zero
always means failure.

**Equivalent path:** Notebook 4 uses `mongomock` by default. The course-authored
model comparison remains available if MongoDB University or Atlas is unavailable.

**Evidence decision:** if CRUD syntax succeeds but model reasoning is weak, use a
growing/unbounded history example before aggregation.

## Week 11: Aggregation, Validation, Sort Performance, and Case Writing

**Student materials:** [Week 11 guide](../week_11/README.md),
[Module 11](../textbook/module_11_mongodb_operations.md),
[pipeline/validation lab](../week_11/lab_01_pipeline_validation.md), and
[sort/case response lab](../week_11/lab_02_sort_and_case_response.md).

**Prerequisite:** basic MQL, embedding/referencing tradeoffs, and index evidence
from PostgreSQL.

### Day 1 Arc

- Retrieve input grain, filter, sort, and grouping.
- Model an aggregation pipeline one stage at a time. After each stage, state the
  current document shape and count.
- Add a validator and run one valid and one expected-invalid write.
- Students complete the pipeline/validation lab individually and submit one
  workload evidence packet.

### Day 2 Arc

- Retrieve stage order and compound-index reasoning.
- Students complete the free external **Improving Performance of Sort Stages -
  Lab Only** activity individually.
- Connect completion to a course-authored explanation of filter, sort, index
  evidence, and cost.
- Students submit the redacted completion evidence and the 200-300 word case-study
  response as one Brightspace text response. No separate Markdown file is needed.

**Live demonstration:** move `$match` before an expensive stage when semantics
permit, inspect explain evidence, and show that validation is database behavior,
not a repair of existing documents.

**Likely misconceptions:** pipelines are unordered lists, `$group` preserves one
row per source document, validation fixes old data, and an index that supports a
sort is free.

**Equivalent path:** use the course pipeline fixture and saved explain evidence if
Atlas or MongoDB University is unavailable. The written interpretation carries
the same conceptual outcome.

**Evidence decision:** if students list stages without tracking shape/grain,
rebuild the pipeline on six documents before reliability.

## Week 12: Replication, Reliability Promises, and Logical Recovery

**Student materials:** [Week 12 guide](../week_12/README.md),
[Module 12](../textbook/module_12_reliability.md),
[reliability lab](../week_12/lab_01_reliability_decisions.md),
[MongoDB recovery notebook](../notebooks/05_mongodb_logical_recovery.ipynb),
[recovery lab](../week_12/lab_02_mongodb_recovery.md), and the canonical
[final project](../final_project.md).

**Prerequisite:** transactions, PostgreSQL recovery, MQL, validators, and indexes.

### Day 1 Arc

- Retrieve replication versus backup and failure versus recovery.
- Model a reliability claim as promise, mechanism, failure case, and verification.
- Trace primary, secondaries, acknowledgment, election, and client interruption
  without promising zero data loss or zero downtime.
- Students complete the reliability-decisions lab individually.
- Introduce the final only through the canonical file and one planning checkpoint.

### Day 2 Arc

- Retrieve BSON types, separate restore target, and metadata omissions.
- Run Notebook 5: export Canonical Extended JSON, hash the artifact, restore
  elsewhere, verify data/type/query behavior, and recreate omitted index/validator
  metadata as supported.
- Students complete the recovery lab individually and state the limits of the
  selected artifact.

**Live demonstration:** show why a replicated accidental delete is still a valid
replicated operation and why an independent recovery artifact addresses a
different failure.

**Likely misconceptions:** replicas are backups, majority acknowledgment solves
every loss scenario, free-tier topology permits every failure test, and JSON
automatically preserves every BSON type and collection setting.

**Equivalent path:** Notebook 5 uses `mongomock` and labels that it cannot enforce
server-side JSON Schema. The logical evidence sequence remains complete.

**Evidence decision:** if students cannot separate data from metadata, compare the
restored documents with the missing index/validator list before scaling.

## Week 13: Capacity, Sharding, Public Data, and Python Integration

**Student materials:** [Week 13 guide](../week_13/README.md),
[Module 13](../textbook/module_13_scale.md),
[public-data notebook](../notebooks/06_public_data_capacity_integration.ipynb), and
[integration lab](../week_13/lab_01_public_data_integration.md).

**Prerequisite:** query/index reasoning, MongoDB document operations, and reliable
import evidence.

### Day 1 Arc

- Retrieve tune, scale up, read replica, partition, and shard distinctions.
- Model a sharded cluster with shards, replica sets, config servers, and `mongos`.
- Use the CISA teaching snapshot to measure cardinality, largest-value frequency,
  monotonic input order, and query targeting.
- Run the notebook's deterministic range and hash simulations.
- Students record an individual “do not shard yet” or conditional candidate
  recommendation with evidence.

### Day 2 Arc

- Retrieve source, transformation, stable key, upsert, and verification.
- Model the notebook's simple SQLite path before showing optional Atlas and
  PostgreSQL branches.
- Students choose one target, enter cloud credentials only through `getpass`, load
  idempotently, and verify count, known identifier, and grouped question.
- Students complete the final-project transfer sentences without creating new
  final deliverables.

**Live demonstration:** rerun the same import and show that the stable key
preserves logical count. Compare local SQLite's process boundary with managed
PostgreSQL and Atlas network/authentication boundaries.

**Likely misconceptions:** high cardinality guarantees a good shard key, hashed
distribution makes every query faster, Atlas Free can deploy a sharded cluster,
and insert count proves trustworthy import.

**Equivalent path:** the versioned CISA fixture is embedded in Notebook 6, and
SQLite is built into Python. No live feed or cloud account is required.

**Evidence decision:** if recommendations ignore query targeting, ask students to
route one exact-ID query and one vendor/date question before Week 14.

## Week 14: Polyglot Incident Response and Final Operations Clinic

**Student materials:** [Week 14 guide](../week_14/README.md),
[Module 14](../textbook/module_14_polyglot.md), and
[polyglot incident lab](../week_14/lab_01_polyglot_incident.md).

**Prerequisite:** relational/document modeling, evidence, recovery, and integration.

### Day 1 Arc

- Retrieve source of truth, idempotency, and synchronization failure.
- Model one ticket stored authoritatively in PostgreSQL with a document-shaped read
  copy in MongoDB. Trace identifier, version/time, and failure points.
- Fade by presenting mismatched values and partial logs without naming the cause.
- Students complete the incident lab individually: impact, boundary evidence,
  diagnosis, safe repair, verification, and prevention.

### Day 2 Arc

- Retrieve one operational evidence pattern from each final-project category.
- Students work individually on their final using the canonical requirements.
- Hold short public demonstrations of model, query, access/performance, and
  recovery evidence; students apply the same checklist to their own work.
- Exit with one verified claim, one unresolved risk, and one next action.

**Live demonstration:** compare a failed dual write with an outbox/idempotent
consumer concept at a beginner level. Emphasize ownership and evidence rather than
adding a framework.

**Likely misconceptions:** two stores are automatically more scalable, both copies
can be authoritative, timestamp comparison alone proves correctness, and retrying
without an idempotent key is safe.

**Equivalent path:** the incident is fully represented in static evidence. Final
work can use the open local path when a cloud service is unavailable.

**Evidence decision:** if students repair values without naming ownership and
verification, require those two statements before final presentations.

## Week 15: Integrated Review, Public Artifact, and Career Translation

**Student materials:** [Week 15 guide](../week_15/README.md),
[Module 15](../textbook/module_15_careers.md),
[GitHub concept-artifact lab](../week_15/lab_01_github_concept_artifact.md), and the
canonical [final project](../final_project.md).

**Prerequisite:** one completed or nearly completed final project and safe public-
artifact practices.

### Day 1 Arc

- Retrieve the course verbs: model, query, restrict, diagnose, measure, recover,
  integrate, and explain.
- Model a short public README that teaches one concept with original explanation,
  safe code or a Markdown guide, expected evidence, and limitations.
- Students create the GitHub concept artifact individually and verify that no
  credential, private account detail, or private dataset appears.
- Translate one artifact into a Situation-Task-Action-Result-Reflection outline.

### Day 2 Arc

- Use the post-course inventory for reflection and course improvement, not a
  final-exam grade.
- Students give short individual final demonstrations centered on one operating
  claim and its evidence.
- Ask follow-up questions about tradeoffs, limitations, and the next production
  check rather than obscure trivia.
- Students complete the interview response and name one next skill/artifact.

**Live demonstration:** turn a weak claim such as “I know MongoDB” into a supported
claim naming the workload, action, observed evidence, tradeoff, and limitation.

**Likely misconceptions:** a tool list is a portfolio, classroom scale invalidates
all skill evidence, confidence requires hiding limitations, and public work should
include real credentials or account screenshots.

**Equivalent path:** a local Markdown/code artifact may be submitted privately if
public GitHub creates a barrier. The interview explanation remains the same.

**Evidence decision:** report aggregate changes in concept categories and material
access. Do not publish named student results or claim causal impact beyond the
available design.

## After the Course

1. Run the technical, link, accessibility, notebook, and slide validation suite.
2. Review aggregate diagnostic/post categories, lab revision patterns, rubric
   dimensions, and access feedback.
3. Separate platform failures from conceptual errors.
4. Record one observed pattern, one cautious interpretation, and one OER change.
5. Update the [created OER catalog](../OER_CATALOG.md), attribution record, and
   release status.
6. Preserve the boundary among public OER, free external resources, and private
   student/grading records.
