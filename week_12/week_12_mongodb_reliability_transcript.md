# Week 12: Connect to Atlas and Recover a Ticket - Spoken Transcript

This transcript follows the current presentation order. Source references marked as not spoken are included for review.

## Slide 1

Start with a simple situation. A repair request says Broken bench slat. Someone changes a restored copy to the wrong subject. The database still has five requests, so a count tells us nothing is missing, even though one request is wrong. Today we will see that mistake, recover the earlier document, and check what we actually recovered. We have one class this week. First I will explain the pieces, then demonstrate the connection and recovery steps. Your individual lab is one code change plus a short explanation in the same notebook. You submit one viewable Colab link.

## Slide 2

MongoDB is the database software. Atlas is the service hosting it. Colab is a different computer, provided through your browser, that runs our Python code. PyMongo is the Python driver: it sends the requests from that runtime to MongoDB. A database groups collections. Our database is cst4714_week12, and a collection is a group of documents. One document represents one request. The Atlas website is where we configure access and inspect data; it is not where this Python cell executes. A saved Colab notebook stores your code and outputs, while the database lives in Atlas and the exported file initially lives only in the temporary runtime.

## Slide 3

Here is the replica-set model for today. Three members, A, B, and C. Together they are a replica set: three copies of the same logical database. These labels describe a conceptual replica set; we do not control Atlas member elections in this exercise.

Start on the left. The client writes ticket 1099. A is the primary, and the primary is the member that accepts writes. A applies the change and records it in its oplog, the operations log. Think of the oplog as a running history of data changes. It is not a table your application queries. It is what the secondaries read so they can catch up.

B and C are secondaries. They fetch entries from that history and apply them to their own copies. Why does that matter? Because they do not do it at the exact same instant as A. Look at C: may temporarily lag. During that gap, C's data is older. That is called replication lag, and it does not mean a write was lost. It means you need to know which member answered your read.

Two more things. The oplog is bounded, so a secondary that falls too far behind can need more than a quick replay of recent entries. And if A fails, an election can pick a new primary, but noticing the failure, holding the election, and reconnecting the client all take time. That is the bottom line of the slide: the oplog carries changes, copies can lag, and failover is not instant.

Sources: https://www.mongodb.com/docs/manual/replication/ ; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ . Native source diagram retained and relabeled for the course A/B/C case.

## Slide 4

Write concern is how the client says how much acknowledgment it wants before it believes a write succeeded. Look at the three settings in the left column, for our three-member case.

w: 1 asks only the primary. That is quick, but read the limitation: the write can lack a second retained copy. If A fails right after saying yes, that confirmed write may not be anywhere else.

w: "majority" asks for two voting, data-bearing members. In our case, A and B can provide those. The cost is that the required members must be reachable. And notice I said our case. Do not reuse the number two blindly for a deployment with different voting members or arbiters. Count the configuration you actually have.

w: 3 asks for all three. That sounds safest, but C is isolated, so this cannot complete now. A stronger-sounding setting just turned into a write that cannot finish.

Now the box at the bottom, which surprises people. A timeout can stop the acknowledgment wait without undoing the write. If the primary already applied the change and the wait runs out, the change can still be there. So a timeout means "I don't know," not "it failed." Journaling and the deployment's configuration are part of durability too.

That is why the choice comes from consequences. A resident's confirmed submission deserves a clear retention promise, and the developer also needs a defined response for when that promise cannot be confirmed in time.

Sources: https://www.mongodb.com/docs/manual/reference/write-concern/ . Table applies to the authored three-voting-data-bearing-member case, not arbitrary topologies.

## Slide 5

This slide changes the category of failure completely. Nothing is broken. Every member is healthy. Somebody with permission deletes the five tickets.

Look at the first row. Before the deletion, A, B, and C each have 5 tickets, and an earlier export holds 5 saved tickets. Second row: after the deletion replicates, A, B, and C all have 0 tickets. Read the first line of the box. Replication correctly carries out the destructive operation. It did its job perfectly. It copies a delete just as faithfully as an insert. That is the key idea of the week: replication is not backup.

The only place the old tickets still exist is the last column. Still 5 saved tickets. A separate artifact, outside the live collection, made earlier. That is what recovery needs. Replicas protect the service when a machine fails. A retained artifact protects history when the data itself goes wrong.

But do not over-trust a file either. You still need to know which moment it represents, what it contains, whether your tools can read it, where you can restore it, and whether the application works afterward. A data file without its rules or credentials can leave the recovery incomplete.

And the bottom line of the slide: an oplog has a bounded history. It is not an indefinite recovery archive. That is why today we keep an explicit small artifact and restore it somewhere else, instead of hoping some replica still has the old version.

Sources: Authored five-ticket deletion example; https://www.mongodb.com/docs/manual/core/replica-set-oplog/ ; https://www.mongodb.com/docs/database-tools/mongodump/ .

## Slide 6

