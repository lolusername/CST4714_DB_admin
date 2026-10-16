# Week 5: Transactions, MVCC, and Locks - Spoken Transcript

## Slide 1

Welcome to Week 5. Up to now we have mostly looked at one statement at a time. Does this query return the right rows? Does this row satisfy the rule? This week we ask what happens when one action needs more than one statement, and what happens when more than one person acts at the same moment.

Look at the two lines on the slide. One assignment changes two records. Two sessions can compete for one row. Those are our two days.

On Day 1 we follow one ticket assignment. Assigning a ticket changes the ticket, and it also writes a history event. We rehearse it, we commit it, and we make it fail on purpose, and every time we check what was actually stored. The SQL is familiar. The new question is where the decision boundary goes.

On Day 2 we open separate database sessions. One changes a ticket's priority and does not commit. Another tries to change the same ticket's status and has to wait. We will see why a plain reader still gets an answer, and we will compare two ways to release the waiting writer.

Why does this matter? Because "the statement succeeded" and "the right thing was saved" are different claims. An update can return a row before anything commits. A query can finish and still keep the wrong data. This week you learn to tell those apart, and to prove which one happened.

[Sources]
- Course textbook, Chapter 5, Transactions Coordinate Competing Work.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 2

Here is the assignment we will use all through Day 1. Look at the first row of the table. Ticket 1004 has no assignee, and its status is new. We want to give it to Agent 202, whose user ID is also 202, and move it to in_progress. That is a change to the current ticket row.

Now the second row. Event 5998 does not exist yet. When we create it, it records that this assignment happened: who made it, the old status, and the new status. So the ticket answers "who is responsible right now," and the event answers "how did it get that way." They do different jobs, which is why we keep both.

Here is the problem. Imagine the ticket update succeeds, and then the connection drops before the event is inserted. A staff member sees Agent 202 on the ticket. Someone reviewing the history finds no assignment at all. Each table, on its own, looks perfectly valid. The action is still only half done.

Read the line at the bottom. Two successful SQL statements are not automatically one transaction. PostgreSQL has no idea that these two commands belong together. We have to say so. That is what a transaction is for: drawing a boundary around changes that mean one thing to the application. In your lab the agent and the event number are different, and the tables are disposable copies, but the relationship between current state and history is exactly the same.

[Sources]
- Course Metro Support fixture and Chapter 5 assignment example.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 3

This diagram is about endings. BEGIN opens a transaction. Then we do the work, the UPDATE and the INSERT, and we can inspect that work from our own connection. Then there are two ways out. COMMIT keeps the changes. ROLLBACK discards them.

Notice that they are alternatives, not two steps in a checklist. You pick one. And look at the line at the bottom: a later ROLLBACK does not reverse a completed COMMIT. Once you commit, the change is real, and other people may already be reading it. If it was a mistake, fixing it means writing another change based on what you know now. That is the same distinction we made when we rehearsed a migration earlier in the course. Rehearsing a change is cheap. Repairing a live system after it has collected new data is not.

One more thing. Closing a browser tab is not a transaction command. A client can keep a connection alive in the background, and an open transaction keeps holding resources even when nobody seems to be working. End your transactions on purpose.

In my demonstration I run the whole block and end with ROLLBACK, so the shared fixture stays unchanged. In your lab you work on a copy and actually COMMIT the approved assignment. Whenever you write down an observation, say where in this diagram you made it. A value you see while the transaction is open is a different fact from what a fresh query shows after it ends.

[Sources]
- Course Chapter 4 and Chapter 5 transaction-boundary discussion.
- https://www.postgresql.org/docs/15/sql-commit.html
- https://www.postgresql.org/docs/15/sql-rollback.html

## Slide 4

Here is the complete rehearsal, starting from the supplied fixture.

BEGIN opens the transaction. The UPDATE targets ticket 1004, and look at the WHERE clause. It also requires status equals new. That is not decoration. It states the transition we mean: we are assigning a ticket that nobody has picked up yet. If someone already moved it, we do not want to quietly overwrite their work.

