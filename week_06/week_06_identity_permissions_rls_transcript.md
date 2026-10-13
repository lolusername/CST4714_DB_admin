# Week 6: Identity, Permissions, and Row-Level Security - Spoken Transcript

## Slide 1

Welcome to Week 6. Two days, two problems, one theme: who is allowed to do what to our data.

The idea is in the two lines on the slide. A useful report can leave private fields out. And a perfectly valid login can still be refused a row. Those two sentences are the whole week.

On Day 1 we build a report reader: a role that can see exactly the open-ticket summary a dashboard needs, and nothing else, and we prove it with one test that succeeds and one test that fails. On Day 2 we take two residents reading the same table who must see different tickets. That needs a different mechanism, row-level security.

Why does this matter? Most data breaches are not someone breaking encryption. They are a legitimate account being allowed to see something it should not. Permissions are the everyday security work of a database administrator, and the good news is that they are testable. That is the mindset for the week. Not "I set it up correctly," but "I ran the test as the user, and here is what they got."

## Slide 2

Here is the scenario that drives the whole week. Resident A is signed in, correctly, with a real password. They open ticket 1, which is theirs, and the URL says tickets slash 1. Then they change the 1 to a 3 and press enter. Ticket 3 belongs to Resident B. Should A see it? No.

Notice that nothing about A's login changed. The password was fine. The session was fine. The only thing that changed was a number the user typed. If the server simply trusts that number, the login has become a key to everybody's tickets. This is one of the most common real vulnerabilities on the web. It has a name, insecure direct object reference, and it shows up in breach reports every year.

So the rule at the bottom of the slide is the lesson. The server has to enforce ownership itself, every time, no matter what ID the caller chooses. Hiding the link does not do it. Making the ID long and random does not do it. Something has to check "does this row belong to this actor," and this week we put that check in the database.

## Slide 3

Four words that people mash together, and we are going to keep them apart all week.

Identity: who is claiming to act? That is the account saying "I am Resident A." Authentication: can we verify that claim? That is the password check or the token check. Authorization: now that we believe you are A, are you allowed to do this specific action on this specific data? And auditing: did we write down what happened?

Here is why the separation matters. On the previous slide, authentication was perfect and authorization was missing. Those are different jobs done by different code. A working password proves exactly one thing: the identity claim checked out. It does not mean the account should read every row.

When something goes wrong this week, your first question is always "which of these four failed?" because the fix is different for each one. You will see that concretely on slide 10.

## Slide 4

Least privilege is a phrase everyone uses and many people get backwards. It does not mean "give nobody anything." It means: start from the work the role actually has to do, give it enough to do that work, and then test that everything else stays unavailable.

Look at the two rows. The report reader has a real job: read open ticket IDs, categories, and statuses, for a dashboard. What is outside that job? Reading residents' email addresses, or changing tickets. The lab analyst, which is your Day 1 lab, has the same shape: read ticket summaries and count them by status, and never read the private source tables or edit anything.

So the design question is always "what does this role need to get its job done?" And the test has two halves: can it do the job, and is it stopped from doing the rest. An allow-only test is half a test. A deny-only test produces a role that cannot work. You need both.

## Slide 5

Let's build the reader. In PostgreSQL there is one concept, a role, that covers both logins and groups.

CREATE ROLE report_reader_demo NOLOGIN makes a role that cannot log in. It has no password. It exists purely to hold a set of permissions. That is a nice property: we define what a reader may do without creating another account someone could guess a password for. The second line, GRANT report_reader_demo TO CURRENT_USER, makes me, the administrator, a member of that role. Membership is what lets me switch into it to test it.

Now the second block. BEGIN starts a transaction. SET LOCAL ROLE makes me act as the reader until the transaction ends. Then I ask PostgreSQL: who am I? Two answers. session_user is who logged in. That is still me. current_user is who I am acting as right now, the reader. ROLLBACK ends the transaction and I am myself again.

That shape, BEGIN, SET LOCAL ROLE, the test, ROLLBACK, is the pattern for every test this week. Run it in your own practice project. Roles belong to the whole server, so never do this in someone else's.

[Sources]
https://www.postgresql.org/docs/15/sql-set-role.html
https://www.postgresql.org/docs/15/user-manag.html

## Slide 6

Here is the complete interface, and I want you to see how small it is.

