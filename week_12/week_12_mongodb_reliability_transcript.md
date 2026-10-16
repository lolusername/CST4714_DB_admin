# Week 12: MongoDB Reliability and Recovery - Spoken Transcript

## Slide 1

Welcome to Week 12. Read the two lines in the middle of the slide, because they are the puzzle for the whole week. A resident submits a request and sees a confirmation. Then the very next page says the request cannot be found. What happened?

I want you to resist answering right away, because there are at least four honest explanations. The write might never have finished. A database copy might be behind. The write might have worked, but the client lost the reply. Or a later operation might have deleted the ticket. Same symptom, four different mechanisms, four different fixes.

Last week we checked that an aggregation counted the right records and that a document rule rejected the right inputs. That was about one database giving correct answers. This week adds two harder questions. When there are several copies of the database, which state does a read actually see? And when data is destroyed, how do we get the earlier version back?

On Day 1 we follow one request through acknowledgment, reads, and a network partition, and we calculate two separate recovery objectives. On Day 2 we use a small notebook to restore five tickets, catch a wrong value that several reasonable checks miss, and repair it from a saved copy. Both labs are individual. The first is one Brightspace text response. The second is the notebook itself. The goal is understanding the mechanism, not producing a stack of reports.

Sources: Course Chapter 12, current Week 12 individual labs, and Notebook 05. Opening scenario and teaching sequence are authored course examples.

## Slide 2

Here is the setup we will use all week. Three members, A, B, and C. Together they are a replica set: three copies of the same logical database. These are the same names the lab uses.

Start on the left. The client writes ticket 1099. A is the primary, and the primary is the member that accepts writes. A applies the change and records it in its oplog, the operations log. Think of the oplog as a running history of data changes. It is not a table your application queries. It is what the secondaries read so they can catch up.

B and C are secondaries. They fetch entries from that history and apply them to their own copies. Why does that matter? Because they do not do it at the exact same instant as A. Look at C: may temporarily lag. During that gap, C's data is older. That is called replication lag, and it does not mean a write was lost. It means you need to know which member answered your read.

Two more things. The oplog is bounded, so a secondary that falls too far behind can need more than a quick replay of recent entries. And if A fails, an election can pick a new primary, but noticing the failure, holding the election, and reconnecting the client all take time. That is the bottom line of the slide: the oplog carries changes, copies can lag, and failover is not instant.

Sources: https://www.mongodb.com/docs/manual/replication/ ; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ . Native source diagram retained and relabeled for the course A/B/C case.

## Slide 3

Now the same request as a table of moments. Read it row by row. Before submission, nobody has it: absent, absent, absent. Next row, A applies the insert, so A says present, and B and C are still absent.

The third row is the one I care about. B has retained the oplog entry, made it durable, but has not yet applied the insert to its collection. Look at the B column: not yet applied. Retaining a change and applying it are two different steps.

Why does that matter? Read the box under the table. In MongoDB 8.0 and later, with the default majority journaling, A's and B's durable oplog entries in that third row can already satisfy a majority acknowledgment. So the client can be told success while B's collection still looks old. Only in the last row does B apply the insert and actually show the request.

And C? C is isolated. It stays absent in every row. If a later read happens to reach C, the request looks missing, even though A and B kept it. That absence tells you about the state that one read saw. It does not prove the acknowledged write disappeared.

These rows are one possible sequence, not fixed delays. With three voting members that all store data, two is a majority, so A and B can satisfy it without C. That is why we tie the confirmation read to the write instead of hoping any copy is current.

Sources: https://www.mongodb.com/docs/manual/reference/write-concern/#reads-after---w---majority----writes ; https://www.mongodb.com/docs/manual/core/read-preference/ . MongoDB 8.0+ sequence with default majority journaling, checked September 14, 2026.

## Slide 4

Write concern is how the client says how much acknowledgment it wants before it believes a write succeeded. Look at the three settings in the left column, for our three-member case.

w: 1 asks only the primary. That is quick, but read the limitation: the write can lack a second retained copy. If A fails right after saying yes, that confirmed write may not be anywhere else.

w: "majority" asks for two voting, data-bearing members. In our case, A and B can provide those. The cost is that the required members must be reachable. And notice I said our case. Do not reuse the number two blindly for a deployment with different voting members or arbiters. Count the configuration you actually have.

w: 3 asks for all three. That sounds safest, but C is isolated, so this cannot complete now. A stronger-sounding setting just turned into a write that cannot finish.

Now the box at the bottom, which surprises people. A timeout can stop the acknowledgment wait without undoing the write. If the primary already applied the change and the wait runs out, the change can still be there. So a timeout means "I don't know," not "it failed." Journaling and the deployment's configuration are part of durability too.

