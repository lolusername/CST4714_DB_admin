# Lab 1: Find the Requests That Need Attention

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_02/01_relational_sql_review.ipynb)

Metro Support needs a reliable list of unfinished work. You will write three
queries that help staff find urgent and unassigned requests, then investigate a
plausible query that returns the wrong answer.

Work individually in class. Submit one SQL file in Brightspace.

## 1. Open the Data and Read One Worked Query

In a personal course database, open Supabase's **SQL Editor**, create a query,
paste the [Metro Support setup](data/postgres_setup.sql),
and run it. It resets only the `metro_support` practice schema. Save any earlier
SQL before resetting it. The result must show **8 users, 12 tickets, 21 events**.

For the Colab path, click **Open in Colab** above, save a copy in Drive, and run
the cells through **Use the Complete Week 2 Lab Dataset**. That section loads
the full lab data. Use `con.sql("""YOUR QUERY""").show()` to run a SELECT.
You can also [download the notebook](01_relational_sql_review.ipynb)
for local Jupyter.

An active ticket has status `new`, `open`, or `in_progress`. This worked query
returns one row per active ticket:

```sql
SELECT ticket_id, subject, priority, status
FROM metro_support.tickets
WHERE status IN ('new', 'open', 'in_progress')
ORDER BY ticket_id;
```

Expect **7 rows**, including unassigned tickets 1004 and 1009. The schema prefix
`metro_support.` matters: a new editor tab may use a different search path.

## 2. Write Three Useful Queries

Create `week_02_sql_review.sql`. Use the worked query as a starting point.

1. Return active tickets whose priority is **high or urgent**, newest first.
   Show the ticket ID, subject, priority, and opening time.
2. Return **all unassigned tickets**, showing the ID, subject, and status.
   Use `assignee_id IS NULL`.
3. Return active tickets requested by residents in the **Harbor** neighborhood.
   Show each ticket ID and the requester's name.

For Query 3, match `tickets.requester_id` to `users.user_id`. Here is how a join
names both sides:

```sql
SELECT t.ticket_id, u.display_name
FROM metro_support.tickets AS t
JOIN metro_support.users AS u ON u.user_id = t.requester_id
WHERE t.ticket_id = 1001;
```

This example returns ticket 1001 and Maya Chen. Adapt its filter to answer the
neighborhood question. Write one sentence in a SQL comment explaining what one
row in Query 3 represents.

## 3. Check a Suspicious Result

A colleague writes this condition to find unassigned work:

```sql
SELECT ticket_id
FROM metro_support.tickets
WHERE assignee_id = NULL;
```

Run it and compare it with your Query 2. Explain why its empty result does not
prove that every ticket is assigned.

Check Query 3 by reading the linked `users.csv` and `tickets.csv` in the
[dataset folder](data/README.md). Identify one ticket that
belongs in the result and one that does not, with the reason for each.

**Submit:** your three queries and the short explanation as
`week_02_sql_review.sql`. Put explanations in `-- SQL comments`. There is no
separate report, screenshot, or GitHub submission.

**If you finish early:** list the distinct categories with active tickets. Then
calculate ticket age relative to the latest opening time in the dataset. Define
whether you mean fractional days or calendar dates before choosing the expression.
This extension is optional and ungraded.