Two recovery numbers this week, and they measure different things. First, recovery point objective, RPO. That is how much work you can afford to lose.

Read the case at the top. A complete artifact represents 16:10. The deletion happens at 16:22. And there is no later export or replayable event log. Now look at the timeline: the saved state at 16:10, the deletion at 16:22. The equation underneath does the math. 16:22 minus 16:10 is a 12-minute recovery-point gap. Anything that happened in those twelve minutes is not in the artifact.

Now the target. The objective allows at most five minutes of lost work. Twelve is more than five, so this artifact does not meet it. And here is the important part: restoring it faster does not help. A lightning-fast restore of a 16:10 file still gives you 16:10 data.

Notice that I said the artifact represents 16:10. That is not the same as saying an export finished at 16:10. A long export over changing data might not reflect one clean instant. In our worked case we are told the point directly, so we can reason without hiding that assumption.

One more discipline. Twelve minutes is a time window. It is not a number of lost tickets. We were not told how many requests arrived in that window, so we do not invent one. And these times belong to this worked example. These are supplied teaching times, not measured Atlas recovery times.

Sources: Original course recovery timeline and Chapter 8/12 recovery-objective definitions. These worked times are not an assessed second lab.

## Slide 7

The second number is recovery time objective, RTO. Not how much data you lose, but how long the service is down.

First, when does the clock start? Not when someone finally types the restore command. It starts at the incident. While people are noticing the problem, finding the artifact, and getting permission to use it, the service is already broken.

Read the table. Detect the deletion: 2 minutes. Retrieve and authorize the artifact: 1 minute. Restore and pass application checks: 4 minutes. In this example the steps happen one after another, so the equation says 2 plus 1 plus 4 is 7 minutes. Against a ten-minute service-restoration objective, this drill passes.

Now read the second line of the box. It still misses the five-minute data-loss objective from the previous slide. Same incident, one pass and one fail. That is exactly why these are two numbers and not one. You can come back quickly with old data, or recover very recent data and be down too long. Those are different consequences for different people.

Last point. Seven minutes is an observed result from one rehearsal, under these supplied conditions. It is not a guarantee for a bigger dataset, a slower operator, a different network path, or a different failure. Our Atlas exercise does not measure a full incident-to-service interval. And if part of the interval from incident to restored service was never measured, say that it is unknown, instead of making up a number that lets the target pass.

Sources: Original course worked recovery timeline; current Week 12 instructor guide. No production service-level guarantee is implied.

## Slide 8

Keep track of three places. On the left is our source collection in Atlas. In the middle is the saved Extended JSON file. On the right is a different Atlas collection used as the restore target. All three initially describe five tickets. We intentionally change ticket 1004 only on the right. Its count stays five. The old subject survives in the middle, so that is the value we use to repair the target. We do not damage the source, delete a database, or ask Atlas to fail over. Cell 05b downloads the synthetic file because a file left only in a temporary Colab runtime is not a retained recovery copy.

## Slide 9

There are two different identities. Your Atlas website login lets you manage the project. A database user is what the driver uses to access documents. The database user needs readWrite on this teaching database. Next comes the network rule. Colab code runs on a remote computer, so adding the laptop's address can allow the wrong machine. Run Cell 02, add its one IPv4 address with slash 32, and use a temporary expiry. Do not choose access from everywhere. Keep the full connection string in Colab Secrets or the hidden prompt, never in a cell. A client variable can exist before a network request succeeds; ping actually asks the server to respond.

## Slide 10

Open the complete data reference above Cell 04. It lists every application field and all five records. Ticket ID is our course identifier; MongoDB adds its own unique ID. Every opening time here is a real UTC date, not a date-shaped string. Run supplied Cell 04a, then visible Cell 04. The collection names include a new random suffix, so the run has its own source and target. The output must show five acknowledged records and ticket 1004 with Broken bench slat. Open Atlas Browse Collections or Data Explorer, select cst4714_week12 and the printed source collection, and find the same ticket there. That is concrete write/read evidence beyond ping.

## Slide 11

Here is the problem. Ordinary JSON knows numbers, strings, objects, arrays, true and false, and null. It has no date type. And it does not distinguish every numeric type that BSON, MongoDB's storage format, keeps apart. So if we write tickets to a JSON file, how does a date come back as a date?

The answer is Canonical Extended JSON. Look at the code box. These are selected fields from ticket 1001, not the complete document. ticket_id is not just 1001. It is wrapped in a marker, dollar numberInt, which says this is an integer. And opened_at is wrapped in dollar date, and inside that, dollar numberLong, with the value 1769987400000. Read the caption: that number is milliseconds since the Unix epoch. For our fixture, it is February 1 at 23:10 UTC, the time in the complete notebook reference.

Notice the quotation marks around the number. That does not mean the date turned into a string. The marker keys tell a BSON-aware parser how to rebuild the stored type. A parser that only knows JSON reads the same text just fine, but it leaves those markers as ordinary dictionaries.

