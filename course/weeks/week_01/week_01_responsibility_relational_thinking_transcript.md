# Week 1: How Applications Use Databases - Spoken Transcript

## Slide 1

A student reports a broken bench. The website gives the student a confirmation number, but the repair desk cannot find the request on its dashboard. We will use that discrepancy to study how an application uses a database. The question is concrete: did the system lose the request, or did the dashboard leave it out? Those possibilities require different repairs.

A database stores organized facts that an application needs to retain. A database management system, or DBMS, is the software that processes requests to read or change those facts. An application usually reaches the DBMS through other software, including a service that checks permissions and handles requests. The arrows here show that relationship. API means application programming interface. In our example, it is the agreed way for the browser to ask the application for an operation.

Our first meeting follows a request through those components. Our second meeting examines the rows and the rule that creates the dashboard. We will introduce relational vocabulary and a few SQL examples, but the lab does not require you to remember SQL or create a cloud account. You will read a small supplied dataset and explain a result. Later, we will execute these ideas in SQL and then compare them with document databases. The same reasoning will help us distinguish a missing record from a missing query result.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?
- https://www.postgresql.org/docs/current/tutorial-arch.html

## Slide 2

The repair desk is a fictional teaching case. Each ticket represents one request for work. The database records its identifier, subject, current status, and staff assignment. An identifier gives us a way to talk about the same request even if its subject or status changes.

The dashboard promises to show every active request. We must define active before we can test that promise. In this exercise, new and open requests count as active. A resolved request does not. Those are application rules. A database cannot infer what a repair desk intends the word active to mean. Someone must express the rule in the software.

The student has confirmation number 1004 for a broken bench. That number lets us compare the student's experience with the stored record and the dashboard result. It does not, by itself, prove which part of the system failed. A response could contain an incorrect number, or a later query could exclude a valid record. The lab supplies the stored rows so we can examine this distinction directly.

There is an important difference between a table and a report made from that table. A table can contain resolved work, active work, and unassigned work. A report chooses some of those rows and some of their attributes. Every condition we add changes which facts the report includes. We will keep that distinction in view while tracing the request and learning the relational operations.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?

## Slide 3

Read the upper diagram from left to right. The browser collects the student's description and sends an HTTP request to the application. HTTP is the protocol used for communication between the browser and a web service. POST commonly requests creation of a resource. The path slash API slash tickets identifies the operation's destination within this illustrative application. The object below it carries the description.

The API endpoint is the application code that receives that request. It checks the caller's identity and whether the caller may create a ticket. Authentication establishes who the caller is. Authorization determines which operations that caller may perform. These checks may happen in more than one component, including database permissions.

The application then asks the DBMS to insert a row. INSERT INTO names the table. The parenthesized list names the columns, and VALUES supplies the corresponding values in the same order. Here 1004 identifies the new request, the subject describes the bench, new records its initial status, and NULL means there is no assigned agent yet. This command illustrates the four-column table used in today's case, before ticket 1004 exists. It is not a setup script for the larger course database, and we are not running it as a lab requirement. Real applications commonly let the database generate an identifier.

The DBMS checks applicable rules and coordinates the write. After a successful commit, the application can return confirmation to the browser. Commit means that the transaction has completed successfully according to the database's guarantees. Closing the browser should not erase a committed ticket. Displaying a list later requires a separate read operation, which can apply different conditions.

[Sources]
- https://www.postgresql.org/docs/current/tutorial-arch.html
- https://www.postgresql.org/docs/current/sql-insert.html
- Course-authored Week 1 four-column illustration

## Slide 4

These three terms describe different parts of a system. The database is the organized data and its declared structure. In our repair-desk example, that includes the tickets, agent records, and rules governing valid relationships. A database can also contain indexes and other supporting information, which we will introduce when we study retrieval and administration.

DBMS abbreviates database management system. It is executable software. PostgreSQL, MongoDB, and SQLite are examples, although they differ in their data models, deployment arrangements, and features. The DBMS accepts operations, evaluates queries, enforces the rules that have been configured, and manages changes to stored data. A useful query is still the developer's responsibility. A DBMS can correctly execute a query that answers the wrong business question.

A managed platform operates database infrastructure and provides related services. Supabase provides a PostgreSQL database with an application platform around it. MongoDB Atlas manages MongoDB deployments. Their web dashboards let authorized people configure and inspect the service. The dashboard is an interface to the system rather than the data itself.

