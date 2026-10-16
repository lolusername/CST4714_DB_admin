# Week 8: Backup, Restore, and Recovery - Spoken Transcript

## Slide 1

Welcome to Week 8. Look at the two lines in the middle of the slide. The database is running. Yesterday's records are gone. Both can be true at the same time, and that is the whole problem for this week.

Picture it. You open the support application, you can connect, queries run, the status light is green. And yesterday's tickets are missing. Nothing about that green light tells you whether you can get them back. Being up and being recoverable are different questions.

So far this semester we have worked on keeping the database correct while it runs: relational ideas, constraints that reject bad states, transactions, permissions, and query plans. This week adds a new question. If the current state becomes unusable, which earlier state can we rebuild, and how do we prove the rebuilt copy actually works?

On Day 1 we follow one small PostgreSQL database through a logical export and a restore into a different database. Three tables and a handful of rows, small enough that we can check the actual values instead of trusting a big output. The tools are the real PostgreSQL tools. On Day 2 we connect this to the midterm: when do you roll back, when do you repair, and when do you restore. You will not need a paid backup plan, and you will not risk your Supabase project, to practice any of it.

[Sources]
- Course textbook, Chapter 8.
- https://www.postgresql.org/docs/15/backup.html

## Slide 2

Here is the kind of incident that makes recovery real. Read the SQL on the slide. BEGIN, DELETE FROM metro_support.ticket_events, COMMIT. This is an illustration, not something to run against your project. The operator meant to remove one test event. But there is no WHERE clause, so the DELETE hits every row in the table, and then the transaction commits.

Now notice what did not happen. The server did not crash. The network did not fail. PostgreSQL keeps answering queries correctly, based on the data it now has. So restarting the server brings nothing back. Durability, the property that protects our committed work, protects a committed mistake just as faithfully. If a replica follows this primary, the deletion may be copied there too. Replication keeps a service running when a machine dies. It is not a separate history you can rewind.

Why does the word committed matter so much? If this were still inside an open transaction we controlled, ROLLBACK would discard it. After COMMIT, a new ROLLBACK cannot reach back into a finished transaction. That is the last line on the slide: recovery needs an earlier usable state, or a reviewed correction.

One more question before acting. Have valid new events arrived since the backup? Replacing everything with an older copy would throw those away. That is why we restore somewhere separate first and look before we touch the live database.

[Sources]
- Course textbook, Chapter 8, opening incident.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 3

This table separates four words people use as if they were the same. Read down the first column: high availability, backup, restore, disaster recovery. Then look at the last column, the important limit, because that is where the confusion lives.

High availability keeps the service running after some component fails. A standby can take over when a machine dies. But its limit is that it can reproduce a harmful committed write. The standby faithfully copies the deletion from the last slide.

A backup is a retained state we can recover later. Its limit is that it must stay accessible and restorable. A backup on the same temporary machine as the source disappears with that machine. A backup locked behind a password nobody can find during the incident is just as useless.

A restore is the operation that rebuilds objects and data in a target. Finishing it does not mean the application can use the result. The roles might be missing, or the app might still point at the damaged source. So it needs verification.

Disaster recovery is the whole tested procedure: people, access, systems, and dependencies.

These work together. A service might use a standby for machine failures and backups for destructive mistakes. Read the line at the bottom: the failure you plan for determines what you keep and test. Today's drill tests a logical restore and some database behavior. It does not prove regional disaster recovery for a production application.

[Sources]
- Course textbook, Chapter 8, Four Mechanisms Solve Different Problems.
- https://www.postgresql.org/docs/15/backup.html
- https://www.postgresql.org/docs/15/high-availability.html

## Slide 4

Two acronyms you will hear in every recovery conversation, and this diagram is here to keep them apart.

RPO, the recovery point objective, is how much recent data you can afford to lose. If the service owner says we can lose at most five minutes of changes, you need a way to recover a state within five minutes of the failure. A daily export cannot keep that promise, no matter how reliable it is.

RTO, the recovery time objective, is how long it may take to get acceptable service back. And that time is much more than the pg_restore command. It includes noticing the problem, getting access, preparing a target, moving the archive, running the restore, checking the result, and reconnecting the application.

Now read the diagram from left to right using the labels on the slide. t sub r is the newest state we can actually recover. t sub f is the failure. t sub a is when service is acceptable again. The data-loss window is t f minus t r. The service-recovery duration is t a minus t f.

