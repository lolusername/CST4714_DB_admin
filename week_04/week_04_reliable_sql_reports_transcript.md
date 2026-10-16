# Week 4: Reliable SQL Reports - Spoken Transcript

## Slide 1

Welcome to Week 4. Look at the line under the title: count requests, summarize histories, select the latest event. Those three verbs are the whole week.

Here is the question behind all of it. Last week we gave useful queries names with views, and we changed a schema safely. This week asks something different: does a report actually count the thing its reader thinks it counts? That sounds obvious, but a query can run without a single error and still hand someone a misleading number. PostgreSQL checks your syntax. It cannot check your business question. That part is our job.

We keep the same Metro Support data on purpose, so all of your attention goes to the reasoning instead of to learning a new domain.

On Day 1 we follow one ticket through its event history and see how joining that history can quietly inflate a request count. We name intermediate results with WITH, and we compute several carefully defined counts without losing categories that have zero matches. On Day 2 we learn exactly one window-function pattern, ROW_NUMBER, to pick one latest event per request. You do not need to memorize a list of window functions.

Both labs are individual, and each one is a single SQL file. The skill I care about is this: say what one result row means, show how your SQL keeps that meaning, and check the result against specific records.

## Slide 2

Before we write any reporting code, let's agree on the data, because every number this week comes from it. Look at the table. users, one row per person, eight rows. tickets, one row per request, twelve rows. ticket_events, one row per recorded event on a request, twenty-one rows. Nothing hidden, nothing bigger behind the scenes.

The users are residents, agents, a supervisor, and an analyst. Every ticket has a required requester and an optional assignee. Every event points back at the ticket whose history it describes.

Open the Week 4 notebook and run the introduction and setup before the Day 1 examples. It starts PostgreSQL and builds a disposable copy of the data, so you cannot hurt anything. You can run the same setup in your personal Supabase project or in PGlite instead. This week does not need the source_channel column we added last week, so a fresh copy is fine. And if you already have a working copy with your own work in it, do not reset it just because the week changed.

Now look at the line at the bottom. Seven tickets are active, and two of them, 1004 and 1009, have nobody assigned. Also peek at ticket 1003, which has three events, and 1004, which has one event and no assignee. Why bother? Because these few tickets teach us the difference between a request and a history row, and between a missing relationship and a missing request.

## Slide 3

Here is ticket 1003, a report of low water pressure. Look at the three rows. Event 5005, created, status open. Event 5006, status changed to in_progress. Event 5007, status changed to resolved. Three rows, in the order they happened.

How many requests is that? One. The resident submitted one ticket. The three history rows describe things that happened to it. So the real question is: what is your report counting? An event report might legitimately count all three. But a report of how many residents asked for help with water must not count this ticket three times.

Notice the second column. ticket_id repeats: 1003, 1003, 1003. Is that a duplicate problem? No. That is a foreign key doing its job, linking all three events to the same request. The event_id is what makes each row unique. So before anyone reaches for DELETE or DISTINCT to make the repetition go away, ask the question at the bottom of the slide: which fact does each row represent?

One more distinction that will matter on Day 2. The current status lives in tickets.status, and for 1003 that is resolved. The event history is a different thing. For today's backlog, use tickets.status. For the story of one request, read ticket_events. And not every event changes the status. An assignment event can leave the status exactly where it was.

## Slide 4

Let's watch the join do its work on that one ticket. Read the query with me. FROM tickets, alias t. JOIN ticket_events, alias e. ON e.ticket_id equals t.ticket_id. That ON line is the relationship, and we state it out loud; PostgreSQL never guesses it from similar column names. WHERE keeps ticket 1003. ORDER BY event_at, event_id lays the history out in time order.

Now run it. Three rows. Look at which columns repeat. ticket_id, subject, and status are the same in every row, because they belong to the request, and the request matched three events. The event_id changes: 5005, 5006, 5007. We did not create three tickets. We produced three ticket-event pairs, which is exactly what the line under the code says.

Why spend a whole slide on three rows? Because if you can explain every row of this small result, you are ready to reason about an aggregate built on top of it. If you can't, stay here. Do not hide a result you don't understand behind GROUP BY.

The prefixes t and e are not decoration either. Both tables have a ticket_id column, and the prefix tells PostgreSQL which one you mean. On the next slide we remove the WHERE filter and count these pairs across every ticket, and you will see a number that looks right and isn't.

## Slide 5

Here is the trap. Imagine a dashboard query that looks completely reasonable. Join tickets to events, group by category, count star, and call the column requests. It runs. No error. Now look at the table under the code.

