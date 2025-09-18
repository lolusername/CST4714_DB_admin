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
- **What**: Callbacks PostgreSQL executes automatically when a table event occurs. Use them for auditing, denormalised counters, enforcing complex business rules, or rejecting invalid changes.
- **Trigger anatomy**:
  * **Trigger function** — written in PL/pgSQL (or another language) and returns `NEW` (for INSERT/UPDATE) or `OLD` (for DELETE). It contains the logic you want to run.
  * **Trigger definition** — `CREATE TRIGGER ... BEFORE|AFTER event ON table FOR EACH ROW|STATEMENT EXECUTE FUNCTION ...`. Timing determines whether you can modify the incoming row (`BEFORE`) or react after the change (`AFTER`). Level decides whether the trigger fires once per row or once per statement.
  * **Transition tables** (PostgreSQL 10+): `REFERENCING NEW TABLE AS ...` lets you access all affected rows inside the trigger for statement-level triggers.
- **Best practices**:
  * Keep trigger functions short and deterministic; document side effects.
  * Avoid heavy queries inside triggers—they run inside the original transaction and can block it.
  * Log actions with `RAISE NOTICE` while testing; remove noisy logging in production.
  * Version-control trigger definitions alongside migrations so changes are reviewable.
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
- **What**: Wrap related statements so they succeed or fail together while preserving isolation. ACID stands for Atomicity, Consistency, Isolation, Durability.
- **How they work**:
  * `BEGIN;` starts a transaction block. PostgreSQL keeps your changes private until you `COMMIT;`.
  * `COMMIT;` makes the changes durable. If anything fails before commit, issue `ROLLBACK;` to undo everything executed after `BEGIN;`.
  * Savepoints (`SAVEPOINT name;` / `ROLLBACK TO name;`) let you partially undo work inside a longer transaction.
- **Isolation levels** control how concurrent transactions see each other:
  * `READ COMMITTED` (default) — each statement sees committed data at its start.
  * `REPEATABLE READ` — the whole transaction sees a consistent snapshot; repeated reads return the same rows even if others commit changes.
  * `SERIALIZABLE` — prevents all anomalies by detecting conflicts and forcing retries.
- **Session vs transaction settings**:
  * `SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL ...;` changes the default isolation level for every transaction you open in that connection from that point onward. Think of it as telling PostgreSQL, “until I disconnect, assume every new `BEGIN;` should run at REPEATABLE READ (or whatever level you chose).” Use this when you want to compare a set of behaviours with the stronger level applied automatically.
  * `SET TRANSACTION ISOLATION LEVEL ...;` must run *inside* an open transaction (after `BEGIN;`). It overrides the isolation level for that single transaction only, then reverts to the session default after `COMMIT;` or `ROLLBACK;`. This is perfect for one-off experiments where you do not want to change the ongoing default.
  * Demo flow: open two shells. In shell A, leave the default isolation in place. In shell B, run `SET SESSION CHARACTERISTICS AS TRANSACTION ISOLATION LEVEL REPEATABLE READ;`, then show how a long-running `SELECT` in shell B keeps seeing the same snapshot while shell A continues to update rows. Repeat the demo with `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;` inside a single transaction so students see a serialization failure without altering the rest of the session.