Why bother with names for clock points? Because an objective is a requirement, and a measured interval is an observation. Writing down an RPO does not make your system meet it. You measure the real intervals and compare them with the targets. The next slide does exactly that with clock times.

[Sources]
- Course textbook, Chapter 8, RPO and RTO Turn We Have Backups Into a Promise.
- Figure retained from the course's original Week 8 presentation.

## Slide 5

Here is that comparison with numbers. This is an illustrative scenario, but follow the arithmetic, because you will do it yourself.

Four times in the table. At fourteen hundred, the newest usable export represents the database. At fourteen seventeen, the harmful deletion commits. At fourteen twenty-one, the operator notices. At fourteen twenty-nine, restore and verification are done and service is acceptable.

The data gap runs from fourteen hundred to fourteen seventeen. That is seventeen minutes of changes this export cannot give back. The recovery duration runs from the failure at fourteen seventeen to fourteen twenty-nine. That is twelve minutes. Notice I start the clock at the failure, not when someone noticed. Start at fourteen twenty-one and you get eight minutes, and you have quietly hidden four minutes of detection delay. Users were affected during those four minutes too.

Now the bottom of the slide. An RPO of five minutes: seventeen is more than five, missed. An RTO of ten minutes: twelve is more than ten, missed again. We did recover. We did not keep the promise. Those are different outcomes.

Two limits. Seventeen minutes does not tell you how many rows were lost; a quiet afternoon and a busy one look the same on a clock. And an export represents its snapshot moment, not the time the file finished writing. For a large, slow export those can differ a lot, so record which state your artifact represents.

[Sources]
- Course textbook, Chapter 8, Work Through the Clock Times. All times are an authored illustrative scenario.
- https://www.postgresql.org/docs/15/app-pgdump.html

## Slide 6

There are two broad ways to back up a database, and you need to know which one a plan uses, because they depend on different things.

Look at the first row. A logical export describes objects and rows as database commands. pg_dump can write out a table's definition, its rows, and the instructions to recreate related objects. The output can be plain SQL or an archive that pg_restore reads. It depends on compatible tools, on including the dependencies, and it takes time to replay.

The second row is physical. Instead of commands, you keep the database's storage plus a continuous, retained sequence of write-ahead log records. With a compatible base backup and an unbroken chain of logs, a supported setup can recover to a chosen point in time. But if a required log segment is missing, the chain breaks.

We are not building that infrastructure today. As the box at the bottom says, we use pg_dump and pg_restore for one course schema.

Here is one reason pg_dump is a good tool for this: it exports related tables from one consistent snapshot. If you download several CSV files while the application keeps writing, each file can capture a different moment. And read the last line. A CSV alone does not carry its keys, checks, indexes, or grants. You get rows without rules, and after the restore we are going to test the rules.

[Sources]
- https://www.postgresql.org/docs/15/backup-dump.html
- https://www.postgresql.org/docs/15/continuous-archiving.html
- https://www.postgresql.org/docs/15/app-pgdump.html

## Slide 7

This is a redacted capture from the course's own Supabase Free project. Look near the top: Healthy. Look farther down: No backups. Both are true at the same time, and that is the point. Healthy describes present availability. No backups describes the recovery history the platform is showing you. A green light today says nothing about what you can get back tomorrow.

The capture is dated August 25, 2026, and the plan documentation was checked September 7, 2026, because interfaces and plans change. Supabase documents automatic backups for paid plans, and Free projects do not get them. So our required work cannot depend on a paid feature. Instead we make a logical dump ourselves and restore it somewhere separate.

For today's lab we skip cloud credentials entirely. The notebook runs PostgreSQL inside a temporary runtime and creates two practice databases, so your attention stays on what the commands do.

If you later used Supabase as an approved source, the tools stay the same but the connection changes: host, port, user, database name, and TLS settings. On an IPv4-only network, the session pooler gives you a reachable path when the direct endpoint needs IPv6. A routing problem is never a reason to turn off certificate verification.

Last point. Exporting the metro_support schema does not copy the whole Supabase project. Authentication, storage, and other service settings need their own recovery plan.

