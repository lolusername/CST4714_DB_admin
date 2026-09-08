# Week 5: Transactions, MVCC, and Locks - Spoken Transcript

## Slide 1

So far, we have used rollback to rehearse changes and we have checked whether individual rows satisfy rules. Today we connect those ideas to an application action that changes more than one record. Assigning a repair request changes the ticket, but it also creates history. A useful system needs those two facts to agree.

Our first meeting follows one assignment from its starting state through a rehearsal, a committed result, and a failed attempt. We will read actual SQL and compare stored values. You will not need to invent a transaction framework or learn a new programming language to complete that lab. The statements are familiar. The new question is where their common decision boundary belongs.

In the second meeting, we introduce independent database sessions. One session changes a ticket's priority while another tries to change its status. We will see why an ordinary reader can still obtain a result while the second writer waits. Then we will compare two ways to end the transaction that is holding up the writer.

The important distinction throughout the week is between the command we issued and the result we established. An update can return a row before anything commits. A query can finish while keeping the wrong business outcome. The database gives us ways to inspect those differences. Our job is to read them and explain what they mean for the application.

[Sources]
- Course textbook, Chapter 5, Transactions Coordinate Competing Work.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 2

Here is the assignment we will use in the demonstration. Ticket 1004 starts without an assignee, and its status is new. We want to assign it to Noah, whose user identifier is 202, and change the status to in progress. Those are changes to the current ticket row.

The second record is an event. Event 5998 does not yet exist. It will say that this assignment happened, identify the actor, and record the old and new statuses. The ticket answers who is responsible now. The event explains how the ticket reached that state. These records serve different purposes, so keeping history does not mean that we should remove the current state from the ticket.

Imagine that we update the ticket successfully and then lose the connection before inserting the event. A staff member might see Noah as the assignee, while someone reviewing the history finds no corresponding assignment. Each table could still contain individually valid rows. The application action would nevertheless be incomplete.

A transaction gives us a place to say that these related changes belong together. That statement is about the application meaning of the work. PostgreSQL does not automatically know that any two nearby SQL commands should share a decision. We have to define the boundary. In the student lab the assignee and event identifier differ, and the tables are disposable copies, but the relationship between current state and recorded history is the same.

[Sources]
- Course Metro Support fixture and Chapter 5 assignment example.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 3

Read this diagram as a choice of endings. Begin opens an explicit transaction. We then perform the update and insert, and we can inspect our work from that connection. If the operation is ready to keep, commit completes it. If we decide to discard the uncommitted work, rollback completes it instead.

Commit and rollback are not consecutive steps in a checklist. Once the transaction has committed, issuing rollback afterward does not take us back to the original rows. Correcting a committed mistake generally requires another change, using the facts we now know. That connects directly to last week's distinction between rehearsing a migration and repairing a system after it has collected new data.

There is also a difference between a transaction and the interface displaying it. Closing a window is not a reliable substitute for issuing the appropriate transaction command. A client may keep a connection alive, and an open transaction can retain resources even while no person appears to be working.

For our first SQL demonstration, we will run the whole block and end with rollback. That keeps the shared source fixture unchanged. In your lab you will use an isolated copy and deliberately keep the approved assignment with commit. When you inspect your results, always attach the observation to a point in this diagram. A value visible while work is open is not the same observation as a value returned by a new query after the transaction ends.

[Sources]
- Course Chapter 4 and Chapter 5 transaction-boundary discussion.
- https://www.postgresql.org/docs/15/sql-commit.html
- https://www.postgresql.org/docs/15/sql-rollback.html

## Slide 4

This is the complete rehearsal, starting from the supplied fixture. Begin opens the transaction. The update identifies ticket 1004 and also checks that its current status is new. The status condition expresses the transition we intend: assign a request that has not yet moved into progress.

The set clause changes the assignee to Noah and the status to in progress. Returning asks PostgreSQL to send back the affected ticket identifier, assignee, and status. For this fixture, that result is 1004, 202, and in progress. It lets us inspect the row changed by this statement.

