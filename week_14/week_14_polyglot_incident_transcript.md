# Week 14: Polyglot Incident Response and Final Project Clinic - Spoken Transcript

## Slide 1

The staff member has resolved a request, but the resident still sees it as open. Each person is looking at a plausible screen. The immediate problem is deciding which stored fact establishes the accepted state and why the other screen has not caught up. This is a common kind of integration problem, even when each database can answer its own queries successfully.

Our case uses PostgreSQL for the authoritative ticket and MongoDB for a resident-facing projection. Polyglot persistence means an application uses different data technologies for different responsibilities. It does not require every project to use several databases. We will study this two-store design because it makes partial failure visible, not because adding another product automatically improves a small system.

Today we will trace one change, examine the transaction that records it, and experiment with repeated and delayed events. The notebook gives us an actual local SQLite transaction and a small Python model of the derived copy. That combination lets us inspect the mechanism without deploying a message broker or managing another cloud account.

The second meeting applies the same reasoning to your existing final project. You will work on a specific operational gap, such as access, an index decision, or a recovery check. The aim is a system you can explain and investigate, with a clear distinction between what your experiment demonstrated and what would require further production work.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08.

## Slide 2

An authoritative record is the record whose accepted update establishes the business fact we are discussing. In this application, the staff operation changes ticket status in PostgreSQL. That is why we treat that row as authoritative for status. This is an application ownership decision, rather than an inherent rule that relational databases always outrank document databases.

A projection is a derived representation arranged for a particular read. The resident page may need a compact document containing ticket details and the latest status. Keeping that representation separately can simplify a read, but someone must maintain it when the source changes. A copy advertised as current becomes misleading when it silently stops updating.

The source version lets us compare accepted progress for the same ticket. Version seventeen follows version sixteen in this ticket's source sequence. It is not the time at which a consumer happened to receive a message. A consumer may receive an older event after a newer one.

Ownership should be stated at the level of facts. PostgreSQL might own status while an object store owns attachment bytes and another system owns independent audit history. We could not reconstruct those bytes merely from a PostgreSQL filename. During repair, we therefore identify the field, its owner, and the direction of reconstruction before copying anything. That prevents a stale display value from accidentally becoming the new authority.

[Sources]
- CST4714 textbook, Chapter 14, sections on ownership and projections.

## Slide 3

Consider an application that sends two ordinary database writes. It first commits the staff update in PostgreSQL. It then tries to update the MongoDB document. If the second action fails, the first action has already changed durable state. Returning an error message to the browser does not travel backward in time and undo that committed transaction.

The important boundary is between the two operations. A PostgreSQL transaction can coordinate its own participating statements. A separate network call to MongoDB does not automatically join that transaction simply because the calls appear next to each other in Python. Reversing their order leaves the same category of problem, with the other store potentially changing first.

This does not mean every integration must use one particular architecture. Some systems coordinate distributed transactions, some use compensating business operations, and some accept asynchronous copies. Each approach has requirements and costs. Our class example uses a transactional outbox because it lets us connect a familiar local transaction to a recorded integration event.

Before that solution, retain the failure model. The application can know that the source committed while still being uncertain about the second write. An error handler should preserve the operation identifier and the known outcome. Silently retrying both writes as if nothing happened may repeat an effect. We need a repair path that understands already-accepted work.

[Sources]
- CST4714 textbook, Chapter 14.
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

## Slide 4

A timeout describes an observation by the client. It tells us that the client did not obtain a suitable response before its deadline. It does not, by itself, tell us exactly what happened inside the remote database.

In the first row, the request never arrives, so no remote write takes place. In the second row, the server applies the write but the response is lost or delayed. The client can see a timeout in either case. Those two histories require different interpretations, even though the exception message can look similar.

That is why our investigation uses stable identifiers and a subsequent record comparison. We look for the particular ticket and event rather than assuming every timeout means a failed write. In the supplied incident, a later MongoDB read still shows version sixteen. That later observation establishes that this projection is behind the source version seventeen. The timeout alone would have been weaker information.

Safe retries must tolerate the possibility that an earlier attempt already applied. Setting a field to an intended value can be repeat-safe under a suitable ordering policy. Incrementing a counter again can create an extra effect. A production design also needs to consider the read's consistency and whether a newer event arrived meanwhile. We will keep those limits explicit while using a small, understandable experiment.

