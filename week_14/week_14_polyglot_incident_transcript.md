# Week 14: Polyglot Incident Response and Final Project Clinic - Spoken Transcript

## Slide 1

Welcome to Week 14. Look at the two lines in the middle of the slide. The staff dashboard says resolved. The resident page says open. Both screens are working. Both databases answer their own queries just fine. And they disagree. That is our problem for the week.

Our case has two stores. PostgreSQL holds the real ticket, the one staff update. MongoDB holds a copy of it arranged for the resident page. Using different databases for different jobs has a name, polyglot persistence. I want to be clear up front: that does not mean every project should use several databases. We are studying this two-store design because it makes partial failure easy to see, not because more products make a small system better.

Here is the plan. On Day 1 we trace one change from the staff click to the resident page, we look at the transaction that records it, and we experiment with events that arrive twice or arrive late. The notebook gives us a real local SQLite transaction and a small Python model of the copy, so we can see the mechanism without a message broker or another cloud account.

On Day 2 we take the same reasoning to your own final project. You pick one operational gap, like access, an index decision, or a restore check, and you close it.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08.

## Slide 2

Three terms on this table, and the whole week leans on them.

The authoritative ticket is the record whose accepted update establishes the fact. When staff resolve a ticket, that update lands in PostgreSQL, so the PostgreSQL row is the authority for status. Now read the box at the bottom. This is a design choice. It is not a rule that relational databases outrank document databases. We decided it, and we wrote it down.

The resident projection is a derived copy, shaped for one particular read. The resident page wants one compact document with the ticket details and the latest status. That makes the read simple. The price is that somebody has to keep the copy up to date. And here is why that matters: a copy that silently stops updating does not look broken. It looks current. That is exactly what our resident is seeing.

The source version is the third row. It identifies the accepted order of updates for one ticket. Version 17 follows version 16. It is not the time a message happened to arrive, because messages can arrive out of order.

Why name an owner for each fact? Because during a repair you need to know which way to copy. If you copy in the wrong direction, the stale display value quietly becomes the new truth.

[Sources]
- CST4714 textbook, Chapter 14, sections on ownership and projections.

## Slide 3

Let's look at the most obvious way to keep two stores in sync, and why it breaks. Read the table from top to bottom.

The application commits the staff update in PostgreSQL. The source now says resolved, version 17. Then it sends the update to MongoDB, and the connection fails or the client times out. So the application returns an error to the browser. But look at the third row. The committed PostgreSQL update still exists. An error message to the browser does not travel back in time and undo a commit.

Why can't one transaction cover both? Because a PostgreSQL transaction coordinates PostgreSQL statements. A network call to MongoDB does not join that transaction just because the two lines sit next to each other in your Python. And the box at the bottom says flipping the order does not help. Write MongoDB first, and now the copy can change while the source never does. Same problem, other side.

There are several real answers to this: distributed transactions, compensating operations, or simply accepting an asynchronous copy. Each one has costs. We are going to use a transactional outbox, because it builds on a local transaction you already understand.

Before we get there, hold on to the failure model. The source committed. The second write is uncertain. Blindly retrying both writes could repeat an effect.

[Sources]
- CST4714 textbook, Chapter 14.
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

## Slide 4

This slide is about one word that misleads people constantly: timeout.

A timeout is something the client observed. It means the client did not get a reply before its deadline. That is all it means. Look at the two rows. In the first, the request never reached the server, so nothing was written. In the second, the server applied the write and the reply got lost on the way back. Now look at the right-hand column. The client sees exactly the same thing in both cases: no reply before the timeout. Two different histories, one identical error.

So a timeout cannot tell you the stored outcome. That is why the box at the bottom says read the relevant record and correlate the event ID. In our supplied incident, a later MongoDB read still shows version 16 while the source is at 17. That later read is what establishes that the projection is behind. The timeout alone was much weaker evidence.

The second line in the box is the design lesson. A retry has to be safe even if the first attempt already applied. Setting a field to a value can be safe to repeat, as long as there is an ordering rule. Adding one to a counter is not, because you get two increments. Keep that difference in mind, because it comes back on slide 11.

[Sources]
- CST4714 textbook, Chapter 14, supplied incident and partial-failure explanation.