A schema, security_demo, to keep our demo objects separate. A view, open_ticket_report, which is just a saved query: ticket id, category, status, only where status is open. Three columns, filtered. Then two grants. USAGE on the two schemas, which only lets the role look up objects inside them. And SELECT on the view. That is it.

Read the note at the bottom. The role gets access to the view, not to the tickets table underneath it. We never say GRANT SELECT ON metro_support.tickets. So the reader cannot query the tickets table directly. It cannot see priorities, requesters, timestamps, or anything else we left out of the view. The view is the window, and we decided exactly what is in the window.

One practical note. Load the Metro Support fixture first, because the view points at metro_support.tickets. If the table is not there, CREATE VIEW fails with "relation does not exist," and that is a missing-object error, not a permission result.

[Sources]
https://www.postgresql.org/docs/15/ddl-priv.html
https://www.postgresql.org/docs/15/sql-createview.html

## Slide 7

Now the positive test. Watch its shape, because it is the same every time. BEGIN. SET LOCAL ROLE to the reader. A SELECT that includes current_user, which is deliberate: the first column of the result proves who ran it. ROLLBACK.

The result: three rows, tickets 1001, 1007, and 1011, all open, and the role column says report_reader_demo. So the reader can do its job. That is half the test. Notice we do not just say "it returned some rows." We name the IDs. Named results are what you can check against the data later.

One warning that will save you time in the lab. Run the whole batch on one connection, all four statements together. Web editors like Supabase's may hand each separate Run to a different connection, so a role switch from one run does not carry into the next. And the Supabase editor shows only the last statement's result, which here is the ROLLBACK, so your rows are hidden. That is why the lab gives you a small Colab cell that runs these tests and prints every result.

## Slide 8

Now the other half: a test that must fail. Same shape, but the action is an UPDATE. Set ticket 1004 to high priority, as the reader. The reader has no grant on the tickets table at all, so the expected result is an error: "permission denied for table tickets," error code 42501.

That code matters. 42501 means "you reached the database, and it refused this operation for this role." A network error is not that. A typo in the table name is not that. Only 42501 is a passed denial test. If the client stops at the error and leaves you inside the transaction, run ROLLBACK by itself to get out.

Here is the clever part of wrapping the test in a transaction. Suppose I got the grants wrong and the UPDATE actually succeeds. The ROLLBACK still throws the change away. The data is safe, I have learned that my grant is too broad, I fix it and run the test again. A denied test built this way is safe to run even when you are wrong.

## Slide 9

Something subtle happened on slide 7 that is worth stopping on. The reader has no permission on the tickets table. Yet it read three tickets. How?

Because a normal view runs with its owner's permissions on the tables underneath. I own the view. I can read tickets. So when the reader selects from my view, PostgreSQL checks my access to tickets, not the reader's. That is exactly what makes a view a good reporting interface: the reader gets three columns of three rows and never touches the source table.

But it is also a warning. If the owner is powerful, the view is powerful. On Day 2 we add row-level security to a table, and a view owned by an administrator would happily show every row regardless, because the owner bypasses those rules. So a view is not automatically a safe window for a resident.

PostgreSQL 15 and later has an option, security_invoker, that makes a view check the caller's permissions instead. But then the caller needs its own access to the base tables. Different design, different test. Know which one you built.

[Sources]
https://www.postgresql.org/docs/15/sql-createview.html

## Slide 10

Before the lab, a triage table, because the most expensive mistake this week is fixing the wrong layer. Four things that all look like "it doesn't work" and are completely different.

Network unreachable: the client never got to the database. No permission check happened at all. Password authentication failed: you reached the database, but the login did not check out. That is authentication. 42501, permission denied: you are in, you are authenticated, and this role is not allowed this operation on this object. That is authorization, and the fix is a specific grant for a specific role. Zero rows with no error: the query ran, it was allowed, and either nothing matched or, on Day 2, a row policy filtered the rows out.

The bottom line matters most. When something fails, the reflex is "grant more." Granting more does nothing for the first two and quietly destroys your security for the other two. Find the failing layer first.

[Sources]
https://supabase.com/docs/guides/database/connecting-to-postgres

## Slide 11

Here is Lab 1. Create the supplied analyst role and the limited view over all twelve tickets. Read the view as the analyst. Then write one report as the analyst: count tickets by status, through the view. The counts should add up to twelve. That is the proof that the role can do useful work.

Then two tests that must fail: reading the email column from the users table, and updating a ticket. Both should give 42501.

