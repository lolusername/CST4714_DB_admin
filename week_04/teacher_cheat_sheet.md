# Teacher Cheat Sheet (Week 3 + Week 4)
## PostgreSQL + Supabase DBA/DevOps

Use this as your rapid teaching guide and Q&A defense document.
It is rigorous, but compressed for classroom use.

---

## 0) 60-Second Positioning Script

"In this class, we treat the database as a **state machine with invariants**.  
Week 3 teaches operations discipline in Supabase: plan, change, verify, recover.  
Week 4 teaches schema discipline: views, identity/sequences, constraints, introspection.  
If we preserve invariants and verify state after each change, systems stay reliable.  
If we skip invariants or verification, we get silent corruption, performance regressions, and security failures."

---

## 1) Core Ontology (Say This Clearly)

Hierarchy:
- Postgres cluster/server
- database
- schema
- objects (tables, views, indexes, functions, sequences)

High-precision line:
- **Database** = connection boundary and logical container.
- **Schema** = namespace inside a database.

Common confusion to correct:
- A new schema is **not** a new database.

---

## 2) Managed Postgres Reality (Supabase)

### What Supabase manages
- Platform/infrastructure layer, project services, managed operational surfaces.

### What you still own
- Data model correctness
- Query and index quality
- Role/grant/RLS policy correctness
- Migration safety
- Performance triage
- Recovery verification

Key line:
- "Managed Postgres removes some infrastructure burden, not accountability for data correctness."

---

## 3) The Operational Lifecycle (Teach as Algorithm)

For every DB change:
1. **Plan** (intent + risk + rollback path)
2. **Apply** (migration, not ad hoc drift)
3. **Verify** (SQL checks + metadata checks + expected outputs)
4. **Observe** (logs/performance)
5. **Recover** if needed (rollback/restore path)

Mathematical framing:
- Let state be `S0` (before) and `S1` (after migration `M`).
- You must show:
  - `M(S0) = S1` (change applied)
  - invariants `I(S1) = true` (constraints, permissions, expected row rules)

---

## 4) Identity vs Sequence (Most Important Q&A Topic)

## 4.1 Sequence Semantics (rigorous)
A sequence is an independent monotone generator of candidate keys.
- `nextval(seq)` advances state and returns a value.
- Sequence advancement is **not rolled back** with transaction failure.

Implication:
- Gaps in IDs are expected (rollback, caching, abandoned tx).

Do not promise:
- contiguous numbering
- strict event chronology from IDs

You can promise:
- practical uniqueness under concurrent writes.

## 4.2 `SERIAL` vs `IDENTITY`
- `SERIAL` = legacy shorthand (sequence + default + ownership behavior).
- `IDENTITY` = SQL-standard explicit syntax.

Use in teaching:
- Prefer `GENERATED ... AS IDENTITY` for new design.

## 4.3 Why students think gaps are errors
Because they assume keys model counting. In reality, keys model identity, not arithmetic continuity.

## 4.4 Sequence drift and repair
Drift can occur after manual inserts/imports.
Repair pattern:
1. `max(id)` from table
2. inspect sequence position
3. `setval(...)` to realign
4. test insert

---

## 5) Views (Standard and Materialized)

## 5.1 Standard view
- Stored query definition (virtual relation).
- Great for stable query interface and logic reuse.

Relational algebra view:
- `V = π, σ, ⋈` composition over base relations.

Teaching line:
- "A view is an interface contract over tables."

## 5.2 Why use views
- Avoid copy-paste joins
- Keep business logic centralized
- Expose only needed columns
- Reduce client coupling

## 5.3 Materialized view
- Stores result snapshot physically.
- Performance gain for expensive reads.
- Tradeoff: freshness.

Formal framing:
- If base state is `R(t)`, materialized state is `MV(t0)` until refresh.
- Staleness exists whenever `t > t0` and base data changed.

## 5.4 Refresh
- `REFRESH MATERIALIZED VIEW ...`
- Must be part of operational routine if freshness matters.

---

## 6) Constraints = Executable Invariants

Think of each constraint as predicate `P(row)` or relation-level rule `P(table)`.
Writes are allowed only if predicates evaluate true.

## 6.1 Constraint types you should fluently explain
- `PRIMARY KEY` = uniqueness + not null
- `UNIQUE` = no duplicate non-null combinations (null behavior nuance)
- `FOREIGN KEY` = referential integrity across relations
- `CHECK` = domain/invariant rule

## 6.2 Why constraints beat app-only checks
App checks are bypassable by other writers.
DB constraints are engine-enforced at commit/write boundary.

## 6.3 Safe rollout pattern (`NOT VALID`)
For large tables:
1. add constraint `NOT VALID`
2. new writes checked
3. validate existing rows later (`VALIDATE CONSTRAINT`)

Operational benefit:
- lower migration disruption risk.

---

## 7) Introspection: Trust Metadata, Not Memory

