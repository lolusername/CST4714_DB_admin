# Week 8: Backup, Restore, and Recovery - Spoken Transcript

## Slide 1

Imagine opening the support application and seeing that its database is online, but yesterday's records have disappeared. You can connect. Queries execute. The service's status indicator is green. None of those observations tells you whether the missing records can be recovered. That distinction is the subject of this week.

So far we have concentrated on making database operations correct while the system runs. We rebuilt relational ideas, used constraints to reject invalid states, and examined transactions, permissions, and query plans. Recovery adds another question. If the current state becomes unusable, which earlier state can we reconstruct, and how will we know that the reconstructed result works?

Today we will follow one small PostgreSQL database through a logical export and a restore into a different database. The example has only three tables and a few records. That size lets us inspect the actual values rather than take a large output on trust. The tools are real PostgreSQL tools, even though the data and environment are temporary.

In the second class we will connect these ideas to the midterm. We will revisit the difference between undoing an open transaction, repairing a committed mistake, and restoring an earlier state. The goal is to choose an appropriate response and explain its limits. You do not need a paid cloud backup service for the lab, and you will not risk your Supabase project to practice a restore.

[Sources]
- Course textbook, Chapter 8.
- https://www.postgresql.org/docs/15/backup.html

## Slide 2

This is an illustrative incident, not a command to run against your project. The operator intended to delete one test event. The statement has no WHERE condition, so it targets every row in the ticket_events table. In this example the transaction commits. The database has accepted the deletion as its new durable state.

Notice what has not happened. The server has not crashed. The network has not failed. PostgreSQL can continue answering other queries correctly according to the data it now contains. Restarting the server therefore does not restore the deleted events. Durability, which normally protects our committed work, also preserves a committed mistake.

If a replica follows the primary's changes, the deletion may reach the replica too. Replication can help keep a service available when a machine fails. It does not automatically preserve a separate history that an operator can use to reverse every harmful write.

The word committed matters here. If the same mistake were still inside an open transaction that we control, a rollback could discard that transaction's work. After commit, a new ROLLBACK cannot travel backward into the completed transaction. We need another recovery source or a reviewed corrective operation.

Before deciding how to recover, we would also ask whether useful new events have arrived since the backup. Replacing the whole database with an older copy could discard those valid changes. A separate restore lets us inspect the earlier state without immediately replacing the active one.

[Sources]
- Course textbook, Chapter 8, opening incident.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 3

The terms in this table describe related mechanisms, but they do not promise the same outcome. High availability concerns keeping a service available through certain failures. A standby or failover arrangement may help after a component stops working. It may do nothing useful for an accidental deletion that the system correctly replicates.

A backup retains a state that we intend to recover later. Its location, access controls, and retention matter. A backup stored only on the same temporary machine as the source can disappear with that machine. A backup protected by a password nobody can obtain during an incident may be effectively unavailable.

A restore is an operation. It reconstructs objects or data in a target using a backup. Completing that operation does not automatically mean the application can use the result. A restore may omit the roles the application needs, or the application may still point to the damaged source.

Disaster recovery covers the larger procedure for returning an acceptable service. It includes the people who make decisions, the credentials and infrastructure they need, the recovery order, and verification before users return.

These mechanisms often work together. A service might use a standby for machine failures and retained backups for destructive changes. We start by naming the failure we want to survive. That choice determines which state we must preserve and what the recovery drill must test. Today's small drill tests a logical restore and selected database behavior. It does not establish regional disaster recovery for a production application.

[Sources]
- Course textbook, Chapter 8, Four Mechanisms Solve Different Problems.
- https://www.postgresql.org/docs/15/backup.html
- https://www.postgresql.org/docs/15/high-availability.html

## Slide 4

There are two time questions in this diagram. The recovery point objective, or RPO, describes the acceptable window of recent data loss. If the service owner can tolerate losing at most five minutes of changes, the recovery design needs a way to recover a state sufficiently close to the failure. Merely scheduling a daily export does not meet that objective.

The recovery time objective, or RTO, describes the target duration for restoring acceptable service. That duration can include detecting the problem, obtaining access, preparing the target, moving the archive, running the restore, checking the result, and reconnecting an application. Measuring only the pg_restore command leaves out much of the service-recovery work.

Read the diagram from left to right. The first point represents the newest state we can actually recover. The middle point is the failure. The last point is the time service becomes acceptable again. The first interval concerns the recoverable-data gap. The second concerns recovery duration.