[Sources]
- Course-owned redacted Supabase interface capture, August 25, 2026: textbook/figures/cloud_interfaces/supabase_project_overview.png. Vendor interface is a third-party rights exception.
- https://supabase.com/docs/guides/platform/backups
- https://supabase.com/docs/guides/database/connecting-to-postgres
- Plan and connection documentation checked September 7, 2026.

## Slide 8

Here is the database we will recover. It is a smaller cousin of Metro Support: three users, three tickets, five events. I kept it small on purpose, so we can trace every ticket back to its requester and see exactly what a bad restore would change.

Look at the three boxes. In users, user_id is the primary key. In tickets, ticket_id is the primary key, and requester_id is a foreign key pointing at a user. In ticket_events, event_id is the primary key, and ticket_id points at the parent ticket. Read the line underneath: one user can request many tickets, and one ticket can have many events.

Why do the foreign keys matter for recovery? Because they are rules, not just matching column names. If a restore copied the rows but lost the rules, later writes could create states the original database would have rejected. So we test behavior, not only data. There is also a named status check on tickets. It allows values like open and in_progress and rejects a value like almost_done. We will use that in a controlled failure test.

Now the note at the bottom, which trips people up. The notebook fixture is three, three, and five. The full Metro Support dataset from earlier weeks is eight users, twelve tickets, and twenty-one events, and some ticket details differ between the two. Neither is right for everything. Always compare against the actual source that produced your archive.

[Sources]
- Course recovery notebook, setup_sql and expected_baseline.
- Course textbook, Chapters 2 and 8.

## Slide 9

This code mixes three layers, so let's peel them apart. The three lines in the box under the code are the translation.

The outer layer is Python. subprocess.run takes a list of arguments and launches a program. That program, PSQL, is the PostgreSQL command-line client. The text after the dash c option is SQL, and psql sends it to the database server. The server counts the rows in metro_support.tickets and sends the answer back through psql to Python. So Python waits, psql talks, and PostgreSQL answers.

SOURCE_DB is just a variable holding the unique name of the practice database the notebook created earlier. It tells psql which database receives the SQL.

Now the options at the bottom. check equals True means that if psql exits with an error, the cell stops instead of quietly carrying on. text equals True gives readable strings. capture_output equals True keeps the output, so a later cell can compare it with the restored result. Why care? Because launching a program successfully proves nothing about whether the query worked. We check the result.

And the last line: in Colab, PG_PREFIX runs the command as the postgres operating-system user, which owns the local server and the temporary archive folder. That is separate from the database name.

You do not need to write code like this from scratch. Follow which database gets the SQL, and read what comes back. Your own check later changes one small query inside this same pattern.

[Sources]
- Course recovery notebook, preparation and query cells.
- https://docs.python.org/3/library/subprocess.html#subprocess.run
- https://www.postgresql.org/docs/15/app-psql.html

## Slide 10

Here is the shell form of the dump the notebook runs. In the notebook, Python passes the same arguments as a list. Let's read it one option at a time.

format equals custom makes a custom archive, meant to be read by pg_restore. schema equals metro_support limits the export to our one schema. file names the output, metro_support.dump. dbname says which database to export from. And SOURCE_DB is just a database name, not a URL with a password inside. Keep passwords out of anything you might paste into a notebook or share.

no-privileges leaves out the GRANT commands. That keeps our classroom restore simple, but it also means this archive cannot show that application permissions were recovered. We have to say that in our results.

Look at the line at the bottom. For a custom archive, pg_dump ignores no-owner. If you want ownership left out, you ask pg_restore, and you will see that option on the restore slide.

Versions matter too. We use client tools that match the server's major version. An older pg_dump cannot export a newer major server, and restoring into an older major version is not generally promised to work. Matching keeps this a recovery exercise instead of a migration puzzle.

Finally, the schema is the scope. Server roles, other databases, and cloud project settings are not in this file. A real recovery plan lists the dependencies the selection leaves out.

[Sources]
- https://www.postgresql.org/docs/15/app-pgdump.html
- Course recovery notebook, dump and tool-selection cells.

## Slide 11

Before we trust the archive, we look inside it. pg_restore dash dash list reads the archive's table of contents without restoring anything. You should see the schema, the three tables, their table data, and the key constraints. One detail worth knowing: you will not see a separate line for the tickets_status_allowed check, and you will not see an index line. The check travels inside the table definition, so the list never shows it by name. That is one more reason we test it after the restore.

