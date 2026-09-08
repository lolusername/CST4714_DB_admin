# Visual Showcase: Operating Cloud Databases

This short gallery is the recommended visual route through the fellowship
project. It demonstrates the size, coherence, technical depth, and currentness of
the work without requiring a reviewer to browse the repository. The complete
inventory remains in the [OER catalog](../../course/OER_CATALOG.md).

## How to Use This Page

Show the first four images to explain the authored learning progression. Show
the final six to explain how current cloud interfaces were investigated,
redacted, interpreted, and converted into durable instruction. The interface
screenshots are evidence used inside original explanations; the vendor interface
itself is not claimed as authored OER.

## 1. Relational Reasoning Comes Before Memorized SQL

![A Week 2 teaching slide maps two small relations into matched join rows and asks students to predict result grain.](images/week02_join_reasoning.png)

**What this demonstrates:** the course does not assume that students remember
SQL. It rebuilds tuple, attribute, key, selection, projection, Cartesian product,
theta join, and result-grain reasoning before administration tasks depend on
those ideas. The second-edition text uses conventional symbols such as
$\sigma$, $\pi$, $\rho$, $\times$, and $\bowtie$ and then translates them into
SQL.

**Authorship boundary:** the explanation, diagram, sequence, slide, exact speaker
script, practice task, and Metro Support examples are course-authored OER.

## 2. Performance Is Taught as a Controlled Experiment

![A Week 7 slide shows a baseline, one controlled index change, and a repeated query-plan measurement.](images/week07_controlled_experiment.png)

**What this demonstrates:** students do not learn that an index is a magic
speed button. They state the workload, capture a baseline plan, change one
variable, rerun the same query, compare rows and plan evidence, and discuss the
write, storage, and maintenance cost. This evidence cycle recurs throughout the
textbook, labs, notebooks, and projects.

**Authorship boundary:** the controlled-experiment framework, fixture, lab,
visual, and interpretation prompts are course-authored OER. PostgreSQL itself
and its documentation are not.

## 3. NoSQL Begins With Workload Choice, Not Product Advocacy

![A Week 9 slide routes workload questions toward key-value, wide-column, document, graph, and vector models.](images/week09_model_choice.png)

**What this demonstrates:** the course explains the evolution and historical
meanings of NoSQL, then introduces key-value, wide-column, document, graph, and
vector systems through the questions they make direct. Students also learn basic
graph notation and cosine similarity rather than seeing graph and vector
databases as unexplained product categories.

**Authorship boundary:** the synthesis, decision visual, JSON alternatives,
graph/vector explanations, and student activities are course-authored OER.
Linked historical papers and vendor documentation remain attributed sources.

## 4. MongoDB Operations Connect Modeling, Rules, and Evidence

![A Week 11 slide explains a MongoDB JSON Schema validator and the evidence needed before enforcing it.](images/week11_validator.png)

**What this demonstrates:** MQL is not isolated syntax practice. Students connect
document shape to access patterns, aggregation grain, schema validation,
compound indexes, and `explain("executionStats")` evidence. The live instructor
activity and assigned individual MongoDB University lab are deliberately
different.

**Authorship boundary:** the course explanation, worked examples, assignment
wrapper, fallback, and evidence requirements are OER. MongoDB University and
MongoDB-supplied educator presentations remain free vendor materials in
[free external resource catalog](../../course/external_resources/INDEX.md).

## 5. Atlas Demonstrates Shared Responsibility

![A redacted Atlas Free project overview shows an active deployment and a separate warning that the current client address cannot connect.](images/atlas_project_overview.png)

**What students learn:** service health and connection readiness are different
facts. Atlas can operate the deployment while the customer still owns network
access, database identity, data loading, modeling, query behavior, and recovery
evidence. The screenshot was captured from a free course project on August 25,
2026 and redacted before inclusion.

## 6. Data Explorer Still Has Connection Prerequisites

![A redacted Atlas Data Explorer screen shows the interface before a usable database connection has been configured.](images/atlas_data_explorer.png)

**What students learn:** a visible database tool is not proof that the client is
authorized, that a database user exists, or that an application can connect.
Students diagnose service, network, TLS, identity, authorization, and object
layers separately instead of weakening certificate validation or guessing.

## 7. Free-Tier Plan Limits Change the Recovery Design

![A redacted Atlas backup screen offers paid continuous or daily backup upgrades rather than an active free-tier backup.](images/atlas_free_tier_backup.png)

**What students learn:** a backup menu is not evidence that a recoverable
artifact exists. The course records the plan boundary, teaches a logical
`mongodump`/`mongorestore` path, requires a separate restore target, and asks for
structure, data, behavior, and limitation evidence.

## 8. Supabase Makes Managed PostgreSQL Observable

![A redacted Supabase project overview reports a healthy Nano project and no backups.](images/supabase_project_overview.png)

**What students learn:** a healthy managed service does not prove schema quality,
query correctness, authorization, or recoverability. The visible lack of backups
becomes an operating constraint to document, not a reason to invent coverage the
free plan does not provide.

## 9. An Empty Table Editor Is a Schema Question

![A redacted Supabase Table Editor shows an empty public schema.](images/supabase_table_editor.png)

**What students learn:** the dashboard distinguishes a project, database,
schema, table, and row. Starting from an empty schema supports deliberate table,
key, relationship, constraint, and access-policy decisions rather than treating
the interface as the model.

## 10. A Reversible Test Produces Better Evidence Than a Success Banner

![A redacted Supabase SQL Editor result shows rollback_verified equals true after a temporary table transaction was rolled back.](images/supabase_sql_rollback.png)

**What students learn:** the live smoke test used a temporary table inside an
explicit transaction and verified that rollback removed it. The result teaches
transaction boundaries, expected state, verification, and cleanup without
leaving persistent course data. A generic `Success` message would be weaker
evidence.

## What the Full Package Adds Beyond These Images

The gallery represents, but does not replace, the complete system: 15 textbook
chapters, 15 two-class weekly guides, 25 individual labs, six notebooks, three
data packages, 15 fully scripted student decks, assessments, two major projects,
instructor adoption guidance, accessibility and currentness records, and a
reproducible Word/PDF/HTML/EPUB publication pipeline.

The current second-edition draft is 119 pages and contains 106 numbered code
listings, 142 MathML equations, editable diagrams, a notation glossary, evidence
templates, and dated/redacted cloud-interface figures. It remains an unpublished
draft pending review, classroom use, revision, approval, and authorized release.