The variables below simply give those clock points short names. We subtract the recoverable-state time from the failure time to calculate the data-loss window. We subtract the failure time from the acceptable-service time to calculate the recovery duration under this convention.

An objective is a requirement. A measured interval is an observation. We compare the observation with the requirement instead of assuming that naming an objective makes the system satisfy it. The next example makes that comparison concrete.

[Sources]
- Course textbook, Chapter 8, RPO and RTO Turn We Have Backups Into a Promise.
- Figure retained from the course's original Week 8 presentation.

## Slide 5

Here are four clock times for an illustrative incident. The newest usable export represents the database at fourteen hundred. The harmful deletion commits at fourteen seventeen. The operator recognizes the problem at fourteen twenty-one. Restoration and verification finish at fourteen twenty-nine, when the service is acceptable again.

The recoverable-data gap runs from fourteen hundred to fourteen seventeen. That is seventeen minutes. We are assuming this export is the newest usable recovery source. If another supported history source exists, we would need to include it in the analysis rather than ignore it.

The service-recovery duration runs from fourteen seventeen to fourteen twenty-nine. That is twelve minutes. Starting the clock only when the operator notices the problem would give eight minutes, but would omit the four minutes of detection delay. The course example explicitly measures from the failure.

Now compare the results with the targets shown. A five-minute RPO would be missed because seventeen is greater than five. A ten-minute RTO would also be missed because twelve is greater than ten. Successfully restoring eventually is different from meeting the required recovery promise.

There are two important limits to the calculation. Seventeen minutes does not tell us how many rows changed during that interval. Also, an export's represented state is its consistent snapshot, not necessarily the time its file finished writing. For a large, slow export, those clock times can differ substantially. A useful recovery record identifies which state the artifact represents.

[Sources]
- Course textbook, Chapter 8, Work Through the Clock Times. All times are an authored illustrative scenario.
- https://www.postgresql.org/docs/15/app-pgdump.html

## Slide 6

A logical export describes database objects and their data in a form the database can reconstruct. PostgreSQL's pg_dump can describe a table, include its rows, and include the instructions needed to recreate associated objects. The output can be plain SQL or an archive format intended for pg_restore.

This is different from copying the database server's storage files. A physical recovery design works with storage in a format tied more closely to the database system and version. With an appropriate base backup and a continuous retained sequence of write-ahead log records, a supported design can recover to selected points in time. Missing required log segments can break that chain.

We are not asking you to build that production infrastructure today. The conceptual distinction still matters. Logical and physical recovery have different prerequisites and costs, so an operator must know which method a plan actually uses.

Our lab uses a custom-format logical archive for one schema. The archive includes related tables from a consistent source snapshot. Independently downloading several CSV files while an application changes can instead produce files representing different moments.

A CSV can be useful for selected data transfer, but it does not by itself recreate the database's primary keys, foreign keys, check constraints, indexes, or permissions. We will explicitly inspect some of those properties after restoration. Also remember that selecting one schema may exclude objects on which it depends. Today's fixture deliberately keeps its dependencies small enough to understand.

[Sources]
- https://www.postgresql.org/docs/15/backup-dump.html
- https://www.postgresql.org/docs/15/continuous-archiving.html
- https://www.postgresql.org/docs/15/app-pgdump.html

## Slide 7

This is a redacted capture from the course's Supabase Free project. It shows Healthy near the top and No backups farther down. Those statements can both be true. The health indicator describes a currently functioning service. The backup area concerns retained recovery history presented by the platform.

The capture is dated because interfaces and product plans change. The current Supabase documentation says the automatic database backups described for paid plans are not provided to Free projects. Our required work therefore cannot depend on students opening a paid backup feature. We use a logical export and a restore that they can perform without paying.

For today's exercise, we avoid cloud credentials altogether. The notebook runs PostgreSQL inside a temporary runtime and creates two different practice databases. That lets us concentrate on what the commands do and what their results establish.

If we later used Supabase as an approved source, the tools would be similar but the connection information would change. We would need the correct host, port, user, database name, and TLS configuration. On an IPv4-only network, the session pooler can provide a reachable alternative to a direct endpoint that requires IPv6. A network-routing failure is not a reason to disable certificate verification.

