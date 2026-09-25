# Week 12: MongoDB Reliability and Recovery - Spoken Transcript

## Slide 1

A resident submits a request, receives a confirmation, and opens the ticket page. The page says that the request cannot be found. We should resist choosing an explanation before examining what happened. The write might not have completed. A database copy might be behind. The client might have lost the response to a write that actually succeeded. A later operation might even have deleted the ticket. Similar symptoms can come from different mechanisms.

Last week we checked whether an aggregation counted the intended records and whether a document rule rejected the intended inputs. This week adds the behavior of multiple database members and the problem of recovering earlier data. A correct query is useful only if we understand which state it can read. A replicated database is useful only if its failure behavior matches what the application promises.

Our first class follows one request through acknowledgment, reading, and a network partition. We will also calculate separate objectives for lost work and time without service. Our second class uses a small recovery notebook. It restores five tickets into another target, reveals a wrong value that several reasonable checks miss, and repairs that document from the saved artifact.

Both labs are individual. The first response stays in Brightspace. The second stays in the notebook. The work is understanding and testing the mechanism, not producing a stack of reports.

Sources: Course Chapter 12, current Week 12 individual labs, and Notebook 05. Opening scenario and teaching sequence are authored course examples.

## Slide 2

A replica set maintains copies of a logical database on multiple members. In this diagram, A is the primary. Under normal operation, it accepts the client's write. B and C are secondaries. They receive changes through replication and apply them to their own copies. The diagram uses the same member names as today's lab so that we can follow one example without changing its labels.

The oplog is a bounded history of data-changing operations used in that replication process. Think of it as the change history that lets a secondary catch up, rather than a separate table that our application normally queries. B and C need not apply each change at precisely the same instant as A. During that interval, their visible data can differ.

This difference is called replication lag. It does not automatically mean that a write has been lost. It means that we need to know which member answered a read and which guarantees that read requested. If a secondary falls behind the history still retained in the oplog, catching up can require more than replaying a few recent entries.

If the primary becomes unavailable, an election may choose a replacement when the necessary members can coordinate. Detecting failure, holding that election, and letting the client find the replacement take time. Multiple members improve the range of failures the system can handle, but do not make every operation uninterrupted.

Sources: https://www.mongodb.com/docs/manual/replication/ ; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ . Native source diagram retained and relabeled for the course A/B/C case.

## Slide 3

Here is the same request represented as a sequence of states. At first, none of the three members contains it. Next, A applies the insert. At that moment A has the request, but the table does not yet show B applying it. C is isolated and still has its earlier state. An application must not turn the fact that one member changed into an unsupported statement about all three.

Now separate retaining a change from applying it. In the third data row, A and B have made the oplog entry durable, but B has not yet applied the insert to its collection. In MongoDB eight point zero and later, with the default majority journaling behavior, those two retained entries can satisfy majority acknowledgment. B's collection can still look older at that moment. In the last row, B applies the insert and its collection contains the request. This extra step is why a successful acknowledgment and an immediately current secondary read are different claims.

Now imagine that a later read reaches C while its older state remains eligible for that read. The request can appear missing there even though A and B retained it. The absence is evidence about the state returned by that read. It is not, by itself, proof that the acknowledged request disappeared from the replica set.

These rows describe a possible sequence, not fixed replication delays. Our three voting members all store data, so two form the majority. C need not participate for A and B to satisfy that condition. The example gives us a reason to connect the confirmation read to the preceding write rather than assume that selecting any secondary will return it immediately.

Sources: https://www.mongodb.com/docs/manual/reference/write-concern/#reads-after---w---majority----writes ; https://www.mongodb.com/docs/manual/core/read-preference/ . MongoDB 8.0+ sequence with default majority journaling, checked September 14, 2026.

## Slide 4

Write concern specifies the acknowledgment the client requests. In our particular three-member example, w equal to one asks for the primary's acknowledgment. That can let the client receive success before another member retains the change. A later failure can therefore have different consequences from a write whose requested acknowledgment includes additional members.

With majority write concern, our three voting, data-bearing members require a majority of two. A and B can provide those acknowledgments in the supplied case. We should not reuse that arithmetic blindly for a deployment with a different combination of voting members and arbiters. The configuration matters, and journaling behavior is part of the durability question.

