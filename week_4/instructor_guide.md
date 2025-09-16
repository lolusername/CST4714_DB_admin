# Week 4 Instructor Guide — Advanced SQL, Constraints, Triggers, and Transactions

This guide gives you everything you need to lead the Week 4 session—even if you are new to the material. The lecture portion is designed for ~50 minutes and flows slide by slide. Each section below provides:

- **Estimated time** to spend on the slide
- **Exact script** you can read or paraphrase
- **Background knowledge** explaining why the concept matters, including quick refreshers on terminology
- **Callouts** that prompt interaction or segue into demos/lab work

The remaining sections cover the live demo, student lab support, and midterm proposal workshop.

---

## Quick Primer Before Class

Spend 15–20 minutes reviewing these concepts so you feel comfortable in front of the room:

- **SQL Functions**: reusable server-side routines created with `CREATE FUNCTION`. Two common languages are SQL (single expression) and PL/pgSQL (procedural).
- **Views vs Materialized Views**: views are stored queries evaluated on demand; materialized views persist the result set and must be refreshed manually.
- **Window Functions**: analytic expressions like `ROW_NUMBER()` or `SUM() OVER (PARTITION BY ...)` that compute aggregates across partitions without collapsing rows. They complement views and functions when building reporting logic.
- **Constraints**: declarative rules such as PRIMARY KEY, UNIQUE, CHECK, FOREIGN KEY, and EXCLUDE that PostgreSQL enforces automatically. Deferrable constraints run at commit.
- **Triggers**: hooks executed before/after table events. A trigger calls a trigger function and can modify or log data.
- **Transactions & ACID**: Atomicity, Consistency, Isolation, Durability. PostgreSQL implements multi-version concurrency control (MVCC) to achieve isolation levels like READ COMMITTED and REPEATABLE READ.
- **Monitoring Tools**: `pg_stat_activity`, `pg_locks`, `log_line_prefix`, and savepoints help diagnose blocking and deadlocks.

If you need a refresher on any term, skim the linked docs in the README first—this guide assumes you know those definitions.

## Hands-On Teacher Reference

Use this section to teach yourself the building blocks before class. Each topic includes a plain-language explanation and a small PostgreSQL snippet you can execute in `psql` or the Supabase SQL editor. Feel free to run these statements in a scratch schema to see the results.

### 1. Functions
- **What**: Reusable routines that run inside the database. PostgreSQL supports multiple languages; the most common are SQL (single expression) and PL/pgSQL (procedural).
- **Syntax walkthrough**:
  1. `CREATE OR REPLACE FUNCTION schema.name(parameter_name parameter_type, ...)` — declares the function and its inputs. Use `OR REPLACE` during development so you can rerun the statement without dropping it first.
  2. `RETURNS data_type` — defines the return value. Use `void` when nothing is returned, `TABLE(...)` or `SETOF` for sets.
  3. `LANGUAGE sql|plpgsql|...` — tells PostgreSQL which language to expect inside the body.
  4. `AS $$ ... $$` — provides the function body. `$$` is a PostgreSQL dollar-quoted string delimiter; it saves you from escaping single quotes inside the function. You can use other markers like `$fn$` as long as they match.
  5. Optional clauses (use them when you need finer control):
     - `IMMUTABLE`, `STABLE`, `VOLATILE`: describe how predictable the function is.
       * `IMMUTABLE` — always returns the same output for the same input (e.g., math). Planner can cache results.
       * `STABLE` — can read data but not modify it; result is consistent within a single statement.
       * `VOLATILE` — default; function may change every call (e.g., now()).
     - `SECURITY DEFINER` vs `SECURITY INVOKER`: choose which role’s privileges execute the body.
       * `INVOKER` (default) uses the caller’s rights.
       * `DEFINER` runs with the function owner’s rights—use sparingly for maintenance tasks.
     - `SET search_path`: temporarily adjusts which schemas the function sees. Set it to avoid surprises if callers change their search path.
