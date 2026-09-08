# Week 3 Instructor Notes
## PostgreSQL Administration + DevOps in Supabase (Deep Guide)

This guide is designed to let you teach Week 3 with confidence, answer advanced student questions, and explain both practical steps and the theory behind them.

If you only have 10 minutes before class, read these sections first:
1. `What Week 3 Is Really About`
2. `The Three Mental Models You Must Teach`
3. `Classroom Demo Flow (90 minutes)`
4. `Hard Questions Students Will Ask`
5. `One-Page Teaching Cheat Sheet`

---

## What Week 3 Is Really About

Week 3 is not “clicking around Supabase.”
Week 3 is students learning to think like operators of a real database system.

Your official course outline says Week 3 focuses on **database structures in Postgres**: schemas, tables, indexes, and reflection. This lesson extends that into real-world admin/DevOps behavior using Supabase as the managed platform.

The operational message to students is:
- A managed platform removes some infrastructure burden.
- It does **not** remove responsibility for correctness, performance, security, and recovery.

If students leave Week 3 with this mindset, they are on track for the midterm project and for internship-level production thinking.

---

## The Three Mental Models You Must Teach

### 1) Structure model: where objects live
Use this hierarchy repeatedly:
- Postgres server/cluster
- Database
- Schema
- Table, view, function, index, sequence

Most student confusion comes from mixing **database** and **schema**.
A reliable sentence to use in class:

> “A database is the container you connect to. A schema is the namespace inside that database.”

### 2) Concurrency model: why reads/writes behave the way they do
Students need basic MVCC intuition:
- Postgres keeps multiple row versions.
- Readers usually see a snapshot.
- Writers create new row versions.
- Vacuum cleans up dead versions later.

Without this, they cannot understand locking behavior, autovacuum, or why long transactions are dangerous.

### 3) Operations model: how change should happen
Teach every change as this sequence:
1. Plan the change.
2. Apply the change (migration-driven).
3. Verify the change (queries + metrics + policy tests).
4. Observe for regressions.
5. Recover if needed (rollback/restore path).

This is the single biggest professional habit students can learn this semester.

---

## Supabase + PostgreSQL: What You Still Own as DBA/DevOps

### Supabase handles a lot
Supabase handles many platform-level tasks, including managed services around Postgres, dashboard tooling, and backup infrastructure options.

### You still own the hard parts that matter
You still own:
- Data model quality
- Query quality
- Index quality
- Role and privilege design
- RLS policy correctness
- Migration safety
- Performance triage
- Incident response quality
- Recovery verification

A strong classroom line:

> “Managed Postgres means fewer server chores, not less accountability.”

---

## Theory Foundation You Should Be Able to Explain

## 1) ACID and why DBAs care operationally

### Atomicity
All or nothing transaction behavior.
Operational relevance: in incidents, partially applied business actions are often atomicity mistakes.

### Consistency
Database constraints and rules remain valid before and after transactions.
Operational relevance: constraints are not just design-time artifacts, they are runtime safety guards.

### Isolation
Concurrent transactions should not create invalid business outcomes.
Operational relevance: isolation choices can trade correctness risks vs throughput.

### Durability
Committed data survives crashes.
Operational relevance: durability depends on WAL and recovery design.

---

## 2) MVCC and row versioning (Postgres core behavior)

Postgres uses MVCC so readers and writers interfere less than in lock-heavy engines.
Key points:
- Each statement sees a snapshot based on isolation level.
- Updates create new tuple versions.
- Old versions remain until no transaction needs them.
- Vacuum reclaims dead tuples.

Why students must understand this:
- It explains bloat.
- It explains why long-running transactions can delay cleanup.
- It explains why “database is slow today” may be a maintenance/stats problem, not just CPU.

---

## 3) Isolation levels and anomalies

In Postgres, practical levels are:
- Read Committed (default)
- Repeatable Read
- Serializable

Teach anomaly vocabulary clearly:
- Dirty read
- Nonrepeatable read
- Phantom read
- Serialization anomaly

Critical nuance:
- PostgreSQL maps `READ UNCOMMITTED` to `READ COMMITTED` behavior.

Operational teaching point:
- Most app workloads can start with Read Committed.
- Critical cross-row invariants may need Serializable or explicit locking patterns.
- Serializable requires retry handling for serialization failures.

---