Asking for three acknowledgments creates a different availability boundary. C is isolated, so the current A/B side cannot collect an acknowledgment from it. A bounded acknowledgment wait can report that the requested condition was not met in time. That report does not reverse modifications that the primary already performed.

The choice follows the application's consequences. A resident's confirmed submission deserves a clear retention promise. A developer also needs a defined response when the promise cannot be confirmed. We should state both the desired success condition and the application's behavior under uncertainty, rather than assume that a stronger-sounding setting makes failures impossible.

Sources: https://www.mongodb.com/docs/manual/reference/write-concern/ . Table applies to the authored three-voting-data-bearing-member case, not arbitrary topologies.

## Slide 5

This is a mongosh example, which means it belongs in the MongoDB shell rather than in a Python notebook cell. The first two lines choose a fresh practice database. The random suffix helps separate this demonstration from a project database or a previous class example. Selecting the database changes the shell's target. The later write creates the stored data.

The inserted document has an internal identifier, submission dash 1099, and a business ticket number, 1099. Keeping a stable identifier for this submission attempt gives the application something precise to ask about later. It is different from creating a new identifier every time a browser retries the same user action.

Notice where writeConcern appears. It is an option to insertOne, outside the ticket document. It changes the requested acknowledgment rather than adding a field to the resident's request. The majority setting names the success condition. The five-thousand value is an acknowledgment timeout in milliseconds. It should not be interpreted as a guarantee that every part of a network operation completes within exactly five seconds.

A normal successful execution demonstrates the command shape and the resulting record. It does not demonstrate what happens when a member fails. Today's first lab is a reasoning exercise, so students do not need to create this shell database or alter a replica set to complete their response.

Sources: Course Chapter 12 acknowledgment example; https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/ ; https://www.mongodb.com/docs/manual/reference/write-concern/ .

## Slide 6

Suppose the client does not receive the acknowledgment it expected. The application now needs to resolve an uncertain outcome. This read asks about the stable submission identifier and retrieves the fields that describe the intended operation. The example illustrates the question to ask, rather than a complete retry library.

If the document exists, its content still matters. Finding the identifier alone is not enough when an identifier may have been reused incorrectly. The application should confirm that the stored ticket represents the same intended submission. A duplicate-key error on a repeated insert similarly tells us that the key is already present. It does not certify that the existing content is the operation we meant to perform.

If the read returns nothing, we must also examine the read path. An unrelated read from an older secondary can return absence even when another side retains the write. The application needs a suitable read-back strategy, bounded waiting, and retry behavior designed for this operation. Blindly producing a new identifier risks creating a duplicate user request.

The distinction between the internal identifier and the business workflow is useful beyond MongoDB. A database can enforce uniqueness for a stored key, while the application remains responsible for associating that key with one intended action. We will use that same distinction when the recovery notebook separately tests its unique ticket-number index.

Sources: Original course read-back illustration; https://www.mongodb.com/docs/manual/core/retryable-writes/ ; https://www.mongodb.com/docs/manual/core/index-unique/ .

## Slide 7

Read preference and read concern address different parts of a read. Read preference selects eligible members. A primary preference directs this ordinary read to the primary. A secondary-preferred route favors an eligible secondary, with the documented fallback behavior. Neither name tells us everything about how recent the returned state must be.

Read concern addresses the consistency and isolation properties of the returned data. Local read concern can expose data that is not majority committed. Majority read concern constrains the read to majority-committed data under the documented semantics. Those words refer to a guarantee about the state, not a command that instantly updates every copy.

Return to the request in our table. C can be behind A and B. An older state that C knows can already be majority committed and still predate the new submission. Therefore majority read concern alone does not mean that this member must return the latest possible value everywhere in the system.

This is why a configuration recommendation should include a specific workflow. An hourly report and a resident's immediate confirmation page have different expectations. We can consider a delayed report route when the application can explain its freshness. For the confirmation page, we need to connect the read to the user's preceding write rather than choose settings from their names alone.

Sources: https://www.mongodb.com/docs/manual/core/read-preference/ ; https://www.mongodb.com/docs/manual/reference/read-concern/ . The report and confirmation comparison is an authored workload example.

## Slide 8

This table gives one concrete candidate for the confirmation workflow. The write requests majority acknowledgment. The following read uses the primary route and majority read concern. Both operations participate in the same causally consistent session. The session is the relationship between these operations, not another database member.

