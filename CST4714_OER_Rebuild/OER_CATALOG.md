# Catalog of Created Open Educational Resources

## Purpose

This catalog describes the educational resources created or adapted for
*Operating Cloud Databases*. It is the authoritative inventory of course OER.
The separate [fellowship project plan](fellowship/OER_FELLOWSHIP_PROJECT_PLAN.md)
describes why and how the project is being produced; it is not itself the course
content. The separate [free external resource catalog](FREE_EXTERNAL_RESOURCES.md)
records no-cost vendor and industry resources that the course links but does not
claim as created OER.

- **Inventory date:** August 9, 2026
- **Package license:** original instructional prose and media CC BY-NC-SA 4.0;
  original code MIT; original synthetic data CC0. Source-specific notices control
  adapted material.

## Status Language

- **Complete:** the editable source exists in this package and is ready for the
  technical and accessibility review required before release.
- **In production:** the item is part of the approved scope but is not counted as
  a completed fellowship deliverable.
- **External:** the item costs students nothing but is not course-created OER.

## Created OER at a Glance

| Category | Complete now | In production | What is original about it |
|---|---:|---:|---|
| Open-text modules | 15 | 0 | one coherent relational-to-document operations progression built around evidence |
| Weekly student guides | 15 | 0 | two-day, lab-first learning sequences with retrieval, worked examples, and transfer |
| Individual in-class labs | 25 | 0 | one manageable evidence artifact per lab; no group work or paid dependency |
| Educational notebooks | 6 | 0 | executable instruction with credential-safe cloud paths and open offline fallbacks |
| Data packages | 3 | 0 | two original synthetic cases and one documented public-data transformation |
| Canonical major projects | 2 | 0 | one midterm operations case and one beginner cloud-database final project |
| Assessment resources | 6 files | 0 | diagnostic/post inventory, retrieval bank, writing prompts, common rubrics, and assessment map |
| Student slide decks | 15 | 0 | student-facing teaching decks with complete spoken scripts |
| Deck PDF handouts and transcripts | 30 | 0 | visually verified handouts and structured-text versions of every spoken script |
| Public implementation resources | 5 core guides | 0 | adoption, troubleshooting, accessibility, data-informed teaching, and release support |

Items are counted only once in this table. For example, a slide deck, its PDF,
and its transcript are three formats or artifacts, while the script in both the
notes and transcript is one authored body of instructional prose.

Each weekly guide also includes one optional, ungraded industry extension. The 15
extensions add no submission and are embedded learning choices, not extra labs in
the inventory count.

## OER 1: Open Textbook and Lab Manual

The 15 modules are not a collection of vendor tutorials. Together they form an
original course narrative: identify an operating promise, inspect evidence,
make one controlled change, and verify the result.

| ID | Module | Original educational contribution | Status |
|---|---|---|---|
| T01 | [Responsibility and Evidence](textbook/module_01_responsibility.md) | shared-responsibility map and reproducible evidence record | Complete |
| T02 | [Relational Model, Algebra, and SQL](textbook/module_02_sql.md) | major re-entry bridge from mathematical operations to result-grain checks and safe SQL | Complete |
| T03 | [Schema and Integrity](textbook/module_03_schema.md) | Metro Support schema audit and expected-failure verification | Complete |
| T04 | [Views and Safe Change](textbook/module_04_change.md) | beginner expand-migrate-contract case and five-part change record | Complete |
| T05 | [Transactions and Concurrency](textbook/module_05_transactions.md) | two-session model connecting ACID, MVCC, locks, symptoms, and evidence | Complete |
| T06 | [Security](textbook/module_06_security.md) | actor-action-resource matrix and allow/deny proof pattern | Complete |
| T07 | [Performance](textbook/module_07_performance.md) | question-plan-hypothesis-change-remeasure workflow | Complete |
| T08 | [Backup and Recovery](textbook/module_08_recovery.md) | free-tier-accurate logical restore and verification framework | Complete |
| T09 | [NoSQL and JSON](textbook/module_09_nosql_json.md) | NoSQL history and model comparison, JSON choices, graph theory, and vector similarity | Complete |
| T10 | [MQL and Document Modeling](textbook/module_10_mql_modeling.md) | access-pattern-driven relational-to-document translation | Complete |
| T11 | [MongoDB Operations](textbook/module_11_mongodb_operations.md) | aggregation, validation, indexing, and explain evidence in one workload | Complete |
| T12 | [Reliability](textbook/module_12_reliability.md) | promise-mechanism-failure-verification reasoning | Complete |
| T13 | [Scale](textbook/module_13_scale.md) | beginner capacity and shard-key reasoning grounded in measurable distributions | Complete |
| T14 | [Polyglot Systems](textbook/module_14_polyglot.md) | source-of-truth, synchronization, and incident-boundary analysis | Complete |
| T15 | [Career Evidence](textbook/module_15_careers.md) | translation from technical evidence to portfolio and interview language | Complete |

