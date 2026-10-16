# In-Class Writing Response: When MVCC Goes Wrong

**Week 6. Individual. About 45 minutes in class: 15 minutes of background, 10 minutes of reading, and 20 minutes of writing. Write your response in the Brightspace assignment.**

No SQL, no screenshots, no database work. Review the background, read one short incident report, then write a reflection on what happened and how a team reduces the risk of recurrence.

## Background (15 minutes)

Slides 24 to 32 explain row versions, vacuuming, and wraparound protection using
PostgreSQL 16 as the technical reference. Slide 33 gives the writing prompt.
The 2015 incident used an older version; do not treat its settings as current
recommendations.

## Read (10 minutes)

**Transaction ID Wraparound in Postgres** by David Cramer, Sentry, July 23, 2015.
https://blog.sentry.io/transaction-id-wraparound-in-postgres/

## What happened, in brief

On July 20, 2015, PostgreSQL's wraparound protection stopped new writes at Sentry.
The team identified vacuum settings and capacity that had allowed maintenance
to fall behind on very large tables. It first moved the primary to stronger
hardware and then waited for existing vacuums. Nearly three hours later, a large
table mapping events to their groups remained unfinished. The team truncated
it, removing its rows while retaining the table definition. It accepted that
loss because the table supported non-critical features and replicas held a copy.
Service returned about five minutes later.

Afterward, the team changed vacuum settings and planned to distribute its data.
Read the article's correction as well: the relevant vacuum code in that
historical version capped memory use at 1 GB, so requesting more memory did not
mean all of it was used. The article does not establish the exact administrative
mode used for truncation.

## Four terms to use

- **Transaction ID (XID):** an identifier used with commit status and snapshots to decide row visibility. Its 32-bit space has roughly four billion values; comparisons divide that circle into about two billion past and two billion future IDs.
- **MVCC:** multi-version concurrency control. Readers can use an earlier row version while a writer changes it; this avoids many reader-writer conflicts, not every possible lock.
- **Vacuum / autovacuum:** maintenance that reclaims obsolete versions and freezes old insertions as safely committed in the past. Frozen rows can still be updated or deleted. Autovacuum schedules this work automatically.
- **Wraparound protection:** PostgreSQL refuses new XID allocation before ID comparisons become unsafe. Read-only work can start and transactions already in progress may continue. Ordinary writes needing a new XID fail; recovery uses an administrative procedure.

## Write (20 minutes)

Write a reflection of **250 to 350 words**. It must cover all four points.

1. **What went wrong.** In your own words, what was PostgreSQL protecting when it stopped accepting writes, and why was stopping the right thing for the database to do?
2. **Why it went wrong.** What let the maintenance fall behind at Sentry? Why is vacuuming a correctness problem and not just a performance problem?
3. **The recovery decision.** Sentry chose to empty a table with `TRUNCATE` to get the service back. What made losing those rows an acceptable risk for them? Would you have made the same call? Say why.
4. **How to reduce the risk.** Propose two concrete actions, and explain which matters most. Think about monitoring, autovacuum settings, table size, hardware for maintenance, or a written recovery runbook. Explain how each action helps without promising that it guarantees prevention.

Requirements:

- Use at least **three** of the four terms above correctly.
- Write full sentences in organized paragraphs. Make an argument, not a summary.
- Ground claims about Sentry in the article, including its correction. Use the class background for PostgreSQL concepts. Clearly label your proposed prevention steps as recommendations; do not invent incident details.
- Distinguish **availability** (is the service up) from **correctness** (is the data right). The whole incident is about trading one for the other.

Suggested shape: one paragraph on the problem and why PostgreSQL intervened, one on the recovery tradeoff, one on prevention.

## Submit

Write your response in the Brightspace assignment for this week.

## Why this sits in Week 6

This week is about which actor holds which power. Emptying a table during
recovery requires both the necessary database privilege and authority to accept
the loss. This week's labs keep destructive privileges away from application
roles. The incident gives you a concrete decision for explaining that boundary.
