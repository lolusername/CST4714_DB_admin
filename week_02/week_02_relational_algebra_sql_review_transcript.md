# Week 2: Relational Algebra and Major SQL Review - Spoken Transcript

## Slide 1

Welcome to Week 2. This week is a SQL review. I am not assuming you remember SQL from an earlier course, so we will rebuild the syntax as we go.

SQL stands for Structured Query Language. The useful thing about it is that you describe the result you want, and the database works out how to find it. That separation is why the same SQL keeps working across different database systems.

Look at the subtitle: finding requests, checking reports, and testing a careful data change. Those are the jobs this week. On Day 1 we find requests that need attention. On Day 2 we repair a staff report that loses unassigned requests, count work for staff who may have no assignments, and test a priority change without keeping it. Ordinary tasks, but a wrong report means a real request gets ignored.

Our data is the Metro Support service desk: eight users, twelve tickets, and twenty-one ticket events. A ticket is a request for help. An event records something that happened to a ticket. One warning about the notebook. Its early demonstration data reuses some of the same ticket numbers with different details, so do not compare those results to the lab. Before either lab, run the section called Use the Complete Week 2 Lab Dataset.

Each lab is one SQL file, and your explanations go right next to the query, as SQL comments that start with two hyphens.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/tutorial-sql.html

## Slide 2

Let's start the way real work starts: with a question in plain English. A staff member asks, which high-priority requests are still active? Before I type a single SQL keyword, I need to know exactly what those words mean, because the database cannot guess.

Take high priority first. In this dataset priority is a stored value: low, medium, high, or urgent. High and urgent are different values. If the staff member really meant high or urgent, that is a different query, so we ask. Now take active. A request can be high priority and already resolved. If I filter on priority alone, finished work sneaks into the list. So for this week, active means status is new, open, or in_progress.

Look at the three boxes. The question says one result row should be one request that still needs work. The condition says priority is high and status is in the active set. Both conditions. And the check says read the matching ticket IDs in the source data yourself, separately from the query.

Here is why the check matters. A syntax error gives you a message, and you fix it. The dangerous mistake is a query that runs perfectly and answers a different question. If a resolved ticket shows up, the status condition is wrong. If a request appears twice, something has changed what a row means. The question, the query, and the result all have to agree.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 3

That last idea has a name, and it is the most useful word this week: grain. Result grain means what one output row represents. Look at the three columns on the slide.

On the left, one row per ticket. A row containing ticket 1003 describes one request, the low water pressure one. Keeping ticket_id in the output is how you tell which request each row is.

In the middle, one row per event. Ticket 1003 has three event records. When we join the ticket to its events, we get three rows, each pairing the same ticket with a different event. You will see 1003 three times. That does not mean three people reported low water pressure. It means one request has a history with three entries.

On the right, one row per status. If we group tickets by status, we get one row for open, one for resolved, and so on, each with a count. Now a row is a group of requests, and no single subject describes it anymore.

Why does this matter? Because someone always asks for a count. If you count ticket-event pairs and label the number tickets, your report is wrong, and nothing in SQL will warn you. So every time we write a query this week, I am going to ask the same question: what does one row represent? That answer tells you which join to use, how to count, and how to check the result.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 4

Here is the vocabulary underneath SQL: relational algebra. A relation is a set of tuples with named attributes. Picture tuples as rows and attributes as columns. The point of the notation is that we can describe an operation on data without caring about any particular screen or programming language.

Read the table row by row. Selection, the Greek letter sigma, keeps rows where a condition is true. In SQL that is WHERE. Look at the last column: unknown does not pass WHERE. Hold on to that, because it comes back with NULL in two slides. Projection, pi, chooses columns. That is your SELECT list. But here is a difference: a mathematical relation is a set, so duplicates disappear. SQL keeps repeated rows unless you ask it to remove them.

Join forms matching pairs of rows, and one source row can have many matches. Remember the ticket with three events. Grouping, gamma, summarizes rows into groups. Strictly speaking it is an extension of the basic algebra, not one of the classic operators. Difference keeps rows in A that are absent from B. SQL calls that EXCEPT, and both sides need the same number of columns with compatible types.

You do not need to memorize the symbols today. What I want is the connection between what an operation means and the SQL that expresses it. And notice why it is never a mechanical translation: SQL adds duplicates and NULL, and you have to reason about both.