## Slide 5

Three fields, three different questions. Look at the Example column.

ticket_id, 1008, answers the question: which business ticket? The same 1008 should appear in the source row, the event, the consumer log, and the resident document. That shared ID is what lets us line the records up. But matching IDs only tell you the records are about the same ticket. They do not tell you the records agree.

event_id, evt-1008-17, answers: which recorded change? When something retries, it should keep that same event ID rather than invent a new one. That is how we connect three delivery attempts to the one piece of work they represent.

source_version, 17, answers: where does this change sit in this ticket's order? Read the box at the bottom. Version 18 of ticket 1008 follows version 17 of that ticket. It says nothing about any other ticket, and nothing about wall-clock time.

A quick note on the numbers. Tickets 1008, 1009, and 1010 in this week's notebook are synthetic. They look like the Metro Support tickets you have used all semester, but they are not those rows, so do not expect the statuses to match.

We also assume one authoritative version sequence per ticket. If several writers assign versions independently, the simple comparison we are about to use is not enough.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08 synthetic ticket fixture.

## Slide 6

Here is the pattern we are going to use. Read the diagram from left to right.

On the left is PostgreSQL with two things in one transaction: the ticket update and a row in an outbox table. The outbox is just an ordinary table for outgoing work. Because both changes are in one transaction, they commit together or not at all. That closes the gap from slide 3. We can no longer end up with the status changed and no record that anybody needs to be told.

After the commit, the relay reads pending events and publishes them. The consumer receives them and makes a version-checked write to MongoDB, the read projection on the right. Relay and consumer are responsibilities. In a small system, one process might do both jobs.

Now read the line at the bottom, because it is the honest part. The outbox closes the gap between the source update and the event. Delivery, retries, lag, and reconciliation still remain. Every arrow after the first box crosses a failure boundary. A relay can publish an event and crash before it records that it did, so on restart it publishes again. A consumer can apply a change and lose its acknowledgment. Duplicates are normal.

So the outbox gives us one atomic boundary followed by retryable delivery. It does not give us exactly-once behavior anywhere downstream.

[Sources]
- CST4714 textbook, Chapter 14.
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

## Slide 7

Now let's make this concrete. This week's notebook is Notebook 08, Polyglot Incident, and it has three parts. Look at the table.

The transaction demonstration creates a small SQLite database inside Python, with three synthetic tickets and an empty outbox table. SQLite runs real SQL and real transactions, so the commits and rollbacks you see are actual commits and rollbacks. We use it because it shows the commit boundary without any new cloud connection.

The delivery experiment uses one Python dictionary as a model of the resident copy. A list of events arrives in an order we choose, and a loop decides which ones change the dictionary. It is deliberately tiny. It makes the decision rule visible. It does not simulate network timing or concurrent workers.

The reconciliation part compares source IDs and field values against a slightly bigger projection. That is where we will see why matching counts can hide problems.

Now read the bottom box. Choose Open in Colab on the weekly page and run the cells in order. No package installation, no cloud database account, no database password. Colab does need a Google sign-in. I will run the first part with you as a demonstration, and the delivery experiment is your individual work. You submit one Brightspace text incident update. The notebook is your working material, not a second file to hand in.

[Sources]
- CST4714 Notebook 08 and Week 14 lab.
- https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager

## Slide 8

This is the first demonstration, and it is about what an exception does to a transaction.

We start right after setup. Ticket 1008 is open, version 16. The line with source_db opens a transaction on this SQLite connection. Inside it, the UPDATE sets the ticket to resolved, version 17. The question marks are placeholders, and the tuple underneath supplies the values separately from the SQL. Then, on purpose, we raise a RuntimeError, before we ever insert the outbox event.

Watch where the exception goes. It leaves the with block first, and that is the moment the pending transaction rolls back. Only after that does the except block catch it and print the message.

Now look at the result line at the bottom. After fresh setup, ticket 1008 is open, version 16. Outbox rows: 0. The UPDATE statement ran, but it did not commit. That is why a log line saying the application reached a certain line of code does not tell you what got stored.

The placement of the try matters. If you catch and swallow the error inside the with block, the block exits normally and commits whatever ran so far. Here the exception crosses the transaction boundary before we catch it.