Now read the table row by row, and focus on the last column. An inventory shows the expected objects appear. It does not show the restore will succeed; a dependency could be missing, or a command could fail. File size shows bytes exist. It says nothing about whether they are the right database or the complete scope.

The third row is SHA-256, a cryptographic hash of the archive's bytes. Compare it with a trusted hash recorded earlier, and a mismatch tells you the file changed. But a hash of a bad original is still a hash of a bad original. It identifies bytes, not whether the content was trustworthy.

And the warning at the bottom is serious. Restoring a dump can run SQL chosen by whoever controlled the source. An unfamiliar dump is not passive data. In this lab, use only the archive you created from the notebook's own fixture.

[Sources]
- https://www.postgresql.org/docs/15/app-pgrestore.html
- https://www.postgresql.org/docs/15/app-pgdump.html
- Course recovery notebook, archive-list and checksum cells.

## Slide 12

Now the restore itself, two commands. createdb makes the destination, RESTORE_DB. It is a different name from SOURCE_DB, and the notebook gives both a unique suffix so your run never overwrites another run's database. The target starts empty.

Then pg_restore reads the archive into that target, and each option is there for a reason. exit-on-error stops at the first error. Without it, the restore keeps going and leaves you a confusing mix of successes and failures. single-transaction wraps this small restore in one transaction, so if anything fails, nothing half-restored is left behind. That is the first line in the box: stop on failure, keep it transactional.

But notice what that option does not do. It does not clear out objects already in a target. It is not permission to aim the command at a populated project. That is why we start with an empty database made just for this drill.

no-owner and no-privileges mean we are not recreating the source's owners and grants. That keeps the classroom example portable. But a restore that works under the local administrator does not prove the application's restricted role can connect and do its job. That is the second line in the box: review ownership and grants separately.

Now the bottom box. Source and target are separate databases on one temporary server. That protects the source from being overwritten. It does not protect either one if the runtime disappears. Real backups need an independent location.

[Sources]
- https://www.postgresql.org/docs/15/app-pgrestore.html
- Course recovery notebook, restore and cleanup cells.

## Slide 13

Now the comparison, and the table gives specific expected values. First row: users, tickets, and ticket_events are three, three, and five in the source, and three, three, and five in the restored target. Second row: tickets with no matching requester, zero and zero. Third row: one in_progress, one open, one resolved, in both. Fourth row: the named constraint tickets_status_allowed exists in both.

Why so many different checks? Because each catches a different kind of mistake. Table names check structure. Counts check quantities. The missing-requester query checks relationships. The status report checks a grouping a total would hide; if a restore changed a status, the total would still be three, but this row would change.

Read the note at the bottom. The notebook compares complete result lines, including table names. That is a programming detail with a general lesson. If you only searched for the text users equals three, it would also match users equals thirty. A test has to compare the property it claims to compare.

And here is the gap. Change a ticket's subject, and nothing on this slide moves. Swap one valid requester for another, and the foreign key is still satisfied, but the record now means something different. So these checks are useful together, and still not everything. The next slide adds a known-ticket comparison. In your write-up, say which checks you ran and what each could detect, not that a few checks prove everything.

[Sources]
- Course recovery notebook, source_check_sql and expected_baseline.
- Course textbook, Chapter 8, Verify Structure, Data, and Behavior.

## Slide 14

This query zooms in on one record. Read it top to bottom. From tickets we take the ticket ID, the status, and the subject. We join users on user_id equals requester_id to get the requester's display name. And WHERE ticket_id equals 1001 narrows it to one ticket.

Look at the result line: 1001, open, Streetlight dark near bus stop, Requester 101. That is what the notebook's source contains, and the restored target should produce exactly the same values.

Now imagine the restored subject was changed to Incorrect subject. Still three tickets. Still one open ticket. The requester relationship still valid. Every check on the previous slide passes. This query catches it, because it looks at the record we care about. That is the box at the bottom: changing only the subject leaves the row counts unchanged.

There is one more comparison. Source equals restore only proves agreement. If the source was already wrong before the export, a perfect restore reproduces the wrong data faithfully. So we also compare against the intended record, the original INSERT.