A causal dependency records that the later operation follows the earlier one. With the documented read and write concerns, that relationship supports reading one's own preceding write. It prevents us from treating the confirmation read as a completely unrelated request with no knowledge of the operation that just happened.

A suitable secondary read can also participate in a causal workflow. If that secondary has not reached the required state, the read may need to wait. During a communication failure it may be unable to make that progress before the application's deadline. Preserving the requested ordering does not mean that every read must return immediately.

The workflow also does not freeze the ticket forever. Another authorized operation may change or delete it later. Causal ordering should not be confused with locking out all other users or guaranteeing the globally newest state for every unrelated request. For the lab, explain the promise for this confirmation sequence, the settings that support it, and what the client should do if it cannot obtain that promise in time.

Sources: https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-concerns/ ; https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/ .

## Slide 9

The network partition separates C from the A/B side. A and B can still communicate with each other, and in this example A is already the primary. The absence of C alone does not require A to stop being primary while it remains healthy and connected to the voting majority.

This distinction matters because a diagram of a broken network is not automatically a diagram of a failed primary. We must identify which members can communicate and which operation the client is asking them to perform. A and B can coordinate their active history. C cannot acknowledge a new change that it has not received from them.

The dashed link represents messages that cannot cross the partition as required. It does not mean that the missing member has an independent copy of every future write. A client reaching that side cannot obtain information that the side has not learned merely by selecting a different read preference.

The practical analysis therefore follows the operation. A majority-acknowledged write can complete on the side with the required participants, subject to the other normal conditions. A read on an older side may have to return older information or wait for a guarantee it cannot currently establish. We will use that concrete conflict to explain CAP, rather than treating the three letters as permanent product categories.

Sources: Retained course native partition diagram, relabeled A/B/C; https://www.mongodb.com/docs/manual/core/replica-set-elections/ ; https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-concerns/ .

## Slide 10

Consider a specific ordering of application events. On the A/B side, a write changes a ticket from open to resolved and completes. Only afterward does a new read begin on the isolated C side. Assume there is no intervening write changing the ticket back. C has not learned the new status because the necessary messages cannot cross the partition.

If C answers open from its old state, the answer conflicts with the promise that operations behave like one current copy in this ordering. If it waits for coordination or cannot complete the operation, it sacrifices availability for that operation under the theorem's definition. Returning an unavailable error is not the same as successfully completing the requested read.

The consistency in CAP is a linearizable, single-copy style property. It is not the same use of consistency as the C in ACID, which concerns preserving the application's integrity conditions. Both copies might contain statuses that are individually valid according to a schema, while still giving incompatible current answers.

The availability definition is also stricter than a monthly uptime percentage. The theorem concerns the inability to guarantee the required behavior for every relevant operation during the modeled communication failure. Real applications make more specific promises, but a product label cannot make the missing communication disappear. Today's task is explaining that conflict with the request state in front of us.

Sources: Course Chapter 12 authored partition example; Gilbert and Lynch, 2002, https://people.cs.rutgers.edu/~rmartin/teaching/spring04/cs553/BrewersConjecture-SigAct.pdf .

## Slide 11

Now change the failure. A itself becomes unavailable. If the remaining eligible B and C can communicate, they can form the voting majority of two in this three-member configuration. They can participate in an election to select a primary according to the replica-set rules. This is different from the previous diagram, where A was still present on the majority side.

In the second row, A is lost and B and C cannot communicate with each other. Each remaining member is alone. Neither can independently collect the majority needed for an election. The existence of two surviving machines is not enough if they cannot coordinate.

From the application's perspective, several pieces of work may contribute to an interruption. Members need to recognize the failed primary. An election must complete successfully. The driver must discover a suitable new target. The duration depends on configuration and conditions, so we should not promise that every failover takes one fixed number of seconds.

Drivers can retry supported operations under their documented rules. That is useful, but it does not transform every multi-step application action into a safely repeatable operation. A database retry and a person pressing Submit again are not automatically the same event. Stable identifiers and operation-specific reasoning remain necessary when the application cannot tell which parts of a workflow completed.

Sources: https://www.mongodb.com/docs/manual/core/replica-set-elections/ ; https://www.mongodb.com/docs/manual/core/retryable-writes/ . Table assumes eligible voting data-bearing members and the stated connectivity.

## Slide 12

This example changes the failure category again. The database members are working, and an authorized operation deletes the five tickets. Replication can carry that deletion to the other members just as it carries inserts and updates. The resulting zero count can be a faithful reproduction of the active change history, even though the deletion was a serious human mistake.