One reminder: this is SQLite in a notebook, not a PostgreSQL server, though the transaction idea is the same.

[Sources]
- CST4714 Notebook 08, rollback cell.
- https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager

## Slide 9

Now the success path, with both writes in one transaction.

Look at the WHERE clause. It says ticket_id equals 1008 and source_version equals 16. So the update can move the ticket from 16 to 17 only if it is still at 16. That expected-version check is what stops two writers from both claiming the same step.

Next line: if changed dot rowcount equals 1. The row count tells us whether the transition actually matched a row. If it did, we insert the outbox event: evt-1008-17, ticket 1008, resolved, version 17. When the with block exits normally, the ticket change and its event commit together.

Read the small print at the bottom. A failed event insert rolls back this transaction's ticket update. The outbox also has a unique ticket-and-version pair, so two different event IDs cannot claim the same version. And if the event insert fails for any reason, the ticket update rolls back with it. We never get a new status without its event. But having the event does not mean it has been published or applied anywhere.

What if I run this cell again? It no longer matches version 16, so zero rows change, and the complete notebook reports that zero match instead of adding another event. In a real system, find out why. The row might be missing, or another accepted update might have moved it forward.

[Sources]
- CST4714 Notebook 08, successful transaction cell and schema.
- https://www.postgresql.org/docs/current/tutorial-transactions.html

## Slide 10

This table tracks ticket 1008 and the outbox through every notebook stage. Read down the rows.

Fresh setup: open, version 16, zero outbox rows. Failure and rollback: open, version 16, zero rows. That is exactly where we started, which is what a rollback should give you. Successful local commit: resolved, version 17, one row. Then a later accepted close operation: staff close the ticket, closed, version 18, and its event is recorded in the same transaction, so two rows.

Read the box at the bottom. The paper incident you will analyze observes version 17. Version 18 only happens later, in the experiment. The incident stops at 17, and the experiment continues the story. Keep those two apart when you write.

The second line of the box is the key point. These local cells do not run a relay or a consumer. Two outbox rows means two pieces of outgoing work exist. It does not mean any resident page changed.

So there are three different milestones: recorded, published, and applied. Each kind of evidence supports a different one. An outbox count tells you work is waiting to leave. A consumer checkpoint tells you what was received or processed. A read of the resident document tells you what is actually being served. When something is stuck, ask which milestone your evidence actually proves.

[Sources]
- CST4714 Notebook 08 and Week 14 supplied incident.

## Slide 11

Two words people use as if they mean the same thing. They do not. Look at the table.

Idempotency means doing an operation twice has the same final effect as doing it once. First row: set status to resolved, twice. You still have resolved. That is idempotent. Second row: add one to a counter, twice. You get two increments instead of one. Not idempotent. That is why retries are dangerous for some operations and harmless for others.

Now the third row, which is the trap. Set an older status after a newer one. Say the ticket is closed, and then an old event arrives that says set it to open. Setting open is perfectly repeat-safe. Do it ten times and you still have open. But it replaced a newer accepted state with an older one. The resident's ticket just went backwards. So idempotent is not the same as correct.

That is why the box says a retry-safe state assignment still needs an ordering rule. Our events are complete-state events. Each one carries the full status at a version assigned by the source, and the consumer only accepts a version newer than the one it holds. Duplicates and old events become no-ops.

That rule rests on assumptions: one ticket, one authoritative version sequence, and payloads that carry the whole status. It is not a promise about every event-driven system.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08 delivery experiment.

## Slide 12

Here is the guard in code. Let's read the loop.

For each event in the deliveries list: if ENFORCE_VERSION is on, and the incoming source_version is less than or equal to the version the projection already holds, we print "Ignore old or duplicate event" and leave the projection alone. Otherwise we apply it. We copy the status, the source_version, and the last_event_id into the projection, and print "Apply".

Notice that it says less than or equal. Equal catches the duplicate. Less than catches the late old event. Both get ignored for the same reason: they carry nothing newer.

The last_event_id field records which event supplied the current state. A duplicate does not change it, and this projection holds only the latest state, not a history.