Water says 5. But water has only two requests. Where does 5 come from? Ticket 1003 brings three history rows and ticket 1008 brings two. Three plus two is five. Across all five categories the counts add up to 21, which is the number of events, while the tickets table has 12 rows. The label says requests. The unit is ticket-event pairs.

And PostgreSQL did nothing wrong. It counted exactly the rows we handed it. The bug is in the meaning, not the syntax, and that is why this bug survives so easily.

So how do we fix it? It depends on the question. If the report only needs ticket facts, like category and request counts, don't join events at all. Read tickets. If the report really needs something from the history, summarize the history down to one row per ticket first, and then join.

You might think: just use COUNT DISTINCT ticket_id. That does answer some distinct-ticket questions. But it is not a general repair. It won't fix a sum that got multiplied, and it won't bring back rows a join removed. The reliable first move is to say what one row should mean, look at the intermediate rows, and then pick the join and the aggregate that match.

## Slide 6

So let's report straight from tickets, and be precise about each count. Look at the three expressions in the query, because they mean three different things.

count star counts rows: every ticket, 12. count of assignee_id counts only rows where assignee_id is not NULL, so it skips the unassigned tickets: 10. count DISTINCT assignee_id counts the different non-null people: 2. Twelve, ten, two. Those are not three competing answers to one question. They answer three different questions, and your column name should say which one.

Now look at the comment line at the bottom: count star FILTER WHERE status equals resolved. FILTER lets one aggregate count only the rows that meet its own condition, while every other aggregate in the same SELECT still sees the whole group.

Why not just write WHERE status equals resolved at the top? Because a top-level WHERE throws away every non-resolved ticket before grouping even starts. Then any category with no resolved work disappears from the report entirely. We want that category to show up with a zero. A zero tells the manager something. A missing row tells them nothing, or worse, makes them think the category doesn't exist.

Read FILTER from the inside out. Is this row resolved? If yes, count it here. If no, leave it out of this one count only. Your lab will combine two conditions with AND, but the idea stays exactly the same.

[Sources] PostgreSQL aggregate-expression documentation: https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-AGGREGATES

## Slide 7

Here is the complete pattern, and it is the one your lab adapts. One SELECT, two aggregates, both reading the same category group. total_tickets counts every request in the category. resolved_tickets counts only the resolved ones. GROUP BY category gives us one row per category.

Read the table with me. Parks, 2 and 0. Sanitation, 3 and 1. Streetlight, 3 and 1. Transportation, 2 and 0. Water, 2 and 2. Notice that parks and transportation are still here, with a zero. That is FILTER doing its job; a top-level WHERE would have deleted those rows.

Now check it, and not by rerunning the same query. The first column adds to 12, which matches the tickets table. The second column adds to 4. Can we confirm 4 a different way? Yes. List the resolved tickets directly and you get 1003, 1005, 1008, and 1012. Four IDs. Two different routes, same answer. That is a real check.

Also notice what we did not do. We never joined events, because neither measure needs history. Leaving out a join you don't need is often the most important decision in a report.

In your lab you will count active tickets, meaning new, open, or in_progress, and active tickets whose priority is high or urgent. Keep all five categories, zeros included. Write the conditions in plain English first, then check them against real ticket IDs instead of trusting a total that merely looks plausible.

## Slide 8

Now a different question, one that genuinely does need history. Suppose a ticket detail report should show how many events each request has. We need the events, but we don't want the tickets to multiply. So we summarize first.

Look at the query. WITH event_counts AS, and inside the parentheses, a plain GROUP BY on ticket_events that counts rows per ticket_id. WITH gives that inner result a name. Below it, we select from event_counts as if it were a table.

But it isn't a table. Nothing is stored. The WITH clause and the SELECT under it are one statement. If you run only the bottom line by itself later, PostgreSQL won't know what event_counts is.

Run it and look at the result. Ticket 1003 has 3 events. Ticket 1004 has 1. In this data every ticket has at least one event, so we get twelve rows. But think about a ticket with no events yet. It would have no row here at all, because this summary starts from events, not from tickets. Hold on to that; it matters on the next slide.

The property we care about is the one on the slide: at most one row per ticket_id. That is what makes the next join safe. And a word on why we use CTEs. They are not a speed trick and they are not cached tables. We use them because each stage gets a name that you can run and inspect on its own.

[Sources] PostgreSQL WITH queries: https://www.postgresql.org/docs/current/queries-with.html