SET puts Agent 202 on the ticket and changes the status to in_progress. RETURNING sends back the row this statement actually changed. For this fixture you get 1004, 202, in_progress. That is our evidence of what the statement touched.

Then the INSERT creates event 5998. Read the column list against the values: ticket 1004, actor 202, type status_changed, old status new, new status in_progress, a short note, and now for the timestamp. I use a fixed event ID so the example is easy to check. A real application would normally generate IDs.

Then ROLLBACK discards both changes. Run the whole block at once, so the transaction is not left open while we talk. Here is the trap. You may see a returned row or a success message before that ROLLBACK, and neither one means the assignment was kept. Also, a web editor may show you only the last result, which is the ROLLBACK. That is why Lab 1 gives you a small Colab helper that prints every result in order. On the next slide we prove what survived.

[Sources]
- Course Chapter 5 worked assignment and Metro Support fixture.
- https://www.postgresql.org/docs/15/dml-returning.html

## Slide 5

How do we know what actually happened? We ask, at the right moment. This table has three moments.

First row: inside the transaction. Our own connection sees ticket 1004 with 202 and in_progress, and after the INSERT, event 5998 is present. We can see our own uncommitted work, even though nothing has been committed.

Second row: after ROLLBACK. Run a fresh query and the ticket is back to NULL and new. Query event 5998 and you get no row. Rollback did not leave a blank event behind. It discarded the insertion, so the record simply does not exist.

Third row is the other possible ending. If we started from the same state, ran the same successful pair, and committed, both changes would remain: 202, in_progress, and event 5998 present. That is a comparison between two endings. It is not a suggestion to type COMMIT after the ROLLBACK we just ran.

Now look at the two queries at the bottom. They ask about exactly the objects we changed, ticket 1004 and event 5998. Why not count all the tickets? Because an update does not change how many tickets there are. The count would look identical whether the assignment survived or not. Choose the check whose answer directly proves your claim.

In your SQL file, a short comment for each observation is enough. Someone reading it should be able to tell what you saw during the transaction apart from what persisted after it ended.

[Sources]
- Course Chapter 5 and the actual assignment rehearsal.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 6

Now let's break it on purpose. The UPDATE sets ticket 1004's priority to urgent. Then the INSERT tries to copy event 5001 back into the events table. Event 5001 already exists, primary key and all, so this insert has to fail.

The INSERT with a SELECT is just a compact way to copy an existing row with every required value. It is deliberately wrong. We expect PostgreSQL to reject it with a unique violation, SQLSTATE 23505. And that rejection is the useful result, because now we can ask the interesting question: what happened to the UPDATE before it, the one that succeeded?

Look at the lower block. After the error, I run it separately. ROLLBACK ends the failed transaction, and then I check the priority. It says low. The urgent change was inside the same transaction as the rejected insert, so it never became a committed fact on its own. The pair goes together or not at all.

Why run the lower block separately? Because the editor may stop at the error, so do not assume the rest of the batch ran. If your client has already ended the failed transaction, the extra ROLLBACK may just tell you there is no transaction in progress. That is fine. The SELECT still gives you the answer.

And notice what the failure did not do. It did not erase event 5001. It refused a new duplicate and left the committed history alone.

[Sources]
- Course Chapter 5 failed-transaction explanation.
- https://www.postgresql.org/docs/15/errcodes-appendix.html
- https://www.postgresql.org/docs/15/sql-rollback.html

## Slide 7

Here is a different kind of failure, and it is sneakier. This UPDATE says: assign ticket 1004 to Agent 202, but only if its status is resolved. Ticket 1004 is new, so nothing matches. Watch what PostgreSQL does. No error. RETURNING gives back zero rows, and the statement completes normally.

