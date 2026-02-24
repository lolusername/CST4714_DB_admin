# Teacher Cheat Sheet (Open Data Edition)
## Week 3 + Week 4: PostgreSQL and Supabase as Data Stewardship

Use this guide to teach the same technical content with clearer big-picture framing:
- database work as public trust work,
- schema decisions as communication decisions,
- operations discipline as accountability.

---

## 0) 60-Second Positioning Script
"In this class we treat a database as a system of state and invariants.  
Week 3 covers operational discipline: plan, change, verify, recover.  
Week 4 covers schema discipline: views, identity/sequences, constraints, introspection.  
Our goal is not only functional SQL. Our goal is reliable, interpretable data that can be used responsibly by different audiences."

---

## 1) Core Teaching Stance
Repeat this distinction:
- database reliability is technical,
- data trust is socio-technical.

Students should leave with both:
1. engineering skill (correctness, performance, security),
2. stewardship skill (documentation, context, limits, responsible release).

---

## 2) Core Ontology (Teach Precisely)
Hierarchy:
- Postgres cluster/server
- database
- schema
- objects (tables, views, indexes, functions, sequences)

Precision sentence:
- Database is a connection boundary and logical container.
- Schema is a namespace inside a database.

Common correction:
- A new schema is not a new database.

---

## 3) Managed Postgres Reality (Supabase)
What Supabase manages:
- platform infrastructure and managed service surfaces.

What teams still own:
- data model quality,
- query and index quality,
- grants and RLS correctness,
- migration discipline,
- incident and recovery verification,
- documentation quality for future users.

One-line summary:
"Managed Postgres reduces server chores, not responsibility."

---

## 4) Open Data Quality Pillars
Use these as recurring checkpoints in class discussions and grading:

1. Clarity
- Can someone new understand field meaning without tribal knowledge?

2. Integrity
- Do constraints and policies enforce key assumptions?

3. Privacy and minimization
- Are we exposing only what is necessary for the stated purpose?

4. Reproducibility
- Can another person recreate outputs from versioned SQL and documented steps?

5. Provenance
- Can we identify source, transformation logic, and refresh timing?

6. Accessibility
- Are names, labels, and definitions readable for mixed technical backgrounds?

Teach this line:
"If data cannot be interpreted safely, it is not high quality."

---

## 5) Operational Lifecycle (Teach as Algorithm)
For each schema or policy change:
1. Plan
- intent, risks, and rollback path.
2. Apply
- migration-first, no silent dashboard drift.
3. Verify
- output checks, metadata checks, and policy checks.
4. Observe
- logs and performance after release.
5. Recover
- rollback or restore when needed.

Mathematical framing:
- start state `S0`
- migration `M`
- end state `S1 = M(S0)`
- required condition: invariants hold on `S1`

---

## 6) Week 4 Concepts Through the Stewardship Lens

### Views
- Not just convenience.
- They are stable interfaces and interpretation layers.
- They reduce logic drift across teams.

Teaching line:
"A view is a contract about meaning, not just syntax reuse."

### Materialized Views
- Performance tool for repeated analytics queries.
- Explicit freshness tradeoff.

Teaching line:
"Fast but stale is sometimes acceptable, sometimes dangerous. State the rule."

### Identity and Sequences
- IDs model identity, not contiguous counting.
- Gaps are expected under concurrency and rollback.

Teaching line:
"Do not confuse key generation with event chronology."

### Constraints
- Engine-level invariant enforcement.
- Prevents invalid writes from any writer path, not only one app.

Teaching line:
"Constraints are executable policy."

### Introspection
- Trust metadata over memory.
- Use `information_schema` and `pg_catalog` to verify reality.

Teaching line:
"If you cannot prove it from metadata, you do not fully know system state."

---

## 7) Inclusive but Neutral Communication Standards
Use practices that improve precision for all learners:
- define specialized terms the first time you use them,
- avoid idioms that assume cultural context,
- avoid examples that rely on stereotypes,
- separate technical critique from personal language,
- encourage evidence-based disagreement.

For student-facing prompts and feedback:
- ask for assumptions and limits,
- reward clear reasoning,
- require citation of source docs,
- value revision after evidence.

---

## 8) Lab Facilitation Pattern (Week 4)
When students work on views, materialized views, and constraints:
1. Ask what question the object is meant to answer.
2. Ask who will read it and how they might misread it.
3. Ask what integrity rule is enforced and where.
4. Ask how they verify state post-change.
5. Ask what could break if data volume grows.

This keeps discussion above syntax while staying concrete.

---

## 9) Release-Ready Evidence Checklist
Before accepting student work as "complete":
- view definitions are explicit (no `SELECT *`),
- materialized view refresh behavior is documented,
- one failed-write constraint example is shown,
- introspection evidence confirms expected objects,
- write-up states audience and limits,
- SQL is organized for another person to rerun.

---

## 10) High-Probability Questions and Strong Answers

Q: Why not write joins directly every time?  
A: Repeated joins drift over time. Views centralize logic and make interpretation more stable.

Q: Why are IDs skipping values?  
A: Sequences optimize uniqueness under concurrent writes; continuity is not guaranteed.

Q: Are views always faster?  
A: Standard views are definitions, not stored data. Speed depends on the execution plan.

Q: If app code validates, why add constraints?  
A: App validation is one writer path. Constraints protect all writer paths.

Q: How do we prove schema matches intention?  
A: Migration history plus metadata introspection plus targeted verification queries.

---

## 11) Things to Correct Immediately in Class
Avoid:
- "IDs should be continuous."
Use:
- "IDs should be unique and stable; gaps are normal."

Avoid:
- "RLS solves access by itself."
Use:
- "Grants, RLS, and key handling must align."

Avoid:
- "It worked once, so we are done."
Use:
- "Done means applied, verified, and documented."

---

## 12) Fast Pre-Class Checklist (5 minutes)
1. Can you explain database vs schema in one sentence?
2. Can you explain sequence gaps in one sentence?
3. Can you explain standard vs materialized view in one sentence?
4. Can you explain grants vs RLS in one sentence?
5. Do you have one introspection query ready to demo?

If yes, Q&A will be stable.

---

## 13) Suggested Closing Line
"I do not optimize for memorizing commands. I optimize for preserving invariants under change and making data understandable to others."

---

## 14) Core References
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