## Slide 9

Now we put the two stages together and save the result. Read it in two parts.

Inside, event_counts is exactly what we just ran: one count per ticket that has history. Outside, tickets is on the left of a LEFT JOIN. Why LEFT? Because this report is about tickets, so tickets decide which rows exist. Every ticket stays, whether or not the summary has a match for it. That closes the gap I pointed out a minute ago.

The ticket_id and subject come from tickets. The count comes from the summary. And look at COALESCE of e.event_count comma zero. When a ticket has no history group, the joined columns are NULL. COALESCE takes the first non-null value, so that NULL becomes zero.

Is zero honest here? Yes, and the reason matters. We counted the rows in the event table and found none for that ticket. Zero recorded events is a true statement about our data. It is not a claim that nothing happened in the real world. And it would be wrong to do the same thing to an unknown source channel or an unknown age; there, a made-up number would be a lie. What the column measures decides whether a default is defensible.

CREATE OR REPLACE VIEW saves the definition as ticket_event_counts. You know views from last week. What is new is arranging each stage so it has the right unit. And a view that was created successfully proves nothing yet. Next, we test it.

## Slide 10

Here is how we test it. Three properties, one small query. Look at the first query.

count star should be 12, because every starting ticket belongs in this report. count DISTINCT ticket_id should also be 12, because no ticket should appear twice. And the sum of event_count should be 21, because that is how many event rows exist. The line at the bottom shows exactly that: 12 rows, 12 ticket IDs, 21 events.

Are we done? No. Those totals could all be right while the counts are attached to the wrong tickets. If two tickets swapped their counts, every total would still match. So the second query checks known records. Ticket 1003 should show 3. Ticket 1004 should show 1. We know those values independently, because we looked at their rows in ticket_events earlier.

This is what query testing looks like without any testing framework. State a property that follows from the question. Write a small, independent query. Compare against records you understand. If the data changes later, 12 stops being the right number, but the properties stay: each intended ticket appears exactly once, and its count matches its recorded history.

One warning for today's lab. Don't copy these exact checks onto your category report. Your report has one row per category, not one row per ticket, so your checks are the category totals and a list of the high-priority active IDs. A test has to use the same unit as the result it is checking.

## Slide 11

These three states can look alike on a dashboard, and they mean different things. Look at the table.

event_count equals zero: the ticket is in the report, and we found no event rows for it. assignee_id IS NULL: the ticket is in the report, and nobody is assigned to it. Ticket absent from the output: the ticket isn't in this result at all, either on purpose or because a join or a filter removed it.

Why does this matter in practice? Think of the queue of work waiting for assignment. It has to include tickets 1004 and 1009, the unassigned ones. If you filled in their NULL assignee with a guessed staff member, you would corrupt what the data means. If an inner join to the staff dropped them, the work would vanish from the queue. The same goes for zero: showing zero events is only fair because the measure is recorded events in this source.

In your lab, a category with no active high-priority work should appear with a zero in that column. It should not disappear because a condition was applied too early.

So here is the order of decisions, which is the line at the bottom of the slide. First decide which rows make up the report population. Then define the measures inside that population. Only then decide whether a missing match becomes zero, stays NULL, or removes a row. Let the question decide, not the urge to make output look complete.

## Slide 12

Your turn. Picture the operations manager deciding where staff attention is needed. They want one row per category, with three measures: all tickets, active tickets, and active tickets with high or urgent priority. Work individually, on the same twelve-ticket data.

Start from the worked FILTER example on slide 7. Active means new, open, or in_progress. For the third measure, both conditions must be true at once: the ticket is active, and its priority is high or urgent. That is an AND inside the FILTER. Keep all five categories, including the zeros. And you don't need events at all; everything you need is in tickets.

Now check it, the way we practiced. Look at the verify box. Your three columns should add up to 12, 7, and 2. Then, separately, write a plain SELECT that lists the two high-or-urgent active ticket IDs. That independent list tells you far more than rerunning the grouped query and staring at it.

Submit one file in Brightspace: week_04_category_report.sql. Put your report and your independent check in it, plus a short explanation in SQL comments, two or three sentences. Say what one result row represents, and why counting a direct join to the event history could overstate the workload. No screenshots, no separate report, no new cloud project. And the later notebook sections belong to Day 2, so you don't need to rush through them now.

## Slide 13

Welcome back. On Day 1 we made a report trustworthy by saying what each row means and checking its counts. Today the report needs a different piece of history: the latest recorded event for each ticket. And we still want one row per request, not every event that ever happened to it.