- **How PL/pgSQL functions run**: The body executes inside its own transaction context. For row-returning functions, use `RETURN` (scalar) or `RETURN QUERY` (set). `RAISE NOTICE` prints debug messages.
- **Demo**:
```sql
-- Simple SQL function (single expression)
CREATE OR REPLACE FUNCTION util.apply_tax(amount numeric)
RETURNS numeric
LANGUAGE sql
AS $$ SELECT amount * 1.08875; $$;

SELECT util.apply_tax(100);  -- returns 108.875

-- Procedural PL/pgSQL function
CREATE OR REPLACE FUNCTION util.bump_price(product_id uuid, pct numeric)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE products
     SET unit_price = unit_price * (1 + pct)
   WHERE id = product_id;
  RAISE NOTICE 'Price updated for %', product_id;
END;
$$;
```

### 2. Views and Materialized Views
- **What**: Both are named queries. A *view* stores the SQL definition only; the result is computed each time you query it. A *materialized view* stores the query results on disk and must be refreshed to pick up new data.
- **Why views matter**:
  * Encapsulation: hide complex joins or calculations behind a simple `SELECT * FROM view_name`.
  * Security: you can expose only the columns/rows you want and grant permissions on the view instead of the base tables.
  * Stability: changing the underlying query in one place updates every consumer.
- **Why materialized views**: ideal for heavy analytical queries when you can tolerate slightly stale data. Refresh on a schedule or after ETL jobs.
- **Syntax walkthrough**:
  1. `CREATE [OR REPLACE] VIEW schema.name AS SELECT ...` — defines a logical view. Use `OR REPLACE` to redeploy safely.
  2. `GRANT SELECT ON view_name TO role;` — allows a role (user/group) to query the view without touching base tables. This is how you implement least privilege.
  3. `CREATE MATERIALIZED VIEW schema.name AS SELECT ... WITH NO DATA;` (optional `WITH NO DATA` lets you populate later). PostgreSQL physically stores the results.
  4. `REFRESH MATERIALIZED VIEW schema.name;` — reruns the SELECT and updates the stored data.
  5. Consider adding indexes to materialized views with `CREATE INDEX` for faster lookups.
- **Operational tips**:
  * Views always reflect current data; materialized views may lag until refreshed.
  * Refreshes can be `CONCURRENTLY` (PostgreSQL 9.4+) to avoid blocking readers—requires unique index.
  * Track ownership: whoever owns the view controls refresh rights; use a controlled role for consistency.
- **Demo**:
```sql
-- Logical view that filters active customers
CREATE OR REPLACE VIEW reporting.customer_snapshot AS
SELECT id, full_name, email
  FROM customers
 WHERE status = 'active';

-- Give analysts read-only access without exposing base tables
GRANT SELECT ON reporting.customer_snapshot TO analyst;

-- Materialized view for monthly revenue (snapshot of data)
CREATE MATERIALIZED VIEW IF NOT EXISTS reporting.monthly_sales AS
SELECT date_trunc('month', created_at) AS month,
       SUM(order_total) AS revenue
  FROM orders
 GROUP BY 1
WITH DATA;

-- Refresh after loading new orders or on a schedule
REFRESH MATERIALIZED VIEW reporting.monthly_sales;
```

### 3. Constraints
- **What**: Declarative integrity rules enforced by PostgreSQL without additional code. Types include:
  * **PRIMARY KEY** — uniqueness + NOT NULL. Backed by a unique index.
  * **UNIQUE** — prevents duplicate values (can allow NULL unless marked `NOT NULL`).
  * **CHECK** — evaluates a Boolean expression per row.
  * **FOREIGN KEY** — ensures referenced rows exist and manages cascading deletes/updates.
  * **EXCLUDE** — uses GiST or SP-GiST indexes to prevent conflicts on ranges, geometric data, etc.
