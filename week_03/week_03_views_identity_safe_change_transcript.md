# Week 3: Views, Identity, and Safe Change - Spoken Transcript

## Slide 1

Welcome to Week 3. Last week was the SQL review. You wrote selects, joins, and aggregates against the Metro Support tickets. This week we stop only reading the database and start changing it, carefully. The idea that runs through both days is simple: a command can succeed and the application can still get the wrong answer. A green "success" message is not the finish line.

On Day 1 we give a useful query a stable name. The support staff need a list of active tickets, and every screen should not have to reinvent what "active" means. So we build an ordinary view, read from it, and then change its columns on purpose. We also build a small table whose IDs come from a sequence, and we cancel one insert to see why an ID and a row count are different things.

On Day 2 the organization wants to record whether each request came in through the web, a phone call, or the mobile app. That sounds like one new column. But the old tickets never recorded it, and older application code does not send it yet. We will handle both problems instead of pretending ALTER TABLE makes them go away.

You work individually in your own database. Each day you submit one SQL file: week_03_views_identity.sql and week_03_safe_migration.sql. Your comments in that file say what your change means, including what the data cannot tell us.

## Slide 2

Before we write a view, we need a shared picture of what it reads. Metro Support is a fictional public-service help desk. A resident reports a broken streetlight or a missed collection, someone on staff may get assigned to it, and the system keeps a history. None of these people are real. The data is small and synthetic on purpose, so you can check any answer by looking at the actual rows.

Look at the middle column of the table, "one row represents." That is the most important column on the slide. The users table has eight rows, and each row is one person, a resident or a staff member, so a user is not automatically an agent. The tickets table has twelve rows, and each one is one support request. Not one update, not one person. The ticket_events table has twenty-one rows, and each one is one event in a request's history.

That is why the counts differ. Twenty-one events does not mean twenty-one requests. Several events belong to the same ticket.

Now the line at the bottom. We define the active queue using the current status in tickets: new, open, or in_progress. In the starting data, seven tickets are active. Keep that seven in your head, because we will check it again and again this week. Knowing what a row means always comes before choosing the SQL.

[Sources] Original Metro Support synthetic CSVs and postgres_setup.sql, supplied with this week.

## Slide 3

Here is a distinction that will decide which join you write in the lab. Look at the first row. Ticket 1001, the streetlight. Its requester_id is 101, which points to Requester 101 in the users table. Its assignee_id is 201, which points to Agent 201, in that same users table. Same kind of number, same table, but two completely different relationships. Requester 101 reported the problem. Agent 201 is handling it. So a join has to say which relationship you mean.

Now the second row. Ticket 1004, the broken bench. Requester 104 reported it. The assignee is NULL, because nobody has been assigned yet. NULL is not some other staff ID, and it is not a zero you can match to a user. It means the assignment is missing.

Read the note at the bottom. Both columns refer to users.user_id, but only the assignment is optional. The schema requires a requester. It allows a missing assignee.

Why does that matter? Today's demonstration joins tickets to their requester, and every ticket has one, so an ordinary inner join loses nothing. Your lab joins tickets to their assignee. If you use an inner join there, ticket 1004 disappears, and so does the other unassigned ticket, 1009. A LEFT JOIN keeps the ticket and shows the missing name. And an unassigned ticket is exactly the work a queue must not hide.

## Slide 4

You have three ways to run this week's PostgreSQL, and you only need one.

The first row is the Colab notebook. It starts a throwaway PostgreSQL database inside the notebook runtime. It does not connect to Supabase and it needs no cloud password. It walks you through setup, loads the full dataset, and gives you marked workspaces for your SQL. One warning: a Colab runtime does not last between class days. Save a copy of the notebook in your Drive so your edits are kept, and save your SQL as you go.

The second row is your personal Supabase project. Use the SQL Editor, not the Table Editor. The third is the PGlite playground, which runs PostgreSQL in your browser and keeps its data in that browser profile. Do not use last week's DuckDB notebook. This lesson needs PostgreSQL's identity columns and catalog.

