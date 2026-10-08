# In-Class Writing Response: When MVCC Goes Wrong

**Week 6. Individual. About 30 minutes. Write your response in the Brightspace assignment.**

No SQL, no screenshots, no database work. Read one short incident report, then write a reflection on what happened and how a team prevents it.

## Read (10 minutes)

**Transaction ID Wraparound in Postgres** by David Cramer, Sentry, July 23, 2015.
https://blog.sentry.io/transaction-id-wraparound-in-postgres/

## What happened, in brief

On Monday, July 20, 2015, the hosted Sentry service was down for most of the US working day. Nobody attacked it and no disk failed. PostgreSQL stopped accepting writes on purpose.

Here is the background you need. Last week you learned that PostgreSQL keeps several versions of a row so readers and writers do not block each other (MVCC). Every transaction that changes data gets a transaction ID, and PostgreSQL uses those IDs to decide which row version each transaction can see. The IDs come from a counter with about two billion usable values. Routine maintenance, called vacuuming, retires old versions and marks old rows as permanently visible so the counter can safely keep going. If that maintenance falls far enough behind, the counter runs out of room. At that point PostgreSQL refuses new writes rather than reuse IDs, because reuse would make deleted rows reappear, updates revert, and constraints break. This is called transaction ID wraparound protection. It is PostgreSQL choosing to be unavailable instead of wrong.

Sentry's database was very write-heavy with some enormous tables, and the team had tuned automatic vacuuming to run less aggressively. The protection kicked in. The database went read-only, the event queue started backing up, and the team let the running vacuums finish while moving the primary to bigger hardware. After several hours one giant table still had not finished. Rather than wait an unknown number of hours more, they truncated that table, a mapping of events to their groups that only served non-critical features and was also present on replicas. Five minutes later the service was back.

Afterward the team gave vacuuming far more memory, CPU, and workers, made it run much more often with less delay, and planned to split the data into several databases so no single table could get that large again.

## Four terms to use

- **Transaction ID (XID):** the number PostgreSQL assigns to a transaction so it can decide which row versions that transaction sees.
- **MVCC:** multi-version concurrency control. PostgreSQL keeps old row versions so readers and writers do not block each other.
- **Vacuum / autovacuum:** the maintenance that removes dead row versions and keeps old transaction IDs safe. Autovacuum runs it automatically.
- **Wraparound protection:** PostgreSQL stops accepting writes when the ID counter is nearly exhausted, to prevent data corruption.

## Write (20 minutes)

Write a reflection of **250 to 350 words**. It must cover all four points.

1. **What went wrong.** In your own words, what was PostgreSQL protecting when it stopped accepting writes, and why was stopping the right thing for the database to do?
2. **Why it went wrong.** What let the maintenance fall behind at Sentry? Why is vacuuming a correctness problem and not just a performance problem?
3. **The recovery decision.** Sentry chose to delete an entire table to get the service back in minutes instead of hours. What made that an acceptable risk for them? Would you have made the same call? Say why.
4. **How to prevent it.** Name two concrete things a team should do so this never happens to them, and say which one matters most. Think about monitoring, autovacuum settings, table size, hardware for maintenance, or a written runbook for the day it happens anyway.

Requirements:

- Use at least **three** of the four terms above correctly.
- Write full sentences in organized paragraphs. Make an argument, not a summary.
- Ground every claim in the article. Do not invent details.
- Distinguish **availability** (is the service up) from **correctness** (is the data right). The whole incident is about trading one for the other.

Suggested shape: one paragraph on the problem and why PostgreSQL intervened, one on the recovery tradeoff, one on prevention.

## Submit

Write your response in the Brightspace assignment for this week.

## Why this sits in Week 6

This week is about which actor holds which power. The engineers who recovered Sentry were using the most powerful credentials in the system to drop a table under pressure. That is exactly the kind of power this week's labs keep away from application roles, and exactly the kind of decision a database administrator has to be ready to make and explain.