Write a few sentences explaining what the analyst can do, which tests show the boundary, and why testing only as the owner would prove nothing, since the owner can do everything.

Submit one file, week_06_least_privilege.sql, with the SQL, the observed results in comments, your explanation, and the cleanup at the end. No screenshots, and no passwords in the file. Use your own project. If Supabase hides your results, use the Colab display cell in the lab.

## Slide 12

Last time we solved a permissions problem with a view and a grant. The report reader could read exactly the columns we chose and nothing else. Today's problem is different, and it is the one most real applications actually have.

Two residents both need to read the tickets table. Same table, same permission, same query. But resident A must only ever see A's tickets, and resident B only B's. A grant cannot express that. A grant says "this role may read this table." It has no idea what a row means or who it belongs to. So we need a second kind of rule, one that looks at each row and asks: does this row belong to the person asking? That is row-level security.

Here is how we will test it today. First, we run the same SELECT as each resident and check that they get different rows. Second, we have a resident ask for someone else's ticket by number, like editing the ID in a URL, and watch what happens. Third, we add a brand new ticket and check that the rule still works without us touching it.

One thing to keep in mind all day: each resident is a database role today, which makes the rule easy to see. In a real app, people are not database roles. We will get to how that maps at the end.

## Slide 13

Here is our entire dataset for today. Four tickets in a table called resident_tickets, inside a schema called security_demo. Look at the owner_role column, because that is the important one. Tickets 1 and 2 belong to resident_a_demo. Tickets 3 and 4 belong to resident_b_demo. Ownership is written down explicitly in a column. We never guess it from the ticket number or the subject.

Both resident roles have been given two things. USAGE on the schema, which just lets them see that the schema exists, and SELECT on this table. Nothing else. No insert, no update, no delete.

Now notice what happens before we add any row rule. If I switch to resident A and select from this table, I get all four rows. Watch the first column, current_user. It says resident_a_demo, and there are four rows. The grant did exactly what grants do. It let the role read the table. It has no idea that owner_role is supposed to limit anything. That is our baseline. Everything we add from here is about turning four rows into the right two.

One housekeeping note. Your lab uses a separate schema called security_lab and roles named resident_101_lab and resident_102_lab, so nothing I create here collides with what you create.

## Slide 14

Two statements here, and I want to run them separately, because the gap between them teaches something.

First: ALTER TABLE, ENABLE ROW LEVEL SECURITY. That flips a switch on the table. It does not say who can see what. Watch what happens when I rerun resident A's query right now. Zero rows. No error, just nothing. Once row security is on, the default is deny. An ordinary role sees no rows until a policy allows some. That is a safe default. It is also the moment where people panic and write USING true to make the rows come back. Do not do that. That allows every row, and you are right back where you started.

Second statement: CREATE POLICY. Read it clause by clause. ON names the table. FOR SELECT means this rule only governs reading. Writes would need their own rule. TO lists the roles the rule applies to, our two residents. USING is the condition PostgreSQL checks against every row: keep the row if owner_role equals current_user, the role running the query.

So when A runs a SELECT, PostgreSQL silently adds "and this row belongs to A" to the query. A never has to remember to write that WHERE clause. That is the entire point. The rule lives in the database, so the application cannot forget it.

One more thing. The policy did not give anyone permission to read the table. The grant did that. The grant says whether. The policy says which rows. You need both.

[Sources]
https://www.postgresql.org/docs/15/ddl-rowsecurity.html

## Slide 15

Now the test. This query is deliberately boring: current_user, ticket id, subject, ordered by ticket id. There is no WHERE clause about ownership anywhere in it.

We wrap it in BEGIN, SET LOCAL ROLE, the query, and ROLLBACK, all together as one batch. SET LOCAL ROLE makes me act as resident A until the transaction ends, and ROLLBACK ends it, so afterward I am myself again. I run it as A: two rows, 1 and 2, and current_user says resident_a_demo. Now I change exactly one word, the role, to resident_b_demo, and run the identical query: two rows, 3 and 4. Same SQL, different answer, because the actor changed. The table still has all four rows. Nobody deleted anything.

