# Week 5 Full Plan
## Transactions, Isolation, and Locking (PostgreSQL + Supabase)

## Teaching Intent
Week 5 should make students operationally competent with concurrency basics, not just familiar with terminology.

Primary outcome:
- Students can run and explain a rollback/commit demo and a blocking demo using evidence.

## Minute-by-Minute Plan (100 minutes)

## 0-10 min: Warm Start and Context
- recap Week 4 discipline (structure + verification)
- introduce Week 5 problem: concurrent writes and correctness
- define objective: preserve invariants under overlap

## 10-25 min: Transaction Mechanics
- BEGIN/COMMIT/ROLLBACK lifecycle
- autocommit vs explicit transaction
- savepoint concept (quick mention)
- short demo: rollback then commit on one row

## 25-50 min: Isolation Basics
- anomaly vocabulary: dirty/non-repeatable/phantom/lost-update
- Read Committed, Repeatable Read, Serializable in practical terms
- explain retries in Serializable context
- Supabase note: same PostgreSQL semantics

## 50-70 min: Locking Symptoms and Diagnosis
- locking vs blocking vs deadlock
- common user symptom language
- diagnostic query walkthrough (`pg_stat_activity` focused)
- mitigation vs root-cause distinction

## 70-85 min: Supabase Operational Layer
- SQL Editor workflow for diagnostics and evidence
- pooling/timeout practical guidance (beginner-safe level)
- migration timing and lock-risk awareness
- incident response sequence (freeze, diagnose, mitigate, verify)

## 85-95 min: Lab Launch
- explain exact guided steps
- stress existing tables only, no new schema build
- show simplified deliverables
- launch Day 1 and Day 2 sequence expectations
- clarify that Day 2 is incident response focused

## 95-100 min: Reading Response Setup and Close
- assign short two-prompt response
- clarify citation expectation
- final recap of invariants + evidence habit

---

## Instructor Demo Scripts to Run Live

## Demo A: Rollback vs Commit
- run controlled update in transaction
- rollback and verify
- rerun and commit, then verify

## Demo B: Blocking
- Session A holds uncommitted update
- Session B attempts conflicting update and waits
- run diagnostic query during wait
- commit Session A and observe Session B continue

---

## Common Failure Risks During Class
1. Sessions are not targeting same row
2. Session A accidentally committed too early
3. Diagnostics executed after wait ended
4. Wrong Supabase project selected

## Live Recovery Pattern
- pause class
- show exact symptom
- isolate one hypothesis
- run one verification query
- apply one fix
- continue

---

## Assessment Alignment
Lab grading emphasizes:
- correct transactional behavior evidence
- observable blocking evidence
- diagnostic literacy
- concise, reproducible artifacts

Reading response checks:
- conceptual clarity
- practical interpretation
- doc citation use

---

## Success Criteria for Week 5
At class end, a strong student can say:
1. "Rollback removed uncommitted changes."
2. "Commit persisted changes."
3. "Blocking occurred because a conflicting row lock was held."
4. "I identified waiting behavior with diagnostics."
5. "I can explain one safer concurrency habit for future systems."
