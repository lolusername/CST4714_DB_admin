# Database Administration Interview and Portfolio Guide

## Purpose
This guide helps you talk about what you learned in CST4714 in job interviews, internship interviews, portfolio reviews, and project presentations.

The goal is not to pretend you are already a senior database administrator.
The goal is to explain beginner-level database administration skills clearly, honestly, and with evidence.

## Short Course Pitch
Use this when someone asks what the class was about:

> In my database administration course, I practiced the operational side of databases, not just writing queries. I worked with PostgreSQL/Supabase and MongoDB Atlas, designed schemas and document models, practiced indexes and query performance, reviewed backup and recovery concepts, learned access-control basics, and built a final cloud database project with administrative evidence.

## What You Can Say You Practiced

### Database Administration
Say:

> I learned that database administration includes planning, building, securing, monitoring, tuning, troubleshooting, and recovering databases.

Evidence you can mention:
- schema design
- user and access decisions
- backup and restore thinking
- index decisions
- query review
- cloud database setup
- final project evidence

### PostgreSQL and Supabase
Say:

> I used Supabase as a managed PostgreSQL platform. I practiced table design, SQL queries, indexes, access-control thinking, and administrative evidence such as connection settings, backup awareness, and project configuration.

Evidence you can mention:
- relational schema
- primary keys and foreign keys
- SQL joins
- indexes
- row-level security concepts
- backup/restore discussion
- connection string troubleshooting

### MongoDB and Atlas
Say:

> I used MongoDB Atlas to learn document databases, JSON-style data, document modeling, aggregation, and cloud database connection workflows.

Evidence you can mention:
- embedding vs referencing
- flexible schemas
- MQL basics
- aggregation pipelines
- Atlas connection strings
- network access/IP allowlisting
- read/write concern concepts

### Data Modeling
Say:

> I learned that data modeling depends on how the application reads and writes data. In relational databases, I focused on tables and relationships. In MongoDB, I focused on document shape and access patterns.

Evidence you can mention:
- SQL tables from application requirements
- JSON documents from CSV-style data
- embedded order items
- referenced records when one source of truth matters
- final project model choices

### Performance
Say:

> I learned that performance tuning should be evidence-based. An index should match a real query pattern, and the tradeoff is that indexes speed up reads but add storage and write-maintenance cost.

Evidence you can mention:
- `CREATE INDEX`
- query filters
- sorting
- `EXPLAIN` or query plan thinking
- MongoDB sort/index labs
- final project query examples

### Reliability
Say:

> I learned that reliability is not just having a backup. A team needs to know what data is official, how recovery would be verified, and what happens when distributed systems disagree.

Evidence you can mention:
- backup/restore verification
- source of truth
- idempotent retries
- write concern
- read concern
- read preference
- incident response labs

### Security
Say:

> I learned basic database security principles such as least privilege, protecting connection strings, using platform access controls, and thinking carefully about who can read or change data.

Evidence you can mention:
- not sharing credentials
- GitHub secret hygiene
- Atlas Network Access
- Supabase row-level security concepts
- database user permissions

## Interview Answer Pattern
Use this structure:

1. Concept: name the concept.
2. Example: describe where you used it in class.
3. Evidence: name the file, lab, query, notebook, or project artifact.
4. Tradeoff: explain one limitation or decision.

Example:

> One concept I practiced was indexing. In my final project, I identified a query that filtered records by status and sorted by creation date. I added or proposed an index that matched that access pattern. The tradeoff is that indexes can improve reads, but they also add storage and can slow down writes, so I would not add indexes randomly.

## STAR Examples

### Performance Example
Situation:
> I had a database query that needed to filter and sort records.

Task:
> I needed to explain how a database administrator would improve the query responsibly.

Action:
> I identified the columns used in the filter and sort, then connected that query to an index strategy.

Result:
> I could explain why the index was justified and what tradeoff it introduced.

### Security Example
Situation:
> A cloud database project needs to protect data and credentials.

Task:
> I needed to show basic access-control thinking.

Action:
> I reviewed connection strings, network access, user permissions, and row-level security concepts.

Result:
> I could explain that database security includes both platform settings and schema-level access rules.

### Reliability Example
Situation:
> A distributed application had official data in one system and event data in another.

Task:
> I needed to decide what the application should trust after systems disagreed.

Action:
> I identified the source of truth, explained why derived data can be stale, and proposed a safe retry or repair pattern.

Result:
> I could explain why operational reliability depends on ownership, verification, and recovery paths.

## Resume Bullet Examples
Use these as models. Rewrite them honestly based on what you actually did.

- Designed a small cloud database project using PostgreSQL/Supabase or MongoDB Atlas with schema/modeling decisions, seed data, and query examples.
- Practiced database administration workflows including access-control review, backup/recovery planning, index decisions, and operational evidence collection.
- Built beginner-level SQL and MongoDB examples demonstrating data modeling, query patterns, and performance tradeoffs.
- Used GitHub to document database concepts, project artifacts, and technical explanations for portfolio review.
- Analyzed relational and document database tradeoffs, including normalization, embedding, referencing, and source-of-truth decisions.

## Better Phrases Than “I Know Databases”
Instead of:

> I know databases.

Say:

> I can design a small relational schema, explain primary and foreign keys, write basic SQL queries, and discuss why indexes and backups matter.

Instead of:

> I used MongoDB.

Say:

> I practiced MongoDB document modeling, including when to embed related data and when to reference separate documents based on access patterns.

Instead of:

> I did a final project.

Say:

> I built a small cloud database project and documented the schema or model, seed data, queries, access choices, and reliability considerations.

Instead of:

> I learned security.

Say:

> I learned beginner database security practices, including least privilege, protecting secrets, and thinking about who should be allowed to read or modify data.

## Questions You Can Ask An Interviewer
These questions show database awareness:

- What database systems does your team use most often?
- How do you handle schema changes or migrations?
- How do you test backup and restore procedures?
- How do you decide when a query needs an index?
- How do you manage database access for developers and applications?
- Does the team use one database system, or does it use multiple systems for different workloads?

## If You Do Not Know An Answer
Use an honest technical answer:

> I have not done that in production yet, but I understand the beginner version. I would start by identifying the source of truth, checking the database documentation, testing in a safe environment, and verifying the result with evidence before changing production.

That is a stronger answer than guessing.

## Portfolio Checklist
Before you share your GitHub or final project, check:
- the README explains what the project or concept is
- there is at least one concrete example
- no passwords, keys, connection strings, or private URLs are exposed
- screenshots do not reveal secrets
- the writing explains why the database choices matter
- tradeoffs are included
- the final project due date is clear: May 26, 2026

## Final Interview Pitch Template
Fill this in for your own work:

> In CST4714, I built a database administration foundation using _____. My final project focused on _____. The main database concept I can explain well is _____. One tradeoff I learned is _____. If I continued this project, the next operational improvement I would make is _____.