That is why the choice comes from consequences. A resident's confirmed submission deserves a clear retention promise, and the developer also needs a defined response for when that promise cannot be confirmed in time.

Sources: https://www.mongodb.com/docs/manual/reference/write-concern/ . Table applies to the authored three-voting-data-bearing-member case, not arbitrary topologies.

## Slide 5

Here is what that looks like in code. This is mongosh, the MongoDB shell, not a Python notebook cell.

The first two lines build a database name with a random eight-character suffix, and the third line switches to it. Why the random part? So this demonstration never collides with a project database or with a previous class example. Switching only changes the shell's target. Nothing is stored until the insert.

Now look at the document's two identifiers. The _id is submission-1099, a stable ID for this one submission attempt. The ticket_id is 1099, the business number. That stable _id is the important design decision. If the app is unsure whether the write worked, it has something precise to ask about later. That is very different from generating a fresh ID every time the browser retries the same action.

Next, look where writeConcern sits. It is the second argument to insertOne, outside the document. It changes the acknowledgment we ask for, not the resident's ticket. w majority is the success condition, and wtimeout 5000 is how long, in milliseconds, we wait for that acknowledgment. It is not a promise that the whole operation finishes in exactly five seconds.

Read the last line of the caption. A normal success shows you the command shape and the stored record. It does not demonstrate a failover. And for Lab 1, you do not need to run this or touch a replica set. It is a reasoning lab.

Sources: Course Chapter 12 acknowledgment example; https://www.mongodb.com/docs/manual/reference/method/db.collection.insertOne/ ; https://www.mongodb.com/docs/manual/reference/write-concern/ .

## Slide 6

Suppose the reply never arrives. The client asked for majority and got a timeout or a dropped connection. Now what?

Look at the code: findOne by the stable _id, submission-1099, and return the fields that describe what we meant to save, ticket_id, status, and subject.

If the document is there, check the content too. Finding the ID proves a document with that key exists. It does not prove it is the submission we intended, especially if an ID was ever reused by mistake.

Read the box in the middle. Because a retry reuses the same _id, the database cannot create a second document with that _id. That protects us from accidental duplicates. But read the next box. A duplicate-key error alone does not prove the existing request is yours. It only says the key is taken.

And the last line: a missing read from a lagging copy does not prove the write failed. If this read lands on an older secondary, like C, it can return nothing while A and B have the request. So the app needs a deliberate read-back route, a bounded wait, and retry behavior designed for this operation. What it must not do is shrug and generate a new ID, because that is how one resident ends up with two tickets.

We will see the same split on Day 2: the database enforces a unique key, and the application decides what that key means.

Sources: Original course read-back illustration; https://www.mongodb.com/docs/manual/core/retryable-writes/ ; https://www.mongodb.com/docs/manual/core/index-unique/ .

## Slide 7

Two controls with similar names that do completely different jobs. Look at the first column.

Read preference is routing. It decides which member answers. primary sends this read to the primary. secondaryPreferred prefers an eligible secondary, with a documented fallback. Neither name tells you how fresh the answer has to be.

Read concern is about the data that comes back. local may include data that is not yet majority committed. majority returns majority-committed data. That is a guarantee about the state, not a command that makes every copy current.

Now read the box at the bottom, because this is where people get caught. A lagging member can hold older majority-committed data. Go back to our table. C is behind A and B. An older version that C holds may already be majority committed, and still predate the new submission. So majority read concern alone does not mean you get the latest value anywhere in the system.

Why does this distinction matter? Because the right setting depends on the workflow. An hourly report can read from a secondary, as long as it shows when its data was refreshed. That takes load off the primary, and nobody is harmed by a slightly older count. A resident's confirmation page is different. They just submitted, and they expect to see their ticket. For that page we need to connect the read to their write rather than pick settings from their names alone. That is the next slide.

Sources: https://www.mongodb.com/docs/manual/core/read-preference/ ; https://www.mongodb.com/docs/manual/reference/read-concern/ . The report and confirmation comparison is an authored workload example.

## Slide 8

Here is one concrete answer for the confirmation page. Read the table top to bottom. Write concern: majority. Read preference: primary. Read concern: majority. And the last row is the piece that ties it together: the write and the following read use the same causal session.

What is a causal session? It is not another server. It is a relationship between operations. The session remembers that this read comes after that write. With majority read and write concern, that relationship supports reading your own write. The confirmation read stops being a stranger that knows nothing about what just happened.

Read the first box. The later read carries a dependency on the earlier write. So if a suitable secondary is asked inside a causal session and it has not caught up yet, it may wait to catch up instead of handing back the old state. Better to wait a moment than to tell a resident their ticket does not exist.