Why use canonical mode? It is wordier than a display meant for people, but it preserves the type information. A restore has to bring back what was stored, not just something that looks similar. On the next slide you will see the difference for yourself in Python.

Sources: Selected fields from Notebook 05; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/extended-json/ ; https://www.mongodb.com/docs/manual/reference/bson-types/ .

## Slide 12

Same text, two parsers. Watch what comes out.

The string at the top is valid JSON. It holds opened_at with the date marker and the same number, 1769987400000. The first parser is plain json.loads from Python's standard library. The second is json_util.loads from the bson package, with the notebook's JSON_OPTIONS. Then we print the type of opened_at from each one.

Look at the result line. Outputs: dict, then datetime.

Why does that matter? Because the plain parser did not fail. No error, no warning. It parsed the syntax perfectly and handed you a dictionary with a key called dollar date. If you inserted that into MongoDB, you would store a nested object, not a date, and anything that expects a date, like sorting by opening time or a validator, would no longer behave the same. Your restore would run and your count would still match.

The BSON-aware parser understands the marker convention and rebuilds a real datetime. The notebook's options also keep the times UTC-aware, consistent from the source, through the file, into the restored database.

Read the scope line at the bottom. The notebook imports json and json_util and defines JSON_OPTIONS before this, so this is not a standalone script. In the notebook we use the BSON-aware result before inserting, and then we check the restored values. We do not just trust the parser's name. Observe the actual type rather than assume it. That habit is the lesson of this slide.

Sources: Original course parser comparison using the exact ticket 1001 instant; https://pymongo.readthedocs.io/en/stable/api/bson/json_util.html .

## Slide 13

The file has two jobs. It retains the earlier values, and it carries enough type information to rebuild the dates. Ordinary JSON has no built-in date type. Extended JSON uses markers that a BSON-aware parser understands. Cell 05 shows the difference directly: the ordinary reader produces a dictionary for the marked date, and the BSON-aware reader produces a datetime. Now run Cell 05b to download the synthetic artifact. Saving your notebook to Drive does not retain the files created inside its runtime. This small export assumes the source is unchanged while we read it. It does not establish a consistent backup of a busy production deployment.

## Slide 14

Run Cell 06 after saving the artifact. It inserts the saved documents into the separate restore collection, then updates only ticket 1004's subject there. The failure at the bottom is deliberate. Count passes because there are still five documents. IDs pass because we changed no identifier. Types pass because the dates are still datetimes. Complete values fail because the subject no longer equals the saved record. Read the target filter before running it. We use this known, isolated defect so we can say exactly why the check failed. The source and the retained artifact still contain the correct subject.

## Slide 15

Your change is deliberately small so you can spend the time explaining what it does. In Cell 07 replace None with a lookup for ticket 1004 in saved_by_id. That dictionary was built from the saved artifact. Do not type the remembered subject directly: the exercise is to recover saved data. The supplied replace_one uses a filter for ticket 1004 in the restore collection and does not use upsert. The first repair changes the wrong subject. Run Cell 08 to repeat the same replacement. Now one document still matches, zero documents need modification, and the total remains five. All four checks must pass. Refresh the target collection in Atlas to inspect the repaired value.

## Slide 16

GitLab's own postmortem describes an accidental deletion during a PostgreSQL incident and difficulties with the available recovery mechanisms. This was not MongoDB, and our five-ticket lab is not a reproduction of that incident. The transferable responsibility is to rehearse recovery and inspect what the recovery actually gives you. In an interview, describe the checks you ran: same count, same IDs, dates reconstructed as dates, and the complete saved values. Then state the limit. We did not test a production service, a real outage, or a full deployment rebuild. A precise account of a small test is stronger evidence than calling it disaster recovery without those boundaries.

Source: https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/

## Slide 17

A successful run proves that your current client could connect, write, read, and recover these five documents using a saved artifact. It does not prove that a replica election will finish in a certain time. Atlas manages the Free cluster's replicas and does not let this class force a primary failover. The artifact holds documents, not users, collection rules, all indexes, or your application configuration. Atlas currently documents an optional billed Free backup subscription in private preview; we do not enable it. The older screenshot in the reading is dated. Use the corrections link for that product detail. Validator reconstruction is optional reference, not required work this week.

## Slide 18

Keep everything together in your own Drive copy. Your explanation should name what you observed, why a count missed the problem, how the saved artifact supplied the earlier value, and a limit such as a missing collection rule. If your Atlas setup was blocked and you observed my real demonstration, label that honestly; do not claim your connection succeeded. There is no second reliability response this week. Do not attach an ipynb file or submit the starter URL. Check sharing and save the outputs before closing. Cell 10 closes the client and does not delete the Atlas data. Your existing final-project package stays the sole project requirements document.

## Slide 19

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Replica sets: oplog, lag, and elections (1:24); Write concern, read preference, and read concern (1:39); Replication is not backup: logical recovery (1:31). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 12 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
