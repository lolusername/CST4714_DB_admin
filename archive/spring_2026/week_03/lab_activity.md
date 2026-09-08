# Week 3 Lab Activity
## Supabase Admin Tour + Easy Postgres Maintenance Concepts

## Purpose
This lab extends Week 3 to a full class hour without making it heavy or risky.

You will:
- practice navigating the main Supabase admin surfaces,
- run read-only SQL checks to inspect database structure,
- learn a few core maintenance concepts,
- connect those concepts to a real PostgreSQL production incident.

This lab is intentionally observation-first. Most of the work is read-only.

## Time Target
- In class: 60 to 70 minutes
- Optional polish after class: 10 to 15 minutes

---

## Before You Start
Open your Supabase project and the SQL Editor.

If your project already has the course tables, use:
- `members`
- `facilities`
- `bookings`

If not, use any 2 to 3 user-created tables and say which ones you used in your write-up.

---

## Step 1: Baseline Check + Orientation (10 minutes)
Run the following read-only queries:

```sql
select current_database() as database_name, current_schema() as schema_name;

select table_name
from information_schema.tables
where table_schema = 'public'
order by table_name;
```

If you have the class dataset, also run:

```sql
select count(*) as members_count from public.members;
select count(*) as facilities_count from public.facilities;
select count(*) as bookings_count from public.bookings;
```

Answer these quick prompts in 1 to 2 sentences each:
- What database and schema are you working in?
- How do you know you are in the correct project?
- Which table do you think changes most often, and why?

Capture:
- one screenshot showing your baseline query output

---

## Step 2: Guided Supabase Admin Tour (15 minutes)
Visit each area below. You do not need to change settings. Just locate the page and record what it is for.

### A. SQL Editor
Write 1 to 2 sentences:
- Why is it useful to keep saved SQL queries during database administration?

### B. Logs
Write 1 to 2 sentences:
- What kind of problem would make you open logs first?

### C. Reports / Monitoring
Write 1 to 2 sentences:
- What trend or metric would you want to watch over time?

### D. Backups / PITR
Write 2 to 3 sentences:
- Why is "backups enabled" not the same as "recovery proven"?

Capture:
- two screenshots total from any two of the admin areas above

---

## Step 3: Read-Only Introspection Practice (15 minutes)
`Introspection` means asking the database to describe its own structure.

Run these queries:

```sql
select table_name, column_name, data_type
from information_schema.columns
where table_schema = 'public'
order by table_name, ordinal_position;
```

```sql
select schemaname, tablename, indexname, indexdef
from pg_indexes
where schemaname = 'public'
order by tablename, indexname;
```

If your project has the class dataset, also run:

```sql
select table_name
from information_schema.tables
where table_schema = 'public'
and table_name in ('members', 'facilities', 'bookings')
order by table_name;
```

Answer these prompts:
- What is one thing you learned from `information_schema.columns`?
- What is one index you found, and what table is it attached to?
- Why is introspection better than guessing when you are troubleshooting?

Capture:
- one screenshot showing table/column metadata
- one screenshot showing index metadata

---

## Step 4: Mini-Lesson Before the Reading (5 minutes)
You will read a short production incident article next. These are the only new ideas you need before reading it.

- `Transaction ID (XID)`: PostgreSQL gives each transaction an ID so it can track which row versions are visible.
- `MVCC`: PostgreSQL keeps multiple row versions so readers and writers can work at the same time.
- `Autovacuum`: PostgreSQL automatically cleans up old row versions and helps keep very old transaction IDs safe.
- `Wraparound protection`: if old transaction IDs are not handled in time, PostgreSQL may block writes to protect correctness.

You do not need to memorize those terms perfectly. Use them as a reading guide.

---

## Step 5: Read the Sentry Incident Article + Answer Questions (20 minutes)
Read:

- [Transaction ID Wraparound in Postgres (Sentry)](https://blog.sentry.io/transaction-id-wraparound-in-postgres/)

After reading, answer the following in short paragraphs or clear bullet points.

### Article Questions
1. In your own words, what is a transaction ID, and why does PostgreSQL care about it?
2. Why is autovacuum important for correctness, not only for performance?
3. What problem was PostgreSQL trying to prevent when it stopped accepting writes?
4. What tradeoff did Sentry make during recovery, and why might a team accept that tradeoff in an emergency?
5. What is one prevention or monitoring step that could reduce the chance of a similar outage?

### Easy Concept Check
Answer each in 1 sentence:
- What is the difference between a performance problem and a correctness problem?
- Why is a large write-heavy table operationally risky if maintenance falls behind?
- Why is "we have backups" not enough by itself during an incident?

---

## Step 6: Wrap-Up Reflection (5 minutes)
Write 4 to 6 bullets:
- one Supabase admin area you would check first during a problem
- one thing you learned about database maintenance this week
- one thing the Sentry article made you take more seriously
- one habit you want to use in your own database work

---

## Deliverables (Simplified)
Submit only:

1. `week3_lab_brief_writeup.md`
   - include your Step 1, Step 2, Step 3, Step 5, and Step 6 answers
   - target length: about 350 to 600 words total

2. `week3_lab_queries.sql`
   - include the SQL you ran for baseline and introspection

3. `week3_lab_screenshots/`
   - 4 to 6 screenshots total
   - baseline output, admin tour evidence, column metadata, index metadata

No long formal report is required.

---

## Grading (100)
- 20 pts: baseline and project-orientation evidence is complete
- 25 pts: admin tour observations are clear and accurate
- 20 pts: introspection queries and explanations are correct
- 25 pts: article questions show real understanding
- 10 pts: submission is organized and readable

---

## Fast Help Checklist
If you get stuck, do this in order:
1. confirm you are in the correct Supabase project
2. copy the exact query or page name you are using
3. check whether the problem is SQL, navigation, or understanding
4. test one small read-only query
5. ask for help with the exact symptom, not a general guess

That is a real database operations habit: identify the symptom, verify the environment, and narrow the problem.