The saved export has a different role. It represents an earlier state outside the current collection. If the artifact remains retained and usable, it can provide the old ticket values after the active copies have all accepted the deletion. That is why we need to distinguish service continuity from access to recoverable history.

The table does not promise that every copied file is a sufficient backup. We still need to know which state it represents, what it contains, whether the tool can read it, where it can be restored, and whether the application works afterward. A data file without the required rules or credentials may leave the recovery incomplete.

An oplog should not be described as an unlimited archive of every application state. Its replication history has bounds and operational constraints. Our classroom exercise therefore retains an explicit small artifact and restores it elsewhere. It addresses a logical recovery question rather than assuming that another active replica is the earlier version we need.

Sources: Authored five-ticket deletion example; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ ; https://www.mongodb.com/docs/database-tools/mongodump/ .

## Slide 13

Recovery point objective, or RPO, describes the tolerated gap in recoverable work. This example supplies the actual represented point: the artifact contains the complete dataset as of sixteen ten. The deletion occurs at sixteen twenty-two. There is no later export or replayable event log available in the stated case.

The difference is twelve minutes. Work occurring after the saved point falls outside what this artifact can recover. If the application's objective tolerates at most five minutes of lost work, this artifact does not meet that objective. Restoring it very quickly would not make it contain those missing later changes.

Notice why the represented time is explicit. Saying only that an export finished at sixteen ten would leave open when its contents were read. A long-running export across changing data may not represent one clean instant at its completion time. Our small worked case supplies a complete point so that we can reason without hiding that assumption.

The timeline expresses a time window, not an invented number of lost tickets. We have not been given an arrival rate or a count of changes in those twelve minutes. A careful incident account would preserve that distinction. We can establish that the artifact misses the time-based objective without fabricating how many residents or records were affected during the uncovered interval.

Sources: Original course recovery timeline and Chapter 8/12 recovery-objective definitions. These worked times differ from the assessed Week 12 Lab 1 case.

## Slide 14

Recovery time objective, or RTO, concerns the tolerated time to restore service. The clock does not necessarily begin when someone finally launches a restore command. The incident has already interrupted the service while people detect the problem, retrieve the artifact, and obtain the access or authorization required to use it.

In this worked case, detection takes two minutes. Retrieving and authorizing the artifact takes another minute. Restoring the data and passing the application checks takes four minutes. These phases are sequential in the supplied example, so the observed total is seven minutes. Against a ten-minute objective, this particular drill fits the service-restoration target.

That result does not repair the twelve-minute gap in the saved data. The preceding slide showed an RPO failure even though this slide shows an RTO success. The two objectives describe different consequences. An application can resume quickly with old data, or recover more recent data while remaining unavailable for too long.

We should also distinguish the stated target from evidence about a particular rehearsal. Seven minutes is an observed result under these supplied conditions. It is not a guarantee for every future dataset size, operator delay, network path, or failure. In the lab, use the times that are actually supplied and identify any part of the incident-to-service interval that has not been measured.

Sources: Original course worked recovery timeline; current Week 12 instructor guide. No production service-level guarantee is implied.

## Slide 15

This is the Atlas backup page, captured on August twenty-fifth. The page offers upgrades for continuous or daily backup. Those controls describe available upgrade choices. They are not a record that a backup has run successfully for this free deployment.

The Free-cluster documentation excludes native Atlas backups and directs users to MongoDB Database Tools as a logical backup alternative. It also limits the failure-testing controls available on this plan. We can study recovery using the free plan without purchasing an upgrade.

A separate logical artifact therefore remains relevant. We can create one for a small dataset, keep it outside the active collection, and test recovery in a different target. The notebook chooses an inspectable document-only file so that its contents and omissions are easy to follow. We will compare that narrower exercise with the broader scope of a MongoDB logical dump.

The screenshot documents the interface and plan boundary at its capture date. The official documentation remains the reference when the interface or plan changes. We should not infer automatic protection from marketing text on an upgrade screen. The operational question is which artifact our current process actually retains and whether we have demonstrated that the intended recovery works.

Sources: Course screenshot, textbook/figures/cloud_interfaces/atlas_free_tier_backup.png, captured August 25, 2026; https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/ , checked September 14, 2026.

## Slide 16

