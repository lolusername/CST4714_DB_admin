# Midterm Review Packet — CST4714 Database Administration

## How to Use This Packet
1. Complete the six-question diagnostic check without notes (10–12 minutes).
2. Review the concept refreshers tied to each question set.
3. Work through the SQL labs using the club database from `week_3/review.sql`.
4. Tackle the schema redesign case study and compare with peers.
5. Finish with the personal study checklist before submitting your exit ticket.

---

## 1. Diagnostic Check (Closed Notes)
1. **Architecture:** In PostgreSQL, what roles do the background writer and checkpointer processes play in durability?
2. **Cloud DBA:** List two advantages and two trade-offs of running PostgreSQL on a managed service like AWS RDS or Supabase.
3. **SQL Functions:** Given a function that returns `SETOF` records, what are two ways to invoke it in a query? Provide sample syntax.
4. **Transactions:** Describe the difference between `READ COMMITTED` and `REPEATABLE READ` isolation levels in PostgreSQL.
5. **Normalization:** A table stores `order_id`, `customer_id`, `customer_name`, `product_id`, `product_name`, `quantity`. Identify two anomalies and the NF violated.
6. **Performance:** What information can you gather from `EXPLAIN (ANALYZE, BUFFERS)` that is not present in `EXPLAIN` alone?

*Answer key provided in Section 5 — complete all questions before checking.*

---

## 2. Concept Refreshers
### 2.1 PostgreSQL Architecture & Durability
- **Write-Ahead Log (WAL):** Every change hits WAL files before heap tables, guaranteeing crash recovery.
- **Background Writer:** Smooths checkpoint activity by writing dirty buffers in the background to avoid spikes.
- **Checkpointer:** Triggers checkpoints at configured intervals to flush dirty pages, ensuring WAL can be recycled.
- **Autovacuum:** Prevents table bloat and keeps visibility maps accurate for index-only scans.

**Quick Recall:** Sketch the data flow of an UPDATE from client connection → shared buffers → WAL → heap.

### 2.2 Cloud DBA Responsibilities
- Managed services remove OS patching but require parameter tuning (e.g., connection limits, storage autoscaling).
- Consider SLA tiers, maintenance windows, backup retention, failover behavior, and cost ceilings.
- Cloud monitoring: integrate cloud-native alerts plus custom checks on query latency and connection health.

### 2.3 Advanced SQL & PL/pgSQL
- **Invoking set-returning functions:** `SELECT * FROM my_func(args);` or `SELECT col1 FROM my_func(args) AS alias(col1, col2);`
- **Trigger tips:** Always include exception logging; ensure `RETURN NEW;` vs `RETURN OLD;` matches timing.
- **Window functions:** Use partitions for cohort analyses; combine with common table expressions (CTEs) for clarity.

### 2.4 Transactions & Isolation
- `READ COMMITTED`: Each statement sees committed data as of execution start; can observe changes made by other transactions mid-session.
- `REPEATABLE READ`: Ensures a consistent snapshot for the entire transaction; avoids non-repeatable reads but still susceptible to phantom reads.
- **Tools:** `SET TRANSACTION ISOLATION LEVEL`, `LOCK TABLE`, `pg_locks`, `pg_stat_activity`.

### 2.5 Normalization & Design Trade-Offs
- **1NF:** No repeating groups; atomic values.
- **2NF:** Non-key attributes fully depend on the entire primary key.
- **3NF/Boyce-Codd:** No transitive dependencies; every determinant is a candidate key.
- Track when denormalization is intentional (reporting performance, snapshot tables).

### 2.6 Performance Analytics
- `EXPLAIN (ANALYZE, BUFFERS)` surfaces actual run time, loop counts, and shared/local buffer hits.
- Compare estimated vs actual row counts to flag stale statistics or missing indexes.
- `auto_explain` extension can log expensive queries for later tuning.

---