That is correct behavior. "Update every row that matches this condition" is allowed to match nothing. No constraint is broken. Which means that if the next statement in the transaction inserted an event, nothing in the database would stop it.

Now picture application code that never looks at that result. It runs the update, runs an insert that says "assigned to Agent 202," and commits. You now have a history event for an assignment that never happened. Wrapping it in BEGIN and COMMIT did nothing to prevent that, because a transaction does not know your business rule. Only the code can see that zero rows came back and decide to stop and roll back.

That is why we keep two ideas separate. A duplicate key is a database rule being enforced. Zero affected rows is a perfectly valid result that may or may not be what the person wanted. In some workflows, doing nothing to an already resolved ticket is exactly right.

You do need to explain why checking RETURNING matters. Read the line at the bottom of the slide: application code must inspect the result before writing history or announcing an assignment.

[Sources]
- Course Chapter 5, Keeping State and History Together.
- https://www.postgresql.org/docs/15/sql-update.html

## Slide 8

Now we can attach real examples to the four letters in ACID.

Atomicity is the boundary. In our successful pair, the assignment and its history commit together. In our failed pair, the urgent priority did not survive on its own.

Consistency means the data stays valid. Declared rules are part of that, like the primary key that rejected the copy of event 5001. But look at the second row of the table: correct application logic is part of it too. The zero-row update showed that valid statements can still fail to record the intended assignment. And do not mix this up with the other "consistency" you will hear about later, when a replica sees a new value.

Isolation is about concurrent work. When several sessions run at once, what can each one see, and what happens when they conflict? That is Day 2.

Durability means a successful commit survives the failures the system is configured to handle. It does not mean the data can never be deleted. An authorized delete later is itself a durable transaction. That is one reason backups and recovery still matter.

Now read the line at the bottom. A transaction covers database effects only. If your program sends an email and then rolls back, that email is already in someone's inbox. And earlier in the course we saw that a sequence can leave gaps after a rollback. These limits tell you exactly which problem a transaction solves, and where the application has to do more.

[Sources]
- Course Chapter 5, ACID and rollback boundaries.
- https://www.postgresql.org/docs/15/wal-intro.html

## Slide 9

Here is Lab 1. You work alone, in a schema called transaction_lab, which holds copies of the source tickets and events. The setup also adds the primary keys explicitly, because CREATE TABLE AS copies the data but not every constraint, and the failure test needs that key.

Your assignment goes to Agent 201, user 201, and your event is 5999. First check that ticket 1004 is unassigned and new. Run the rehearsal ending in ROLLBACK and confirm nothing stuck. Then run the committed version and confirm that it did.

Next, the failed pair. Change the priority and copy event 5001 again. You get the duplicate-key error. Run ROLLBACK separately, then check that the new priority is gone while Agent 201's assignment and event 5999 are still there.

Last, the outdated request. Another screen still thinks the ticket is new and tries to assign it to Agent 202. The UPDATE requires status new, but you already moved it to in_progress, so it returns no rows and raises no error. The SELECT still shows 201. We write no event, because nothing was assigned.

In short SQL comments, explain why the update and insert must commit together. Add one sentence for the developer: check the returned ticket before writing history or announcing success. An empty result could mean an outdated status or a missing ticket, so look at the current record.

To see every result, use the Colab helper in the lab. Submit one file, week_05_transaction_outcomes.sql.

[Sources]
- Week 5, Lab 1: Assign a Ticket and Record Its History Together.
- https://www.postgresql.org/docs/15/sql-createtableas.html
- https://www.postgresql.org/docs/15/sql-update.html

## Slide 10

Welcome back. On Day 1 we stayed on one connection and asked where the boundary around related changes belongs. Today we keep the same habit of checking the actual stored state, but now there is more than one session: separate connections whose transactions overlap in time.

The setup is deliberately tiny. Session A changes a ticket's priority and leaves its transaction open. Session B wants to change the same ticket's status. A third connection just watches. Small enough that we can account for every value.