- **Demo**:
```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Raise default isolation level for subsequent transactions in this session
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
> “Welcome to Week 4: Advanced SQL and Transaction Management. Think of today as moving from basic querying into administration skills. When I say *Advanced SQL*, I mean the server-side tools—functions, views, triggers, constraints—that let us enforce data rules in the database itself. *Transaction management* is about grouping related statements so they succeed or fail together, which is critical for reliability. These topics feed directly into your midterm: every project must show how it protects data quality and handles concurrent users.”

**Key terms explained**
- *Advanced SQL*: features beyond SELECT/INSERT/UPDATE that live inside the database engine.
- *Database administrator (DBA)*: the role responsible for configuration, security, backups, and performance.
- *Transaction*: a unit of work that is either fully applied or fully rolled back.

**Teaching Notes**
- Highlight that lecture, demo, lab, and proposal workshop are tightly linked; students should carry notes from each segment into their midterm plan.

### Slide 2 — Agenda (3 minutes)
**Script**
> “Here’s how we’ll spend the session. First, we’ll review the building blocks—functions, views, triggers, constraints, transactions—so you know what tools exist. Then we’ll combine them to see how integrity is enforced. After that we’ll dig into ACID and isolation levels so you understand how PostgreSQL keeps transactions safe. Once the concepts are clear, I’ll run a live demo showing each feature in action. You’ll practice the same steps in the lab, and we’ll end by outlining your midterm proposal.”

**Key terms explained**
- *ACID*: stands for Atomicity, Consistency, Isolation, Durability—the four guarantees of reliable transactions.
- *Isolation level*: rule that controls how simultaneous transactions can see each other’s changes.

**Background**
- Reiterate timing: lecture (~50 min), demo (20 min), lab (60 min), proposal workshop (20 min). Encourage students to jot questions for each block.

### Slide 3 — Advanced SQL Building Blocks (4 minutes)
**Script**
> “Administrators lean on five pillars: functions, views, constraints, triggers, and transactions. Functions package reusable logic right next to the data. Views give users a clean window onto the tables without exposing raw structures. Constraints describe the rules data must obey. Triggers let us react automatically when data changes. Transactions glue everything together so related statements succeed or fail as a unit. We will study each pillar, see examples, and discuss when to choose one tool over another.”

**Key terms explained**
- *Declarative vs procedural*: declarative features (views, constraints) describe what must be true; procedural features (functions, triggers) run step-by-step instructions.
- *Optimizer*: the part of PostgreSQL that decides how to run queries; it understands declarative rules, so favor those when possible.

### Slide 4 — User-Defined Functions Overview (6 minutes)
**Script**
> “Functions are mini-programs stored in the database. A simple SQL function can be one SELECT statement—great for transforming values. PL/pgSQL functions give you variables, loops, and conditionals. PostgreSQL asks every function to label its *volatility*: `IMMUTABLE` means the output never changes for the same inputs and lets the planner cache results; `STABLE` allows reads but not writes and stays consistent within a statement; `VOLATILE` is the default when outputs may change each call, like `now()`. We also pick the security context: `SECURITY INVOKER` runs with the caller’s privileges, while `SECURITY DEFINER` runs with the owner’s privileges—useful for maintenance jobs but potentially dangerous if you elevate rights.”

**Examples to mention**
- Data-cleanup function that uppercases names.
- Reporting helper that calculates tax or discounts.

**Key terms explained**
- *Volatility*: hint to the planner about how predictable the function is.
- *Security context*: whose permissions apply during execution.
- *Parameter modes*: `IN` (default input), `OUT` (returned via parameters), `VARIADIC` (variably sized argument list).

### Slide 5 — Creating PL/pgSQL Functions (6 minutes)
**Script**
> “This slide breaks down the anatomy of a PL/pgSQL function. We give it a name, schema, and parameter list; we specify the return type. Inside `BEGIN … END` we can run any SQL, declare variables, raise notices, and even call other functions. To send data back we use `RETURN` for single values or `RETURN QUERY` for result sets. Notice the example fires a `pg_notify` message—functions often integrate with other systems. Whenever you write a function, decide on volatility and security, and think about tests. The pgTAP extension is a popular way to unit test functions.”

**Key terms explained**
- *`pg_notify`*: PostgreSQL messaging feature that lets you send notifications to listeners.
- *`RAISE NOTICE`*: command used for debug output from PL/pgSQL.
- *Unit testing functions*: ensures behavior stays correct during schema changes.

### Slide 6 — Views & Materialized Views (5 minutes)
**Script**
> “Views are saved SELECT statements. They shield users from complex joins and let you centralize business logic. Because a view only stores the SQL text, each query pulls current data. Materialized views go a step further: they store the query results on disk, which speeds up heavy analytics but means you must refresh them periodically. In PostgreSQL you refresh with `REFRESH MATERIALIZED VIEW`, and you can even do it `CONCURRENTLY` if you add a unique index so readers aren’t blocked. Granting SELECT on a view is safer than granting access to base tables because you decide exactly which columns and rows are exposed.”

**Key terms explained**
- *Encapsulation*: hiding complexity behind a simpler interface (the view).
- *Least privilege*: giving users only the permissions they need.
- *Refresh*: rerunning the materialized view query to update stored data.

### Slide 7 — Designing Robust Views (4 minutes)
**Script**
> “When views are updatable, use `WITH CHECK OPTION` to stop users from inserting rows that violate the view’s filter—otherwise the row would disappear after insert. Set `security_barrier = true` for security-sensitive views; it forces PostgreSQL to apply the view’s filter before client-supplied filters to prevent data leaks. Treat views like source code: keep them in migrations, review changes, and document dependencies. If a view becomes slow, analyze its query plan with `EXPLAIN` just like you would for tables.”

**Key terms explained**
- *Updatable view*: one where PostgreSQL can translate inserts/updates back to the base table.
- *`EXPLAIN`*: command that shows how PostgreSQL plans to execute a query.

### Slide 8 — Constraint Toolbox (6 minutes)
**Script**
> “Constraints are declarative guarantees. A PRIMARY KEY enforces uniqueness and not-null in one step; UNIQUE constraints ensure no duplicate values; CHECK constraints evaluate Boolean expressions like `quantity > 0`; FOREIGN KEYS ensure relationships remain valid; EXCLUDE constraints use GiST indexes to block overlapping ranges—perfect for scheduling or geospatial data. Because constraints are declarative, the optimizer can use them to simplify queries and they run faster than trigger-based checks. Before writing procedural code, ask if a constraint can solve the problem.”

**Examples**
- CHECK preventing negative account balances.
- FOREIGN KEY ensuring every order references an existing customer.
- EXCLUDE to stop room double-bookings.

### Slide 9 — Advanced Constraint Management (4 minutes)
**Script**
> “Real systems need flexibility. `DEFERRABLE INITIALLY DEFERRED` lets you postpone checks until `COMMIT` so you can insert a parent row and its children in one transaction. `ALTER TABLE … VALIDATE CONSTRAINT` lets you add a constraint as `NOT VALID`—meaning new rows must comply, but existing rows are checked later without blocking writes. For foreign keys, choose the right action: `CASCADE` deletes dependent rows, `SET NULL` clears the reference, `RESTRICT` blocks the delete. Document these behaviors so teammates aren’t surprised.”

**Key terms explained**
- *Deferrable*: enforcement can be delayed until transaction end.
- *Backfill*: populating historical data after the fact.

### Slide 10 — Trigger Fundamentals (5 minutes)
**Script**
> “Triggers are automatic reactions. `BEFORE` triggers let you modify or reject a change before it hits the table—great for validation or derived columns. `AFTER` triggers run once the change is saved, perfect for logging. Decide whether the trigger fires for each row or once per statement. The trigger function must return `NEW` (the incoming row) or `OLD` (the existing row) depending on the event. Triggers execute inside the user’s transaction, so if they fail, the entire statement fails. Keep them fast and documented.”

**Key terms explained**
- *Row-level vs statement-level*: whether the trigger fires per affected row or once per SQL statement.
- *`NEW`/`OLD` records*: special variables representing the row data before/after the change.

### Slide 11 — Trigger Design Patterns (5 minutes)
**Script**
> “Common patterns include audit trails that copy changes into history tables, denormalised counters that maintain summary totals, data sanitisation that formats values, and guard rails that raise exceptions when business rules are broken. Use triggers when the rule depends on multiple rows or you need a history of changes. If a declarative constraint can do the job, prefer the constraint; it’s simpler for the optimizer and easier to test.”

**Examples**
- Audit trigger logging before/after values for compliance.
- Inventory trigger subtracting quantities from a stock table.
- Validation trigger rejecting updates that would set `balance < 0`.

### Slide 12 — Transactions & ACID (6 minutes)
**Script**
> “Transactions guarantee ACID. **Atomicity**: either all statements succeed or none do—managed with `BEGIN`, `COMMIT`, and `ROLLBACK`. **Consistency**: constraints and triggers keep the data valid before and after the transaction. **Isolation**: concurrent transactions act as if they ran in sequence, depending on the isolation level. **Durability**: once committed, changes survive crashes because PostgreSQL writes them to the Write-Ahead Log (WAL). Use savepoints for complex workflows so you can roll back part of a transaction without losing earlier work.”

**Key terms explained**
- *Write-Ahead Log (WAL)*: sequential log PostgreSQL uses to guarantee durability and for recovery.
- *Savepoint*: named checkpoint in a transaction for partial rollback.

### Slide 13 — Isolation Levels & Concurrency (5 minutes)
**Script**
> “Isolation decides which anomalies are allowed. `READ COMMITTED` (default) prevents dirty reads but allows non-repeatable reads and phantom rows. `REPEATABLE READ` adds protection against non-repeatable reads—once you read a row, you see the same snapshot—but phantoms can still appear. `SERIALIZABLE` simulates running transactions one at a time; PostgreSQL detects conflicts and forces retries. Explain anomalies with quick examples so students understand why isolation matters. Show how `SELECT … FOR UPDATE` locks rows to avoid lost updates.”

**Key terms explained**
- *Dirty read*: seeing uncommitted data from another transaction.
- *Non-repeatable read*: reading the same row twice and getting different results because another transaction committed in between.
- *Phantom read*: new rows matching a condition appear between two scans.

### Slide 14 — Transaction Troubleshooting (4 minutes)
**Script**
> “Production systems hit blocking and deadlocks. Monitor `pg_stat_activity` to spot long-running queries and `pg_locks` to see who is waiting. Use `SET lock_timeout` or `statement_timeout` so clients fail gracefully instead of hanging forever. Savepoints help isolate risky statements. When PostgreSQL reports a deadlock, grab the log entry—it lists the queries and lock types involved so you can fix the order of operations. Encourage students to practice reproducing a deadlock in the lab to understand the error message.”

**Key terms explained**
- *Deadlock*: two transactions waiting on each other’s locks, so neither can proceed.
- *Timeout*: automatic cancel after a specified waiting period.

### Slide 15 — Lab & Midterm Preparation (6 minutes)
**Script**
> “The lab walks through real administration tasks: create a reporting view, enforce a deferrable constraint, wire up an inventory trigger, and experiment with transactions and isolation levels. Capture screenshots or notebook cells showing each success—they’re required for the lab submission. After the lab, begin your midterm proposal: define the dataset, list constraints you’ll enforce, identify triggers or functions you’ll need, and describe at least one critical transaction flow. We’ll use the proposal workshop to stress-test your ideas.”

**Key terms explained**
- *Deferrable constraint*: constraint evaluated at commit time.
- *Proposal scope*: the boundaries of the midterm project—dataset, users, features, risks.

Total speaking time: ~50 minutes (with richer explanations).

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

## Day 2 Lab — Indexed Analytics & Automation (75 minutes)

Day 2 is meant to feel friendly: keep the dataset, but slow the pace and show each new SQL feature in tiny steps. Everything still lives in the `week4_day2` schema so students can reset safely.

### Before Class (10 minutes)
- Run `psql -f week_4/week4_day2_lab.sql` (or execute the file in Supabase) to reset the schema. The script rebuilds only the `week4_day2` objects, so it will not touch `public`.
- Skim the key tables:
  - `week4_day2.students` — roster of 60 students.
  - `week4_day2.course_offerings` — which course runs in which term.
  - `week4_day2.enrollments` — mix of completed/enrolled/dropped rows used for indexing and analytics.
  - `week4_day2.term_credit_summary`, `week4_day2.enrollment_audit` — start empty for the trigger exercise.
- Take 2–3 screenshots (before/after `EXPLAIN`) so you have real numbers to reference while teaching.

### Agenda & Talking Points

**1. Index warm-up (15 minutes)**
- Prompt: “Let’s prove an index matters before we talk theory.”
- Baseline plan:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS)
  SELECT *
  FROM week4_day2.enrollments
  WHERE offering_id = 18 AND status = 'completed';
  ```
  It should show a sequential scan and ~thousands of heap fetches.