Finally, exporting the metro_support schema would not copy the entire Supabase project. Authentication, object storage, and other service settings need their own scoped recovery arrangements. The platform name alone does not define the contents of our archive.

[Sources]
- Course-owned redacted Supabase interface capture, August 25, 2026: textbook/figures/cloud_interfaces/supabase_project_overview.png. Vendor interface is a third-party rights exception.
- https://supabase.com/docs/guides/platform/backups
- https://supabase.com/docs/guides/database/connecting-to-postgres
- Plan and connection documentation checked September 7, 2026.

## Slide 8

The recovery notebook uses a smaller relative of the Metro Support database. There are three users, three tickets, and five events. The small size is intentional. We can trace each ticket back to a requester and inspect what an incorrect restore would change.

In the users table, user_id is the primary key. A ticket has its own ticket_id and stores requester_id as a foreign key referring to a user. A user can request more than one ticket. Each event has an event_id and a ticket_id referring to its parent ticket. A ticket can have multiple events.

The foreign keys make these relationships enforceable. They are more than matching column names. If a restore copied the rows but omitted the rules, later writes could produce states that the original database would reject. That is why we test behavior as well as existing data.

There is also a named status check on tickets. It permits the specified status vocabulary, including open and in_progress, while rejecting the invalid value almost_done. We will use that difference in a controlled failure test.

Do not confuse this fixture with the full Metro Support dataset from earlier chapters. The full baseline has eight users, twelve tickets, and twenty-one events. The notebook baseline is three, three, and five. Neither number is universally correct for every exercise. A recovery comparison must use the actual source state that produced its archive, including any intentional changes made before the export.

[Sources]
- Course recovery notebook, setup_sql and expected_baseline.
- Course textbook, Chapters 2 and 8.

## Slide 9

This code can look unfamiliar because it combines tools at different layers. The outer expression is Python. It calls subprocess.run with a list of command arguments. The program represented by PSQL is the PostgreSQL command-line client. The text following the command option is SQL that psql sends to the database server.

The database name comes from SOURCE_DB. It is a variable containing the unique practice database name created earlier in the notebook. The SELECT asks the server to count tickets. The server evaluates that SQL and sends a result back through psql to Python.

The options at the bottom control Python's interaction with the program. check equals True makes an unexpected nonzero exit stop the cell. text equals True gives us readable strings. capture_output equals True keeps the output available so a later cell can compare it with the restored result. A successful launch alone would not prove the query succeeded, which is why checking the result matters.

In Colab, PG_PREFIX runs the local command as the postgres operating-system user. That identity owns the local PostgreSQL service and needs access to the temporary archive directory. It is separate from the Python variable holding a database name.

You do not need to design a wrapper library to complete this lab. Follow the arguments, identify which database receives the SQL, and read the returned output. When adapting the known-ticket check, you will change a small query inside the same visible pattern.

[Sources]
- Course recovery notebook, preparation and query cells.
- https://docs.python.org/3/library/subprocess.html#subprocess.run
- https://www.postgresql.org/docs/15/app-psql.html

## Slide 10

This slide shows the shell form of the notebook's dump operation. In the notebook, Python supplies the same kinds of arguments as a list and adds the local command prefix where needed. The SOURCE_DB variable holds a database name. It does not contain a password-bearing connection URL.

The format option selects a custom archive. That archive is intended for pg_restore. The schema option limits the selected content to metro_support. The file option names the output artifact. The database option identifies the source from which PostgreSQL exports the objects and rows.

The no-privileges option omits grant commands. That makes the classroom restore less dependent on recreating the original access configuration, but it also means the archive cannot by itself establish that application permissions have been recovered. We must state that omission.

Ownership suppression needs particular care. For a custom-format archive, pg_dump ignores no-owner. The appropriate place to request that behavior is pg_restore. You will see that option on the restore command shortly.

For this lab we use clients matching the server's major version. An older pg_dump cannot export a newer-major PostgreSQL server. Although some cross-version migrations are supported, restoring an output into an older-major target is not generally promised to work. Matching versions keeps our beginner exercise focused on recovery rather than migration compatibility.

The selected schema is also the scope boundary. Server roles, other databases, and cloud project settings are outside this particular archive. A real recovery plan must list required dependencies that the selection leaves out.

[Sources]
- https://www.postgresql.org/docs/15/app-pgdump.html
- Course recovery notebook, dump and tool-selection cells.

## Slide 11

