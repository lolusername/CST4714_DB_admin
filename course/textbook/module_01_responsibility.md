# How Database-Backed Applications Work

## Opening Question

You tap **Submit** in an application. A moment later, a new support ticket,
playlist, order, or game item appears on screen. What happened between the click
and the stored result?

That question is the starting point for database administration. Before tuning,
backing up, securing, or scaling a database, you need a useful mental model of
the complete system around it.

We will follow one fictional service, Metro Support, from a resident's request to
the reports used by staff. Keeping one case lets us see how an early decision has
consequences later. An optional assignee affects a join. A status spelling affects
a workload count. A second copy affects what a resident sees after an update.
Database administration begins with understanding those connections, not with
memorizing a dashboard.

## Learning Outcomes

After this chapter, you can:

- distinguish data, a database, a database management system, and a managed
  cloud platform;
- trace a request from an application to stored data and back;
- explain how PostgreSQL relates to Supabase and how MongoDB relates to Atlas;
- describe the technical work performed by database administrators, backend
  developers, data engineers, and cloud support staff;
- recognize where schemas, queries, identities, networks, and storage can affect
  one request; and
- create a simple Markdown course file with GitHub's browser editor.

## Begin With a Familiar Application Action

Suppose a resident submits a streetlight repair ticket. The application may send
data resembling this request:

```json
{
  "requester_id": 101,
  "category": "streetlight",
  "priority": "high",
  "description": "Lamp is dark at Harbor Avenue"
}
```

The browser does not usually write directly to a database. A common path is:

1. the browser or mobile client collects input;
2. an application server or API checks the request;
3. the application authenticates the user and determines what the user may do;
4. the application sends a SQL statement or MongoDB operation to a DBMS;
5. the DBMS checks types, constraints, permissions, and transaction state;
6. the DBMS reads or changes stored data; and
7. the result travels back through the application to the user.

A delay or error can occur at any stage. The database is important, but it is not
the entire application.

The request body above is input, not proof of identity. A caller could change
`requester_id` from 101 to somebody else's number. The server must establish who
the caller is and either derive the requester ID from that identity or check
that the caller is permitted to act for the named person. A valid JSON object
and a valid database foreign key would not, by themselves, make that request
authorized. We will separate those responsibilities carefully in Chapter 6.

### Persistence Is Different From What the Screen Shows

The browser may hold unsaved text in memory. The API may hold a request while it
is being processed. The DBMS manages the stored record. These are different
states, even when they display the same words. Closing a browser tab should not
delete a ticket that the service has already accepted into durable storage.
Conversely, showing a friendly confirmation before a database write completes
can promise more than the system has done.

A database also contains more than what one screen chooses to retrieve. Consider
this small example, which we will use in the Week 1 lab:

| Ticket | Status | Assigned agent |
|---:|---|---|
| 1001 | open | 201 |
| 1003 | resolved | 201 |
| 1004 | new | none yet |
| 1009 | new | none yet |

Suppose the staff screen first keeps active requests, where active means `new` or
`open` in this small example. That leaves 1001, 1004, and 1009. It then matches
each request to a known agent and retains only successful matches. Now only 1001
appears. Nothing in that sequence deleted either unassigned request. The screen
has answered "which active requests already have a matching agent?" rather than
"which requests still need attention?"

The appropriate repair is to preserve an active request even when its agent is
missing, then label the missing assignment clearly. Adding a larger server,
restoring a backup, or recreating the missing requests would not repair this
query's meaning. This is why we review the relational model before studying
performance and recovery. A fast, highly available system can still give the
wrong answer.

### A Confirmation Can Be Lost After a Write Succeeds

Now consider a different failure. The DBMS stores a new request, but the network
connection breaks before the API's reply reaches the browser. The resident sees
an error even though the ticket exists. Pressing Submit again might create a
second ticket unless the application can recognize the repeated operation.

At this point we do not need a particular implementation. We need the right
distinction: "the client did not receive success" is not identical to "the
database did not make the change." Later chapters introduce transactions,
operation identifiers, and retries. Each is a way to make this uncertainty
manageable rather than pretending it cannot occur.

## Four Terms That Should Not Be Blurred Together

### Data

**Data** represents facts or observations. In the ticket example, `101`,
`streetlight`, and `high` are values. Their column or field names provide
meaning.

### Database

A **database** is an organized collection of data. It may contain tables,
documents, indexes, views, constraints, and metadata.

### Database Management System

A **database management system**, or **DBMS**, is the software that stores and
retrieves data while coordinating users and programs. PostgreSQL and MongoDB are
DBMSs. They provide query languages, access controls, indexes, transactions,
concurrency behavior, and recovery mechanisms.

### Managed Database Platform

A **managed platform** runs a DBMS on cloud infrastructure and adds management
services. The platform may handle servers, storage hardware, software updates,
monitoring, and parts of high availability. The customer still creates data
models, queries, indexes, users, network rules, and application code.