- Create the index together:
  ```sql
  CREATE INDEX CONCURRENTLY IF NOT EXISTS week4_day2_enrollments_offering_status_idx
      ON week4_day2.enrollments (offering_id, status);
  ANALYZE week4_day2.enrollments;
  ```
- Rerun the `EXPLAIN`. Point out “Bitmap/Index Scan”, lower timings, and the drop in buffer hits. Optional: show `pg_stat_user_indexes` to prove the index was used.

**2. Window functions in three passes (20 minutes)**
- Goal: students see that a window function is “GROUP BY plus extra columns” rather than magic.
- Pass 1 — regular aggregate:
  ```sql
  SELECT s.full_name,
         o.term,
         SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
         SUM(e.credits_earned) AS term_credits
  FROM week4_day2.enrollments e
  JOIN week4_day2.course_offerings o ON o.offering_id = e.offering_id
  JOIN week4_day2.students s        ON s.student_id = e.student_id
  WHERE e.status = 'completed'
  GROUP BY s.full_name, o.term
  ORDER BY o.term, term_gpa DESC;
  ```
  Describe this as “scoreboard by term.”
- Pass 2 — add a simple ranking window:
  ```sql
  WITH per_term AS (
      -- paste the query from Pass 1
  )
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY term ORDER BY term_gpa DESC) AS term_rank
  FROM per_term
  ORDER BY term, term_rank;
  ```
  Explain: “PARTITION BY term means restart the numbering each term.”