Look at the two lines on the slide. A reader can see committed data while a second writer waits. Those are two different behaviors, and we take them one at a time. A plain reader gets a committed version of the row even while A's change is uncommitted. A second writer is different. It has to coordinate with the transaction that is already changing that row, so it waits.

Then we capture that wait, release A, and inspect the final ticket. In the lab you change just one thing, how A's transaction ends, and run it again. Read the line at the bottom: you compare two ways to end the blocking transaction. Both endings let B finish, but they keep different data.

The notebook handles the connections and the concurrency. You do not need to learn thread programming. Your job is to follow the SQL, predict the result, and explain what you saw.

[Sources]
- Course Chapter 5, Waiting Is a Relationship Between Sessions.

## Slide 11

Let's be precise about what a session is. A database session is the server-side context for one connection. Its transaction state belongs to that connection alone. So even if the same person opens two connections with the same database role, they are independent. A's open transaction is A's business, not B's.

Look at the three boxes. Session A changes the priority and leaves it uncommitted. Session B changes the status and waits for the same row. The diagnostic connection reads activity and blocking relationships. Why a third one? Because a connection stuck waiting for its own command cannot also be used to look around. You need a free observer.

Now read the line under the boxes. A browser tab is not necessarily a persistent database session. That is why we do not do this with two editor tabs. The notebook opens and labels three connections through Supabase's Session pooler. Session mode keeps each connection tied to one database session. A transaction pooler hands connections around between transactions, which would break exactly the things we are trying to observe.

The fixture is separate too. Look at the bottom: lock_lab.tickets, row 1004, medium and open. That is not the Metro Support ticket from Day 1, and that is on purpose. One priority change and one status change, nothing else. Use the starting row the notebook prints, not values from memory.

Run this only in your own practice project. Setup recreates the disposable schema, and cleanup removes it.

[Sources]
- Notebook 02 connection and fixture code.
- https://supabase.com/docs/guides/database/connecting-to-postgres

## Slide 12

MVCC stands for multi-version concurrency control, and it explains the first surprise of the day. When A updates a row, PostgreSQL does not overwrite the only copy. It keeps row versions, and it decides which version each read is allowed to see.

Look at the two boxes on top. The committed version of 1004 is medium and open. A's update creates a new, uncommitted version: high and open. Now look at the two boxes below. A sees its own change, high, because a transaction always sees its own earlier writes. But an ordinary reader on another connection sees medium and open. It does not wait for A, and it does not see A's uncommitted value just because A already got an update result back.

The notebook runs that reader before B even starts, so you can compare both observations directly. B's update waiting for the row is a separate behavior, which we get to in two slides.

Two things MVCC is not. It is not two tickets. These are internal versions of one logical row. And read the line at the bottom: old versions are not a permanent event archive. Database maintenance reclaims versions that nobody can see anymore. If you need a lasting record of what changed, you store it on purpose, like the events table from Day 1.

Also, a long-running transaction can keep old versions relevant and get in the way of that cleanup. One more reason to finish transactions promptly.

[Sources]
- Course Chapter 5, MVCC Lets Readers and Writers Coexist.
- https://www.postgresql.org/docs/15/mvcc-intro.html

## Slide 13

This slide uses a separate thought experiment, so read the line at the top. A reads the priority and gets low. Then B changes it to high and commits. A has not finished its transaction, and it reads the row again. Does A see high or low? It depends on A's isolation level.

First row, Read Committed, which is PostgreSQL's default. Each statement starts a new snapshot, so A's second read sees high. That suits a live work queue. But it means two reads inside one transaction can disagree.

Second row, Repeatable Read. A's snapshot was established by its first data statement, so the second read still shows low. B's high value did not vanish. Look at the note at the bottom: a fresh transaction would see it. A is simply still reading from its earlier snapshot.