In your lab, you adapt this query to ticket 1002 or 1003. Read that ticket's INSERT in the notebook itself, not the full Metro Support files from earlier weeks, because this small fixture has its own details and some of them differ. Then explain what your selected values add to the earlier checks. It is a small code change, but a real change in the question you are asking.

[Sources]
- Course recovery notebook, setup_sql and Your Check: Compare One Known Ticket.
- Course textbook, Chapter 8, Data verification.

## Slide 15

A database can have all the right rows and still be missing a rule. This test asks one thing: does the restored status check still work?

Read the SQL. BEGIN, then an INSERT of ticket 1099 for user 101 with the status almost_done, which is deliberately outside the allowed list, then ROLLBACK. When I run it, the INSERT should be refused with SQLSTATE 23514, a check-constraint violation, and the error should name tickets_status_allowed. That exact code and that exact name are the pass condition.

Why be that picky? Because many unrelated problems also produce errors. A missing table errors. A syntax mistake errors. A dropped connection errors. None of them test the status rule. That is the line at the bottom: those are different failures. Celebrating any error is not a test.

Now the transaction. If the constraint rejects the insert, the transaction fails and cannot commit. If the constraint was lost and the insert sneaks through, the ROLLBACK still throws it away. Either way the practice data is safe, and the notebook then checks that ticket 1099 is not in the table.

Notice why these inputs were chosen. In this fixture, user 101 exists and ticket 1099 does not. So a missing requester or a duplicate key cannot be the reason for the rejection. The status is the only thing wrong. When you design your own failure test, make every other input valid, so you isolate exactly the rule you mean to examine.

[Sources]
- Course recovery notebook, expected-failure cell.
- https://www.postgresql.org/docs/15/errcodes-appendix.html
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 16

Here is the Day 1 lab, and it all lives in one notebook. Click Open in Colab on the lab page, or the badge beside the backup and restore notebook on the Week 8 page. Save a copy in Drive first so your results are kept. If you prefer local Jupyter, you can download the notebook instead. No Supabase password is needed. The notebook starts PostgreSQL inside the runtime and creates uniquely named practice databases.

Run the cells in order and read the output as you go: source baseline, then dump, then the separate restore. Later cells use variables made by earlier cells, so if you jump straight to a restore or verification cell, names will be undefined.

In the section called Your Check: Compare One Known Ticket, first run the supplied check for ticket 1001. Then adapt it to ticket 1002 or 1003, read that ticket's original INSERT, and compare. Explain what this catches that row counts could miss. You may extend the columns for a different meaningful check.

Then write your short recovery account right in the notebook, using the results already there. Say where you restored, what the checks showed, one thing still untested, and which connection would change if the source were Supabase. No second report.

Keep the output, then run the final cleanup cell. It removes the practice databases and artifact folder and stops the Colab service. Submit the completed notebook individually through Brightspace. The dump is not a submission.

[Sources]
- Week 8 lab_01_backup_restore.md.
- Course recovery notebook.
- https://research.google.com/colaboratory/faq.html

## Slide 17

Welcome to Day 2, the PostgreSQL operations clinic. Read the line in the middle: a working schema must survive ordinary changes and mistakes. Accepting a few inserts is not enough. The relationships must model the problem, the transactions must keep the intended changes, and the operations must stay understandable when something waits, fails, or needs recovery.

We use your midterm operations case as the setting. The assignment already has the requirements and the rubric; these slides do not add new ones. The Week 8 page also asks you to revisit Chapter 3 on keys and constraints, so today, find the supplied schema's keys and three non-key integrity controls, and say which invalid state each one prevents.

One distinction right away. The midterm has transaction work and a blocking investigation. They are related, but not interchangeable. A rollback in one connection does not show you diagnosed a second connection waiting on a lock. And a blocking observation does not show a correct committed business change.

The improvement part lets you choose, for example, access control, an index, or a safe schema change. Pick a problem your case really has, and examine it with a comparison that fits.

Recovery is in the case too. A recovery plan is required. Performing a restore for the midterm is optional. Our Day 1 recovery notebook gives you the experience to make the plan precise, but it does not let you claim that a different project was restored if you never ran that test.

[Sources]
- Course assignments/midterm_project.md, canonical requirements.
- Course textbook, Chapters 4 through 8.

## Slide 18

Here is a schema change you can rehearse safely, on the disposable notebook fixture only. Read the SQL. BEGIN. Then ALTER TABLE tickets ADD COLUMN follow_up, type text. It is nullable, so existing rows simply get NULL, and we do not invent follow-up values for old tickets.