This distinction helps us describe problems precisely. An invalid query differs from an unavailable database server. A missing permission differs from a disconnected browser session. It also helps us retain transferable knowledge. Understanding a primary key or a transaction remains useful when a vendor moves a button. Managed services change how we perform some operational work, but we still need to understand the data and the rules our application depends on.

[Sources]
- https://www.postgresql.org/docs/current/tutorial-arch.html
- https://supabase.com/docs/guides/database/overview
- https://www.mongodb.com/docs/atlas/

## Slide 5

This is a redacted Supabase project screenshot captured for the course in August 2026. It shows the project overview, not the rows in a ticket table. The database appears as one component with information about its health and resource use. Labels and layout may change, so we will learn the role of each tool rather than memorize the location of every control.

Supabase gives a project a PostgreSQL database. PostgreSQL performs the relational database work: storing tables, evaluating SQL, enforcing constraints, and coordinating transactions. Supabase adds services and interfaces around that database. Its dashboard includes a table editor and a SQL editor. The table editor provides a visual way to inspect or edit rows. The SQL editor sends SQL commands to the database. They are different interfaces to the same underlying data.

Authentication is another platform service. It can help an application identify a signed-in user. Identifying a user does not automatically grant appropriate access to every table. The application and database still need authorization rules. We will develop those rules later with concrete allowed and denied examples.

A healthy status in an overview tells us something about service operation. It cannot certify that our dashboard includes every active ticket. That requires inspecting the query and its result. Likewise, a backup label does not establish that a particular plan provides every recovery feature. Today's purpose is to recognize the platform and database layers. You do not need to buy a plan or create a project for this week's exercise.

[Sources]
- https://supabase.com/docs/guides/database/overview
- Course screenshot: August 2026, account identifiers redacted

## Slide 6

This second screenshot shows MongoDB Atlas. It is also a managed platform, but the database software here is MongoDB. An Atlas project organizes deployments and access settings. A cluster is a database deployment that an application can connect to. The word cluster has different precise meanings across products, so we will use each product's definition when we configure it.

Inside MongoDB, a database contains collections. A collection holds documents. A document represents a record using named fields, and a field can itself contain a nested document or an array. MongoDB stores these documents using BSON, a binary representation that supports values such as dates in addition to familiar JSON-like structures. We will introduce JSON carefully before asking you to write MongoDB queries. No BSON syntax needs to be memorized today.

Notice that access settings surround the database. A person can be able to sign in to the Atlas website while an application still cannot connect to a cluster. Database users, connection details, and network access rules affect that application connection. Website sign-in and database authentication are related operational concerns, but they are not interchangeable credentials.

The two platform screenshots show a common pattern: an application connects to database software running somewhere, and a management interface helps people operate it. The main difference we will study is how the records are organized and queried. For now, both systems can store a support request, and neither can automatically decide which requests our repair-desk dashboard ought to display. This screenshot is a dated illustration, not a requirement to configure an account today.

[Sources]
- https://www.mongodb.com/docs/atlas/
- https://www.mongodb.com/docs/manual/core/databases-and-collections/
- Course screenshot: August 2026, account identifiers redacted

## Slide 7

We can describe database administration through the promises a working application needs to keep. Correctness means the stored facts and the operations on them follow the intended rules. In the repair desk, a ticket should retain its identity when its status changes, and an assigned agent should refer to a real staff record. We will use constraints to reject some invalid states and transactions to coordinate related changes.

Security concerns which people or programs may read or change particular information. A student who submits a repair request should not gain permission to delete the entire ticket collection. Least privilege means granting the access needed for a task while withholding unrelated powers. We will test both permitted and rejected operations rather than assume a permission setup works.

Availability concerns whether legitimate users can reach the service when they need it. A stopped server or broken connection can prevent a correct query from completing. Slow operations can also make a service impractical to use. We will learn to observe these conditions and distinguish them from errors in the query's meaning.

Recovery concerns bringing useful data back after a mistake or failure. Creating a backup file is one action. Restoring it into a separate target and checking important records is how we learn whether it can support recovery. Those later exercises will build on the same habit we use today: state an expected outcome, examine the actual records, and explain the difference. We begin with four rows because the mechanism is easier to see before scale makes the symptoms harder to interpret.

