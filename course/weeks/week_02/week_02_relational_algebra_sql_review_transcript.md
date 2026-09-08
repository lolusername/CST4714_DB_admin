# Week 2: Relational Algebra and Major SQL Review - Spoken Transcript

## Slide 1

This week we will use SQL to answer questions about a small service desk. SQL stands for Structured Query Language. It lets us describe the data we want and the changes we want the database to make. We do not have to specify the exact physical steps the database should use to find each row. That separation is one reason SQL remains useful across different database systems.

We will begin with finding requests that need attention. Then we will repair a staff report that loses unassigned requests, count work for staff members who may have no assignments, and test a priority change without keeping it. These are ordinary database tasks with consequences for the people who use the reports.

The complete course dataset contains eight users, twelve tickets, and twenty-one ticket events. A ticket is a request for help. An event records something that happened to a ticket. The notebook begins with a smaller demonstration dataset, so its early counts are different. Before either lab, we will use the section labeled complete Week 2 lab dataset, or the PostgreSQL setup file linked in the weekly guide.

We will rebuild the syntax as we go. Chapter 2 explains the same ideas with additional examples. Each lab has one SQL-file submission. Short explanations belong beside the relevant query as SQL comments, which begin with two hyphens.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/tutorial-sql.html

## Slide 2

Suppose a staff member asks for high-priority requests that are still active. Before choosing SQL clauses, we need to decide exactly what those words mean. In this dataset, priority is a stored value such as low, medium, high, or urgent. High and urgent are different values. A request can have high priority and already be resolved. A condition on priority alone would include that finished work.

For this week, active means that status is new, open, or in_progress. We need both conditions: priority must be high, and status must belong to the active set. The output should have one row for each matching request. Including the ticket identifier helps us recognize which request each row describes.

This definition also gives us a way to check the answer. We can read the small source table and identify the matching ticket IDs independently. If the query returns a resolved ticket, the active-status condition is missing or incorrect. If a request appears twice, we need to examine whether a join has changed what each output row represents.

SQL syntax errors usually produce an error message. A more dangerous mistake is a query that executes successfully but answers a different question. A database cannot infer that our definition of active work is wrong. The reporting question, the query, and the result all need to agree.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 3

Result grain means what one output row represents. The word grain refers to the level of detail. A ticket-level result describes individual requests. An event-level result describes individual events. A status-level result describes groups of requests. These are different answers even when they come from the same tables.

Start with the tickets table. A row containing ticket 1003 describes one water-pressure request. If we choose its identifier and subject, it is still one row for that request. Now connect the request to its events. Ticket 1003 has three event records. The join can return three rows, each pairing the ticket with a different event. The repeated ticket ID does not mean that three separate requests were submitted.

Grouping changes the level of detail in another way. If we group all tickets by status, the result has one row for open work, one for resolved work, and so on. The number beside resolved summarizes several requests. An individual subject no longer identifies the whole group.

This distinction matters whenever someone asks for a count. Counting ticket-event pairs and labeling that number as tickets creates an incorrect report. Looking at identifiers makes the difference visible. We will repeatedly ask what one row represents, because that sentence helps us choose a join, an aggregate, and a useful check.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 4

Relational algebra gives names to operations on relations. In this setting, a relation is a set of tuples with named attributes. We can picture tuples as rows and attributes as columns. The symbols let us describe a data operation independently of a particular screen or programming language.

Selection, written with the Greek letter sigma, keeps rows that satisfy a condition. In SQL, a WHERE clause commonly performs that job. Projection, written with pi, chooses attributes. SQL's output column list has that role, but there is an important difference: mathematical relations are sets, while SQL results retain repeated rows unless we request duplicate removal.

A join forms pairs of related rows. The condition states what makes a pair relevant. Grouping, often written with gamma, combines rows and calculates a summary. Grouping belongs to extended relational algebra rather than the smallest classical operator set. Difference keeps rows present in one result and absent from another. SQL provides EXCEPT for compatible result shapes.

We do not need to memorize all the symbols at once. The useful connection is between an operation's meaning and the SQL that expresses it. SQL also has NULL and three-valued logic, which require special care. Translating the notation into SQL therefore involves reasoning about duplicates, missing values, and the intended result, rather than replacing one symbol with one keyword mechanically.

