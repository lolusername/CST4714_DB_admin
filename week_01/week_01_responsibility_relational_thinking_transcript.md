# Week 1: How Applications Use Databases - Spoken Transcript

## Slide 1

Every application that remembers something depends on a data system. A music service remembers playlists. A game remembers inventory and scores. A store remembers products, orders, and payments. This course is about what happens behind those familiar screens. We will learn how applications represent information, how database software protects and retrieves it, how administrators diagnose failures, and how cloud platforms change the work without eliminating the underlying concepts. Today begins with one simple question: when a person clicks Save, where does the information actually go? We will trace that path from the client, through an application service, to a database management system and durable storage. Then we will learn the relational vocabulary that lets us describe tables precisely instead of treating SQL as a collection of memorized commands.

[Sources]
- CST4714 course textbook, Chapter 1: How Database-Backed Applications Work.
- CST4714 course textbook, Chapter 2: Relations, Algebra, and SQL.

## Slide 2

A database is not an abstract topic separated from software. It is the organized memory behind products people already understand. Consider a music service. The interface may show album art and a Play button, but the system must store tracks, artists, users, subscriptions, playlists, and the order of tracks inside each playlist. An online store has a different interface, yet it also needs stable identities, relationships, validation rules, and concurrent updates. A city service request system must preserve locations, status history, assignments, and accountability over time. The important shift is to look through the screen and ask what facts the system must remember, which questions it must answer, and which mistakes it must prevent. Those questions lead directly to schema design, queries, permissions, transactions, indexes, backups, and monitoring.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.1.

## Slide 3

A Save action usually crosses at least five boundaries. The client, such as a browser or phone app, creates an HTTP request. An API endpoint receives that request and translates it into application logic. Identity and authorization checks decide who the caller is and what the caller may do. The application then sends a database command, such as SQL for PostgreSQL or a document operation for MongoDB. The database management system validates the command, coordinates concurrent work, and changes durable data. This path matters because a visible symptom does not identify the failing layer. A disabled button is different from an HTTP error. An HTTP success response is different from a committed database transaction. Database administration begins by tracing the actual path and locating the boundary where expected behavior stops.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.2.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST
- https://www.postgresql.org/docs/current/sql-insert.html

## Slide 4

The word database is often used loosely, but three layers deserve separate names. A database is the organized information and its structure. In a relational system, that includes tables, rows, columns, constraints, and indexes. A database management system, or DBMS, is the software that accepts commands and manages that information. PostgreSQL, MongoDB, and SQLite are DBMS products with different architectures and data models. A managed cloud platform operates infrastructure around a DBMS. Supabase provides a managed PostgreSQL environment plus services such as authentication and APIs. MongoDB Atlas provides managed MongoDB clusters plus operational tools. The cloud platform reduces some installation and maintenance work, but the database concepts remain. You still need to understand data shape, access control, query behavior, performance, and recovery.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.3.
- https://www.postgresql.org/docs/current/intro-whatis.html
- https://www.mongodb.com/docs/manual/introduction/
- https://supabase.com/docs/guides/database/overview

## Slide 5

This is a Supabase project dashboard. The interface gives one place to configure a managed project, but it is important to understand what sits underneath it. The database engine is PostgreSQL. When we create tables, write SQL, define constraints, examine query plans, add indexes, or reason about transactions, we are using PostgreSQL concepts. Supabase adds surrounding services and a web interface that make the system easier to access from applications and from a classroom. The dashboard is therefore not the database itself. It is an operational view into a larger platform. If an application fails to read a table, the cause could be a PostgreSQL permission, a row-level security policy, an API configuration, an incorrect connection string, or the application code. Naming the layers keeps those possibilities distinct.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.4.
- CST4714 redacted course screenshot: textbook/figures/cloud_interfaces/supabase_project_overview.png, captured August 25, 2026.
- https://supabase.com/docs/guides/database/overview

## Slide 6

This is a MongoDB Atlas project overview. Atlas organizes resources into an organization, a project, and one or more clusters. The cluster runs MongoDB. Inside MongoDB, data is organized into databases, collections, and BSON documents rather than relational tables and rows. Atlas also controls access around the database. A database user supplies credentials. A network access rule determines which source addresses may attempt a connection. The connection string tells a client how to locate the cluster. These are separate conditions, and all of them must be correct. The screenshot also shows a free-tier cluster paused after inactivity. Resuming the cluster changes availability; it does not change the stored data model. Later in the course, we will connect to Atlas, inspect documents, write MQL, model relationships, and reason about replication and recovery.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.4.
- CST4714 redacted course screenshot: textbook/figures/cloud_interfaces/atlas_project_overview.png, captured August 25, 2026.
- https://www.mongodb.com/docs/atlas/
- https://www.mongodb.com/docs/manual/core/document/