[Sources]
- Course textbook, Chapter 2, relational notation and SQL semantics.
- https://www.postgresql.org/docs/current/queries.html

## Slide 5

Let's write the first real query. Read it from the FROM line. metro_support.tickets means the tickets table inside the metro_support schema. A schema is a named namespace inside the database. Why bother with the prefix? Because a new editor tab may have a different default search path, and without the prefix your query might not find the table at all.

WHERE priority = 'high' keeps rows whose priority is the text value high. Text in SQL goes in single quotes. The SELECT list chooses three columns: ticket_id, subject, and priority. ORDER BY ticket_id sorts the result. Look at the note on the right: ORDER BY changes order, not membership. Sorting never adds or removes a ticket.

The result is four tickets: 1001, 1005, 1008, and 1011. Now look closer. 1005 and 1008 are resolved. Is the query wrong? No. It answers exactly what it asks, all high-priority tickets. It just is not the question from slide 2 yet. To get there we would add a condition on status.

One more thing about grain. This result has one row per ticket because we kept ticket_id. If I selected only the priority column, I would get four rows that all say high. SELECT DISTINCT priority would give one row. Choosing a column and removing duplicates are two different decisions, and SQL makes you say which one you want.

[Sources]
- Course textbook, Chapter 2.
- Course dataset, metro_support/tickets.csv.
- https://www.postgresql.org/docs/current/queries-select-lists.html

## Slide 6

Two tickets in our dataset have nobody assigned yet. Their assignee_id is NULL. NULL means the information is missing. It is not zero, it is not an empty string, and it is not some imaginary staff member.

Look at the three predicates on the slide. The first is the one everybody writes: assignee_id = NULL. Result: no rows. Why? Comparing a value to missing information does not give true or false. It gives unknown. Even NULL compared to NULL is unknown, because two missing values are not known to be equal. And WHERE keeps only rows where the condition is true. Unknown is not true, so every row is dropped. The query runs fine, returns nothing, and looks like it is telling you every ticket is assigned. It is not.

The second predicate, IS NULL, is built for exactly this. It returns tickets 1004 and 1009. The third, IS NOT NULL, returns the other ten. Ten plus two is twelve, so together they account for every ticket.

One subtlety. Unknown and false both fail WHERE, but they are not the same thing. NOT applied to unknown is still unknown, which is why negative conditions can surprise you. The chapter has a short truth table if you want to follow that further.

For the lab, the skill is simple: recognize a missing value, use IS NULL, and be able to say which field is missing and whether the report must still include that row.

[Sources]
- Course textbook, Chapter 2, NULL.
- https://www.postgresql.org/docs/current/functions-comparison.html

## Slide 7

Now a query with more moving parts: the three newest active requests. Each clause answers a different part of the question, so let's read it that way.

WHERE status IN new, open, in_progress. IN means the status must equal one of the listed values. That is our definition of active, written down explicitly. A resolved request does not qualify, no matter how recent it is.

ORDER BY opened_at DESC. DESC means descending, so the latest timestamps come first. Then a second sort key, ticket_id descending. Why? If two requests opened at exactly the same time, the database could put them in either order. The second key breaks the tie, so you get the same answer every time. Then LIMIT 3 keeps the first three rows of the sorted result.

The answer, in order, is 1011, 1009, and 1007. Two things to notice. Ticket 1012 is newer than all of them, but it is resolved, so the filter removed it before the sort ever mattered. And 1009 has no assignee, but that does not exclude it, because nothing in this query asks for an assignee.

Here is the trap. Without ORDER BY, LIMIT 3 still returns three rows, and they might even look right today. But the order rows happen to come out in is not a promise. As data and indexes change, the database may read them differently. So the filter defines who is eligible, the sort defines who comes first, and the limit defines how many you keep.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-order.html
- https://www.postgresql.org/docs/current/queries-limit.html

## Slide 8

Now we connect two tables. This diagram shows three tickets from the full dataset. On the left, two users, 101 and 102. On the right, tickets. Tickets 1001 and 1005 were requested by Requester 101. Ticket 1002 was requested by Requester 102. Each line connects a ticket's requester_id to a user's user_id.