- Pass 3 — add a running total for credits:
  ```sql
  WITH per_term AS (
      -- same as before
  )
  SELECT full_name,
         term,
         term_gpa,
         term_rank,
         SUM(term_credits)
             OVER (PARTITION BY full_name ORDER BY term
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS credits_so_far
  FROM per_term
  ORDER BY term, term_rank;
  ```
  Emphasise that the window clause just tells PostgreSQL “add the current student’s earlier rows.”
- Show a sample output so everyone can picture it:
  ```text
   full_name        | term         | term_gpa | term_rank | credits_so_far
  ------------------+--------------+----------+-----------+----------------
   Andrea Flores    | 2023-Fall    | 3.67     |         1 |             12
   Brian Kim        | 2023-Fall    | 3.20     |         2 |              9
   ...
  ```

**3. Turn it into an easy-to-share view (10 minutes)**
- Reuse the Pass 3 query inside a view so advisors do not need to retype the logic.
  ```sql
  CREATE OR REPLACE VIEW week4_day2.vw_student_term_progress AS
  <pass 3 query>;
  ```
- Keep the conversation simple: “Views = saved SELECT.”
- Optional: grant `SELECT` on the view to a read-only role.

**4. Trigger automation without the math headache (15 minutes)**
- Message: “Every time a grade changes, refresh the summary table.”
- Provide this easier trigger function that re-summarises rather than doing manual arithmetic:
  ```sql
  CREATE OR REPLACE FUNCTION week4_day2.update_term_summary()
  RETURNS trigger
  LANGUAGE plpgsql AS $$
  DECLARE
      v_term text;
      v_attempted int;
      v_earned    int;
      v_quality   numeric(10,2);
  BEGIN
      SELECT term INTO v_term
      FROM week4_day2.course_offerings
      WHERE offering_id = NEW.offering_id;

      SELECT COALESCE(SUM(e.credits_attempted), 0),
             COALESCE(SUM(e.credits_earned), 0),
             COALESCE(SUM(COALESCE(e.grade_points, 0) * e.credits_attempted), 0)
      INTO  v_attempted, v_earned, v_quality
      FROM week4_day2.enrollments e
      JOIN week4_day2.course_offerings o ON o.offering_id = e.offering_id
      WHERE e.student_id = NEW.student_id
        AND o.term = v_term
        AND e.status = 'completed';

      INSERT INTO week4_day2.term_credit_summary(student_id, term, credits_attempted,
             credits_earned, quality_points, gpa, last_recalc)
      VALUES (NEW.student_id, v_term, v_attempted, v_earned, v_quality,
              CASE WHEN v_attempted > 0 THEN v_quality / v_attempted ELSE NULL END,
              now())
      ON CONFLICT (student_id, term) DO UPDATE
          SET credits_attempted = EXCLUDED.credits_attempted,
              credits_earned    = EXCLUDED.credits_earned,
              quality_points    = EXCLUDED.quality_points,
              gpa               = EXCLUDED.gpa,
              last_recalc       = now();

      RETURN NEW;
  END;
  $$;
  ```