## Slide 7

Database administration is not a collection of dashboard clicks. It is the discipline of changing a shared data system without losing its meaning or its service. Correctness includes choosing data types, defining constraints, and using transactions so related changes succeed or fail together. Availability includes observing system health, understanding dependencies, and planning for failure. Security includes identities, roles, permissions, network rules, and the principle of least privilege. Recovery includes backups, restoration procedures, and tests that demonstrate whether a useful state can be recovered. Performance connects to all four areas because slow queries can become availability problems, and careless tuning can weaken correctness or security. Throughout the semester, each technical skill will be tied to one of these responsibilities and practiced in PostgreSQL, MongoDB, or both.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.5.
- https://www.postgresql.org/docs/current/ddl-constraints.html
- https://www.mongodb.com/docs/manual/core/security-transport-encryption/

## Slide 8

Suppose a ticket form reports success, but the ticket does not appear in the list. The symptom is real, yet it does not identify the cause. Start at the request path. Confirm that the client sent the request the user intended. Inspect the API status and response body. Determine whether the database command succeeded and committed. Then examine the query used to refresh the list. A successful write can be hidden by a filter, stale cache, or read from a different environment. A successful HTTP response can also be returned before a failed asynchronous operation. The goal is not to collect every possible observation. The goal is to choose the smallest observation that separates competing explanations. That habit makes troubleshooting faster and prevents random changes from creating additional problems.

[Sources]
- CST4714 course textbook, Chapter 1, section 1.6.
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201

## Slide 11

The second part of Week 1 introduces the relational model. A relation can be displayed as a table, but the model is more precise than a spreadsheet grid. A relation has named attributes, values drawn from domains, tuples that represent facts, and keys that preserve identity. Relational algebra describes how one relation can be transformed into another. Selection keeps rows that satisfy a condition. Projection keeps or computes selected attributes. Join combines related tuples. These operations are the conceptual foundation of SQL, even though SQL has additional features and slightly different semantics. Learning the model gives us a durable way to reason about queries. Instead of memorizing clauses, we can ask what relation exists before an operation, what relation should exist afterward, and which operation bridges the two.

[Sources]
- CST4714 course textbook, Chapter 2: Relations, Algebra, and SQL.
- E. F. Codd, A Relational Model of Data for Large Shared Data Banks, Communications of the ACM, 1970, https://doi.org/10.1145/362384.362685

## Slide 12

This table displays a relation named tickets. Its schema defines four attributes: ticket_id, title, status, and requester_id. The schema also includes a domain for each attribute. Ticket identifiers and requester identifiers might be integers, while title and status are text with additional rules. Each data row is a tuple representing one ticket fact. In the pure relational model, a relation is a set, so tuple order is not meaningful and duplicate tuples are not part of the relation. A key is an attribute, or combination of attributes, whose value uniquely identifies a tuple. Here ticket_id is the natural candidate for the primary key. The highlighted value 101 is not merely the first cell in a spreadsheet. It is the identity of one ticket that other relations can reference.

[Sources]
- CST4714 course textbook, Chapter 2, sections 2.1 and 2.2.

## Slide 13

Schema and instance describe different aspects of a database. The schema is the declared structure: relation names, attribute names, data types, keys, and constraints. It answers what kinds of facts the database is designed to store and which values are allowed. The instance is the set of tuples present at a particular moment. It answers what the database currently knows. A schema should change through deliberate migrations because applications and queries depend on it. The instance changes through ordinary inserts, updates, and deletes. Domains connect structure to meaning. If status is unrestricted text, misspellings such as opened or close can fragment the data. A domain or constraint can limit status to accepted values such as open and closed. Database design is therefore not only about where values fit; it also defines which states are valid.

[Sources]
- CST4714 course textbook, Chapter 2, sections 2.1 through 2.3.
- https://www.postgresql.org/docs/current/ddl-constraints.html

## Slide 14