The insert then creates event 5998. Read its column list together with its values. The event belongs to ticket 1004, actor 202 made the change, and the old and new status fields describe the transition. The note is explanatory text, and now supplies the transaction timestamp. We use a fixed event identifier to keep the classroom example easy to inspect. A real application would normally generate identifiers and manage retries explicitly.

The final rollback discards both changes. Run this as one complete block in the editor so the transaction does not remain open while we discuss it. PostgreSQL may show a successful command or a returned row before that final decision. Neither means the assignment has been retained. We will establish the outcome with fresh queries next. Also notice that this demonstration uses the source schema, while the lab creates separate copies before it commits anything.

[Sources]
- Course Chapter 5 worked assignment and Metro Support fixture.
- https://www.postgresql.org/docs/15/dml-returning.html

## Slide 5

The table separates three observation points. Inside the transaction, our connection sees Noah's assignment and, after the insert, the new event. Those changes are available to our own transaction even though we have not committed them.

After rollback, a fresh query shows the original ticket: no assignee and status new. Querying event 5998 returns no row. Rollback did not replace the event with a blank event. It discarded that insertion, so the record does not exist.

The last row describes the alternative ending. If we run the same successful pair from the same initial state and commit, the ticket and event both remain. This is a comparison of two possible completed transactions, not a suggestion to append commit after the rollback we just ran.

The queries at the bottom inspect the specific objects we changed. Counting all tickets would not answer whether the assignment survived because an update does not necessarily change the number of ticket rows. Similarly, counting all events would be less precise than asking for the particular event identifier. We want a check whose result directly answers the claim.

In your SQL file, a brief comment can record these observations. You do not need a separate report for each query. What matters is that someone reading the file can distinguish the value returned during the transaction from the state that persisted after it ended. That distinction will also help when we introduce concurrent readers in the second meeting.

[Sources]
- Course Chapter 5 and the actual assignment rehearsal.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 6

Now we deliberately make the second statement fail. The update proposes changing ticket 1004's priority to urgent. The next statement attempts to insert a copy of event 5001 back into the same event table. That event already exists, including its primary key, so the insert violates the uniqueness rule.

The insert-select form here is simply a compact way to copy an existing row with all its required values. It is deliberately wrong for this test. We expect PostgreSQL to reject it with SQLSTATE 23505, a unique violation. Rejection is the useful result because it lets us investigate the transaction boundary around the earlier update.

After the error, run the lower block separately. Rollback ends the failed transaction, and the select checks the priority. It should still be low. The earlier urgent update was inside the same transaction as the rejected insert, so that proposed change did not become a separate committed fact.

An editor may stop execution when it encounters the error. That is why the rollback is a separate action here, rather than an instruction to assume the rest of a batch ran. If the client has already ended the failed transaction, the extra rollback may report that no transaction is active; the final query still establishes the result.

The failure does not erase event 5001. It rejects a new duplicate and leaves the earlier committed event intact. In the lab you will make the same distinction using your already approved event and a new proposed priority change.

[Sources]
- Course Chapter 5 failed-transaction explanation.
- https://www.postgresql.org/docs/15/errcodes-appendix.html
- https://www.postgresql.org/docs/15/sql-rollback.html

## Slide 7

This update also fails to accomplish the proposed assignment, but it does so in a different sense. The where clause requires ticket 1004 to have status resolved. In our initial fixture its status is new, so no row matches. PostgreSQL can execute that request correctly and return no rows.

There is no constraint violation here. A request to update all rows satisfying a condition is allowed to match an empty set. That means a later insert in the same transaction would not automatically be stopped merely because this update affected nothing.

Suppose application code ignored the returned result, inserted an event claiming an assignment, and committed. It could record an event for an assignment that never happened. Wrapping the statements in begin and commit would not invent the missing business check. The application must examine the affected-row result and decide whether to continue or roll back.

This is one reason we distinguish database errors from application outcomes. A duplicate key is an enforced-rule failure. Zero affected rows is a valid SQL outcome that may or may not satisfy what the person requested. In another workflow, doing nothing when a request has already been resolved could be exactly the desired behavior.

For this course, you do not need to build the complete retry logic yet. You do need to explain why checking returning is useful and why its absence matters. Our rehearsal still ends in rollback so the example leaves the source fixture alone. The broader habit is to connect a successful statement to the particular application fact it was supposed to establish.