## 4) Locking and deadlocks

Even with MVCC, locking exists.

What students should know:
- Row-level locks appear with updates and `SELECT ... FOR UPDATE` patterns.
- Table-level locks can occur during DDL and maintenance operations.
- Deadlocks are not “rare bugs”; they are normal in poorly ordered concurrent workflows.

Operational response pattern:
1. Identify blocker/waiter chain.
2. Find the transaction and SQL responsible.
3. Mitigate quickly (sometimes terminate session).
4. Fix design pattern (ordering, transaction scope, access path).

---

## 5) WAL and crash recovery in practical terms

Write-Ahead Logging (WAL) is the durability backbone.

Simple way to explain:
- Data change intent is recorded in WAL before data pages are finalized.
- After crash, WAL is replayed to reach consistent state.

Operational implications:
- WAL rate matters for throughput and storage.
- Backup and PITR workflows depend on WAL continuity.
- High write bursts can expose poor storage/maintenance configuration.

---

## 6) Vacuum, Analyze, and planner statistics

### Vacuum
Reclaims storage from dead tuples and maintains visibility metadata.

### Analyze
Refreshes statistics used by planner for cardinality estimates.

If stats are stale:
- Planner may choose poor plans.
- Query latency becomes unpredictable.

Teach this sentence:

> “Slow query problems are often planner-estimation problems, not only missing-index problems.”

---

## Supabase-Specific Operations You Should Teach Clearly

## 1) Roles in Supabase context

Important default roles students hear about:
- `postgres`
- `anon`
- `authenticated`
- `service_role`
- `authenticator`

Core warning to repeat:
- `service_role` bypasses RLS and must not be exposed in client code.

Good practice:
- Create app-specific roles/users as needed.
- Use least privilege.
- Track grants with SQL, not memory.

---

## 2) RLS as primary data access control

RLS in Supabase is central, not optional.

Teach policy structure with clarity:
- `USING` controls row visibility for SELECT/UPDATE/DELETE.
- `WITH CHECK` controls row validity for INSERT/UPDATE.

Common mistakes:
- Enabling RLS without creating policies.
- Writing overly broad policies using weak predicates.
- Testing only happy path and not deny path.

Professional habit:
- Add policy tests to migration verification checklist.

---

## 3) Connection strategy (direct vs pooler)

Students should understand why connection strategy matters.

Direct connections:
- Good for admin tasks, stable backends, long sessions.

Pooled connections:
- Better for bursty/serverless workloads.
- Reduces connection storm risk.

Operational pitfall:
- Many app outages are actually connection-management failures.

---

## 4) Observability in Supabase

Use these as your operational triad:
- Logs Explorer
- Query/performance reporting surfaces
- SQL diagnostics via Postgres stats views and CLI tools

Teach students to always correlate:
- Time of issue
- Recent migration/deploy event
- Error pattern
- Query pattern

Without timeline correlation, troubleshooting becomes guessing.

---

## Week 3 Deep Content You Can Use in Lecture

## A) Schema governance standards

Students should not treat schema work as ad hoc SQL.

Teach standards:
- Stable naming conventions for tables, indexes, constraints.
- Explicit schema usage for logical separation.
- Migration file for each structural change.
- Short human-readable migration message explaining intent.

Why this matters:
- Faster incident debugging
- Safer collaboration
- Cleaner rollbacks
- Better code review quality

---

## B) Index strategy beyond “add index to slow column”

Teach index selection as workload engineering:
- B-tree for equality/range/order defaults.
- GIN for document/full-text/multi-value scenarios.
- GiST/SP-GiST for specialized structures.
- BRIN for large append-style tables with natural ordering.
- Partial indexes for high-value subsets.
- Composite indexes for frequent multi-column predicates.

Important nuance:
- Every index improves reads but hurts writes and adds maintenance overhead.
- Unused indexes are technical debt with runtime cost.

Classroom demonstration idea:
1. Run `EXPLAIN ANALYZE` before index.
2. Add index.
3. Run same query again.
4. Compare plan and timing.
5. Ask students whether write overhead is worth the gain.

---

## C) Query plan literacy (minimum viable expert level)

Students should learn to read these plan concepts:
- Seq Scan vs Index Scan/Bitmap Heap Scan
- Nested Loop vs Hash Join vs Merge Join
- Estimated rows vs actual rows
- Sort and memory spill indicators