Now the limit at the bottom. Timeouts and later changes by other requests remain possible. During a network failure, that wait might not finish before the app's deadline. And causal order does not freeze the ticket. Another authorized request can still change or delete it later. It is not a lock.

For your lab, this is the shape of a good answer: the promise for this confirmation, the settings that support it, and what the client does when it cannot get that promise in time.

Sources: https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-concerns/ ; https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/ .

## Slide 9

Now we break the network. Look at the picture. On the left, A and B, two voting members, and A can remain primary. In the middle, the network partition: messages are lost or delayed between sides. On the right, C alone, one voting member, and it cannot form a voting majority.

First thing to notice. This is not a failed primary. A is healthy, A can still talk to B, and two out of three is a majority. So losing contact with C does not force A to stop being primary. Ask which members can talk to each other and what operation the client wants.

Read the line at the bottom. C cannot acknowledge a new write that it has not received from A and B. C simply has no way to learn about something that never reached it.

The dashed link means messages cannot cross. It does not mean C secretly has its own copy of future writes. And a client that reaches C cannot get information C does not have just by choosing a different read preference.

So the analysis follows the operation. A majority write can complete on the A and B side. A read on C's side has two options: return older information, or wait for a guarantee it cannot get right now. That exact choice is what CAP describes, which is the next slide, and we will use this concrete case instead of treating CAP as three letters on a product label.

Sources: Retained course native partition diagram, relabeled A/B/C; https://www.mongodb.com/docs/manual/core/replica-set-elections/ ; https://www.mongodb.com/docs/manual/core/causal-consistency-read-write-concerns/ .

## Slide 10

Let's make CAP concrete. Read the top box. On the A and B side, a write changes a ticket's status to resolved, and that write completes. Only after that does a new read begin on the C side. Assume nothing changes the ticket back in between. C never got the update, because the partition is blocking the messages.

So what can C do? Look at the table. Option one: return the old status, open. The consequence column says that read can violate the single-current-copy promise. Someone already resolved this ticket, and C is telling you it is open. Option two: wait or reject until coordination is possible. Then that operation is unavailable in the CAP sense. An error is not a successful read.

There is no third row. That is the whole theorem for this case. During a partition, for this operation, you choose between a possibly stale answer and no answer.

Now the definitions at the bottom, because both words are tricky. Consistency in CAP means linearizable behavior, acting like one current copy. It is not the C in ACID, which is about keeping the application's integrity rules. Open and resolved are both valid statuses under any schema, and they still disagree about what is current.

And CAP availability is not an uptime percentage. It is about whether every relevant operation can complete during the modeled communication failure. Real applications make more specific promises than that, but no product label makes the missing messages appear.

Sources: Course Chapter 12 authored partition example; Gilbert and Lynch, 2002, https://people.cs.rutgers.edu/~rmartin/teaching/spring04/cs553/BrewersConjecture-SigAct.pdf .

## Slide 11

Now a different failure. This time A itself is lost. Look at the first row. If B and C can still communicate, they have two votes out of three, and eligible members can elect a new primary. Compare that with the last slide, where A was alive on the majority side and no election was needed at all.

Second row. A is lost, and B and C cannot talk to each other either. Now each one is alone with one vote. Neither has a voting majority, so neither can become primary. Two surviving machines are not enough if they cannot coordinate. Why so strict? If each isolated member could promote itself, you could end up with two primaries accepting conflicting writes. The majority rule prevents that.

Read the first box under the table. Failure detection, election, and driver reconnection take time. The members have to notice A is gone, hold an election, and then the driver has to find the new primary. While there is no writable primary, some operations fail or wait. How long depends on configuration and conditions, so do not promise a fixed number of seconds.

And the second box. Supported driver retries help with particular operations, under documented rules. But a driver retrying one insert and a person pressing Submit again are not the same event. A retry does not make every application action safe to repeat. That is why we keep coming back to stable identifiers like submission-1099.

Sources: https://www.mongodb.com/docs/manual/core/replica-set-elections/ ; https://www.mongodb.com/docs/manual/core/retryable-writes/ . Table assumes eligible voting data-bearing members and the stated connectivity.

## Slide 12

This slide changes the category of failure completely. Nothing is broken. Every member is healthy. Somebody with permission deletes the five tickets.

Look at the first row. Before the deletion, A, B, and C each have 5 tickets, and an earlier export holds 5 saved tickets. Second row: after the deletion replicates, A, B, and C all have 0 tickets. Read the first line of the box. Replication correctly carries out the destructive operation. It did its job perfectly. It copies a delete just as faithfully as an insert. That is the key idea of the week: replication is not backup.

The only place the old tickets still exist is the last column. Still 5 saved tickets. A separate artifact, outside the live collection, made earlier. That is what recovery needs. Replicas protect the service when a machine fails. A retained artifact protects history when the data itself goes wrong.