Two things to notice. First, we compare the actual IDs, not the counts. Both residents got "two rows." If the policy were wrong you could still get two rows and never know. Second, why all four lines go together. In the Supabase SQL editor, every time you press Run you may land on a different connection. If you SET ROLE in one run and SELECT in the next, the role switch is gone. You are querying as yourself, the administrator, you see all four rows, and you conclude the policy is broken. It is not. Paste the whole batch every time, and read the current_user column before you read the ticket numbers.

## Slide 16

This is the slide 2 scenario, the edited URL. Resident A asks for ticket 3 by number. I added WHERE ticket_id equals 3, and I did not touch the policy. Zero rows. No error.

Think about why. The grant says A may read this table, so PostgreSQL does not refuse the query. Then it applies the policy: keep rows where owner_role is resident_a_demo. Ticket 3 belongs to B, so it is filtered out. A asked a legitimate question and got an honest empty answer.

This matters because people expect security failures to look like errors. A lot of the time they do not. A restricted read usually works by leaving rows out, not by shouting at you. So in the lab, when you get zero rows here, that is the correct result. Write "zero rows, no error" in your comments, not "permission denied."

One caveat we only get because we built the data ourselves: we know ticket 3 exists. In a real application, an empty result could also mean the ticket does not exist at all. A security test needs that knowledge, which is why we use a tiny fixture we understand completely.

## Slide 17

Here is the test that catches lazy rules. Before I run anything, predict. I am going to insert ticket 5, owned by resident A, subject Blocked drain. What does A see afterward? What does B see?

The insert runs as me, the administrator, because the residents have no insert permission, and that is deliberate. Now I rerun A: 1, 2, and 5. I rerun B: still 3 and 4. I did not edit the policy. It compared the new row's owner_role to the current role, the same as every other row.

Compare that to a rule someone might write in a hurry: "A can see tickets 1 and 2." That rule passes every test we ran before this slide, and it fails the moment a new ticket arrives. A good rule describes the relationship between the row and the actor, not a list of numbers.

In your lab you will insert ticket 5 for resident 102, not 101, and rerun both residents. If you accidentally run the insert twice you get a duplicate key error on ticket 5. That just means it already worked. Look at the row instead of inserting again.

## Slide 18

Now watch me run the same SELECT with no role switch at all, just as myself. Five rows. Every one of them. Did the policy fail? No. I own this table, and in PostgreSQL the table owner is not subject to row security by default. Superusers are not either, and neither is any role with the BYPASSRLS attribute.

Here is why that matters to you specifically. The Supabase SQL editor runs as a role called postgres, which has BYPASSRLS. So when you test a policy in the SQL editor and see every row, you have learned nothing about what a real user sees. It is not evidence the policy is broken, and it is not evidence that it works. You have to test as the role the application actually uses. That is the whole reason our tests switch roles.

There is a setting called FORCE ROW LEVEL SECURITY that makes a plain table owner obey the policies too, but it does nothing to superusers or BYPASSRLS roles.

The lesson for your write-up: a security claim names its actor. "The policy works" means nothing. "Resident 101 sees 1 and 2, resident 102 sees 3, 4, and 5, and the direct lookup for 3 returns nothing" is a claim someone can check.

[Sources]
https://www.postgresql.org/docs/15/ddl-rowsecurity.html

## Slide 19

So far every resident has been a PostgreSQL role. That is great for a classroom and wrong for a real application. You do not create a database role for every person who signs up.

Here is what actually happens in a Supabase app. A resident signs in through Supabase Auth and gets back a token, a signed piece of text that says "this is user such-and-such." Every request the app makes carries that token. Supabase's API verifies the signature, then runs your query as one shared database role called authenticated. Everybody who is signed in shares that same role.

So how does the policy tell people apart? Through the token. A function called auth.uid returns the user ID from the verified token for the current request. The policy compares the row's owner to that ID.

Two things to be careful about. One, the browser cannot become someone else by sending a different user ID in the request body. The ID has to come from a token the server verified. Two, a signed token is usually readable. You can decode it and see the claims inside. It is still a credential. If someone copies it, they are you until it expires. Do not paste tokens into shared notebooks.

And to be honest about what we did today: switching roles with SET ROLE is a database test. It is not a test of the login flow.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security
https://supabase.com/docs/guides/getting-started/api-keys

## Slide 20

This is what our policy looks like translated for a real app. Instead of comparing owner_role to current_user, it compares a column called requester_auth_id to auth.uid. The role is authenticated, the shared one from the previous slide. The nested SELECT around auth.uid is just the form Supabase recommends. It lets PostgreSQL evaluate the function once instead of once per row.