[Sources]
- CST4714 textbook, Chapter 14, supplied incident and partial-failure explanation.

## Slide 5

These three values answer different questions. The ticket identifier tells us which business record we mean. Ticket one thousand eight should refer to the same ticket when it appears in a source row, an event, a consumer log, or a derived document. A shared identifier makes correlation possible, but it does not prove that the records contain the same values.

The event identifier names one recorded change. Event e-v-t, one thousand eight, seventeen is a particular event for that ticket. A retry should preserve that identity rather than inventing a new identity for the same logical change. This allows us to connect repeated delivery attempts to the work they represent.

The source version represents order within this ticket's accepted update sequence. Version eighteen comes after seventeen for ticket one thousand eight. It says nothing about the version sequence of another ticket. It also does not tell us that the consumer received the events in that order.

In our data, versions are positive integers assigned by the source. We assume a single authoritative sequence per ticket. If several writers independently assign conflicting versions, the simple comparison we are about to use is insufficient. Likewise, an event ID alone does not solve ordering. Identity lets us name work, while the version lets us compare the progress represented by complete-state events for the same ticket.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08 synthetic ticket fixture.

## Slide 6

The transaction on the left contains two database changes: the business ticket update and an outgoing event row. They commit together. If the transaction rolls back, neither change becomes committed work. This closes the gap in which the source status changes but the application never records that it needs to notify another part of the system.

The outbox is an ordinary table used for this outgoing work. After the transaction commits, a relay reads recorded events and publishes them. A consumer receives those events and updates the resident projection. Relay and consumer describe responsibilities. A small implementation may combine responsibilities in one process, while another architecture may separate them.

The arrows after the transaction still cross failure boundaries. A relay can send an event and stop before recording its acknowledgment. On restart it may send the event again. A consumer can apply a change and lose its acknowledgment. Repeated delivery is therefore a normal possibility that the receiving operation must handle.

The diagram gives us one atomic source boundary followed by retryable delivery. It does not promise immediate cross-store consistency or exactly-once effects throughout the application. We still need stable identity, ordering rules, and checks for stalled progress. The notebook first isolates the local transaction so we can see what that boundary guarantees before reasoning about the separate delivery behavior.

[Sources]
- CST4714 textbook, Chapter 14.
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html

## Slide 7

Notebook zero eight has three connected parts. The first creates a small SQLite database inside the Python process. It contains three synthetic tickets and an empty outbox table. SQLite executes real SQL statements and real local transactions. We are using it to observe commit and rollback behavior without requiring a new cloud connection.

The second part uses a Python dictionary as a model of the resident projection. A list of events arrives in a chosen order, and a loop decides which events can change that dictionary. This is deliberately smaller than a deployed MongoDB consumer. It makes the decision rule visible, but it does not simulate network timing, concurrent processes, or durable queue acknowledgments.

The third part compares source identifiers and field values with a wider projection. It reveals why a matching count can conceal missing records and incorrect values. The final cleanup closes the local database. No cloud resources or network access rules are created by this notebook.

The weekly page links the notebook. Download it, open Colab, and choose File, then Upload notebook. Run the cells in order. The first part supports our shared transaction demonstration, and the delivery experiment is your individual practice. Your submission will be one Brightspace text incident update. The notebook remains working material rather than becoming a second file you must submit.

[Sources]
- CST4714 Notebook 08 and Week 14 lab.
- https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager

## Slide 8

This excerpt begins after the initialization cell has created the tables and inserted the starting tickets. Ticket one thousand eight initially has status open and source version sixteen. The with block manages the transaction for this SQLite connection.

Inside the block, the update temporarily changes the ticket to resolved at version seventeen. The question marks are parameter placeholders. The tuple supplies the values separately from the SQL statement. We then deliberately raise a RuntimeError before inserting an outbox event. The exception leaves the with block, which causes the pending transaction to roll back. The surrounding except block prints a description after that rollback.

The stored result is therefore open at version sixteen, with zero outbox events. The update statement executed, but the transaction did not commit. That distinction is central to interpreting a log saying that an application reached a particular line of code.