"Managed" describes an allocation of work. It is not a guarantee that every
application rule, query, permission, or recovery procedure is correct. If a
provider replaces a failed disk, that addresses one infrastructure problem. It
does not determine whether our analyst should be allowed to read residents'
email addresses. A useful administrator can identify the particular control
responsible for a result instead of treating the provider as one indivisible box.

Two comparisons will recur throughout this course:

| DBMS | Managed platform used in class | Main representation |
|---|---|---|
| PostgreSQL | Supabase | relations, usually shown as tables |
| MongoDB | MongoDB Atlas | BSON documents, usually written in JSON-like syntax |

Supabase is not a replacement name for PostgreSQL. It is a platform built around
PostgreSQL and additional services. Atlas similarly operates MongoDB deployments
and provides cloud management tools.

### Why Database Systems Separate Logical and Physical Decisions

In the relational model, a user asks for facts by naming relations, attributes,
and conditions rather than by naming disk locations. This distinction is part of
*data independence*: programs should not need to change merely because the system
changes how it stores or finds the same facts. Codd's 1970 paper made protection
from representation changes a central motivation for relational databases.
The original paper's [IBM research record](https://research.ibm.com/publications/a-relational-model-of-data-for-large-shared-data-banks)
provides historical context; the chapter explains the concept without requiring
a paid article download.

For example, the question "which requests are still open?" remains the same if
the DBMS adds an index. The index is a physical access choice, and the query can
retain its logical meaning. If we instead rename a field or redefine what
`open` means, we have changed an interface or a data contract. A consumer may
need revision even though the files remain on the same disk. Chapter 4 studies
how to manage that second kind of change.

This separation is an aim, not perfect insulation. Physical choices can change
latency and resource cost, and those changes matter to an application. The
important advantage is being able to discuss logical correctness and physical
execution as related but different questions.

## Read a Cloud Dashboard Without Treating It as the Database

Figure 1.1 shows a Supabase project overview. The screen combines several kinds
of information: project health, database location, compute size, request counts,
and shortcuts to other platform services. The **Primary Database** card refers
to PostgreSQL; the surrounding dashboard belongs to the Supabase platform.