I want to be clear: this is an illustration, not something to paste into our Metro Support table. Our tickets have integer requester IDs. Supabase Auth identifies people with UUIDs, those long hexadecimal strings. A UUID is an identifier, not a secret, and you cannot just rename a column to switch from one to the other. You would have to actually map every existing ticket to a real signed-in user.

Here is a nice connection to Week 2. If there is no signed-in user, auth.uid returns NULL. What is NULL compared to anything? Not true, not false. Unknown. And a row is only kept when the condition is true. So an anonymous request matches no rows. The same three-valued logic that bit you in your WHERE clauses is now quietly doing security work.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security
https://www.postgresql.org/docs/15/functions-comparison.html

## Slide 21

Reading rows and writing rows are two different decisions, and policies have two clauses for them. USING is what we have been using all day: which existing rows may this operation see or touch. WITH CHECK is about a row you are trying to create or change: is the new version of the row allowed?

Picture resident A submitting a ticket. The app must not let A set the owner to B just by editing a field in the form. An INSERT policy with WITH CHECK compares the proposed owner to the authenticated user and rejects the row if they do not match. And unlike a filtered read, a rejected write does produce an error, because there is no row to quietly leave out.

Two reminders. A policy is not a grant. To insert, a role still needs INSERT permission on the table. And today's residents only have SELECT. If one of you tries an insert as a resident, you get "permission denied for table," and that is the grant stopping you, before any policy is even consulted.

When you write up your lab, say that you tested reads only. Do not claim you tested writes you did not test.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security

## Slide 22

The word "key" causes a lot of damage, because people treat all keys as the same thing. Four different credentials, four different powers.

The publishable key, which older projects call the anon key, identifies your application to Supabase. It is meant to live in browser code. It does not identify a person, and anything using it is subject to row security.

The user's access token is the person. That is what makes auth.uid work. Keep it private.

The secret key, or the legacy service-role key, is for a trusted server, and it bypasses row security entirely. It never goes into browser code or a shared notebook.

And the database password or connection URI is a fourth thing. It logs into PostgreSQL directly as a database user. It has nothing to do with app users. That is why the lab's Colab cell asks for the URI through a hidden prompt instead of putting it in a cell.

Last thing. If a secret ends up in Git, deleting the line does nothing. It is still in the history, and anyone who saw it still has it. Rotate the secret first, then clean up.

[Sources]
https://supabase.com/docs/guides/getting-started/api-keys

## Slide 23

Your lab is the demo you just watched, in your own schema, with one twist.

Set up security_lab with two resident roles and the same four tickets. Enable row security and create the policy. Run both residents, and run the direct lookup for ticket 3 as resident 101. Then, as the administrator, insert ticket 5 owned by resident 102, and rerun both residents. Resident 101 should be unchanged. Resident 102 should gain ticket 5.

Finish with a few sentences to the developer: what each resident saw before and after, what the direct lookup returned, why testing as the owner proves nothing, and the one test that is still missing before deployment, a request with each resident's real login token.

Three practical things. Every resident test is one batch. Paste all four lines together. The Supabase editor only shows the last statement's result, which is the ROLLBACK, so use the Colab display cell from Lab 1 to see your rows. And when you copy the pooler connection string, replace the YOUR-PASSWORD placeholder yourself before pasting it into the hidden prompt.

Submit one file, week_06_rls_test.sql, with the cleanup at the end. No screenshots.

## Slide 24

We are going to step away from permissions for about thirty minutes and look at a different kind of failure. On Monday, July 20, 2015, the hosted Sentry service was down for most of the US working day. Nobody attacked it. No disk failed. PostgreSQL stopped accepting writes on purpose, because continuing would have made the data wrong.

You already know the mechanism underneath this from last week: MVCC, row versions, and the fact that old versions have to be cleaned up by maintenance. Today we fill in the piece we skipped. What that maintenance actually is, why teams change its settings, and what happens on the day it falls behind.

Here is the plan. Four short slides of background: row versions, transaction IDs, vacuum, and autovacuum. One slide on why people tune it and the trap in doing so. One slide on the protection that stopped Sentry. Then the incident itself, two queries you can run to see whether your own database is anywhere near this, and the writing prompt. You will read the original incident report and write a short reflection in Brightspace. No SQL today, just thinking clearly about availability versus correctness.