In Supabase or PGlite you load the data with postgres_setup.sql. That is a reset script. Its very first command drops the old practice schema, so never run it over work you want to keep.

After setup, run the query on the slide, SELECT current_database, current_user. It tells you which database and role actually answered. And read the yellow line: load once, and keep your Day 1 view for Day 2. The second lab changes the view and table you build in the first, so a reset between them throws away the thing you are about to change.

## Slide 5

Before we build anything, let's make sure everybody has the same data. Two queries.

The first one stacks three counts with UNION ALL, one row per table, each with a name so you know which count is which. You should get eight users, twelve tickets, and twenty-one events. Those are counts of stored rows, not columns and not active work. If your numbers are different, stop. Fix your setup first. Otherwise you will spend an hour debugging a query that was never wrong.

The second query reads one ticket, 1004. We picked it because its missing assignee matters in the lab. Look at the expected line at the bottom: requester 104, assignee NULL, status new. You can open tickets.csv and find the same values. Having a second, independent look at the source data is what lets you say why a later result is right or wrong, instead of just hoping.

If you are in the Supabase SQL Editor, it only shows the result of the last statement in a run. So run each of these SELECTs on its own if you want to see both.

Notice that every table name starts with metro_support and a dot. That is the schema, a namespace inside the database. Writing it out means we do not depend on whatever search path your editor tab happens to have. It is not your cloud project name, and it does not connect you to anything by itself.

## Slide 6

Three kinds of object on this slide, and the middle column is the one to read: what PostgreSQL actually keeps.

The first row is the base table. Our tickets table keeps the actual ticket rows. A SELECT asks PostgreSQL to produce a result from them, and your columns and your filter decide what comes back.

The second row is an ordinary view. It keeps a SELECT definition under a name. That is all. When someone queries the view, PostgreSQL uses that definition to build the result from whatever data is visible right now. Why is that useful for us? Because the definition of "active" lives in one place. We do not copy the same WHERE clause into five reports and then watch them drift apart.

Read the line at the bottom. Suppose ticket 1001 gets resolved, and that change is committed. The next query against our active view simply stops returning 1001. Nobody deletes it from the view. The filter just evaluates differently against the current data.

The third row is a materialized view, which is a different tool. It keeps result rows that were computed earlier. That can help when the calculation is expensive, but those rows sit there until someone refreshes them. A result can be fast and still be too old to use.

Today we only use ordinary views. A view does not make a query faster on its own, and its name does not make anything secure. Those are separate questions.

## Slide 7

Here is a complete view definition. Let's read it top to bottom.

CREATE OR REPLACE VIEW gives the object its name, metro_support.active_ticket_summary. Everything after AS is the SELECT that defines the result. If the view does not exist yet, PostgreSQL creates it. Replacing an existing one has some rules, and we will get to those in two slides.

Read the SELECT list first. Ticket ID, subject, priority, and the requester's display name. The letters t and u are aliases for tickets and users, so every column says where it comes from. And AS requester_name gives the output column a name that says which person this is. Not just "name." The requester's name.

Now the join, on requester_id. Look at the box on the right. Every ticket has one required requester, and user_id is the primary key of users, so the join finds exactly one person per ticket and never multiplies a ticket into two rows. The WHERE clause keeps our three active statuses.

Now the box at the bottom. Running CREATE saves the definition. It does not print seven tickets. You read the results with a separate SELECT, and that is the next slide.

And the middle box is your warning for the lab. The lab joins the assigned agent instead, and assignment is optional. An inner join on assignee_id would quietly drop the unassigned tickets. That relationship needs a LEFT JOIN. The meaning of the relationship picks the join.

## Slide 8

Now we read through the name we just created. Look at the FROM line. It says active_ticket_summary. We do not repeat the tickets-to-users join, and we do not repeat the status filter. That is the whole point of the view. And notice we only ask for two of its four columns. A view defines an interface, and the caller can still pick a narrower result from it.

