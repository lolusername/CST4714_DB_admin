# Week 4 Lab Activity
## Schema Management with Existing Supabase Data

## Purpose
This lab practices Week 4 skills at a manageable level:
- create useful views,
- create and refresh one materialized view,
- practice basic constraints,
- verify object state with introspection.

You will work in your existing Supabase project and **use existing tables**.

## Time Target
- 65 to 75 minutes in class
- optional 20 to 30 minutes polish after class

This is intentionally over an hour but not advanced-heavy.

---

## Before You Start
Confirm these tables exist in `public` (from the class dataset):
- `members`
- `facilities`
- `bookings`

If they do not exist, import the class dataset first, then continue.

---

## Step 1: Baseline Verification (10 minutes)
Run these checks and capture one screenshot:
- list tables in `public`
- row counts from `members`, `facilities`, `bookings`

Example:
```sql
select count(*) as members_count from public.members;
select count(*) as facilities_count from public.facilities;
select count(*) as bookings_count from public.bookings;
```

---

## Step 2: Create Two Standard Views (20 minutes)
Create two views using existing data.

### View A: Detailed booking view
Create `public.v_booking_details` with a join across bookings, members, facilities.
Include fields like:
- booking id
- start time
- member name
- facility name
- slots

### View B: Member summary view
Create `public.v_member_booking_summary` with grouped totals per member.
Include fields like:
- member id
- member name
- booking count
- total slots booked

Requirements:
- Use explicit columns (no `SELECT *`)
- Query each view after creating it
- Capture one screenshot per view output

---

## Step 3: Create One Materialized View (15 minutes)
Create `public.mv_facility_usage` to summarize booking activity per facility.

Suggested fields:
- facility id
- facility name
- number of bookings
- total slots

Then run:
```sql
refresh materialized view public.mv_facility_usage;
```

Requirements:
- Query the materialized view
- Capture a screenshot showing refresh + query output
- In your write-up, explain in 1-2 sentences why a materialized view can be useful

---

## Step 4: Basic Constraint Practice (10-15 minutes)
Use a temporary table so you can practice safely without changing core course tables.

Create a temporary table named `constraint_practice` with:
- an id column,
- a code column,
- a status column,
- a check constraint on allowed status values,
- a unique constraint on code.

Then:
1. run one insert that fails (invalid status or duplicate code),
2. run one corrected insert that succeeds,
3. query the table.

Capture:
- one screenshot of the error
- one screenshot of successful result

---

## Step 5: Introspection Check (10 minutes)
Run metadata queries to prove objects exist:
- your two views
- your one materialized view
- constraints on the temp table (or result from your constraint definition step)

Capture one screenshot of introspection output.

---

## Deliverables (Simplified)
Submit only these three items:

1. **Brief write-up** (`week4_brief_writeup.md`, ~200-350 words)
   - What you built
   - One issue you hit
   - How you fixed it

2. **SQL file** (`week4_queries.sql`)
   - SQL/queries used in the lab

3. **Screenshots folder** (`week4_screenshots/`)
   - 6 to 8 screenshots total
   - baseline checks, view outputs, matview refresh/output, constraint fail/success, introspection

No long formal report required.

---

## Grading (100)
- 30 pts: views + materialized view work correctly
- 25 pts: constraint practice includes fail + fix evidence
- 20 pts: introspection evidence is clear
- 15 pts: SQL file is complete and readable
- 10 pts: brief write-up is clear and honest

---

## Fast Help Checklist
If blocked, do this in order:
1. confirm you are in correct Supabase project
2. confirm base tables exist
3. copy exact error text
4. run one small test query to isolate problem
5. apply one fix and re-test

That is the same process used in real support work.