Why is this in the permissions week? Because the engineers who recovered Sentry used the most powerful credentials in the system to drop a table under pressure. That is exactly the power this week's labs keep away from application roles, and exactly the kind of call a database administrator has to be ready to make and explain.

[Sources]
https://blog.sentry.io/transaction-id-wraparound-in-postgres/

## Slide 25

Last week's MVCC slide said PostgreSQL does not overwrite a row when you update it. Here is what that looks like if you ask for it. Every table has two hidden columns you can select by name: xmin, the ID of the transaction that created this version, and xmax, the ID of the transaction that expired it. Zero means nobody has.

I ran this on a fresh PostgreSQL 16 this afternoon. Before the update, ticket 1004's row version had been created by transaction 733 and had xmax zero. I updated the priority to high in transaction 735. Now the visible version says xmin 735, xmax 0. The old version is still physically in the table file with its xmax set to 735. Any snapshot taken before 735 committed can still read it, which is the whole reason it has to stay.

Once no snapshot can see that old version any more, it is dead. Not deleted. Dead. It takes up space in the table and in every index that points at it, and nothing in an ordinary UPDATE or DELETE ever removes it. Something else has to come along and do that. That something is vacuum, and it is the next three slides.

One correction to a common mental picture: this is not two tickets. It is one logical row with two physical versions. Your count query says twelve either way.

[Sources]
https://www.postgresql.org/docs/16/ddl-system-columns.html
https://www.postgresql.org/docs/16/mvcc-intro.html

## Slide 26

Here is the number at the center of the incident. A transaction ID is a 32-bit integer. That gives about four billion values, and PostgreSQL treats them as a circle, not a line. From wherever the counter currently is, about two billion IDs count as the past and about two billion count as the future. Visibility is a comparison: a row version created by a past transaction that committed is visible; one created by a future transaction is not.

Now imagine the counter keeps going and laps itself. A row that was created two billion transactions ago now has an ID that looks like it is in the future. From PostgreSQL's point of view that row has not been created yet, so it disappears. A delete from two billion transactions ago looks like it has not happened yet, so the deleted row comes back. Nothing on disk changed. The arithmetic just stopped meaning what it meant. The documentation calls this catastrophic data loss, and that is fair.

The defense is called freezing. Vacuum looks at rows whose creating transaction is older than vacuum_freeze_min_age, fifty million by default, and marks them frozen: visible to every transaction, forever, no comparison needed. Once every old row in a table is frozen, that table does not care how far the counter has moved. PostgreSQL records the oldest unfrozen ID for each table and for each database. The age of that ID is the number you watch. On a quiet server it is tiny; mine this afternoon read 14.

[Sources]
https://www.postgresql.org/docs/16/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND

## Slide 27

So what is vacuum? It is the routine maintenance that keeps MVCC honest, and it has three jobs. First, it finds dead row versions, the ones no snapshot can see any more, and marks their space reusable, in the table and in the indexes that point at them. Second, it freezes old transaction IDs, which is the wraparound defense from the previous slide. Third, it maintains the visibility map, which lets later vacuums skip clean pages and lets index-only scans avoid the table, and when it runs with ANALYZE it refreshes the row counts and value distributions the planner uses.

Two things people get wrong. Plain VACUUM does not give space back to the operating system; it makes the space available for reuse inside the table. It runs alongside ordinary SELECT, INSERT, UPDATE, and DELETE. VACUUM FULL is a different command: it rewrites the whole table into a new file with no dead space, needs that much extra disk, and takes an ACCESS EXCLUSIVE lock, so nothing else can touch the table while it runs. You almost never want FULL on a production table during the day.

And the point Chapter 5 makes bears repeating: seeing vacuum in your logs is normal. It is the system doing its job. The failure we are about to look at is vacuum not running enough, not vacuum running at all.

I ran it on my twelve-ticket table after seven updates. Before: seven dead rows in pg_stat_user_tables. After VACUUM VERBOSE: seven removed, twelve remain, zero dead. That is the whole operation at small scale.

[Sources]
https://www.postgresql.org/docs/16/routine-vacuuming.html
https://www.postgresql.org/docs/16/sql-vacuum.html

## Slide 28

