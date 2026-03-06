# CST4714 Database Administration
## Midterm Project Options 

## Due March 26, 2026

This version is adapted from the historical midterm options and aligned to what this class has covered so far:
- Week 1-2: PostgreSQL + Supabase foundations
- Week 3: Admin/DevOps operations in Supabase
- Week 4: schema management (views, identity/sequences, constraints, introspection)
- Week 5: transactions, isolation basics, locking/blocking diagnosis

Project weight: **35%** of final grade.

You may choose one of three tracks. All tracks use one shared rubric.

---

## Shared Expectations (All Tracks)

Every track must demonstrate:
1. SQL reproducibility (clear scripts someone else can run).
2. Data integrity thinking (constraints + schema clarity).
3. Operational evidence (screenshots or logs showing what happened).
4. Concurrency literacy (commit/rollback and at least one lock/blocking diagnostic).
5. Clear documentation of choices and tradeoffs.

Required evidence in all tracks:
- `COMMIT` vs `ROLLBACK` demonstration
- one blocking/waiting scenario with metadata evidence (`pg_stat_activity`, optionally `pg_blocking_pids`)
- at least one admin/ops control from class (roles/grants, RLS test, backup/restore check, or migration workflow evidence)

---

## Track 1: Structured Build (Recommended Default)

Best for students who want a guided technical path.

### Requirements
1. Build a small domain schema with **3+ related tables**.
2. Use **PK/FK** and at least **2 additional constraints** (`CHECK`, `UNIQUE`, `NOT NULL`, etc.).
3. Load sample data (minimum **15 rows per core table**).
4. Write **6 SQL queries**:
- at least 2 joins
- at least 1 aggregate/grouping query
- at least 1 subquery or CTE
- at least 1 view-based query
5. Show one transaction demo:
- explicit `BEGIN`
- one `ROLLBACK` outcome
- one `COMMIT` outcome
6. Show one lock/block diagnostic in two sessions.
7. Complete one admin task:
- roles/grants setup, or
- backup and restore verification, or
- migration-style change + verification script

### Deliverables
- `schema.sql`
- `seed_data.sql`
- `queries.sql`
- `admin_ops.sql` (roles, backup steps, or migration checks)
- ER diagram (image or PDF)
- short report (3-5 pages)
- screenshot folder (8-12 screenshots)

---

## Track 2: Operations and Incident Analysis Report

Best for students who prefer analysis/reporting with practical SQL evidence.

### Requirements
1. Start from an existing class dataset/schema (e.g., club tables).
2. Document current schema risks (at least **3 findings**).
3. Implement **2 concrete improvements** (constraint, view, or role/policy adjustment).
4. Reproduce one concurrency incident:
- blocking/wait scenario
- diagnostics query output
- mitigation choice and verification
5. Include one backup/recovery readiness check or migration verification workflow.

### Deliverables
- `changes.sql` (all implemented changes)
- `incident_walkthrough.sql` (commands used in incident simulation)
- technical report (5-7 pages) with before/after evidence
- screenshot folder (8-12 screenshots)

---

## Rubric (All Tracks, 100 Points)

1. Schema and Integrity Design - 20
- relationships are coherent
- constraints are intentional and correct

2. SQL and Analysis Quality - 20
- queries are correct, meaningful, and readable

3. Transactions and Concurrency Evidence - 20
- commit/rollback and blocking diagnosis are correctly demonstrated

4. Admin/DevOps Execution - 25
- security, backup/recovery, or migration discipline is demonstrated with evidence

5. Documentation and Professionalism - 15
- artifacts are complete, well organized, and interpretable by another reviewer

---

## Guardrails (So Scope Matches Class Progress)

Required:
- stay within technologies taught so far (PostgreSQL + Supabase core features)
- prioritize correctness, evidence, and explanation over complexity

Optional but not required:
- advanced trigger frameworks
- recursive query-heavy architectures
- external app stack integration

No penalty for choosing simpler implementation if evidence and reasoning are strong.


---

## Submission Package (Single Folder/Zip)

1. `README.md` with run order.
2. SQL files.
3. ER diagram.
4. Report/reflection PDF or Markdown export.
5. Screenshots folder.
6. Optional repo link (if used).

---

## Quick Track Selection Advice

- Choose **Track 1** if you want structure and direct practice.
- Choose **Track 2** if you are stronger in analysis and technical writing.

If no track is declared, default to **Track 1**.
