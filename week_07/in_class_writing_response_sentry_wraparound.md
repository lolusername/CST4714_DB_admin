# Week 7 In-Class Writing Response
## PostgreSQL Transaction ID Wraparound and the Sentry Incident

## Activity Type
In-class individual writing response (participation credit)

## Time
20-25 minutes

## Assigned Reading
Read:
- **Transaction ID Wraparound in Postgres** by David Cramer (Sentry)

## Goal
Explain why transaction ID wraparound is a database correctness problem that can also become a service availability problem.

## Background
In July 2015, Sentry experienced a major outage after PostgreSQL entered transaction ID wraparound protection and stopped accepting writes. During recovery, the team had to weigh data preservation against faster service restoration and chose to truncate one large, noncritical table so the system could come back sooner.

## Writing Task
Write a **250-350 word response** explaining why transaction ID wraparound is **not** "just a maintenance issue."

Your response must address all four of the following:

1. **What PostgreSQL is protecting** when it stops accepting writes.
2. **Why vacuuming matters** for long-term correctness, not only performance.
3. **What tradeoff Sentry made** when it truncated a table to recover faster.
4. **One prevention strategy** you think matters most for avoiding a similar incident.

## Planning Questions
You do not need to answer these separately. Use them to shape your response.

- What role do transaction IDs play in PostgreSQL visibility rules?
- Why is wraparound dangerous for MVCC correctness?
- Why would PostgreSQL block writes instead of continuing in an unsafe state?
- Why might a team accept data loss in one table during an emergency?
- What is the difference between a **performance** problem and a **correctness** problem?

## Requirements
- Write in full sentences and organized paragraphs.
- Use at least **three** of these terms correctly:
  - transaction ID (XID)
  - wraparound
  - vacuum or autovacuum
  - visibility
  - write-heavy workload
  - replica
  - truncation
  - invariant
- Make a clear argument, not just a summary.
- Ground your response in the Sentry incident.

## Suggested Structure
- **Paragraph 1:** Explain the technical problem and why PostgreSQL intervenes.
- **Paragraph 2:** Explain why vacuuming matters for database correctness.
- **Paragraph 3:** Evaluate Sentry's recovery tradeoff and name one prevention step.

## What Strong Responses Show
- They distinguish **availability** from **correctness**.
- They connect a low-level PostgreSQL mechanism to a real production outage.
- They explain truncation as a tradeoff, not as an obviously right or wrong decision.
- They propose a realistic prevention step, such as better autovacuum tuning, earlier monitoring, smaller table design, or a clearer operational runbook.

## Submission
- Write your response during class.
- Submit it in the format your instructor specifies.
- Put your name and the date at the top of your response.

## Optional Extension
If you finish early, add 2-3 sentences answering this question:

**If you were the engineer on call, would you have made the same truncation decision? Why or why not?**