Read the note under the code. Each cell run resets the projection to open, version 16. That is deliberate. When you flip a flag and rerun, you start from the same place, so you are comparing like with like instead of inheriting leftovers from your last run.

And the second line: the dictionary loop models one consumer. It is not a concurrent database write. The check and the assignment are two separate Python steps, and two real workers could both read version 16 before either one writes. In a few slides we will see the MongoDB command that does the check and the write as one atomic operation.

[Sources]
- CST4714 Notebook 08, Section 2.
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 13

Let's run the default list and read the trace from top to bottom. We start at open, version 16.

First delivery: version 17. It is newer than 16, so it applies. Stored state: resolved, 17. Second delivery: 17 again, the same event redelivered. 17 is not newer than 17, so the guard ignores the duplicate. Still resolved, 17. Third: version 16, arriving late. It carries the old open status, but 16 is older than 17, so it is ignored. Still resolved, 17. Fourth: version 18, closed. Newer, so it applies. Closed, 18.

Look at the right-hand column. It shows the stored state after each delivery, not the event's payload. That is why a line about an old event is followed by the newer state. The handler decided to leave things alone.

Now here is a subtle trap. Suppose the guard were off. With this order, the late 16 would knock the ticket back to open for a moment, and then 18 would arrive last and set it to closed. The final line would look perfect. The ending value hides the mistake in the middle. A resident who loaded the page at the wrong second would have seen open.

That is why your experiment moves the old event to the very end. A correct final value under one lucky arrival order proves much less than testing what happens when the order changes.

[Sources]
- CST4714 Notebook 08, default delivery list and guard behavior.

## Slide 14

Now it is your turn. There are four steps on the slide.

In the delivery cell, move the whole version 16 event to the end of the deliveries list. Keep all of its fields together. The order is now 17, 17 again, 18, and 16 last. Run it with ENFORCE_VERSION equal to True. You should end at closed, version 18.

Then change it to False and rerun. Same events, same payloads. The only thing that changed is whether the consumer refuses a stale version. Look at the final status and version. This is the broken run, and you are watching the late event win.

Then restore True and rerun. That is your repaired run. Because the cell resets the projection each time, these runs are comparable. You are not relying on leftover state from the run before.

Now read the bottom box. Write down the final status and version from the broken run and from the repaired run. Those observed values go into your Brightspace incident update. Use what you actually saw, not what you expected to see.

If Python gives you a syntax error after the move, it is almost always a missing comma between dictionary entries or the closing square bracket of the list. You do not need to touch the loop or write a new function. The small edit is enough to expose the ordering problem. When you are done, continue to the reconciliation section.

[Sources]
- CST4714 Week 14 lab and Notebook 08, individual experiment.

## Slide 15

This slide marks the edge of the technique, and it is worth understanding, because it is where the simple guard stops working.

Look at the first row. The event means: the current total is 3. That is a complete state. If version 18 arrives before 17, that is fine. 18 says the total is 3, it is authoritative and complete, so it can replace the older state, and ignoring 17 afterward loses nothing.

Second row. The event means: add 2, after an earlier add 1. That is a delta, a change rather than a state. Now suppose 18, add 2, arrives first, and then we ignore 17, add 1, because it is older. We just lost the 1. The total is wrong, and no version number can bring back an effect we chose not to apply.

So delta events need a different policy. You might replay a complete ordered history, or notice a missing version and wait for it, or rebuild from an authoritative total. Which one is right depends on the operation.

Read the bottom box. The lab uses complete-state events. The delta case is an optional extension, and it is in the README if you want to try it. It is ungraded and adds no submission.

This is good interview reasoning, by the way. You can say where your technique works and where it does not. The guard fits ticket status. It does not fit an inventory stream.

[Sources]
- CST4714 textbook, Chapter 14, complete-state and delta-event comparison.

## Slide 16

Here is what the version rule looks like as a real database operation. Read the updateOne.

The first object is the filter: underscore id 1008, and source_version less than 18, written as dollar lt 18. The second object is the update: dollar set status to closed, source_version to 18, and last_event_id to evt-1008-18.