That matching ID is a relationship, and I want you to think about what it means before you write any join. Two columns that both contain numbers is not a reason to join them. A requester ID identifies the person who reported a problem. An assignee ID identifies the staff member handling it. Both point at the users table, and they answer completely different questions. Join on the wrong one and your query runs perfectly and reports nonsense.

An inner join keeps matching pairs. Look at Requester 101: that user shows up in two pairs, because two different tickets point to the same person. That repetition is expected. It does not mean the users table has two copies of Requester 101.

Keep in mind this is only an excerpt. The full dataset has other tickets for these residents too. Because every ticket must have a requester who actually exists, the requester join keeps exactly one row per ticket. Other relationships behave differently. A ticket can have no assignee at all, or many events, and we will see both cases. Reading the relationship first is what stops you from joining columns that only look alike.

[Sources]
- Course dataset, metro_support/users.csv and tickets.csv.
- Course textbook, Chapter 2, Join Related Facts.

## Slide 9

Here is that requester relationship written in SQL. I want you to read it in the order shown on the right, not top to bottom.

First, the sources. FROM metro_support.tickets AS t, JOIN metro_support.users AS u. The letters t and u are aliases, short names that exist only inside this statement. They make it obvious which table each column comes from.

Second, the matching condition. ON u.user_id = t.requester_id. That says which user-ticket pairs belong together: the user who reported the ticket. Look at the note at the bottom. requester_id means who reported the issue. assignee_id means who is handling it. Same users table, different relationship.

Third, the filter and the grain. WHERE t.status = 'open'. Notice that open is one specific status. It is narrower than our active definition, which also includes new and in_progress. The SELECT gives one row per open ticket, with its subject and the requester's display name.

The result is tickets 1001, 1007, and 1011. Requester 101 reported 1001. Requester 103 reported both 1007 and 1011, so that name appears twice, for two different requests.

How would you check this without trusting the query? Open tickets.csv, find the open tickets, read their requester IDs, and look those up in users.csv. That is a second path to the same answer. In Lab 1 you will adapt this into a neighborhood question. Neighborhood lives on the users table, so you need the requester relationship, not the assignee.

[Sources]
- Course textbook, Chapter 2.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 10

Here is Lab 1, Find the Requests That Need Attention. Work individually, with the complete fixture: eight users, twelve tickets, twenty-one events.

The main path is the Colab notebook. Open it, save a copy in Drive, and run the cells through Use the Complete Week 2 Lab Dataset. You do not need a Supabase account this week. If you already have a personal Supabase practice project, you can run the setup file in its SQL Editor instead, and it resets the metro_support practice schema. Either way, if your counts are not eight, twelve, and twenty-one, stop and fix that first, because every answer after it depends on the data.

Write three queries. First, active requests with high or urgent priority, newest first. Second, every unassigned request, using IS NULL. Third, active requests reported by residents in the Harbor neighborhood. The lab gives you a requester-join example to adapt for that one.

Then investigate the colleague's query that compares assignee_id to NULL with an equals sign, and explain why its empty result does not mean every ticket is assigned. And check your Harbor query against the CSV files: name one ticket that belongs and one that does not, with the reason for each.

Submit week_02_sql_review.sql in Brightspace, with your explanations as SQL comments. Copy in the SQL itself, not the Python wrapper around it. No screenshot, no separate report, no GitHub repository. If you finish early, the extension is optional and ungraded.

[Sources]
- Course Week 2, Lab 1: Find the Requests That Need Attention.
- Course textbook, Chapter 2.

## Slide 11

Welcome back. Today is about relationships, summaries, and safe changes, and we start with a picture of what a join actually means.

Look at the figure. The tickets relation has twelve rows and the users relation has eight. A Cartesian product pairs every ticket with every user. Twelve times eight is ninety-six candidate pairs. Most of them are nonsense: a ticket paired with someone who has nothing to do with it.

Now apply the condition at the bottom of the slide: tickets.assignee_id equals users.user_id. In the notation, the Greek letter theta stands for that condition, and selection keeps only the pairs where it is true. A join with a stated condition is a theta join, and when the condition is equality, we call it an equijoin.

For the assignee relationship, ten pairs survive. Each assigned ticket matches one user. And the two unassigned tickets? Their assignee_id is NULL, NULL compared with anything is unknown, so they produce no pair at all. That is exactly how an inner-join dashboard loses requests even though the tickets table still has them.

