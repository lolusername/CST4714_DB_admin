# Week 4 Lab Activity (Open Data Edition)
## Schema Management for Trustworthy Public Data

## Purpose
This lab practices Week 4 skills at a practical level:
- create two reusable views,
- create and refresh one materialized view,
- enforce one or more constraints,
- verify system state with introspection.

The bigger goal is database stewardship. You are not only writing SQL; you are shaping data that other people may rely on for analysis, services, and public decisions.

## Big-Picture Lens
Treat this as an open data workflow. Every step should support:
- clarity (people can understand fields and meaning),
- integrity (rules prevent invalid writes),
- privacy (only necessary detail is exposed),
- reproducibility (another person can verify your process),
- accessibility (outputs are readable and well-labeled).

## Time Target
- 65 to 75 minutes in class
- optional 20 to 30 minutes polish after class

---

## Scenario
Assume your team is preparing facility usage data for internal analytics and possible public reporting.

Your job this week:
1. create stable data interfaces (views),
2. create a performant summary (materialized view),
3. enforce one integrity rule (constraint practice),
4. prove what exists using metadata (introspection),
5. explain tradeoffs in plain language.

---

## Before You Start
Confirm these tables exist in `public`:
- `members`
- `facilities`
- `bookings`

If they do not exist, import the class dataset first.

Also define one sentence for your release intent:
"This dataset helps users answer: _______."

---

## Step 1: Baseline Verification and Context (10 minutes)
Run baseline checks and save one screenshot:
- list tables in `public`,
- row counts for `members`, `facilities`, `bookings`.

Example:
```sql
select count(*) as members_count from public.members;
select count(*) as facilities_count from public.facilities;
select count(*) as bookings_count from public.bookings;
```

Then write 2-3 lines in your notes:
- what the data appears to represent,
- one misuse risk if fields are misunderstood.

---

## Step 2: Create Two Standard Views (20 minutes)
Create two views from existing data.

### View A: Detailed booking interface
Create `public.v_booking_details`.
Join bookings, members, and facilities with explicit columns.

Include fields such as:
- booking id
- start time
- member display field (or anonymized member label)
- facility name
- slots

Design note:
- Avoid `SELECT *`.
- Include only fields needed for the intended question.

### View B: Member-level summary interface
Create `public.v_member_booking_summary`.
Group totals per member.

Include fields such as:
- member id
- member display field
- booking count
- total slots booked

Requirements:
- query each view after creation,
- capture one screenshot per view output,
- add one short comment describing who should use each view and why.

---

## Step 3: Create One Materialized View (15 minutes)
Create `public.mv_facility_usage` to summarize booking activity per facility.

Suggested fields:
- facility id
- facility name
- number of bookings
- total slots

Then refresh:
```sql
refresh materialized view public.mv_facility_usage;
```

Requirements:
- query the materialized view,
- capture a screenshot showing refresh plus output,
- explain in 2-3 sentences:
  - why this view might be faster for reporting,
  - when stale data would be a problem,
  - what refresh policy you would recommend.

---

## Step 4: Constraint Practice as Integrity Policy (10-15 minutes)
Use a temporary table so core course tables stay unchanged.

Create `constraint_practice` with:
- `id`,
- `code`,
- `status`,
- one `CHECK` constraint on valid status values,
- one `UNIQUE` constraint on code.

Then:
1. run one insert that fails,
2. run one corrected insert that succeeds,
3. query the table.

Capture:
- one screenshot of error output,
- one screenshot of successful output.

Write one sentence:
"This constraint protects against _______ by enforcing _______."

---

## Step 5: Introspection and Open Data Readiness (10 minutes)
Run metadata queries that prove objects exist:
- your two views,
- your one materialized view,
- constraints for `constraint_practice`.

Capture one screenshot of introspection output.

Then add a short readiness note:
- field names are interpretable,
- logic is discoverable from SQL,
- sensitive information is minimized for the intended audience,
- validation rules are visible and testable.

---

## Deliverables
Submit these four items:

1. `week4_brief_writeup.md` (250-400 words)
- what you built,
- one issue you hit and how you fixed it,
- one quality or ethics tradeoff you considered.

2. `week4_queries.sql`
- all SQL used in this lab.

3. `week4_screenshots/`
- 6 to 8 screenshots total.

4. `week4_open_data_note.md` (120-220 words)
- intended audience,
- what should and should not be exposed,
- basic freshness and documentation expectations.

---

## Evaluation (100 points)
- 30 pts: views and materialized view work and align with stated purpose
- 20 pts: constraint evidence includes fail case plus corrected case
- 20 pts: introspection and verification evidence is clear
- 15 pts: written explanation is precise and understandable
- 15 pts: open data note shows sound judgment (clarity, privacy, reproducibility)

---

## Inclusion and Professional Language Standard
Write for a mixed audience with different backgrounds.
- use precise terms and define domain language,
- avoid assumptions about user identity or technical history,
- focus on evidence and reasoning, not personal traits,
- prefer neutral labels and transparent definitions.

This is not about "sounding nice." It is about building data work that is usable and trustworthy for real people.