Here is the result. Seven rows: 1001, 1002, 1004, 1006, 1007, 1009, and 1011. Seven, the same number we saw on the data slide. Now look down the requester column. Requester 101 shows up twice, on 1001 and 1009. Requester 102 is on 1002 and 1006. Requester 103 is on 1007 and 1011. Those are not duplicate rows. Each row is a ticket, and one person can open more than one ticket. The ticket ID is what tells those requests apart.

Read the note at the bottom right. ORDER BY ticket_id is in the reading query because we want a predictable order. If a query happened to come back in some order last time, that is not a promise about next time. If you need an order, ask for it.

One last habit for your own view. Check the IDs, not just the count. A count of seven cannot tell you that the right seven survived the join. In the lab, the two unassigned IDs, 1004 and 1009, are the ones to look for.

## Slide 9

Once other queries use a view, its columns become a contract. Look at the first column of the table. The lab's view starts with five columns in this order: ticket_id, subject, status, priority, opened_at. Some other report may already depend on exactly that shape.

Here is the rule. CREATE OR REPLACE VIEW has to keep the existing column names, their order, and their data types. It lets you add new columns at the end. So in the lab, assignee_name goes last, after opened_at. Do not slip it in between two existing columns, and do not rename an old one. PostgreSQL will usually refuse, and even if it did not, you would be breaking whoever reads that view. If you truly need a different shape, you make a new view with a new name and move callers over.

Now the subtle part, in the box about SELECT star. When you create a view with SELECT star, PostgreSQL expands the star right then, into the columns that exist at that moment. If someone later adds a column to the table, the existing view does not grow. But the next time somebody reruns that script, it suddenly does. That is how a sensitive new column ends up exposed in a report by accident. Writing the columns out explicitly makes the interface something a person can review.

The textbook's example uses a separate name, chapter4_active_queue, so reading along cannot overwrite your lab view.

[Sources]
- PostgreSQL 15, CREATE VIEW: https://www.postgresql.org/docs/15/sql-createview.html

## Slide 10

Before we change anything, let's ask where our commands are actually running. This small query answers that.

current_database tells you which PostgreSQL database you are connected to. current_user tells you which role you are acting as right now. current_schema is the first schema in your search path, and SHOW search_path prints the whole path PostgreSQL uses to find a table when you do not write a schema name.

Look at the first box on the right. current_user is a database role, an actor that gets privileges. It has nothing to do with the identity column we build on the next slide. That one is a generated number that tells one row from another. Same everyday word, "identity," two completely different mechanisms. I want you to keep them apart.

Your results will not match mine. Your hosted project has different names and roles, and that is fine. The useful question is not "do my values match the slide." It is "am I in the practice database I meant to be in."

That is also why we write metro_support.tickets. The part before the dot is the schema, the part after it is the table. We never rely on an editor tab's search path to guess.

One more thing. A query that works in an administrator's SQL editor proves nothing about what an application role can do. We test permissions as specific roles in Week 6. Today, when a result surprises you, check this context first.

## Slide 11

Now the other kind of identity. This demonstration table stores notes about database changes. It is deliberately separate from tickets, so we can study how IDs are handed out without touching real ticket keys. It is also separate from your lab's table, change_notes, so my demonstration and your experiment can sit side by side.

Read the first column. note_id is a bigint, a whole number with a very large range. GENERATED BY DEFAULT AS IDENTITY means: if an insert leaves this column out, PostgreSQL gets the next number from a sequence attached to the column. The words BY DEFAULT also mean a caller is allowed to supply its own value. That is handy for imports, but it needs care, because a hand-typed value can collide with one the sequence hands out later.

PRIMARY KEY is a separate clause with a separate job. It makes the ID unique and not null. Generating a number and enforcing uniqueness work together here, but you should be able to say which clause does which.

change_name is required text. created_at is a timestamp with time zone, and its default fills in now. So an insert can name only change_name and let the database fill in the rest.