The placement of exception handling matters. If an application catches and suppresses an error inside the transaction block, it may allow the block to exit normally. Here the exception crosses the transaction boundary before we catch it. Also remember that this context manager does not close the connection. The notebook keeps the connection for the next demonstration and closes it explicitly in the cleanup cell. These are SQLite results, not observations from a PostgreSQL server.

[Sources]
- CST4714 Notebook 08, rollback cell.
- https://docs.python.org/3/library/sqlite3.html#how-to-use-the-connection-context-manager

## Slide 9

This attempt puts both intended writes in one transaction. The update includes the expected starting version in its predicate. It can change ticket one thousand eight from version sixteen to seventeen only while the stored version still equals sixteen.

The cursor's row count tells us whether that transition matched a row. If it matched one row, the next statement inserts the outgoing event. A normal exit from the transaction block commits the ticket change and its event together. The outbox schema also has a unique ticket-and-version pair, so two different event IDs cannot represent the same accepted version in this small example.

If the event insert fails, the transaction rolls back its earlier ticket update. That is the useful guarantee. We are avoiding a committed new source status without its associated outgoing record. The event's presence still does not mean it has been published or applied elsewhere.

Rerunning this successful transition after it has committed no longer matches version sixteen. The complete notebook reports that zero-match case instead of adding another event. A real application must inspect why a conditional update did not match. The row might be absent or another accepted update might have advanced it. Treating every zero match as an identical successful retry would hide those differences. Our fixture is small enough to read the resulting ticket directly.

[Sources]
- CST4714 Notebook 08, successful transaction cell and schema.
- https://www.postgresql.org/docs/current/tutorial-transactions.html

## Slide 10

The table separates the stages we can actually observe in the notebook. Fresh initialization produces an open ticket at version sixteen and no outbox events. The deliberate failure returns us to exactly that committed state. The successful attempt produces resolved at version seventeen and one recorded event.

For the later delivery experiment, the notebook then performs another accepted source update. Staff close the ticket at version eighteen, and the same transaction records its outgoing event. At that point there are two outbox rows. This later version does not rewrite the paper incident's earlier observation. The supplied incident stops at version seventeen, while the experiment continues the story.

Recorded, published, and applied describe different milestones. These cells record events in a local table. They do not start a relay, deliver messages, or update a remote MongoDB collection. Two outbox rows therefore establish that outgoing work exists, not that two resident pages have changed.

This separation gives us a useful debugging habit. State which milestone a count or timestamp supports. An outbox count can help locate work waiting to leave the source. A consumer checkpoint can describe receipt or processing progress. A read of the derived document can show the version currently served. None of those observations automatically substitutes for all the others, especially when a service is paused or acknowledgments have been lost.

[Sources]
- CST4714 Notebook 08 and Week 14 supplied incident.

## Slide 11

Idempotency means that applying the same operation again has the same intended final effect as applying it once. Setting a status to resolved can have that property. If the record already contains resolved, assigning resolved again leaves the same value. Adding one to a counter does not have that property by itself. Two applications produce two increments.

Ordering is a separate issue. Suppose a ticket becomes closed and then an old event assigns open. Assigning open repeatedly is repeat-safe in the narrow sense, but it still replaces a newer accepted state with an older one. Being idempotent is therefore not a complete correctness argument for an event handler.

Our experiment uses complete-state events. Each event carries the intended status at a particular source version. The consumer accepts only a version newer than the one it already holds. Duplicate and older complete-state deliveries become no-ops under that rule.

There are assumptions behind the rule. All events in this loop describe the same ticket, their versions come from one authoritative sequence, and their payloads describe the whole projected status. We are not applying arbitrary financial transfers or independent increments. A side effect such as sending an email would also need its own repeat-handling policy. Keeping the operation's meaning explicit prevents a useful version check from becoming an overgeneralized promise about every event-driven system.

[Sources]
- CST4714 textbook, Chapter 14, and Notebook 08 delivery experiment.

## Slide 12

The loop reads each event from the delivery list. When version enforcement is enabled, it compares the incoming source version with the version currently stored in the projection. An incoming version that is equal or smaller is ignored. A larger version can update the status, stored version, and last event identifier.

The last event identifier records which applied event supplied the current projected state. Receiving a duplicate does not replace that state with an extra history entry. This particular model stores the latest state rather than accumulating an event log in the projection itself.