After creating the archive, we inspect it before trying the restore. pg_restore with the list option reads its table of contents. The list should include the expected schema, table definitions, table data, and associated constraints. This lets us notice some obvious omissions before depending on the file.

An inventory is still not an executed restoration. The target might lack a required dependency, or a command could fail when PostgreSQL tries to create an object. That is why the next stage actually restores the archive into a separate database.

File size answers a narrower question. A nonempty file has bytes, but those bytes might describe the wrong database or an incomplete scope. We record size without treating it as a correctness test.

The notebook also computes SHA-256, a cryptographic hash of the archive bytes. If we compare that result with a trusted hash recorded earlier, a mismatch tells us the artifact changed. A hash computed from a bad original file does not magically make that file good. It identifies bytes, not their business meaning or trustworthiness.

There is a security issue here too. Restoring a dump can execute SQL chosen by privileged users on the source. An unfamiliar archive is therefore not passive data to try against an important database. Today's permitted artifact is the one you created from the synthetic notebook fixture. For a real external source, an approved inspection and isolated restore procedure would be necessary before use.

[Sources]
- https://www.postgresql.org/docs/15/app-pgrestore.html
- https://www.postgresql.org/docs/15/app-pgdump.html
- Course recovery notebook, archive-list and checksum cells.

## Slide 12

The first command creates the destination database. RESTORE_DB and SOURCE_DB hold different names. The notebook gives both a unique suffix so this run does not overwrite a database from another run. The target starts empty.

The restore command then reads the custom archive. Exit-on-error stops after an error instead of continuing through later archive items and leaving us with a misleading mixture of successes and failures. Single-transaction keeps this small restore together as a transaction, so a failure does not retain a partly restored set of transactional objects.

That option does not remove objects already present in a target. It is not permission to point the command at a populated project. We begin with the empty database created specifically for the drill and avoid adding destructive cleanup options to force a restore over unfamiliar objects.

No-owner and no-privileges mean we are not restoring the source's original ownership and grants here. That is useful for a portable classroom example, but application access needs a separate reviewed procedure. A successful restore under the local administrative identity does not prove that an application's restricted identity can connect or operate correctly.

There is another boundary to notice. The source and target are separate databases on the same temporary server. This protects the source from being overwritten during our experiment. It does not protect either database or the dump from losing the notebook runtime. A production backup retention design would need an appropriate independent location and access arrangement.

[Sources]
- https://www.postgresql.org/docs/15/app-pgrestore.html
- Course recovery notebook, restore and cleanup cells.

## Slide 13

Now we compare specific results. The notebook's source has three users, three tickets, and five events. Those same counts should appear in the restored target. The query also looks for tickets that have no matching requester. It expects zero in this fixture.

The grouped status report asks another question. There is one in-progress ticket, one open ticket, and one resolved ticket. If a restore or later mistake changed a status while preserving the total ticket count, that report could reveal the difference.

We also check the expected table names and the named status constraint. The notebook compares the complete expected result lines, not an accidental substring such as users equals three appearing inside users equals thirty. That is a programming detail with a general lesson: a test has to compare the property it claims to compare.

These checks are deliberately varied. Table names concern structure. Counts concern quantities. The missing-requester query concerns existing relationships. The status report concerns a useful grouping. None of them, by itself, verifies every property of the recovered database.

In particular, changing a ticket's subject does not change its table count or its status group. Swapping one valid requester for another may preserve the foreign-key rule while changing the meaning of the record. We therefore add a known-ticket comparison next. When you write your recovery account, explain which checks you ran and which types of error they could detect. Avoid the much broader claim that a few checks prove everything.

[Sources]
- Course recovery notebook, source_check_sql and expected_baseline.
- Course textbook, Chapter 8, Verify Structure, Data, and Behavior.

## Slide 14

This query follows a relationship that you already know. The tickets table gives us the ticket identifier, status, and subject. The join matches requester_id to the user's primary key and retrieves the requester's display name. The WHERE condition narrows the result to ticket 1001.

In the notebook's source fixture, that ticket is open, its subject is Streetlight dark near bus stop, and the requester is Maya Chen. Running the same query against the restored target should produce the same selected values.

Now consider changing only the restored subject to Incorrect subject. We would still have three tickets. We would still have one open ticket. The requester relationship could remain valid. The earlier count and status checks could all look normal. This query exposes the changed value because it examines the particular record we care about.

