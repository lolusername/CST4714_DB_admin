# Lab 2: Join, Summarize, and Change Safely

## Purpose

Recover the SQL skills most likely to fail silently: joins that change the result
grain, aggregates that count the wrong thing, and updates that affect more rows
than intended.

This is individual work completed in class. Submit one SQL file.

## 1. Join at the Intended Grain

Create `week_02_relational_sql_studio.sql`. For each task, write a comment naming
the result grain before the query.

1. Return every ticket with its requester's name and, when assigned, its agent's
   name. Preserve unassigned tickets. Use clear aliases because `users` appears
   twice.
2. Return the chronological event history for ticket 1003 with the actor's name.
   Explain why three output rows for one ticket are correct.
3. Return each agent and the count of active assigned tickets, including an agent
   with zero. Explain why the active-status condition belongs in the join for this
   question and why `count(ticket_id)` differs from `count(*)`.

## 2. Build a Summary in Named Steps

Use at least one CTE to return one row per category with:

- total tickets;
- unresolved tickets;
- urgent or high-priority tickets; and
- most recent opening timestamp.

Sort by unresolved count and then category. Add a direct filtered count that
verifies one category.

Then use `EXCEPT` to return user IDs that have requested a ticket but have never
been assigned a ticket. State the relational-algebra operation in a comment.

## 3. Practice a Safe Change Without Keeping It

Metro Support considers treating ticket 1006 as high priority.

Write an ordered block that:

1. previews the target row with `SELECT`;
2. begins a transaction;
3. updates only ticket 1006;
4. uses `RETURNING` to show the affected key and new priority;
5. verifies the changed value inside the transaction;
6. rolls back; and
7. proves that the original value returned.

Add one comment explaining what would be different if the change were approved.
Do not replace `ROLLBACK` with `COMMIT` for this lab.

## Submit One Thing

Save the file as `week_02/week_02_relational_sql_studio.sql` and submit it in
Brightspace. It should contain the three join queries, the CTE summary, the set-
difference query, one independent verification, and the rolled-back change.