[Sources]
- Course Chapter 5, Keeping State and History Together.
- https://www.postgresql.org/docs/15/sql-update.html

## Slide 8

We now have examples to attach to the four letters in ACID. Atomicity concerns the transaction boundary. In our successful pair, the assignment and history commit together. In the failed pair, the new priority does not survive on its own.

Consistency concerns maintaining valid state. Declared constraints are part of that, but application logic is also necessary. The zero-row example showed how valid statements could still fail to represent the intended assignment. Do not confuse this use of consistency with the later question of when a replica sees a new value. Those are related database topics, but they ask different questions.

Isolation concerns concurrent work. When several sessions operate at once, the selected isolation rules determine what their reads can see and how conflicting operations behave. We will make that visible with a reader and competing writer in the second meeting.

Durability concerns committed work surviving the failures covered by the system's configuration and mechanisms. It does not mean a record can never be deleted. A later authorized delete can itself be a durable transaction. That is one reason backups and recovery remain necessary.

Finally, our transaction covers database effects within its boundary. If a program sends an email before committing, a database rollback does not retrieve that email from the recipient. Last week we also saw that a sequence can leave gaps after rollback. These limits do not make transactions unhelpful. They tell us precisely which coordination problem a transaction solves and where an application needs additional design.

[Sources]
- Course Chapter 5, ACID and rollback boundaries.
- https://www.postgresql.org/docs/15/wal-intro.html

## Slide 9

Your first lab now applies the transaction example in disposable tables. The setup creates transaction_lab and copies the source tickets and events. It explicitly adds the primary keys that the failure test needs. Create table as copies query results; it does not promise to recreate every constraint or operational property of the source tables.

The proposed assignment in your lab is to Priya, user 201, and the new event is 5999. Start by checking ticket 1004's actual initial state. Run the rehearsal ending in rollback, then query the ticket and event afterward. Next, keep the approved pair by replacing that ending with commit and check the stored result again.

The last experiment starts a new transaction, changes priority, and deliberately attempts to insert the already approved event key. Run rollback separately after the expected error. Your checks should distinguish the discarded new priority from the earlier committed assignment and event, which remain.

Use short comments in the same SQL file to explain what happened. The explanation should answer why putting the update and insert in separate committed transactions could leave the application's current state and history inconsistent. It should not just say that transactions are safer.

Keep the expected-error batch clearly labeled so someone rerunning your file knows where execution pauses. If you restart the full exercise, use its disposable setup rather than resetting the source schema. There is one submission: your SQL file with the queries, observed results, and explanation. No second database session is required for this first lab.

[Sources]
- Week 5, Lab 1: Assign a Ticket and Record Its History Together.
- https://www.postgresql.org/docs/15/sql-createtableas.html

## Slide 10

In the first meeting we kept our attention on one connection and the boundary around related changes. Today we keep the same habit of checking actual state, but introduce concurrent sessions. That means separate connections whose transactions can overlap in time.

The situation is deliberately small. Session A changes a ticket's priority and leaves that transaction open. Session B wants to change the same ticket's status. A third connection observes the situation. The small fixture lets us account for every value without trying to diagnose a complicated application at the same time.

Before we look at activity views, we need to understand what readers and writers are allowed to see. An ordinary reader can obtain a committed version of the row while A's proposed change remains uncommitted. A competing update is different because it needs to coordinate with the transaction already changing that row.

We will capture that wait, release A, and inspect the final ticket. Then you will change just A's transaction decision and repeat the experiment. Both runs can restore progress, but they keep different data. That comparison is the reason the lab goes beyond identifying a process number.

The notebook supplies the connection and concurrency mechanics. You are responsible for following the SQL, predicting the result, and interpreting the captured relationship. We are not asking you to learn thread programming before you can understand a database lock. The required new skills are observing transaction state and connecting a resolution decision to its stored outcome.

[Sources]
- Course Chapter 5, Waiting Is a Relationship Between Sessions.

## Slide 11

A database session is the server-side context associated with a connection. Its transaction state is independent of another connection's state, even if the same person opened both and both use the same database role.