There is one more comparison beyond source versus restore. We should compare with the intended record in the original setup. If the source was already wrong before the export, a perfect restoration would reproduce that wrong state. Equality between two outputs establishes agreement, not independent correctness of the original data.

Your lab adapts this supplied query to ticket 1002 or 1003. You can read those original INSERT statements directly, so the exercise does not depend on guessing the correct answer. Explain what the selected values add to the earlier checks. That is a modest change in code, but a meaningful change in the question you are testing.

[Sources]
- Course recovery notebook, setup_sql and Your Check: Compare One Known Ticket.
- Course textbook, Chapter 8, Data verification.

## Slide 15

A database can contain apparently correct rows while missing a rule that should govern future writes. This test asks whether the restored status constraint still enforces the allowed vocabulary. The proposed value almost_done is deliberately outside that vocabulary.

The intended outcome is a check-constraint violation. PostgreSQL identifies that error category with SQLSTATE 23514. The notebook also checks the exact constraint name, tickets_status_allowed. If the server instead reports a missing table, a syntax error, or a connection failure, that is not a successful test of the status rule.

The transaction around the write protects the practice state. If the constraint rejects the insert, the connection's failed transaction cannot commit. If a missing constraint unexpectedly allows the insert, the following rollback still discards it. The notebook checks afterward that test ticket 1099 does not remain in the table.

This is a useful pattern for testing a denial or a safety boundary. State the operation that should fail, state the intended reason, and inspect the actual failure. Simply celebrating red error text is not enough, because many unrelated faults produce errors.

The statement is specific to the small notebook fixture, where user 101 exists and ticket 1099 does not. Those prerequisites keep a missing requester or duplicate key from becoming the reason for rejection. In your own case, choose a controlled test whose other inputs are valid. That lets you isolate the rule you intend to examine.

[Sources]
- Course recovery notebook, expected-failure cell.
- https://www.postgresql.org/docs/15/errcodes-appendix.html
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 16

The lab gives you the complete recovery sequence in one notebook. Download it from the Week 8 guide, open Colab, and use File, then Upload notebook. No Supabase password is required. The setup starts local PostgreSQL inside the runtime and uses uniquely named practice databases.

Run the notebook in order and read the output as you go. The source baseline comes before the dump, which comes before the separate restore. The later cells reuse variables created by earlier cells, so skipping directly to a restore or verification cell can leave required names undefined.

When you reach the known-ticket section, first run the supplied check for ticket 1001. Then adapt it to ticket 1002 or 1003. Read the original INSERT for your chosen ticket and compare the selected values. Explain what this catches that the row counts could miss. You may extend the selected columns if you want a different meaningful check.

Write the short recovery account in the notebook itself. Use the actual results already there. State the separate target, summarize what the checks established, and name something you have not tested. Explain which connection would change for a permitted Supabase source. There is no second report to assemble.

After retaining the output, run the final cleanup cell. It removes this run's practice databases and temporary artifact folder and stops the Colab practice service. Submit the completed notebook individually through Brightspace. The dump is a disposable practice artifact, not an additional submission.

[Sources]
- Week 8 lab_01_backup_restore.md.
- Course recovery notebook.

## Slide 17

The second class brings the first half of the course together. A working schema has to do more than accept a few inserts. Its relationships must represent the problem correctly, its transactions must preserve intended changes, and its operations must remain understandable when something waits, fails, or needs recovery.

We will use the midterm operations case as the setting for that review. The assignment already contains the requirements and rubric. The slides will help you reason through the operations without creating a second, competing set of requirements.

One distinction is worth making immediately. The midterm includes both transaction work and a blocking investigation. They are related, but they are not interchangeable. Showing a rollback in one connection does not show that you diagnosed another connection waiting for a lock. Likewise, a blocking observation does not by itself show a correct committed business change.

The improvement part offers alternatives such as access control, an index, or a safe schema change. Choose a problem that your case actually has and use a relevant comparison to examine the proposed improvement.

Recovery is also part of the case. The required midterm work is a recovery plan. Performing an additional restore for the midterm is optional. Yesterday's recovery notebook gives you experience that can make the plan precise, but it does not justify claiming that a different project has been restored if you did not run that test. Our clinic will help you connect your actual work to the explanation beside it.

[Sources]
- Course assignments/midterm_project.md, canonical requirements.
- Course textbook, Chapters 4 through 8.

## Slide 18

