# Week 4: Reliable SQL Reports - Spoken Transcript

## Slide 1

We have learned to store requests, protect values with constraints, and give useful queries names through views. This week asks a different question: does a report actually count the thing its reader thinks it counts? A query can run successfully and still produce a misleading number. The database cannot infer the business question from valid SQL syntax.

We will keep the same Metro Support data so we can concentrate on that reasoning rather than learn another domain. The first meeting follows a ticket through its event history and shows why joining that history can inflate a request count. We will name intermediate results with WITH and compute several carefully defined measures without losing categories with zero matching requests.

The second meeting introduces one new window-function pattern. We will number each ticket's events from newest to oldest, keep the first event, and attach it to a request report. You will see each intermediate result before combining the query. There is no requirement to memorize a list of window functions.

Both labs are individual. Each asks for one SQL file containing a working query and a short explanation. The important skill is being able to state what a result row means, show how the SQL preserves that meaning, and check a result against specific records.

## Slide 2

Before any reporting code, let us establish the dataset. We are not switching to a larger or hidden source. There are eight users, twelve tickets, and twenty-one events. Users include residents, agents, a supervisor, and an analyst. A ticket has a required requester and an optional assignee. Events refer back to the ticket whose history they describe.

Open the Week 4 notebook and run its introduction and setup before the Day 1 examples. The notebook uses PostgreSQL and creates a disposable copy of the data. You may instead use the supplied setup in a personal Supabase project or the PGlite playground. This week's queries do not require the source_channel column from last week, so a fresh copy is fine. If you keep an existing copy, do not reset it simply because a new week has started.

Check the starting counts and inspect ticket 1003. It has three events. Then inspect ticket 1004. It has one event and no assignee. The overall active set contains seven tickets, including unassigned tickets 1004 and 1009. These examples will help us distinguish a request from a history row and a missing relationship from a missing request.

We will state the unit of each result before counting. A row per ticket and a row per ticket-event pair are not interchangeable, even when both outputs contain a ticket_id column.

## Slide 3

Ticket 1003 reports low water pressure. The ticket row holds its current state, which is resolved. Its history contains a created event, a change to in_progress, and a later change to resolved. The table on this slide shows those three events in chronological order.

There is still only one request. The three history rows describe things that happened to it. A useful event report might count all three. A report of how many residents submitted water requests should not count this ticket three times.

The event identifier distinguishes each history record. The ticket identifier repeats because it links all three records to the same request. Repetition of that foreign key is expected; it does not mean the event table has duplicate primary keys. Before deciding to delete a row or add DISTINCT, we need to identify which fact each row represents.

The current status in tickets and the sequence of event statuses answer different questions. For the current backlog, we use tickets.status. For the history of a particular request, we inspect ticket_events. Later we will find the latest recorded event, but we will not assume that every event necessarily changes a status: an assignment event can leave the status unchanged.

## Slide 4

This query follows the relationship explicitly. PostgreSQL reads a ticket and pairs it with every event whose ticket_id matches. The WHERE condition keeps ticket 1003, and ORDER BY makes its history easy to inspect. The output has three rows because that one ticket has three matching events.

Notice which columns repeat. The ticket identifier, subject, and current status belong to the request, so they are repeated once for each matching history row. The event identifier changes. The query has not created three stored tickets. It has produced three rows in a result.

Run this query and compare the event identifiers with the previous slide. If you can explain all three rows, you are ready to reason about the aggregate. If not, stay with this small example rather than hide it behind GROUP BY.

The alias t stands for tickets in this query, and e stands for ticket_events. The prefixes tell PostgreSQL which ticket_id we mean. ON states the relationship; WHERE selects a particular request. Neither clause is inferred from similar column names. In the next example, we will remove the single-ticket filter and see why counting the joined rows can answer the wrong question.

## Slide 5

Suppose a dashboard groups these joined rows by category and labels COUNT star as requests. That label is misleading. The join has changed the unit being counted to a ticket-event pair. Each ticket contributes as many rows as it has events.

