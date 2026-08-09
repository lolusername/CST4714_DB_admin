# Lab 2: Diagnose One Blocking Relationship

## Purpose

Create one controlled row lock, identify the blocked and blocking sessions, resolve
the incident without terminating the wrong session, and verify the final state.

This is individual work completed in class. Use only your personal course database
or the instructor-approved environment.

## Primary Path: Course Notebook

Open [`02_postgres_transactions_locks.ipynb`](../notebooks/02_postgres_transactions_locks.ipynb)
in Colab. The notebook:

1. prompts at runtime for a temporary PostgreSQL connection string;
2. opens two clearly labeled database sessions;
3. creates a disposable `lock_lab` table;
4. leaves one update uncommitted;
5. starts a competing update;
6. queries `pg_stat_activity` and `pg_blocking_pids` from a diagnostic connection;
7. rolls back the blocker; and
8. verifies the final row.

Use a Supabase session-pooler connection when your network cannot reach the direct
IPv6 endpoint. Never paste the connection string into a Markdown or code cell.

Complete the notebook's incident-record Markdown prompts with:

- blocked PID and query;
- blocking PID and transaction age;
- evidence that proves the relationship;
- resolution action and why it targeted the blocker; and
- final-state verification.

## Fallback Path

If the cloud database is unavailable, use the supplied transcript embedded in the
notebook. Identify the same relationship and write the resolution and verification
steps. The reasoning and grading criteria are identical.

## Submit One Thing

Submit the completed notebook file. Before submission, restart and run all
non-cloud cells, confirm no connection string appears in cell source or output,
and keep only the concise evidence needed for the incident record.