Session A in this experiment changes priority and remains uncommitted. Session B sends the competing status update. The diagnostic connection queries activity and blocking information without needing to borrow either worker's connection. Keeping these roles separate is useful because a connection waiting for its command to finish cannot also be used as if it were a free interactive observer.

The notebook opens three named connections and uses a Supabase session-pooler connection for this exercise. A session pool keeps a connection associated with a database session. A transaction pool has a different lifecycle, which can make session-level labels and settings unsuitable for the observations we are teaching. Two web editor tabs are not a substitute we can assume has the same behavior.

The fixture is also separate. It uses lock_lab.tickets with one row, ticket 1004, starting at medium priority and open status. That starting state is intentionally different from the full Metro Support ticket. The simplified table focuses the experiment on one priority change and one status change. You should use the starting row printed by this notebook rather than copy the source dataset's values from memory.

Only run this in your personal practice environment. The setup recreates the disposable schema, and cleanup removes it. It does not need to reset your earlier course tables.

[Sources]
- Notebook 02 connection and fixture code.
- https://supabase.com/docs/guides/database/connecting-to-postgres

## Slide 12

MVCC stands for multi-version concurrency control. Instead of treating an update as immediately replacing the only readable value, PostgreSQL maintains row versions and determines which versions are visible to a particular read.

In our experiment, the committed starting row is medium and open. Session A's uncommitted update creates a proposed high-priority version. A can see that change because a transaction reads its own earlier writes. The ordinary diagnostic reader, using its own statement, still sees medium and open. It does not have to show A's uncommitted value just because A has already received an update result.

The notebook queries that reader before starting B's competing write, so you can compare both observations directly. This is a concrete example of visibility, rather than only a definition of the acronym. We will separately observe that B's update waits for the same row. Reader visibility and writer coordination are different parts of the behavior.

These versions do not mean the application has two tickets. They are internal representations of the same logical row with different visibility conditions. They also do not replace the event history from the first lab. Old versions can become obsolete and be reclaimed by database maintenance. If the application needs a lasting record of an assignment, it must store that history deliberately.

Long-running transactions can keep old versions relevant and complicate cleanup. That gives us another reason to finish transactions promptly. The exact set of values visible across multiple reads depends on the isolation level, which is the next distinction.

[Sources]
- Course Chapter 5, MVCC Lets Readers and Writers Coexist.
- https://www.postgresql.org/docs/15/mvcc-intro.html

## Slide 13

This comparison uses a separate reasoning example. A reads a priority value of low. B then changes that value to high and commits. A has not ended its transaction and reads the row again. The question is whether that second ordinary read should use a new snapshot or retain the earlier snapshot.

At Read Committed, PostgreSQL's default, the second statement receives a new snapshot and can see high. That can be useful for an interactive queue where recently committed updates should appear. It also means that two reads inside one transaction are not guaranteed to show identical data.

At Repeatable Read, A's ordinary second read still shows low. Its snapshot was established by the first data statement. B's committed high value has not disappeared; a new transaction can see it. A is simply continuing to read from its earlier transaction snapshot.

Serializable also supports a stable transaction view, but its stronger purpose is to reject combinations of decisions that cannot fit an equivalent serial execution. Applications must be prepared to retry a transaction that receives a serialization failure. Stronger isolation does not mean every conflicting transaction will quietly succeed.

For today's lab, use the notebook's ordinary default behavior. You are not required to implement all three isolation levels. What you should be able to explain is why a later read might differ from an earlier read, and why a stable view is not the same thing as a guarantee that an entire application invariant has been encoded correctly. Chapter 5's on-call example explores that last point further.

[Sources]
- Course Chapter 5 isolation comparison and on-call example.
- https://www.postgresql.org/docs/15/transaction-iso.html

## Slide 14

Read the two SQL blocks as operations on separate connections. A begins, changes ticket 1004's priority to high, and remains uncommitted for the controlled experiment. B begins and attempts to change that same row's status to in progress. Although the two statements assign different columns, they still target the same row.

B's update must coordinate with the transaction already changing that row. It waits before it can reach commit. The fact that an ordinary reader could see medium and open did not give another writer permission to finalize a conflicting row change without that coordination.

