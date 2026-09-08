# Week 7 In-Class Activity
## PostgreSQL Transaction ID Wraparound: Mini Lab + Reading Response

## Activity Type
In-class hybrid activity:
1. short inspection lab
2. short individual writing response

## Time
- Part A lab: 15-20 minutes
- Part B writing response: 15-20 minutes
- Total: 30-40 minutes

## Goal
Connect PostgreSQL maintenance concepts to a real outage by:
- inspecting safe wraparound-related metadata in PostgreSQL,
- reading the Sentry incident article,
- explaining why wraparound is a correctness problem, not just a performance problem.

## Assigned Reading
Read:
- **Transaction ID Wraparound in Postgres** by David Cramer (Sentry)
- URL: [https://blog.sentry.io/transaction-id-wraparound-in-postgres/](https://blog.sentry.io/transaction-id-wraparound-in-postgres/)

## Background
In July 2015, Sentry experienced a major outage after PostgreSQL entered transaction ID wraparound protection and stopped accepting writes. During recovery, the team had to weigh data preservation against faster service restoration and chose to truncate one large, noncritical table so the system could come back sooner.

The point of this activity is to connect:
- MVCC row/version visibility,
- vacuum and autovacuum maintenance,
- transaction ID age,
- and operational recovery decisions.

---

## Part A: Mini Lab (Safe Inspection Only)

## Setup
Use your existing PostgreSQL environment from class.

Preferred:
- your existing Supabase project

Alternative:
- local Docker PostgreSQL from class

This activity is **read-only**.
Do **not** create or delete objects for this exercise.

---

## Step 1: Confirm Context
Run:

```sql
select current_database() as db_name, txid_current() as current_xid;
```

Capture:
- Screenshot 1 showing the current database and current transaction ID

---

## Step 2: Check Database-Level Transaction Age
Run:

```sql
select
  datname,
  age(datfrozenxid) as xid_age
from pg_database
where datname = current_database();
```

Purpose:
- see that PostgreSQL tracks transaction ID age at the database level

Capture:
- Screenshot 2 showing `xid_age`

---

## Step 3: Inspect Table Health Signals
Run:

```sql
select
  relname,
  n_live_tup,
  n_dead_tup,
  last_autovacuum,
  last_autoanalyze
from pg_stat_user_tables
where schemaname = 'public'
order by n_dead_tup desc, relname
limit 10;
```

Purpose:
- inspect dead tuples and whether autovacuum/autoanalyze has run

Capture:
- Screenshot 3 showing table health metadata

---

## Step 4: Inspect Table XID Age
Run:

```sql
select
  n.nspname as schema_name,
  c.relname as table_name,
  age(c.relfrozenxid) as table_xid_age
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where c.relkind = 'r'
  and n.nspname = 'public'
order by table_xid_age desc, table_name
limit 10;
```

Purpose:
- see that transaction ID age can also be inspected at the table level

Capture:
- Screenshot 4 showing the highest `table_xid_age` values you can see

---

## Step 5: Quick Observation Notes
Write 4-6 bullets based on your query results:
- what `txid_current()` showed you,
- what `age(datfrozenxid)` suggests,
- what dead tuples/autovacuum columns suggest,
- which table had the highest visible XID age,
- one reason this metadata matters operationally.

You do not need a long explanation here.
These bullets are your bridge into Part B.

---

## Part B: Reading Response

## Writing Task
Write a **250-350 word response** explaining why transaction ID wraparound is **not** "just a maintenance issue."

Your response must address all four of the following:

1. **What PostgreSQL is protecting** when it stops accepting writes.
2. **Why vacuuming matters** for long-term correctness, not only performance.
3. **What tradeoff Sentry made** when it truncated a table to recover faster.
4. **One prevention strategy** you think matters most for avoiding a similar incident.

You should also connect your explanation to **at least one thing you observed in Part A**.

---

## Planning Questions
You do not need to answer these separately. Use them to shape your response.

- What role do transaction IDs play in PostgreSQL visibility rules?
- Why is wraparound dangerous for MVCC correctness?
- Why would PostgreSQL block writes instead of continuing in an unsafe state?
- What did your metadata queries show about how PostgreSQL tracks age and cleanup?
- Why might a team accept data loss in one table during an emergency?
- What is the difference between a **performance** problem and a **correctness** problem?

---

## Requirements
- Write in full sentences and organized paragraphs.
- Use at least **three** of these terms correctly:
  - transaction ID (XID)
  - wraparound
  - vacuum or autovacuum
  - visibility
  - dead tuples
  - truncation
  - invariant
  - correctness
- Make a clear argument, not just a summary.
- Ground your response in the Sentry incident.
- Refer to at least one observation from your Part A lab queries.

---

## Suggested Structure
- **Paragraph 1:** Explain the technical problem and why PostgreSQL intervenes.
- **Paragraph 2:** Explain why vacuuming matters for database correctness and connect to one metadata result.
- **Paragraph 3:** Evaluate Sentry's recovery tradeoff and name one prevention step.

---

## Deliverables (Simplified)
Submit:

1. `week7_wraparound_response.md`
   - your 250-350 word response
   - your 4-6 observation bullets at the top or bottom

2. `week7_wraparound_queries.sql`
   - the SQL you ran in Part A

3. `week7_wraparound_screenshots/`
   - 4 screenshots total

No long formal report required.

---

## What Strong Responses Show
- They distinguish **availability** from **correctness**.
- They connect a low-level PostgreSQL mechanism to a real production outage.
- They use the Part A inspection results as evidence, not filler.
- They explain truncation as a tradeoff, not as an obviously right or wrong decision.
- They propose a realistic prevention step, such as better autovacuum tuning, earlier monitoring, smaller table design, or a clearer operational runbook.

---

## Optional Extension
If you finish early, add 2-3 sentences answering this question:

**If you were the engineer on call, would you have made the same truncation decision? Why or why not?**