## 3. SQL Practice Lab
**Setup:** Run `week_3/review.sql` to provision the `cd` schema (club database).

- Optional warm-up: revisit the [three-table join practice](https://pgexercises.com/questions/joins/threejoin2.html) from pgexercises before starting the prompts below.

> Work inside explicit transactions where noted. Include screenshots or copied query output in your notes.

### Prompt 1 — Membership Utilization
```sql
-- Return each member's total booked slots and the percentage
-- relative to the most active member.
```

### Prompt 2 — Peak Facility Demand (Window Functions)
```sql
-- For each facility, list the top three busiest days by total slots booked.
-- Include ties, and display cumulative slots using a window frame.
```

### Prompt 3 — Trigger Diagnostic
```sql
-- Write a BEFORE INSERT trigger on bookings that prevents members
-- from booking more than 10 slots per day. Log violations to a table
-- named booking_audit(bookid, memid, booking_date, message).
```

### Prompt 4 — Transaction Isolation Experiment
1. Session A: Begin a `REPEATABLE READ` transaction and query the number of rows in `bookings`.
2. Session B: Insert a new booking and commit.
3. Session A: Re-run the count and observe the result. Explain why it behaves that way.

### Stretch Goal — Maintenance Planning
```sql
-- Propose an index or materialized view that improves a frequent query of your choice.
-- Write the DDL and justify the impact using EXPLAIN ANALYZE output notes.
```

---

## 4. Schema Redesign Case
You are reviewing the following table used for subscription renewals:

| Column | Sample Value | Notes |
| --- | --- | --- |
| subscription_id | 5012 | Primary key |
| customer_id | 183 | FK to customers table |
| customer_email | pat@example.com | Redundant with customers table |
| product_code | DBA-PLUS | Subscription SKU |
| product_category | Training | Derived from product table |
| renewal_date | 2024-11-01 | Next planned renewal |
| renewal_status | pending | Enum stored as text |
| last_invoice_total | 299.00 | Value copied from invoices table |

### Tasks
1. Identify at least **three anomalies** that could occur with this design.
2. Propose a revised schema (tables + key fields) that satisfies 3NF.
3. Document one place where controlled denormalization may still add value, and explain the monitoring required to keep it accurate.

---

## 5. Answer Key & Self-Check
| Diagnostic Item | Expected Response Highlights |
| --- | --- |
| 1 | Background writer flushes dirty buffers steadily; checkpointer creates consistent on-disk checkpoints to guarantee WAL reuse/durability. |
| 2 | Pros: automated backups, reduced patching; Cons: limited superuser access, cost scaling surprises, maintenance windows outside control. |
| 3 | `SELECT * FROM func(args);` or `SELECT alias.col FROM func(args) AS alias(col1, col2);` |
| 4 | `READ COMMITTED` sees latest committed data per statement; `REPEATABLE READ` pins snapshot for transaction, preventing non-repeatable reads. |
| 5 | Update anomaly (customer name mismatch); insertion anomaly (new product without order); violates 2NF/3NF due to mixed dependencies. |
| 6 | Provides actual execution time, loops, and buffer usage to contrast with planner estimates. |

**If you missed two or more questions:** revisit the corresponding Concept Refresher and schedule time with a classmate or TA.

---

## 6. Personal Study Checklist
- [ ] Re-watch or skim Week 3 architecture and cloud lectures; note any terminology gaps.
- [ ] Rerun `week_4/week4_advanced_sql_lab_student.ipynb` prompts focusing on functions and transactions.
- [ ] Review normalization notes and redo at least one schema critique from Week 5’s lab.
- [ ] Complete all SQL practice prompts above and record findings from `EXPLAIN ANALYZE`.
- [ ] Update midterm project proposal with current ERD, normalization summary, and open risks.
- [ ] Schedule at least one group study session or office hour before the exam.

---

*Prepared for Week 7 midterm prep — last revised 2025-02-14.* 