The [textbook index](textbook/README.md) supplies reading order and module-level
navigation. All modules remain editable Markdown for adaptation and accessible
web publication. The reproducible [publication package](publication/README.md)
builds the modules as a standalone semantic HTML book, EPUB, and Word import
file. Those are alternate formats of the same 15-module OER, not additional
modules in the inventory count.

## OER 2: Weekly Guides and Individual Labs

Each [weekly guide](README.md#weekly-course-map) converts module concepts into a
two-class learning sequence. The 25 labs use a stable design: a focused operating
question, a small authentic task, explicit evidence, a short interpretation, and
one submission. Every lab is individual.

| IDs | Week and lab focus | Count | Status |
|---|---|---:|---|
| L01-L02 | Week 1: responsibility evidence; relational reasoning | 2 | Complete |
| L03-L04 | Week 2: SQL query ladder; joins, aggregates, and safe DML | 2 | Complete |
| L05-L06 | Week 3: schema x-ray; integrity constraints | 2 | Complete |
| L07-L08 | Week 4: views and identity; safe migration | 2 | Complete |
| L09-L10 | Week 5: transaction outcomes; blocking incident | 2 | Complete |
| L11-L12 | Week 6: least privilege; RLS test harness | 2 | Complete |
| L13-L14 | Week 7: plan reading; index experiment | 2 | Complete |
| L15 | Week 8: logical backup and verified restore | 1 | Complete |
| L16 | Week 9: multiple valid CSV-to-JSON models | 1 | Complete |
| L17-L18 | Week 10: Atlas/MQL evidence; document-model decision | 2 | Complete |
| L19-L20 | Week 11: pipeline and validation; sort performance and case response | 2 | Complete |
| L21-L22 | Week 12: reliability decisions; MongoDB logical recovery | 2 | Complete |
| L23 | Week 13: public-data integration and capacity evidence | 1 | Complete |
| L24 | Week 14: polyglot incident analysis | 1 | Complete |
| L25 | Week 15: public GitHub concept artifact and career explanation | 1 | Complete |

The lab files are linked from their corresponding `week_01` through `week_15`
directories. Linked MongoDB University practice is an external resource; the
course-authored prompt, evidence requirement, fallback, and interpretation are
the OER contribution.

## OER 3: Educational Notebooks

| ID | Notebook | Educational contribution | Cloud and open path | Status |
|---|---|---|---|---|
| N01 | [Relational and SQL Review](notebooks/01_relational_sql_review.ipynb) | predicts and executes relational algebra, joins, grouping, set operations, and rollback | DuckDB runs locally or in Colab | Complete |
| N02 | [PostgreSQL Transactions and Locks](notebooks/02_postgres_transactions_locks.ipynb) | interprets a two-session concurrency incident | credential-safe PostgreSQL path plus static incident fallback | Complete |
| N03 | [PostgreSQL Backup and Restore](notebooks/03_postgres_backup_restore.ipynb) | creates a real dump, restores separately, and verifies behavior | disposable local PostgreSQL in notebook | Complete |
| N04 | [Atlas MQL and Modeling](notebooks/04_atlas_mql_modeling.ipynb) | teaches direct CRUD, arrays, nested fields, and model decisions | runtime Atlas credential or `mongomock` | Complete |
| N05 | [MongoDB Logical Recovery](notebooks/05_mongodb_logical_recovery.ipynb) | preserves BSON-aware values and distinguishes data from metadata | runtime Atlas credential or `mongomock` | Complete |
| N06 | [Public Data, Capacity, and Integration](notebooks/06_public_data_capacity_integration.ipynb) | evaluates a public source, measures key distributions, and loads idempotently | Atlas, PostgreSQL, or SQLite path | Complete |

Notebooks never contain course credentials. Cloud secrets are entered at runtime,
and outputs are checked before publication.

## OER 4: Reusable Data Packages

| ID | Package | Origin and transformation | License/status |
|---|---|---|---|
| D01 | [Metro Support](datasets/metro_support/README.md) | original relational service-desk case with users, tickets, events, and PostgreSQL setup | CC0; Complete |
| D02 | [Mini Inventory](datasets/mini_inventory/README.md) | original small CSV case for alternative JSON/document designs | CC0; Complete |
| D03 | [CISA KEV Teaching Sample](datasets/cisa_kev_sample/README.md) | 75-record, field-reduced, versioned transformation of an official U.S. government feed | source terms retained; transformation code MIT; Complete |

D03 is not described as an original dataset. Its README records the source,
retrieval metadata, transformation, omissions, safety limits, and applicable
source terms.

## OER 5: Assessment and Project Materials

| ID | Resource | Purpose | Status |
|---|---|---|---|
| A01 | [Diagnostic](assessments/diagnostic.md) | low-stakes baseline of relational, SQL, evidence, security, recovery, and document reasoning | Complete |
| A02 | [Critical and Career Writing](assessments/critical_writing.md) | eight claim-evidence-tradeoff prompts tied to technical work and workplace genres | Complete |
| A03 | [Common Rubrics](assessments/rubrics.md) | transparent criteria for technical evidence and communication | Complete |
| A04 | [Assessment Map](assessments/README.md) | explains formative and summative evidence and data stewardship | Complete |
| A05 | [Retrieval and Exit Bank](assessments/retrieval_exit_bank.md) | 15 module-aligned sets for low-stakes spaced practice and instructional decisions | Complete |
| A06 | [Post-Course Inventory](assessments/post_course_inventory.md) | paired applied-concept, confidence, access, and material feedback measure | Complete |
| P01 | [Midterm Operations Case](midterm_project.md) | one canonical PostgreSQL/Supabase operations investigation | Complete |
| P02 | [Final Cloud Database Project](final_project.md) | one canonical beginner project using PostgreSQL, MongoDB, or a justified combination | Complete |

Private student records, answer keys, named-student analytics, and private grading
notes are not OER and are not included in the public package.

## OER 6: Student-Facing Slides and Study Formats

The package includes 15 PowerPoint decks containing 214 authored slides. Visible
content teaches students directly. Every slide has complete word-for-word spoken
prose in its PowerPoint speaker notes, and every script is reproduced in a
matching structured-text transcript. Every deck also has a visually verified PDF
handout. All 15 PDFs report tagged structure, contain extractable text, and are
unencrypted. Automated tag-tree inspection found only `Figure`, `Div`, and `P`
structures and no figure alternative-text metadata. The handouts are therefore
not claimed as accessible PDFs; the transcript and module remain the
authoritative structured-text alternatives.

| ID | Week and original instructional role | Slides | Published formats | Status |
|---|---|---:|---|---|
| S01 | responsibility boundaries, reproducible evidence, and relational grain | 15 | [PPTX](week_01/week_01_responsibility_relational_thinking.pptx), [PDF](week_01/week_01_responsibility_relational_thinking.pdf), [transcript](week_01/week_01_responsibility_relational_thinking_transcript.md) | Complete |
| S02 | relational algebra as a prediction model for a major SQL review | 19 | [PPTX](week_02/week_02_relational_algebra_sql_review.pptx), [PDF](week_02/week_02_relational_algebra_sql_review.pdf), [transcript](week_02/week_02_relational_algebra_sql_review_transcript.md) | Complete |
| S03 | schemas, metadata, constraints, and expected-failure evidence | 13 | [PPTX](week_03/week_03_schemas_constraints_evidence.pptx), [PDF](week_03/week_03_schemas_constraints_evidence.pdf), [transcript](week_03/week_03_schemas_constraints_evidence_transcript.md) | Complete |
| S04 | views, execution identity, dependencies, and reversible schema change | 13 | [PPTX](week_04/week_04_views_identity_safe_change.pptx), [PDF](week_04/week_04_views_identity_safe_change.pdf), [transcript](week_04/week_04_views_identity_safe_change_transcript.md) | Complete |
| S05 | transaction state, MVCC, locking, blocking, and two-session evidence | 13 | [PPTX](week_05/week_05_transactions_mvcc_locks.pptx), [PDF](week_05/week_05_transactions_mvcc_locks.pdf), [transcript](week_05/week_05_transactions_mvcc_locks_transcript.md) | Complete |
| S06 | identity boundaries, least privilege, grants, RLS, and secret safety | 13 | [PPTX](week_06/week_06_identity_permissions_rls.pptx), [PDF](week_06/week_06_identity_permissions_rls.pdf), [transcript](week_06/week_06_identity_permissions_rls_transcript.md) | Complete |
| S07 | plan reading, `EXPLAIN ANALYZE`, controlled index experiments, and cost | 14 | [PPTX](week_07/week_07_query_plans_index_design.pptx), [PDF](week_07/week_07_query_plans_index_design.pdf), [transcript](week_07/week_07_query_plans_index_design_transcript.md) | Complete |
| S08 | RPO/RTO, logical backup, independent restore, verification, and midterm synthesis | 12 | [PPTX](week_08/week_08_backup_restore_midterm.pptx), [PDF](week_08/week_08_backup_restore_midterm.pdf), [transcript](week_08/week_08_backup_restore_midterm_transcript.md) | Complete |
| S09 | NoSQL history and models, graph/vector foundations, JSON syntax, and alternative designs | 18 | [PPTX](week_09/week_09_nosql_models_json.pptx), [PDF](week_09/week_09_nosql_models_json.pdf), [transcript](week_09/week_09_nosql_models_json_transcript.md) | Complete |
| S10 | credential-safe Atlas access, basic MQL, write evidence, and document boundaries | 15 | [PPTX](week_10/week_10_mql_document_modeling.pptx), [PDF](week_10/week_10_mql_document_modeling.pdf), [transcript](week_10/week_10_mql_document_modeling_transcript.md) | Complete |
| S11 | aggregation grain, validation, compound index order, explain evidence, and career writing | 15 | [PPTX](week_11/week_11_aggregation_validation_indexes.pptx), [PDF](week_11/week_11_aggregation_validation_indexes.pdf), [transcript](week_11/week_11_aggregation_validation_indexes_transcript.md) | Complete |
| S12 | replication, read/write settings, partition choices, and logical MongoDB recovery | 15 | [PPTX](week_12/week_12_mongodb_reliability.pptx), [PDF](week_12/week_12_mongodb_reliability.pdf), [transcript](week_12/week_12_mongodb_reliability_transcript.md) | Complete |
| S13 | capacity evidence, replication versus sharding, shard-key risk, and safe integration | 14 | [PPTX](week_13/week_13_scale_integration.pptx), [PDF](week_13/week_13_scale_integration.pdf), [transcript](week_13/week_13_scale_integration_transcript.md) | Complete |
| S14 | polyglot ownership, outbox reasoning, idempotency, reconciliation, and incident repair | 12 | [PPTX](week_14/week_14_polyglot_incident.pptx), [PDF](week_14/week_14_polyglot_incident.pdf), [transcript](week_14/week_14_polyglot_incident_transcript.md) | Complete |
| S15 | integrated review, publication safety, portfolio evidence, and interview communication | 13 | [PPTX](week_15/week_15_synthesis_careers.pptx), [PDF](week_15/week_15_synthesis_careers.pdf), [transcript](week_15/week_15_synthesis_careers_transcript.md) | Complete |

## OER 7: Public Adoption and Implementation Materials

| ID | Resource | Reuse contribution | Status |
|---|---|---|---|
| I01-I15 | [Course Implementation Guide](instructor/implementation_guide.md) | 15 two-class lesson plans with outcomes, live-demo boundaries, misconceptions, fallbacks, and evidence decisions | Complete |
| I16 | [Technical Setup and Troubleshooting](instructor/technical_setup_troubleshooting.md) | safe free-platform setup, Atlas TLS and Supabase network diagnosis, tool compatibility, and outage paths | Complete |
| I17 | [Accessibility and Adaptation](instructor/accessibility_adaptation.md) | accessible authoring, equivalent evidence, cognitive-load, notebook, slide, and adaptation practices | Complete |
| I18 | [Data-Informed Teaching Protocol](instructor/data_informed_teaching.md) | low-stakes evidence cycle, aggregate decision rules, privacy, and revision reporting | Complete |
| I19 | [Production, Validation, and Release Guide](RELEASE_CHECKLIST.md) | inventory, pedagogy, technical, accessibility, licensing, privacy, and release checks with a reusable validator | Complete |

These are public adoption resources, not private answer keys. Private student
records and grading notes remain outside the release.

## What Is Not Counted as Created OER

The following items may support the project but are deliberately excluded from
the created-OER totals:

- fellowship plans, schedules, evaluation protocols, and administrative reports;
- free vendor platforms, vendor courses, official documentation, and account
  services linked in `FREE_EXTERNAL_RESOURCES.md`;
- the underlying CISA source records, which are documented as a public-data
  transformation rather than an original course dataset;
- private student records, private grading notes, answer keys, credentials, and
  internal teacher-only material; and
- temporary authoring, rendering, inspection, or slide-generation files used to
  produce and validate the published formats.

## Fellowship Talking Points About the Created OER

- **The package is one course, not a folder of unrelated tutorials.** One Metro
  Support case and one evidence cycle connect relational review, PostgreSQL
  administration, MongoDB modeling, recovery, scale, incidents, and career
  communication.
- **The relational review is a major original bridge.** The first three weeks
  rebuild forgotten SQL through grain, relational algebra, prediction, execution,
  and verification before administration lessons assume query fluency.
- **The labs reduce logistics without reducing thinking.** Twenty-five
  individual, in-class labs use one explicit submission, a small authentic task,
  observable evidence, and a short interpretation. No graded lab depends on
  group formation.
- **Cloud realism is separated from vendor dependence.** Supabase and Atlas
  provide authentic interfaces, while each essential outcome also has a local,
  static, or simulated route. Vendor courses remain linked free resources and are
  not presented as authored OER.
- **The slide collection is a substantial authored teaching resource.** Fifteen
  decks contain 214 student-facing slides, native diagrams and code examples,
  complete word-for-word scripts in notes, exact transcripts, and PDF handouts.
  The scripts teach the content rather than telling an instructor what to say.
- **Open executable materials make operations inspectable.** Six notebooks,
  PostgreSQL setup files, synthetic data, a documented CISA transformation, and
  credential-safe examples let adopters reproduce query, concurrency, recovery,
  modeling, and integration evidence.
- **Assessment is tied to workplace communication.** Labs and writing prompts
  ask students to state a claim, preserve evidence, identify a tradeoff, and name
  a limitation. The final module translates that evidence into portfolio and
  interview language without inflating technical scope.
- **Accessibility is provided in multiple editable formats.** Core prose is
  structured Markdown; spoken content is available as exact transcripts; decks
  use large, high-contrast student-facing layouts; and cloud barriers have
  equivalent evidence paths. PDFs are described accurately as handouts whose
  reported tags still require a human quality and reading-order audit.
- **Release quality is reproducible.** The public validator checks inventory,
  links, datasets, notebooks, secrets, individual-work rules, canonical
  assignments, notes/transcript identity, and presentation formats. The release
  guide records visual, execution, SQL, link, accessibility, and licensing checks.
- **Created OER and curation are counted separately.** The catalog records what
  the fellowship authored or compatibly adapted; the free-resource catalog
  records what students may access at no cost; and the fellowship folder records
  planning and evaluation work.

## How to Describe the OER Contribution

A concise project description is:

> The project creates a 15-module, lab-first open course in cloud database
> operations. Its original contribution is a coherent evidence cycle across
> relational review, PostgreSQL administration, MongoDB document systems,
> reliability, scaling, and career communication. The current package includes
> 15 open-text modules, 15 weekly guides, 25 individual labs, six completed
> educational notebooks, three reusable data packages, 15 student decks with 214
> slides and complete spoken scripts, 15 transcripts, 15 PDF handouts, five
> public implementation guides, and canonical midterm and final projects. Free
> vendor platforms and tutorials are linked separately and are not counted as
> created OER.

For formal reporting, use this catalog together with the
[deliverable register](fellowship/OER_DELIVERABLE_REGISTER.md), which tracks
planned identifiers and release status.