- Wire it up:
  ```sql
  CREATE TRIGGER enrollment_finalize_summary
  AFTER INSERT OR UPDATE OF status, grade_points, credits_earned
  ON week4_day2.enrollments
  FOR EACH ROW EXECUTE FUNCTION week4_day2.update_term_summary();
  ```
- Demo: flip enrollment 25 to `completed`, then show the summary table.

**5. Advisor helper function (10 minutes)**
- Purpose: give advisors a quick list of students who need attention.
- Sample definition (reuses the view + summary table):
  ```sql
  CREATE OR REPLACE FUNCTION week4_day2.fn_flag_at_risk(
      p_term text,
      p_min_gpa numeric,
      p_min_credits int)
  RETURNS TABLE (
      student_id uuid,
      full_name text,
      term text,
      term_gpa numeric,
      credits_so_far int)
  LANGUAGE sql AS $$
      SELECT v.student_id,
             v.full_name,
             v.term,
             v.term_gpa,
             t.credits_earned AS credits_so_far
      FROM week4_day2.vw_student_term_progress v
      JOIN week4_day2.term_credit_summary t
        ON t.student_id = v.student_id AND t.term = v.term
      WHERE v.term = p_term
        AND (v.term_gpa < p_min_gpa OR t.credits_earned < p_min_credits)
      ORDER BY v.term_gpa;
  $$;
  ```