But do not over-trust a file either. You still need to know which moment it represents, what it contains, whether your tools can read it, where you can restore it, and whether the application works afterward. A data file without its rules or credentials can leave the recovery incomplete.

And the bottom line of the slide: an oplog has a bounded history. It is not an indefinite recovery archive. That is why on Day 2 we keep an explicit small artifact and restore it somewhere else, instead of hoping some replica still has the old version.

Sources: Authored five-ticket deletion example; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ ; https://www.mongodb.com/docs/database-tools/mongodump/ .

## Slide 13

Two recovery numbers this week, and they measure different things. First, recovery point objective, RPO. That is how much work you can afford to lose.

Read the case at the top. A complete artifact represents 16:10. The deletion happens at 16:22. And there is no later export or replayable event log. Now look at the timeline: the saved state at 16:10, the deletion at 16:22. The equation underneath does the math. 16:22 minus 16:10 is a 12-minute recovery-point gap. Anything that happened in those twelve minutes is not in the artifact.

Now the target. The objective allows at most five minutes of lost work. Twelve is more than five, so this artifact does not meet it. And here is the important part: restoring it faster does not help. A lightning-fast restore of a 16:10 file still gives you 16:10 data.

Notice that I said the artifact represents 16:10. That is not the same as saying an export finished at 16:10. A long export over changing data might not reflect one clean instant. In our worked case we are told the point directly, so we can reason without hiding that assumption.

One more discipline. Twelve minutes is a time window. It is not a number of lost tickets. We were not told how many requests arrived in that window, so we do not invent one. And these times belong to this worked example. Lab 1 gives you its own times.

Sources: Original course recovery timeline and Chapter 8/12 recovery-objective definitions. These worked times differ from the assessed Week 12 Lab 1 case.

## Slide 14

The second number is recovery time objective, RTO. Not how much data you lose, but how long the service is down.

First, when does the clock start? Not when someone finally types the restore command. It starts at the incident. While people are noticing the problem, finding the artifact, and getting permission to use it, the service is already broken.

Read the table. Detect the deletion: 2 minutes. Retrieve and authorize the artifact: 1 minute. Restore and pass application checks: 4 minutes. In this example the steps happen one after another, so the equation says 2 plus 1 plus 4 is 7 minutes. Against a ten-minute service-restoration objective, this drill passes.

Now read the second line of the box. It still misses the five-minute data-loss objective from the previous slide. Same incident, one pass and one fail. That is exactly why these are two numbers and not one. You can come back quickly with old data, or recover very recent data and be down too long. Those are different consequences for different people.

Last point. Seven minutes is an observed result from one rehearsal, under these supplied conditions. It is not a guarantee for a bigger dataset, a slower operator, a different network path, or a different failure. In the lab, use the times the lab gives you. And if part of the interval from incident to restored service was never measured, say that it is unknown, instead of making up a number that lets the target pass.

Sources: Original course worked recovery timeline; current Week 12 instructor guide. No production service-level guarantee is implied.

## Slide 15

This is the actual backup page of an Atlas Free cluster, captured August 25. Look at what it offers: continuous or daily backup, as upgrades. Now read the boxes on the right. No native Atlas backup on the Free cluster. These are upgrade choices. No completed backup appears here.

Why show you a screen for something we are not buying? Because it is easy to see the word backup on a page and assume you are protected. Nothing on this page says a backup ever ran. It is an offer.

MongoDB's own Free-cluster documentation, which we checked on September 14, says the same thing. Free clusters exclude native Atlas backups, and the documentation points to MongoDB Database Tools as the logical backup alternative. The Free plan also limits the failure-testing controls. So we can study recovery on the free plan without paying for anything, but we have to do the recovery work ourselves.

That is the middle box: use a separate logical recovery artifact and a tested restore target. That is exactly what the Day 2 notebook does. It makes a small file you can read with your own eyes, keeps it outside the live collection, and restores it somewhere else.

One caution about screenshots in general. This one documents the interface on its capture date. Interfaces and plans change, and the documentation is the reference. The operational question never changes, though: which artifact does our process actually keep, and have we proven that restoring it works?

Sources: Course screenshot, textbook/figures/cloud_interfaces/atlas_free_tier_backup.png, captured August 25, 2026; https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/ , checked September 14, 2026.

## Slide 16

Here is Lab 1. One individual Brightspace text response, in two parts.

Part one is the confirmation page. Using the supplied A, B, and C case, decide how many members acknowledge the write, where the next read goes, which read concern it uses, and how a causal session connects it to the write. Then say what the client does if the write times out and it cannot confirm the outcome. A timeout does not necessarily mean failure, and a stable request ID plus a status check can prevent a duplicate submission.

