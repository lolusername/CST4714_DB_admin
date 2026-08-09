# Final Cloud Database Project

## Purpose

Design, build, query, and document one small cloud database system. The project
is beginner-friendly and is graded on database decisions and operational
evidence, not on building a polished web application.

This is an individual project.

## Choose One Platform Path

### PostgreSQL with Supabase

Use this path when your data has stable entities, relationships, integrity rules,
SQL reporting needs, or row-level access concerns.

### MongoDB with Atlas

Use this path when your workload benefits from nested documents, flexible fields,
changing event details, document-oriented access patterns, or aggregation
pipelines.

### Both Platforms

Use both only when each system has one clear responsibility. For example,
PostgreSQL might own authoritative users and tickets while MongoDB stores flexible
event details. The split must solve a real modeling or operational problem. More
technology does not automatically earn more credit.

## Beginner-Friendly Ideas

- campus club event tracker;
- small inventory and restock tracker;
- tutoring or appointment scheduler;
- support ticket tracker;
- course resource library;
- book lending tracker;
- personal expense tracker;
- cybersecurity finding tracker; or
- another small scenario approved by the instructor.

## Keep the Scope Small

- PostgreSQL path: 3-5 related tables.
- MongoDB path: 2-4 collections.
- Two-platform path: the smallest defensible split, with one source of truth for
  each kind of record.
- At least 20 realistic records total for a single-platform project, or at least
  10 records in each platform for a two-platform project.

Do not build a full social network, e-commerce platform, learning management
system, multi-tenant SaaS product, or anything that depends on paid cloud
features.

## Required Evidence

### Data Model

- PostgreSQL: tables, columns and types, primary keys, foreign keys, integrity
  constraints, and at least one justified index.
- MongoDB: collections, representative documents, an embedding or referencing
  decision, optional validation where useful, and at least one justified index.
- Both: a diagram or explanation of what each platform owns, how identifiers
  cross the boundary, and why the split is worth its operational cost.

### Queries

Provide at least four meaningful queries that answer realistic questions. At
least one must summarize or aggregate data, and at least one must support an
operational or administrative question.

### Operations

Provide:

- one index decision tied to a real query or workload;
- one access-control or permission concern and your response;
- one logical backup and restore plan that works with your platform's free tier;
- one restore verification checklist; and
- one reliability limitation or tradeoff.

Atlas Free does not include native backup, and Supabase Free does not include
automatic backups. Use platform-appropriate logical tools such as
`mongodump`/`mongorestore`, `mongoexport`/`mongoimport`, `pg_dump`, or an
instructor-approved equivalent.

### Written Explanation

Write 700-1,000 words explaining the project purpose, platform choice, model,
queries, administrative decisions, recovery plan, one tradeoff, and what you
would improve with more time. Use specific evidence from your own project.

### Presentation

Prepare a 5-7 minute demonstration that shows the system's purpose, model, one
query, one operational decision, and one lesson learned. Do not use live
credentials in the presentation.

## Submission

GitHub is encouraged for weekly practice and portfolio evidence, but a public
GitHub repository is not required for the final project.

Submit one package containing:

- schema or model files;
- seed data files;
- query files;
- an `operations_runbook.md`;
- the written explanation; and
- presentation materials.

Also provide one approved verification path:

- reproducible local or cloud-safe files that let the instructor rebuild and
  inspect the work; or
- time-limited, read-only instructor access to the relevant cloud project.

For Atlas, add the instructor to the Atlas project only if the instructor has
provided an account and requested that review method. For Supabase, do not share
your password or service-role key. Follow the course-specific review instructions
in Brightspace.

## Checkpoints

| Week | Checkpoint |
|---:|---|
| 12 | choose a platform and scenario; write a one-paragraph workload statement |
| 13 | create the model, load seed data, and run the first two queries |
| 14 | add index, access, recovery, and reliability evidence; complete an individual review checklist |
| 15 | submit the package and present the project |

Checkpoints are practice toward this assignment, not additional deliverables with
different requirements.

## Rubric: 100 Points

| Area | Points | What strong work shows |
|---|---:|---|
| Data model | 25 | structure matches the workload; relationships or document boundaries are coherent; integrity choices are explicit |
| Meaningful queries | 20 | four correct queries answer real questions and include aggregation and operational evidence |
| Operations and reliability | 20 | index, access, recovery, verification, and tradeoff decisions are specific and technically plausible |
| Seed data and reproducibility | 15 | data is realistic; files or approved access allow verification; secrets are absent |
| Written explanation | 10 | claims use project evidence and acknowledge tradeoffs |
| Presentation | 10 | demonstration is focused, understandable, and technically accurate |