Why does this matter? Because MongoDB checks the filter and changes the document in one atomic operation. Compare that with the Python loop on slide 12, where we read the version and then wrote it in two separate steps. With two workers, that gap is a race. Here there is no gap. A slow, delayed writer cannot sneak in and lower the version after a newer one has landed, because its filter simply will not match.

Be clear about the scope. This is one existing document. It does not coordinate PostgreSQL, a message broker, and every MongoDB document together. Acknowledging the queue message is still a separate job.

Read the small print. This is a reference for an existing practice document, and the notebook explains it but does not run it. Your required experiment stays local. If you try it later, use a disposable practice collection and look at the matched and modified counts.

And notice there is no upsert option on this command. That is on purpose, and the next slide explains why.

[Sources]
- CST4714 Notebook 08, corresponding MongoDB operation.
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 17

Suppose the command from the last slide comes back with a matched count of zero. What does that mean? Nothing matched the filter. It does not tell you why. Look at the three rows.

First row: the document is already at version 18 or newer. The less-than-18 filter fails. That is the normal, healthy case. A duplicate or stale event has nothing newer to apply, so ignoring it is correct.

Second row: the document is absent. There is nothing to update. If you treat that like the first row, the resident record just stays missing. You need an initialization policy, ideally built from a verified complete source state.

Third row, the sneaky one: version 18 with the wrong status. The document claims to be current, but the value is wrong. The filter fails because the version is not older, so resending the event will never fix it. Only reconciliation, comparing values as well as versions, will find it.

Now read the warning box. The tempting fix is to add upsert, so that any zero match inserts a fresh document. But if a newer document with the same underscore id already exists, it fails the version filter, the upsert tries to insert, and that insert collides with the existing underscore id.

So three different states need three different decisions. One retry option cannot stand in for all of them.

[Sources]
- CST4714 Notebook 08 and Chapter 14, tested version-filtered update example.
- https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/

## Slide 18

Now the supplied incident. This is the paper incident in your lab, and it follows one event. All the times are UTC. Read down the timeline.

At 14:03:12, PostgreSQL commits resolved, version 17, and the outbox gets evt-1008-17. At 14:03:13, the relay marks the event published, and the consumer records that it received it. Then, between 14:03:13 and 14:03:14, the consumer times out writing the projection and queues a retry. At 14:04:00, the retry worker pauses, because its database credential has expired. At 14:04:05, a read of the resident projection still shows open, version 16.

So where did progress stop? After receipt. The consumer got the event. It could not write, and the retry path cannot make progress.

Notice what each piece of evidence proves. The published mark at 14:03:13 would not, on its own, prove the consumer received anything. We have the received log for that. The timeout alone would not prove the write failed. The later read at version 16 is what proves this projection is behind.

Read the box at the bottom. The record does not establish the state of every other ticket. A paused worker probably has a backlog, so do not assume only this ticket is affected, and do not assume everything is broken either. And keep this incident's version 17 separate from the notebook's version 18.

[Sources]
- CST4714 Week 14 lab, supplied incident record.

## Slide 19

So how do we fix it? Read the steps on the slide in order.

First, restore the consumer's approved access. The thing that cannot make progress is the retry worker with the expired credential, so that is what we fix, through the proper operational process, with only the narrow access this consumer needs. Then resume the recorded work through the normal version-checked handler. Then compare the resulting projection with the current source.

Now read the bottom box, because this is the mistake people make under pressure. Keep PostgreSQL's accepted status. You could make both screens agree instantly by setting the PostgreSQL ticket back to open. Agreement achieved. And you would have thrown away a staff member's valid, committed update. Agreement is not the goal if it comes from the wrong direction. The authority stays the authority.

Also, when you compare after the repair, the correct answer might be newer than 17. If another accepted update came in while the worker was paused, version 17 is no longer the target. Do not force the record back to the number in the incident report.

Then go wider: inspect other queued tickets or consumer lag. The same expired credential probably affected more than the first complaint.

In your write-up, this credential repair is a proposal. You did not perform it. What you actually ran is the notebook experiment. Keep those two clearly separate.

[Sources]
- CST4714 Week 14 lab and Chapter 14 incident response.

## Slide 20

Now we zoom out from one ticket to several. These are still the notebook's synthetic tickets. Look at the table.