Here is a small schema-change rehearsal using the disposable notebook fixture. We begin a transaction and add a nullable text column named follow_up to the tickets table. Existing rows can have NULL in this new column, so the example does not invent follow-up values for every old ticket.

The catalog query asks whether that column exists. information_schema.columns describes columns that the current user can see. The filters identify our schema, our table, and the new column name. Inside this transaction, the query returns follow_up.

The final rollback discards the change. If we run the same catalog query afterward, it returns no rows. This demonstrates transactional DDL for this PostgreSQL operation. It is a rehearsal: the example intentionally leaves the original schema in place.

Do not infer that every schema change is harmless or that every database system treats every DDL command this way. Even a transactional ALTER TABLE can acquire locks. A long transaction can block other work while it remains open. A production migration also needs a compatibility plan for the application and a decision about old and new code running together.

We would use this example to discuss a possible safe-change improvement, not to require everyone to add this particular column to the midterm. The relevant question is what your application needs and how you would show that the old required behavior still works. If a change commits and later proves harmful, the recovery decision becomes different from this simple rollback rehearsal.

[Sources]
- Course textbook, Chapters 4 and 8.
- https://www.postgresql.org/docs/15/sql-altertable.html
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 19

The response depends on the state of the change. In the first row, the harmful write remains inside an open transaction. If we control that transaction and agree that its work should be discarded, rollback may be the appropriate response. We coordinate with its owner because the transaction may contain other work as well.

In the second row, the mistake has already committed, but we know a small correct repair. A reviewed compensating change may be safer than replacing the database with an older state. We still need to avoid overwriting valid changes that happened afterward. Knowing that a row was wrong yesterday does not tell us that its current value should be replaced blindly today.

In the third row, the required state is missing and an earlier recovery source is necessary. We can restore that source into a separate target, inspect it, and decide how to recover the required content. Before directing application traffic to that target, we consider valid newer changes, permissions, and application behavior.

These are candidate responses, not automatic rules based on a single word in an incident report. Scope and consequences matter. Losing one table, losing an entire database, and losing access credentials may need different procedures.

For the midterm, explain why the chosen response fits the actual problem. A backup is valuable preparation, but its existence does not make restoration the safest answer to every issue. A waiting connection, for example, may be resolved by dealing with an open transaction rather than recovering old data.

[Sources]
- Course textbook, Chapter 8, Safe Migrations and Recovery Are Connected.
- https://www.postgresql.org/docs/15/tutorial-transactions.html

## Slide 20

This table recalls the blocking exercise from Week 5. Session A changed a ticket and left its transaction open. Session B then tried to update the same ticket and waited. A separate diagnostic connection let us inspect the situation without depending on the waiting connection to diagnose itself.

The blocking relationship is the important observation. A slow-looking operation can be waiting for another transaction rather than doing an expensive scan. Adding an index would not necessarily resolve that wait, and restoring an earlier database would not be an appropriate first response to it.

The pg_blocking_pids function helps identify which backend is blocking the waiting backend. We connect that information with the transaction states and the operations we deliberately started. A backend identifier on its own is not a business explanation. We need to know which practice operation it belongs to and why it still holds the relevant lock.

After the owner resolves A by committing intended work or rolling back unwanted work, B can proceed. We then query the final row to see which changes remain. That final verification matters because releasing a lock and obtaining the intended database state are related but different outcomes.

For your midterm, use the blocking path allowed by the canonical assignment and label the environment accurately. If you analyze the supplied trace instead of running concurrent sessions, describe it as trace analysis. Do not write that you observed live blocking if you did not. Close your practice transactions and connections when the exercise ends.

[Sources]
- Course Week 5 blocking notebook and canonical midterm assignment.
- https://www.postgresql.org/docs/15/functions-info.html
- https://www.postgresql.org/docs/15/explicit-locking.html

## Slide 21

An improvement needs an operating problem and a comparison that addresses it. If a reporting identity can modify data, a least-privilege role is a relevant improvement. We should test both the allowed read and a write that should be denied. Testing only the read would leave the unwanted capability unexamined.

If one application user can see another user's rows, row-level access control may be the relevant mechanism. The comparison needs different identities and expected visible rows. Running every query as the database owner could bypass the very boundary we intend to test.

If a small queue query requires a broad scan, an index may provide another access path. We compare the same result identifiers before and after, read the plan work, and account for the index's storage and unmeasured write costs. A faster query that returns different tickets is not a successful optimization of the original question.