In this fixture, the five category results sum to twenty-one. The base ticket table contains twelve rows. Water shows five because ticket 1003 contributes three history rows and ticket 1008 contributes two. Water actually has two requests. The command succeeds because PostgreSQL is counting exactly the rows the query supplied.

There are two important repairs, depending on the question. If the report needs only ticket attributes and request counts, do not join the event table at all. Read tickets. If the report needs a summary of event history for each ticket, summarize that history to one row per ticket before joining it.

COUNT DISTINCT of a ticket identifier can answer some distinct-ticket questions, but it is not a universal repair for a query whose relationships are wrong. It also will not automatically repair sums or preserve unmatched records. The more reliable first move is to state the intended row meaning, inspect the intermediate rows, and choose the join and aggregation that implement that meaning.

## Slide 6

We will first report directly from tickets. COUNT star counts result rows. COUNT assignee_id ignores NULL values in that column. COUNT DISTINCT assignee_id counts the different non-null identifiers. On the starting fixture those results are twelve tickets, ten assigned tickets, and two different assignees. Those are three different facts, not three competing answers to the same question.

For the lab we need several measures for each category. PostgreSQL's FILTER clause lets an aggregate count only rows that satisfy its own condition, while the other aggregates still see the whole group. The expression on this slide counts resolved tickets. A top-level WHERE resolved condition would instead remove every non-resolved ticket before grouping.

That difference matters for categories with no resolved work. We want to show the category with a zero, not make it vanish from the result. The starting data contains five categories. Counting all tickets and counting only resolved tickets within the same group preserves each of those categories.

Read the expression from the inside out: test whether the row's status is resolved; include it in this count if true; otherwise do not include it in this count. A later lab measure will combine two conditions with AND, but the relationship between the group and the conditional count stays the same.

[Sources] PostgreSQL aggregate-expression documentation: https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES

## Slide 7

Here is the complete worked pattern. Both aggregates read the same ticket group. total_tickets counts every request in that category. resolved_tickets counts only the rows whose status is resolved. GROUP BY gives us one output row per category, and ORDER BY controls the display order.

Parks has two requests and zero resolved requests. Transportation also has two and zero. Sanitation has three and one, streetlight has three and one, and water has two and two. The totals add to twelve tickets and four resolved tickets. We can independently check four by listing the identifiers with status resolved: 1003, 1005, 1008, and 1012.

We have not joined events because neither requested measure needs event data. Keeping an unnecessary join out of a report is often more important than making a complicated query shorter. Nor have we guessed a denominator: total_tickets clearly refers to all requests in the category.

Your lab will adapt this complete pattern. It asks for active requests and for active requests whose priority is high or urgent. Keep all five categories, even where a particular conditional count is zero. First translate that sentence into predicates, then check the combined condition against actual ticket identifiers rather than trusting a plausible total.

## Slide 8

Now change the question. Suppose a ticket detail report also needs the number of events recorded for each request. We do need history, but we do not want the final result to repeat tickets. First group the event table by ticket_id.

WITH gives this intermediate query the name event_counts. Within this statement, we can read that name much like a table. It is not a newly stored table and it is not a separate command that you run and retain for the next query. The WITH clause and the following SELECT form one statement.

Run this example by itself and inspect its result. Ticket 1003 has an event_count of three. Ticket 1004 has one. On the current fixture, every ticket has a recorded event, so there are twelve intermediate rows. If a request had no event yet, it would have no row in this particular summary because the summary starts from events.

The useful property is at most one summary row per ticket identifier. That prepares us to join the summary to the tickets table without multiplying ticket rows. CTEs are a way to express and inspect stages of a query. They are not automatically cached tables or an assurance that a query will be faster; the benefit we are using here is clear reasoning about each intermediate result.

[Sources] PostgreSQL WITH queries: https://www.postgresql.org/docs/current/queries-with.html

