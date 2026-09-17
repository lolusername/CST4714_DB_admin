# Lab 2: Repair the Staff Dashboard

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_02/01_relational_sql_review.ipynb)

The dashboard must show every ticket, report current staff workload, and allow
a carefully targeted priority change. You will test those three behaviors.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Keep the Missing Tickets

Use the complete [Metro Support data](data/README.md):
8 users, 12 tickets, and 21 events. If necessary, rerun the
[setup](data/postgres_setup.sql) in your practice database.
You can continue in your Colab copy from Lab 1. To start a new copy, click
**Open in Colab** above and run through **Use the Complete Week 2 Lab Dataset**.
The [downloadable notebook](01_relational_sql_review.ipynb) also
supports local Jupyter.

This query claims to list every ticket:

```sql
SELECT t.ticket_id, t.subject, u.display_name AS assignee
FROM metro_support.tickets AS t
JOIN metro_support.users AS u ON u.user_id = t.assignee_id
ORDER BY t.ticket_id;
```

Run it, find which ticket IDs are absent, and repair the join so all 12 tickets
remain. An unassigned ticket should have a null assignee name. Do not invent a
staff member to fill the blank.

In your SQL file, keep the repaired query and one comment explaining the mistake.

## 2. Count Staff Workload, Including Zero

An active ticket is `new`, `open`, or `in_progress`. For this report, **staff**
means users whose role is `agent` or `supervisor`. There are three staff users:
Priya (201), Noah (202), and Elena (203). Elena has no assigned tickets.

A common table expression (CTE) gives a temporary name to a query result:

```sql
WITH active AS (
    SELECT ticket_id, assignee_id
    FROM metro_support.tickets
    WHERE status IN ('new', 'open', 'in_progress')
)
SELECT ticket_id, assignee_id
FROM active
ORDER BY ticket_id;
```

Keep that CTE. Replace its final SELECT with a query that starts from
`metro_support.users`, left-joins `active`, and returns one row per staff member
with their name and active-ticket count. Use `count(active.ticket_id)`, not
`count(*)`, so a staff member with no matching ticket gets zero.

Check Priya's count by listing her active ticket IDs directly. Explain why
the two unassigned active tickets are not counted as anybody's workload.

## 3. Test a Priority Change Without Keeping It

Staff are considering changing ticket 1006 from medium to high priority.
Use this complete transaction pattern and fill in the two missing statements:

```sql
-- Preview: verify the ID and original priority before changing anything.
SELECT ticket_id, priority
FROM metro_support.tickets WHERE ticket_id = 1006;

BEGIN;
-- Add UPDATE ... SET priority = 'high' ... WHERE ticket_id = 1006
-- and RETURNING ticket_id, priority here.
-- Add a SELECT for ticket 1006 here to see the change.
ROLLBACK;

SELECT ticket_id, priority
FROM metro_support.tickets WHERE ticket_id = 1006;
```

Run the transaction block together in one SQL Editor execution. Its final query
must show `medium` again. In the notebook, use `con.execute(...)` for BEGIN and
ROLLBACK and `con.sql(...).show()` for queries and UPDATE RETURNING.

**Submit:** `week_02_relational_sql_studio.sql` with the repaired dashboard query,
workload query and direct check, and rollback experiment. Keep your explanation
beside the relevant SQL. No separate writing assignment is required.

**If you finish early:** join ticket 1003 to its three events, including actor
names. Explain why three rows are correct for that question. Use `EXCEPT` to
find requester IDs that never appear as assignees. These are ungraded extensions.