Ticket 1008: closed, 18 on both sides. After the guarded experiment, it matches. Good. Now count the rows. The source has three records. The resident projection has three records. A simple count check passes. Read the box: three source records, three resident records, three discrepancies.

Ticket 1009: resolved, version 5 in the source, absent from the projection. It is missing. Ticket 9999: absent from the source, open, version 1 in the projection. It is an extra record with no source. One missing plus one extra, and the count comes out even. That is why equal counts tell you almost nothing.

Ticket 1010 is the nasty one. Both sides say version 7, but the source says resolved and the resident says open. If you only compared versions, you would miss it. This is the third row from slide 17, a wrong value at an equal version.

So the second line of the box is the method. Compare the union of IDs from both sides, and compare the source-owned fields, status and version, for each one.

The notebook reports three findings with the guard restored. If you leave the guard off with version 16 last, 1008 becomes a fourth. We do not compare last_event_id, because that is processing metadata, not a business fact.

[Sources]
- CST4714 Notebook 08, reconciliation fixture and comparison loop.

## Slide 21

So how do we repair the projection? Not by patching it in place. We build a separate candidate from the authority. Read the code.

rebuilt_records is a new dictionary. For each ticket_id and its fields in source_records, we copy the fields in. The source is only read, never changed. That is the point of this slide: the repair direction is explicit. Data flows from the authority into a new candidate.

Then two prints. The first checks that the set of IDs matches the source. The second checks that the field values match. Read the result line: both comparisons return True, and the source stays unchanged.

Let me be honest about what that proves. We built the candidate by copying the source, so of course it matches. The check cannot really fail here. It also does not fix the three discrepancies in the existing resident records, because it never touches them. What it shows is the pattern: build from the authority, verify the candidate, and leave both the source and the live copy alone while you do it.

Read the limit box. A real rebuild must keep fields the projection owns separately, handle new writes that arrive during the rebuild, and switch readers over safely. This model does none of that cutover.

And ticket 9999, the extra record? Investigate it before you delete it. It might be a deleted source record or an ownership mistake.

[Sources]
- CST4714 Notebook 08, separate rebuild candidate and stated cutover limitations.

## Slide 22

Here is what you hand in. One Brightspace text response, and it is short.

Read the first box. Explain the user impact: what does the resident see, and why does it matter? Say where progress stopped in the supplied incident. Propose a repair that respects which system owns ticket status. Then include the final status and version you observed in your broken run and your repaired run. Those come from your own notebook, not from my slides.

Then name one broader check before closing the incident, such as other queued tickets or the consumer's lag, and say why that check follows from a paused worker. Do not just add a random metric.

Write it for a colleague who needs to know what is affected and what happens next. A list of product names does not help them. A sentence like "the source accepted a newer status, and the consumer cannot advance the resident copy" does.

Be precise about what kind of claim each sentence makes. The supplied record supports your diagnosis. Your notebook supplies the broken and repaired results. The credential repair is a proposal, not something you did in production. Keeping those straight makes the update more credible, not less.

Read the bottom box. Work individually. No notebook attachment, no separate timeline, and no five-check matrix. One clear incident update.

[Sources]
- CST4714 Week 14 lab submission instructions.

## Slide 23

Welcome back. Today is Day 2, the Final Project Operations Clinic. Read the line in the middle. A useful query runs. The next task is to make its operation understandable.

Getting a query to return an answer is a real milestone. But a working database has to answer other questions too. Who is allowed to use this data? How does an important operation behave? What happens if we have to restore it? Today you take one of those questions for your own project and close it.

Read the bottom box. Use the model, queries, and project guide you already have. The final-project assignment and its rubric are the requirements source. I am not adding a new project or another submission list. And a one-platform project, PostgreSQL only or MongoDB only, is still a completely valid choice.

Here is the method, and it is the same one we used on the incident. Name the fact or operation that matters. Find its current state. Pick a specific check. Say what the result supports. A missing permission test is a different gap from a broken query. A backup file is different from a restore you have actually checked.

We will walk through access, indexes, recovery, and demonstration choices, and then you will work individually. You do not need a second database or a polished interface. You need a small system you can explain, limits included.

[Sources]
- CST4714 final-project assignment and Week 14 project clinic.