The first lab asks for one individual Brightspace text response. Its first part concerns the resident's confirmation and immediate ticket page. Use the supplied A, B, and C case to connect the requested acknowledgment, eligible read route, read concern, and causal relationship. The explanation should describe what the client does when it cannot confirm the outcome.

The second part uses the lab's own recovery times. Those times are different from the worked example we just calculated. Distinguish the represented recovery point from the interval required to restore service. If part of the incident response is not measured, say what remains unknown rather than inventing a duration that makes the target pass.

Work from the member states and incident times in the lab. Leave your cloud deployment running normally. Explain the proposed behavior as if a colleague were deciding what a confirmation message should mean. Name the reason for each setting and describe the result when the required members cannot respond.

We will also introduce the final through the single final-project page linked in this week's guide. Use your existing project notes to identify an important write and the behavior its user expects. That discussion transfers today's ideas into a project without adding another Week 12 deliverable or replacing the final's canonical instructions with a competing checklist.

Sources: course/weeks/week_12/lab_01_reliability_decisions.md and course/assignments/final_project.md.

## Slide 17

Our second class moves from reasoning about failure to performing a small recovery. The notebook starts with five synthetic tickets and creates an inspectable saved artifact. It restores the documents into a different target so that the source remains available and the recovery process does not overwrite the collection we are trying to understand.

Successful insertion into that target is only the beginning. We will compare the restored information with the saved version and introduce one deliberate error after restoration. The result keeps the correct count, the correct identifiers, and valid date types, but a subject is wrong. That counterexample lets us examine what our checks actually establish.

Your repair selects the saved document for one ticket and replaces the damaged version. The surrounding code is provided so that the work focuses on the source of the recovery value and the operation's result. Repeating the repair should not create another ticket or change an unrelated one.

We will then distinguish those document values from the collection's operational rules. The JSON file does not recreate the unique business key, compound index, or validator automatically. Restoring those definitions and testing their behavior is a separate part of reopening the application. The finished notebook and a short recommendation inside it form the one submission for this class.

Sources: Current Notebook 05 and Week 12 Lab 2. All ticket values and the incorrect-migration scenario are synthetic course examples.

## Slide 18

The default notebook uses an in-memory library called mongomock. It lets us work with the documents, serialize and parse the artifact, repair the target, and test the unique ticket-number index without an Atlas account. It does not implement the server's schema validation feature. The notebook therefore labels those schema outcomes as a supplied trace rather than pretending the local library enforced the rules.

The Atlas path runs the same recovery work against MongoDB and adds actual server schema tests. To use it, the notebook must connect from its own runtime. In Colab, that runtime belongs to Google's environment. Adding the current IP from your laptop's browser can therefore authorize a different computer from the one running Python.

The notebook prints the runtime IPv4 address before the connection cell. Add that single address as a temporary slash-thirty-two entry and wait for the rule to become active. Enter the driver URI only in the hidden prompt. Keep TLS certificate verification enabled rather than treating an insecure switch as a connection fix.

The database user also needs the operations used in the two practice databases, including collection modification for validation. A website login and a successful ping do not grant those permissions. If setup would prevent the lesson, local mode remains available, with its limitation stated accurately in the recommendation.

Sources: Current Notebook 05 connection cells; https://www.mongodb.com/docs/atlas/security/ip-access-list/ ; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/ .

## Slide 19

These are the five records in the recovery notebook. They are a fresh, self-contained fixture. We do not need a surviving collection from last week's class, and we should not assume that a reused ticket number means every field matches a previous teaching example.

Read the statuses first. Ticket 1001 is open. Ticket 1002 is in progress. Ticket 1004 is new. Those are the three active tickets under the course's definition. Tickets 1003 and 1005 are resolved, but they are still part of the saved dataset. Recovering the active-query result must not accidentally mean recovering only active records and silently losing resolved history.

The subjects give us known values that are easy to recognize. The first ticket concerns a dark streetlight near a bus stop. Ticket 1004 concerns a broken bench slat. Either can be used for the supplied incorrect-migration case later. Their distinct content helps us check more than the existence of the ticket number.

The opening times are UTC values in February 2026. The notebook constructs actual datetime values and the driver stores BSON dates. The abbreviated display on this slide is for readability. Later we will inspect a type-preserving representation and compare it with a parser that recognizes only ordinary JSON structure. All five documents should survive the complete recovery exercise.