## Slide 9

This version turns the intermediate result into a reusable report. Read it in two stages. Inside event_counts, GROUP BY produces one count per ticket with recorded history. Outside it, tickets is on the left of a LEFT JOIN. Every ticket is preserved, whether or not the summary has a match.

The selected ticket identifier and subject come from the request. The count comes from the summary. COALESCE uses the first non-null value. When a ticket has no matching history group, the summary columns are NULL, and COALESCE turns that absent count into zero recorded events.

Zero is justified here because we counted the rows in the available event table and found none for that ticket. We are not proving that nothing happened in the real world. We are also not filling an unknown source channel or unknown age with an invented number. The meaning of the measurement determines whether a default is defensible.

CREATE OR REPLACE VIEW saves the query definition under ticket_event_counts. A later SELECT reads its current result. We already studied views last week; the new work is arranging the query so each stage has the right unit. Next we will inspect the output count and a known record instead of treating successful view creation as proof that the report is right.

## Slide 10

We can test three separate properties of the view. COUNT star should be twelve because all starting tickets belong in this report. COUNT DISTINCT ticket_id should also be twelve because no ticket should appear twice. The sum of event_count should be twenty-one because that is how many event records exist in the starting fixture.

Those checks are useful together, but they still do not prove that each count belongs to the correct ticket. Swapping counts between requests could preserve every total. Therefore the second query checks known records. Ticket 1003 should have three events; ticket 1004 should have one. We can verify both by listing their rows in ticket_events.

This is how to make query testing concrete without creating a separate testing framework. State a property that follows from the question, write a small independent query, and compare it with records whose meaning you understand. If the fixture changes later, twelve is no longer a universal truth. The underlying properties remain: each intended ticket appears exactly once, and its count equals its recorded history.

For today's lab, the expected measures are different. You will check category totals and list the high-priority active identifiers. Do not simply copy the tests on this slide onto a report that has one row per category. A test must use the same unit as the result it is checking.

## Slide 11

Three report states can look similar on a dashboard but mean different things. A displayed zero event_count means the query found no recorded history rows for that included request. A NULL assignee_id means the included request has no assigned person. A missing ticket row means the request is outside this result entirely, whether intentionally or because a join or filter removed it.

The distinction is operational. A queue of work waiting for assignment should include the unassigned requests. Replacing their missing assignee with a guessed staff member would corrupt the meaning. Removing them with an inner join would hide the work. Likewise, showing a zero for a missing history count is only justified if the report's measurement is recorded events in this source.

The same care applies to categories with no active high-priority work. We want a visible category row with a zero conditional count. We do not want that category to disappear just because we applied the condition too early.

This is the bridge from the worked examples to the lab. Decide which rows define the report population first. Then define the measures within that population. Only after that should you choose whether an absent match becomes zero, remains NULL, or legitimately removes a result row. Those decisions should come from the question, not from an urge to make an output look complete.

## Slide 12

You will now build a report for the person deciding where staff attention is needed. Work individually with the same twelve-ticket fixture. The question is one row per category, with three measures: all tickets, active tickets, and active tickets whose priority is high or urgent.

Use the worked FILTER example as your starting point. The active vocabulary is new, open, and in_progress. For the third measure, both the active condition and the high-or-urgent condition must be true. Keep all five category rows, including categories where a measure is zero. This report does not need an event join because all the facts needed are in tickets.

Check the totals across the five rows. They should be twelve total tickets, seven active tickets, and two high-or-urgent active tickets on the supplied fixture. Then list those last two ticket identifiers with a simple SELECT. That independent check is more informative than repeatedly rerunning the grouped query.

Submit one SQL file, week_04_category_report.sql, in Brightspace. Put a short explanation in SQL comments: state what one result row represents and explain why counting a direct join to event history could overstate workload. The lab does not require a second report, screenshots, or a new cloud project. The later notebook sections belong to the second meeting; you do not need to rush through them now.

## Slide 13

