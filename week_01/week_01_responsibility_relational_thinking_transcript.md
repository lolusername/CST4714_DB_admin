# Week 1: How Applications Use Databases - Spoken Transcript

## Slide 1

Welcome to Week 1. Let me start with a small mystery, because it carries the whole week. A student reports a broken bench through a website. The website gives them a confirmation number. Then the repair desk opens its dashboard, and the request is not there.

So which is it? Did the system lose the request, or did the dashboard leave it out? Those sound similar, but they need completely different repairs. If the data is gone, we have a storage problem. If the data is there and the screen does not show it, we have a problem with the question the screen is asking. The line on the slide gives away where we are headed: the stored rows explain it.

Look at the three boxes: client, API, database. A database holds the organized facts an application needs to keep. A database management system, a DBMS, is the software that reads and changes those facts. The API, the application programming interface, is the agreed way for the browser to ask the application to do something. The browser almost never talks to the database directly.

Today we follow one request through those boxes. Next meeting we look at the rows and the rule behind the dashboard. You will see a little SQL, but the lab does not require you to remember SQL or create a cloud account. You will read a small dataset and explain a result.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?
- https://www.postgresql.org/docs/current/tutorial-arch.html

## Slide 2

Here is the case we will use all week. It is a fictional repair desk, and it is small on purpose, so you can hold all of it in your head.

Look at the first card, stored facts. Each ticket has an ID, a subject, a status, and an assignee, and one row represents one request. The ID matters most. It lets us talk about the same request even when its subject or status changes.

The middle card is the dashboard's promise: every active request should appear. Notice we had to say what active means. Here it means status new or open. A resolved request is not active. That definition is a business rule. The database cannot guess what a repair desk means by the word active. Somebody has to write it into the software, and somebody can write it wrong.

The third card is the complaint. The student has confirmation 1004 for a broken bench, and staff cannot find it. That number lets us line up three things: what the student was told, what is stored, and what the dashboard shows. By itself it does not tell us which part failed.

Now read the sentence at the bottom, because it is the key idea of the week. A stored record and a query result can contain different rows. A table can hold resolved work, active work, and unassigned work. A report picks some of those rows. Every condition we add changes which facts make it in.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?

## Slide 3

Let's follow the student's request from left to right across the top of the slide. Step one, the browser collects the description and sends an HTTP request. HTTP is how the browser talks to a web service. Look at the box on the left: POST slash api slash tickets. POST usually means "create something," the path says where, and the little object underneath carries the subject, Broken bench slat.

Step two, the API endpoint receives it. Step three is identity and rules, and this is where two words need to stay separate. Authentication asks who you are. Authorization asks what you are allowed to do. You can be correctly signed in and still not be allowed to do something, and those checks can happen in more than one place, including the database itself.

Step four, the application asks the DBMS to store a row. Look at the SQL on the right. INSERT INTO tickets names the table. The list in parentheses names the columns. VALUES gives the values in the same order: 1004, the subject, status new, and NULL for the assignee, because nobody has taken the job yet. This is an illustration of our four-column table. We are not running it, and real applications usually let the database generate the ID.

Why does commit matter? After the database commits, closing the browser should not erase the ticket. And showing a list later is a separate read, which can apply different conditions. Keep that in mind.

[Sources]
- https://www.postgresql.org/docs/current/tutorial-arch.html
- https://www.postgresql.org/docs/current/sql-insert.html
- Course-authored Week 1 four-column illustration

## Slide 4

Three words that people use as if they were the same thing. We are going to keep them apart, because it makes both design and troubleshooting much easier.

Look at the left column. The database is the organized data and its structure: tables, rows and constraints, or collections and documents, plus indexes and metadata. In our repair desk, that is the tickets, the agent records, and the rules about valid relationships.

The middle column is the DBMS, the software. PostgreSQL, MongoDB, and SQLite are all examples, and they differ a lot in data model and features. The DBMS accepts operations, runs queries, enforces the rules you configured, and manages changes. Here is the catch. A DBMS will correctly run a query that answers the wrong question. Asking the right question is still our job.