Part two is the recovery timeline. Use the lab's own times, not the 16:10 and 16:22 example we just worked. Keep the recovery point separate from the time to restore service. If some part of the incident response is not measured, say what is unknown instead of inventing a duration that makes the target pass.

Read the scope box. Work from the supplied member states and incident times. Keep your cloud deployment running normally. No failover, no reconfiguration.

The last box is the final project, which we introduce this week. Open the single final-project page linked in the week guide. That page is the only requirements document. Its Week 12 checkpoint is to choose a platform and scenario and write a one-paragraph workload statement. As you do, pick one important write in your scenario and ask today's question: what should its confirmation promise? That thinking is not a second Week 12 lab submission.

Sources: course/weeks/week_12/lab_01_reliability_decisions.md and course/assignments/final_project.md.

## Slide 17

Welcome back. Day 1 was reasoning about failure. Today we actually perform a small recovery.

Read the line in the middle of the slide. Five restored tickets can have the right IDs and still contain the wrong information. That sentence is the trap, and we are going to walk into it on purpose.

Here is the plan. The notebook starts with five synthetic tickets and saves them to a file you can read. Then it restores them into a different target, not on top of the original. Why a different target? Because if the restore goes wrong, you have not destroyed the thing you were trying to understand.

Then the notebook introduces one deliberate error after the restore. The count is still right, the IDs are still right, and the dates are still real dates, but one subject is wrong. We will look at what each of our checks really proves, and why three of them pass anyway.

Your job is the repair. You pick the saved version of the damaged ticket and replace the bad one. Running that repair a second time should not create another ticket or change any other ticket.

Then come the rules the data file omitted. The JSON file holds documents. It does not bring back the unique business key, the compound index, or the validator. Rebuilding and testing those is a separate step. The finished notebook, with a short recommendation inside it, is your one submission for today.

Sources: Current Notebook 05 and Week 12 Lab 2. All ticket values and the incorrect-migration scenario are synthetic course examples.

## Slide 18

Before you run anything, choose your path. Look at the table.

The local path is USE_ATLAS equals False, the default. It uses an in-memory library called mongomock, so no Atlas account is needed. It runs the data recovery, the repair, and the unique-index test. But read the limit: schema outcomes are a supplied trace. Mongomock does not implement the server's schema validator, so the notebook shows you those outcomes and labels them honestly as a trace, not as enforcement.

The Atlas path is USE_ATLAS equals True. The same work, plus real server schema tests. The cost is setup: network access and permissions are required.

Now the box at the bottom, because this is where most connection problems come from. In Colab, Python runs on Google's computer, not your laptop. If you click Add Current IP in your laptop's browser, you authorize your laptop, which is the wrong machine. So the notebook prints the runtime's IPv4 address. Add that one address as a temporary slash-thirty-two entry, pause until it is active, and then enter your connection URI in the hidden prompt. Never paste the URI into a cell.

Keep TLS verification enabled. If the connection fails, turning off certificate checks is not a fix. Your database user also needs permission for these operations, including collMod for the validator, and a successful ping does not prove you have it. If setup is blocking the lesson, local mode is fine. Just state its limits accurately in your recommendation.

Sources: Current Notebook 05 connection cells; https://www.mongodb.com/docs/atlas/security/ip-access-list/ ; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/ .

## Slide 19

Here is our fixture, the five tickets the notebook creates fresh. You do not need anything left over from last week. And if a ticket number looks familiar, do not assume the other fields match. Read the last line of the box: this fixture is separate from Week 11's four-ticket example.

Read the status column first. 1001 is open. 1002 is in_progress. 1004 is new. Those are the three active IDs under the course's definition. 1003 and 1005 are resolved. Now read the first line of the box: all five documents should survive recovery. Why point that out? Because it is easy to check a recovery with your everyday active-tickets query, get three rows, feel good, and quietly lose the resolved history. Recovery means everything that was saved, not just what today's dashboard shows.

The subjects are deliberately distinct and easy to recognize. 1001 is Streetlight dark near bus stop. 1004 is Broken bench slat. Those are the two tickets you will choose between for the damage case later. Distinct text means we can check more than whether a ticket number exists.

Last column, the opening times, in UTC, all in February 2026. Ticket 1001 opened February 1 at 23:10. The slide abbreviates them for reading, but the notebook builds real datetime values, and the driver stores them as BSON dates. Keep that in mind, because on the next slide we look at how a date survives being written into a text file.

Sources: Exact current Notebook 05 source fixture. This table abbreviates display dates but does not change their recorded instants.

## Slide 20