- Call it live: `SELECT * FROM week4_day2.fn_flag_at_risk('2024-Spring', 2.5, 9);`
- Talk through result columns so advisors hear plain-language benefits.

### Deliverables & Exit Tickets
- `EXPLAIN (ANALYZE, BUFFERS)` screenshot before/after the index.
- Query result showing window rankings.
- Result from `SELECT * FROM week4_day2.term_credit_summary ORDER BY student_id, term LIMIT 5;`.
- Output from `fn_flag_at_risk` with their chosen thresholds.
- One takeaway posted in the LMS discussion: “Indexing mattered most when ______.”

### Common Sticking Points
- Remind students to `ANALYZE week4_day2.enrollments;` if the planner still prefers a sequential scan after creating the index.
- `permission denied for schema week4_day2` → grant usage: `GRANT USAGE ON SCHEMA week4_day2 TO <role>;`
- If the trigger double-counts credits, check whether they filtered to `NEW.status = 'completed'` before adding earned credits.
- Encourage multi-session testing (psql tabs) so they can see trigger-side effects live.

---

## Day 2 Slide Guide — Instructor Notes & Script (≈55 minutes)

Use this guide alongside `Week4_Day2_Indexed_Analytics.pptx`. Each slide section below includes:

- **Talking points for the instructor** — what to review before class and how it ties back to the lab dataset (`week4_day2_lab.sql`).
- **Suggested demo cues** — when to tab over to `psql` or show result screenshots.
- **Word-for-word script** — read verbatim or adapt slightly for your style. Emphasis words are intentional; practice them beforehand.

### Instructor Prep Checklist (20 minutes)
- Rerun `psql -f week_4/week4_day2_lab.sql` so your environment mirrors the students'.
- Capture baseline vs indexed `EXPLAIN` outputs to quote real timings (expect ~4–6x improvement on offering 18).
- Test the trigger path by updating enrollment 25 so you can confirm the delta in `term_credit_summary` and optional `enrollment_audit` log.
- Execute `SELECT * FROM week4_day2.fn_flag_at_risk('2024-Spring', 2.50, 9);` to reference a concrete result set while teaching the function.
- Skim the view definition and be ready to explain why `security_barrier` is helpful even in a lab.

### Slide-by-Slide Script

**Slide 1 — Week 4 Day 2: Indexed Analytics & Automation (2 minutes)**
- *Context*: Frame the day as a continuation of advanced SQL with a performance and automation focus.
- *Script*:
  > “Welcome back to Week 4, Day 2. Today we’re staying inside the database to build indexed analytics and lightweight automation. We’ll benchmark a real query, layer on window logic, and use triggers and functions to keep our reporting data clean. Everything we touch comes from the `week4_day2` schema you reset with the new lab script.”

**Slide 2 — Agenda (2 minutes)**
- *Context*: Outline the flow; reinforce that the deck mirrors the lab steps.
- *Script*:
  > “Here’s the map for the next hour: we’ll reset the dataset, run the indexing benchmark, craft analytic windows, harden those results with views, automate credit summaries with triggers, then package advisor insights inside a reusable function. We’ll close with deliverables and next steps so you know exactly what to capture for the lab submission.”