Sources: Exact current Notebook 05 source fixture. This table abbreviates display dates but does not change their recorded instants.

## Slide 20

Ordinary JSON supports numbers, strings, objects, arrays, booleans, and null. It does not define a native date value or distinguish every numeric storage type that BSON supports. An application can agree on a representation, but the parser must understand that agreement if it is to reconstruct the intended stored types.

This example shows two selected fields from ticket 1001 in Canonical Extended JSON. The numberInt marker identifies the integer ticket number. The date marker contains a numberLong value representing milliseconds since the Unix epoch. For the opening time in our fixture, that value corresponds to February first at twenty-three ten UTC.

The quotation marks around the marker's numeric text do not mean that the intended recovered date is just an arbitrary string. The combination of reserved marker keys and values tells a BSON-aware parser how to interpret it. A parser that knows only JSON can read the syntax while leaving these marker objects as ordinary dictionaries.

Canonical mode emphasizes preservation of BSON type information. That makes the text more explicit and sometimes less compact than a display intended only for people. We use it here because a restore should retain the stored meaning, not merely produce similar-looking text. The next example makes the difference between a successful JSON parse and a typed reconstruction visible in Python.

Sources: Selected fields from Notebook 05; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/extended-json/ ; https://www.mongodb.com/docs/manual/reference/bson-types/ .

## Slide 21

Both parsers receive the same valid JSON text. The text contains an opened-at field whose value uses the Extended JSON date marker. The ordinary json library successfully parses that syntax, so there is no JSON syntax error to warn us that we are using the narrower interpretation.

The first output is dict. The opened-at value is still a Python dictionary holding the marker structure. It is not a datetime value that the driver can use as the same BSON date merely because the keys happen to contain a dollar sign and the word date.

The second parser comes from BSON's json_util module. It understands the marker convention and, with the notebook's options, reconstructs the corresponding datetime. The second output is therefore datetime. The options also keep our UTC-aware date handling consistent across the source, file parse, and restored database values.

This difference is more useful than a general instruction to check types because we can observe the two actual results. A plain parse can be appropriate when a program intends to inspect or transform the marker objects. It is incomplete when our goal is to reconstruct the original stored date without that extra interpretation. In the notebook, we use the BSON-aware result before inserting the recovered documents, then verify the resulting values rather than assuming the parser's name is sufficient evidence.

Sources: Original course parser comparison using the exact ticket 1001 instant; https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html .

## Slide 22

The recovery workflow has three distinct objects. The source collection contains the five stored documents and its collection rules. The artifact contains selected document data encoded as Canonical Extended JSON. The separate target begins with the recovered documents and MongoDB's automatic internal-identifier index, but without the custom rules we will reconstruct later.

The notebook keeps a manifest beside this process. It records the expected collection, count, identifiers, index definitions, validator definition, and file digest. That manifest stays in the notebook. It is not secretly embedded into each ticket document or automatically recovered from the document-only JSON file.

Before resetting the disposable target, the restore checks the artifact's digest and parses the content. If either step fails, it should stop before discarding the existing target state. This ordering is useful even in a classroom because it makes a failed precondition visible instead of converting a bad artifact into another destructive step.

A matching digest identifies the bytes recorded by the manifest. It does not prove a trusted origin, completeness, or a consistent snapshot across changing collections. Our source is a small quiescent fixture, so we can compare every saved document with a known baseline. Production recovery needs a strategy matched to its scale and invariants, as well as access and verification beyond this one-collection demonstration.

Sources: Current Notebook 05 export/manifest/restore cells. Diagram is an authored explanation of that exact scope, not a claim of a production snapshot service.

## Slide 23

The target now contains an intentionally wrong subject. In the displayed case, ticket 1001 should describe a dark streetlight near a bus stop. The incorrect migration replaced that subject with unrelated text. No document was inserted or deleted by this change.

That explains the first true result: there are still five documents. The update also left every ticket number unchanged, so the expected identifiers still match. It did not change opened-at, so the datetime check also remains true. Each check answers a legitimate question, but none of those questions concerns whether this subject matches the saved version.

The complete typed-value comparison becomes false. The notebook serializes the compared values with the same Canonical Extended JSON options and sorted field names. That also avoids treating an integer and an equal-valued double as interchangeable simply because ordinary Python numeric equality permits that comparison.