This shows up everywhere. The last update on an order. The most recent login for an account. The latest reading from a sensor. Here is what makes it tricky: we want the whole row that wins an ordering rule, with its ID, its type, and its time, not just the largest value in one column.

So we learn one window function, ROW_NUMBER, and we build it in small steps. First, look at the raw events. Second, number each ticket's events newest first. Third, keep position one in an outer query. Fourth, join that one-row-per-ticket result to the tickets the report should include. You will see each intermediate result before we combine anything.

Keep the definitions from Day 1. Ticket status is the current state, stored in tickets. The event table is history. The latest event might be an assignment rather than a status change, so we show the event's ID, type, and time next to the current status instead of swapping one for the other.

Open the same Week 4 notebook at the Day 2 heading after setup. Your lab reuses last week's view skill to give the final report a stable name.

## Slide 14

The first idea most people reach for is MAX. Look at the query: select ticket_id and max of event_at, grouped by ticket. It works, and it answers exactly one question: what is the latest timestamp for each ticket?

What it does not do is bring along the rest of that row. Look at the bottom line on the slide. If you also ask for MAX of note, PostgreSQL finds the greatest note, which could come from a completely different event. Each MAX is computed on its own column. You don't get one original event back; you get a mix.

You might try putting a plain note column next to MAX event_at. PostgreSQL rejects that, correctly, because a ticket has several notes and you didn't say which one. Adding note to GROUP BY instead changes the unit, and now you can get several rows per ticket. Neither approach says which single row you want.

Ticket 1003 makes this concrete. Its latest time belongs to event 5007, and we want that event's type and status change, together, as one row.

You could join back to the maximum timestamp. But if two events share a timestamp, you get both back, and now the ticket appears twice. So we use ROW_NUMBER, which makes the tie rule explicit. Keep one more thing in mind: a window function adds a value to each row. It does not collapse the history the way GROUP BY does.

## Slide 15

Here is the new expression. Read ROW_NUMBER as: give this row a position. OVER says which rows it is being compared with, and in what order.

Look at the two lines inside OVER. PARTITION BY ticket_id starts a separate count for each ticket, so the numbering restarts at 1 for every ticket. To be clear, this has nothing to do with table partitioning or splitting data across machines. It is just the grouping for the numbering.

ORDER BY event_at DESC, event_id DESC decides who gets number 1. Newest timestamp first. And if two events have the same timestamp, the larger event_id wins. Event IDs are unique, so together those two terms always pick exactly one row. rn is just the name we give the position.

Now look at the last line: ORDER BY ticket_id, rn. That one is different. It only controls how the final result is displayed. The ORDER BY inside OVER decides the calculation. The one at the bottom decides the display. They do different jobs, and here you need both.

Run it and find ticket 1003. All three of its events are still there, now numbered 1, 2, and 3. And the whole result still has 21 rows. Nothing has been filtered yet. That is the point of this step: we look at the labels before we trust them. If that is clear, the next step is just naming this result and keeping the rows where rn is 1.

[Sources] PostgreSQL window-function tutorial: https://www.postgresql.org/docs/current/tutorial-window.html

## Slide 16

Let's zoom in on the labels for two tickets. Look at the table. Ticket 1003: event 5007 gets position 1, 5006 gets 2, and 5005 gets 3. Ticket 1004 has only one event, 5008, so it gets 1 in its own partition. The last column shows which rows we will keep later: the ones in position 1.

Compare that with GROUP BY. GROUP BY would squash ticket 1003's three events into one row, a count or a max. ROW_NUMBER keeps all three rows and just adds a number to each. That is the whole reason it works for us: because the original rows survive, the event's type and time stay together with its ID.

One caution. The rn number is not stored anywhere. It is a property of this query and this ordering, not a new identifier. If a newer event is added to ticket 1003 later, it gets position 1 the next time you run the query, and 5007 slides down to 2. The stable identifier is still event_id.

And look at the line at the bottom: the ranking query still returns all 21 event rows. Don't skip this intermediate look. It is what makes the next filter make sense.

One more thing to keep in mind. In our data every ticket has at least one event. But a robust report should still handle a future ticket whose history hasn't arrived yet. That is why LEFT JOIN comes back once we have picked the ranked rows.

## Slide 17

Now we keep only position 1. Look at the query. It is the same WITH pattern we used for event counts on Day 1. The ranking query goes inside, under the name ranked_events. The outer SELECT reads from it and says WHERE rn equals 1.