[Sources]
- Operating Cloud Databases, Chapters 1 and 3 through 8
- https://www.postgresql.org/docs/current/ddl-constraints.html

## Slide 8

Here is the reported problem again. The form reports success, but ticket 1004 does not appear on the staff dashboard. The response shown below says HTTP 201 Created and includes ticket identifier 1004. In normal HTTP semantics, 201 indicates that the request succeeded and created a resource. We still need to connect that response to the stored record and the later read operation.

First, the client must have sent the intended request. Second, the application must have handled it and returned the response we are examining. Third, the database write must have committed. A commit is different from the browser merely displaying a message. Fourth, the query that refreshes the dashboard must include the ticket if it meets the dashboard's stated purpose.

The supplied lab data lets us examine the fourth step without logging into a cloud account. If ticket 1004 is present in the table but absent from the query result, deletion is not the explanation supported by those rows. The row and the displayed result are two different objects. A filter can exclude a row, and a join can exclude a row that has no match. We will define both operations in the next part of the lesson.

There are other possible causes in real applications, such as reading a different database or showing an older cached result. We should not add those explanations when the supplied case already identifies the relevant rule. A useful diagnosis names the observation, connects it to a mechanism, and proposes a change that addresses that mechanism. The second part of this week's lab develops exactly that explanation.

[Sources]
- Course-authored Week 1 lab, Where Did the Requests Go?
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201

## Slide 9

Our second meeting moves from the path of a request to the structure of its data. The relational model gives us a precise way to describe records and transformations. E. F. Codd introduced the relational model in 1970 as a way to describe data independently of many details of its physical storage. That separation helps explain why a query can state a desired result while the database chooses how to retrieve it.

A relation is a set of tuples with named attributes. We can display it as a table, with one tuple per row and one attribute per column. The words are new labels for ideas we can inspect directly. We will identify what one row means before writing a query. For the tickets table, it means one support request.

The two Greek symbols introduce operations on relations. Sigma denotes selection, which keeps rows satisfying a condition. Pi denotes projection, which keeps chosen attributes. We will first show these operations separately. A later example combines them with a join, which matches related rows.

SQL draws on these ideas but does not follow every rule of classical set algebra. SQL results can contain duplicates, and SQL uses NULL for missing or unknown values. Classical relations do not contain duplicate tuples. We will make these differences explicit when they affect a result. Today's aim is to describe which rows and columns an operation should produce. The next week gives us extensive practice expressing and checking those descriptions in SQL.

[Sources]
- E. F. Codd, A Relational Model of Data for Large Shared Data Banks, 1970, https://doi.org/10.1145/362384.362685
- https://www.postgresql.org/docs/current/tutorial-concepts.html

## Slide 10

This table shows three of the tickets used in our lab. The subjects are shortened on the slide so the fields remain readable. The lab handout contains the complete four-row example, including ticket 1009. Here we have four attributes: ticket identifier, subject, status, and assignee identifier. Each row describes one request.

A tuple means one complete row of attribute values. Ticket 1001 is open and assigned to agent 201. Ticket 1003 is resolved and also assigned to agent 201. Ticket 1004 is new and has NULL in its assignee field. In this application, that NULL records the absence of an assignment. It is not the number zero and not the text word NULL. The ticket row itself still exists.

A schema describes the permitted structure, including attribute names, types, and rules. A key identifies a row. We choose ticket_id as the primary key for this example, meaning it must be unique and cannot be NULL. Two requests might have the same subject, so the subject is not a dependable substitute for the identifier.

The table's displayed row order is just a presentation choice. Relational reasoning does not treat the first displayed row as inherently first in the data. SQL similarly requires an explicit ordering rule when the result order matters. We will add ORDER BY in the SQL review. For now, follow identifiers rather than positions. That habit lets us track the same request through filters, joins, and later changes.

[Sources]
- Course-authored Week 1 ticket excerpt
- https://www.postgresql.org/docs/current/tutorial-concepts.html
- https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-PRIMARY-KEYS

## Slide 11

Schema and instance distinguish a rule from the facts currently governed by that rule. The schema on the left says tickets have identifiers, subjects, statuses, and assignee identifiers. The notation is a compact description, not a complete SQL CREATE TABLE command. Integer indicates a whole-number type. Text indicates a character string. A full SQL declaration would also state keys, nullability, and any additional constraints.