Each execution of the complete cell resets the projection to open at version sixteen before processing the list. That makes comparisons between experiments meaningful. Changing a flag and rerunning the cell starts from the same initial condition rather than carrying an unknown result from an earlier run.

This loop is intentionally single-consumer Python. The comparison and dictionary assignment are separate language operations. We must not copy that read-then-write arrangement into two independent database workers and assume it is race-free. Two workers might both read an old version before either writes. Later in the deck we will express the comparison and update in one MongoDB command. For now, the small loop lets us reason about the acceptance rule and inspect the result after every delivery.

[Sources]
- CST4714 Notebook 08, Section 2.
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 13

Read this trace from top to bottom, starting with open at version sixteen. The first version-seventeen event is newer, so it applies and the resident sees resolved at seventeen. The next delivery is the same event again. Its version equals the stored version, so the guard ignores it.

Version sixteen then arrives late. It carries the older open status, but sixteen is smaller than seventeen. The projection remains resolved at seventeen. Finally, version eighteen arrives with closed. It is newer than the stored version, so the projection becomes closed at eighteen.

The output describes the projection after each delivery, not just the event payload. That is why a line containing an old event can still be followed by the newer resident state. The handler made a decision to leave the stored state alone.

Notice a limit of checking only the final line. With the default order, an unguarded handler could briefly regress to open at sixteen and then finish at closed eighteen because eighteen happens to arrive last. The ending value would conceal the intermediate error. Our individual experiment moves the old event to the end so the regression is easier to see. Both traces matter when explaining why the rule exists. A successful final value under one convenient arrival order is weaker than testing the behavior when delivery order changes.

[Sources]
- CST4714 Notebook 08, default delivery list and guard behavior.

## Slide 14

In the delivery cell, move the entire version-sixteen event entry to the end of the list. Keep the event's fields together. The order should now be seventeen, seventeen again, eighteen, and finally sixteen. Leave version enforcement enabled and rerun that cell.

Next change ENFORCE_VERSION to False and run the same cell again. Compare the final resident status and source version with the previous run. The event payloads have not changed. What changed is whether the consumer refuses a stale version. After observing the broken behavior, restore the flag to True and run it again.

Because the complete cell resets its starting projection, each of those runs is comparable. You are not relying on a leftover dictionary from an earlier experiment. Keep the actual final status and version from the broken and repaired runs for your incident update.

If Python reports a syntax error after moving the entry, check the comma between dictionary entries and the closing square bracket of the list. You do not need to rewrite the loop or introduce another helper function. The small edit is enough to expose the ordering problem. After restoring the guard, continue to the reconciliation section. It will show why fixing the visible ticket still leaves a reason to inspect the other records served by the same application.

[Sources]
- CST4714 Week 14 lab and Notebook 08, individual experiment.

## Slide 15

The distinction in this table is about event meaning. A complete-state event says what the state should be at a particular accepted version. If version eighteen says the current total is three, it may supersede an older complete state, assuming the source is authoritative and the event contains all the fields this projection owns.

A delta event says how to change an existing state. Suppose version seventeen adds one and version eighteen adds two. If we apply eighteen first and then ignore seventeen merely because it is older, we lose the earlier increment. A monotonic version number cannot reconstruct an effect that we chose not to apply.

Delta processing therefore needs an appropriate design for ordering, duplicate detection, or reconstruction. An implementation might replay a complete ordered history, detect a missing version and wait, or rebuild from an authoritative total. The correct choice depends on the operation. We are not implementing those alternatives in today's required lab.

This is useful interview reasoning because it states the boundary of a technique. You can explain that the simple guard works for our ticket's complete-state status events while recognizing that an incrementing inventory stream requires more care. The optional notebook extension explores that difference. The required submission remains the same short incident update using your observed broken and repaired status values, rather than an additional distributed-systems design report.

[Sources]
- CST4714 textbook, Chapter 14, complete-state and delta-event comparison.

## Slide 16

This reference shows the database operation corresponding to the version rule. The filter identifies the existing document by its underscore-ID value and requires its source version to be less than eighteen. The update assigns closed, version eighteen, and the event identifier that supplied that state.