How to sound expert in Q&A:
- Talk in hypotheses: “The planner estimate is off, likely stale stats or correlated predicate.”
- Talk in evidence: “Actual rows differ from estimate by 20x.”
- Talk in controlled changes: “Let’s test one index or rewrite, then re-measure.”

---

## D) Locking triage playbook

When students ask “why is this hanging?” use this flow:
1. Confirm symptom: hanging query, timeout, high latency.
2. Check active sessions and wait events.
3. Identify blocking PID and blocked query.
4. Determine lock type and relation.
5. Decide mitigation: wait, cancel, terminate, or hotfix app pattern.
6. Capture postmortem notes.

Key lesson:
- “Kill session” is incident mitigation, not root-cause resolution.

---

## E) Backup and recovery theory + practice

Different backup mindsets:
- Logical backup (`pg_dump`) for portability and object-level control.
- Physical/managed snapshots for rapid platform recovery patterns.
- PITR for time-targeted recovery.

Restore-first principle:
- A backup is only real when restore has been tested and validated.

Post-restore checklist to teach:
- Schemas/tables present
- Constraints/triggers present
- Critical row counts match expectations
- Critical business queries return expected shape
- App can reconnect and function minimally

---

## F) DevOps migration discipline in Supabase

Use migration-driven release flow:
1. Create migration file (`supabase migration new ...`).
2. Apply/test locally or staging.
3. Review migration SQL.
4. Deploy with `supabase db push`.
5. Run verification SQL.
6. Monitor logs/performance.

Key command set to explain in class:
- `supabase link --project-ref <ref>`
- `supabase db pull`
- `supabase migration new <name>`
- `supabase db push`
- `supabase db diff`

Failure pattern to warn about:
- Dashboard-only schema edits that are not captured in migration history.

---

## G) Security model (roles + policies + secrets)

Your expert framing:
- Grants control object privileges.
- RLS controls row access behavior.
- JWT claims/context map auth identity to policy logic.
- Secret handling controls blast radius outside DB.

Security anti-patterns students should avoid:
- Exposing privileged keys client-side.
- Granting table-level access too broadly.
- Assuming auth alone implies correct data access.
- Skipping deny-case policy testing.

---

## Classroom Demo Flow (90 minutes)

## Segment 1 (10 min): Concept anchor
- Explain shared responsibility in managed Postgres.
- Explain schema vs database vs table vs index.
- Explain why Week 3 is operations discipline.

## Segment 2 (20 min): Supabase surfaces
- Dashboard orientation.
- Database settings and connection modes.
- SQL editor and saved diagnostics.
- Logs and reports navigation.

## Segment 3 (20 min): Schema + index + performance
- Show migration creation.
- Show one index addition.
- Show EXPLAIN ANALYZE before/after.

## Segment 4 (20 min): Security operations
- Show role/grant pattern.
- Show RLS enable + policy creation.
- Show positive and negative policy test queries.

## Segment 5 (10 min): Recovery discipline
- Review backup settings conceptually.
- Show restore checklist.
- Explain why restore drills matter.

## Segment 6 (10 min): Lab briefing
- Required artifacts.
- Scoring emphasis on process evidence.
- Troubleshooting expectations.

---

## Hard Questions Students Will Ask (and Strong Answers)

## Q1) “If Supabase is managed, why do we need DBA skills?”
Answer:
Managed platforms remove some infrastructure burdens, but they do not design your schema, secure your rows, optimize your queries, or validate your recoverability. Those are DBA/DevOps responsibilities and they are exactly what production teams need.

## Q2) “Why did adding an index not speed up my query?”
Answer:
Possible reasons include poor selectivity, stale stats, planner estimates favoring sequential scan, mismatched predicate order in composite index, or small table size where index overhead is not justified. Validate with EXPLAIN ANALYZE and row estimate comparison.

## Q3) “Why do I still get blocked if Postgres uses MVCC?”
Answer:
MVCC reduces read/write blocking, but writes still coordinate through locks. DDL and explicit lock clauses can also block. Long transactions and conflicting updates can create waits or deadlocks.

## Q4) “Is RLS enough without grants?”
Answer:
No. Grants and RLS solve different layers. Grants determine whether a role can attempt an operation on an object. RLS decides which rows are allowed for that operation.