The timeout in B bounds how long its statement can continue. It is a safety limit for the exercise, not a resolution of A's transaction. If B times out, A can still hold its uncommitted work. The appropriate cleanup must address both sessions' actual states. Do not treat a timeout message as proof that all locks disappeared.

The notebook runs the sequence inside one experiment cell, using a small background worker for B. The main execution path captures the activity result, ends A's transaction, and waits for B to finish before returning. This avoids asking you to leave a transaction open while reading the next page of instructions.

The code shown here explains the SQL mechanism. Use the notebook rather than copying these blocks into arbitrary browser tabs. That way we know the connections are distinct and can ensure the demonstration finishes its own work. Afterward, the saved output remains available for careful interpretation without leaving the ticket blocked.

[Sources]
- Notebook 02 controlled concurrency code.
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 15

The activity view describes database processes and their current state. This query selects the PID, application name, activity state, wait information, and transaction age. It also asks pg_blocking_pids to identify processes preventing the selected session from continuing.

A PID is a process identifier, not a ticket identifier or user identifier. The result belongs to a particular observation of a running server. You should not expect another student's PID values to match yours, and you should never use a number from this slide as a command target.

The application names help us label the demonstration. The notebook goes further and filters by the two exact PIDs associated with the connections it just opened. That prevents another similarly named practice session from being mistaken for this run's session. It supplies those values through parameter placeholders rather than assembling SQL by concatenating text.

Transaction age is calculated relative to the capture time. It can help distinguish a brief, expected overlap from unexpectedly old work, but age alone does not decide whether a transaction should be committed or discarded. We still need ownership, purpose, and data consequences.

Access to activity details depends on permissions and managed-service settings. Missing query details are not a reason to grant broad access indiscriminately. In this personal exercise the connections use the same course identity. In an operational environment, a designated monitoring role and appropriate handling of query text would be part of the design. The next slide shows how to interpret the important relationship without confusing activity with progress.

[Sources]
- Notebook 02 diagnostic query.
- https://www.postgresql.org/docs/15/monitoring-stats.html
- https://www.postgresql.org/docs/15/functions-info.html

## Slide 16

These PID values are illustrative and match the teaching trace rather than your current server. Start with B. Its state is active, but its wait is a lock wait on a transaction identifier. Active means the backend is executing a command; it does not guarantee that the command is currently making progress or consuming CPU.

The blocking-PID result for B contains 7310. That points to A. A is idle in transaction: it is waiting for another client command while its transaction remains open. This is why the word idle must not be interpreted as having no effect on other work.

The empty blocker list for A says that this observation does not show A waiting on another process. It does not say that A holds no locks. In this experiment A's uncommitted row change is precisely what B needs to wait for. The direction of the relationship matters: B waits for A, not the other way around.

ClientRead is a different wait description from B's lock wait. A is waiting for input from its client. B is waiting for a database transaction dependency to end. A session can therefore be waiting in one sense while also acting as a blocker in another.

Your notebook captures both rows while the relationship is real, then releases the transaction before displaying the saved snapshot. When you write your explanation, make that timing clear. You observed a captured wait; you are not claiming the same PID relationship still exists after cleanup. We then use the final row to establish which changes survived the resolution.

[Sources]
- Notebook 02 illustrative trace and captured activity fields.
- https://www.postgresql.org/docs/15/monitoring-stats.html

## Slide 17

The two rows describe the experiment you will compare. In both cases B is already waiting to change status. The difference is what A does with its proposed high priority.

If A rolls back, its priority change is discarded. That releases the row lock, and B can complete its status update and commit. A fresh query shows medium priority and in-progress status. We kept B's change but not A's proposed change.

If A commits, the high priority becomes part of the committed row. B can then proceed with its update on the row version that remains after A completes, subject to the operation's condition. In this small fixture, B targets the same ticket identifier and changes only status, so the final row shows high priority and in-progress status.

Neither outcome follows merely from saying that B finished. Both restore progress. Only inspecting the columns tells us which data decision we made. That is why an incident update should include verification of the stored result rather than ending with the statement that the spinner stopped.