Third row, Serializable. You also get a stable view, but the stronger point is that PostgreSQL may reject combinations of decisions that could not have happened in some one-at-a-time order. When it does, the application has to retry the whole transaction. Stronger isolation does not mean nothing ever fails.

For today's lab, use the notebook's ordinary default. You do not have to implement all three levels. What you should be able to explain is why a later read might differ from an earlier one, and why a stable snapshot alone does not guarantee every business rule. Chapter 5's on-call example explores that last point.

[Sources]
- Course Chapter 5 isolation comparison and on-call example.
- https://www.postgresql.org/docs/15/transaction-iso.html

## Slide 14

Now the writer. Read the two code blocks as two different connections. On the left, A begins, sets ticket 1004's priority to high, and then just stays there, uncommitted. On the right, B begins and tries to set the same ticket's status to in_progress.

Notice that they change different columns. That does not matter. They change the same row, and a row change has to wait for another transaction's uncommitted change to that row. So B waits, before it ever reaches its COMMIT. The fact that a reader could see medium and open a moment ago gives a second writer no permission to skip that coordination.

Now look at B's SET LOCAL statement_timeout line. That is a safety limit for the exercise, so B cannot wait forever. It is not a fix. Read the note at the bottom: a timeout in B would not end A's transaction. If B times out, A is still holding its uncommitted change.

The notebook's code differs from the slide in small details. It sets B's fifteen-second timeout for the whole session, it adds RETURNING so you can see the row, and it gives A its own idle-in-transaction timeout as a second safety net. The mechanism is the same. It runs the sequence in one cell: B waits in a small background worker, while the main code captures the activity, ends A's transaction, and waits for B to finish. Use the notebook rather than pasting these blocks into browser tabs.

[Sources]
- Notebook 02 controlled concurrency code.
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 15

So B is stuck. How do we see that? We ask PostgreSQL. pg_stat_activity is a view with one row per server process: what it is doing, and what it is waiting on.

Read the SELECT list. pid, application_name, and state. Then wait_event_type and wait_event, which say what kind of thing it is waiting for. Then the important one, pg_blocking_pids of pid, which returns the process IDs preventing this session from continuing. And transaction_age, the clock time now minus the moment the transaction started.

Read the note on the right. A PID is a process identifier on the database server. It is not a ticket ID and not a user ID. You should never take a number from a slide and use it as the target of a command.

The WHERE clause here filters by the application names the notebook gave its connections. The notebook goes one step further, as the bottom note says. It narrows the query to the two exact PIDs it just opened, so another practice session with a similar name cannot get mixed in, and it passes those values as parameters instead of gluing text into the SQL.

Transaction age helps you tell a brief, normal overlap from something old and forgotten. But age alone does not tell you whether to commit or discard. You still need the owner, the purpose, and the data consequences. And what you can see depends on permissions. Hidden details are not a reason to grant broad access.

[Sources]
- Notebook 02 diagnostic query.
- https://www.postgresql.org/docs/15/monitoring-stats.html
- https://www.postgresql.org/docs/15/functions-info.html

## Slide 16

Here is what that query returns. These PIDs are illustrative. They match the supplied teaching trace, not your server. Start with the second row, B, PID 7332. State: active. Wait: Lock, transactionid. Active means the backend is in the middle of a command. It does not mean the command is making progress. B is active and stuck at the same time.

Now look at B's last column. Blocking PIDs: 7310. That points to A. Look at A's row, PID 7310. State: idle in transaction. A is waiting for its client to send the next command, but its transaction is still open. So "idle" does not mean harmless here. The idle one is the one holding everybody up.

A's blocking list is empty. That only says this observation does not show A waiting on anyone. It does not say A holds no locks. In fact A's uncommitted change is exactly what B is waiting for. Direction matters: B waits for A, not the other way around.

Compare the two wait descriptions. A's ClientRead means it is waiting for input from its client. B's lock wait means it is waiting for another transaction to end. So a session can be waiting in one sense and blocking in another.