Why the extra layer? Why not put WHERE rn equals 1 in the same SELECT that calculates rn? Because of the order PostgreSQL does things. Inside one query, the WHERE filter runs before the window function is calculated. At that moment rn doesn't exist yet. So we calculate the ranking in one query, and filter it in the query around it. Two steps, written as two steps.

Run it. Twelve rows, one per ticket, each one that ticket's selected event. Ticket 1003 now shows only event 5007. And the event table itself is untouched; it still has all 21 records. That is the line at the bottom of the slide: first number the rows, then keep position 1, and the stored history doesn't change.

You could write this with a subquery instead of a CTE, and it would do the same thing. I use the CTE because you can name the inner step, run it alone, and look at it. Just remember that WITH and its SELECT run together as one statement. ranked_events is not saved anywhere. Next, we join this to the tickets, instead of assuming every ticket has history.

## Slide 18

Here is the full pattern, and your lab adapts it. The ranking inside the WITH is unchanged. What is new is the outer query. It now starts FROM tickets, so the tickets decide which rows the report has. Then we LEFT JOIN ranked_events.

Look closely at the ON line: e.ticket_id equals t.ticket_id AND e.rn equals 1. The rn condition sits inside the join condition, and that placement is the whole lesson of this slide. Here is why. Picture a ticket with no events. It has no ranked row to match. A LEFT JOIN keeps it anyway, with NULL in the event columns. Now move e.rn equals 1 down into a WHERE clause. For that ticket, rn is NULL, NULL equals 1 is not true, and the ticket is filtered out. It simply disappears. Same words, different location, different meaning.

Notice where each column comes from. t.status is the ticket's current status. event_id, event_type, and event_at come from the one matched history row. Two different facts, kept apart.

On our data every ticket has history, so we get twelve rows. But the query also says clearly what will happen to a future ticket with none.

Read it in three parts: rank the events within each ticket, keep the tickets you want, attach only the selected event. You don't need to invent this from memory. In the lab you will adapt it to active tickets and save it as a view. First, though, what happens when timestamps tie?

## Slide 19

Here are two illustrative events for one ticket, 7001 and 7002. Look at the recorded time column. They are identical, to the second. If we ordered only by event_at, which one is newest? PostgreSQL doesn't promise either answer. You might get one today and the other tomorrow, and the report would flicker.

Our ordering rule settles it: ORDER BY event_at DESC, event_id DESC. When the times tie, the larger event_id wins. So 7002 gets position 1 and 7001 gets position 2. That is deterministic, because event IDs are unique.

But be careful about what that proves. Read the second line in the box: deterministic selection is not proof of real-world arrival order. A larger ID does not mean the event happened later. IDs can be handed out before a transaction commits, and imported records can arrive in a different order from the events they describe. Our rule is a reporting decision that we declare and test. It is not a statement about history.

In some applications the right answer is different. Maybe you show both tied events, or you use a trusted sequence number from the source system. That is a business decision, not a SQL one.

The notebook has a small equal-timestamp demonstration: two invented rows in a temporary table, inside a block that rolls back, so the real twenty-one events never change. Run it and watch the higher ID take position 1. That checks determinism. It does not create a chronology our data doesn't have.

## Slide 20

Here is a boundary case our twelve starting tickets don't cover: a ticket exists, but it has no events at all. Maybe an import was partial, or the application writes history a little later through a delayed process. A report that claims to show all tickets should reveal that gap, not hide the ticket.

Look at the table. When events exist, the LEFT JOIN gives the ticket plus its one selected event, while the shortcut of joining every event would repeat the ticket. When no event is recorded, the LEFT JOIN gives the ticket with NULL event fields, while the shortcut filters the unmatched ticket away entirely.

Those NULLs are honest. They say we found no matching history row. Don't manufacture an event ID or timestamp so the output looks finished.

Compare this with the event count from Day 1. There, zero was a true count of recorded events. Here we are asking for an actual event record, and there is no record to pick, so its fields stay NULL. What the column claims to be decides the answer.

To be clear, the notebook does not build a zero-event ticket for you. It explains this case in words, because the starting data has none. If you want to try it yourself, use a disposable copy or a transaction that you roll back. Never delete real history in a shared or valuable database just to see what happens. Afterward the data should still have twelve tickets and twenty-one events.

## Slide 21

Once the SELECT returns what we want, we can give it a name with a view. This is the same view idea from last week, applied to a more careful query.