Look at the bottom of the slide. Create this table once. If it already exists from an earlier run, the numbers will not start at one again. That is a different starting state, not a bug.

## Slide 12

This batch is three separate transactions, and each one ends with a decision we make on purpose.

The first one inserts "Initial view" and commits. RETURNING note_id asks PostgreSQL to show us the number that insert received, so we do not have to guess. The second inserts "Cancelled change." It also gets a number. Then we roll it back, so the row is gone. The third inserts "Approved revision" and commits.

Look at the line at the bottom. On a freshly created table, those three RETURNING results are one, two, and three. Hold on to that, because the next slide is about what is left in the table.

Why the explicit BEGIN and COMMIT around the first insert? Because we should not trust an editor's batch behavior to draw the transaction boundaries we meant. Writing them out says clearly: the first row survives no matter what happens to the second.

A practical warning. Some editors, including the Supabase SQL Editor, only show the last result from a run. So you may only see the three. That does not mean the first two failed. The SELECT on the next slide shows what actually stayed.

Run the whole batch together. Do not leave it paused halfway inside a transaction while you go do something else. An open transaction can hold locks. And if something does fail and the session says the transaction is aborted, run ROLLBACK to end it before you try again.

## Slide 13

This table separates two things: getting a number, and keeping a row. Look at the first column. Every insert got a number: one, two, three. Now the last column. Only the first and third transactions kept a row. So when we run the SELECT at the bottom, we get note 1, Initial view, and note 3, Approved revision. Two rows.

Where did two go? Nowhere mysterious. We know exactly why it is missing: we rolled back that insert. The row was undone, but the sequence did not take its number back. Sequences work that way on purpose. If they had to wait to see whether each transaction commits before handing out the next number, every insert would have to wait in line behind every other one.

Now read the line at the bottom. Final row count, two. Largest ID, three. So the largest ID is not a row count. Deletes make the difference even bigger. If you need to count, use count. If you need to identify a record, use its key.

And no sequence promises an unbroken series of committed numbers. If a business genuinely needs gapless numbers, like some invoice rules, that has to be designed as its own process.

Gaps can also come from other causes in real systems, so a gap alone does not tell you its history. Here we know, because we ran the experiment. In the lab, a few SQL comments explaining the returned numbers versus the final rows are enough.

[Sources]
- PostgreSQL 15, sequence manipulation functions: https://www.postgresql.org/docs/15/functions-sequence.html

## Slide 14

You now have both worked examples you need for Lab 1. It is individual work, in your own course database, and it starts from the full Metro Support data.

Step one, on the slide. The lab gives you a five-column active queue. Your change is to add the assigned agent's display name as the last column, called assignee_name. Use my requester view to see the join syntax, but think about the relationship. A ticket can exist before anyone is assigned, so this one needs a LEFT JOIN. Then check that tickets 1004 and 1009 are still in the result. Their assignee names will be NULL, and that is correct. A missing name is information, not a reason to drop the ticket.

Step two. Create the disposable change_notes table, run the committed and rolled-back inserts, look at the final rows, and explain the gap in the IDs. The lab also gives you two metadata queries that show how PostgreSQL describes the view and the identity column you built.

Submit one file in Brightspace: week_03_views_identity.sql. Working SQL, plus short comments explaining your join and the ID result. No screenshots, no separate report.

And keep this database as it is. Tomorrow's lab changes the tickets table underneath the view you build today. If something fails, look at the current definition before you rerun a CREATE a second time.

## Slide 15

Day 2. Today we change the table underneath the view we just built, and we keep the view working while we do it.

The new requirement is a source channel for every request. The allowed values are web, phone, mobile, and unknown.

The word unknown is the important one. The old tickets were created before this field existed. There is a note in the event history that mentions a mobile form, but one clue about one ticket does not justify stamping a channel on every old request. The database can make sure every row holds an allowed word. It cannot make sure that word is true. That part is our job.

