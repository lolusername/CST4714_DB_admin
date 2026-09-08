# Teacher Cheat Sheet (Week 5)
## Transactions, Isolation, and Locking — Fast Q&A Mastery

Use this as your quick instructor defense sheet.
It is concise, rigorous, and built for classroom response under pressure.

---

## 1) 30-Second Core Definition Pack

- **Transaction**: a finite state transition unit with atomic commit boundary.
- **Rollback**: revert uncommitted transition.
- **Commit**: persist transition to durable state.
- **Isolation**: constraints on visibility/interleaving among concurrent transitions.
- **Locking**: coordination mechanism to prevent unsafe write overlap.

Teaching line:
"A transaction is not just SQL grouping. It is a correctness boundary."

---

## 2) ACID Without Fluff

- Atomicity: all-or-nothing write set
- Consistency: invariants remain true after commit
- Isolation: concurrent execution does not violate invariant model
- Durability: committed effects survive crash recovery

Math-friendly framing:
- Let state be `S` and invariant set be `I`.
- Transaction `T` is acceptable if after commit: `I(T(S)) = true`.

---

## 3) Isolation Level Quick Decisions

## Read Committed
- default practical baseline
- each statement sees latest committed snapshot at statement start
- good for many CRUD paths

## Repeatable Read
- stable snapshot across transaction
- useful when repeated reads must be internally consistent

## Serializable
- strongest correctness model
- may abort transactions to preserve serializable schedule
- requires safe retry strategy

Decision heuristic:
- choose the lowest isolation that still preserves required business invariants.

---

## 4) Anomalies You Must Explain Clearly

- dirty read
- non-repeatable read
- phantom read
- lost update

High-value sentence:
"Single-query correctness does not imply concurrent correctness."

---

## 5) Locking and Blocking in One Breath

- Locks are normal.
- Blocking is expected when conflicting writes overlap.
- Problem = excessive lock hold duration or bad transaction design.

Symptoms users report:
- "query hangs"
- "save takes forever"
- "timeouts increased suddenly"

---

## 6) Deadlock Plain-English Model

Deadlock = wait cycle.
- T1 waits on T2
- T2 waits on T1
- no progress possible

Postgres response:
- detect cycle
- abort one transaction

Correct operator response:
- retry-safe workflow + ordering fix

---

## 7) Supabase-Relevant Talking Points

- Supabase uses PostgreSQL semantics for transaction/isolation behavior.
- Managed platform does not remove concurrency responsibility.
- Keep transaction windows short in pooled application patterns.
- Use SQL Editor + metadata queries for fast triage evidence.

---

## 8) Must-Know SQL Diagnostic Snippet

```sql
select pid, usename, state, wait_event_type, wait_event, query
from pg_stat_activity
where state <> 'idle';
```

Use during blocking demo to prove wait behavior.

---

## 9) Lab Scope Reminder (Current)

Week 5 lab is intentionally moderate:
- existing tables only
- commit/rollback demo
- two-session blocking demo
- one diagnostics capture
- lightweight deliverables only

Deliverables:
1. brief write-up
2. SQL file
3. screenshots

---

## 10) High-Probability Student Questions

## Q: "Why did IDs skip numbers?"
A: sequence advancement is not rolled back; uniqueness is guaranteed, contiguity is not.

## Q: "Is blocking always bad?"
A: no, blocking is normal coordination; prolonged blocking is operational risk.

## Q: "Why did Serializable fail?"
A: abort is expected under conflict to preserve correctness; retry workflow is required.

## Q: "Why did rollback not change anything?"
A: likely no open explicit transaction or statement already autocommitted.

---

## 11) Instructor Recovery Script if Demo Fails

1. state exact symptom calmly
2. verify two sessions target same row
3. verify Session A still open (uncommitted)
4. rerun diagnostic query
5. continue once evidence appears

This preserves confidence and models professional debugging behavior.

---

## 12) One-Line Closing

"Concurrency safety is the art of preserving invariants under interleaving state transitions."
