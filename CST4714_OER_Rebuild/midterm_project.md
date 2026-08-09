# Midterm Operations Case: Repair Metro Support

## Purpose

The midterm asks you to demonstrate the PostgreSQL and Supabase skills from the
first half of the course in one connected case. Metro Support has a small but
unreliable help-desk database. You will build it reproducibly, test one
transaction, diagnose one blocking incident, make one defensible improvement,
and write a recovery verification plan.

This is an individual project. Correct, well-explained evidence matters more than
complexity.

## Starting Materials

Use the course files in [`datasets/metro_support`](datasets/metro_support/) and
the starter SQL published with Week 8. You may work in a dedicated Supabase
project or an instructor-provided PostgreSQL environment.

## Your Work

### 1. Build and Verify

Create the Metro Support schema from a script. It must include:

- three related tables;
- primary and foreign keys;
- sensible data types;
- at least three non-key integrity controls, such as `NOT NULL`, `UNIQUE`, or
  `CHECK`; and
- seed data from the supplied CSV files or equivalent insert statements.

Write two verification queries that prove the row counts and relationships are
what you expect.

### 2. Show Transaction Control

Demonstrate one change that is rolled back and one change that is committed.
Record the query you used to prove each outcome.

### 3. Diagnose Blocking

Use two database sessions to create a controlled blocking situation. Capture the
diagnostic SQL and a small text record of:

- which session was blocked;
- which session was blocking it;
- what resource or row was involved; and
- how you safely resolved and verified the incident.

### 4. Make One Improvement

Choose one improvement supported by evidence:

- a least-privilege role or grant;
- a row-level security policy test;
- an index tied to a real query and plan; or
- a safe schema change with a verification and rollback plan.

Explain the original risk, the change, the evidence that it works, and one
remaining tradeoff.

### 5. Plan Recovery

Write a one-page runbook for creating a logical backup and restoring it into a
separate environment. You may perform the restore for extra practice, but the
required evidence is a platform-accurate plan with commands or interface steps,
a safe destination, and at least three verification checks.

Supabase Free does not promise automatic backups. Your plan must therefore use a
logical export such as `pg_dump`, the Supabase CLI, or an instructor-approved
equivalent rather than a paid dashboard feature.

## Submit One Package

Submit one folder or zip containing:

- `README.md` with the run order and environment used;
- `schema_and_seed.sql`;
- `verification_queries.sql`;
- `transaction_and_lock_lab.sql`;
- `improvement.sql`;
- `evidence.md`, including concise outputs or redacted screenshots and your
  explanations; and
- `recovery_runbook.md`.

Do not submit passwords, connection strings, API keys, or service-role keys.

## Rubric: 100 Points

| Area | Points | What strong work shows |
|---|---:|---|
| Reproducible schema and data integrity | 25 | scripts run in order; relationships and controls match the case; verification is explicit |
| Transactions and blocking diagnosis | 25 | rollback/commit outcomes are proved; blocking evidence is correctly interpreted and safely resolved |
| Evidence-based improvement | 20 | change addresses a real risk or workload; before/after evidence and tradeoff are clear |
| Recovery readiness | 15 | runbook is safe, free-tier accurate, and includes meaningful restore checks |
| Documentation and professional communication | 15 | package is organized, secrets are absent, evidence is readable, and another person can follow it |

## Scope Guardrails

Do not add a web application, advanced trigger framework, or unrelated feature.
Use only PostgreSQL/Supabase skills taught by Week 8. A smaller correct solution
with strong evidence earns more credit than a large solution that cannot be
reproduced or explained.