The right column is the managed platform: Supabase, MongoDB Atlas, Amazon RDS. A platform operates the DBMS for you and adds services around it. Its web dashboard is an interface to the system. It is not the data.

Why bother with the distinctions? Because a broken query is a different problem from a server that is down, and a missing permission is different from a dropped browser session. Naming the layer tells you where to look. It also keeps your knowledge portable. A primary key or a transaction means the same thing when a vendor moves a button next year.

[Sources]
- https://www.postgresql.org/docs/current/tutorial-arch.html
- https://supabase.com/docs/guides/database/overview
- https://www.mongodb.com/docs/atlas/

## Slide 5

This is a real Supabase project screen, captured for the course in August 2026, with the account details redacted. Notice what it shows: the project overview, the health of the service, resource use. It does not show a single ticket. Screens like this change, so do not memorize where the buttons are. Learn what each tool is for.

Look at the two boxes at the bottom. The first one is what the platform adds: the dashboard, managed infrastructure, API services, authentication, logs, and configuration. The second is what PostgreSQL still does: tables, SQL, constraints, transactions, query planning, indexes, and roles. Supabase gives each project a real PostgreSQL database. All the relational work happens there.

Supabase has a table editor and a SQL editor. The table editor lets you look at rows visually. The SQL editor sends SQL to the database. They are two windows onto the same data.

Authentication is one of the platform services. It can tell the application who is signed in. It does not decide what that person may read. That still takes authorization rules, which we build later with tests that should succeed and tests that should be refused.

Here is why this matters for our mystery. A green "healthy" status tells you the service is running. It cannot tell you the dashboard includes every active ticket. Only the query and its result can. You do not need a project or a paid plan this week.

[Sources]
- https://supabase.com/docs/guides/database/overview
- Course screenshot: August 2026, account identifiers redacted

## Slide 6

Here is the second platform, MongoDB Atlas. Same pattern, different database software. Underneath this one is MongoDB, not PostgreSQL.

Look at the two boxes at the bottom. The Atlas layer is the project, the cluster, network access, database users, and logs. A project organizes your deployments and access settings. A cluster is a database deployment an application can connect to. Be careful with that word, because cluster means different things in different products, so we will use each product's own definition when we get there.

The MongoDB layer is databases, collections, documents, queries, and indexes. A database contains collections. A collection holds documents. A document is a record made of named fields, and a field can hold a nested document or a list. MongoDB stores documents in a format called BSON, a binary relative of JSON that also understands types like dates. You do not need any of that syntax today.

Here is something that surprises people. You can sign in to the Atlas website perfectly well while your application still cannot connect to the cluster. The website login and the database login are different credentials, and database users, connection details, and network rules all sit in between.

So both screenshots show the same pattern: database software running somewhere, and a management interface for people. Either system can store a support request. Neither one can decide which requests our dashboard ought to show. The note on the slide is true: no cloud account is needed for this week's lab.

[Sources]
- https://www.mongodb.com/docs/atlas/
- https://www.mongodb.com/docs/manual/core/databases-and-collections/
- Course screenshot: August 2026, account identifiers redacted

## Slide 7

So what does a database administrator actually do? Look at the center of the slide: shared data. The job is to keep that data correct, available, secure, and recoverable. 

Correctness means the stored facts follow the intended rules. A ticket keeps its identity when its status changes. An assigned agent refers to a real staff record. Later we use constraints to reject bad values and transactions to coordinate related changes.

Availability means people can reach the service when they need it. A stopped server or a broken connection can stop a perfectly correct query. So can an operation that is just too slow to be usable. We will learn to tell those failures apart from a query that means the wrong thing.

Security means each person or program gets the access appropriate to its job. A student who submits a repair request should not be able to delete every ticket. That idea is called least privilege, and we will test it both ways: what is allowed, and what must be refused.

Recovery means getting useful records back after a mistake or a failure. Making a backup file is one step. Restoring it somewhere separate and checking the important rows is how you find out whether it actually works.

Every one of those later exercises uses the habit we start today: predict the outcome, look at the actual rows, explain the difference. We begin with four rows because the mechanism is easier to see before scale hides it.

[Sources]
- Operating Cloud Databases, Chapters 1 and 3 through 8
- https://www.postgresql.org/docs/current/ddl-constraints.html