There is also an application problem. An older program may still insert tickets with an explicit list of the original columns. If the new column is required and has no default, that perfectly valid old insert starts failing. So we give the column a default, which keeps that old writer working while newer code starts sending the real channel.

Our order today is: inspect, rehearse, verify, roll back, and only then apply. The transaction makes the rehearsal reversible here. It does not remove every locking or deployment risk, and I will be honest about where those limits are.

Continue in the same database as Day 1. If you are on Colab and your runtime expired, create a new practice database, load the dataset with the setup cells, and rerun your saved Day 1 SQL before the precheck.

## Slide 16

One column, three audiences. Read this table one column at a time.

First, the historical tickets. Before the change they have no channel column at all. After it, the value is unknown, unless we have a trustworthy reason to say something more specific about that particular ticket. Look at the note at the bottom left. A note mentioning a mobile form does not justify labeling every old ticket web. If we did that, every report would look complete while quietly making a claim nobody can back up.

Second, the new writers. Updated application code sends the real channel. The allowed-value rule rejects any spelling we did not agree on, which keeps the data consistent. It still cannot prove that the app reported the real event truthfully.

Third, the older writers. These are programs that insert using the old list of columns and simply leave the new one out. DEFAULT unknown takes care of that. It does not make every old program compatible with every possible change. A program that depends on column positions, or a changed type, or a different result shape, needs its own check.

Now the bottom right. This is a twelve-row practice migration, small enough to verify every row. A production table with millions of rows and constant traffic raises harder questions about lock time, batches, and deployment order. The textbook describes the broader expand-and-migrate pattern for that.

The goal is to record better facts going forward without pretending we already knew the old ones.

## Slide 17

Before we change anything, we write down the starting state with ordinary queries.

The first query reads information_schema.columns, which describes the columns PostgreSQL shows to your role. We narrow it to the tickets table, in metro_support, and to one name, source_channel. Look at the expected results on the right. Zero column rows. That means no such column exists yet. And notice that zero rows is different from one row that contains a zero. The next two queries are counts, so they each return one row: twelve tickets, and seven tickets in the active queue.

Those numbers are expectations for the unchanged classroom data plus your Day 1 view. They are not universal truths about every support database.

Read the box at the bottom. If the column already exists, do not just add it again. You will get an error, and worse, you may not know what state you are in. Look at your earlier attempt and figure out whether you already committed the migration. If the queue count is not seven, check the view definition and the data before you go further.

If you are in the Supabase SQL Editor, remember it only shows the last result. Run each of these three SELECTs on its own so you can see every answer.

Keep these queries in your SQL file. They tell another person exactly what you assumed before you started, and they help you diagnose a rerun.

## Slide 18

This is the complete rehearsal. Let's walk through it.

BEGIN starts the transaction. The first ALTER TABLE adds source_channel as text, and for now it is allowed to be empty. Then the UPDATE fills the empty values with unknown. Look at its WHERE clause, source_channel IS NULL. It says exactly which rows need the backfill instead of overwriting everything.

The next statement adds a CHECK constraint, and we give it a name, tickets_source_channel_allowed. A CHECK says which values are allowed: web, phone, mobile, or unknown. This comes from Chapter 3's section "Constraints Reject Invalid States." We name it because when we deliberately try fax later, the error will tell us exactly which rule stopped it.

Then two more rules: NOT NULL, and DEFAULT unknown. These three rules have different jobs. The CHECK limits which text is allowed. NOT NULL rejects a missing value. The default fills in a value when a writer leaves the column out entirely.

The grouped SELECT runs before the transaction ends, so it sees our uncommitted changes. Look at the line at the bottom: unknown, twelve. Then ROLLBACK throws away the column, the rules, and the backfill.

Run the whole batch together. If the Supabase editor hides that grouped result because the last statement is the ROLLBACK, use the Colab notebook, which prints every result. Do not split the transaction into separate runs. And if a statement fails and leaves you in an aborted transaction, run ROLLBACK before you retry.

## Slide 19

