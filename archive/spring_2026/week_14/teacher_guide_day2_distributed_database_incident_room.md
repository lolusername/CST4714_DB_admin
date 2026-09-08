# Week 14 Day 2 Teacher Guide
## Distributed Database Incident Room

## Quick Summary
Today is an advanced-topics class that should still feel beginner-friendly.

The class uses a fictional incident to teach why distributed databases need clear source-of-truth decisions, consistency choices, safe retries, and recovery checks.

The student-facing activity is not a final-project work session only.
It introduces a new distributed database administration topic, then connects that topic back to final project thinking.

## Materials For Today
- `Week_14_Day2_Distributed_Database_Incident_Game.pptx`
- `lab_day2_distributed_database_incident_room.md`
- `week14_mongodb_atlas_incident_demo.ipynb`
- MongoDB University: [Practice: Read and Write Concerns with MongoDB Deployments](https://learn.mongodb.com/learn/course/replication-in-mongodb/lesson-5-read-and-write-concerns-with-mongodb-deployments/last-lesson)
- MongoDB University course context: [Replication in MongoDB](https://learn.mongodb.com/courses/replication-in-mongodb)

## What Students Should Leave Understanding
Students do not need to become distributed systems experts today.

They should leave able to say:
- A source of truth is the place the application treats as official.
- Derived data can be useful but should not silently become official unless the design says so.
- Event logs, caches, analytics stores, and search indexes can lag behind the source of truth.
- A retry can fix a failed operation, but a retry can also duplicate work unless it is designed safely.
- An idempotency key helps make repeated attempts safe.
- MongoDB read concern, write concern, and read preference are reliability knobs.
- Stronger consistency can improve correctness, but it can cost latency or availability.
- Faster reads can improve user experience, but they may be stale or incomplete.

## Syllabus Alignment
This fits Week 14 because it covers:
- advanced database administration topics
- polyglot persistence
- cloud database behavior
- distributed reliability tradeoffs
- operational thinking instead of only query syntax
- final project readiness through source-of-truth and recovery thinking

## Core Story
The fictional app is `Campus Food Rush`.

The app lets students preorder food during a busy lunch rush.

The app uses:
- Postgres for users, orders, and payments
- MongoDB for cart events, activity logs, and menu snapshots
- a cache for fast menu availability
- a kitchen screen that shows orders to prepare

The incident:
Some students were charged, but their orders disappeared from the kitchen screen.

The key clue:
The kitchen screen read from MongoDB events, but the official order/payment state was in Postgres.

The teaching point:
The bug is not simply “MongoDB failed” or “Postgres is better.”
The bug is that the system did not clearly protect the path from official order creation to derived kitchen visibility.

## Class Flow
Use this if you want the class to run smoothly without adding extra files.

1. Start with the incident story.
2. Ask students what data system they would trust first.
3. Teach the vocabulary from the slide deck: source of truth, derived data, cache, event, consistency, idempotency.
4. Have students open the MongoDB University read/write concerns practice.
5. Connect the MongoDB University lab back to the incident.
6. Walk through the deck’s repair patterns.
7. Optionally run the Colab notebook as a live demo.
8. Give students the lab as an individual Brightspace text response.
9. End with an exit ticket about one tradeoff.

## If You Are Short On Prep Time
Say this at the beginning:

“Today is about what happens when an application uses more than one data system. This is common in real software. One database might store official orders, another system might store logs or events, and a cache might store fast temporary information. The problem is that these systems can disagree. Our job today is to decide what the application should trust, how to detect disagreement, and how to repair a failure safely.”

Then use the student lab exactly as written.

## Key Concepts To Explain

### Polyglot Persistence
Polyglot persistence means an application uses more than one kind of database or storage system because different parts of the application have different needs.

Example:
- Postgres is good for structured records, constraints, transactions, and relational integrity.
- MongoDB is good for flexible documents, event-like records, nested data, and fast developer iteration.
- A cache is good for fast reads of temporary data.

Important warning:
Using multiple systems is not automatically better.
Every extra system adds synchronization, ownership, monitoring, and recovery problems.

Plain-language explanation:
“Polyglot persistence is like using different tools in a kitchen. A knife, oven, and refrigerator all make sense, but you need to know which one is responsible for which job. If every tool is treated as the official source, the kitchen becomes chaotic.”

### Source Of Truth
A source of truth is the system the application treats as official when there is disagreement.

For the incident:
- If a student paid and an order row exists, the kitchen should not ignore that just because an event is missing.
- The event log can help notify the kitchen, but the official order state should be checked when correctness matters.

Common student mistake:
Students may say “the payment provider is the source of truth.”

Better answer:
The payment provider is the source of truth for charge status, but not necessarily for the full order. The application still needs an official order record that ties the payment to a student, item, status, and fulfillment workflow.

### Derived Data
Derived data is data copied, transformed, or generated from another source.

Examples:
- a kitchen event created after checkout
- an analytics dashboard row
- a search index document
- a cached menu availability value
- a notification record

Derived data can be extremely useful.
The danger is treating derived data as official when it can be delayed or missing.

### Consistency
Consistency means different reads and systems agree in the way the application expects.

Beginner framing:
“If I paid for the burrito, every important part of the app should eventually agree that I paid for the burrito. The question is how quickly they must agree and which screen is allowed to be temporarily behind.”

For today:
- A kitchen screen needs high correctness.
- An analytics report can tolerate delay.
- A menu cache can be fast but might be slightly stale.

### Write Concern
Write concern is a MongoDB setting that controls how much acknowledgment MongoDB requires before a write is reported as successful.

Simple version:
“How sure do we want MongoDB to be before saying the write worked?”

Example:
- `w: 1` means one MongoDB node acknowledged the write.
- `w: "majority"` means a majority of voting replica set members acknowledged the write.

Tradeoff:
Majority acknowledgement improves durability confidence, but it may be slower or less available during failures.

### Read Concern
Read concern controls the consistency and isolation level of data returned by a read.

Simple version:
“How trustworthy or settled does the data need to be when we read it?”

For today:
Students do not need every read concern level.
They need the idea that stronger read guarantees can matter when the read controls a real action, like preparing a paid order.

### Read Preference
Read preference controls which replica set member the client may read from.

Simple version:
“Should this app read from the primary, or is it allowed to read from a secondary copy?”

Tradeoff:
Reading from a secondary can reduce load or improve locality, but it can also return stale data if replication is behind.

### Idempotency
Idempotency means repeating the same operation does not create a different final result.

Simple version:
“If the checkout request is retried three times, the student should not be charged three times and the kitchen should not receive three duplicate orders.”

Concrete pattern:
Give each checkout attempt or logical order event an idempotency key, such as `checkout_success:ord_1003`.

If a retry happens:
- the system checks whether that key already exists
- if it exists, the system does not create a duplicate
- if it does not exist, the system creates the missing event

### Restore Verification
A backup is not enough.
A restore must be tested.

For today:
Students only need the idea that after an incident, the team should verify that the official data can be restored or reconstructed.

Plain-language version:
“A backup is a promise. A restore test proves whether the promise works.”

## MongoDB University Lab Integration
Use the MongoDB University practice early in class.

The specific activity is:
[Practice: Read and Write Concerns with MongoDB Deployments](https://learn.mongodb.com/learn/course/replication-in-mongodb/lesson-5-read-and-write-concerns-with-mongodb-deployments/last-lesson)

It belongs to:
[Replication in MongoDB](https://learn.mongodb.com/courses/replication-in-mongodb)

Why this lab fits:
- It introduces the exact MongoDB vocabulary behind distributed reliability.
- It gives students a small official activity before the scenario.
- It makes the incident lab less like opinion writing and more like applied technical reasoning.

What students should focus on:
- write concern is about write acknowledgement
- read concern is about read consistency and isolation
- read preference is about which replica member serves reads
- the right choice depends on what the application is doing

What students do not need:
- they do not need to memorize every option
- they do not need to deploy their own replica set today
- they do not need to tune production settings
- they do not need to write MQL for the Brightspace submission

## Colab Notebook Demo
Use `week14_mongodb_atlas_incident_demo.ipynb` if you want a live coding element.

The notebook demonstrates:
- how to get the Colab public IP
- where to add that IP in Atlas Network Access
- how to load a `MONGODB_URI` secret
- how to connect using `MongoClient` and `certifi`
- how to insert official order records with majority write concern
- how to insert an incomplete event log
- how to find missing derived events with `$lookup`
- how to repair the missing event using an idempotency key
- why safe retries matter
- how read preference and read concern connect to stale data

Use this teacher explanation while running it:

“This notebook is not trying to build the whole food app. It is isolating one reliability problem. We have official orders, and we have checkout events. If those two disagree, the application needs to know which one to trust. The missing event is not just a missing row. It is an operational failure that can affect a real person.”

## Slide-By-Slide Teaching Plan

### Slide 1: Distributed Database Incident Room
Tell students they are acting as database incident responders.
The point is not to memorize terminology.
The point is to make a defensible decision when data systems disagree.

### Slide 2: Why This Matches The Syllabus
Connect the lesson to advanced topics and polyglot persistence.
Students have already seen SQL, MongoDB, modeling, indexing, and cloud admin.
Today combines those ideas into an operational scenario.

### Slide 3: The App: Campus Food Rush
Make the app concrete.
Students understand food ordering.
Use this slide to emphasize that real apps often use multiple systems.

### Slide 4: Vocabulary You Need
Do not rush vocabulary.
These words are the entire lesson:
- source of truth
- derived data
- cache
- event
- consistency
- idempotency

### Slide 5: Clue Board: What We Know
Have students identify which clue sounds official and which clue sounds derived.
Correct direction:
Postgres orders and payment provider status are closer to official truth.
MongoDB events and cache are useful but can be incomplete or stale.

### Slide 6: Tradeoff: Fast Reads vs Correct Reads
Use the kitchen screen example.
Fast is not enough if the screen misses paid orders.
Correctness matters more when the data controls action.

### Slide 7: Failure Pattern: The Ghost Order
Define the ghost order:
The student paid, but the kitchen did not see the order.

Emphasize that this is a systems design failure, not merely a UI bug.

### Slide 8: Repair Pattern: Make The Write Recoverable
Explain that a reliable design has a way to recover when a step fails.
Safe retries and idempotency keys are beginner-friendly reliability patterns.

### Slide 9: CAP Without The Math
Keep CAP simple.
When systems are distributed, there are moments when the app must choose between always answering quickly and answering with the most correct current state.

Do not over-theorize this.
Tie it back to the kitchen screen.

### Slide 10: Choose Your Fix
Students should see that multiple fixes can be valid.
The important part is matching the fix to the failure.

Strong fixes:
- kitchen reads official orders
- missing events are retried safely
- checkout has idempotency keys
- monitoring detects paid orders with no kitchen event

Weak fixes:
- refresh the page
- blame the user
- just use one database without explaining the tradeoff
- manually check orders forever

### Slide 11: Pattern Cards For Real Systems
Translate the incident into reusable patterns.
These are the patterns students can mention in final projects.

### Slide 12: Mini Lab: Incident Commander Report
Give students the lab.
Make clear that this is individual work and one Brightspace text response.

### Slide 13: If You Finish Early
Students can connect the idea to their final project.
They do not need to invent a complicated distributed architecture.
Even one database project has source-of-truth and recovery questions.

### Slide 14: Exit Ticket
End with a tradeoff sentence.
If students can write a tradeoff sentence, they understood the class.

## Strong Student Answers

### Strong Root Cause Example
“The disappearing orders probably happened because checkout created official order/payment state, but the event that the kitchen screen depended on was missing or delayed. The official truth should be the order/payment record, while the MongoDB checkout event stream was incomplete. The cache may also have been stale because it only described menu availability, not whether an order should be prepared.”

### Strong Source Of Truth Example
“The kitchen screen should trust official orders, not only MongoDB events, because a paid order needs to be prepared even if an event write fails. MongoDB events can still be used for notifications or activity history, but they should not be the only place the kitchen checks for paid work.”

### Strong Repair Pattern Example
“I would add an idempotency key to checkout and retry failed event writes safely. If the same checkout is submitted twice, the application can recognize that it is the same logical order and avoid duplicate charges or duplicate kitchen tickets.”

### Strong Tradeoff Example
“This design improves correctness, but it may make the kitchen screen slightly slower because it has to check the official order state instead of trusting only a fast event feed.”

### Strong MongoDB University Connection Example
“The MongoDB University lab connects to this incident because read and write concerns are about deciding how much consistency and acknowledgement the application needs before trusting data.”

## Likely Student Questions

### Is MongoDB Bad For This?
No.
MongoDB is not the problem by itself.
The problem is unclear ownership and missing recovery logic.
MongoDB can be a good fit for events, flexible documents, and application logs.
But if the kitchen screen depends on events, the system needs to detect and repair missing events.

### Should Everything Just Be In Postgres?
Maybe, for a beginner project.
One database is often easier to administer and reason about.
But real systems sometimes use more than one data store for performance, flexibility, analytics, search, or scale.
The correct answer depends on the application and the failure risks.

### What Is The Difference Between Read Concern And Read Preference?
Read preference decides where reads are routed.
Read concern decides what consistency guarantee the read asks for.

Plain version:
Read preference asks, “which server can I read from?”
Read concern asks, “how reliable or settled should the data I read be?”

### Why Do We Need Idempotency If We Already Have A Database?
Because networks fail and users retry.
A database can store the data, but the application still needs a safe rule for repeated operations.
Without idempotency, a retry can accidentally create duplicate payments, duplicate events, or duplicate orders.

### How Does This Connect To The Final Project?
Every final project should have an answer to:
- What is the source of truth?
- What data would be dangerous if it became stale?
- What query or screen needs an index?
- What would the student check after a restore?
- If using more than one service, which service owns which data?

## What To Grade For
The Brightspace response should show reasoning, not memorization.

Full-credit responses should:
- identify an official source of truth
- identify incomplete or stale derived data
- choose a repair pattern that matches the failure
- explain a tradeoff in plain language
- connect the MongoDB University activity to consistency, acknowledgement, or read routing

Partial responses may:
- say “MongoDB broke” without explaining derived data
- choose the cache as source of truth for paid orders
- suggest retrying without explaining duplicate prevention
- mention consistency without tying it to a concrete screen or query

## Instructor Closing Script
“The main lesson today is that databases do not exist in isolation. Real applications often have official data, copied data, cached data, event data, and reporting data. A database administrator needs to know which data is official, which data can be stale, and how the system recovers when a write or event fails. That is why source of truth, write concern, read concern, read preference, and idempotency are not abstract vocabulary. They are how we keep real systems from losing important work.”