Last meeting we made a report trustworthy by stating its row meaning and checking its counts. Today the report needs a different piece of history: one latest recorded event for each ticket. We still want one result row per request, not every event that ever happened to it.

This is a common pattern in application work. A dashboard might show the last update on an order, the most recent login for an account, or the latest reading from a device. The challenge is to select the complete row that meets an ordering rule, not merely the largest value in one column.

We will learn one window function, ROW_NUMBER, in small stages. First inspect the original events. Then give each ticket's events a position in newest-first order. Next keep position one in an outer query. Finally join that one-row history result to the population of tickets the report should include.

Keep the same data definitions: ticket status is the current state in tickets, while the event table is recorded history. A latest event can be an assignment rather than a status change. We will therefore show the event identifier, type, and time alongside the current ticket status instead of silently substituting one for the other. Our lab will reuse last week's view skill to give the final active-ticket report a stable name.

## Slide 14

MAX event_at answers the question, what is the greatest recorded timestamp in this group? It does not automatically carry along the event_type, note, or identifier from the row containing that timestamp. Applying MAX to each of those other columns separately would select their individual greatest values, not reconstruct one original event.

It is tempting to group by ticket_id and select a note next to MAX event_at. PostgreSQL correctly rejects an ungrouped note because several notes can belong to that ticket. Grouping by note instead changes the unit and may return several rows per ticket. Neither approach states which single history row we want.

Ticket 1003 makes this visible. Its greatest event time belongs to event 5007. The relevant row includes that event's type and status transition. We need to select that whole row according to an ordering rule.

A query could join back to a maximum timestamp, but tied timestamps could then return more than one event. We will use ROW_NUMBER so the tie rule is explicit. The concept is simple: within each ticket's history, order the records and label the first one. We will inspect those labels before using them to filter anything. A window function adds a calculated value to each input row; it does not initially collapse the history into one row.

## Slide 15

Here is the new expression. Read ROW_NUMBER as give this row a position. OVER describes which other rows it is being compared with and in what order. PARTITION BY ticket_id starts a separate numbering sequence for each ticket. It does not create database partitions or split the table across machines.

Inside OVER, ORDER BY event_at DESC puts the greatest timestamp first within each ticket. The secondary event_id DESC gives a deterministic rule when two timestamps are equal. Each event identifier is unique, so these two ordering terms together distinguish the rows in this fixture. The alias rn is simply the name we give the calculated position.

The final ORDER BY ticket_id, rn controls the order in which we display the complete result. That is separate from the ordering inside the window. A window ordering determines the calculation; it does not promise how every later reader will receive the output.

Run this query and inspect ticket 1003. You should still see all three of its event rows, now numbered one, two, and three. Across the whole fixture the result still has twenty-one rows. Nothing has been filtered yet. If that distinction is clear, the next step is only to name this result and select the rows whose position is one.

[Sources] PostgreSQL window-function tutorial: https://www.postgresql.org/docs/current/tutorial-window.html

## Slide 16

These rows show the calculation for two tickets. Ticket 1003's latest event, 5007, receives position one. Event 5006 receives two, and 5005 receives three. Ticket 1004 has only event 5008, so that row receives one in its own partition.

Compare the window result with GROUP BY. A grouping operation could reduce the three events for 1003 to one count. ROW_NUMBER instead keeps all three event rows and adds a label. This is why we can later keep the event's type, time, and other values together.

The numbering is a property of this query's ordering, not a new identifier stored in the table. If a later event is inserted, the numbering can change the next time we run the query. The event_id remains the stable identifier for the stored event.

Do not skip this intermediate result. It makes the next filter intelligible. The rows with rn equal to one are the candidates we want, one within each ticket's history. The other rows still exist in the database; the report will simply not show them. Our current fixture has an event for every ticket, but a robust ticket report should still handle a future request whose history has not arrived. That is why a LEFT JOIN will matter again after we select the ranked rows.

## Slide 17