One caution. Ninety-six pairs is the logical meaning. PostgreSQL does not physically build all ninety-six and then filter. The optimizer may use an index lookup or a hash join, as long as the result is the same. Today we use the meaning to explain missing rows. Later, when we read query plans, we will look at how the work is actually done.

[Sources]
- Course textbook, Chapter 2, relational join figure.
- https://www.postgresql.org/docs/current/queries-table-expressions.html
- https://www.postgresql.org/docs/current/using-explain.html

## Slide 12

So here is the reporting question that exposes the problem. We want every ticket, with the assignee's name when there is one. The inner join on the left cannot do that. It keeps only matching pairs, so it omits 1004 and 1009, the two tickets with a NULL assignee_id. The table holds twelve tickets, and the dashboard quietly shows ten.

The left join on the right fixes this. With tickets on the left side, a LEFT JOIN keeps every ticket, even when no user matches on the right. For an unmatched ticket, the user columns come back NULL, while the ticket's own ID and subject stay. Run it on the full fixture and you get all twelve. We did not invent a fake user called Unassigned, and we did not touch the stored data. The fix is in the query.

There is one catch. A later WHERE clause can still remove rows. Say you add WHERE the user's role is agent. For an unassigned ticket the role is NULL, the condition is unknown, and the row disappears. You are back to an inner join without realizing it. If a condition decides which right-side rows are allowed to match, put it in ON, or filter the right side first.

Neither join is wrong. An inner join is right when the question requires an assignment. A left join is right when the report promises every ticket.

[Sources]
- Course textbook, Chapter 2, outer joins and predicate placement.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 13

Now the other surprise a join can give you: more rows instead of fewer. Ticket 1003 has three events. An event records an action or a change on that ticket. When we join tickets to ticket_events on ticket_id, the database makes a pair for each matching event, so the output has three rows with ticket ID 1003.

Is that a bug? It depends on the question. If the question is show me this ticket's history, three rows is exactly right. Each row can show the event ID, the time, and the action. If the question is how many tickets are there, counting those three rows gives the wrong answer.

So let's be precise about counting. COUNT star counts result rows, and after this join a row is a ticket-event pair. COUNT DISTINCT t.ticket_id counts distinct ticket IDs among those pairs, which answers a different question. And even that would miss a ticket with no events at all, because the inner join already removed it. The join and the aggregate both matter.

A third option is EXISTS. It asks whether at least one matching event exists, without adding every event row to the result. That fits a question like which tickets have any events. The chapter shows the syntax.

The general lesson is that repeated values are not automatically a defect. Follow the stable IDs on both sides, and you can tell a real one-to-many relationship from a join that went wrong.

[Sources]
- Course textbook, Chapter 2, row multiplication and EXISTS.
- https://www.postgresql.org/docs/current/functions-subquery.html

## Slide 14

Now summaries. Read this query in the order shown on the right, because each clause works at a different level.

WHERE opened_at is on or after February first, 2026. WHERE filters individual ticket rows, before any grouping happens. In this fixture every ticket meets that date, so it removes nothing, but it shows you where row filtering lives.

GROUP BY status collects tickets with the same status into one group. COUNT star counts the rows in each group, and AS ticket_count gives that column a readable name. The grain has changed: one row per status, not one row per ticket.

HAVING count star at least two filters groups. It looks at each group's count and keeps the groups with two or more. ORDER BY puts bigger counts first and uses status to order equal counts, so the order is stable.

The result is resolved 4, open 3, in_progress 2, and new 2. The closed group has one ticket, so HAVING leaves it out.

Why two filtering clauses? Because they ask different things. WHERE looks at one ticket row at a time, so it cannot ask about a count. HAVING looks at a whole group, so it can.

And one grain point. You cannot just add subject to this SELECT list. A status group contains several different subjects, so no single subject describes it. Every output column has to identify the group or summarize what is in it.

[Sources]
- Course textbook, Chapter 2, Group and Aggregate.
- https://www.postgresql.org/docs/current/tutorial-agg.html

## Slide 15

Here are two ways to ask the same question: which tickets are assigned to users whose role is agent? On the full fixture, both return the same ten assigned ticket IDs.

The left version is a nested query, a SELECT inside parentheses. Read it inside out. The inner query returns the user IDs of agents. Then the outer query uses IN to ask: is this ticket's assignee_id in that list? It is a membership question, and you can run the inner part by itself first.