- **Why constraints first**: The planner understands them, so it can optimise queries and enforce them efficiently. Triggers require procedural code and are harder to validate.
- **Syntax walkthrough**:
  1. Define inline within `CREATE TABLE` or add later with `ALTER TABLE ... ADD CONSTRAINT`.
  2. Give meaningful names (`reservation_times`, `orders_customer_fk`) to aid debugging.
  3. For FOREIGN KEYs specify actions: `ON DELETE CASCADE`, `SET NULL`, or `RESTRICT`.
  4. EXCLUDE constraints require an index type (usually `USING gist`) and operators describing conflicts.
  5. For heavy backfills, add `NOT VALID` to defer checking existing rows, then run `ALTER TABLE ... VALIDATE CONSTRAINT` after cleanup.
- **Operational tips**:
  * Use `DEFERRABLE INITIALLY DEFERRED` when parent/child inserts happen in the same transaction.
  * Monitor constraint violations in logs—PostgreSQL reports the constraint name.
  * Document cascading behaviour; unexpected cascades can delete data silently.
- **Demo**:
```sql
CREATE TABLE reservations (
    id serial PRIMARY KEY,
    room_id int NOT NULL,
    starts_at tstzrange NOT NULL,
    CONSTRAINT reservation_times
      EXCLUDE USING gist (room_id WITH =, starts_at WITH &&)
);

ALTER TABLE reservations
  ADD CONSTRAINT starts_before_ends
  CHECK (lower(starts_at) < upper(starts_at));

ALTER TABLE orders
  ADD CONSTRAINT orders_customer_fk
  FOREIGN KEY (customer_id)
  REFERENCES customers(id)
  ON DELETE RESTRICT;
```

### 4. Triggers
- **What**: Callbacks that fire before/after table events. Use for auditing, denormalised counters, or enforcing multi-row logic.
- **Key pieces**: trigger function (returns `NEW`/`OLD`), trigger definition (timing + event + level).
- **Demo**:
```sql
CREATE OR REPLACE FUNCTION audit.log_order_change()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  INSERT INTO audit.order_history(order_id, payload, changed_at)
  VALUES (NEW.id, row_to_json(NEW), now());
  RETURN NEW;
END;
$$;

CREATE TRIGGER orders_after_update
AFTER UPDATE ON orders
FOR EACH ROW EXECUTE FUNCTION audit.log_order_change();
```

### 5. Transactions & ACID
- **What**: Wrap related statements so they succeed or fail together while preserving isolation.
- **Teaching tip**: Use `BEGIN/COMMIT`, roll back on error, and demonstrate isolation differences.
- **Demo**:
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

### 6. Window Functions
- **What**: Analytical aggregates that operate over partitions without collapsing rows, ideal for rankings and running totals. They differ from GROUP BY because every input row still appears in the result.
- **Syntax quick hits**:
  * `OVER (PARTITION BY ...)` groups rows into partitions.
  * `ORDER BY` inside the window defines the evaluation sequence (required for running totals/rankings).
  * Optional frame clause like `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` controls how many rows contribute to the calculation.
- **Demo**:
```sql
SELECT
    o.id,
    o.customer_id,
    o.order_total,
    ROW_NUMBER() OVER (PARTITION BY o.customer_id ORDER BY o.created_at) AS order_position,
    SUM(o.order_total) OVER (PARTITION BY o.customer_id ORDER BY o.created_at
                             ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_total
FROM orders o;
```

### 7. Extensions (e.g., pgcrypto)
- **What**: Optional modules packaged with PostgreSQL that add extra data types, functions, or utilities. Many Supabase projects already enable common extensions (e.g., `pgcrypto`, `pgjwt`).
- **Teaching tip**: Emphasise that enabling an extension is like installing a plugin at the database level. You only need to enable it once per database.
- **Demo**:
```sql
-- Enable pgcrypto if it is not already installed
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Use a helper from pgcrypto
SELECT gen_random_uuid();

-- List installed extensions
SELECT extname, extversion FROM pg_extension;
```

```sql
-- (Optional) Remove an extension if you no longer need it
DROP EXTENSION IF EXISTS pgcrypto;
```

Remind students that some extensions power Supabase features; removing them may break functionality.

Run each block in a sandbox project before class so you can describe the results with confidence.



---

## Slide Scripts (≈50 minutes total)