## Slide 24

First, access. An access test means something only if you know which identity ran it. Look at the table.

First row: the administrator reads a record. That proves the administrator has access, which we already knew. It tells you nothing about the application's reader. This is the most common mistake I see in projects. Everything is tested as the admin, so everything passes.

Second row: the intended reader reads an allowed record. Now you have shown the read path works for the identity that actually uses it. Third row: the intended reader attempts a forbidden write, and it is denied for the expected permission reason. That is the other half. You need both, the allow and the deny, the same idea from Week 6.

The fourth row is a different thing. An invalid value fails a constraint. That is an integrity rule rejecting bad data. It says nothing about who may access the table. Both protections matter, but do not describe one as the other.

Two platform notes. In Supabase, the admin SQL editor is not the same as an authenticated user going through row-level security. In Atlas, the account that manages the project is not automatically the database user in your connection string.

Read the bottom box. Use disposable project data, and keep passwords, connection strings, and privileged service keys out of the demo. Name the role, the action, and the result. Never the secret.

[Sources]
- CST4714 textbook, Chapter 6, and final-project access requirement.
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://www.mongodb.com/docs/atlas/security-add-mongodb-users/

## Slide 25

Next, indexes. Read the top line: an index decision begins with one query. Our example workload is finding a resident's recent open tickets. The filter fields and the sort order tell you what the database has to find and how it has to order it. An index name alone does not explain why the index helps.

Look at the two columns. On the left is what you keep fixed: the filter, the sort, the dataset, the returned rows, the exact parameters, and the environment and how you measured. If any of those change between before and after, you are not comparing anything.

On the right is what you compare: the selected plan, how much work was examined, which index fields support the filter and the order, and any timing, with its limits. In PostgreSQL, tell the planner's estimates apart from the actual execution numbers. In MongoDB, tell documents returned apart from documents and keys examined.

Read the bottom box. A small collection can legitimately use a scan. That is not a failure. It is an observation to explain, and it is better than inventing a speedup. A single faster run is weak evidence, because caching changes timings.

Also record the cost. Every index takes storage and adds work to every write. In the clinic, an easy improvement is adding the exact query, the observed plan, and one limitation to an index explanation you already have.

[Sources]
- CST4714 textbook, Chapters 7 and 11, and final-project index requirement.
- https://www.postgresql.org/docs/current/using-explain.html
- https://www.mongodb.com/docs/manual/reference/explain-results/

## Slide 26

Recovery next. Read the title: a restore test answers more than a backup command. A backup command tells you a file was created. It does not tell you what is in it, or whether you can get a working database back from it.

Look at the table. Each row is something you observe in an isolated restore target, a separate place, not your original project. First, expected IDs and selected field values. That checks the data survived in the expected form. Remember slide 20: matching counts alone can hide missing and wrong records. Second, a familiar query returns its expected answer. That checks the restored data actually supports something the application does.

Third, inspect indexes, constraints, and access. Read the bottom box: a CSV or JSON export alone does not recreate every database object. You do not get the indexes, validators, roles, or policies. If something needs a separate step to recreate, write that step in your project guide.

Fourth, record the restore command and the elapsed time. That describes one run under those conditions. It is not a promise about recovery time under a bigger workload during a real incident.

Keep the restore isolated so the original data stays available while you inspect it. Use the recovery approach that fits your platform and artifact. And be honest about which steps you actually ran and which are still a plan. Today is a good day to turn one recovery claim into a checked result.

[Sources]
- CST4714 textbook, Chapters 8 and 12, and final-project recovery requirement.
- https://www.postgresql.org/docs/current/app-pgdump.html
- https://www.mongodb.com/docs/database-tools/mongoexport/

## Slide 27

If you have two stores, recovery needs an order, and the order comes from ownership. Read the first box.

For a rebuildable resident projection, like our MongoDB copy of PostgreSQL-owned status, the order is: restore the authoritative source in isolation, reconstruct the source-owned projection fields from it, compare IDs and values, and only then coordinate access. That is the same direction as Day 1's repair. Authority first, copy second.

Now, why not just restore both dumps? Read the second box. Two dumps from different times do not automatically represent one application-consistent point. If the PostgreSQL dump was taken before a status update and the MongoDB dump after it, each file is fine on its own, and together they disagree.