MongoDB evaluates the filter and changes the matching document as one atomic operation. We do not first fetch the version into a separate Python variable and later issue an unconditional write. Keeping the expected condition inside the update prevents a delayed writer from blindly lowering the version after another worker has advanced the document.

The command concerns one existing document. It assumes valid numeric versions from the same authoritative sequence and an event payload that represents the complete projected state. It does not atomically coordinate PostgreSQL, a message broker, and every MongoDB document. Any queue acknowledgment is still a separate responsibility.

The notebook includes this as an explained reference fragment, not an executed cloud cell. Your required experiment runs locally. If you later try the MongoDB operation, use an initialized, disposable practice collection and inspect the matched and modified counts. A zero match has several possible meanings, which we examine next. There is deliberately no unconditional upsert option attached to this version-filtered update, because initialization requires a separate decision.

[Sources]
- CST4714 Notebook 08, corresponding MongoDB operation.
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 17

A matched count of zero tells us that no document satisfied the filter. It does not identify the reason by itself. If the document is already at version eighteen or later, the less-than-eighteen condition should fail. Ignoring that stale or duplicate event is the intended normal behavior.

If the document is absent, there is nothing to update. We need an initialization policy, perhaps based on a verified complete source state. Treating this case as an ordinary already-applied event would leave the resident record missing.

There is a third case that a version-only check cannot repair. A document might claim version eighteen but contain the wrong status. The filter still fails because its version is not older. Repeatedly sending the same event will not discover or correct that corrupted field under this rule. Reconciliation compares values as well as versions so we can investigate that mismatch deliberately.

Adding upsert to every zero-match operation is unsafe here. An existing newer document can fail the version filter. An attempted insert using the same underscore-ID then conflicts with that existing document's identity. The command needs a defined response for an already-current record, an absent record, and incorrect equal-version data. Those are different states, so one unexamined retry option should not stand in for all three decisions.

[Sources]
- CST4714 Notebook 08 and Chapter 14, tested version-filtered update example.
- https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/

## Slide 18

The supplied incident records ticket one thousand eight at a specific observation point. At fourteen-oh-three and twelve seconds UTC, PostgreSQL commits resolved at source version seventeen, and the outbox contains event e-v-t one thousand eight seventeen. The relay later marks it published, and the consumer log separately records receiving that same event.

The consumer then times out while writing the projection and queues a retry. At fourteen-oh-four, the retry worker pauses because its database credential has expired. A later read of the resident projection still shows open at version sixteen.

These observations support a failure after receipt, with the retry path unable to make progress. The published timestamp alone would not prove that the consumer received or applied the event. Here we have the received-event log as an additional observation. Similarly, the timeout alone would not prove the write never happened. The later version comparison establishes that this inspected projection remains behind.

We should not infer that every ticket is wrong or that only this ticket is affected. The paused worker may have a wider backlog. The next investigation would inspect other queued records or the worker's lag. Keep the paper incident's version seventeen distinct from the notebook's later accepted version eighteen. The experiment continues the state sequence to test delayed events, while the incident table preserves the earlier chronology.

[Sources]
- CST4714 Week 14 lab, supplied incident record.

## Slide 19

The first repair addresses the component that cannot progress. In this incident, that means restoring the consumer's approved database access and resuming the recorded work through its normal version-checked handler. We would make the credential change through the appropriate operational process, with the narrow access that this consumer actually needs.

We would not change the authoritative PostgreSQL ticket back to open merely to make both screens agree. The staff update was valid and committed. Replacing it with the stale resident value would create agreement by discarding accepted work. Agreement alone is not the goal if we obtain it from the wrong source.

After resuming delivery, compare the projection with the current authoritative state. If a newer accepted version has arrived meanwhile, the correct result may be newer than seventeen. We should not force every repaired record back to the earlier observation simply because that is the value in the incident report.

Then broaden the check to other queued tickets or consumer lag. The same paused credential can affect more than the first visible complaint. If the repaired path behaves unexpectedly, preserve the observations and pause further changes while investigating. In today's paper incident you propose this operational repair. Your executed notebook results demonstrate the version rule locally. Keep the proposed production action and the experiment you actually ran distinct in the response.

[Sources]
- CST4714 Week 14 lab and Chapter 14 incident response.