### Slide 1 — Week 4 Overview (3 minutes)
**Script**
> “Welcome to Week 4: Advanced SQL and Transaction Management. Up to now we focused on writing queries; today we look at how database administrators extend SQL with functions, views, triggers, and constraints, and how we wrap everything in reliable transactions. These skills are critical for the midterm project because your designs must enforce data integrity and behave safely under concurrent load.”

**Teaching Notes**
- Emphasise that everything in this deck appears in the lab and midterm proposal.
- Remind students the session has four parts: lecture, demo, lab, proposal planning.

### Slide 2 — Agenda (2 minutes)
**Script**
> “Here’s the agenda. We’ll start with advanced SQL building blocks, plug them together with constraints and triggers, examine ACID transactions, and preview the hands-on lab. Keep the midterm proposal in mind—each concept maps to a deliverable in that assignment.”

**Background**
- Clarify the timing: 50-minute lecture, 20-minute live demo, 60-minute lab, 20-minute proposal workshop.

### Slide 3 — Advanced SQL Building Blocks (3 minutes)
**Script**
> “Advanced SQL for administrators covers five pillars: server-side functions, views, triggers, constraints, and transactions. Functions let you package logic; views expose curated data; triggers react to changes; constraints guard data quality; transactions wrap everything so it either succeeds together or fails together. We’ll drill into each pillar next.”

**Background**
- Stress that DBAs prefer declarative features (views/constraints) before procedural ones (triggers) because the optimizer understands them better.

### Slide 4 — User-Defined Functions Overview (5 minutes)
**Script**
> “PostgreSQL can run custom code right in the database. The simplest approach is a SQL function—a single SELECT expression. When we need flow control or variables we switch to PL/pgSQL, the built-in procedural language. Every function declares its volatility—`IMMUTABLE` means it always returns the same output for the same input, `STABLE` allows reads but no writes, and `VOLATILE` can do anything. That metadata helps the query planner cache results correctly. Functions also define security: by default they execute with the caller’s permissions (`SECURITY INVOKER`), but `SECURITY DEFINER` elevates to the owner’s role for maintenance tasks. Use definer functions sparingly and document them.”

**Background**
- Walk through the SQL snippet on the slide: point out the simple SQL function versus the PL/pgSQL trigger-style function.
- Explain parameter modes (`IN`, `OUT`, `VARIADIC`) if asked; emphasise most functions use `IN` parameters.

### Slide 5 — Creating PL/pgSQL Functions (5 minutes)
**Script**
> “This slide shows the full anatomy of a PL/pgSQL function. We name the function, list arguments with types, and declare the return type. Inside the `BEGIN … END` block we can run any SQL, set variables, raise notices, or call other functions. If the function returns data we either `RETURN` a scalar or `RETURN QUERY` for sets. Notice the snippet notifies a channel via `pg_notify`; functions often emit events for application queues. When you write these, think about volatility and permissions, then add unit tests—`pgTAP` is a popular extension for that.”

**Background**
- Mention that the lab demonstrates the structure indirectly via trigger functions; reassure everyone they will practice in the notebook.

### Slide 6 — Views & Materialized Views (4 minutes)
**Script**
> “Views are named SELECT statements. They let us hide join complexity, expose only approved columns, and enforce security by granting access to the view instead of the underlying tables. Materialized views persist the result set to disk—great for heavy analytical queries—but they must be refreshed explicitly. In PostgreSQL you refresh with `REFRESH MATERIALIZED VIEW`. Remember to index materialized views if you filter on them often.”

**Background**
- Highlight the snippet that grants SELECT to an `analyst` role; point out how DBAs layer security.
- Emphasise differences: views are always current; materialized views are snapshots.

### Slide 7 — Designing Robust Views (4 minutes)
**Script**
> “Two pro tips for views: first, use `WITH CHECK OPTION` when the view is updatable. That prevents users from inserting rows that fall outside the view’s filter. Second, set `security_barrier = true` when you rely on views for row-level security—the planner then applies your filters before the client’s predicates, preventing information leaks. Finally, treat your view definitions like code: version them in migrations so teammates know when semantics change.”