Look at the example. CREATE OR REPLACE VIEW metro_support.ranked_ticket_events saves the ranking query: every event, with its rn. Then a separate SELECT reads from the view and keeps rn equal to 1.

Now the line at the bottom, because people get this wrong. A view stores the query, not the rows. It is not a backup, and it doesn't freeze today's answer. Every time someone reads it, PostgreSQL computes it again from the current data. So if a new event is committed for a ticket, the next read can number that event 1. That is exactly what you want from a live report.

Your lab view goes one step further. It is called active_ticket_latest_event, and it holds the active ticket population and the selected event together. It needs the five columns named in the assignment: ticket_id, status, event_id, event_type, and event_at. And status there means the ticket's current status, not an event's new_status.

Two practical habits. Create the view only after you can run and explain the SELECT. And if CREATE OR REPLACE complains because you changed a column's name, order, or type, read the error and fix your definition. Don't drop a view other people depend on just to silence the error. Then query the view and check IDs, not just that CREATE succeeded.

## Slide 22

How do we know the latest-event report is right? Here is a trap. Suppose it has exactly twelve distinct ticket IDs. That shows the population and the uniqueness are right. It does not show the right event was picked. A query that always picked the oldest event would pass both of those checks.

So check selected rows against tickets you know. For 1003, the latest event is 5007. For 1004, the only event is 5008. Read their original rows in time order first, so you have your own reason for the expected answer.

Now your lab. It changes the population to active tickets, so the expected count is 7, not 12. Look at the table on the slide. Seven distinct tickets, including 1004 and 1009. Ticket 1003 is resolved, so it should not appear at all. And the selected events for those two: 1004 gets 5008, and 1009 gets 5016. Notice these are two different kinds of check. Which tickets appear follows the current status. Which event is attached follows the ordering rule.

Last, look at the query on the slide. Group the view by ticket_id and keep only groups with a count greater than 1. That lists any duplicate tickets. Why bother if the count is already 7? Because one duplicate plus one missing ticket also adds up to 7. We expect no rows, and an empty result proves this one property, not the whole report.

## Slide 23

Second lab. The active queue gets a history summary. Look at the first box: create metro_support.active_ticket_latest_event using the worked ROW_NUMBER plus LEFT JOIN pattern. Include only tickets whose current status is new, open, or in_progress. Use the five columns: ticket_id, status, event_id, event_type, event_at. And don't add a required join to an assignee, because that would drop 1004 and 1009.

Where do the conditions go? The ranking still looks at every ticket's full history. The active condition belongs to the tickets in the outer query. And e.rn equals 1 stays in the LEFT JOIN's ON clause, so a ticket with no history could still appear. Run your SELECT and look at it before you wrap it in CREATE OR REPLACE VIEW.

Then check, as the second box says. Seven unique ticket IDs. 1004 with event 5008, and 1009 with event 5016. Run the duplicate check from the last slide. And pick one active ticket with several events and compare its selected event against its source history yourself. If something doesn't match, figure out whether the problem is the population, the ranking, or the join before you change several things at once.

Submit one file in Brightspace: week_04_latest_event.sql. It holds the view, your verification queries, and short comments explaining the tie-break and what would happen to a ticket with no events if e.rn equals 1 moved from ON into WHERE. No screenshots, no notebook. Use the notebook as your workspace, and save your own SQL out of it.

## Slide 24

Let's step back. This week we separated kinds of correctness. Choose the right population. Combine tables without accidentally multiplying rows. Pick the intended history row. Expose columns whose meaning is clear. And we checked every one of those claims with counts and specific IDs on data we know.

Now look at the two lines on the slide. Query correctness asks which rows this statement should return. That is what we did this week. Transaction behavior asks which committed changes the statement can actually see. That is next week.

Why does that matter? Real databases change while people use them. Imagine you check the active count in one statement, and then read the active queue in a second statement. If someone resolves a ticket in between, your two results disagree, even though both queries are written correctly. DISTINCT won't fix that, and no record was lost.

Next week we cover transactions, visibility, and blocking: which changes each statement can see, where a transaction starts and ends, and what is kept after COMMIT or thrown away by ROLLBACK.

For today, be honest about what you proved. Your report was tested against this data and this ordering rule. You haven't proven that two reports run at different moments describe the same snapshot. Save your SQL, and clean up only the notebook database made for this exercise. Keep your project connection details private. The skill that transfers is being able to say what a result means and how you checked it.

## Slide 25

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: What does one row mean after a join? (1:16); Counting workload, including zero (1:28); A view stores a query, not rows (1:14). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 4 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