Here is the problem. Ordinary JSON knows numbers, strings, objects, arrays, true and false, and null. It has no date type. And it does not distinguish every numeric type that BSON, MongoDB's storage format, keeps apart. So if we write tickets to a JSON file, how does a date come back as a date?

The answer is Canonical Extended JSON. Look at the code box. These are selected fields from ticket 1001, not the complete document. ticket_id is not just 1001. It is wrapped in a marker, dollar numberInt, which says this is an integer. And opened_at is wrapped in dollar date, and inside that, dollar numberLong, with the value 1769987400000. Read the caption: that number is milliseconds since the Unix epoch. For our fixture, it is February 1 at 23:10 UTC, the time from the last slide.

Notice the quotation marks around the number. That does not mean the date turned into a string. The marker keys tell a BSON-aware parser how to rebuild the stored type. A parser that only knows JSON reads the same text just fine, but it leaves those markers as ordinary dictionaries.

Why use canonical mode? It is wordier than a display meant for people, but it preserves the type information. A restore has to bring back what was stored, not just something that looks similar. On the next slide you will see the difference for yourself in Python.

Sources: Selected fields from Notebook 05; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/extended-json/ ; https://www.mongodb.com/docs/manual/reference/bson-types/ .

## Slide 21

Same text, two parsers. Watch what comes out.

The string at the top is valid JSON. It holds opened_at with the date marker and the same number, 1769987400000. The first parser is plain json.loads from Python's standard library. The second is json_util.loads from the bson package, with the notebook's JSON_OPTIONS. Then we print the type of opened_at from each one.

Look at the result line. Outputs: dict, then datetime.

Why does that matter? Because the plain parser did not fail. No error, no warning. It parsed the syntax perfectly and handed you a dictionary with a key called dollar date. If you inserted that into MongoDB, you would store a nested object, not a date, and anything that expects a date, like sorting by opening time or a validator, would no longer behave the same. Your restore would run and your count would still match.

The BSON-aware parser understands the marker convention and rebuilds a real datetime. The notebook's options also keep the times UTC-aware, consistent from the source, through the file, into the restored database.

Read the scope line at the bottom. The notebook imports json and json_util and defines JSON_OPTIONS before this, so this is not a standalone script. In the notebook we use the BSON-aware result before inserting, and then we check the restored values. We do not just trust the parser's name. Observe the actual type rather than assume it. That habit is the lesson of this slide.

Sources: Original course parser comparison using the exact ticket 1001 instant; https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html .

## Slide 22

Three boxes, and keeping them separate is the point.

On the left, the source collection: 5 tickets, plus its indexes and validator. In the middle, the document artifact: 5 saved documents in Canonical Extended JSON. On the right, a separate target: 5 recovered tickets, with initially only the _id_ index. Look at that last line. The file brought back documents, not rules. MongoDB creates the _id_ index automatically. Everything else we rebuild later.

Read the box at the bottom. The notebook keeps the metadata manifest separately: the expected collection, the count, the IDs, the index and validator definitions, and the file's hash. That manifest lives in the notebook, not in the JSON file.

Now the order of operations. Before the notebook resets its target, it checks the artifact's hash and parses the data. Why first? Because resetting the target is destructive. If the file is damaged, you want to find out before you throw away what was there. A failed check should stop the restore, not turn a bad file into a second loss.

Read the last line. An unchanged hash identifies bytes, not completeness or authenticity. A matching hash says this is the same file the manifest recorded. It does not say the file came from a trusted source or captured everything. Our source is a small fixture that nobody is changing, so we can compare every document. Production recovery needs much more than this one-collection exercise.

Sources: Current Notebook 05 export/manifest/restore cells. Diagram is an authored explanation of that exact scope, not a claim of a production snapshot service.

## Slide 23

Here is the trap. After the restore, the notebook simulates an incorrect migration. Look at the box on the right. Saved 1001: Streetlight dark near bus stop. Restored 1001: Text replaced by an incorrect migration. One subject is wrong. Nothing was inserted, nothing was deleted.

Now the table. Five documents: True. Of course, nothing was added or removed. Expected ticket IDs: True. The migration did not touch ticket numbers. All opening values are datetime: True. It did not touch the dates either. Three passing checks, and every one of them asks a legitimate question. None of them asks whether this subject matches the saved version.

The last row asks that. All saved document values and types match: False. That check serializes every value with the same Canonical Extended JSON options and sorted field names, then compares the results. That also catches subtle problems, like an integer quietly becoming an equal-valued double, which plain Python equality would treat as the same.

Now the bottom line of the slide. The wrong subject is still a string, so the schema alone cannot detect this error. A validator can reject a missing field or a wrong type. It cannot know that a resident wrote about a streetlight. Valid and correct are different words.