If the application needs an additional field, a safe schema change may be the right improvement. We examine whether the old required behavior still works and how the change could be reversed or repaired if necessary.

These are alternatives from the midterm, not four additional tasks. Choose the option that fits your case and that you can explain using actual results. The quality comes from connecting a problem, a change, and a relevant test. Adding several mechanisms without understanding them can make the case harder to reason about without improving the database.

[Sources]
- Course assignments/midterm_project.md, Evaluate One Improvement.
- Course textbook, Chapters 4, 6, and 7.

## Slide 22

A recovery plan becomes useful when another operator can identify its purpose, target, and acceptance checks. This example concerns the Metro Support schema after an accidental loss. The target must be an approved empty database separate from the source, so the rehearsal does not destroy the only current copy.

The checks should use the actual project's baseline. If you use the full Metro Support fixture, do not copy the small notebook's three-three-five counts. If your project intentionally changes the seed data, explain which state the planned archive will represent and how you will establish the expected results.

A known-ticket query and a meaningful report complement the structure and count checks. An intended constraint failure examines future behavior rather than only existing rows. If application service is the recovery objective, roles, permissions, and a safe application connection also belong in the plan.

Be explicit about the distinction between planning and execution. The midterm requires a recovery plan. An executed restore is optional extra work. A plan can say that an operator will compare the selected ticket after restoration. It cannot honestly say the comparison passed unless someone performed it against the relevant target.

The same distinction applies to time objectives. You can state an RPO or RTO requirement and explain the mechanism intended to support it. A fast restore of a tiny classroom fixture does not establish that a much larger production service will meet that target. State which part you measured and which part still requires a drill.

[Sources]
- Course assignments/midterm_project.md, Plan Recovery.
- Course textbook, Chapter 8, Worked Example: A Recovery Runbook Entry.

## Slide 23

Read this example as an operator's handoff to another person. It begins with the scope: the three-table practice archive. It names the separate restore, then explains several observations. The counts and grouped report matched. The selected ticket retained its subject and requester. The status rule rejected the invalid value.

The last sentence names important unfinished work. The drill did not restore application roles or test application reconnection. Consequently, it does not establish that the full service is ready for users. That limit is part of the technical result, not an apology for it.

Compare this with a statement such as everything worked. That statement leaves the reader unable to tell which database was tested, which properties were checked, or what remains unsafe to assume. A precise explanation can be short while still letting another operator decide the next action.

This is also a useful professional writing habit. An engineer may need to summarize a restore drill in an issue, a handoff note, or an incident review. The reader needs enough detail to understand the result and its consequences without reading every line of terminal output.

Your own account must reflect your actual work. If you selected ticket 1002, explain that record rather than copying ticket 1001 from this slide. If a check failed, report the failure and the next step rather than substituting the expected result. For the midterm, connect the explanation to the project's tested operations and distinguish any recovery plan from an executed restore.

[Sources]
- Worked course example based on the recovery notebook's operations, not a production incident.
- Course textbook, Chapter 8, verification and runbook discussions.

## Slide 24

The remaining class work uses the materials already connected in the Week 8 guide. Chapter 8 contains the recovery concepts, command reference, and runbook example. The Week 5 notebook contains the blocking experiment. The canonical midterm assignment contains the requirements and rubric, including the allowed alternatives and the submission format.

Choose one incomplete part of your own case that you can improve now. Begin with the actual failure or uncertainty. Perhaps the setup does not run from a clean state, a query duplicates tickets through a join, a transaction demonstration leaves the wrong final value, or an improvement lacks a meaningful comparison. Fix that part and rerun the relevant test before revising the explanation.

When asking for help, show the specific command or query, the actual output, and the result you expected. That lets us diagnose the operation instead of guessing from a general statement that the database does not work. Do not include a password or private connection URL in the material you display.

This clinic adds no separate report. Keep the work in the midterm files described by the assignment. The purpose of class support is to help you understand and complete the existing case, not to multiply submissions.

Next week we begin NoSQL models and JSON. We will compare them with relational strengths you now understand: explicit keys and relationships, constraints, transactions, and declarative queries. Alternative models make more sense when you can explain what they preserve, change, or trade away for a particular workload.

[Sources]
- Course Week 8 guide and canonical midterm assignment.
- Course syllabus, Weeks 8 and 9.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