## Slide 20

After the guarded experiment, ticket one thousand eight matches its later authoritative state: closed at version eighteen. We now inspect more than that one ticket. The source contains three records, and the resident projection also contains three records. A simple count comparison passes.

Looking at identifiers reveals that ticket one thousand nine is missing from the projection. Ticket nine thousand nine hundred ninety-nine appears only in the projection. Those differences cancel in the total, so an equal count cannot identify them.

Ticket one thousand ten has a different problem. Both sides show version seven, but the source status is resolved while the resident status is open. Comparing versions alone would miss that wrong value. Reconciliation therefore considers the union of identifiers and compares the source-owned status and version fields for each relevant ticket.

The notebook reports three records needing investigation after the guard has been restored. If you leave the guard broken with version sixteen arriving last, ticket one thousand eight adds a fourth discrepancy. This connects the event-order experiment to the broader comparison rather than treating them as unrelated exercises.

We do not compare projection-only processing metadata as though it were another authoritative business field. The last event identifier has a different purpose. A useful reconciliation check states which fields it owns and what equality means after any necessary representation conversions.

[Sources]
- CST4714 Notebook 08, reconciliation fixture and comparison loop.

## Slide 21

The small model rebuilds a separate candidate using the authoritative records. Each ticket identifier becomes a key in the new dictionary, and the source-owned fields are copied into that candidate. The source itself stays unchanged. This makes the repair direction explicit.

The first comparison checks that the sets of identifiers agree. The second compares the owned field values for those identifiers. Both return True for this candidate. The full notebook also reports an empty remaining-mismatch list. These observations are stronger than merely noticing that the two dictionaries have the same number of entries.

This code constructs and checks an in-memory candidate. It does not perform a safe production cutover. A live source may continue accepting writes while a rebuild runs. A projection may contain independently owned annotations that a wholesale replacement would erase. Readers need a controlled way to switch to the verified candidate, and rollback needs its own plan.

An unexpected projection identifier also deserves investigation before deletion. It may reflect an ownership mistake, a deleted source record, or a different lifecycle policy. In our synthetic fixture the intended source is fully specified, so the comparison is straightforward. In a real system, the ownership and deletion rules must come first. The transferable skill is identifying the authoritative direction and validating a candidate without casually overwriting either the source or a live derived store.

[Sources]
- CST4714 Notebook 08, separate rebuild candidate and stated cutover limitations.

## Slide 22

Your submission is one short Brightspace text response. Explain the resident-facing impact, identify where progress stopped in the supplied incident, and propose a repair that respects the source of ticket status. Then include the final status and version you observed in the broken and repaired notebook runs.

The writing combines diagnosis with a small executed experiment. It should be understandable to a colleague who needs to know what is affected and what should happen next. A list of product names is less useful than a clear explanation that the source has accepted a newer status while the consumer cannot advance the resident copy.

Name one broader check before closing the incident. You could inspect other queued tickets or the consumer's lag. Explain why that check relates to the paused worker rather than adding an unrelated metric. You do not need a separate timeline, a matrix of five checks, or a notebook attachment.

Be precise about the status of each action. The supplied record supports your diagnosis. The notebook supplies the broken and repaired local results. The production credential repair is a proposed action, not something you performed in a real incident. That distinction makes the response more useful and more credible. Work individually, using your own observed results, and keep the notebook as working material you can return to when discussing the concept later.

[Sources]
- CST4714 Week 14 lab submission instructions.

## Slide 23

Today we apply the same operational reasoning to your final project. A query that returns an answer is an important beginning. The next step is explaining how the data is represented, which identity can use it, how an important operation behaves, and what would happen if the data had to be restored.

You already have a canonical final-project assignment and rubric. We will use that document instead of introducing a new project or another submission list. Your notebook, script, and project guide can remain the same package. A one-platform PostgreSQL or MongoDB project remains a valid choice.

The incident lesson gives us a method for this clinic. Identify the fact or operation that matters, locate the current state, choose a specific check, and explain what the result supports. A missing permission test is different from a broken query. A backup file is different from a demonstrated restore. Naming the gap clearly helps you spend the class period on the work that will make the project more reliable.