"ALTER TABLE succeeded" is useful, but it only answers a small part of our question. This table lists the specific things we need to check, during the rehearsal and after the rollback.

Read the middle column first, inside the rehearsal. The new column exists with its CHECK, its default, and NOT NULL. All twelve historical rows say unknown. And the old queue still returns seven tickets.

Now the right column, after ROLLBACK. There is no source_channel column. The original rows are still there. And the queue still returns seven.

The query at the bottom is the same column lookup from the precheck. After the rollback, the expected answer is zero rows again.

These rows check two different things: structure and meaning. We could build a perfectly valid NOT NULL column and fill it with an invented channel. Every structural check would pass, and the history would still be wrong. Or we could get the backfill right and then replace the view in a way that drops the unassigned tickets. We need checks for both risks.

If your editor shows only one result at a time, run the read-only checks on their own, after the transaction ends.

One honest limit. This rehearsal shows that this particular PostgreSQL change can be rolled back. It does not show that holding a lock is harmless, or that undoing a future data change will bring back lost detail. Keep each check right next to the change it verifies in your SQL file.

## Slide 20

This is a saved screenshot of the Supabase SQL Editor from August 25, 2026. I am showing it so you can see that the same transaction language works in a hosted browser editor. But be clear about what it shows. It is a tiny temporary-table check, not the tickets migration.

Here is what was run. BEGIN. Create a temporary table called oer_validation with one integer column. ROLLBACK. Then one visible SELECT, the one in the results pane, asking whether PostgreSQL can still find that table. The function to_regclass returns an identifier when it finds the named object, and NULL when it cannot. Comparing that to IS NULL gives true, and that is the rollback_verified column you see. True means the table is gone, because it was created inside a transaction that rolled back.

Look at point three on the right. Checking that this temporary table vanished tells us nothing about our ticket change. For the migration we check source_channel itself, the rules attached to it, the twelve historical rows, and the seven-row queue. A verification query has to be about the object and the behavior that actually matter for your change.

Notice too that the editor shows one result, from the last statement. That is the same behavior I warned you about earlier.

Your Supabase screen may look different today. The transaction boundaries and what the result means matter more than matching this picture.

[Sources]
- Course screenshot: textbook/figures/cloud_interfaces/supabase_sql_rollback.png, captured August 25, 2026.

## Slide 21

Once the rehearsal works and the rollback puts everything back, we apply it for real. Look at the first line on the slide: repeat the same migration with COMMIT in place of ROLLBACK. That keeps the column and its data. Only do this once. Do not rerun the ADD COLUMN block after it has committed. If you are not sure what state you are in, inspect first.

Committing does not change the view. It does not pick up source_channel on its own. So we replace the view's definition with an explicit seven-column interface. Look at the SELECT list. The first five columns are exactly the original lab view, same names, same order: ticket_id, subject, status, priority, opened_at. The sixth is the assignee name you added on Day 1. The seventh, and the only new one, is source_channel. We append. We never insert in the middle.

Look at the bottom of the slide. The LEFT JOIN is still there, because assignment is still optional. Adding a channel did not change that fact, so tickets 1004 and 1009 must stay in the queue. A new requirement should never quietly undo a correct decision from yesterday.

After this runs, read the queue. You should still see seven active tickets, and on the unchanged classroom data their channel should be unknown.

A caller that asks for the original columns keeps working. A caller that wants the new field asks for it by name.

## Slide 22

A rule needs two tests: one value it should accept and one it should reject.

Look at the top block. We start a transaction, set ticket 1004 to mobile, and RETURNING shows us the ticket ID and the new channel. Mobile is on the allowed list and it is not null, so the update succeeds and returns mobile.

Then we roll back. Why? Because we have no real evidence that ticket 1004 came from the mobile app. We should not leave a made-up value in the history just because it made a nice demonstration. After the rollback, ticket 1004 says unknown again.

Now the bottom block. Same ticket, but the value is fax. Run it on its own, separate from the first batch. Look at the expected result on the right. PostgreSQL rejects it with SQLSTATE 23514, and the error names our constraint, tickets_source_channel_allowed. That name is why we bothered naming it. It tells you exactly which protection fired. The stored value stays unknown.