We now use WITH exactly as we did for event counts. The inner query is named ranked_events. It selects event values and calculates rn. The outer SELECT can then refer to rn like any other column supplied by that intermediate result.

Why not put WHERE rn equals one in the same SELECT that defines rn? PostgreSQL evaluates that query's WHERE filtering before its window calculations. The ranking value is not yet available at that stage. An outer query makes the two operations explicit: calculate the ranking first, then filter its result.

On the supplied data, keeping rn equal to one gives twelve event rows. Each is the selected history row for a different ticket. Ticket 1003 now appears only with event 5007. The original event table still contains all twenty-one records.

A CTE is not the only way to write this; a subquery can express the same stages. Use the CTE here because we can name, run, and reason about the intermediate query. Remember that WITH and its final SELECT must run as one statement. Running only the second part later will not find a permanently stored ranked_events table. The next example will join this ranked history to the tickets population rather than assume that every possible ticket has history.

## Slide 18

The inner ranking query is unchanged. The outer query now starts from tickets, so the request population controls the report. We LEFT JOIN ranked_events on both the matching ticket identifier and rn equal to one.

Putting rn equal to one in the join condition is important. A ticket with no event has no matching ranked row, but a LEFT JOIN still preserves the ticket with NULL event columns. If we moved e.rn equals one into the outer WHERE clause, those unmatched rows would fail the condition and disappear. The filter's location changes the meaning.

The selected status comes from tickets. The event identifier, type, and time come from the one matched history row. That keeps the current request state and selected history facts distinct. On this fixture, every ticket has history and the query returns twelve rows. The design also states what will happen if a future request lacks history.

Read the query in three parts: rank the events within each ticket, preserve the intended ticket rows, and attach only the selected event. You are not expected to invent this syntax from memory. In the lab you will adapt this worked pattern to active tickets and give the result a view name. Before that, we will examine what our ordering rule means when timestamps tie.

## Slide 19

Imagine these two illustrative event rows for one ticket. Both have the same recorded timestamp. Ordering only by event_at does not specify which one receives position one. A repeatable report needs another ordering term if it must select exactly one row.

Our query uses the greater event_id when timestamps tie. This is deterministic because event identifiers are unique. It is a declared reporting rule, not proof that the event with the greater identifier happened later in the real world. Identifiers can be allocated before commit, and imported records can arrive in a different order from the events they describe.

For some applications, the correct rule would be to show both tied events or to use a trusted source sequence. That is a domain decision. In this class example, we document the event_id tie-break and test it, rather than leave PostgreSQL to choose an unspecified order.

The notebook contains a small, isolated equal-timestamp example. Changing its input order should not change which identifier wins when both ordering terms are present. That test checks determinism. It does not establish a business chronology that our data does not contain. This is another example of distinguishing what a successful computation proves from what someone might mistakenly infer from its label.

## Slide 20

Here is a boundary case that the starting twelve rows do not cover: a ticket is present but its event history is empty. Perhaps the import was partial or the application writes history through a delayed process. A report intended to show all tickets should reveal that gap, not hide the request.

The LEFT JOIN pattern preserves the ticket and leaves the selected event fields NULL. That result accurately says that no matching history row was found. We should not manufacture an event identifier or timestamp to make the output look finished.

Contrast this with yesterday's event count. There, zero recorded events was a meaningful count. Here, we want an actual event record. There is no record to select, so its fields remain NULL. The choice is driven by what the columns claim to represent.

For a boundary test, use a disposable fixture or a transaction that rolls back. Do not delete an existing request's history in a shared or valuable database merely to see what happens. The notebook demonstrates the missing-match logic without altering your permanent project. After the test, the main fixture should still contain twelve tickets and twenty-one events. Good tests target a small condition and leave the next exercise's starting state understandable.

## Slide 21

Once the SELECT returns the intended result, we can save its definition as a view. This is the same view concept from the previous week, applied to a more careful reporting query. CREATE VIEW does not turn the result into a backup or freeze the selected event forever.