We will review access, index evaluation, recovery, and demonstration choices before you work individually. You do not need to add a second database or a polished application interface. Focus on a small system whose decisions and limitations you can explain. If a cloud connection fails during a demonstration, saved, clearly labeled results can still support a useful technical discussion while you describe the current connection problem honestly.

[Sources]
- CST4714 final-project assignment and Week 14 project clinic.

## Slide 24

An access test is meaningful only when we know which identity performed it. An administrator successfully reading a record establishes that the administrator can read it. It does not show that the intended application reader has the same permitted path or that the reader is prevented from performing a forbidden action.

For a least-privilege claim, test the operation using the identity whose boundary you intend to describe. A reader should be able to perform the allowed read. A forbidden write should fail for the expected permission reason. Use disposable project data and inspect the actual result rather than interpreting any error as a successful security test.

Integrity rules answer a different question. A constraint or validator can reject an invalid value even for an identity that is otherwise allowed to write. That tests a data rule, not necessarily authorization. Both kinds of protection matter, but they should not be described interchangeably.

In Supabase, remember that an administrative SQL session is not the same as an authenticated application's row-level access path. In Atlas, an account that manages the project is not automatically the database user in a driver's connection string. Use the course's earlier access material when choosing the appropriate identity. Never display or submit privileged credentials as part of the explanation. The result should name the role, attempted action, and observed boundary without exposing the secret that authenticated the test.

[Sources]
- CST4714 textbook, Chapter 6, and final-project access requirement.
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://www.mongodb.com/docs/atlas/security-add-mongodb-users/

## Slide 25

An index decision begins with a query and a workload. Our example is finding a resident's recent open tickets. The relevant filter fields and sort order tell us what the database needs to locate and order. An index name by itself does not explain why that structure is useful.

When comparing before and after, keep the query parameters and dataset fixed. Confirm that the returned rows or documents still answer the same question. Then inspect the chosen plan and the amount of examined work. In PostgreSQL, distinguish the planner's estimates from actual execution measurements. In MongoDB, distinguish returned documents from examined documents and keys when the plan provides those statistics.

A small fixture can legitimately use a scan. That is an observation to explain, not a reason to invent a large speedup. Timing can change with caching and other activity, so a single faster run is weak support for a broad performance claim. Describe the environment and method if you report a measurement.

The index also requires storage and maintenance during writes. Your project explanation should connect that cost to a useful access pattern. During the clinic, you can improve an existing index explanation by adding the exact query, the observed plan, and a limitation. You do not need a new benchmarking framework or a paid cluster to make that reasoning specific.

[Sources]
- CST4714 textbook, Chapters 7 and 11, and final-project index requirement.
- https://www.postgresql.org/docs/current/using-explain.html
- https://www.mongodb.com/docs/manual/reference/explain-results/

## Slide 26

A backup command and a restore test answer different questions. A command may create an artifact successfully, but we still need to know what that artifact contains and whether the recovery procedure can recreate useful data and behavior in a separate target.

The first checks compare expected identifiers and selected field values. A familiar query then tests whether the restored data supports an operation that matters to the application. Matching counts alone can hide the same kinds of differences we saw in the projection experiment.

Next inspect required database objects and access behavior. A CSV or JSON data export does not automatically contain every index, constraint, validator, role, or policy. A logical dump's scope also depends on the tool and options. If an object requires a separate recreation step, put that step in the existing project guide rather than implying that the data file includes it.

Record the command and observed elapsed time when you actually execute the restore. That observation describes one run under particular conditions. It does not guarantee a future recovery-time objective under a larger workload or an incident.

Keep the restore isolated from the original project. The original data should remain available while you inspect the restored target. Use the course's platform-appropriate recovery material, and state honestly which steps you executed and which remain a plan. The clinic is an opportunity to replace one uncertain recovery claim with a checked result.

[Sources]
- CST4714 textbook, Chapters 8 and 12, and final-project recovery requirement.
- https://www.postgresql.org/docs/current/app-pgdump.html
- https://www.mongodb.com/docs/database-tools/mongoexport/

## Slide 27

A two-store system needs a recovery order based on ownership. If MongoDB contains only a rebuildable resident projection of PostgreSQL-owned facts, we may restore the authoritative source in isolation and reconstruct the projection from that verified source. We then compare the candidate's identifiers and owned values before coordinating access.