## Q5) “Can I trust backups if the platform says backups are enabled?”
Answer:
You can trust the mechanism, but operational trust requires restore testing and validation. Backup status without restore verification is incomplete risk management.

## Q6) “When should we use Serializable isolation?”
Answer:
Use it when correctness across concurrent multi-row business invariants matters more than throughput, and when your application can handle retries for serialization failures. Many ordinary workloads start at Read Committed.

## Q7) “Why does performance degrade over time without code changes?”
Answer:
Data distribution changes, table growth, bloat, stale stats, connection behavior changes, and workload mix shifts all affect plans and runtime. Performance is dynamic and requires continuous observation.

## Q8) “What is the difference between policy bug and app bug?”
Answer:
A policy bug is data access logic at the database layer. It can expose or block rows regardless of app code correctness. App bugs exist in request handling, but policy bugs live in the data trust boundary.

---

## Instructor-Ready Practical SQL Snippets

Use these as talking examples in class.

## 1) Role and grant baseline
```sql
create role app_readonly;
grant usage on schema public to app_readonly;
grant select on all tables in schema public to app_readonly;
alter default privileges in schema public grant select on tables to app_readonly;
```

## 2) Enable RLS and add simple policy
```sql
alter table public.bookings enable row level security;

create policy bookings_select_own
on public.bookings
for select
using (auth.uid() = user_id);
```

## 3) Lock inspection pattern (example shape)
```sql
select
  a.pid,
  a.usename,
  a.state,
  a.wait_event_type,
  a.wait_event,
  a.query
from pg_stat_activity a
where a.state <> 'idle';
```

## 4) Basic EXPLAIN ANALYZE loop
```sql
explain (analyze, buffers)
select *
from public.bookings
where starttime >= now() - interval '30 days'
order by starttime desc
limit 50;
```

## 5) Post-change stats refresh (when appropriate)
```sql
analyze public.bookings;
```

Use caution when demonstrating on live data. Prefer read-safe examples.

---

## Common Failure Modes and How to Explain Them

## 1) Wrong environment mistakes
Symptom:
- Changes appear “missing” or “unexpected”.

Root cause:
- Working in wrong project or wrong DB target.

Teach fix:
- Confirm project ref and connection target before running change.

## 2) Migration drift
Symptom:
- Local, staging, and remote schemas diverge.

Root cause:
- UI-only edits not captured as migration.

Teach fix:
- Force migration-first workflow and review SQL artifacts.

## 3) RLS lockout
Symptom:
- Queries return zero rows unexpectedly.

Root cause:
- Overly restrictive policy logic.

Teach fix:
- Test policies by role and claim context; include deny and allow cases.

## 4) Connection saturation
Symptom:
- Intermittent connect failures.

Root cause:
- Too many open connections from app pattern.

Teach fix:
- Use pooler where appropriate and tune application connection lifecycle.

## 5) Query regression after deploy
Symptom:
- Endpoint latency spikes after schema change.

Root cause:
- Planner changed path due to data/statistics/index effects.

Teach fix:
- Compare EXPLAIN plans pre/post and roll back quickly if needed.

---

## Week 3 Reflection Prompts (for student discussion)

Use one or two in class:
- “What operational risk is highest in your current project: performance, security, or recoverability? Why?”
- “What is one schema decision that could make incident response easier later?”
- “What evidence would convince you your backup strategy is actually reliable?”
- “What is one policy test that should always be in your release checklist?”

---

## Midterm Alignment (why this week matters)

Week 3 directly supports midterm requirements:
- Schema and migration quality
- Access controls and RLS
- EXPLAIN + indexing performance investigation
- Restore-first runbook

Tell students:

> “If you master Week 3 process habits, the midterm is mostly an execution problem, not a confusion problem.”

---

## One-Page Teaching Cheat Sheet

Use this right before class starts.

## The five sentences to repeat
1. “Managed Postgres changes tooling, not accountability.”
2. “A database is what you connect to; a schema is the namespace inside it.”
3. “Every change must be migration-tracked, verified, and recoverable.”
4. “Grants control object access; RLS controls row access.”
5. “A backup you have not restored is a backup you have not proven.”

## The five checks after any DB change
1. Object exists exactly where expected.
2. Privileges/policies still enforce intended boundaries.
3. Critical query plan did not regress.
4. Logs show no new critical errors.
5. Rollback or recovery path is still valid.