[Sources]
- Course textbook, Chapter 2, relational notation and SQL semantics.
- https://www.postgresql.org/docs/current/queries.html

## Slide 5

This query finds all high-priority tickets, whether active or finished. Read the source first: metro_support.tickets names the tickets table inside the metro_support schema. A schema is a named namespace within a database. Using the prefix makes this query work even when a new editor tab has a different default search path.

The WHERE clause retains rows whose priority equals the text value high. SQL text literals use single quotation marks. The SELECT list chooses three output columns: ticket_id, subject, and priority. ORDER BY places the rows in ascending ticket-ID order. It does not change which tickets qualify.

On the complete lab dataset, the four matching identifiers are 1001, 1005, 1008, and 1011. Tickets 1005 and 1008 are resolved. Their presence is correct for this query because we have not asked for active status yet. To answer the reporting question from the earlier slide, we would add a condition on status.

The result has one row per matching ticket because this query reads the tickets table directly and retains its identifier. If we selected only priority, SQL would return four rows containing high. SELECT DISTINCT priority would instead return one row. That is the difference between choosing a column and explicitly removing duplicate result values.

[Sources]
- Course textbook, Chapter 2.
- Course dataset, metro_support/tickets.csv.
- https://www.postgresql.org/docs/current/queries-select-lists.html

## Slide 6

Two tickets in our dataset do not yet have an assigned staff member. Their assignee_id is NULL. NULL marks missing information. It is not the number zero, an empty string, or an identifier for an imaginary staff member.

The first predicate uses ordinary equality: assignee_id equals NULL. SQL cannot establish that comparison as true. Comparing an ordinary value with missing information produces unknown, and comparing NULL with NULL also produces unknown. WHERE keeps only rows for which its condition is true. That explains why the first query returns no rows even though unassigned tickets exist.

IS NULL is the predicate designed for this situation. It returns tickets 1004 and 1009. IS NOT NULL returns the other ten tickets. Together these two tests account for all twelve rows.

Unknown and false both fail a WHERE filter, but they are not interchangeable in every SQL context. For example, NOT applied to unknown remains unknown. This is one reason negative conditions can surprise us. The textbook includes a small truth-table example if you want to follow that distinction further.

For the lab, the immediate skill is recognizing a missing value and choosing the appropriate predicate. A blank-looking result cell alone is not a complete explanation. We should know which field is missing, what that means in the case, and whether the report must include that row.

[Sources]
- Course textbook, Chapter 2, NULL.
- https://www.postgresql.org/docs/current/functions-comparison.html

## Slide 7

This query asks for the three newest active requests. The word active has an explicit definition in the WHERE clause: new, open, or in_progress. IN means that the status must equal one of the listed values. A resolved request does not qualify even if its opening time is very recent.

ORDER BY sorts by opened_at in descending order, so later timestamps come first. DESC means descending. The second sort key, ticket_id descending, resolves ties if two requests share the same opening time. LIMIT 3 then keeps the first three rows of the ordered result.

In the complete dataset, the identifiers are 1011, 1009, and 1007, in that order. Ticket 1012 is newer, but it is resolved and therefore excluded. Ticket 1009 has no assignee, but that does not exclude it because this query does not require an assignee.

Without ORDER BY, LIMIT would still return at most three rows, but they would not reliably be the newest three. Apparent storage order is not a promise. A database may change its access path as data and indexes change.

This query illustrates how clauses answer different parts of a question. The filter defines eligibility, the sort defines precedence, and the limit defines the maximum number of results. Changing one part changes the question. The lab will use this pattern without requiring any advanced date arithmetic.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-order.html
- https://www.postgresql.org/docs/current/queries-limit.html

## Slide 8

This diagram shows three selected tickets from the full dataset. Maya has user ID 101 and requested tickets 1001 and 1005. Luis has user ID 102 and requested ticket 1002. The lines connect each ticket's requester_id to the matching user's user_id.