Nobody runs VACUUM by hand on a busy system. A background process called autovacuum wakes up once a minute, looks at the statistics for each table, and starts a worker when a table crosses a threshold. The formula is on the slide. Fifty dead rows, plus twenty percent of the table's row count. That default is tuned for ordinary tables. Look at what it does at the extremes. Our twelve-row tickets table needs fifty-three dead rows, so it is vacuumed rarely, which is fine. A billion-row table needs two hundred million dead rows before anything happens, which is a lot of bloat to carry and a very long vacuum when it finally starts. That is why operators lower the scale factor on their biggest tables, and you will see Sentry's numbers in a moment.

There is a second trigger that has nothing to do with dead rows. Every table has an oldest unfrozen transaction ID. When its age passes autovacuum_freeze_max_age, two hundred million by default, autovacuum vacuums that table to freeze it whether or not anything else is due. This happens even if you have turned autovacuum off. It is the system's own insurance against wraparound, and when people say a vacuum started on its own in the middle of the day on a huge table, this is usually the trigger that fired.

Three workers at a time by default, and they share one I/O budget. Hold on to that, because it is where the tuning story starts.

[Sources]
https://www.postgresql.org/docs/16/routine-vacuuming.html#AUTOVACUUM
https://www.postgresql.org/docs/16/runtime-config-autovacuum.html

## Slide 29

Here is why a sensible team ends up in trouble. Every one of these settings exists for a good reason. Vacuum reads and writes a lot of disk. On a write-heavy system, the easiest way to make the daytime faster is to slow vacuum down: raise the cost delay so each worker pauses more often. Three workers is not many when you have hundreds of tables, so people raise that. The twenty percent scale factor is far too lazy for a billion-row table, so people lower it per table. And when a forced anti-wraparound vacuum lands on a huge table in the middle of the day, the tempting fix is to raise autovacuum_freeze_max_age so it happens less often.

Now look at the direction of each change. Slowing vacuum down to protect today's traffic means dead rows and unfrozen IDs pile up for tomorrow. Raising the freeze age means the table gets closer to the wraparound horizon before anyone is forced to deal with it. That is the trap. Autovacuum tuning looks like a performance decision, and most of the time it is. But vacuum is also the only thing standing between your data and the counter from two slides ago, and the counter does not negotiate.

Sentry's own account: before the outage they ran with too high a value for autovacuum_freeze_max_age, the default three workers, and far too much cost delay. Each of those is a defensible choice on its own. Together they meant the maintenance on their biggest tables was always a little behind, until one day it was two billion transactions behind.

[Sources]
https://www.postgresql.org/docs/16/runtime-config-autovacuum.html
https://blog.sentry.io/transaction-id-wraparound-in-postgres/

## Slide 30

This is the protection that stopped Sentry. PostgreSQL will not let the counter lap your oldest unfrozen row, because the alternative is the data loss from the horizon slide. So it watches the distance between the oldest unfrozen ID in each database and the wraparound point, and it escalates.

With more than forty million transactions to spare, nothing special happens; forced freezing vacuums keep starting at age two hundred million, as we saw. At forty million left, every command starts logging the warning on the slide: database must be vacuumed within so many transactions. At three million left, PostgreSQL stops assigning new transaction IDs. Reads still work, because a read-only transaction does not need a new ID. Every INSERT, UPDATE, DELETE, and TRUNCATE fails with the error on the slide. In 2015 that last line was drawn at one million; version 14 moved it to three million. The shape is the same.

Read the message again: not accepting commands to avoid wraparound data loss. PostgreSQL is choosing to be unavailable rather than wrong. That is a design decision, and I think it is the right one, but it means the outage is now yours to resolve, and the only way out is a vacuum that freezes the old rows. On a table with billions of rows that vacuum takes hours, and you cannot speed it up by panicking.

One practical note, since the error's hint text is older than the advice. The hint says to stop the server and vacuum in single-user mode. The current documentation says not to do that. End any very old transactions and prepared transactions, drop stale replication slots, then run VACUUM in that database normally. Keep that in mind when you read Sentry considering the single-user route.

[Sources]
https://www.postgresql.org/docs/16/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND

## Slide 31

Now the incident itself, in the order it happened. Monday morning, writes stop. The protection from the previous slide has fired on Sentry's main database. Sentry's job is to receive error events from other people's applications, so within minutes the queue of unwritten events is growing and the buffers in front of the database are, in their words, getting out of control.