These outcomes use the stated starting row and this particular SQL. They are not a rule that any waiting statement will always succeed after a blocker commits. A concurrent deletion, a condition that no longer matches, another error, or a different isolation level could change the result. For the assigned lab, hold those other factors constant and change just A's decision. The comparison then has a clear explanation instead of several competing causes.

[Sources]
- Notebook 02 controlled fixture and two transaction endings.
- https://www.postgresql.org/docs/15/transaction-iso.html

## Slide 18

People often describe both situations as a slow query. One command might be doing a large amount of necessary or unnecessary work. Another might be unable to proceed because a different transaction has not released what it needs. The same user-visible delay can therefore call for different investigations.

If we observe a lock wait and a blocking PID, we first inspect the relevant transaction and its ownership. Adding an index does not make an already open transaction release its lock. It might reduce the duration of future work in some cases, but it is not the direct resolution of this captured dependency.

If we do not observe this lock wait, that does not prove the query is healthy or actively using CPU. It may be waiting on I/O, returning data to a client, or moving between different execution phases. Plans and work measurements help with those questions. We will study query plans and indexes later, so today we are learning to separate categories of observation rather than to tune every possible delay.

Also distinguish canceling a command from ending a connection. A cancellation request targets running work. An idle connection with an open transaction may have no command available to cancel. Terminating a connection is a stronger action and can discard uncommitted work. Our controlled experiment does neither blindly: it uses the known owner connection to make an explicit transaction decision.

That boundary is part of the skill. A diagnostic function can identify a dependency, but it does not supply authority or decide whether the business operation should be retained.

[Sources]
- Course Chapter 5, Safe Incident Communication.
- https://www.postgresql.org/docs/15/functions-admin.html

## Slide 19

Our notebook creates a one-direction wait: B needs A to finish. A is not waiting for B, so ending A's transaction can release the dependency. A deadlock has a different shape.

Here A already holds the row for ticket 1001 and next requests ticket 1002. B already holds ticket 1002 and next requests ticket 1001. A cannot get its next resource until B releases it, and B cannot get its next resource until A releases it. Follow the two arrows and you return to the starting session. That cycle is the key idea.

Simply asking both transactions to wait longer cannot solve this arrangement. PostgreSQL detects deadlocks and aborts one transaction so the other can proceed. Application code must handle the error and, when appropriate, retry the complete transaction using fresh state. Retrying only a final statement can lose the relationship to the earlier decisions that belonged to the transaction.

One prevention technique for this pattern is consistent lock order. If operations that need both tickets acquire them in the same order, they do not create this particular opposite-order cycle. That is not a promise that every possible deadlock in a larger system disappears, but it is a concrete design rule connected to the diagram.

The optional extension asks you to draw and explain this relationship. You do not need to create a deadlock on a hosted project to understand it, and it is not another required submission. The required live lab remains the simpler blocker-and-waiter case so its data outcomes stay easy to account for.

[Sources]
- Week 5 optional wait-for graph activity.
- https://www.postgresql.org/docs/15/explicit-locking.html#LOCKING-DEADLOCKS

## Slide 20

This is the setting you will change in the notebook. Use cloud must be true for the connection experiment to run. Keep A change is initially false, meaning A rolls back. For your second run, change only that second setting to true. The table setup and B's SQL should remain unchanged so that the comparison isolates A's decision.

Download Notebook 02, open Colab, and use File, then Upload notebook. In Supabase, use the Connect dialog's Session pooler connection for this exercise. Follow the notebook's SSL instructions and enter the connection URL only when the hidden prompt appears. Do not paste a password-bearing URL into a code cell or a Markdown explanation.

The notebook contains more mechanics than you need to write yourself. It opens labeled connections, starts B's work in a background worker, observes the actual blocking relationship, and ends A before waiting for B to finish. Its cleanup path is designed to avoid leaving a row blocked while you study the output.

Read the SQL and the explicit commit-or-rollback decision carefully. The concurrency scaffolding is supplied so you can investigate database behavior without first building a concurrent client application. That is different from ignoring what the notebook does. You should still be able to identify which connection writes, which one observes, and where each transaction ends.