**Slide 3 — Resetting the Lab Dataset (3 minutes)**
- *Demo cue*: Show the command (either in terminal history or the SQL editor).
- *Script*:
  > “Before class, and whenever results look off, rerun `psql -f week_4/week4_day2_lab.sql`. The script drops and recreates only the `week4_day2` schema, so it’s safe to run repeatedly. It seeds about a thousand enrollments across four terms, which guarantees we see meaningful differences once the index is in place.”

**Slide 4 — Schema Quick Reference (3 minutes)**
- *Context*: Emphasise relationships; have the ER mental map ready.
- *Script*:
  > “The schema mirrors a registrar slice. `students`, `faculty`, and `courses` are reference tables. `course_offerings` ties a course, term, and instructor together. `enrollments` logs each student–offering pair along with status and grades. The `term_credit_summary` and `enrollment_audit` tables start empty so our triggers can populate them during the lab.”

**Slide 5 — Table Definitions In Context (3 minutes)**
- *Context*: Highlight unique constraints.
- *Script*:
  > “Each table has constraints that mimic production rules. `students` enforces a reasonable credit goal range. `enrollments` uses the `enforce_completed_grade` check so a completed record can’t have a missing grade. Foreign keys ensure an enrollment can’t exist without the related student or offering. These guardrails keep our analytics trustworthy without writing extra code.”

**Slide 6 — Synthetic Data Highlights (2 minutes)**
- *Context*: Mention data variety for realistic plans.
- *Script*:
  > “The data generator leans on `generate_series` with looping arrays to create sixty unique students. Offerings cover four consecutive terms with rotating instructors. We randomise status by using modular arithmetic so every cohort has enrollments that are completed, dropped, or still in progress. Completed rows carry grade points and earned credits so the GPA math is meaningful.”

**Slide 7 — Baseline Enrollment Query (4 minutes)**
- *Demo cue*: Run the baseline `EXPLAIN` live. Point out seq scan.
- *Script*:
  > “Let’s feel the pain before we fix it. Run `EXPLAIN (ANALYZE, BUFFERS)` on the query filtering offering 18 for completed enrollments. The planner chooses a sequential scan because the table lacks a useful index. Notice the high buffer counts and the timing—capture this screenshot now; it’s the ‘before’ artifact you’ll submit.”

**Slide 8 — Creating the Covering Index (3 minutes)**
- *Demo cue*: Execute the CREATE INDEX statement, explain CONCURRENTLY.
- *Script*:
  > “Now craft the covering index: `CREATE INDEX CONCURRENTLY IF NOT EXISTS week4_day2_enrollments_offering_status_idx ON week4_day2.enrollments (offering_id, status);`. We use `CONCURRENTLY` to mirror real production practice—writers keep running while the index builds. Follow it with `ANALYZE week4_day2.enrollments;` so the planner picks up the new statistics immediately.”

**Slide 9 — Comparing Plans After Indexing (4 minutes)**
- *Demo cue*: Rerun `EXPLAIN`, show `pg_stat_user_indexes`.
- *Script*:
  > “Rerun the same `EXPLAIN`. You should see an index or bitmap scan with dramatically lower timing and buffer usage. Grab that screenshot—it’s your ‘after’ evidence. Then run `SELECT relname, idx_scan FROM pg_stat_user_indexes WHERE schemaname = 'week4_day2' AND relname = 'week4_day2_enrollments_offering_status_idx';` to watch the usage counter climb. Remind students that indexing trades faster reads for slightly slower writes, so we measure both sides.”

**Slide 10 — Maintaining Healthy Statistics (2 minutes)**
- *Context*: Reinforce manual ANALYZE in lab.
- *Script*:
  > “Labs don’t always have autovacuum, so don’t be shy about running `ANALYZE`. If you’re curious what the planner knows, query `pg_stats` for the enrollments table. Document your indexing decision in the midterm proposal—operators will want to know what you tuned and why.”

**Slide 11 — Window Function Primer (3 minutes)**
- *Context*: Show that a window is just “aggregate plus extra column.”
- *Script*:
  > “If regular `GROUP BY` is a scoreboard, a window function is that same scoreboard with bonus columns. We’ll build it in passes: first the plain totals, then add a row number, then add a running credit total. Because we keep the original rows, we can give advisors the full story instead of one line per student.”