Keys let separate relations describe connected facts without copying an entire record each time. In the users relation, user_id is the primary key. It identifies a user independently of a name, which might not be unique and might change. In the tickets relation, requester_id is a foreign key. Its value refers to an existing user_id. Ticket 101 stores the value 7, which connects the ticket to Luis. This design avoids repeating Luis’s name in every ticket and gives the system one authoritative user record. A foreign key constraint can prevent a ticket from referring to a user that does not exist. The connection is logical rather than visual: the database stores matching values, and a join reconstructs the combined view when a query needs ticket and user information together.

[Sources]
- CST4714 course textbook, Chapter 2, section 2.3.
- https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK

## Slide 15

Selection is a unary relational operation, meaning it takes one relation as input. It evaluates a condition for each tuple and keeps only the tuples for which that condition is true. The Greek letter sigma denotes selection. In this example, sigma subscript status equals open applied to tickets returns the two highlighted tuples, ticket 101 and ticket 103. The result remains a relation with the same attributes as the input, but potentially fewer tuples. In SQL, the WHERE clause performs the corresponding filtering job. The SELECT star portion keeps all available columns, while WHERE status equals open controls which rows qualify. Thinking in algebra separates two choices that SQL writes in one statement: selection controls tuples, while projection, introduced next, controls attributes.

[Sources]
- CST4714 course textbook, Chapter 2, section 2.4.
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-WHERE

## Slide 16

Projection is also a unary operation, but it changes the attributes rather than filtering tuples. The Greek letter pi denotes projection. Pi ticket_id comma title applied to tickets returns a relation with exactly those two attributes. Its output schema is therefore ticket_id and title. In SQL, the list after SELECT performs this job. Projection can also compute expressions or rename outputs in practical query languages, although the formal algebra is often introduced with simple attribute lists. Selection and projection commonly appear together. We might first select open tickets and then project only their identifiers and titles. The order can affect intermediate data and, in some cases, whether later operations still have the attributes they need. The key question is always explicit: which tuples should remain, and which attributes should the result expose?

[Sources]
- CST4714 course textbook, Chapter 2, section 2.4.
- https://www.postgresql.org/docs/current/queries-select-lists.html

## Slide 17

The Cartesian product pairs every tuple from one relation with every tuple from another. If relation R has three tuples and relation S has four, the product contains twelve pairs. That operation is mathematically simple but usually produces combinations with no business meaning. A join adds a condition that keeps only meaningful pairs. An equi-join compares attributes for equality. Joining tickets and users where tickets.requester_id equals users.user_id pairs each ticket with the user who requested it. The number of output tuples depends on the data and the relationship. A primary-key-to-foreign-key join typically returns at most one matching parent for each child. A many-to-many join can return many matches. Understanding cardinality is essential because incorrect join conditions create wrong results and can expand intermediate data dramatically.

[Sources]
- CST4714 course textbook, Chapter 2, sections 2.4 and 2.5.
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN

## Slide 18

This example translates one relational expression into SQL. Begin with tickets joined to users where requester_id equals user_id. That reconstructs each ticket together with its requester. Next, selection keeps only tuples whose ticket status is open. Finally, projection keeps the title and user name attributes needed in the output. SQL writes the same logic in a different surface order. SELECT names the projected output. FROM and JOIN identify the input relations and matching condition. WHERE applies the selection condition. A database optimizer may execute an equivalent plan in a different physical order, but the logical meaning remains. This translation skill is more durable than memorizing one query. When a query is wrong, describe the intended result as relations and transformations, then compare that description with the SQL clauses actually present.

[Sources]
- CST4714 course textbook, Chapter 2, sections 2.4 through 2.6.
- https://www.postgresql.org/docs/current/queries.html

## Slide 20

Week 1 established four foundations. First, trace a user action through the client, API, identity layer, DBMS, and stored data. Second, distinguish the data itself from the software that manages it and the cloud platform that operates surrounding infrastructure. Third, describe relational data with precise terms: relation, attribute, tuple, domain, schema, instance, primary key, and foreign key. Fourth, interpret selection, projection, product, and join as transformations that produce new relations. These ideas will return throughout the semester. Before Week 2, read Chapter 2 with particular attention to joins, grouping, subqueries, and window functions. Bring the Week 2 SQL Query Ladder lab. The next class will turn today’s logical operations into increasingly expressive SQL and will examine how query structure affects correctness before performance tuning begins.

[Sources]
- CST4714 course textbook, Chapter 2, sections 2.5 through 2.8.
- CST4714 Week 2: SQL Retrieval and Query Reasoning.

## License

Except where otherwise noted, this transcript is licensed under CC BY 4.0.