And notice how we know the right answer. Not by guessing what the resident meant. We kept the earlier artifact. That is the only reason this damage is repairable at all.

Sources: Current Notebook 05 incorrect-migration case and typed-value comparison. Results were tested for both documented student ticket choices.

## Slide 24

Here is the repair.

The first block builds saved_by_id, a lookup from ticket number to document. Look where it comes from: restored_documents, the documents parsed from the verified file. Not a fresh query against the damaged target. Why? Because the target is exactly the state we no longer trust. The recovery value has to come from the saved artifact.

The next line picks recovery_document, the saved version of DAMAGED_TICKET, which is 1001 or 1004, whichever you chose.

Then replace_one, with two arguments. The first is the filter: find the ticket whose ticket_id is the damaged one. The second is the replacement: the whole saved document. The saved _id is the same _id the existing document already has, so we restore its values without inventing a new identity.

The print on the slide shows two counts. Read the result line. First repair: 1 matched, 1 modified. Repeat: 1 matched, 0 modified. Five tickets remain. Zero modified on the second run is good news. It means the document already matches the saved version, so there was nothing to change. It does not mean the ticket vanished.

One practical note for the lab. In your notebook, the repair cell does not print those two counts. It checks that exactly one document matched, then prints whether all document values were recovered and the ticket count. So after your repair you should see all values recovered, True, and a count of five, and rerunning the cell should still show five.

Sources: Current Notebook 05 documented repair; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/ .

## Slide 25

Here is the second half of recovery, the half people forget. The restored collection can hold exactly the right documents and still behave differently on the next write.

Read the table. Automatic _id_ index: present in the source, and created automatically in the restore. That one is MongoDB's own. But the next three rows say missing. The unique ticket_id index, missing. The status and date compound index, missing. The server schema validator on the Atlas path, missing.

Why does that matter? Take the unique index. The _id_ index only stops two documents with the same _id. It does nothing to stop two documents with different _ids from both claiming ticket 1001. In the source, the unique ticket_id index enforced that business rule. In the restore, nothing does. The data looks perfect, and the next bad insert goes straight in.

The compound index is missing too. With five tickets, we cannot claim it makes anything measurably faster, but we can check whether its definition came back. And the validator, which rejected bad statuses and wrong types in the source, is simply not installed.

Read the box at the bottom. The notebook supplies the definitions separately from the document JSON. And an index name alone would not be enough. You need its keys, their order, and whether it is unique. So if a colleague hands you only the JSON file, the right reaction is to ask for the collection definitions and the relevant environment details before anyone reopens the application.

Sources: Current Notebook 05 source and document-only restore; https://www.mongodb.com/docs/manual/core/index-unique/ ; https://www.mongodb.com/docs/manual/core/schema-validation/ .

## Slide 26

So we rebuild the rules from their definitions. Three commands.

The first create_index is on ticket_id with unique equals True, named unique_ticket_id. The name just helps us recognize it when we inspect the collection. The unique option is what actually creates the constraint. A friendly name enforces nothing.

The second is a compound index: status ascending, then opened_at descending, named status_by_date. That is the definition the course's workload discussion uses. Creating an index is a write to the database's metadata, so it needs permission, and its existence is not evidence that every query got faster.

The third command only runs if USE_ATLAS is true. It is collMod on the tickets collection, installing ticket_validator, the schema the notebook defined earlier, with validationLevel strict and validationAction error. Strict means it checks every insert and update. Error means a violating write is rejected, not just logged. Read the context line: local mode skips collMod, because mongomock cannot run that server feature, and the notebook says so.

Now the last line on the slide. Installing a rule does not prove the restored subject is correct. The validator would happily accept a wrong subject, because it is still a string. And a command that succeeds is not a test either. To show a rule works, we need an input it accepts and inputs it rejects. That is the next slide. Keeping rules separate from data lets us say exactly which step brought back which behavior.

Sources: Current Notebook 05 rule reconstruction; https://www.mongodb.com/docs/manual/reference/command/collMod/ ; https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/ .

## Slide 27

A rule you have not tested is a hope. Here are five tests, and the first one is the one people skip.

Valid new ticket 1099: accept. Why test a success? Because a validator that rejects everything also passes every rejection test. If a good ticket cannot get in, the application is broken.

Second row: a second document with ticket_id 1001. It has a new _id, so the _id_ index will not stop it. Only the unique ticket_id index can. Expected result: reject, duplicate key, 11000.

The last three rows are schema tests. 1100 has status almost_done, which is not an allowed status. 1101 stores the date as text. 1102 is missing opened_at. Each one changes exactly one thing, so a rejection tells you which rule caught it. Expected result for all three: reject, validation, 121. Notice that 11000 and 121 are different codes from different rules.