## Slide 8

Back to the mystery. Look at the top box, the observed symptom: the form reports success, but ticket 1004 is absent from the staff dashboard.

Look at the response at the bottom: HTTP 201 Created, ticket_id 1004, status new. In HTTP, 201 means the request succeeded and created something. But it is one observation, and we still have to connect it to the stored row and to the later read.

So we check the path in four steps, the four numbered boxes. One, client: did the browser send the request we think it sent? Two, API: what status and body came back? Three, database: did the command actually commit? A commit is not the same thing as a success message on a screen. Four, the read path: is the query that builds the dashboard filtering the ticket out?

The write path and the read path are separate, and each can fail on its own. The lab gives you the stored rows, so you can check step four. If ticket 1004 is in the table and missing from the result, the rows do not support "it was deleted." A filter can drop a row, and so can a join that finds no match.

In real systems there are other suspects, like reading the wrong database or an old cached result. But do not invent causes the evidence does not point to. Name the observation, connect it to a mechanism, and propose a fix for that mechanism.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201

## Slide 9

Welcome to Day 2. Last time we followed a request through the system. Today we look at the shape of the data itself, and we need some precise language for that. That language is the relational model.

E. F. Codd introduced the relational model in 1970. His big idea was to describe data separately from how it is physically stored. That separation is why you can write a query that says what result you want and let the database decide how to fetch it.

A relation is a set of tuples with named attributes. You already know it as a table: one tuple per row, one attribute per column. Before we write any query, we always say what one row means. For the tickets table, one row means one support request. Look at the line on the right: a row represents one fact, and queries produce new results.

Now look at the two lines of relational algebra. The Greek letter sigma is selection. It keeps the rows that satisfy a condition, here status equals open. The letter pi is projection. It keeps the columns you choose, here ticket ID and subject. Later today we combine them with a join.

One honest caveat. SQL borrows these ideas but bends some of the rules. SQL results can contain duplicates, and SQL uses NULL for missing or unknown values. A classical relation has no duplicate tuples. Next week you get lots of practice writing these in SQL.

[Sources]
- E. F. Codd, A Relational Model of Data for Large Shared Data Banks, 1970, https://doi.org/10.1145/362384.362685
- https://www.postgresql.org/docs/current/tutorial-concepts.html

## Slide 10

Here are three tickets from the lab. The subjects are shortened so they fit. The lab has a fourth ticket, 1009, that is not on this slide.

Look across the header: ticket_id, subject, status, assignee_id. Four attributes. Now read down the rows. Each one is a tuple, one complete row of values. Ticket 1001 is open and assigned to agent 201. Ticket 1003 is resolved and also assigned to agent 201. Ticket 1004 is new, and its assignee is NULL.

In this application, that NULL means nobody has been assigned yet. It is not the number zero, and it is not the word NULL typed into a box. And notice that the row is still there. A missing assignee is not a missing ticket. That distinction is going to solve our mystery.

Now the three labels on the right. The schema is the structure: attribute names, types, and rules. The key is stable identity. We make ticket_id the primary key, which means it must be unique and can never be NULL. Why not use the subject? Because two people can report a broken bench, and two requests can share a subject.

Last point. The order of the rows on the slide means nothing. A table has no built-in first row. If order matters, SQL makes you ask for it with ORDER BY, which we add next week. So follow IDs, not positions. That is how you track one request through filters, joins, and changes.

[Sources]
- Course-authored Week 1 ticket excerpt
- https://www.postgresql.org/docs/current/tutorial-concepts.html
- https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS

## Slide 11

The schema is the rule. The instance is the rows that exist right now under that rule.

On the left, tickets has a ticket_id that is an integer, a subject that is text, a status that is text, and an assignee_id that is an integer. That is shorthand notation, not a full SQL command. A real CREATE TABLE would also declare keys, nullability, and other constraints.

Now the instance. At 10:00 there are 3 tickets. At 10:05 there are 4. A row was inserted, and the schema did not change. The instance changes every time rows are inserted, updated, or deleted. Renaming a column, by contrast, changes the schema and can break application code.