Next, a catalog query. information_schema.columns lists the columns the current user can see, and the filters pick our schema, our table, and the name follow_up. Inside the transaction, the query returns follow_up. The column exists.

Then ROLLBACK. Run the same catalog query again and you get no rows. The column is gone, as if we never added it. That is transactional DDL in PostgreSQL. Why is that useful? You can try a change, check it, and back out cleanly.

Now the boundary line at the bottom. Do not take this to mean every schema change is harmless, or that every database system treats DDL this way. Even a transactional ALTER TABLE takes locks, and a transaction left open can block other work for as long as it stays open. A production migration also needs a plan for old and new application code running at the same time.

This is an example for the safe-change improvement, not a requirement to add follow_up to your midterm. The real question is what your application needs, and how you would show the old required behavior still works afterward. And once a change commits and turns out harmful, this simple rollback is no longer available.

[Sources]
- Course textbook, Chapters 4 and 8.
- https://www.postgresql.org/docs/15/sql-altertable.html
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 19

This table is the decision you make in an incident, and the deciding factor is the state of the change. Read the first column.

Row one: the harmful write is still uncommitted. If we control that transaction and agree its work should go, ROLLBACK is the response. But look at the constraint: coordinate with the transaction owner, because that transaction may contain other work someone needs.

Row two: the mistake has committed, but it is small and we know the correct fix. A reviewed compensating change is often safer than swapping in an older database. The constraint is to avoid overwriting valid newer work. Knowing a row was wrong yesterday does not mean its current value should be blindly replaced today.

Row three: the needed state is gone and we need an earlier copy. Restore into a separate target, inspect it, then decide how to recover the content. Before the application uses it, reconcile the valid changes made since, and check permissions and behavior.

These are candidates, not automatic rules triggered by one word in an incident report. Losing one table, a whole database, or your access credentials may each need a different procedure.

Now the line at the bottom. Having a backup does not make every incident a restore incident. For the midterm, explain why your response fits the actual problem. A waiting connection, for example, may be solved by dealing with an open transaction, not by bringing back old data.

[Sources]
- Course textbook, Chapter 8, Safe Migrations and Recovery Are Connected.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 20

Here is that last point in practice. This table recalls the blocking exercise from Week 5. Session A changed a ticket and left its transaction open. Session B tried to update the same ticket and waited. A separate diagnostic connection used pg_blocking_pids, which identified A as B's blocker.

Why a separate connection? Because B is stuck waiting. You cannot ask a stuck session to diagnose itself.

The key lesson is that something that looks slow may be waiting, not working. An index does not necessarily fix a lock wait. And as the bottom line says, restoring yesterday's database is not the response here at all.

pg_blocking_pids gives you backend process identifiers. A number on its own is not an explanation. You connect it to the transactions you deliberately started, and ask which operation it belongs to and why it still holds the lock.

Then the owner resolves A, either by committing the intended work or rolling back the unwanted work, and B can finish. Look at the middle line: verify the final row and close the practice connections. That check matters, because releasing a lock and reaching the intended data are related but different outcomes.

For your midterm, use a blocking path the assignment allows, and label it honestly. If you analyzed the supplied trace instead of running live sessions, call it trace analysis. Never write that you observed live blocking if you did not. And close your practice transactions and connections when you are done.

[Sources]
- Course Week 5 blocking notebook and canonical midterm assignment.
- https://www.postgresql.org/docs/15/functions-info.html
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 21

For the improvement part of the midterm, every option starts with a specific operating problem and a comparison that actually tests it. Read the table one row at a time, left to right.

First row: a reader can write data. The improvement is a least-privilege role, and the comparison is an allowed SELECT and a denied write. Why both? Testing only the read leaves the unwanted capability unexamined, and that was the whole problem.

Second row: a user can see another user's rows. The improvement is a row-level access policy, and the comparison needs two identities with different visible rows. If you run everything as the database owner, you can bypass the very boundary you are trying to test.

Third row: a small queue query needs a broad scan. An index may help. Compare the same result IDs before and after, read the plan work, and account for the index's storage and its write costs. A faster query that returns different tickets is not an optimization of the original question.