Keep your first result in the final Markdown cell before rerunning. Notebook output is replaced as cells execute again, while the Markdown comparison can preserve both observations. Run cleanup after each experiment.

[Sources]
- Notebook 02 configuration and controlled experiment.
- https://supabase.com/docs/guides/database/connecting-to-postgres

## Slide 21

Your individual lab compares two resolutions of the same controlled wait. Start with the rollback case, follow the captured relationship from B's PID to A's PID, and keep the final priority and status in the comparison cell. The order of rows in the output is not the definition of which session blocks another; the blocking-PID result establishes that relationship.

Before the second run, predict what will remain when A commits. Then change the setting, rerun the experiment from configuration through cleanup, and compare the actual row with your prediction. B's statement stays the same. Explain why the final priority differs even though B completes in both cases.

Your short writing addresses the developer whose status update appeared stuck. Use one run's observed relationship to explain the wait and use the comparison to explain the consequence of the transaction choice. You do not need to fill out a separate incident form or provide a collection of screenshots.

If a connection is unavailable, the supplied trace supports a different kind of practice. Label the rollback observation as a supplied trace and the commit result as an unexecuted prediction. Tell me that you used that path so we can arrange a connection demonstration. Interpreting a trace is useful, but it is not proof that you opened or administered a live session.

Submit the completed notebook with the comparison and explanation in its final Markdown cell. Confirm cleanup ran and remove any accidentally saved credential. The database result and your reasoning belong together in this one artifact.

[Sources]
- Week 5, Lab 2: The Query Finished, but Which Change Survived?

## Slide 22

This short update explains the rollback case in ordinary technical language. It identifies the status update as the waiting operation, ties the wait to A's uncommitted change of the same row, and points to the captured PID relationship. Then it states what happened to the actual data after A rolled back and B committed.

The placeholders for A's and B's PIDs are not numbers to invent. Use values from your executed run, or identify the supplied teaching trace. We want the explanation to reflect how the conclusion was obtained rather than imitate the appearance of an incident report.

Your comparison adds the consequence of committing A. B still completes its status update, but the high priority remains. That is the important addition: choosing an action to restore progress also chooses what happens to somebody else's proposed data change.

In a real application, we would need to know whether that priority change was valid, who owned the transaction, and whether other work belonged to the same operation. We might contact the owner or follow an established operational procedure rather than decide from a process list alone. You can state that limitation without pretending our classroom experiment caused or measured an actual production outage.

This kind of writing is useful in interviews as well. Instead of saying only that you know PostgreSQL locks, you can describe a controlled test, the diagnostic function you used, the different outcomes you verified, and the limit of your conclusion. That gives someone a concrete basis for asking about your understanding.

[Sources]
- Course writing guide, Write an Incident Update.
- Notebook 02 lab comparison.

## Slide 23

We can now describe several claims that initially sound similar but require different checks. A statement succeeded. A transaction committed. A waiting query finished. The application retained the intended state. Those are not interchangeable statements.

Our first lab grouped an assignment and its history into one transaction. We observed both rollback and commit, then saw that a failed statement prevented a new partial change from persisting. We also separated an SQL error from a valid update that matched no rows. That distinction explained why transaction boundaries still need correct application logic.

The second lab introduced independent sessions. A reader could see the committed row while another connection held an uncommitted version. A competing writer waited, and PostgreSQL's activity information showed the dependency. Releasing A with rollback or commit let B proceed, but the final priority revealed different data decisions.

The models and terminology help because they organize those observations. MVCC explains visibility through row versions. Isolation determines the snapshot behavior. Locks coordinate conflicting work. A wait-for cycle explains why deadlock differs from the one-direction wait we created. You do not have to memorize every lock mode to reason correctly about this example.

Next we will ask who should be allowed to perform each operation. That introduces roles, privileges, and row-level security. The same discipline carries forward: use the intended identity, observe what the system actually permits, and verify the result before making a larger claim. Your SQL file and notebook already contain concrete examples you can return to when those access-control decisions become more complicated.

[Sources]
- Course Chapter 5 and Week 5 individual labs.
- Course Chapter 6 preview, Access Should Be Useful and Limited.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