The instance on the right means the rows present at one moment. Inserting a fourth ticket changes the instance without necessarily changing the schema. Renaming a column or adding a constraint changes the schema and may affect application code. We will study how to make such changes safely after rebuilding SQL fluency.

A domain is the set of values permitted for an attribute. An integer type rules out ordinary words, but a type alone may be too broad for an application's meaning. Status is text, yet our course case uses a specific vocabulary: new, open, resolved, and closed. The application considers only new and open active. A database constraint can reject misspellings, but it cannot choose the organization's intended vocabulary for us.

A separate nullability rule decides whether a value must be present. Ticket identifiers must be present. An assignee can be absent until someone takes the work. Treating every missing value as an error would prevent us from representing a valid unassigned request. The correct rule depends on what the attribute means. This distinction becomes important in the lab because an unassigned ticket can be active and still deserve a place on the staff dashboard.

[Sources]
- https://www.postgresql.org/docs/current/ddl-constraints.html
- Course-authored Week 1 lab and Metro Support status vocabulary

## Slide 12

The agents table records staff identities. Agent 201 is Priya Shah, and agent 202 is Noah Williams. In this example, agent_id is the primary key. A ticket's assignee_id can refer to that key. The arrow points from the reference in tickets toward the identified agent.

Ticket 1001 stores 201 rather than repeating Priya's full staff record. Ticket 1003 refers to the same agent. This is a many-to-one relationship: several tickets can refer to one agent. The reference does not require an agent to have a ticket. Noah can exist in the agents table even when no displayed ticket is assigned to Noah.

A declared foreign key constraint checks that a non-NULL reference has an allowed matching key. If a ticket refers to nonexistent agent 999, the database can reject that value. A nullable foreign key also permits the unassigned state shown for ticket 1004. NULL does not create an imaginary agent, and it does not identify a matching agent record.

Storing an identifier and combining records are different operations. The foreign key constrains a relationship. A join uses a matching condition to produce a query result that can include both the ticket subject and the agent name. SQL can perform a join even without a declared foreign key, but then we must be especially careful about what matches and whether the data satisfies the relationship we assume. Our next examples show how those matching decisions change a report.

[Sources]
- https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK
- Course-authored Week 1 agent and ticket data

## Slide 13

Selection keeps rows satisfying a condition. The Greek letter sigma names this operation. In this example the condition is status equals open. Apply it to each row in the displayed ticket excerpt. Ticket 1001 satisfies it. Ticket 1003 is resolved, and ticket 1004 is new, so neither satisfies this particular condition. Only the highlighted row remains.

The SQL statement expresses the same filtering idea. FROM tickets names the input table. WHERE status equals open supplies the condition. SELECT star requests every column of the qualifying row. Selection therefore changes which rows remain while retaining the input attributes. It does not change the status value in any stored row, and it does not delete the excluded tickets.

Notice the difference between open and active. Our lab defines active as either new or open. This example deliberately selects only open tickets so we can see one equality test clearly. If we used this condition for a dashboard promising every active ticket, it would omit new requests. A syntactically valid condition can still express an incomplete business rule.

We will build the broader active condition in the combined query. First, keep the two questions separate: which rows qualify, and which columns should the result contain? WHERE answers the first question. The list after SELECT answers the second. Despite the word SELECT in SQL, relational selection is the row-filtering idea, not simply the name of the first SQL keyword.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-WHERE
- Course-authored Week 1 ticket excerpt

## Slide 14

Projection keeps selected attributes. Pi denotes projection in relational algebra. Here the highlighted columns are ticket_id and subject. Projecting those attributes gives a result with two columns. We have not added a condition on status, so the projection still represents all three displayed tickets.

The SQL list after SELECT names the requested output columns. SELECT ticket_id comma subject FROM tickets returns those two attributes. Compare it with the preceding slide: the WHERE condition chose rows, while this list chooses columns. In the full lab table, the same statement would include all four tickets because the full table also contains ticket 1009. The slide is showing an excerpt rather than changing the lab's data.

There is one important difference between classical projection and ordinary SQL. A mathematical relation is a set, so duplicate output tuples collapse into one. An ordinary SQL SELECT can keep duplicates. If we projected only assignee_id, repeated assignments to agent 201 could produce repeated values in SQL. SELECT DISTINCT is how SQL explicitly removes duplicates from the output. In today's identifier-and-subject projection, the unique ticket identifier distinguishes each row.