The subject remains a string, so the schema alone cannot identify its incorrect business meaning. A validator can reject a missing or wrong-typed field while accepting a plausible but inaccurate value. This is why recovering data and restoring rules are complementary activities. For your repair, we know the correct value because we retained the earlier artifact. We are not asking you to guess the resident's intended subject from the damaged database.

Sources: Current Notebook 05 incorrect-migration case and typed-value comparison. Results were tested for both documented student ticket choices.

## Slide 24

The saved lookup uses documents parsed from the verified artifact. It is not a fresh query against the source or the damaged restore target. That matters because the current target is precisely the state we have reason to distrust. Each ticket number selects its saved document in this lookup.

The replacement call has two arguments to read separately. The first selects the existing ticket using the damaged ticket number. The second supplies the complete saved document as the replacement. The saved internal identifier still belongs to that same document, so the operation restores its values without inventing a different identity.

On the first repair of the supplied error, one document matches and one document changes. On a repeated repair, the same document still matches, but its values already agree with the replacement, so the modified count is zero. The total remains five. A zero modified count on that second run is not evidence that the intended ticket vanished.

This is a useful example of interpreting operation results in context. We check which record matched, whether the values now agree, and whether another record appeared. The student change is selecting the correct saved document in the provided code. The important explanation is why that source and replacement are appropriate, and why the earlier count-only confidence was insufficient.

Sources: Current Notebook 05 documented repair; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/ .

## Slide 25

The source and the document-only restore can contain matching ticket documents while behaving differently on the next write. Collection rules are not ordinary fields that travel inside each ticket. We must examine them as a separate part of the recovered system.

MongoDB creates the internal-identifier index for the restored collection. That automatic index checks the internal id. It does not, by itself, prevent two documents with different internal ids from using the same business ticket number. Our unique ticket-id index supplied that separate rule in the source, and it is missing from the initial document-only restore.

The compound index on status and opening date is also missing. Its definition concerns the keys and their order. The small five-ticket exercise does not establish a measured performance improvement from that index, but it does let us inspect whether the expected definition has been recreated.

On the Atlas path, the source validator restricts required fields and permitted types or values. The document file does not reinstall that validator automatically. A name in an inventory is not enough to reconstruct every rule: the required key order, uniqueness flag, schema, and enforcement settings matter. This is why the colleague receiving only the JSON file should ask for the collection definitions and relevant environment information before assuming the application is ready to reopen.

Sources: Current Notebook 05 source and document-only restore; https://www.mongodb.com/docs/manual/core/index-unique/ ; https://www.mongodb.com/docs/manual/core/schema-validation/ .

## Slide 26

These commands recreate the definitions separately from the saved ticket values. The first index uses ticket-id as a unique business key. The name makes it recognizable when we inspect the collection. The uniqueness option, not the friendly name, establishes the constraint.

The second index orders status ascending and opening date descending. This returns a definition used by the workload discussion in the course. Recreating an index is still a write to database metadata and needs the appropriate permission. Its existence should not be confused with a measured improvement for every query.

The final command runs only on the Atlas path. The notebook has already defined ticket-validator as the schema for this five-ticket fixture. collMod installs that validator on the restored collection with strict validation and an error action. The local library cannot execute that server feature, so the code skips it and states the limitation.

Installing a schema does not rewrite an inaccurate subject into the value the resident intended. Nor is issuing a successful metadata command the end of verification. We still need an allowed input and rejected counterexamples to demonstrate the rule's behavior. Keeping reconstruction separate from data restoration lets us explain exactly which part of the procedure supplied the missing behavior and which assumptions remain outside this artifact's scope.

Sources: Current Notebook 05 rule reconstruction; https://www.mongodb.com/docs/manual/reference/command/collMod/ ; https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/ .

## Slide 27

The first test is an allowed write. A validator that rejects everything would not make a usable application, so success on a valid example matters. The temporary ticket uses values that satisfy the notebook's required fields and permitted types. It should be accepted before we interpret any negative case.

The duplicate test uses a new internal identifier but repeats ticket number 1001. The separate unique business-key index must reject it. Error eleven-thousand identifies that duplicate-key failure. It is different from document-validation error one-twenty-one, which the Atlas path expects for the three schema counterexamples.

Those counterexamples change one relevant property at a time: an unsupported status, a date represented as text, and a required date that is absent. A network error or permission denial would not establish that the schema rejected the intended input. The notebook propagates unrelated errors rather than counting every failure as a successful test.