The right version starts with WITH agents AS. That is a common table expression, a CTE. It gives the result in the parentheses a name, agents, and then the final SELECT joins tickets to that named result. Look at the note at the bottom: the name exists for this statement only. It does not create an agents table, and it does not change the users table.

Why use a CTE? Readability. You give an intermediate result a meaningful name, and the main query reads almost like a sentence. Do not assume it makes anything faster, though. Depending on the query, the database may fold a CTE into the surrounding query or compute it separately.

Here is where this goes next. In the worked example coming up, the named result holds resolved tickets. In your lab, it holds active tickets. Naming that filtered input keeps the status definition separate from the staff report that uses it.

[Sources]
- Course textbook, Chapter 2, subqueries and CTEs.
- https://www.postgresql.org/docs/current/queries-with.html

## Slide 16

This is the worked example behind Lab 2: a staff report that includes zero. The question is how many resolved tickets each staff member has, including anyone with none.

The CTE named resolved holds the ticket ID and assignee ID of every resolved ticket. The status filter lives here, inside the CTE, so it only shapes the right-hand side.

The main query starts FROM users, because the report must keep every staff member, and it left-joins resolved on assignee ID. The WHERE keeps users whose role is agent or supervisor. Notice that it filters the preserved left side, the users, so it cannot knock out an unmatched row.

GROUP BY user_id and display_name gives one row per staff member. We keep the ID so two people with the same name would still be counted separately.

Look at the result. Agent 201 has 2, tickets 1003 and 1008. Agent 202 has 2, tickets 1005 and 1012. Agent 203 has 0. One labeling trap: despite that name, user 203 is the supervisor, which is why the WHERE includes supervisor.

Now the key part, in the box on the right. Agent 203 has no match, but the left join still produces one row for that user, with NULL in the ticket columns. COUNT of r.ticket_id ignores the NULL and gives 0. COUNT star counts the row and gives 1. One small change in what you count, and the report says someone resolved a ticket they never touched.

[Sources]
- Course textbook, Chapter 2, staff-workload example.
- https://www.postgresql.org/docs/current/functions-aggregate.html

## Slide 17

Set operators combine the results of two queries. The rule is that the results must be compatible: same number of columns, and matching columns with compatible types. They compare whole result rows, not primary keys, unless the key is one of the columns you selected.

Look at the table. A contains 1 and 2. B contains 2 and 3. UNION gives rows from either side and removes repeats: 1, 2, 3. UNION ALL keeps everything, so 2 shows up twice: 1, 2, 2, 3. INTERSECT keeps what is in both, just 2. EXCEPT keeps what is in A but not in B, just 1.

Read the caveat at the bottom. We listed those values in sorted order so you can compare them easily. SQL does not promise that order. UNION ALL does not even promise that all of A arrives before all of B. If you need an order, put ORDER BY on the combined query.

So how do you choose between UNION and UNION ALL? That is a decision about meaning. If two event sources each record a real event with the same selected values, removing one throws away information, so UNION ALL is right. If you want a list of distinct people, removing repeats is right. Pick the operator that says what you mean.

The lab extension uses EXCEPT to find requester IDs that never appear as assignees. It is optional. The required work stays on the join, the staff count, and the controlled update.

[Sources]
- Course textbook, Chapter 2, set operations.
- https://www.postgresql.org/docs/current/queries-union.html

## Slide 18

Now the most important habit of the week: changing data carefully. This is a full rehearsal of a priority change on ticket 1002.

First a SELECT that previews the target. Ticket 1002 is medium in the starting data. You look before you change, so a wrong ID gets caught early.

BEGIN starts a transaction, a boundary around related actions so they succeed together or get undone together. UPDATE sets priority to high, WHERE ticket_id = 1002. That WHERE is the whole safety of the statement. Leave it off and every ticket becomes high. RETURNING shows the row the update actually changed: 1002, high. The next SELECT shows high again, because a transaction can see its own changes.

Then ROLLBACK throws the change away, and the final SELECT shows medium again. Do not skip that last query. It is how you prove the rollback worked instead of assuming it did.

A practical warning. Run the whole block together, on one connection. If the pieces land on different connections, the transaction boundary breaks. And the Supabase SQL Editor shows only the last statement's result, which here is the final medium, so you would never see the high rows. That is why we watch this in the notebook: it keeps one connection and shows every result.