The team's first decision is to let the running vacuums finish rather than restart them, because interrupting a vacuum throws away its progress. They move the primary to new hardware with more memory and CPU so the vacuums run faster. Nearly three hours pass. Then they query PostgreSQL's own statistics and find that every table has finished except one: a very large table that maps each event to its rollup group, one row per event ever received.

Here is the decision I want you to think hard about. They have no way to know whether that last vacuum needs one more hour or ten. They decide they are willing to lose everything in that table if it means recovering immediately. Their reasoning: it served features that were not critical, and replicas held a copy. They truncate it. Five minutes later the service is fully restored.

Afterward they changed the numbers from two slides ago: six workers instead of three, a fifteen-second naptime, zero cost delay, much more maintenance memory, and a lower freeze minimum age so rows freeze sooner. The bigger plan was architectural: split the data across several databases so no single table could grow to that size again.

Notice who did this. The people who ran TRUNCATE were using the most powerful credentials in the system, under pressure, with the whole company waiting. That is what this week has been about.

[Sources]
https://blog.sentry.io/transaction-id-wraparound-in-postgres/

## Slide 32

You do not have to wait for the warning. Two queries tell you where you stand, and both run in any practice project, including yours.

The first asks every database for the age of its oldest unfrozen transaction ID. That number should sit comfortably under two hundred million, because forced vacuums start there. If you see it climbing steadily toward two billion, something is preventing freezing: a vacuum that cannot keep up, a transaction that has been open for days, or a replication slot nobody cleaned up. On my practice server this afternoon the answer was fourteen for every database. That is what a healthy, nearly idle server looks like.

The second asks the statistics view for the tables with the most dead rows and when autovacuum last touched them. Dead rows should rise and then fall back after each vacuum. If a big table's count only ever rises and last_autovacuum is empty or days old, that is the Sentry pattern forming. Before vacuuming my tickets table I saw seven dead rows; after, zero.

These are the two numbers I would put on a dashboard with an alert. Sentry's own write-up says they found the one unfinished table by querying these statistics. They could have run the same query a month earlier. In your reflection, this is what a concrete prevention step looks like: not "monitor the database," but "alert when the transaction ID age passes a number we chose."

[Sources]
https://www.postgresql.org/docs/16/monitoring-stats.html#MONITORING-PG-STAT-ALL-TABLES-VIEW
https://www.postgresql.org/docs/16/routine-vacuuming.html#VACUUM-FOR-WRAPAROUND

## Slide 33

Here is the writing task. First, read the original incident report by David Cramer at Sentry. The link is on the week page. It is short, it is honest, and it was written three days after the outage by the people who lived it. Give it ten minutes and read it properly, including the update at the end where they correct their own memory numbers.

Then write two hundred fifty to three hundred fifty words in the Brightspace assignment. Four things it must cover. One: what PostgreSQL was protecting when it stopped accepting writes, and why stopping was the right thing for the database to do. Two: what let the maintenance fall behind at Sentry, and why vacuuming is a correctness problem and not only a performance problem. Three: the recovery decision. They deleted an entire table to get back in minutes instead of hours. What made that an acceptable risk for them, and would you have made the same call? Say why. Four: two concrete things a team should do so this never happens to them, and which one matters most.

Use at least three of the four terms on the slide, and use them correctly. Write an argument in paragraphs, not a summary in bullets. And keep two words apart the whole way through: availability, is the service up, and correctness, is the data right. The entire incident is PostgreSQL trading the first for the second, and then Sentry trading the other way.

It is submitted as text in Brightspace. No SQL, no screenshots. If you finish early, go back to Lab 2.

[Sources]
https://blog.sentry.io/transaction-id-wraparound-in-postgres/
Course page: week_06/in_class_writing_mvcc_wraparound.md

## Slide 34

Let's be precise about what we can now claim. The analyst can produce the report through a limited view. Each resident sees exactly their own tickets, including a new one, and asking for someone else's ticket returns nothing. And every one of those checks ran as the intended role, which we proved by looking at current_user.

Those are specific claims with evidence behind them. They are much stronger than "row security is enabled" or "the grant ran," which only describe what we intended.

Let's be equally precise about what we have not shown. We have not shown that every API route uses the right role, that tokens are handled correctly, or that a leaked administrator credential is harmless. A real review has to look at the actual request paths.

Run your cleanup before you leave. Keep the SQL and your observations in your file, and never the credentials. Next week we turn to performance. Once a query is correct and permitted, how much work does PostgreSQL do to answer it, and how do we read its plan.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