Those matching identifiers express a relationship. The fact that two columns contain numbers is not enough to justify joining them. We need to know what the numbers identify. A requester ID identifies the person who reported a problem. An assignee ID identifies the staff member responsible for handling it. Those relationships answer different questions.

An inner join keeps matching pairs. Maya's user information appears in two pairs in this excerpt because two different tickets refer to her. That repetition is expected. It does not mean that the users table contains duplicate Maya records.

This diagram is an excerpt, not the complete history of either resident. The full dataset includes other tickets. The schema ensures that each ticket has a requester referring to a valid user, so the requester join can preserve one result row per ticket. A different relationship can behave differently. A ticket can have no assignee or many events, and we will see both cases.

Reading the relationship before writing SQL prevents a common error: joining columns that look similar but represent different roles in the application.

[Sources]
- Course dataset, metro_support/users.csv and tickets.csv.
- Course textbook, Chapter 2, Join Related Facts.

## Slide 9

Here is the requester relationship written in SQL. FROM names the tickets table and gives it the alias t. An alias is a shorter name used within this statement. The users table receives the alias u. These aliases make it easier to see which table supplies each column.

The ON condition matches u.user_id with t.requester_id. It describes which user-ticket pairs belong together. The WHERE condition then keeps open tickets. In this dataset, open is one specific status. It is narrower than our active definition, which also includes new and in_progress.

SELECT returns the ticket identifier, subject, and requester's display name. The complete fixture returns tickets 1001, 1007, and 1011. Maya requested 1001. Amina requested 1007 and 1011. Her name therefore appears twice for two different requests.

We could check this result by finding open ticket IDs in tickets.csv, reading each requester ID, and looking up those users in users.csv. That is an independent check of the same relationship, rather than running the same SQL twice.

The first lab changes this example into a neighborhood question. Neighborhood belongs to users, so joining requester information gives the query access to that value. Keep the relationship condition, then adapt the filter. A condition on a resident's neighborhood should use the requester relationship, not the staff assignee relationship.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 10

The first lab asks you to find requests that need attention. Use the complete fixture with eight users, twelve tickets, and twenty-one events. In Supabase, the linked setup creates the metro_support practice schema. In the notebook, use the section for the complete Week 2 dataset. The early notebook demonstration is smaller and will not produce the same counts.

Write three queries. The first finds active requests with high or urgent priority and orders them newest first. The second finds every unassigned request. The third finds active requests reported by residents in the Harbor neighborhood. The lab includes a requester-join example that you can adapt for the third query.

Then investigate the supplied condition that compares assignee_id with NULL using ordinary equality. Explain why its empty result does not mean every ticket has an assignee. Check the Harbor query against the CSV files by identifying one ticket that belongs and one that does not, with a reason for each.

Your submission is week_02_sql_review.sql in Brightspace. Put the brief explanations in SQL comments. You do not need a separate report, screenshot, or GitHub repository. Work individually, and use the chapter or the worked examples when you need a reminder of syntax.

The task is finished when the queries answer the specified questions and your comments explain the supplied error and the independent check. The optional extension is ungraded and adds no required submission.

[Sources]
- Course Week 2, Lab 1: Find the Requests That Need Attention.
- Course textbook, Chapter 2.

## Slide 11

This figure connects the assignee join to relational algebra. The full tickets relation has twelve rows, and the users relation has eight. A Cartesian product pairs every ticket with every user, so it contains ninety-six candidate pairs. Most of those pairs do not describe an assignment.

The condition compares the ticket's assignee_id with the user's user_id. The Greek letter theta represents that condition. Selection keeps the pairs where the condition is true. A theta join is a join using a specified condition, and equality gives us the equijoin used here.

For this assignee relationship, ten ticket-user pairs match. Each assigned ticket refers to one user. The two unassigned tickets have NULL assignee IDs and do not produce matching pairs under ordinary equality. That result explains why an inner-join dashboard can lose requests even when the tickets table contains them.

The ninety-six-pair diagram describes the operation's logical meaning. It does not claim that PostgreSQL physically creates all ninety-six pairs before filtering. The optimizer can choose a different implementation, such as an index lookup or a hash join, while preserving the required result.