The notebook captures both rows while the wait is real, then releases A before showing you the snapshot. In your write-up, be clear about that timing. You observed a captured wait. You are not claiming the relationship still exists after cleanup.

[Sources]
- Notebook 02 illustrative trace and captured activity fields.
- https://www.postgresql.org/docs/15/monitoring-stats.html

## Slide 17

Now the payoff. In both rows of this table, B is already waiting to change the status. The only difference is what A does with its proposed high priority.

First row: A rolls back. Its priority change is discarded, the row lock is released, and B completes its status update and commits. Run the query at the bottom and you get medium, in_progress. We kept B's change and lost A's.

Second row: A commits. Now high is part of the committed row. B proceeds on the version that remains after A finishes. Since B changes only the status, the final row is high, in_progress.

Read the line at the bottom. B finishing establishes progress. The row values show which changes survived. If all you report is "the spinner stopped," you have not said which data decision you made. In both cases the application started working again. In one of them, somebody's priority change quietly disappeared. That is why an incident update has to include the stored result.

One caution. These outcomes hold for this starting row and this SQL. They are not a rule that a waiting statement always succeeds once its blocker commits. A concurrent delete, a condition that no longer matches, another error, or a different isolation level could change what B gets. For the lab, hold everything else constant and change only A's decision. Then the difference between your two runs has exactly one explanation.

[Sources]
- Notebook 02 controlled fixture and two transaction endings.
- https://www.postgresql.org/docs/15/transaction-iso.html

## Slide 18

People call both of these situations "a slow query," and they need completely different checks. Look at the table.

First row: a lock wait with a blocker. The query is not slow because it is doing a lot of work. It cannot proceed, because another transaction has not let go. So the useful next check is about that transaction: its owner, its state, its age, and the operation that is waiting. But look at the last column. None of that establishes that the blocker should be killed.

Second row: a long-running query that is not in this lock wait. Now you look at the plan, the work performed, and I/O and other waits. And the last column says that no lock wait does not prove the query is using CPU efficiently. We learn to read plans and choose indexes in Week 7.

Read the first line at the bottom. An index cannot release another session's open transaction. If B is blocked by A, no amount of tuning B fixes that.

And canceling is different from ending a connection. A cancel request stops a running command. An idle-in-transaction session may have no command to cancel. Terminating the connection is a stronger action, and it discards uncommitted work. Our experiment does neither blindly. It uses A's own connection to make an explicit decision. A diagnostic function identifies a dependency. It does not give you the authority to decide what happens to someone else's work.

[Sources]
- Course Chapter 5, Safe Incident Communication.
- https://www.postgresql.org/docs/15/functions-admin.html

## Slide 19

Everything so far has been a one-direction wait. B needs A. A does not need B. So when A ends, the dependency is gone. A deadlock has a different shape.

Follow the boxes. A already holds ticket 1001 and now requests ticket 1002. B already holds ticket 1002 and now requests ticket 1001. So A waits for B, and B also waits for A. Follow the arrows and you come right back to where you started. That cycle is the whole idea. Read the middle line: neither can finish by waiting alone.

So PostgreSQL detects the cycle and aborts one of the transactions, which lets the other proceed. The application has to catch that error and, when it makes sense, retry the complete transaction with fresh data. Look at the last line: retries must restart the transaction. Retrying only the final statement loses the earlier decisions that belonged with it.

How do you prevent this particular pattern? Consistent lock order. If every operation that needs both tickets takes them in the same order, this opposite-order cycle cannot form. That is not a promise that no deadlock can ever happen in a large system, but it is a concrete rule you can tie to this picture.

This is the optional Deadlock Detective activity in the README. Draw the wait-for graph and explain it on paper. It is ungraded and adds no submission, and you should not create a real deadlock in a shared database.

[Sources]
- Week 5 optional wait-for graph activity.
- https://www.postgresql.org/docs/15/explicit-locking.html#LOCKING-DEADLOCKS

