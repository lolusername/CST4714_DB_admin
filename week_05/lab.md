# Week 5 Lab Activity
## Transactions, Isolation, and Locking (Supabase, existing tables)

## Purpose
Practice concurrency basics safely on existing class data.

You will:
- run explicit transaction blocks,
- compare rollback vs commit outcomes,
- observe blocking with two sessions,
- run diagnostics during wait state,
- submit lightweight evidence.

## Time Target
- In class: 65-75 minutes
- Optional polish: 20-30 minutes

---

## Required Setup
Use your existing Supabase project and existing `public` tables:
- `members`
- `facilities`
- `bookings`

Open two SQL sessions/tabs (Session A and Session B).

---

## Step 1: Baseline Check (10 min)
Run row counts and capture one screenshot:
```sql
select count(*) as members_count from public.members;
select count(*) as facilities_count from public.facilities;
select count(*) as bookings_count from public.bookings;
```

---

## Step 2: Commit vs Rollback Demo (20 min)
Pick one safe target row (example: one `members` row).

### Part A: Rollback
1. `BEGIN;`
2. Update one field on the target row.
3. Query row and observe changed value.
4. `ROLLBACK;`
5. Query row again and confirm original value restored.

### Part B: Commit
1. `BEGIN;`
2. Update the same row again.
3. `COMMIT;`
4. Query row and confirm persisted value.

Capture screenshots:
- rollback result
- commit result

---


## Step 3: Short Analysis (5-10 min)
Write 4-6 bullet points:
- what rollback proved,
- what commit proved,
- what blocking looked like,
- what query you used to diagnose,
- one prevention habit for future systems.

---

## Grading (100)
- 30 pts: rollback/commit demonstration is correct and evidenced
- 30 pts: blocking demo is correct and evidenced
- 20 pts: diagnostics evidence is clear
- 10 pts: SQL file is complete and organized
- 10 pts: brief write-up is clear and accurate

---