The lab uses ticket 1006, which also starts at medium. A different ID on purpose, so you read the target instead of copying. And remember, a transaction protects you before commit, not after.

[Sources]
- Course textbook, Chapter 2, Review Safe Data Changes.
- https://www.postgresql.org/docs/current/tutorial-transactions.html
- https://www.postgresql.org/docs/current/dml-returning.html

## Slide 19

How do you know a report is right? Not by running the same query twice. A useful check comes at the answer from a different direction.

One: list the ticket IDs behind a single staff count. If the summary says someone has two resolved tickets, pull that person's resolved tickets straight from the tickets table. The list should explain the number, not just repeat it.

Two: keep a staff member with zero matches. Agent 203 is our boundary case, a staff member with no assigned tickets. If the report leaves that user out, an inner join or a filter is removing zero-workload staff. If it says one, COUNT star is counting the placeholder row from the left join. Two different symptoms, two different repairs.

Three: check that tickets 1004 and 1009 still appear on an all-ticket dashboard. Both are real requests with no assignee. And check the IDs, not just the total. If one ticket goes missing and a bad join repeats another, the count can still look right. Only the identifiers reveal it.

Four: a correct answer on this small fixture says nothing about speed on a million tickets, safety when people change data at the same time, or surviving a server failure. Those are later weeks.

In a code review, a short statement of the question and one concrete boundary check beat a screenshot of an unexplained result table. That is why your labs keep the explanation beside the SQL.

[Sources]
- Course textbook, Chapter 2, verification examples.
- Course Week 2 individual labs.

## Slide 20

Here is Lab 2, Repair the Staff Dashboard. Same complete dataset, individual work, one SQL file.

Part one. Run the supplied all-ticket query. It uses an inner join to the assignee, and it loses two requests. Find which ticket IDs are missing, then repair the join so all twelve tickets remain. An unassigned ticket should show a NULL assignee name. Do not invent a staff member to fill the blank, and do not edit the source records.

Part two. Use the supplied active-ticket CTE to count active work for each staff member. Staff here means role agent or supervisor, and a staff member with zero matching tickets must still appear, with zero. This is the worked example from slide 16, with active work in place of resolved. Then check Agent 201's count with a direct list of that user's active ticket IDs, and explain why the two unassigned active tickets are not anybody's workload.

Part three. Test changing ticket 1006 from medium to high. Preview the row, show the change inside the transaction, roll back, and verify it is medium afterward. Do this part in the Colab notebook so you can actually see the high value before the rollback, because the Supabase editor shows only the final result.

Submit week_02_relational_sql_studio.sql in Brightspace, with short comments next to the SQL they explain. No separate reflection, and never a database password or connection URL in the file. The extensions at the end of the lab are ungraded.

[Sources]
- Course Week 2, Lab 2: Repair the Staff Dashboard.
- Course textbook, Chapter 2.

## Slide 21

Let's pull the week together. Read the first line on the slide: filters choose rows, joins form pairs, and grouping changes what one result row represents. Every query we wrote this week was some combination of those three, and the question we kept asking was the same: what does one row mean?

The service desk made each idea concrete. A missing assignee must not remove a ticket from an all-ticket report. That is the left join keeping 1004 and 1009. COUNT of the ticket ID gives zero when a left join finds no match. That is Agent 203 getting zero instead of one. And a ticket can legitimately repeat when it has several events, which is fine for a history and wrong for a count.

The last line is the habit I most want you to keep: a targeted change can be inspected before ROLLBACK discards it. Preview the target, change it inside a transaction, look at the new value, roll back, and check the original again. Your SQL file records the operation and the reasoning together.

These are foundation skills for the rest of the course. Next week we use these same queries to build views, look at generated identifiers, and rehearse a schema change safely. After that we keep adding security, performance, and recovery questions on top of them. Chapter 2 stays useful as a reference, so if joins or transactions still feel shaky, revisit this week's worked examples before Week 3.

[Sources]
- Course textbook, Chapters 2 and 3.
- Course Week 2 individual labs.

## Slide 22

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: NULL: why = NULL finds nothing (1:20); What does one row mean after a join? (1:16); Counting workload, including zero (1:28). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 2 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