## Slide 20

Before you run anything, let's be clear about how the pieces fit, because three different things are involved. Look at the table. Lab 2 is the assignment: compare rollback and commit. The Colab notebook, Notebook 02, holds the supplied Python and SQL cells and the space for your writing. Colab runs it in a hosted Python runtime. And your Supabase project hosts the PostgreSQL database those cells connect to. The notebook talks to that database over three separate connections.

Now the steps. Open the Lab 2 page from the Week 5 README and click Open in Colab. Then choose File, Save a copy in Drive. Work in your copy, so your two results and your comparison stay saved. Keep your existing course project open in a separate Supabase tab. You do not need a new project or another copy of the Metro Support dataset.

The Supabase SQL editor lives inside your project, so it can already reach the database. Colab runs somewhere else, so it needs connection details. Read the line at the bottom: run today's code in Colab. Do not paste Python into the SQL editor, and do not treat two browser tabs as two controlled database sessions. The notebook opens and labels the real connections.

The notebook's First-Time Setup section near the top walks through all of this before it asks for any credential. It creates its own lock_lab row, medium and open. The Lab 1 event IDs do not matter today.

[Sources]
- Week 5, Lab 2 and Notebook 02 introduction.
- https://research.google.com/colaboratory/faq.html

## Slide 21

Now the connection string. In your Supabase course project, click Connect, choose Session pooler, and copy the PostgreSQL URI. It begins with postgresql, colon, slash, slash. The project's HTTPS API URL and its API keys belong to a different interface, and they will not work here.

Keep the host, port, and username exactly as you copied them. Replace the literal text YOUR-PASSWORD, in square brackets, with the database password for that project. That is not the password you use to sign into the Supabase website. If you do not know your database password, stop and sort that out first.

Look at the box on URL encoding. Some characters mean something special inside a URL. If your password has an at sign, write %40. A hash becomes %23, and a percent sign becomes %25. Encode only the password, and only once. A malformed URL can fail before PostgreSQL even checks your password.

Next, encryption. Look at the before and after. If the URL ends in slash postgres with nothing after it, add question mark sslmode equals require. If it already has a query, add ampersand sslmode equals require instead. If sslmode is already there, set it to require or keep verify-ca or verify-full, but never add it twice. Require encrypts this classroom connection without verifying the server's hostname. Production uses verify-full with the proper certificate.

And the bottom line: paste the finished URL only into Colab's hidden connection prompt.

[Sources]
- Notebook 02 connection validation.
- https://supabase.com/docs/guides/database/connecting-to-postgres
- https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS
- https://www.postgresql.org/docs/current/libpq-ssl.html

## Slide 22

Back in your Colab copy, find the configuration cell near the top and look at the two flags on the slide. Set USE_CLOUD to True. Leave KEEP_A_CHANGE as False for the first run. That is the rollback case. The notebook ships with USE_CLOUD set to False, which skips every connection and shows an offline trace. Seeing that trace does not mean you connected.

Run the code cells one at a time from the top: the install cell, the configuration cell, then the connection cell in Section 1. It says Paste the temporary PostgreSQL connection URL. Paste your URL into that hidden box and press Enter.

Look at the success box. Continue only when you see Opened Session A, Session B, and the diagnostic session. Then Section 2 builds the disposable table and prints Starting row: 1004, medium, open. Two separate checkpoints from two cells. If the connection fails, stop there and check the URL, the database password, and the SSL setting.

Then the bottom of the slide. Section 4 runs the experiment: it captures B waiting, rolls A back, and waits for B to finish. Section 5 shows the blockers, and under B, blocking_pids should contain A's PID. Section 6 shows the final row, 1004, medium, in_progress. Run Section 7 cleanup. Then change only KEEP_A_CHANGE to True and rerun from configuration through cleanup. You should get 1004, high, in_progress. Both runs succeed. There is no duplicate-key error in this lab.