**Background**
- If students ask about updatable views, explain that PostgreSQL allows updates if it can map the view back to a single base table.

### Slide 8 — Constraint Toolbox (5 minutes)
**Script**
> “Constraints are declarative—PostgreSQL enforces them with zero extra code. Primary keys and unique constraints guarantee identity. Foreign keys maintain referential integrity. CHECK constraints let us express business rules, like `unit_price >= 0`. Exclusion constraints are advanced: they use GiST indexes to prevent overlaps, perfect for scheduling, geospatial ranges, or time bookings. Whenever you think about writing a trigger to block bad data, pause and ask whether a constraint can do the job.”

**Background**
- Explain domains (reusable type wrappers) as a way to apply shared constraints—e.g., an `email_address` domain with validation.

### Slide 9 — Advanced Constraint Management (3 minutes)
**Script**
> “Sometimes we defer constraint enforcement. Adding `DEFERRABLE INITIALLY DEFERRED` tells PostgreSQL to check at commit time. That’s handy when you insert a parent row and child rows in the same transaction. You can also validate constraints later using `ALTER TABLE … VALIDATE CONSTRAINT`—great for backfilling data without blocking writes. Be explicit about foreign key actions: `ON DELETE CASCADE` removes dependents, `SET NULL` clears references, and `RESTRICT` blocks the delete. Document these choices so downstream teams know what happens.”

**Background**
- Mention the lab’s deferrable constraint example; preview that you’ll show it fail in the demo.

### Slide 10 — Trigger Fundamentals (5 minutes)
**Script**
> “Triggers execute automatically when a table changes. They can fire BEFORE or AFTER an event. BEFORE triggers are ideal for validation or modifying the incoming row; AFTER triggers are used for logging or side effects. Triggers can be row-level—once per row—or statement-level—once per statement. A trigger always invokes a trigger function; for row-level triggers that function must return `NEW` or `OLD`. Remember that triggers run inside the same transaction, so failures roll everything back.”

**Background**
- Reinforce that triggers add hidden complexity; keep them documented and minimal.

### Slide 11 — Trigger Design Patterns (4 minutes)
**Script**
> “Common trigger patterns include audit trails, denormalised counters, data sanitisation, and guard rails. The slide shows a counter trigger that logs inventory consumption and another that raises an exception when an update would create a negative balance. In your projects, prefer triggers when the rule depends on multiple rows or needs historical logging. Otherwise, start with constraints.”

**Background**
- Point out that the teacher notebook includes the audit-style trigger logic.

### Slide 12 — Transactions & ACID (4 minutes)
**Script**
> “Transactions group statements into an all-or-nothing unit. Atomicity means every statement succeeds or none persist—you manage that with `BEGIN`, `COMMIT`, and `ROLLBACK`. Consistency relies on constraints and triggers to keep the database valid. Isolation defines how concurrent transactions interact; PostgreSQL defaults to READ COMMITTED but can run REPEATABLE READ or SERIALIZABLE. Durability ensures committed data survives crashes thanks to the Write-Ahead Log (WAL). The code snippet shows a simple transfer and how to change isolation level.”

**Background**
- Briefly explain MVCC: each transaction sees a snapshot of data; updates create new versions.

### Slide 13 — Isolation Levels & Concurrency (3 minutes)
**Script**
> “Isolation levels trade off throughput and anomaly protection. READ COMMITTED prevents dirty reads. REPEATABLE READ adds protection against non-repeatable reads but can allow write skew. SERIALIZABLE protects against all anomalies by detecting conflicts and forcing retries. When you need to guarantee correctness—think ledger balances—raise the isolation level and possibly lock rows with `SELECT … FOR UPDATE`. Monitor live sessions using `pg_locks` and `pg_stat_activity`.”

**Background**
- Mention the lab isolation experiment: Transaction 1 with REPEATABLE READ, Transaction 2 updating data.

