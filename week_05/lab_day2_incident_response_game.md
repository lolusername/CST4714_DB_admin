# Week 5 Lab Day 2
## Concurrency Incident Drill (Supabase SQL Editor)

## Purpose
Day 2 is a coherent incident workflow:
1. instructor worked example,
2. guided team practice,
3. short independent challenge.

This lab teaches students to:
- reproduce row-lock blocking on purpose,
- diagnose wait state using metadata,
- choose a safe mitigation,
- verify and clean final data state,
- report evidence clearly.

## Time Target
- Full class: 90-100 minutes

## Team Format
Teams of 3:
- Driver A: Session A (first transaction and lock holder)
- Driver B: Session B (conflicting transaction)
- Observer/Reporter: diagnostics, timeline, screenshots

Rotate roles after Phase 1.

## Safety Rules
1. Use existing tables only (`members`, `facilities`, `bookings`).
2. No new schema creation.
3. Every claim requires SQL evidence.
4. Do not terminate sessions unless instructor asks.
5. Clean all temporary text changes before submission.

---

## Setup (10 minutes)
Open three SQL Editor tabs:
- Tab 1: Session A
- Tab 2: Session B
- Tab 3: Observer

Pick one target member row:
```sql
select memid, surname, firstname
from public.members
order by memid
limit 10;
```

Record:
- `TARGET_MEMID`
- original `surname`
- original `firstname`

Capture Screenshot 1: baseline row.

---

## Phase 1: Instructor Worked Example (15 minutes)
Follow instructor exactly once before team independence.

### Session A
```sql
begin;
update public.members
set surname = surname || '_A1'
where memid = <TARGET_MEMID>;
-- keep transaction open
```

### Session B
```sql
begin;
update public.members
set surname = surname || '_B1'
where memid = <TARGET_MEMID>;
-- should wait
```

### Observer (run while Session B waits)
```sql
select
  now() as observed_at,
  pid,
  usename,
  state,
  wait_event_type,
  wait_event,
  pg_blocking_pids(pid) as blocking_pids,
  query
from pg_stat_activity
where datname = current_database()
  and state <> 'idle'
order by pid;
```

### Close worked example
```sql
-- Session A
rollback;

-- Session B (after it unblocks)
rollback;
```

Capture:
- Screenshot 2: Session B waiting
- Screenshot 3: diagnostics output

---

## Phase 2: Guided Team Run (35 minutes)
Now repeat the incident as a team with role rotation.

### Step A: Recreate blocking
Session A:
```sql
begin;
update public.members
set firstname = firstname || '_LOCKA'
where memid = <TARGET_MEMID>;
-- keep open
```

Session B:
```sql
begin;
update public.members
set firstname = firstname || '_LOCKB'
where memid = <TARGET_MEMID>;
-- expect wait
```

### Step B: Diagnose before mitigation
Observer:
```sql
select
  now() as observed_at,
  pid,
  xact_start,
  state,
  wait_event_type,
  wait_event,
  pg_blocking_pids(pid) as blocking_pids,
  query
from pg_stat_activity
where datname = current_database()
  and state <> 'idle'
order by xact_start nulls last;
```

### Step C: Choose mitigation
Session A chooses one path:
- `commit;` keep Session A change
- `rollback;` discard Session A change

Session B (after unblocked):
```sql
rollback;
```

### Step D: Verify
```sql
select memid, firstname, surname
from public.members
where memid = <TARGET_MEMID>;
```

Capture:
- Screenshot 4: blocked state
- Screenshot 5: diagnostics with `blocking_pids`
- Screenshot 6: final verification state

---

## Phase 3: Independent Mini-Challenge (20 minutes)
Use a new row (`CHALLENGE_MEMID`) and run without instructor prompts.

Requirements:
1. Reproduce blocking once.
2. Capture diagnostics while wait is active.
3. Mitigate with justified commit/rollback decision.
4. Verify final state.
5. Clean temporary suffixes.

Cleanup pattern:
```sql
update public.members
set surname = '<ORIGINAL_SURNAME>', firstname = '<ORIGINAL_FIRSTNAME>'
where memid = <CHALLENGE_MEMID>;
```

Capture Screenshot 7: cleaned final state.

---

## Debrief (10-15 minutes)
Write 5-7 bullets:
1. Symptom observed by "app users"
2. Root cause in one sentence
3. Evidence query that proved the blocker
4. Mitigation chosen and why
5. One prevention habit for future systems

---

## Deliverables (Simplified)
Submit only:
1. `week5_day2_brief_writeup.md` (250-400 words)
2. `week5_day2_queries.sql` (all SQL used)
3. `week5_day2_screenshots/` (7-10 screenshots)

## Grading (100)
- 30: correct incident reproduction
- 30: diagnostics quality and evidence clarity
- 20: mitigation + verification correctness
- 20: write-up clarity and prevention insight