If the editor then tells you the current transaction is aborted, finish it with ROLLBACK before you continue. And do not confuse that later "aborted" message with the real reason fax was rejected.

In your submitted file, keep the fax statement commented out, and write the expected error in a comment. That way anyone can run the negative test on purpose, but a normal run of your file does not stop halfway. We will keep this habit of testing both sides in later weeks.

## Slide 23

Undoing a change and repairing it later are not the same thing. Read the table one row at a time.

First row, before COMMIT. We can roll back the rehearsal, and the original rows and the original interface come back. That is exactly what we just watched.

Second row. Now suppose the migration has committed and new requests are coming in. A new request from the mobile app correctly records mobile. If someone panics and drops the whole column, they destroy a real fact the old database never had. So writing the "opposite" command is not automatically a recovery plan. Often the right move is a forward repair: fix the view, or fix the writer, and keep the new channel data. Look at the last column. Newly collected channel values have to survive.

Now the box about the default. Be precise here. An older writer that leaves the column out gets unknown. A writer that explicitly sends NULL gets a NOT NULL error. Leaving a column out of an INSERT and sending a missing value for it are two different operations. And a newer writer should send the real channel when it knows it, not lean on the default.

The last box. A transaction can hold locks for as long as it stays open. "Transactional" does not mean nobody else has to wait. Keep the practice batch together and finish it.

In your lab write-up, say which state can be recovered and which facts must survive.

## Slide 24

Lab 2 continues in the same database and the same queue from Day 1. It is individual work, and it starts with the supplied precheck. If you have not finished Lab 1's view yet, do that first. The identity experiment is useful background, but you do not need it to change the tickets table.

Step one on the slide: confirm the starting state, then complete the three rules. The starter gives you the transaction, the new column, the backfill, and the grouped check. You add the named CHECK, NOT NULL, and the default. Use the worked slide and the textbook. The point is to connect each rule to its job and check that it behaves, not to recite keywords from memory.

Step two: rehearse, confirm that rollback removes the column, then apply it with COMMIT. Then append source_channel to your existing view, keeping every earlier column and the LEFT JOIN.

Step three: test mobile inside a transaction that rolls back, and test fax separately. Then explain unknown, and explain the repair limit.

Submit one file in Brightspace: week_03_safe_migration.sql. Include the precheck, the completed migration, the view update, and your verification queries. In short comments, say why historical rows use unknown, how the default helps an older writer, and why dropping the column later could erase real data.

If your result does not match, investigate the definition and the specific ticket IDs. Do not reach for the reset script. That would erase the very change you are trying to understand.

## Slide 25

Let's finish with what we can now claim. Read the title: a change is ready when its callers still work. Not when the command succeeded.

Look at the three lines on the slide. First, the queue still includes unassigned work. A queue can look perfectly fine while quietly losing unassigned requests, which is why we checked specific IDs, 1004 and 1009, and not just a count of seven.

Second, generated IDs distinguish records without counting them. A gap can be the normal result of a rolled-back insert. The key tells one record from another. It does not tell you how many committed. We could explain the actual result because we followed the transaction boundaries.

Third, the new channel rule accepts known values without inventing old facts. We added a useful field without making up history. We kept older writers working by letting them leave the field out. We kept the view's columns and appended the new one. And we tested one value that should pass and one that should fail.

This is something you can describe in a technical interview. You changed a PostgreSQL interface, rehearsed the migration in a transaction, checked old and new behavior, and identified the point where a later repair must preserve new data. Be honest that it was a classroom database, not a production service.

Next week, Week 4, is Reliable SQL Reports. We count the right records, pick the latest event without losing requests, and test a report before anyone depends on it.

## Slide 26

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: A view stores a query, not rows (1:14); Why identity values have gaps (1:24); Adding a required field without inventing history (1:27). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 3 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