Look at the right box, status values: new, open, resolved, closed. Those are the four values in this week's small case. A domain is the set of values an attribute is allowed to have. The type says text, but text is far too broad. A constraint can reject a misspelling like "opne," but it cannot decide what the vocabulary should be. When you meet the full Metro Support data next week, you will see a fifth status, in_progress, which is exactly why the meaning of active has to be written down.

Nullability is a separate decision. A ticket ID must be present. An assignee can be missing until someone takes the job. If we required it, we could not record a valid unassigned request, and that request still belongs on the dashboard.

[Sources]
- https://www.postgresql.org/docs/current/ddl-constraints.html
- Course-authored Week 1 lab and Metro Support status vocabulary

## Slide 12

Look at the agents table: two staff rows, agent IDs 201 and 202. The names are deliberately plain labels, Agent 201 and Agent 202, so you can keep your eyes on the IDs. In this table agent_id is the primary key. The assignee_id column in tickets refers to that key, and the arrow on the slide, PK from FK, points from the reference in tickets to the agent it identifies.

Ticket 1001 stores just the number 201. It does not copy the agent's whole record into the ticket. Why? Because if the agent's details change, we want to change them in one place, not in every ticket. Ticket 1003 points at the same agent. That is a many-to-one relationship: many tickets can refer to one agent. It does not work the other way. Agent 202 exists even though no ticket on this slide points to them.

A declared foreign key constraint checks every non-NULL reference. If someone tries to assign a ticket to agent 999, the database can refuse. And because this foreign key allows NULL, ticket 1004 can say "no agent yet." NULL does not invent an agent, and it does not match one either.

A foreign key constrains a relationship. A join is a query that combines the rows. SQL will happily join tables with no declared foreign key, but then nothing has checked that the matches you assume are really there. Next we see how matching decisions change a report.

[Sources]
- https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
- Course-authored Week 1 agent and ticket data

## Slide 13

First relational operation: selection. The Greek letter sigma. Selection keeps the rows that satisfy a condition, and here the condition is status equals open.

Let's apply it ourselves, row by row. Ticket 1001, status open. It passes. Ticket 1003, resolved. It fails. Ticket 1004, new. It also fails, because new is not the same word as open. So only the highlighted row, 1001, survives.

Now look at the SQL box. FROM tickets names the input. WHERE status equals open is the condition. SELECT star asks for every column of the rows that pass. Notice what did not happen. No status was changed, and no ticket was deleted. Tickets 1003 and 1004 are still sitting in the table. They just are not in this result.

Here is the trap, and it is the same trap as our mystery. Our dashboard promises every active ticket, and active means new or open. If someone wrote this query for that dashboard, every new request would vanish from the screen. The query is perfectly valid SQL, and it runs without a single error. It is just the wrong rule. Valid syntax does not mean a correct business rule.

Keep two questions apart. Which rows qualify? That is the WHERE clause. Which columns come back? That is the list after SELECT. And yes, this is confusing: the SQL keyword SELECT is not relational selection. Relational selection is the row filter, and in SQL that lives in WHERE.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-WHERE
- Course-authored Week 1 ticket excerpt

## Slide 14

Second operation: projection, the Greek letter pi. Selection chose rows. Projection chooses columns.

Look at the highlighted columns, ticket_id and subject. Project those two and you get a two-column result. We did not add any condition on status, so all three tickets from the slide are still there, each with just two attributes. In the full lab table the same query would return four rows, because the lab also has ticket 1009.

Look at the SQL box. SELECT ticket_id, subject FROM tickets. The list after SELECT names the output columns. Compare that with the last slide: there the WHERE clause chose rows, and here the SELECT list chooses columns.

Now the difference the subtitle mentions. A mathematical relation is a set, so if two output rows are identical, they collapse into one. Ordinary SQL keeps both. Picture projecting only assignee_id. Tickets 1001 and 1003 both have 201, so SQL would show 201 twice. If you want duplicates removed, you have to ask with SELECT DISTINCT. In today's example that never comes up, because ticket_id is unique, so every row is already different.

Projection does not remove anything from the stored table. It only decides what this one query shows its reader. A screen can show IDs and subjects while the database keeps everything else. Later we will use a limited view of columns as part of a permission boundary. But hiding a field on a screen is not, by itself, security.