The box also says a MongoDB collection with independent historical facts needs its own recovery source. If MongoDB holds history or annotations that PostgreSQL never owned, rebuilding from the ticket table loses them. You cannot reconstruct what the source never had.

So, for your project: you do not need to turn a one-database project into a two-database project. If you chose one platform, explain its recovery boundary. If you chose both, explain what each owns and how your recovery respects that split.

The skill here is knowing which data can be rebuilt, which must be preserved independently, and what you check before users come back. More backup files do not replace that reasoning.

[Sources]
- CST4714 textbook, Chapter 14, recovery order and ownership.

## Slide 28

Now the demonstration. The question is whether another person can follow it. Look at the table, Show on the left, Explain on the right.

First, show one query with its input and result, and explain the question, what a returned row or document means, and the expected answer for your data. That lets the audience judge correctness instead of just watching a command finish.

Second, one operational decision. That could be an index comparison, an expected permission denial, or a separate restore check. Explain what you tested and what changed.

Third, a failure or limitation, and how you detected it. Put the limitation where it affects the conclusion, not in a vague disclaimer at the very end.

Fourth, a saved result in case the cloud connection fails. Label when and where it ran. If the live connection breaks during your demo, you can show that result and say plainly that it is a prior run. It does not become a live result just because it sits next to the command.

Read the bottom box. The notebook or script can be the presentation. A second slide deck is optional in the final-project assignment. Keep credentials off the screen and out of saved output.

And a smooth demo is not the same as a good one. If something breaks and you can diagnose it, show a previous checked result, and say what you would test next, that shows real command of your system.

[Sources]
- CST4714 final-project presentation requirement and Week 14 clinic.

## Slide 29

Here is what you do for the rest of class. There are three steps on the slide.

Open the final-project assignment and your existing package. Choose the highest-risk unfinished item in the rubric. That means the item most likely to stop you from explaining or verifying your system. Make it specific enough to finish today.

For example: a query that returns the wrong unit of analysis after a join. An index explanation without the query it supports. An access section that only shows an administrator's successful read. A recovery guide that stops right after making the backup file. Each of those needs a different next action, so do not treat today as a reason to add more features.

Then complete and check that item in the same notebook, code, or guide. If you hit a dependency, say you need correct seed data before the query can be evaluated, fix the dependency first. Record the actual result and the remaining limitation in the guide you already have.

Read the bottom box. Possible work includes a query correction, a permission test, an index comparison, or a separate restore check. A one-platform project remains a valid choice. And there is no separate Week 14 project submission.

This is individual work. By the end of class, you want one concrete improvement to your project and a clear sentence about what comes next, not a new pile of overlapping documents.

[Sources]
- CST4714 final-project assignment and Week 14 README.

## Slide 30

Last slide for the week, and it is about how you talk about this work. Read the paragraph in the box.

It starts with the setting: in a class experiment. That is honest, and honest is more convincing than claiming distributed-database experience after one notebook. Then it names the problem, a stale resident view traced to a paused consumer. Then what was tested: duplicate and delayed full-state events. Then the comparison: IDs and values across the source and the projection. And then what was learned: why a version guard matters, and why matching record counts alone can miss corruption.

That pattern works for anything. A concrete problem, the mechanism you built, the result you observed, and the boundary of what you showed.

Read the bottom box. Describe the work you actually ran. The local notebook does not establish experience operating a distributed production service. You did not run a production queue, coordinate concurrent workers, or do a live cutover. But you can still explain why a production MongoDB update needs the version check inside the atomic operation, and why independently owned data changes the recovery plan. Interviewers value that kind of precision.

Use the same pattern for your final project. Pick examples you can explain down to the code and the data.

Next week is course review, final demonstrations, and career explanations. The goal is that you can make your database decisions clear to another person, including when they ask you what failed.

[Sources]
- CST4714 textbook, Chapters 14 and 15, and Notebook 08.

## Slide 31

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Polyglot persistence: one owner per fact (1:30); Keeping two databases consistent: outbox and version guard (1:42); Triage a cross-database incident (1:24). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 14 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