The distinction between logical meaning and physical execution is useful throughout database administration. Today we use the logical model to explain missing rows. Later, when we inspect query plans, we will ask how the database carries out the operation and what work it performs.

[Sources]
- Course textbook, Chapter 2, relational join figure.
- https://www.postgresql.org/docs/current/queries-table-expressions.html
- https://www.postgresql.org/docs/current/using-explain.html

## Slide 12

Now the reporting question is different. We want every ticket, together with an assignee name when one exists. The previous inner-join pattern is not sufficient for that requirement. It requires a matching pair and therefore removes an unassigned ticket.

With tickets on the left, a LEFT JOIN keeps each ticket even when there is no matching user on the right. For the unmatched ticket, the right-side output columns contain NULL. The ticket's own identifier and subject remain available. We do not create a fake user or alter the stored data to achieve this result.

On the complete fixture, an inner join from assignee_id to user_id returns ten tickets and omits 1004 and 1009. A left join without a later excluding filter returns all twelve. Those two missing identifiers make the difference easy to test.

There is one important qualification. A later WHERE condition can still remove rows. If we put a condition on the right-side user in WHERE, the unmatched row may fail that condition. When the condition defines which right-side rows are eligible to match while preserving the left side, it belongs in ON or in a filtered input query.

The repair depends on the report's requirement. An inner join is appropriate when the question requires an existing assignment. A left join is appropriate for an all-ticket report that must show unassigned work as well.

[Sources]
- Course textbook, Chapter 2, outer joins and predicate placement.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 13

Ticket 1003 has three events. An event records an action or transition associated with that ticket. When we join tickets to ticket_events on ticket_id, the database forms a pair for each matching event. The output therefore contains three rows with ticket ID 1003.

If the question is to list the ticket's history, those three rows are useful. Each can show the event identifier, event time, and action. If the question is how many tickets exist, counting those three joined rows would answer the wrong question.

COUNT(*) counts result rows. After this join, those rows represent ticket-event pairs. COUNT(DISTINCT t.ticket_id) counts distinct ticket identifiers among the joined pairs, which answers a different question. It still would not count a ticket excluded by an inner join because it had no events. The join and the aggregate both matter.

Another option is EXISTS, which tests whether a matching event exists without adding every event row to the result. That can express a question such as which tickets have any events. Chapter 2 shows the syntax, but the first step is deciding which question we intend to answer.

Repeated values are not automatically a defect. Their meaning depends on the level of detail in the result. We can distinguish source duplication, a legitimate one-to-many relationship, and an incorrect join by following the stable identifiers on both sides.

[Sources]
- Course textbook, Chapter 2, row multiplication and EXISTS.
- https://www.postgresql.org/docs/current/functions-subquery.html

## Slide 14

This query produces a status summary. It starts with ticket rows whose opening date is on or after February first, 2026. Every ticket in this particular fixture satisfies that date condition. The condition still illustrates where source-row filtering happens.

GROUP BY status collects rows with the same status into groups. COUNT(*) counts the ticket rows in each group. AS ticket_count gives that calculated output column a readable name. The result now has one row per status group, rather than one row per ticket.

HAVING applies a condition to each group. It keeps groups with at least two tickets. The complete fixture produces resolved with four, open with three, in_progress with two, and new with two. Closed has one ticket, so HAVING excludes that group. ORDER BY puts larger counts first and uses status to order equal counts consistently.

WHERE and HAVING are not interchangeable. WHERE can filter individual ticket rows before grouping. HAVING can filter a group based on an aggregate such as its count. These are logical meanings; the database may choose an optimized physical execution plan.

A subject column would not describe a whole status group because the group can contain several different subjects. The output columns must identify the group or summarize its contents. That is the same result-grain idea applied to an aggregate query.

[Sources]
- Course textbook, Chapter 2, Group and Aggregate.
- https://www.postgresql.org/docs/current/tutorial-agg.html

## Slide 15

These two queries find tickets assigned to users whose role is agent. They express the same question in different ways. On the complete fixture, both return the same ten assigned ticket IDs. The two unassigned tickets do not qualify.