[Sources]
- Notebook 02 configuration, connection, setup, experiment, diagnostic output, final state, and cleanup cells.

## Slide 23

Here is Lab 2. It is individual work in Notebook 02, and you compare two endings of the same controlled wait.

Start with the rollback case. Follow the captured relationship from B's PID to A's PID, and keep the final priority and status for your comparison. Do not decide who is blocking whom by which row prints first. The blocking_pids result establishes that.

Before the second run, write down your prediction. What will the row look like if A commits? Then change the setting, rerun from configuration through cleanup, and compare the actual row with your prediction. B's statement never changes. Then explain why B finishes both times but the final priority differs.

Then, in the final Markdown cell, complete the comparison table and write a short update to the developer whose status update looked stuck. Use one run's actual PIDs to explain the wait, and use your comparison to explain what the transaction choice did to the data. No incident form and no screenshots.

If you cannot get a connection, the notebook includes a supplied trace. Label the rollback result as a supplied trace and the commit result as an unexecuted prediction, and tell me, so we can arrange a connection demonstration. A trace is practice, not proof of a live session.

To submit, save your copy in Colab, use Share to give me viewer access, and put that sharing link in Brightspace. Run cleanup after each experiment, and make sure no credential was saved in the notebook.

[Sources]
- Week 5, Lab 2: The Query Finished, but Which Change Survived?

## Slide 24

Here is what a useful update looks like, for the rollback case. "The status update waited for A's uncommitted change to the same ticket." That names what was stuck and why. "The captured result showed B's PID blocked by A's PID." That is the evidence. "Rolling back A let B finish: priority stayed medium and status became in_progress." That is what happened to the data.

Three sentences, and each one does a job: what waited, how we know, and what was stored.

Look at the bottom line of the slide. Use the real PIDs from your run, or say clearly that you used the supplied trace and an unexecuted prediction. Do not invent numbers to make it look like an incident report.

Now the middle box. Your comparison adds the commit case. B still finishes, but now the high priority remains. That is the point: choosing how to restore progress also chooses what happens to somebody else's proposed change.

So say why you could not choose blindly in a real application. You would want to know whether that priority change was valid, who owned the transaction, and whether other work belonged to it. You might contact the owner or follow an established procedure rather than decide from a process list.

This is also how you talk about it in an interview. Not "I know PostgreSQL locks," but the test you ran, the function you used, the outcomes you verified, and the limits of your conclusion.

[Sources]
- Course writing guide, Write an Incident Update.
- Notebook 02 lab comparison.

## Slide 25

Let's pull the week together. Read the line in the middle of the slide: a successful statement, a finished query, and a correct application outcome are different claims. They sound alike, and each one needs its own check.

On Day 1 we put an assignment and its history in one transaction. We watched rollback and commit, and we saw a failed statement keep a new partial change from persisting. We also separated a real SQL error from a valid update that matched zero rows, which is why transaction boundaries still need correct application logic around them.

On Day 2 we opened independent sessions. A reader saw the committed row while another connection held an uncommitted version. A competing writer waited, and pg_blocking_pids showed exactly which transaction it was waiting for. Rolling back or committing A both let B finish, but the final priority revealed two different data decisions. Look at the top of the slide: the database showed us what committed, what another session could see, and which transaction prevented progress.

The vocabulary organizes those observations. MVCC explains what readers see. Isolation decides which snapshot a read uses. Locks coordinate conflicting work. A wait-for cycle is what makes a deadlock different from the one-way wait we created.

Next week, as the bottom of the slide says, roles and permissions determine who may perform each operation. Same discipline: act as the intended identity, observe what the system actually allows, and verify before you claim.

[Sources]
- Course Chapter 5 and Week 5 individual labs.
- Course Chapter 6 preview, Access Should Be Useful and Limited.

## Slide 26

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: One assignment, one transaction (1:28); Row versions and snapshots (1:22); Who is waiting on whom? (1:28). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 5 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