The shortened example on this slide names the ranking itself as a reusable view. Reading that view still computes from the current visible event data. Each request's positions can change when a new event is committed. A separate reading query can then keep rn equal to one.

In your lab, the named interface will go one step further. active_ticket_latest_event will include the active ticket population and the selected history columns. It should have the five columns named in the assignment: ticket_id, status, event_id, event_type, and event_at. Keep the current ticket status distinct from an event's possible new_status.

Create the view only after you can run and explain the SELECT. If you are replacing an existing view, PostgreSQL's column-name, order, and type rules still apply. Do not remove a view used by other people to silence an error. In our disposable exercise, inspect the current definition and fix the intended interface. Then query the view and check identifiers, not just whether CREATE returned successfully.

## Slide 22

Suppose a latest-event report has exactly twelve distinct ticket identifiers. That confirms the population and uniqueness on this fixture, but it does not prove that the right event was selected for each ticket. A query that consistently picks the oldest event could pass those two checks.

Use a known multi-event ticket. For 1003, the latest recorded event is 5007. For 1004, the only event is 5008. Inspect their original event rows in chronological order before comparing with the report. This gives you an independent reason for the expected values.

The lab changes the population to active tickets, so its expected count is seven rather than twelve. Ticket 1003 is resolved and should not appear in that active report. Tickets 1004 and 1009 should remain, despite their missing assignees. These are different checks: inclusion follows ticket status, while event selection follows the history ordering rule.

Finally, check that no ticket identifier appears more than once. A count of seven alone can hide both a duplicate and a missing row. The compact query on this slide returns only duplicate identifiers. An empty result is what we expect for that specific property, not universal proof that the entire report is correct. The tests work together because each corresponds to a stated part of the report's contract.

## Slide 23

The second lab gives the queue a useful history summary. Adapt the worked ranking and LEFT JOIN query, and name the view metro_support.active_ticket_latest_event. Include only tickets whose current status is new, open, or in_progress. Include the five requested columns without adding a required assignee join.

Run your SELECT before saving the view so you can inspect its intermediate result. The event ranking still considers each ticket's recorded history. The active-ticket condition belongs to the ticket population in the outer query. Keep the rn condition in the LEFT JOIN so a ticket without history could still appear.

On the supplied fixture, the view should return seven unique ticket identifiers. Check 1004 with event 5008 and 1009 with event 5016. Then run the duplicate-identifier check and inspect at least one multi-event active ticket against its source history. If a result differs, identify whether the issue is the population, the ranking, or the join before changing several clauses at once.

Submit one SQL file, week_04_latest_event.sql. Include the view, your verification queries, and brief comments explaining the tie-break and the effect of moving rn equals one from ON into WHERE. No extra notebook or screenshot submission is needed. You can use the notebook as your workspace and save your own SQL from it. The goal is one report you can explain and rerun, not a large collection of unrelated query puzzles.

## Slide 24

We have now distinguished several kinds of correctness. The query must choose the intended population, combine relationships without unintended multiplication, select the intended history row, and expose columns whose meaning is clear. We checked those claims with counts and specific identifiers on a known fixture.

Real applications add another complication: other sessions can change data while a person is working. Imagine checking the active count in one statement and reading the active queue in a later statement. If another session resolves a request between those reads, the two results can differ even when both queries are written correctly.

This leads into next week's work on transactions and isolation. We will not solve concurrency by adding DISTINCT, or by assuming the database has lost a record. We will ask which changes each statement can see, where a transaction begins and ends, and which changes are kept after commit or discarded by rollback.

For today, keep the boundaries honest. Your report is tested against the supplied state and ordering rule. You have not proven that two separate reports run at different moments always describe the same snapshot. Save your SQL, finish the notebook cleanup when you no longer need its temporary database, and keep any project connection details private. The transferable skill is not one particular query: it is explaining exactly what a result means and how you checked it.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