[Sources]
- https://www.postgresql.org/docs/current/queries-select-lists.html
- Operating Cloud Databases, Chapter 2, relational algebra and SQL duplicates

## Slide 15

Now we combine two tables, and there are two very different ways to do it.

Look at the left box, the Cartesian product, R times S. It pairs every ticket with every agent. The vertical bars mean "number of rows." The full lab has 4 tickets and 2 agents, so the product has 8 pairs. Most of them are nonsense. Ticket 1001 gets paired with Agent 202, even though its assignee is 201. The product does not care what the rows mean.

The right box is the join. A join keeps only the pairs that satisfy a condition, and the condition is written right there: tickets.assignee_id equals agents.agent_id. That condition is the whole point. The join symbol by itself does not tell you what matches.

Ticket 1001 has 201, and Agent 201 has 201. Match. Ticket 1003, also 201. Match. Tickets 1004 and 1009 have NULL, and NULL matches nothing, so neither one produces a row. And Agent 202 has no ticket pointing at them in the lab data.

This is what a join means, not how it runs. The database does not have to build all 8 pairs first. It picks an efficient method that gives the same answer.

And look at the line at the bottom of the slide. An inner join keeps only matches. A left join can keep a ticket even when its assignee has no match, without inventing an agent. Hold on to that sentence, because it is the fix for our dashboard.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN
- Course-authored Week 1 four-ticket, two-agent fixture

## Slide 16

Here is the actual dashboard query from the lab. The left side says it in words. The right side is the SQL. You do not need to run it for the assignment.

FROM tickets AS t gives the tickets table the short name t. JOIN agents AS a brings in agents as a. ON t.assignee_id equals a.agent_id is the matching condition. Because this is an inner join, a ticket with no matching agent produces no row at all. WHERE t.status IN new, open keeps the active statuses. And the SELECT list returns the ticket ID, the subject, and the agent's name.

On the slide I numbered the steps match, then keep active, then choose columns. Your lab describes the first two in the other order. For an inner join with a WHERE condition, the order you think about them in does not change which rows come out.

This query contains two separate decisions. One defines active work, the status condition. The other requires an agent match. The status rule can be perfect and the dashboard can still drop active work because of the join. The DBMS runs this query exactly as written, and the result still breaks the dashboard's promise.

For the lab, list the IDs that should appear and compare them with what the dashboard shows. Then predict what happens if ticket 1004 is assigned to Agent 202. That changes the data, not the rule. Describe the fix in plain words. We write the outer join next week.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html
- Course-authored Week 1 lab, current dashboard rule

## Slide 17

Let's pull the week together, box by box.

Request path: client, API, identity, DBMS, data. A browser sends a request, the application checks who is asking and what they may do, and the DBMS reads or changes stored data. A dashboard is a later, separate query. That is why a successful save and a complete report need separate checks.

System layers: the database is not the DBMS, and the DBMS is not the managed platform. Naming the layer tells you where to look.

Row meaning: relations, attributes, tuples, domains, keys. One ticket row is one request. The primary key tells requests apart. A nullable assignee lets us record work nobody has accepted yet.

Query operations: selection decides which rows qualify, projection decides which columns come back, and a join combines rows by a matching condition. An inner join drops rows that have no match. That one sentence explains our missing tickets.

Now the lab. It is one individual submission in Brightspace: your short request trace, your explanation based on the supplied rows, and your prediction after the assignment changes. The lab itself does not need SQL, a cloud account, or GitHub.

Next week is a substantial SQL review. We write filters, handle NULL carefully, compare inner and outer joins, and build summaries whose counts mean what we intend. We also practice changing data inside a transaction and rolling the change back. The Week 2 guide assigns the reading from Chapter 2. Before then, review filtering, NULL, and joins.

[Sources]
- Course-authored Week 1 lab and weekly guide
- Operating Cloud Databases, Chapters 1 and 2
- https://www.postgresql.org/docs/current/tutorial-concepts.html

## Slide 18

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Following one request (1:24); Selection and projection (1:34); Where did the requests go? (1:18). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 1 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