The query on the left contains another SELECT inside parentheses. That inner query returns the identifiers of users whose role is agent. IN tests whether a ticket's assignee_id appears in that result. This is a membership question. We can understand it by first reading the smaller inner query, then the outer query that uses its result.

The version on the right begins with WITH agents AS. This is a common table expression, usually shortened to CTE. The name agents refers to the result inside the parentheses for this statement. The final SELECT joins tickets to that named result. It does not create a permanent agents table or change the users table.

A CTE can make a query easier to read by giving an intermediate result a useful name. It does not automatically make the query faster. Some CTEs are folded into the surrounding query, and others may be materialized depending on the query and database behavior.

For the next worked example, the named result will contain resolved tickets. In the lab, it will contain active tickets. Naming that filtered input keeps the status definition separate from the staff summary that uses it.

[Sources]
- Course textbook, Chapter 2, subqueries and CTEs.
- https://www.postgresql.org/docs/current/queries-with.html

## Slide 16

This worked report counts resolved tickets for every staff member, including anyone with zero. It is a different question from the active-workload lab, but it uses the same structure. The CTE named resolved contains ticket identifiers and assignee identifiers for tickets whose status is resolved.

The outer query starts from users because the report must preserve staff members. It left-joins the resolved input by assignee ID. The WHERE clause keeps users whose role is agent or supervisor. Notice that this filter refers to the preserved left side. The status condition has already filtered the right-side input inside the CTE.

GROUP BY combines matches for each staff identifier and display name. We include the identifier so that two people with the same name would remain distinct staff members. COUNT(r.ticket_id) counts non-NULL ticket identifiers. Priya has resolved tickets 1003 and 1008. Noah has 1005 and 1012. Elena has no matching ticket, so her count is zero.

For Elena, the left join still produces a row carrying her user information, with NULL in the right-side ticket columns. COUNT(*) would count that row and incorrectly report one resolved ticket. COUNT(r.ticket_id) ignores the missing ticket value and reports zero.

The lab changes the filtered input from resolved tickets to active tickets. Keep the report's intended unit, one row per staff member, and check one person's count with a direct ticket list. That adaptation tests whether the relationship and counting mechanism make sense.

[Sources]
- Course textbook, Chapter 2, staff-workload example.
- https://www.postgresql.org/docs/current/functions-aggregate.html

## Slide 17

Set operators combine compatible query results. Compatible means the results have the same number of columns and corresponding columns have compatible types. The operator compares complete result rows, not the tables' original primary keys unless those keys are part of the selected output.

The small example uses A containing one and two, and B containing two and three. UNION includes values from either result and removes repeated result rows, giving one, two, and three. UNION ALL retains both copies of two. INTERSECT keeps the shared value two. EXCEPT keeps the value in A that does not occur in B, which is one.

We have displayed the values in sorted order to make the comparison easy. Neither UNION nor UNION ALL guarantees that output order. In particular, UNION ALL does not promise that every A row arrives before every B row. To require an order, the combined SQL query needs ORDER BY.

Keeping duplicates can be the correct choice. If two independent event sources each contain a real event with the same selected values, removing one may lose useful information. Conversely, a list of distinct people may need duplicate removal. The operator should express that decision.

The lab extension uses EXCEPT to compare requester IDs and assignee IDs. It is optional. The core assignment concentrates on the join, staff count, and controlled update rather than adding another required set of queries.

[Sources]
- Course textbook, Chapter 2, set operations.
- https://www.postgresql.org/docs/current/queries-union.html

## Slide 18

This is a complete rehearsal of a change to ticket 1002. The first SELECT previews its current priority, which is medium in the starting fixture. We then begin a transaction. A transaction gives related database actions a boundary within which they can succeed together or be rolled back before commitment.

UPDATE changes the priority to high, but only where ticket_id equals 1002. That WHERE clause is essential. Without it, the command could change many tickets. RETURNING shows the identifier and new priority of the affected row. The SELECT inside the transaction confirms that the transaction can see its own change.

ROLLBACK discards this uncommitted update. The final SELECT must show medium again. That final query is important: it checks the restored value instead of assuming that the rollback worked as intended.

Run this whole block together in one SQL Editor execution. Running fragments in separate pooled sessions can break the intended transaction boundary. The notebook uses one connection and explains which commands go through execute and which return a result table.