That approach is different from blindly restoring two independent dumps and declaring the application consistent. A PostgreSQL dump taken before a status update and a MongoDB dump taken afterward can represent different application moments. Each artifact may be internally useful while their combination disagrees.

Ownership changes the procedure. If a MongoDB collection contains independent historical events or annotations that PostgreSQL does not own, those records need their own recovery source. Rebuilding only from the relational ticket table would lose information. Similarly, a current source snapshot cannot necessarily recreate a historical state that the application promised to preserve.

The clinic does not require you to turn a one-database project into a two-database project. If you chose one platform, explain its recovery boundary clearly. If you chose both, explain what each owns and how recovery respects that split. The useful professional skill is being able to identify which data can be reconstructed, which data must be preserved independently, and which checks are needed before users return. More backup files do not eliminate the need for that reasoning.

[Sources]
- CST4714 textbook, Chapter 14, recovery order and ownership.

## Slide 28

A demonstration becomes easier to follow when each result is connected to an input and a question. Show one useful query, explain what one returned row or document represents, and state the expected answer for the data you loaded. That gives the audience a way to understand correctness rather than simply watching a command finish.

Then show an operational decision. It could be an index comparison, an expected permission denial, or a separate restore check. Explain the mechanism and the observed result. If the experiment has a limitation, include it where it affects the conclusion instead of hiding it in a vague final disclaimer.

Prepare a saved result for a cloud-dependent step. Label when and where it ran. If the current connection fails, you can show that result while explaining that it is a prior run. It does not become a live result merely because it appears beside the command in a notebook.

The final-project assignment permits a demonstration directly from the notebook or code and results. A separate slide deck is optional. Keep credentials out of both the live view and saved output. An understandable demonstration is not the same as a perfectly smooth demonstration. Being able to diagnose a current failure, explain a previous checked result, and identify what you would test next can still show substantial command of the system you built.

[Sources]
- CST4714 final-project presentation requirement and Week 14 clinic.

## Slide 29

Use the final-project assignment and rubric as the source of requirements. Open the package you have already been building and identify the unfinished item most likely to prevent you from explaining or verifying the system. That item should be specific enough to work on during this class.

For example, a query may return the wrong unit of analysis after a join. An index decision may lack the query it supports. An access explanation may show only an administrator's successful read. A recovery guide may stop after creating the backup file. Each gap suggests a different next action, so avoid treating the clinic as a generic instruction to add more features.

Complete and check the chosen item inside the same notebook, script, or project guide. If you discover a dependency, such as needing correct seed data before evaluating the query, address that dependency first. Record the actual result and the remaining limitation in the guide you already maintain.

This remains individual work. There is no separate Week fourteen project submission, and the platform choices remain unchanged. A small one-platform project with coherent queries and operations can meet the assignment without a second database or a web application. By the end of the clinic, the important outcome is a concrete improvement to your existing project and a clear explanation of the next remaining issue, rather than a new collection of overlapping documents.

[Sources]
- CST4714 final-project assignment and Week 14 README.

## Slide 30

This example of interview language begins by naming the setting accurately: a class experiment. It then identifies the problem, the investigation, and the checks performed. That is more informative than claiming broad experience with distributed databases after running a single notebook.

You can explain that the resident view was stale, that you traced the accepted version through the incident record, and that you tested how duplicate and delayed complete-state events affect a projection. The broken and repaired results give you something specific to discuss. The reconciliation example adds a second insight: equal counts can conceal missing identifiers and wrong field values.

The limits are part of the explanation. Your local dictionary loop did not operate a production queue, coordinate concurrent workers, or perform a live cutover. You can still explain why a production MongoDB update needs the version condition inside its atomic operation and why independently owned data changes the recovery plan.

When translating your own final project, use the same pattern of concrete problem, implemented mechanism, observed result, and remaining boundary. Choose examples you can explain at the level of the actual code and data. Next week we will bring the course together through review, project demonstrations, and career explanations. The goal is to make the database decisions you have practiced understandable to another person, including when that person asks what failed or what you would change next.

[Sources]
- CST4714 textbook, Chapters 14 and 15, and Notebook 08.

## License

Except where otherwise noted, this transcript is licensed under CC BY 4.0.