## The five red flags in student work
1. No migration file, only screenshots.
2. No before/after plan evidence.
3. No deny-case RLS test.
4. No restore verification checklist.
5. No environment confirmation proof.

---

## Suggested Teaching Script for Tough Moments

When a student is stuck, use this structure:
1. “Show me the exact symptom.”
2. “Show me the last successful state.”
3. “Show me the exact change that happened between those two points.”
4. “Let’s test one hypothesis only.”
5. “Now document the fix and prevention.”

This keeps class troubleshooting professional and calm.

---

## Relevant Resources (Current + Course Materials)

## Official PostgreSQL docs (primary)
- Concurrency control: [https://www.postgresql.org/docs/current/mvcc.html](https://www.postgresql.org/docs/current/mvcc.html)
- Transaction isolation: [https://www.postgresql.org/docs/current/transaction-iso.html](https://www.postgresql.org/docs/current/transaction-iso.html)
- Explicit locking: [https://www.postgresql.org/docs/current/explicit-locking.html](https://www.postgresql.org/docs/current/explicit-locking.html)
- Routine vacuuming/analyze: [https://www.postgresql.org/docs/current/routine-vacuuming.html](https://www.postgresql.org/docs/current/routine-vacuuming.html)
- EXPLAIN usage: [https://www.postgresql.org/docs/current/using-explain.html](https://www.postgresql.org/docs/current/using-explain.html)
- WAL intro: [https://www.postgresql.org/docs/current/wal-intro.html](https://www.postgresql.org/docs/current/wal-intro.html)

## Official Supabase docs (primary)
- Managing environments: [https://supabase.com/docs/guides/deployment/managing-environments](https://supabase.com/docs/guides/deployment/managing-environments)
- Database migrations: [https://supabase.com/docs/guides/deployment/database-migrations](https://supabase.com/docs/guides/deployment/database-migrations)
- Postgres roles: [https://supabase.com/docs/guides/database/postgres/roles](https://supabase.com/docs/guides/database/postgres/roles)
- Row Level Security: [https://supabase.com/docs/guides/database/postgres/row-level-security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- Query optimization: [https://supabase.com/docs/guides/database/query-optimization](https://supabase.com/docs/guides/database/query-optimization)
- Debugging/monitoring (Inspect): [https://supabase.com/docs/guides/database/inspect](https://supabase.com/docs/guides/database/inspect)
- Backups/PITR: [https://supabase.com/docs/guides/platform/backups](https://supabase.com/docs/guides/platform/backups)
- Postgres logs troubleshooting: [https://supabase.com/docs/guides/troubleshooting/how-to-interpret-and-explore-the-postgres-logs-OuCIOj](https://supabase.com/docs/guides/troubleshooting/how-to-interpret-and-explore-the-postgres-logs-OuCIOj)
- Supabase CLI usage: [https://supabase.com/docs/reference/cli/usage](https://supabase.com/docs/reference/cli/usage)

## Course-local resources
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/CST4714.pdf`
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/week_02/Supabase_deep_drive.pptx`
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/postgres/Docker_Postgres_Supabase.pptx`
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/week_03/Week_03_Postgres_Admin_DevOps_Supabase.pptx`

## Textbook references in your repo
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/textbook_Molina,Ullman - Database Systems The Complete Book.pdf`
  - Useful for deep theory: transactions, logging/recovery, locking, deadlocks, serializability.
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/textbook_Regina O. Obe, Leo S. Hsu - PostgreSQL_ Up and Running_ A Practical Guide to the Advanced Open Source Database (2017, O’Reilly Media).pdf`
  - Useful for practical Postgres admin: roles, grants, backup/restore, EXPLAIN, tuning, replication overview.
- `/Users/atiliobarreda/Desktop/academics/teaching/courses/CST4714_Database_Administration/textbook_PostgreSQL 16 Cookbook.pdf`
  - Useful for operations recipes: WAL/autovacuum, partitioning, HA patterns, backup/recovery runbooks.

---

## Final Reminder Before You Teach

You do not need to know every edge case live.
You need to demonstrate a professional method:
- clear model,
- evidence-based diagnosis,
- controlled change,
- explicit verification,
- documented recovery path.

If you consistently model that behavior in Week 3, students will perceive competence and professionalism, and you will have a stable foundation for the rest of the semester.