You should be able to prove current state using metadata queries.

## 7.1 Two catalog layers
- `information_schema`: portable, cleaner for teaching
- `pg_catalog`: Postgres-specific depth

## 7.2 Core query pack you should keep
- list tables
- list columns/defaults/nullability
- list constraints by table/type
- list views and definitions
- list indexes

Use introspection in three moments:
1. before migration (baseline)
2. after migration (verification)
3. before release promotion (drift detection)

---

## 8) Supabase Security Model (Q&A critical)

Three layers to explain distinctly:
1. **Role grants** (object-level capability)
2. **RLS policies** (row-level filtering/authorization)
3. **API key handling** (secret exposure risk)

High-value line:
- "Grants decide whether a role can try an operation; RLS decides which rows that operation may touch."

Important warning:
- Privileged server keys and bypass-capable roles must never be exposed in client code.

---

## 9) Performance/Operations Mini-Playbook

When query is slow:
1. confirm symptom and scope
2. inspect plan (`EXPLAIN ANALYZE` pattern)
3. check if issue is access path, cardinality estimate, or join strategy
4. apply one change
5. re-measure

When behavior is inconsistent:
- check for stale stats / maintenance state
- check schema drift
- check role/policy differences across environments

When students are stuck:
- force exact error text + minimal reproducer + one hypothesis at a time

---

## 10) Week 4 Lab: What Is Actually Required Now

Current simplified lab scope:
- use existing Supabase tables (`members`, `facilities`, `bookings`)
- create 2 standard views
- create 1 materialized view + refresh
- do basic constraint practice in a **temporary table**
- run introspection checks

Deliverables only:
1. brief write-up
2. SQL file with queries used
3. screenshots

This is intentionally lighter and aligned to lecture coverage.

---

## 11) High-Probability Student Questions (with strong concise answers)

## Q1: Why not just write joins directly every time?
Because repeated joins create logic drift. Views centralize logic and stabilize the query interface.

## Q2: Why are IDs skipping numbers?
Sequence generators prioritize uniqueness under concurrency, not contiguous arithmetic counting. Rollbacks/caching create gaps normally.

## Q3: Are views faster than tables?
Standard views are query definitions, not stored data; speed depends on underlying plan. Materialized views can be faster but trade freshness.

## Q4: Why use constraints if app already validates?
App validation is not authoritative for all writers. Constraints enforce invariants at the database boundary for every writer.

## Q5: How do I prove production matches intended schema?
Use migration history + metadata introspection and resolve any drift before release.

## Q6: Why did materialized view show old data?
Because it is snapshot-based. It must be refreshed to include recent base-table changes.

---

## 12) Practical “Don’t Say This” Corrections

Avoid:
- "IDs should be continuous."
Say:
- "IDs should be unique and stable; continuity is not guaranteed."

Avoid:
- "RLS is enough by itself."
Say:
- "RLS + grants + key handling must align."

Avoid:
- "If it worked once, migration is done."
Say:
- "Migration is done only after verification and evidence."

---

## 13) Your Fast Pre-Class Checklist (5 minutes)

Before teaching:
1. Confirm you can explain database vs schema in one sentence.
2. Confirm you can explain sequence gaps in one sentence.
3. Confirm you can explain standard vs materialized view in one sentence.
4. Confirm you can explain grants vs RLS in one sentence.
5. Open one introspection query you will demo live.

If you can do those five things, your Q&A will be stable.

---

## 14) Suggested “Expert but Human” Closing Line

"I don’t optimize for memorizing syntax; I optimize for preserving invariants under change.  
If we can state the invariant, implement it, and verify it from metadata, we can run databases safely."

---

## 15) References You Can Cite in Class

- PostgreSQL `CREATE VIEW`:
  [https://www.postgresql.org/docs/current/sql-createview.html](https://www.postgresql.org/docs/current/sql-createview.html)
- PostgreSQL `CREATE MATERIALIZED VIEW`:
  [https://www.postgresql.org/docs/current/sql-creatematerializedview.html](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- PostgreSQL identity columns:
  [https://www.postgresql.org/docs/current/ddl-identity-columns.html](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
- PostgreSQL constraints:
  [https://www.postgresql.org/docs/current/ddl-constraints.html](https://www.postgresql.org/docs/current/ddl-constraints.html)
- PostgreSQL information schema:
  [https://www.postgresql.org/docs/current/information-schema.html](https://www.postgresql.org/docs/current/information-schema.html)
- Supabase migrations:
  [https://supabase.com/docs/guides/deployment/database-migrations](https://supabase.com/docs/guides/deployment/database-migrations)
- Supabase roles + RLS docs:
  [https://supabase.com/docs/guides/database/postgres/roles](https://supabase.com/docs/guides/database/postgres/roles)
  [https://supabase.com/docs/guides/database/postgres/row-level-security](https://supabase.com/docs/guides/database/postgres/row-level-security)