Both paths exercise their unique-index behavior. Only the real server path enforces the schema here. The local schema lines are a supplied trace to interpret, and your recommendation should preserve that distinction. The notebook then removes its temporary records and leaves the five practice tickets. Tests should tell us something about the restored application behavior without quietly leaving extra data behind.

Sources: Current Notebook 05 positive/negative cases; https://www.mongodb.com/docs/manual/core/schema-validation/handle-invalid-documents/ ; https://www.mongodb.com/docs/manual/core/index-unique/ .

## Slide 28

The first row describes the file we actually used. It contains selected collection documents in a BSON-aware textual representation. We reconstructed the collection rules from separate definitions. Receiving that file alone would not give a colleague every rule or hosted project setting required by the application.

MongoDB Database Tools provide a broader logical dump and restore path. Within documented behavior, a dump can include selected namespace data and metadata such as collection options and index definitions. Compatibility, credentials, the destination namespace, and tool errors still matter. The broader scope should not be summarized as recreating an entire Atlas project.

The PostgreSQL archive from Week 8 likewise carries schema and constraints within its selected dump scope. It differs from the document-only JSON file, but it also leaves hosted project settings and external application dependencies to separate procedures. The useful comparison identifies concrete contents and omissions rather than declaring one filename extension universally safer.

Our source did not change during this classroom export. We have not established a live multi-collection snapshot, a point-in-time recovery service, or a production cutover plan. Those require additional mechanisms and tests. The exercise gives us a transparent way to reason about artifact scope and verify a small recovery, which is a foundation for understanding larger backup systems rather than a substitute for their operational requirements.

Sources: https://www.mongodb.com/docs/database-tools/mongodump/ ; https://www.mongodb.com/docs/database-tools/mongorestore/ ; https://www.postgresql.org/docs/current/app-pgdump.html ; course Week 8 archive and Notebook 05.

## Slide 29

Complete the recovery notebook individually. Choose one of the two supplied ticket numbers for the incorrect-migration case, select its saved document in the repair cell, and check the resulting values. Repeat the repair so that you can interpret a matched record whose data no longer needs changing.

Your short recommendation stays in the notebook. Explain why the incorrect subject survived the earlier checks, name a rule that required separate reconstruction, and compare the artifact's scope with the PostgreSQL archive from Week 8. Use the execution path you actually used. Interpreting a supplied schema trace should not become a claim that you tested a server validator.

The cleanup code removes only the practice tickets collections from the two uniquely named databases. It also deletes this run's temporary JSON file and closes the Python client. It does not remove unrelated collections or shut down a shared hosted deployment. That narrow scope is deliberate: classroom cleanup should not become a reason to discard someone else's work.

If you used Atlas, remove the temporary network-access entry separately and clear the printed runtime-IP output before submission. Keep the synthetic data and meaningful query results. Submit the completed notebook in Brightspace. No separate report, exported-file attachment, or additional final-project checkpoint is required for this lab.

Sources: Current course/weeks/week_12/lab_02_mongodb_recovery.md and Notebook 05 cleanup cells. No hosted cluster deletion is part of the assignment.

## Slide 30

An interview explanation should connect a problem, an action, and a result that you can actually explain. The sample account names a small collection and a separate restore target. It identifies a concrete failure in the checking strategy: the right count did not prove the values were correct. It then describes recovering a document from a retained artifact and treating collection rules as a separate concern.

You do not need to inflate this into a claim of running production disaster recovery. You can show the code, explain the expected values, and discuss what the experiment left out. That makes the account useful to a developer, analyst, or database operator who wants to understand how you reason about data correctness.

Adapt the statement to your actual path. If you used local mode, say which operations you executed and which schema behavior you interpreted from the supplied trace. If you used Atlas, distinguish its real validation results from the replica-state scenarios that we analyzed without triggering a failover.

The same habits carry into the next week. Before recommending more capacity or sharding, we need a workload, a meaningful measure, and a clear limitation. Before loading another dataset through Python, we need to know its identifiers, types, and repeat-run behavior. Reliability, recovery, performance, and integration become connected engineering decisions rather than disconnected lists of product features.

Sources: Authored career account based on the current Week 12 work; syllabus Week 13 capacity, sharding, and Python integration handoff. This is a model to adapt, not a claim about unperformed professional experience.

## License

Original course prose is licensed under CC BY 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