### Slide 14 — Transaction Troubleshooting (4 minutes)
**Script**
> “Real databases see blocking and deadlocks. Watch `pg_stat_activity` for long-running statements and use lock timeouts so clients fail fast instead of hanging forever. Savepoints are mini-checkpoints—wrap risky statements in a savepoint so you can roll back part of a transaction without losing earlier work. When you hit a deadlock, PostgreSQL writes a detailed message to the logs; capture those logs and reconstruct the lock graph to fix the ordering problem.”

**Background**
- Encourage enabling `log_line_prefix` with PID/session info to trace blocking queries.

### Slide 15 — Lab & Midterm Preparation (5 minutes)
**Script**
> “The lab has you build the order summary view, add a deferrable constraint, install the inventory trigger, and experiment with transactions. Submit the notebook output plus SQL scripts. Then start drafting your midterm proposal: Define the dataset, required constraints, triggers, and key transactions. We’ll spend the last 20 minutes brainstorming project scope—bring any dataset ideas you have.”

**Background**
- Remind students the proposal requires integrity rules and transaction scenarios drawn from today’s topics.

Total speaking time: ~50 minutes.

---

## Live Demo (20 minutes)

Use the **student notebook** for the commands and reference the **teacher notebook** for expected outcomes.

1. **Order Summary View (5 min)**
   - Run the view creation cell (`week4_lab_student.ipynb`). Show resulting row(s).
   - Discuss how the view hides joins and calculates totals.

2. **Deferrable Constraint (5 min)**
   - Execute the constraint addition cell, then run the “paid order without items” test. Point out the deferred violation on COMMIT.
   - Explain why this pattern matters during data imports.

3. **Inventory Trigger (5 min)**
   - Run the trigger creation cell, insert a new order item, then query the ledger. Highlight the negative delta.
   - Mention that a trigger is the only way to keep historical change data without separate application code.

4. **Transaction Snapshot (5 min)**
   - In one session run the REPEATABLE READ block; in another shell update the order total. Return to the first session to show the unchanged value.
   - Stress that higher isolation protects against anomalies but may require retries.

---

## Lab Facilitation (60 minutes)

- Encourage pair programming; ensure every student has a Supabase service-role connection string or a local PostgreSQL instance.
- Troubleshooting tips:
  - “`pgcrypto` does not exist” → run `CREATE EXTENSION IF NOT EXISTS pgcrypto;`
  - Permission errors → confirm they’re using the service-role or superuser connection.
  - `pg_dump` not available → let them document steps and run the command on a machine where `pg_dump` is installed later.
- Remind students to capture outputs (screenshots or exported notebook) for submission.
- Suggest they fill out the `proposal_notes` cell while concepts are fresh.

---

## Midterm Proposal Workshop (20 minutes)

Prompt groups with these questions:
1. What dataset will you use and who benefits from it?
2. Which tables require strict constraints (e.g., CHECK, exclusion, deferrable foreign keys)?
3. What triggers or functions will you need for auditing or derived data?
4. Describe one mission-critical transaction flow and the isolation level you’d choose.

Have teams jot answers in the notebook and share highlights. Offer guidance on scope—projects should be complex enough to showcase advanced SQL but manageable within the semester.

---

## After Class

- Review student notebooks for:
  - View definition and output
  - Successful trigger execution (ledger entry)
  - Constraint violation demonstration
  - Transaction rollback results
- Provide midterm proposal feedback before Week 5 lab so students can adjust early.
- Consider a short quiz next week focusing on ACID properties, deferrable constraints, and trigger timing.

---

## Reference Library
- PostgreSQL Functions: https://www.postgresql.org/docs/current/functions.html
- CREATE VIEW / Materialized View: https://www.postgresql.org/docs/current/sql-createview.html
- Constraint Documentation: https://www.postgresql.org/docs/current/ddl-constraints.html
- Trigger Documentation: https://www.postgresql.org/docs/current/plpgsql-trigger.html
- MVCC & Transactions: https://www.postgresql.org/docs/current/mvcc.html
- Lock Monitoring (`pg_stat_activity`, `pg_locks`): https://www.postgresql.org/docs/current/monitoring-stats.html