**Slide 12 — Window Function: Three Passes (5 minutes)**
- *Demo cue*: Type each pass live, pausing between them.
- *Script*:
  > “Pass one: plain aggregate per student and term. Pass two: wrap it in a CTE and add `ROW_NUMBER()` with `PARTITION BY term` so the numbering restarts each term. Pass three: add `SUM(term_credits) OVER (PARTITION BY full_name ORDER BY term)`—that one sentence literally means ‘for this student, add up the earlier rows.’ Stop after each pass so students can read the output and see how little the SQL changes.”

**Slide 13 — Save the Query as a View (3 minutes)**
- *Context*: Keep the terminology friendly.
- *Script*:
  > “Views are saved SELECT statements. Drop the Pass Three query inside `CREATE OR REPLACE VIEW week4_day2.vw_student_term_progress AS ...`. Now anyone can `SELECT * FROM week4_day2.vw_student_term_progress WHERE term = '2024-Spring';` without touching the complex SQL. Mention that comments and simple grants help future you remember why the view exists.”

**Slide 14 — Sharing the View Safely (2 minutes)**
- *Context*: Quick reminder about permissions.
- *Script*:
  > “Grant access on the view, not the base tables: `GRANT SELECT ON week4_day2.vw_student_term_progress TO reporting_role;`. If you later need stricter security, you can add `security_barrier = true`, but for the lab the main idea is ‘one clean doorway for analysts.’”

**Slide 15 — Trigger Automation Blueprint (3 minutes)**
- *Context*: Explain the simplified trigger story.
- *Script*:
  > “Every time a grade changes we want the summary table refreshed. We’ll attach an `AFTER INSERT OR UPDATE` trigger to enrollments. The trigger just says ‘call our helper function.’ Because it runs inside the same transaction, if the summary update fails the grade change also rolls back—automatic consistency.”

**Slide 16 — update_term_summary() Walkthrough (5 minutes)**
- *Demo cue*: Highlight the SELECT ... INTO block and the upsert.
- *Script*:
  > “The function stays friendly: find the term, aggregate the student’s completed enrollments for that term, then upsert one row into `term_credit_summary`. No hand math, no complicated offsets. Point out the guard: if the student has zero attempted credits we store NULL GPA, otherwise quality points divided by attempted credits.”

**Slide 17 — Optional Audit Trail (2 minutes)**
- *Context*: Still optional, but relate it to storytelling.
- *Script*:
  > “If you like receipts, drop a tiny `INSERT` into `week4_day2.enrollment_audit` right before `RETURN NEW;`. The table captures before/after status and grades so you can answer ‘who changed what?’ later. Totally optional, but nice to mention for ambitious students.”

**Slide 18 — Advisor Function Goals (2 minutes)**
- *Context*: Connect back to the view.
- *Script*:
  > “The advisor function is just packaging. We point it at the view, layer a WHERE clause for GPA or credit thresholds, and give advisors a neat list. Because the heavy logic lives in the view, the function body stays five lines long.”

**Slide 19 — fn_flag_at_risk() Example (4 minutes)**
- *Demo cue*: Run the function and read the columns aloud.
- *Script*:
  > “Here’s the SQL: it selects from the view, joins to the summary table for credits, and filters by the parameters. Run `SELECT * FROM week4_day2.fn_flag_at_risk('2024-Spring', 2.5, 9);`, then literally read the results like a checklist: student name, term GPA, credits so far. That helps everyone see why we built the earlier pieces.”

**Slide 20 — Lab Deliverables & Evidence (2 minutes)**
- *Context*: Reinforce documentation requirement.
- *Script*:
  > “To complete the lab, capture before-and-after `EXPLAIN` screenshots, show the ranking query results, dump the first five rows of `term_credit_summary`, and include the advisor function output. Finish with the reflection prompt: ‘Indexing mattered most when …’. These artifacts prove you exercised every feature we built today.”

**Slide 21 — Wrap-Up & Next Steps (2 minutes)**
- *Context*: Encourage midterm prep.
- *Script*:
  > “Before you leave, double-check that your trigger math looks right and the audit table is logging what you expect. Document your new index, view, trigger, and function so you can reuse the patterns in the midterm proposal. If you have stretch ideas—like extending the advisor function—bring them to tomorrow’s workshop.”

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
