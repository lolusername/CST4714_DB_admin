# Catalog of Created Open Educational Resources

## Purpose

This catalog describes the educational resources created or adapted for
*Operating Cloud Databases*. It is the authoritative inventory of course OER.
The separate [fellowship project plan](../oer_fellowship/planning/OER_FELLOWSHIP_PROJECT_PLAN.md)
describes why and how the project is being produced; it is not itself the course
content. The separate [free external resource catalog](external_resources/INDEX.md)
records no-cost vendor and industry resources that the course links but does not
claim as created OER.

- **Inventory date:** September 8, 2026
- **Package license:** original instructional prose and media CC BY-NC-SA 4.0;
  original code MIT; original synthetic data CC0. Source-specific notices control
  adapted material.

## Status Language

- **Draft built:** the editable content exists. This status does not certify
  technical correctness, visual quality, accessibility, or classroom effectiveness.
  A new audit is revising the course; generated exports must match those revisions
  before release. No deposit or public OER release has been approved.
- **In production:** the item is part of the approved scope but is not counted as
  a completed fellowship deliverable.
- **External:** the item costs students nothing but is not course-created OER.

## Created OER at a Glance

| Category | Drafts built | In production | What is original about it |
|---|---:|---:|---|
| Open-text modules | 15 | 0 | one coherent relational-to-document progression built around database reasoning and operations |
| Weekly student guides | 15 | 0 | two-day, lab-first learning sequences with retrieval, worked examples, and transfer |
| Individual in-class labs | 24 | 0 | one manageable submission per lab; no group work or paid dependency |
| Educational notebooks | 7 | 0 | executable instruction with credential-safe cloud paths and open offline fallbacks |
| Data packages | 3 | 0 | two original synthetic cases and one documented public-data transformation |
| Canonical major projects | 2 | 0 | one midterm operations case and one beginner cloud-database final project |
| Assessment resources | 6 files | 0 | diagnostic/post inventory, retrieval bank, writing prompts, common rubrics, and assessment map |
| Student slide decks | 15 | 0 | student-facing teaching decks with complete spoken scripts |
| Deck PDF handouts and transcripts | 30 | 0 | handouts and structured-text versions; visual reinspection follows current revisions |
| Public implementation resources | 5 core guides | 0 | adoption, troubleshooting, accessibility, data-informed teaching, and release support |

Items are counted only once in this table. For example, a slide deck, its PDF,
and its transcript are three files, while the script in both the
notes and transcript is one authored body of instructional prose.

Fourteen weekly guides include an optional, ungraded industry extension. Week 1
uses its single integrated case without another extension. These embedded choices
add no submission and are not extra labs in the inventory count.

## OER 1: Open Textbook and Lab Manual

The 15 modules are not a collection of vendor tutorials. Together they form an
original course narrative: define an operating question, model the mechanism,
make one controlled change, interpret the result, and state the tradeoff.

| ID | Module | Original educational contribution | Status |
|---|---|---|---|
| T01 | [How Database-Backed Applications Work](textbook/module_01_responsibility.md) | request-path model connecting clients, APIs, identity, DBMSs, storage, and managed platforms | Draft built |
| T02 | [Relational Model, Algebra, and SQL](textbook/module_02_sql.md) | major re-entry bridge from mathematical operations to result-grain checks and safe SQL | Draft built |
| T03 | [Schema and Integrity](textbook/module_03_schema.md) | Metro Support schema audit and expected-failure verification | Draft built |
| T04 | [Views and Safe Change](textbook/module_04_change.md) | identity behavior, backward-compatible migration, and honest treatment of unknown historical values | Draft built |
| T05 | [Transactions and Concurrency](textbook/module_05_transactions.md) | two-session model connecting ACID, MVCC, locks, symptoms, and diagnosis | Draft built |
| T06 | [Security](textbook/module_06_security.md) | actor-action-resource matrix and allowed/denied test pattern | Draft built |
| T07 | [Performance](textbook/module_07_performance.md) | question-plan-hypothesis-change-remeasure workflow | Draft built |
| T08 | [Backup and Recovery](textbook/module_08_recovery.md) | free-tier-accurate logical restore and verification framework | Draft built |
| T09 | [NoSQL and JSON](textbook/module_09_nosql_json.md) | NoSQL history and model comparison, JSON choices, graph theory, and vector similarity | Draft built |
| T10 | [MQL and Document Modeling](textbook/module_10_mql_modeling.md) | complete referenced ticket-page reads, authoritative contact corrections, retained versus displayed history, and growth tradeoffs | Revised draft; actual shell examples tested locally |
| T11 | [MongoDB Operations](textbook/module_11_mongodb_operations.md) | aggregation, validation, indexing, and explain measurements in one workload | Draft built |
| T12 | [Reliability](textbook/module_12_reliability.md) | promise-mechanism-failure-verification reasoning | Draft built |
| T13 | [Scale](textbook/module_13_scale.md) | beginner capacity and shard-key reasoning grounded in measurable distributions | Draft built |
| T14 | [Polyglot Systems](textbook/module_14_polyglot.md) | source-of-truth, synchronization, and incident-boundary analysis | Draft built |
| T15 | [Professional Communication](textbook/module_15_careers.md) | translation from technical decisions and results to portfolio and interview language | Draft built |