![Figure 1.1: A redacted Supabase Free project overview. The database is one component inside a larger managed platform. Interface captured August 25, 2026.](figures/cloud_interfaces/supabase_project_overview.png){#fig-supabase-overview width=68%}

Figure 1.2 shows an Atlas project overview. The project contains a MongoDB
deployment and links to Data Explorer, network access, database users, backup,
and other services. The yellow network notice matters because a running database
can still be unreachable from the current client.

![Figure 1.2: A redacted MongoDB Atlas project overview showing a free deployment and the surrounding platform controls. Interface captured August 25, 2026.](figures/cloud_interfaces/atlas_project_overview.png){#fig-atlas-project-overview width=94%}

The labels and menus may change, but the underlying distinctions remain useful:

- **project or organization access** controls who can manage the cloud account;
- **database identity** controls who can connect to the DBMS;
- **network access** controls which clients can reach the service;
- **schema or document design** controls how data is represented; and
- **queries and indexes** control what work the database performs.

## What Database Professionals Actually Do

Database work appears under several job titles. A database administrator may
work beside backend developers, data engineers, site reliability engineers,
security analysts, and cloud support staff. The boundaries differ by workplace,
but the technical work commonly includes the following.

### Model Data

Choose tables, documents, keys, relationships, types, and constraints that match
the facts the application needs to store.

### Manage Access

Create roles and users, grant only necessary privileges, protect credentials,
and review who can read or change sensitive data.

### Change Schemas and Data Safely

Plan migrations, preserve compatibility, use transactions where appropriate,
and avoid losing or misinterpreting existing data.

### Investigate Performance

Read query plans, measure expensive work, design indexes for real queries, and
consider the cost of maintaining those indexes.

### Coordinate Concurrent Work

Understand what happens when many sessions read and write at the same time.
Diagnose blocking, deadlocks, and transaction behavior without guessing.

### Prepare for Failure

Create backups or exports, rehearse restores, understand replication and
failover, and decide how much data loss or downtime an application can tolerate.

### Automate and Communicate

Use scripts, notebooks, version control, logs, and runbooks so recurring work is
consistent and understandable to the next person.

This course practices all of these areas at an introductory level.

## The Same Ticket in Two Database Models

A relational design might separate users and tickets into tables:

The SQL below illustrates definitions. You do not need to execute it in Week 1,
and it is not the full Metro Support setup used in the later labs.

```sql
CREATE TABLE users (
    user_id      integer PRIMARY KEY,
    display_name text NOT NULL
);

CREATE TABLE tickets (
    ticket_id    integer PRIMARY KEY,
    requester_id integer NOT NULL REFERENCES users(user_id),
    category     text NOT NULL,
    priority     text NOT NULL,
    status       text NOT NULL
);
```

The foreign key states that each `requester_id` must identify an existing user.
A query can join the two relations when it needs both ticket and requester data.

A document design might store a bounded requester summary inside a ticket:

```json
{
  "ticket_id": 1001,
  "requester": {
    "user_id": 101,
    "display_name": "Maya Chen"
  },
  "category": "streetlight",
  "priority": "high",
  "status": "open"
}
```

Neither shape is automatically better. The relational design gives the user one
central row and joins when needed. The document design can read a ticket and its
requester summary together but must decide what happens if the display name
changes. Later chapters connect these choices to access patterns, consistency,
and growth.

## A Practical Troubleshooting Order

Consider the report: "The ticket page spins and then says it could not load."
Do not immediately rewrite a query or create an index. First locate the failing
part of the request path.

| Area | Useful first question | Example observation |
|---|---|---|
| Client | Did the browser send a request? | request is absent, pending, or returned an HTTP status |
| Application/API | Did the route run and accept the identity? | application log or authentication error |
| Network | Can this client reach the database endpoint? | DNS, timeout, or allow-list error |
| DBMS | Did the database receive work? | active session, database error, or lock wait |
| Query and data | Did the operation ask for too much or meet an unexpected data shape? | query text, plan, row count, or rejected value |

The purpose of this table is not to produce paperwork. It prevents random changes
to several layers at once.

## Protect Credentials From the First Class

A password, connection string, API key, or private token can grant real access.
Never place one in a public repository, shared slide, submitted notebook output,
or chat message.

Use these habits throughout the course:

- enter secrets only when the program is running;
- use environment variables or the notebook's password prompt;
- keep `.env` files out of Git;
- remove secrets from outputs before sharing work; and
- rotate a credential immediately if it is exposed.

The course datasets use synthetic names and the reserved `example.test` domain,
so they do not contain real student or customer records.

## GitHub as the Course Code Notebook

GitHub stores versions of text files and notebooks. In this course, it can hold
SQL, JSON, Markdown, and small scripts. You do not need to know the command line
on the first day.

To create a Markdown file in the browser:

1. open your course repository;
2. choose **Add file** and **Create new file**;
3. enter a path such as `week_01/app_database_map.md`;
4. write in the editor and check the **Preview** tab; and
5. choose **Commit changes** with a short description.

Markdown uses simple punctuation for structure:

```markdown
# Music App Database Map

## Data the app stores

- users
- playlists
- songs

## Questions the database must answer

1. Which songs are in this playlist?
2. Which playlists belong to this user?
```

The weekly lab states the submission format for that activity.

## Worked Example: Trace One Request

**Action:** An agent changes ticket 1001 from `open` to `in_progress`.

**Possible request path:**

1. the browser sends the ticket identifier and new status;
2. the API identifies the agent;
3. an authorization rule permits agents to update assigned tickets;
4. PostgreSQL begins a transaction;
5. a constraint checks that `in_progress` is an allowed status;
6. PostgreSQL updates the row and commits; and
7. the API returns the new ticket state.

This one action touches identity, authorization, a transaction, a constraint,
stored data, and application behavior. The remaining course studies those pieces
one at a time and then reconnects them.

## In-Class Connection

Before the first meeting, read through **Four Terms That Should Not Be Blurred
Together**, including the request-path examples. Before the second, review
**Persistence Is Different From What the Screen Shows** and the opening
relational-model sections of Chapter 2. In class, use the same missing-request
case to explain a read path and a write path. The weekly page supplies the single
lab submission; the questions below are study practice, not an additional report.

## Chapter Summary

- A database is stored information; a DBMS is the software that manages it; a
  cloud platform operates the DBMS with additional services.
- PostgreSQL is the relational DBMS used by Supabase. MongoDB is the document
  DBMS used by Atlas.
- A user action travels through several layers before it becomes stored data.
- Database work includes modeling, access control, schema change, concurrency,
  performance, recovery, automation, and communication.
- SQL and document models organize related facts differently; the workload
  determines which tradeoffs matter.
- Credentials must never be committed or shared.

## Check Your Understanding

1. Explain the difference between PostgreSQL and Supabase.
2. Explain the difference between MongoDB and Atlas.
3. Name three places a request can fail before the DBMS executes a query.
4. Why might a foreign key be useful in the ticket example?
5. What tradeoff appears when a user name is embedded in a ticket document?
6. Name four kinds of work performed by database professionals.

## Further Reading

- [PostgreSQL, "About PostgreSQL"](https://www.postgresql.org/about/)
- [Supabase architecture](https://supabase.com/docs/guides/getting-started/architecture)
- [MongoDB Atlas documentation](https://www.mongodb.com/docs/atlas/)
- [GitHub Skills, "Introduction to GitHub"](https://github.com/skills/introduction-to-github)
- [O*NET, Database Administrators](https://www.onetonline.org/link/summary/15-1242.00)