Projection does not remove columns from the stored table. It describes what one query exposes to its reader. An application can display a short list containing identifiers and subjects while retaining statuses, assignments, and other information in the database. Later, we will also consider when exposing fewer columns supports a permission boundary, while recognizing that hiding a field on a screen alone does not enforce database security.

[Sources]
- https://www.postgresql.org/docs/current/queries-select-lists.html
- Operating Cloud Databases, Chapter 2, relational algebra and SQL duplicates

## Slide 15

A Cartesian product pairs every row from one input with every row from another. The vertical bars in this notation mean the number of rows. With four tickets and two agents, there are eight possible ticket-agent pairs. That includes arbitrary pairs such as ticket 1001 with Noah even though its assignee identifier is 201.

An equality join retains pairs whose values satisfy an equality condition. For this case, the condition compares tickets.assignee_id with agents.agent_id. Ticket 1001 matches Priya because both identifiers are 201. Ticket 1003 matches Priya for the same reason. Ticket 1004 and ticket 1009 have no matching agent because they are unassigned. Noah has no matching ticket in the original lab data.

This is a conceptual explanation of join meaning. It does not require the database to physically build all eight pairs before filtering them. A database can choose an efficient algorithm that produces the same result. We will study those execution choices after we understand the desired rows.

An inner join keeps only matches. A left join can preserve rows from its left input even when the right input has no match. That distinction is central to the dashboard problem. Keeping a ticket row in a query result does not require us to invent an assignee. We can preserve the ticket and show that the assignment is missing. The output row count depends on both the matching condition and the data. Neither the word join nor the size of a table is enough to predict it.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN
- Course-authored Week 1 four-ticket, two-agent fixture

## Slide 16

This query expresses the dashboard rule supplied in the lab. The left side explains the operations in words, and the right side shows their SQL representation. It uses all four lab tickets and both agents. You do not need to execute it to complete the assignment.

FROM tickets AS t gives the tickets table the short name t. JOIN agents AS a introduces the agents table with the short name a. ON t.assignee_id equals a.agent_id supplies the matching condition. Because this is an inner join, a ticket without a matching agent does not produce an output row. WHERE then keeps statuses in the list new and open. IN means the status may equal either listed value. SELECT chooses the ticket identifier, subject, and matching agent name for the displayed result.

These clauses let us name two independent decisions. One decision defines active work through the status condition. Another decision requires an agent match. A dashboard can implement the active condition correctly and still omit active work because of the join. The DBMS can execute that query exactly as written while the result violates the dashboard's promise.

For the lab, compare the qualifying ticket identifiers with the identifiers the current dashboard actually returns. Then consider the supplied change that assigns ticket 1004 to Noah. That is a change to the data, not a change to the query's rule. Your explanation should distinguish those two ways of changing a result. If the intended report includes unassigned work, describe the necessary behavior in plain language. We will write and verify the corresponding outer join during the SQL review.

[Sources]
- https://www.postgresql.org/docs/current/queries-table-expressions.html
- Course-authored Week 1 lab, current dashboard rule

## Slide 17

We can now connect the two parts of the week. A browser sends a request to an application. The application checks permissions and asks the DBMS to read or change stored data. A later dashboard query selects and combines some of that data. Those steps explain why a successful write and a complete report require separate checks.

The relational vocabulary gives us a way to describe the data precisely. One ticket row represents one request. A primary key distinguishes that request from other requests. A nullable assignee reference can represent work that no agent has accepted yet. Selection decides which rows satisfy a condition. Projection decides which attributes a result contains. A join uses a matching condition to combine rows, and an inner join omits rows without matches.

Use those ideas to finish the single individual lab in Brightspace. Its required response is the short request trace and the explanation based on the supplied rows, including the prediction after the assignment changes. You do not need to create a GitHub repository, install a database, or submit a second reflection for this exercise.

Next week provides a substantial SQL review. We will write filters, work carefully with NULL, compare inner and outer joins, and construct summaries whose counts mean what we intend. We will also practice changing data inside a transaction and rolling the practice change back. The weekly guide identifies the assigned reading. In the complete course package that includes the relevant sections of our textbook. The Week 1-only package provides free PostgreSQL readings without requiring access to the unpublished book.

[Sources]
- Course-authored Week 1 lab and weekly guide
- Operating Cloud Databases, Chapters 1 and 2
- https://www.postgresql.org/docs/current/tutorial-concepts.html

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