And the code matters. If one of these failed with a network error or a permission error, that would not prove the schema rejected the input. The notebook lets unrelated errors stop the run instead of counting every failure as a pass.

Read the scope box. Both paths test the unique index. Only Atlas executes the schema tests. On the local path, those three lines are a supplied trace, not server enforcement, and your recommendation should say that. Last line: the notebook removes its temporary test documents and keeps the five tickets. A good test does not leave clutter behind.

Sources: Current Notebook 05 positive/negative cases; https://www.mongodb.com/docs/manual/core/schema-validation/handle-invalid-documents/ ; https://www.mongodb.com/docs/manual/core/index-unique/ .

## Slide 28

Let's compare our file with two other recovery artifacts. Look at the column headings: documents or rows, rules in its scope, and hosted project settings.

First row, the file we used today. This Extended JSON file holds the selected collection. Rules: rebuilt separately. Hosted project settings: no. If a colleague hands you only this file, you get data, not a working application.

Second row, a MongoDB logical dump, the kind mongodump makes. It covers selected namespaces, and it includes metadata and indexes. That is a broader scope. But look at the last column: not the whole project. It does not recreate your Atlas project. And compatibility, credentials, and the destination still matter when you restore it.

Third row, the PostgreSQL archive from Week 8. It carried schema and constraints for the database content you dumped. Also not the whole project. So the honest comparison is not that one file type is safe and another is not. It is what each artifact contains and what it leaves out.

Now the box at the bottom. Our classroom data stays unchanged during export, so one file captures one clean state. A busy application is different. It needs a way to capture related data consistently while writes keep arriving, and a plan for switching the application to its restored database. We have not built those here. What we built is a small, transparent, verified recovery. That is a foundation for understanding larger backup systems, not a substitute for them.

Sources: https://www.mongodb.com/docs/database-tools/mongodump/ ; https://www.mongodb.com/docs/database-tools/mongorestore/ ; https://www.postgresql.org/docs/current/app-pgdump.html ; course Week 8 archive and Notebook 05.

## Slide 29

Here is Lab 2. Open Notebook 05 in Colab and save a working copy in your Drive.

Choose ticket 1001 or 1004 for the damage case. In the Your Repair cell, select its saved document, run the repair, and confirm that all five documents match the artifact again. Then run the repair once more and confirm it does not create a sixth ticket.

Then write a short recommendation inside the notebook. The question is: if a colleague handed you only this JSON file, what could you recover, and what else would you ask for before reopening the application? Explain why the wrong subject survived the earlier checks, name one rule that had to be rebuilt separately, and give one difference from the PostgreSQL archive you used in Week 8. Use the path you actually ran. If you used local mode, interpreting the schema trace is not the same as testing a server validator, so do not claim that you did.

Now look at the cleanup code. It drops the tickets collection in the source database, drops it in the restore database, deletes the temporary JSON file, and closes the client. It does not touch anything else or shut down a cluster. Cleanup should never become a reason to delete someone else's work.

Read the bottom box. If you used Atlas, remove your temporary IP rule yourself and clear the printed runtime IP before you submit. Submit the completed notebook in Brightspace, with no separate report or data-file attachment.

Sources: Current course/weeks/week_12/lab_02_mongodb_recovery.md and Notebook 05 cleanup cells. No hosted cluster deletion is part of the assignment.

## Slide 30

Last slide. How would you describe this work in a job interview?

Read the paragraph on the slide. It has three parts. A problem: I restored a small collection into a separate target and found that the right count did not prove the values were correct. An action: I recovered the damaged document from the saved artifact, checked its typed values, and tested the collection rules separately. And a judgment: I can explain which failure this method addresses and which parts of a hosted deployment it leaves out.

That last sentence is what makes the account strong. Plenty of people say they have done disaster recovery. Far fewer can say exactly what their recovery proved and what it did not. You can show the code, explain the expected values, and name the limits.

Read the boundary box. Use the account that matches your own work and execution path. If you ran local mode, say which operations you executed and that the schema behavior came from a supplied trace. If you used Atlas, you can describe real validator results, but the replica-set scenarios from Day 1 were reasoning, not a failover you triggered. Do not inflate it.

Next week we carry these habits into capacity, sharding, and safe Python data integration. Before adding capacity, we need a workload and a measure. Before loading data through Python, we need its identifiers, its types, and what happens on a rerun.

Sources: Authored career account based on the current Week 12 work; syllabus Week 13 capacity, sharding, and Python integration handoff. This is a model to adapt, not a claim about unperformed professional experience.

## Slide 31

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Replica sets: oplog, lag, and elections (1:24); Write concern, read preference, and read concern (1:39); Replication is not backup: logical recovery (1:31). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 12 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
