# Midterm Operations Case: Repair Metro Support

## Purpose

The midterm asks you to demonstrate the PostgreSQL and Supabase skills from the
first half of the course in one connected case. Metro Support has a small but
unreliable help-desk database. You will build it reproducibly, test one
transaction, diagnose one blocking incident, make one defensible improvement,
and write a recovery verification plan.

This is an individual project. Correct, well-explained work matters more than
complexity.

## Starting Materials

Start from [Metro Support's schema and seed SQL](../datasets/metro_support/postgres_setup.sql).
The [dataset guide](../datasets/metro_support/README.md) explains its three CSVs.
Work in your own Supabase practice project or a local/instructor-provided
PostgreSQL environment.

## Your Work

### 1. Build and Verify

Create the Metro Support schema from a script. It must include:

- three related tables;
- primary and foreign keys;
- sensible data types;
- at least three non-key integrity controls, such as `NOT NULL`, `UNIQUE`, or
  `CHECK`; and
- seed data from the supplied CSV files or equivalent insert statements.

Write two verification queries that confirm the row counts and relationships are
what you expect.

### 2. Show Transaction Control

Demonstrate one change that is rolled back and one change that is committed.
Record the query you used to check each outcome.

### 3. Diagnose Blocking

Use [Week 5's notebook](../notebooks/02_postgres_transactions_locks.ipynb) to create
a controlled block and automatically release it. Capture the
diagnostic SQL and a small text record of:

- which session was blocked;
- which session was blocking it;
- what resource or row was involved; and
- how you safely resolved and verified the incident.

If a PostgreSQL connection is unavailable, analyze the notebook's supplied trace
and explicitly label that path. Explain the resolving action and final state;
do not claim to have executed a live incident. This fallback has the same
reasoning criteria as the weekly lab.

### 4. Make One Improvement

Choose one improvement supported by a specific risk, rule, or workload:

- a least-privilege role or grant;
- a row-level security policy test;
- an index tied to a real query and plan; or
- a safe schema change with a verification and rollback plan.

Explain the original risk, the change, the result after the change, and one
remaining tradeoff.

### 5. Plan Recovery

Write a one-page runbook for creating a logical backup and restoring it into a
separate environment. You may perform the restore for extra practice, but the
required work is a platform-accurate plan with commands or interface steps,
a safe destination, and at least three verification checks.

Supabase Free does not promise automatic backups. Your plan must therefore use a
logical export such as `pg_dump`, the Supabase CLI, or an instructor-approved
equivalent rather than a paid dashboard feature.

## Submit One Package

Submit one folder or zip with two core files:

- `midterm.sql`: the schema/seed script, verification queries, transaction work,
  and chosen improvement, separated by clear SQL comments. Keep deliberate
  expected-failure statements commented so the normal run can finish.
- `README.md`: run order and environment, a few relevant results, the blocking
  diagnosis, your improvement explanation, and the recovery plan.

If you modified the blocking notebook, include it rather than copying its
Python into SQL. You may split a long code file for readability, but extra files,
screenshots, and repeated reports earn no additional credit. The README is the
single place for the explanation and recovery plan.

Do not submit passwords, connection strings, API keys, or service-role keys.

## Rubric: 100 Points

| Area | Points | What strong work shows |
|---|---:|---|
| Reproducible schema and data integrity | 25 | scripts run in order; relationships and controls match the case; verification is explicit |
| Transactions and blocking diagnosis | 25 | rollback/commit outcomes are checked; blocking state is correctly interpreted and safely resolved |
| Workload-based improvement | 20 | change addresses a real risk or workload; before/after results and tradeoff are clear |
| Recovery readiness | 15 | runbook is safe, free-tier accurate, and includes meaningful restore checks |
| Documentation and professional communication | 15 | package is organized, secrets are absent, results are readable, and another person can follow it |

## Scope Guardrails

Do not add a web application, advanced trigger framework, or unrelated feature.
Use only PostgreSQL/Supabase skills taught by Week 8. A smaller correct solution
with clear results earns more credit than a large solution that cannot be
reproduced or explained.