Fourth row: the application needs another field. A safe schema change, where the comparison is that old behavior still works afterward, plus how you would reverse or repair it.

Now the line at the bottom. These are alternatives, not four tasks. Pick the one that fits your case and that you can explain with actual results. Quality comes from connecting a problem, a change, and a relevant test, not from stacking up mechanisms you cannot explain.

[Sources]
- Course assignments/midterm_project.md, Evaluate One Improvement.
- Course textbook, Chapters 4, 6, and 7.

## Slide 22

A recovery plan is useful when someone else can follow it. Read the example line by line. Purpose: recover the Metro Support schema after accidental loss. Target: an approved empty database, separate from the source, so a rehearsal can never destroy the only current copy. Checks: expected objects and counts, a known ticket, a report, and the intended constraint failure. And before application use: restore reviewed access and verify a safe client path.

Your checks must use your project's baseline. If you work with the full Metro Support fixture, do not copy the notebook's three, three, and five counts. And if your project changes the seed data on purpose, say which state the archive will represent and how you will establish the expected results.

Each check covers something different. Counts and structure catch missing objects. The known ticket and the report catch changed values. The constraint failure tests future behavior. And if getting the service back is the goal, roles, permissions, and a safe application connection belong in the plan too.

Now the lines at the bottom. The midterm requires a plan. An executed restore is optional extra work. A plan can say an operator will compare the selected ticket. It cannot say the comparison passed unless someone ran it. Same for RPO and RTO: a fast restore of a tiny classroom fixture does not show a large production service will meet its target. Say what you measured and what still needs a drill.

[Sources]
- Course assignments/midterm_project.md, Plan Recovery.
- Course textbook, Chapter 8, Worked Example: A Recovery Runbook Entry.

## Slide 23

Read this paragraph as if a teammate just handed it to you. It is a worked example based on the notebook.

It starts with scope: the three-table practice archive, restored into a separate database. Then the observations. The counts and the grouped status report matched the source. Ticket 1001 kept its subject and requester. The restored status rule rejected the invalid test value. Each sentence is a check someone could repeat.

Then the last sentence names what was not done. Application roles were not restored, and reconnection was not tested, so this drill does not show the service is ready for traffic. That limit is part of the technical result. It is not an apology. It tells the next person exactly what is left.

Compare that with the sentence "everything worked." It tells the reader nothing: which database, which properties, what is still unsafe to assume. A precise handoff can be short and still let someone decide the next action.

This is a professional habit. You will write summaries like this in tickets, handoff notes, and incident reviews, for readers who will never see your terminal output.

Now the line underneath. Use your own results and limitations. If you picked ticket 1002, describe ticket 1002, not 1001 from this slide. If a check failed, report the failure and your next step. And for the midterm, keep a recovery plan clearly separate from any restore you actually ran.

[Sources]
- Worked course example based on the recovery notebook's operations, not a production incident.
- Course textbook, Chapter 8, verification and runbook discussions.

## Slide 24

Here is where to look for the rest of the clinic. The first box: Chapter 8 has the recovery concepts, the command reference, and the runbook example. The Week 5 notebook has the blocking experiment. The canonical midterm assignment has the requirements and the rubric, including the allowed alternatives and the submission format.

The middle box is your work for the rest of class. Pick one incomplete part of your own case, repair it, rerun it, and update the explanation beside the result. Start from an actual failure or uncertainty. Maybe the setup does not run from a clean state. Maybe a join duplicates tickets. Maybe a transaction demonstration leaves the wrong final value, or your improvement has no meaningful comparison. Fix it and rerun the test before you rewrite the words, because the explanation should describe the result you actually have.

When you ask me for help, show me the exact command or query, the actual output, and what you expected. Then I can diagnose the operation instead of guessing from "it doesn't work." Never put a password or a private connection URL on screen.

This clinic adds no separate report. Everything stays in the midterm files the assignment describes.

Next week we start NoSQL models and JSON. We will compare them with the relational strengths you now know: keys and relationships, constraints, transactions, and declarative queries. Other models make sense once you can say what they keep, change, or give up for a particular workload.

[Sources]
- Course Week 8 guide and canonical midterm assignment.
- Course syllabus, Weeks 8 and 9.

## Slide 25

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: RPO and RTO on the clock (1:29); Dump, restore, verify (1:35); Point-in-time recovery with WAL (1:20). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 8 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