The earlier [first-edition source](../archive/oer_first_edition/textbook/README.md)
remains preserved for provenance and is not assigned in the current course. The
[current textbook source](textbook/README.md) is the assigned version:
it retains the same 15-module scope while adding conventional mathematical
notation, fully labeled code, editable diagrams, dated and redacted cloud
screenshots, a notation glossary, and reusable technical templates. The
[textbook publishing workspace](textbook/publishing/README.md) builds a
161-page PDF with its editable Word counterpart, standalone HTML, and EPUB with
141 numbered listings and 152 MathML elements. These are revisions and formats of the same 15
modules, not 15 additional modules in the inventory count.

## OER 2: Weekly Guides and Individual Labs

Each [weekly guide](README.md#weekly-course-map) converts module concepts into a
two-class learning sequence. The 24 labs use a stable design: a focused operating
question, a small authentic task, an observable result, a short interpretation, and
one submission. Every lab is individual.

| IDs | Week and lab focus | Count | Status |
|---|---|---:|---|
| L01 | Week 1: trace a request and explain a dashboard's missing rows | 1 | Draft built |
| L03-L04 | Week 2: SQL query ladder; joins, aggregates, and safe DML | 2 | Draft built |
| L05-L06 | Week 3: schema x-ray; integrity constraints | 2 | Draft built |
| L07-L08 | Week 4: views and identity; safe migration | 2 | Draft built |
| L09-L10 | Week 5: paired state/history changes; compare commit and rollback after blocking | 2 | Revised draft; actual SQL and both notebook branches tested locally |
| L11-L12 | Week 6: a restricted analyst report; ownership tests before and after a new row | 2 | Revised draft; actual lab SQL and display code tested locally |
| L13-L14 | Week 7: compare scan work for two result limits; measure an ordered-index change and write a developer recommendation | 2 | Revised draft; actual lab queries, repeated measurements, result IDs, and cleanup tested locally |
| L15 | Week 8: logical restore, known-record comparison, and a concise recovery account in one notebook | 1 | Revised draft; local execution and student variants tested |
| L16 | Week 9: two JSON representations of the same selected ticket facts, with an access-pattern explanation | 1 | Revised draft; paired book/deck examples and lab rows checked against the CSVs |
| L17-L18 | Week 10: exact CRUD and array experiments; a latest-two-event page with retained history and shared contact details | 2 | Revised draft; tested notebook and distinct instructor/student University lessons |
| L19-L20 | Week 11: diagnose a misleading summary and test a date rule; guided sort lab and inventory design response | 2 | Revised draft; tested notebook and distinct instructor demonstration align with the revised deck |
| L21-L22 | Week 12: confirmation and recovery-point decisions; diagnose and repair a misleading MongoDB restore | 2 | Revised lab draft; notebook tested, slide alignment still pending |
| L23 | Week 13: public-data integration and capacity analysis | 1 | Draft built |
| L24 | Week 14: polyglot incident analysis | 1 | Draft built |
| L25 | Week 15: public GitHub concept project and career explanation | 1 | Draft built |

L02 was retired when Week 1 became one integrated lab. It is not counted as an
additional resource. The remaining historical IDs stay stable.

The lab files are linked from their corresponding `weeks/week_01` through
`weeks/week_15` directories. Linked MongoDB University practice is an external resource; the
course-authored prompt, completion requirement, fallback, and interpretation are
the OER contribution.

## OER 3: Educational Notebooks

| ID | Notebook | Educational contribution | Cloud and open path | Status |
|---|---|---|---|---|
| N01 | [Relational and SQL Review](notebooks/01_relational_sql_review.ipynb) | predicts and executes relational algebra, joins, grouping, set operations, and rollback | DuckDB runs locally or in Colab | Draft built |
| N02 | [PostgreSQL Transactions and Locks](notebooks/02_postgres_transactions_locks.ipynb) | interprets a two-session concurrency incident | credential-safe PostgreSQL path plus static incident fallback | Draft built |
| N03 | [PostgreSQL Backup and Restore](notebooks/03_postgres_backup_restore.ipynb) | explains Python/tool/SQL layers, restores a real archive, compares known values, and tests the intended constraint failure | disposable local PostgreSQL; separate optional Supabase connection reference | Revised draft; local and Linux root/sudo paths tested, not hosted Colab |
| N04 | [Atlas MQL and Modeling](notebooks/04_atlas_mql_modeling.ipynb) | teaches direct CRUD, array counterexamples, repeat-write counts, exact cleanup, and model decisions | hidden Atlas credential with temporary runtime-IP rule, or `mongomock` | Revised draft; 96 local/repeated/failure checks, not hosted Atlas or Colab |
| N05 | [MongoDB Logical Recovery](notebooks/05_mongodb_logical_recovery.ipynb) | repairs a wrong document from a verified artifact, checks typed values, and reconstructs omitted rules | runtime Atlas credential or `mongomock`; server schema trace labeled in local mode | Revised draft; both student choices and failure cases tested locally |
| N06 | [Public Data, Capacity, and Integration](notebooks/06_public_data_capacity_integration.ipynb) | evaluates a public source, measures key distributions, and loads idempotently | Atlas, PostgreSQL, or SQLite path | Draft built |
| N07 | [Aggregation and Validation](notebooks/07_aggregation_validation.ipynb) | exposes misleading equal totals after unwind; adds urgency and newest date; tests valid, text, and missing dates | verified-TLS Atlas path with temporary runtime-IP rule, or local aggregation with labeled validation trace | Revised draft; 91 local/repeated/failure checks, not hosted Atlas or Colab |

Notebooks never contain course credentials. Cloud secrets are entered at runtime,
and outputs are checked before publication.

## OER 4: Reusable Data Packages

| ID | Package | Origin and transformation | License/status |
|---|---|---|---|
| D01 | [Metro Support](datasets/metro_support/README.md) | original relational service-desk case with users, tickets, events, and PostgreSQL setup | CC0; Draft built |
| D02 | [Mini Inventory](datasets/mini_inventory/README.md) | original small CSV case for alternative JSON/document designs | CC0; Draft built |
| D03 | [CISA KEV Teaching Sample](datasets/cisa_kev_sample/README.md) | 75-record, field-reduced, versioned transformation of an official U.S. government feed | source terms retained; transformation code MIT; Draft built |

D03 is not described as an original dataset. Its README records the source,
retrieval metadata, transformation, omissions, safety limits, and applicable
source terms.

## OER 5: Assessment and Project Materials

| ID | Resource | Purpose | Status |
|---|---|---|---|
| A01 | [Diagnostic](assessments/diagnostic.md) | low-stakes baseline of relational, SQL, evidence, security, recovery, and document reasoning | Draft built |
| A02 | [Critical and Career Writing](assessments/critical_writing.md) | eight novice-supported explanations integrated into existing labs, with a separate link to the Week 11 video response | Draft built |
| A03 | [Common Rubrics](assessments/rubrics.md) | transparent criteria for technical evidence and communication | Draft built |
| A04 | [Assessment Map](assessments/README.md) | explains formative and summative evidence and data stewardship | Draft built |
| A05 | [Retrieval and Exit Bank](assessments/retrieval_exit_bank.md) | 15 module-aligned sets for low-stakes spaced practice and instructional decisions | Draft built |
| A06 | [Post-Course Inventory](assessments/post_course_inventory.md) | paired applied-concept, confidence, access, and material feedback measure | Draft built |
| P01 | [Midterm Operations Case](assignments/midterm_project.md) | one canonical PostgreSQL/Supabase operations investigation | Draft built |
| P02 | [Final Cloud Database Project](assignments/final_project.md) | one canonical beginner project using PostgreSQL, MongoDB, or a justified combination | Draft built |

Private student records, answer keys, named-student analytics, and private grading
notes are not OER and are not included in the public package.

## OER 6: Student-Facing Slides and Study Formats

The package includes 15 PowerPoint decks containing 321 authored slides. Each
slide has notes reproduced in a matching structured-text transcript, and every
deck has a PDF handout. Weeks 1-11 now have substantively revised student-facing
instruction and word-for-word educational scripts. Their 262 slides and PDF
pages have been individually reviewed. The remaining 59 slides in Weeks 12-15
still need the same review against revised labs and book chapters; older notes
or visual checks do not certify the new teaching sequence. The
existing PDFs provide extractable text. Earlier automated inspection found
limited tag semantics; each revised export still needs semantic and reading-order
review. The handouts are therefore not certified accessible PDFs. The transcript
and chapter provide structured-text alternatives, with their own accessibility
review still required.

| ID | Week and original instructional role | Slides | Available formats | Status |
|---|---|---:|---|---|
| S01 | application request path, PostgreSQL/Supabase, MongoDB/Atlas, relational notation, and one integrated missing-request lab | 17 | [PPTX](weeks/week_01/week_01_responsibility_relational_thinking.pptx), [PDF](weeks/week_01/week_01_responsibility_relational_thinking.pdf), [transcript](weeks/week_01/week_01_responsibility_relational_thinking_transcript.md) | Revised draft; SQL and visual checks recorded |
| S02 | major SQL review with matching-pair diagrams, concrete NULL results, a zero-inclusive staff report, and safe transaction rehearsal | 21 | [PPTX](weeks/week_02/week_02_relational_algebra_sql_review.pptx), [PDF](weeks/week_02/week_02_relational_algebra_sql_review.pdf), [transcript](weeks/week_02/week_02_relational_algebra_sql_review_transcript.md) | Draft revised; slide/PDF review and local PostgreSQL checks complete |
| S03 | schemas, dependencies, types, metadata, and passing/rejected integrity tests | 20 | [PPTX](weeks/week_03/week_03_schemas_constraints_integrity.pptx), [PDF](weeks/week_03/week_03_schemas_constraints_integrity.pdf), [transcript](weeks/week_03/week_03_schemas_constraints_integrity_transcript.md) | Revised draft; local examples and rendered exports checked |
| S04 | worked views and query results, generated identity gaps, column contracts, complete migration and tests, and a precisely captioned Supabase rollback example | 21 | [PPTX](weeks/week_04/week_04_views_identity_safe_change.pptx), [PDF](weeks/week_04/week_04_views_identity_safe_change.pdf), [transcript](weeks/week_04/week_04_views_identity_safe_change_transcript.md) | Draft built; current SQL and visual review completed |
| S05 | complete paired writes, transaction failures, MVCC and isolation results, competing-writer diagrams, and a commit/rollback comparison | 23 | [PPTX](weeks/week_05/week_05_transactions_mvcc_locks.pptx), [PDF](weeks/week_05/week_05_transactions_mvcc_locks.pdf), [transcript](weeks/week_05/week_05_transactions_mvcc_locks_transcript.md) | Revised draft; local examples and all slide/PDF pages checked |
| S06 | complete report-reader setup, safe allowed/denied tests, row visibility and new-row comparisons, view-owner boundaries, verified identities, and secret handling | 24 | [PPTX](weeks/week_06/week_06_identity_permissions_rls.pptx), [PDF](weeks/week_06/week_06_identity_permissions_rls.pdf), [transcript](weeks/week_06/week_06_identity_permissions_rls_transcript.md) | Revised draft; 39 local checks and all slide/PDF pages reviewed |
| S07 | captured plan rows, estimates and buffers, B-tree and composite-key diagrams, complete partial-index experiment, a nonmatching query, measured storage, and developer writing | 24 | [PPTX](weeks/week_07/week_07_query_plans_index_design.pptx), [PDF](weeks/week_07/week_07_query_plans_index_design.pdf), [transcript](weeks/week_07/week_07_query_plans_index_design_transcript.md) | Revised draft; 35 local checks and all slide/PDF pages reviewed |
| S08 | worked recovery times, three-table fixture, actual dump/restore commands, known-value and constraint tests, transactional migration, and midterm clinic | 24 | [PPTX](weeks/week_08/week_08_backup_restore_midterm.pptx), [PDF](weeks/week_08/week_08_backup_restore_midterm.pdf), [transcript](weeks/week_08/week_08_backup_restore_midterm_transcript.md) | Revised draft; 17 code/content checks and all slide/PDF pages reviewed |
| S09 | worked key-value and wide-column patterns, directed traversal, cosine/distance calculations, JSON syntax and interoperability, complete paired designs, and GitHub/Atlas orientation | 32 | [PPTX](weeks/week_09/week_09_nosql_models_json.pptx), [PDF](weeks/week_09/week_09_nosql_models_json.pdf), [transcript](weeks/week_09/week_09_nosql_models_json_transcript.md) | Revised draft; 34 local example checks and all slide/PDF pages reviewed |
| S10 | Atlas connection layers, actual Python CRUD and array results, repeat-write counts, atomic updates, referenced page reads, and growing histories | 28 | [PPTX](weeks/week_10/week_10_mql_document_modeling.pptx), [PDF](weeks/week_10/week_10_mql_document_modeling.pdf), [transcript](weeks/week_10/week_10_mql_document_modeling_transcript.md) | Revised draft; 69 local slide/guide checks and all slide/PDF pages reviewed |
| S11 | SQL-to-pipeline bridge, exact four-ticket results, equal-total identity trap, BSON date counterexamples, measured compound-index work, and case writing | 28 | [PPTX](weeks/week_11/week_11_aggregation_validation_indexes.pptx), [PDF](weeks/week_11/week_11_aggregation_validation_indexes.pdf), [transcript](weeks/week_11/week_11_aggregation_validation_indexes_transcript.md) | Revised draft; 79 exported-example checks and all slide/PDF pages reviewed |
| S12 | replication, read/write settings, partition choices, Atlas plan boundaries, and logical recovery | 17 | [PPTX](weeks/week_12/week_12_mongodb_reliability.pptx), [PDF](weeks/week_12/week_12_mongodb_reliability.pdf), [transcript](weeks/week_12/week_12_mongodb_reliability_transcript.md) | Draft built |
| S13 | capacity analysis, replication versus sharding, shard-key risk, and safe integration | 15 | [PPTX](weeks/week_13/week_13_scale_integration.pptx), [PDF](weeks/week_13/week_13_scale_integration.pdf), [transcript](weeks/week_13/week_13_scale_integration_transcript.md) | Draft built |
| S14 | polyglot ownership, transactional outbox, idempotency, reconciliation, and incident repair | 13 | [PPTX](weeks/week_14/week_14_polyglot_incident.pptx), [PDF](weeks/week_14/week_14_polyglot_incident.pdf), [transcript](weeks/week_14/week_14_polyglot_incident_transcript.md) | Draft built |
| S15 | integrated review, publication safety, portfolio writing, and interview communication | 14 | [PPTX](weeks/week_15/week_15_synthesis_careers.pptx), [PDF](weeks/week_15/week_15_synthesis_careers.pdf), [transcript](weeks/week_15/week_15_synthesis_careers_transcript.md) | Draft built |

## OER 7: Public Adoption and Implementation Materials

| ID | Resource | Reuse contribution | Status |
|---|---|---|---|
| I01-I15 | [Course Implementation Guide](instructor/implementation_guide.md) | 15 two-class lesson plans with outcomes, live-demo boundaries, misconceptions, fallbacks, and teaching decisions | Draft built |
| I16 | [Technical Setup and Troubleshooting](instructor/technical_setup_troubleshooting.md) | safe free-platform setup, Atlas TLS and Supabase network diagnosis, tool compatibility, and outage paths | Draft built |
| I17 | [Accessibility and Adaptation](instructor/accessibility_adaptation.md) | accessible authoring, equivalent evidence, cognitive-load, notebook, slide, and adaptation practices | Draft built |
| I18 | [Data-Informed Teaching Protocol](instructor/data_informed_teaching.md) | low-stakes evidence cycle, aggregate decision rules, privacy, and revision reporting | Draft built |
| I19 | [Production, Validation, and Release Guide](RELEASE_CHECKLIST.md) | inventory, pedagogy, technical, accessibility, licensing, privacy, and release checks with a reusable validator | Draft built |

These are public adoption resources, not private answer keys. Private student
records and grading notes remain outside the release.

## What Is Not Counted as Created OER

The following items may support the project but are deliberately excluded from
the created-OER totals:

- fellowship plans, schedules, evaluation protocols, and administrative reports;
- free vendor platforms, vendor courses, official documentation, and account
  services linked in `external_resources/INDEX.md`;
- the underlying CISA source records, which are documented as a public-data
  transformation rather than an original course dataset;
- private student records, private grading notes, answer keys, credentials, and
  internal teacher-only material; and
- temporary authoring, rendering, inspection, or slide-generation files used to
  produce and validate the published formats.

## Fellowship Talking Points About the Created OER

- **The package is one course, not a folder of unrelated tutorials.** One Metro
  Support case and one question-model-test cycle connect relational review, PostgreSQL
  administration, MongoDB modeling, recovery, scale, incidents, and career
  communication.
- **The relational review is a major original bridge.** The first three weeks
  rebuild forgotten SQL through grain, relational algebra, prediction, execution,
  and verification before administration lessons assume query fluency.
- **The labs reduce logistics without reducing thinking.** Twenty-four
  individual, in-class labs use one explicit submission, a small authentic task,
  observable results, and a short interpretation. No graded lab depends on
  group formation.
- **Cloud access has documented alternatives.** Supabase and Atlas provide
  authentic interfaces. Local database paths and labeled simulations support
  practice when hosted access is unavailable. A static trace supports analysis,
  but does not establish that a student operated a live service. Vendor courses
  remain linked free resources and are not presented as authored OER.
- **The slide collection is a substantial authored teaching resource.** Fifteen
  decks contain 321 draft slides, native diagrams, redacted platform
  screenshots, and code examples,
  complete word-for-word scripts in notes, exact transcripts, and PDF handouts.
  The current revision replaces generic teaching directions with actual spoken
  explanations. Weeks 1-10 have completed this alignment and visual export review;
  image alt text and semantic reading order still need accessibility work.
- **Open executable materials make operations inspectable.** Seven notebooks,
  PostgreSQL setup files, synthetic data, a documented CISA transformation, and
  credential-safe examples let adopters reproduce query, concurrency, recovery,
  modeling, and integration workflows.
- **Assessment is tied to workplace communication.** Labs and writing prompts
  ask students to state a decision, interpret a result, identify a tradeoff, and name
  a limitation. The final module translates that work into portfolio and
  interview language without inflating technical scope.
- **Multiple editable formats support access.** Core prose is
  structured Markdown; spoken content is available as exact transcripts; decks
  use large, high-contrast student-facing layouts; and cloud alternatives state
  what they do and do not reproduce. PDFs are described as handouts whose
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
> operations. Its original contribution is a coherent question-model-test cycle across
> relational review, PostgreSQL administration, MongoDB document systems,
> reliability, scaling, and career communication. The current package includes
> 15 open-text modules, 15 weekly guides, 24 individual labs, seven drafted
> educational notebooks, three reusable data packages, 15 student decks with 321
> slides and complete spoken scripts, 15 transcripts, 15 PDF handouts, five
> public implementation guides, and canonical midterm and final projects. Free
> vendor platforms and tutorials are linked separately and are not counted as
> created OER.

For formal reporting, use this catalog together with the
[deliverable register](../oer_fellowship/planning/OER_DELIVERABLE_REGISTER.md), which tracks
planned identifiers and release status.