This demonstration uses ticket 1002. The lab applies the same pattern to ticket 1006. Both start at medium, but the different identifier makes you inspect the target rather than copy a statement without reading it. A transaction does not make a bad predicate harmless after commitment, and this simple update does not establish a general recovery strategy.

[Sources]
- Course textbook, Chapter 2, Review Safe Data Changes.
- https://www.postgresql.org/docs/current/tutorial-transactions.html
- https://www.postgresql.org/docs/current/dml-returning.html

## Slide 19

A useful check approaches the result from a different direction. Suppose a staff summary says that one person has two resolved tickets. We can list that person's resolved ticket IDs directly from the tickets table and count them. That list should explain the aggregate instead of merely repeating it.

Boundary cases are particularly informative. Elena is a staff member with no assigned tickets. If the report omits her, an inner join or a filter may be removing zero-workload staff. If the report says she has one ticket, COUNT(*) may be counting the placeholder row produced by a left join. Those two mistakes require different repairs.

For an all-ticket dashboard, the important boundary cases are 1004 and 1009. Both lack assignees, but both are real requests. A report that promises every ticket must retain them. Comparing only total counts can hide a mistake if one missing row is accidentally balanced by another repeated row. Checking identifiers helps expose that situation.

These checks establish specific properties on this fixture. They do not show that the query is fast on a million tickets, safe under concurrent changes, or available during a server failure. Later weeks develop those additional questions.

In a code review, a short explanation of the question and a concrete boundary-case check are often more useful than a screenshot containing an unexplained result table. The lab keeps that explanation with the SQL it describes.

[Sources]
- Course textbook, Chapter 2, verification examples.
- Course Week 2 individual labs.

## Slide 20

The second lab repairs a staff dashboard. It uses the same complete dataset, but the reporting problem now includes relationships, summaries, and a controlled change. Work individually and keep the work in one SQL file.

First, run the supplied all-ticket query. It uses an inner join to the assignee and loses two requests. Repair the join so that all twelve tickets remain. A missing assignee name should remain NULL. There is no need to invent a staff member or modify the source records.

Second, use the supplied active-ticket CTE to count active work for each staff member. Staff means agent or supervisor for this report. Preserve a staff member with zero matching tickets. The resolved-ticket example from class shows how a filtered input, a left join, and COUNT of the ticket identifier work together. Adapt the definition to active work, then check Priya's count with a direct list of her active ticket IDs.

Finally, test a change to ticket 1006 from medium to high priority. Preview the row, observe the changed value inside the transaction, roll back, and verify medium afterward.

Submit week_02_relational_sql_studio.sql in Brightspace with concise comments next to the relevant SQL. No separate reflection, database password, connection URL, or additional document belongs in the submission. The required work is the repaired report, the checked staff summary, and the rollback experiment.

[Sources]
- Course Week 2, Lab 2: Repair the Staff Dashboard.
- Course textbook, Chapter 2.

## Slide 21

We have used SQL to describe results at several levels of detail. A filter chooses which rows qualify. The output list chooses which values describe them. A join forms related pairs, and its type determines what happens to unmatched rows. Grouping changes the result from individual records to summaries.

The service-desk case gives each of those ideas a concrete consequence. Unassigned tickets disappear from an inner-join dashboard. One ticket can repeat when it has several events. A staff member with no matching tickets needs a left join to remain in a staff report, and COUNT of the ticket identifier to receive zero rather than one.

We also separated a tentative data change from a committed change. The transaction experiment previews a specific target, changes it, inspects the new value, rolls it back, and checks the original value again. The SQL file records the operation and its explanation together.

These are foundation skills for the rest of the course. Next week we will inspect and improve schemas. A schema tells us which values and relationships the database permits. Understanding the query result helps us decide which rules matter and how to test them.

Chapter 2 remains available as a reference. The weekly guide names the reading for each meeting, and later labs will reuse these SQL operations in new situations. We will continue practicing them as we add security, performance, and recovery questions.

[Sources]
- Course textbook, Chapters 2 and 3.
- Course Week 2 individual labs.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
