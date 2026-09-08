# Week 14 Lab Day 2
## Distributed Database Incident Room

## Purpose
Today is a fun advanced-topic lab about distributed database tradeoffs.

You are the incident commander for a fictional campus food preorder app.
The app uses more than one data system, and something went wrong during a lunch rush.

The goal is to practice Week 14 concepts:
- polyglot persistence
- source of truth
- consistency
- MongoDB read concern, write concern, and read preference
- idempotent retries
- fast reads vs correct reads
- restore and verification thinking

## Individual Work Only
This lab is individual.
There is no group submission.

## Scenario
The app is called `Campus Food Rush`.

Architecture:
- Postgres stores users, orders, and payments.
- MongoDB stores cart events, activity logs, and menu snapshots.
- A cache stores fast menu availability.
- The kitchen screen shows orders that need to be prepared.

Incident:
Some students were charged, but their orders disappeared from the kitchen screen.

Clues:
- The menu cache said burritos were available.
- Postgres created an order row with status `pending`.
- The payment provider marked the charge as successful.
- MongoDB missed some `checkout_success` events.
- The kitchen screen read from MongoDB events, not from Postgres orders.
- Some students refreshed the page and submitted checkout again.

## What To Do

### 1. MongoDB University Skill Builder
Open this MongoDB University practice:

[Practice: Read and Write Concerns with MongoDB Deployments](https://learn.mongodb.com/learn/course/replication-in-mongodb/lesson-5-read-and-write-concerns-with-mongodb-deployments/last-lesson)

This practice is part of the official MongoDB University course:

[Replication in MongoDB](https://learn.mongodb.com/courses/replication-in-mongodb)

As you work, focus on these three ideas:
- `write concern`: how much acknowledgment MongoDB should require before a write counts as successful
- `read concern`: how consistent or durable the data read should be
- `read preference`: which replica set member a client may read from

You do not need to memorize every option.
For today, the important question is:

`When speed, availability, and correctness conflict, what should the application trust?`

In your submission, include one sentence that connects the MongoDB University lab to the `Campus Food Rush` incident.

### 2. Root Cause
Write 2-3 sentences.

Answer:
- What probably caused the disappearing orders?
- Which system had the official truth?
- Which system had incomplete or stale information?

### 3. Source Of Truth Decision
Choose what the kitchen screen should trust.

Pick one:
- Postgres orders
- MongoDB events
- cache/menu availability
- payment provider status

Explain why.

### 4. Repair Pattern
Choose one repair pattern.

Pick one:
- make Postgres orders the source of truth for the kitchen screen
- retry failed event writes safely
- add an idempotency key to checkout
- monitor event lag and failed checkout events
- create a restore verification checklist

Explain how your repair would reduce the risk next time.

### 5. Tradeoff
Write one tradeoff sentence.

Use this format:

`This design improves _____, but it may make _____ harder.`

Examples:
- `This design improves correctness, but it may make the kitchen screen slightly slower.`
- `This design improves retry safety, but it requires storing and checking request IDs.`
- `This design improves analytics, but it should not become the source of truth for orders.`

### 6. Optional Final Project Connection
Write one sentence connecting today to your own final project.

Example:
`In my final project, the source of truth for ticket status should be the tickets table, not a screenshot or exported CSV.`

## Submit
Submit one Brightspace text response.

Include:
1. one sentence connecting the MongoDB University lab to the incident
2. root cause
3. source of truth decision
4. repair pattern
5. tradeoff sentence
6. optional final project connection

## Success Standard
You are successful if you can explain why distributed systems need clear ownership, safe retries, and restore checks.
