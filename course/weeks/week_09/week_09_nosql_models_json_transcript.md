# Week 9: NoSQL Models and JSON - Spoken Transcript

## Slide 1

We have spent the first part of the course using relations, keys, queries, transactions, and recovery procedures. Those ideas remain useful when we change database systems. This week we will ask what happens when the application's everyday work suggests a different arrangement of the data.

Our recurring example is a support ticket. It has an identity and a current status. A person requested it. Someone may be assigned to it. Over time, the ticket also acquires a history of events. We could put those facts in separate tables, as we have already done. We could also package some of them together in a document. Both choices represent relationships, but they make different reads and changes convenient.

Today we will learn the vocabulary of several database models and work through small graph and vector examples. You do not need previous graph theory or machine learning experience. In our second meeting, we will learn JSON from its punctuation upward and compare two complete representations of the same ticket.

The individual lab will use three CSV files and a text editor. It will not require a database query, a Python program, or a working Atlas connection. That gives us room to reason about the data before introducing another query language.

[Sources]
- Course textbook, Chapter 9. Metro Support is the course-created synthetic dataset.

## Slide 2

Let us recover three ideas from our relational work. First, an identity should survive a change in the attributes that describe the entity. Maya can change her display name while remaining user 101. If we use the name itself as the identity, that ordinary change becomes much more difficult to manage.

Second, requester_id means something specific. It identifies the person who requested a ticket. A matching number in an unrelated field would not establish the same relationship. In our PostgreSQL schema, a foreign key checks that the referenced user exists. A JSON file by itself does not perform that check.

Third, one ticket can have many events. Keeping events separately lets history grow without adding more columns to the ticket row. The event's ticket_id records its owner. We can retrieve related records by matching those identifiers.

When we introduce documents, keep all three ideas. We might place a requester object or an event array inside a ticket, but that placement still expresses a relationship. We still need to define what a name means, how to identify an event, and what changes should remain consistent. A model change does not remove the responsibility to understand the facts.

[Sources]
- Course textbook, Chapters 2, 3, and 9. Metro Support CSVs and PostgreSQL schema.

## Slide 3

The history helps explain why the term NoSQL covers several different ideas. Codd's 1970 relational paper emphasized a logical representation of data and independence from the details of physical storage. We have used that separation whenever we wrote a SELECT without specifying which disk pages PostgreSQL should read.

The earlier use of the name NoSQL by Carlo Strozzi referred to a relational system that did not use SQL. That is different from the broad nonrelational meaning that later became common. The name alone is therefore a poor technical definition.

Google's Bigtable paper appeared in 2006. It described a sparse distributed map for large structured datasets. Amazon's Dynamo paper appeared in 2007 and described a key-value design with strong availability requirements. These systems responded to specific workloads and operating conditions. They did not establish that every small application should abandon relations.

The later NoSQL movement grouped several alternatives under one convenient label. Today, features overlap across products. A relational database can store JSON, and a document database can support transactions. When we compare systems, we need to name the actual model and operation rather than infer every capability from a label. Also keep the research system Dynamo distinct from the later DynamoDB cloud service.

[Sources]
- https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
- https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
- https://sources.debian.org/src/nosql/3.1-4/nosql.lsm/
- Course textbook, Chapter 9, historical discussion and references.

## Slide 4

An access pattern is a recurring read or change that the application needs to perform. It is more specific than saying that the application needs to be fast. For example, opening ticket 1001 and showing its latest events identifies both the record we start with and the related information we want to retrieve.

Now compare a report that counts every event by type across all tickets. That report begins with a population of events rather than one ticket. A representation that makes the ticket page convenient may require additional work for the report. We have not discovered a contradiction. We have discovered two different access patterns.

The diagram groups models by the operations they make natural. A key-value store centers on a known key. A document groups nested information. A graph makes paths explicit. Vector search retrieves numeric neighbors. Wide-column designs put considerable importance on the access key and row organization.

These categories are useful starting points, not a product-selection algorithm. We also need to know how often data changes, how much it grows, which rules matter, and what the team can operate. Adding a second store means another system to secure, monitor, synchronize, and recover. The benefit has to justify that additional work.

[Sources]
- Course textbook, Chapter 9. Course-created model map.

## Slide 5

Imagine a browser presents a session token. The application already knows the exact key, session colon 8f21, and wants the associated value. The value might identify user 101 and record an expiry timestamp. This is a natural key-value operation because the lookup begins with a known identifier.

The text inside the dark area is conceptual notation. It explains the contents without introducing a product command, and it is not strict JSON. We will learn that syntax on Day 2.

Now change the request. An administrator wants every active session belonging to user 101. We know the user ID, but we do not know all of that user's session tokens. The original lookup arrangement does not by itself provide a convenient answer. We may need a separate mapping from user IDs to session keys, an index supported by the product, or a scan that could be expensive.

This is the main design lesson. Fast access through one key says little about a different access path. The same principle will return when we create indexes in MongoDB. Also, an expiry field only stores a timestamp. A real system needs an agreed rule for enforcing expiry, and some products offer automatic expiration features to help implement that rule.

[Sources]
- Course textbook, Chapter 9, Key-Value Store.
- https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

## Slide 6

Here is a small illustration of a Bigtable-style key arrangement. The first part of the key identifies a device. The second part is a timestamp in a consistent, sortable format. With this arrangement, rows beginning with device07 stay together in the logical key ordering, and their timestamps put readings in order within that prefix.

The rows are sparse. The first reading contains temperature. The next contains temperature and battery. A reading from another device contains humidity. Missing cells do not require us to fill every possible measurement with an empty value.

Suppose our common request is to retrieve device07's readings over an interval. This key arrangement gives that request a useful starting point. A report about low batteries across every device starts with a different attribute, so the same arrangement may not serve it directly. We might need another representation or an additional supported access path.

This is an illustration, not a deployment recipe. Actual partitioning and key design must account for how writes distribute and whether some keys become unusually busy. Also, wide-column systems and analytical columnar storage describe different design ideas. The shared word column does not make them interchangeable. We will return to distribution and hot keys later in the course.

[Sources]
- https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
- Course textbook, Chapters 9 and 13.

## Slide 7

This preview packages selected ticket facts into one nested document. The outer object describes ticket 1001. Inside it, requester is another object containing a user ID and a display name. The tags field holds an array. For now, concentrate on containment. We will learn exactly how the braces, brackets, quotes, and commas work during our second meeting.

If a page repeatedly needs the ticket and this small set of details, a document can keep them together. We do not have to assume that every fact associated with a ticket belongs inside it. The word bounded matters. A small, predictable set of labels has a different growth pattern from a history that accumulates events for years.

The nested requester still represents a relationship with user 101. It also introduces a copy of Maya's name if an authoritative user record exists elsewhere. We must decide whether that copy means her current name or her name at a historical moment. Those meanings imply different update rules.

The tags are an illustrative new field rather than a direct copy of a CSV column. Adding fields can be useful, but we should identify which facts came from a source and which fields we introduced as part of the design.

[Sources]
- https://www.mongodb.com/docs/manual/data-modeling/
- Course-created Metro Support example. The tags are illustrative additions.

## Slide 8

A graph has vertices and edges. We often write that as G equals the pair V and E. V is the set of vertices, which people also call nodes. E is the set of edges, which represent relationships. Our example has four vertices and four directed edges.

Every arrow means depends on. Portal depends on Identity and on API. Identity depends on Database, and API also depends on Database. Direction matters. The arrow from Portal to Identity does not say that Identity depends on Portal.

Portal has an out-degree of two because two edges leave it. Database has an in-degree of two because two edges enter it. Portal can reach Database through either Identity or API. Each route has two edges. We call such a connected sequence a path.

A graph representation makes these paths an explicit part of the model. That is useful for dependency analysis, account-device relationships, recommendations, and other problems where several hops matter. It does not mean a relational database cannot store edges or evaluate recursive queries. We are comparing the convenience of a representation and its operations.

Notice that the diagram records dependencies, not a complete failure model. Caches, redundancy, and fallback behavior can affect whether a database failure actually makes Portal unavailable.

[Sources]
- Course textbook, Chapter 9, Graph Database and the dependency example. This is a course-created directed graph.

## Slide 9

Breadth-first search explores a graph one edge-distance level at a time. Begin at Portal, which is zero edges from itself. Its direct neighbors are Identity and API, so they appear at distance one. Their outgoing edges lead to Database, which appears at distance two.

We keep a record of vertices we have already visited. Both Identity and API lead to Database, but that does not make Database two different vertices. The visited set prevents repeated work. It also prevents an endless loop when a graph contains a cycle.

For a graph where every edge has the same cost, this level-by-level exploration finds a path with the fewest edges. Suppose instead that an edge has a latency or travel-time weight. A route with fewer edges could still have a larger total cost. The algorithm and the meaning of shortest must match the problem.

For impact analysis after a Database problem, we would reverse the direction of the question. We would seek services that depend on Database, which means following incoming relationships backward in this diagram. That yields Identity and API first, then Portal. We would still need operating information before declaring that every reachable service has failed. Reachability gives us candidates to investigate.

[Sources]
- Course textbook, Chapter 9, graph traversal discussion. The table derives directly from the four displayed edges.

## Slide 10

A vector is an ordered list of numbers. A two-dimensional vector might contain only two coordinates, such as one and zero. A text embedding often has many more coordinates, produced by a machine-learning model. Those coordinates are learned features and need not have simple labels such as brightness or urgency.

The two incident descriptions on this slide use different words but describe related problems. A suitable embedding model may map them to nearby locations under a suitable similarity measure. The model produces the numbers. The database stores those numbers and uses them to retrieve candidate records. Creating a vector index does not train the embedding model.

The word suitable is important. A model that works well for one kind of language or domain may perform differently on another. The search metric also needs to match how the representation was designed. We should evaluate retrieved results against the task rather than assume that numeric closeness guarantees usefulness.

We will use tiny invented coordinates to understand the geometry. They are not real embeddings of these sentences. You do not need an API key, paid model, or vector database deployment. The immediate goal is to understand what similarity search computes and what it leaves for us to judge.

[Sources]
- https://www.mongodb.com/docs/vector-search/
- Course textbook, Chapter 9. The incident descriptions are illustrative.

## Slide 11

Both vectors begin at the same origin. The horizontal and vertical axes describe a two-dimensional coordinate system. The green vector and the orange vector point in different directions and have different lengths. Theta labels the angle between the two vectors. It does not label the angle between a vector and the horizontal axis.

Cosine similarity compares directions after accounting for the lengths. Its formula divides the dot product by the product of the two Euclidean lengths. We will calculate each of those pieces on the next slide, so there is no need to treat the notation as a formula to memorize without understanding it.

For nonzero vectors pointing in exactly the same direction, cosine similarity equals one. For perpendicular vectors, it equals zero. For vectors pointing in opposite directions, it equals negative one. These are geometric statements. A negative cosine is not a negative probability, and a value near one does not establish that two documents are factually identical.

If we multiply a vector by a positive number, we change its length but preserve its direction. Cosine therefore stays the same. Multiplying by a negative number reverses direction, so the positive-factor qualification matters. A zero vector has no usable direction for this formula because its length makes the denominator zero.

[Sources]
- Course textbook, Chapter 9. Course-created vector geometry figure and elementary vector derivation.

## Slide 12

Let our query vector q be one, zero. Candidate a is ten, zero. Candidate b is one, one. We will calculate cosine similarity instead of treating the answer as a black box.

The dot product multiplies matching coordinates and adds the results. For q and a, one times ten plus zero times zero gives ten. For q and b, one times one plus zero times one gives one.

The Euclidean length measures distance from the origin. We square each coordinate, add the squares, and take the square root. The length of q is one. The length of a is ten. The length of b is the square root of two, because one squared plus one squared equals two.

Now divide each dot product by the product of the corresponding lengths. For a, ten divided by one times ten equals one. For b, one divided by the square root of two is approximately zero point seven zero seven. Larger cosine means the direction is more similar, so cosine ranks a first.

Candidate a points along the same ray as q, even though it lies farther from the origin. Keep that observation in mind. The next calculation will use ordinary straight-line distance and produce a different ranking without either calculation being incorrect.

[Sources]
- Course textbook, Chapter 9, Calculate a Small Example. Values are an original worked mathematical example, not measured embeddings.

## Slide 13

Euclidean distance begins with differences between coordinates. For q and a, the horizontal difference is one minus ten, or negative nine. The vertical difference is zero. Squaring and adding gives eighty-one, and its square root is nine.

For q and b, the horizontal difference is zero and the vertical difference is negative one. Squaring, adding, and taking the square root gives one. Smaller distance means closer points, so Euclidean distance ranks b first.

The two measures answer different questions. Cosine compares direction and removes positive changes of scale. Euclidean distance measures straight-line separation, which depends on both direction and magnitude. If magnitude records something meaningful for our application, throwing it away could lose useful information. If magnitude varies for reasons irrelevant to the task, cosine may be more appropriate.

There is also a precise connection. Divide each nonzero vector by its length and it becomes a unit vector. For the same normalized vectors, squared Euclidean distance equals two minus twice cosine similarity. Maximizing cosine and minimizing that distance then give the same exact ordering, with the usual qualifications about ties and numerical precision.

So the lesson is not that cosine always wins. We need a measure that matches the representation and the question we want the search to answer.

[Sources]
- Course textbook, Chapter 9, worked distance comparison and normalization identity.

## Slide 14

An exact top-five search supplies a reference result under a chosen metric. Our example returns A, B, C, D, and E. An approximate search returns A, C, E, F, and G. Three record IDs overlap, so recall at five for this query is three divided by five, or zero point six.

Approximate nearest-neighbor methods can reduce search work at scale by trading some exactness for speed. How much work they save and how many neighbors they miss depend on the data, algorithm, and settings. A tiny example does not establish a production performance claim.

Recall here measures agreement with the exact retrieval target. It does not tell us that a human found the five results helpful, that the incident descriptions are accurate, or that the results are fair across different kinds of reports. We need examples and evaluation criteria that reflect the actual task as well.

Finally, the closest record may be private. Similarity does not grant the current user permission to read it. The application and database need appropriate access controls. A secure system must apply those rules even when filtering changes the candidate set or the results returned. A useful vector feature is therefore a combination of representation, retrieval, evaluation, and controlled access.

[Sources]
- https://www.mongodb.com/docs/vector-search/
- Course textbook, Chapter 9. The recall calculation uses an original five-ID example.

## Slide 15

This table lets us compare models without treating one as the universal winner. A known session token points naturally toward key-value lookup. One device's ordered readings suggest attention to row keys and a wide-column access pattern. A ticket page with a bounded set of details can fit a document.

Multi-hop dependency questions make graph traversal useful. Similar descriptions can motivate vector search. Shared facts with changing reports remain a strong reason to consider a relational design.

The final column matters as much as the candidate column. For the session store, we need to investigate lookups that do not start with a session key. For documents, we need rules for copied names and arrays that can grow. For vectors, we need to evaluate retrieval and keep track of the embedding model version. The relational choice also has work to do, including appropriate joins, indexes, and schema changes.

These are first hypotheses about useful representations. Actual products often support several models, and a small application may be better served by capabilities inside its existing database than by another service. A sound recommendation identifies the operation, proposes a candidate, and explains the cost it introduces. It should also identify what we would need to measure before claiming that the design is better.

[Sources]
- Course textbook, Chapter 9, model comparison and access-pattern discussion.

## Slide 16

We will now use the vocabulary on a small design problem. The support portal has two needs. It opens individual ticket pages, and it produces a report that counts events across tickets. In your own notes, choose a representation that would help with the page and explain one consequence for the report or for a name change. This is individual practice, not a separate submission.

For example, a document that includes a requester name and a few recent events makes the page's data easy to see together. That answer becomes more useful when we add its cost. If the requester name means the current name, a later change must reach the copy. If we put every event inside every ticket, the event-count report needs to process those nested arrays and the documents continue to grow.

A relational answer is equally available. Keeping users, tickets, and events separately gives shared users one authoritative row and supports flexible reporting. We then need to retrieve the page's related records through appropriate queries and indexes.

The purpose is to state an assumption and follow its consequences. You do not need to invent a complicated multi-database architecture. One clear choice with an explained tradeoff demonstrates more understanding than a list of product names.

[Sources]
- Course-created design exercise based on Metro Support and Chapter 9.

## Slide 17

In our first meeting, we compared database models by what an application reads and changes. Today we will make the document idea concrete by writing JSON. We will begin with the value kinds and punctuation, then build two complete representations of the same ticket.

The first representation will keep users, tickets, and events in separate arrays connected by IDs. The second will place related facts inside the ticket. Both examples will retain the same selected source facts. That allows us to compare the arrangement rather than accidentally compare different information.

We will also see how GitHub's browser editor can hold a Markdown explanation and readable JSON examples in one file. We will distinguish Atlas account settings from database-user credentials and network access. Those tools support the course, but neither GitHub nor a working database connection is required to reason about a JSON shape.

For the individual lab, you will use a different ticket with three events. You will write two designs and a short comparison in one Markdown file. There is no SQL, MQL, or Python requirement today. We are separating representation from execution so that next week's database commands operate on structures you can already explain.

[Sources]
- Course Week 9 guide and individual CSV-to-JSON lab.

## Slide 18

JSON stands for JavaScript Object Notation. Its notation grew from JavaScript object syntax, but JSON is a language-independent data format. A Python service and a JavaScript browser application can exchange the same JSON text and parse it into their own language's values.

Douglas Crockford's RFC 4627 documented JSON in 2006. RFC 7159 revised the specification in 2014, and RFC 8259 became the Internet standard in 2017. ECMA-404 provides the parallel syntax standard. The development reflects an interoperability problem: different programs need to interpret exchanged data consistently.

The small example contains a ticket identifier and a status. The same grammar can express nested objects and arrays, which makes it useful for API responses, events, logs, and configuration. Text is inspectable, and common languages provide parsers. For many application payloads, the notation is also less verbose than an equivalent XML representation. That does not make JSON ideal for every document or every interchange problem.

JSON supplies data representation. It does not store the data durably, enforce a foreign key, or execute a query. We still need applications and database systems for those responsibilities. Keeping those layers distinct will make it easier to understand what Atlas, MongoDB, and a Python driver each do later.

[Sources]
- https://www.rfc-editor.org/info/rfc4627/
- https://www.rfc-editor.org/info/rfc7159/
- https://www.rfc-editor.org/info/rfc8259/

## Slide 19

JSON has six value kinds. An object contains named members. An array contains an ordered sequence of values. A string contains quoted text. A number supplies a numeric value. A Boolean uses either true or false. Null is its own explicit value.

True and false are two spellings within the Boolean kind. Counting their spellings separately can produce seven grammar alternatives, but it should not confuse us into teaching seven different data types. We will consistently use six value kinds, matching the textbook.

The names inside an object must be strings. In the first example, status is a name and open is its string value. An object's member order is not a reliable way to encode a sequence. If order is meaningful, as with a displayed event history, an array can represent that order. An array can technically mix value kinds, although an application may require every element to follow the same structure.

The current JSON standard also permits any JSON value at the top level. A string or number can therefore be an entire JSON text. Our lab deliberately asks for one top-level object in each example because that makes the two designs straightforward to package and compare. That is an assignment choice, not a universal JSON restriction.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- Course textbook, Chapter 9, JSON Has Six Value Kinds.

## Slide 20

Read the outer braces as one object. Each line inside supplies a property name, a colon, and a value. The ticket_id value is the number 1004. The subject and status values are strings, so double quotes surround their text. The assignee_id is null, without quotes. A quoted word null would instead be a string containing four letters.

The tags value begins with a square bracket and ends with a square bracket. That makes it an array. Its two elements are strings. The comma between them separates neighboring values inside that array. At the object level, commas separate neighboring members. There is no comma after the final member.

Indentation is for readers. It does not change which object contains a field, but it makes that containment much easier to follow. Opening and closing punctuation supplies the actual structure.

This example uses selected facts from ticket 1004. The tags are an illustrative addition. They show how a document can contain an array without requiring another CSV table. We should still document such additions rather than suggest that every displayed value came directly from a source file. During the lab, retain the required source facts first, then make the relationships clear through your chosen shape.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- Metro Support ticket 1004. Tags are illustrative additions.

## Slide 21

The first line resembles a Python dictionary or a JavaScript object expression, but it is invalid JSON. There are two independent problems. The property name and string value use single quotes, and a comma follows the final member.

The repaired line uses double quotes and removes the final comma. Repairing only one error would leave the other. When a parser reports the first place it cannot continue, that location does not prove that the rest of the text is correct. Small examples help us isolate one issue at a time.

Standard JSON also excludes comments, NaN, Infinity, and numbers written with a leading zero such as 01. A string such as double-quote zero one double-quote is different and can preserve the spelling of an identifier. An ISO timestamp must also be a string or follow some other explicit representation convention.

Parser behavior needs care. Python's default json parser accepts some nonstandard numeric extensions, and common parsers accept duplicate member names with potentially surprising results. Successful parsing therefore does not by itself prove portable, unambiguous data. For our examples, use standard syntax and unique names. Never use a general-purpose eval operation to read untrusted JSON text, because evaluating code has different risks from parsing data.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- https://docs.python.org/3/library/json.html#standard-compliance-and-interoperability

## Slide 22

These examples distinguish absence from several explicit values. An empty object contains no assignee_id property. The next object includes the property and gives it null. The third includes an events array with no elements. The fourth includes a numeric estimated cost of zero.

An application might define an omitted assignee and a null assignee to mean the same thing, but JSON does not make that policy for us. Another application might use omission to mean that a field was not requested, while null means that the field was requested and there is no assigned person. We need to read or define the contract.

The empty events array has a similar ambiguity. It tells us what this response supplies. It does not tell us whether the ticket has no history, whether a filter removed every event, or whether this response deliberately omitted history. If the distinction matters, the application needs additional information or a clear rule.

Zero is a number, not a missing amount. An estimated cost of zero may be intentional, while no estimated_cost property may mean that no estimate exists. These distinctions become important in filters and updates. Learning them now will help us avoid treating every empty-looking value as interchangeable when we begin MQL.

[Sources]
- Course textbook, Chapter 9, Missing, Null, Empty, and Zero Are Different.

## Slide 23

The value displayed for opened_at is a JSON string. Its characters follow an agreed timestamp format, including a Z that indicates UTC. The JSON grammar does not automatically convert that string into a date object or verify that it describes a possible calendar date.

MongoDB stores documents using BSON, which supports additional types such as Date and ObjectId. When a driver sends data or an import tool reads it, that step determines which BSON type reaches the database. If we insert ordinary text without a conversion, we should not assume that MongoDB silently turns every date-looking string into a Date.

Extended JSON provides JSON-compatible ways to describe BSON values that ordinary JSON cannot represent directly. We will encounter that distinction when we work with actual stored documents. Today's lab deliberately keeps dates as strings so that the task stays focused on structure.

Two other rules help interoperability. Use unique member names inside an object. Also preserve identifiers as strings when exact spelling matters, such as a code with leading zeros or a very large identifier that a receiving language cannot represent exactly as a number. Valid syntax is only one layer. The application still needs meaningful field names, expected types, and rules about which values are acceptable.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- https://www.mongodb.com/docs/manual/reference/bson-types/
- Course textbook, Chapter 9.

## Slide 24

Our worked example uses a small, explicitly selected part of the Metro Support dataset. Users 101 and 201 are Maya Chen and Priya Shah. Ticket 1001 has the subject Streetlight dark near bus stop, an open status, Maya as its requester, and Priya as its assignee.

Two events belong to this ticket in the supplied CSV. Event 5001 records creation at the displayed UTC timestamp. Event 5002 records assignment at the second timestamp. For the next two examples, we will preserve both events' identifiers, types, and timestamps, as well as the ticket facts and the two users' identities and names.

We are intentionally omitting other columns. For example, a user's email address is not needed to compare these two ticket-page shapes. Omitting an out-of-scope field is different from accidentally dropping one of the facts we promised to preserve.

Both designs must contain the same selected information. Otherwise, a shorter example might appear simpler merely because it has lost data. We will first connect separate records with IDs and then express the relationships through containment.

Your lab uses ticket 1003 instead. It has a different status and three events. The worked example supplies the method without completing your assigned case for you.

[Sources]
- course/datasets/metro_support/users.csv
- course/datasets/metro_support/tickets.csv
- course/datasets/metro_support/ticket_events.csv

## Slide 25

This is one complete JSON object. Inside it are three arrays named users, tickets, and events. It packages separate kinds of records in a single text example. That packaging does not create three MongoDB collections, and we are not yet importing it into a database.

In users, each record has a user_id and a display_name. In tickets, requester_id refers to user 101 and assignee_id refers to user 201. To show the requester name, a reader or application matches requester_id with the appropriate user_id.

Each event contains ticket_id 1001. That field connects the event to its ticket. The two event IDs remain distinct, and both timestamps are present. In a larger dataset, we could retrieve events for one ticket by matching that identifier, provided the database and indexes support the needed access efficiently.

This arrangement resembles the separate CSV tables. It retains one displayed copy of each user's name in this package. A current-name change can update the authoritative user record instead of every ticket-shaped copy. The ticket page then has to assemble facts from the related records.

Notice that indentation and line breaks keep a complete, valid example readable. We do not use an ellipsis in place of missing records. Both promised events are present, so the next design can be compared fairly.

[Sources]
- Course-created JSON representation of Metro Support ticket 1001 and events 5001 and 5002.
- Course textbook, Chapter 9, referenced design discussion.

## Slide 26

This alternative makes the ticket itself the outer object. Requester and assignee are nested objects. Both retain the user's ID and the selected name. The events array now lives inside ticket 1001, so containment identifies the owner of those events.

We can omit ticket_id from each nested event because the containing ticket supplies that relationship in this example. Event_id still identifies the event independently. If we later copy an event into a separate collection or message, we would need to carry enough context to identify its ticket there.

The values match the referenced design. We have the same ticket, status, subject, requester, assignee, and two timestamped events. The difference is the arrangement of those facts, not the information we selected.

The ticket page can obtain this bounded example in one document read. In exchange, it carries copies of user names. If user 101 appears in many ticket documents and those copies mean the current display name, a name change creates synchronization work.

History also needs a growth rule. Two events fit comfortably in a teaching example. That observation does not justify embedding every future event indefinitely. A production design should consider how many events can accumulate, how they are queried, and what changes need to be atomic.

[Sources]
- Course-created alternate JSON representation of the same Metro Support facts.
- https://www.mongodb.com/docs/manual/data-modeling/

## Slide 27

A copied name can have more than one legitimate meaning. Suppose Maya changes her display name. If the field means Maya's current display name, the copy should eventually match the authoritative user record under a clearly defined consistency policy. Updating one user record does not automatically update every independent copy.

If the field means the name supplied when the ticket opened, keeping the original text can be correct. A name such as requester_name_at_open tells the reader that it is a historical snapshot. We should not silently update a historical record when the intended fact is what was recorded at the earlier time.

A third choice is to keep only the user ID and retrieve the current name from its authoritative record. That avoids a stored current-name copy in the ticket, but the read must obtain the related user information.

These alternatives explain why there can be several right JSON answers. The rightness depends on an explicit meaning and a workable update policy. We should not classify all duplication as a mistake, and we should not call every stale value a historical snapshot after the fact. The design needs to state the intended meaning before the change happens. Your short lab comparison should make that kind of reasoning visible.

[Sources]
- Course textbook, Chapter 9, Snapshot Plus Reference and Flexible Schema Is Still a Schema.

## Slide 28

Here is a hybrid design for a ticket that may accumulate years of history. The ticket document keeps its ID, status, and at most five recent events for the page preview. Separate event records preserve the complete retained history and identify their ticket with ticket_id.

The five-event bound is a deliberate application rule. It keeps the preview small, but it must not become an accidental deletion policy for the authoritative history. When the sixth event arrives, the preview can drop its oldest entry while the separate history retains the event according to the application's retention requirements.

This convenience introduces another responsibility. The preview is a copy, so something must refresh it. We need to decide what readers can see if the event record has changed but the preview has not yet caught up. A version, timestamp, or documented refresh policy can help make the behavior explicit.

Also, two separate document writes are not automatically one atomic change. We should not promise that simply choosing a hybrid shape solves coordination. Later lessons will address actual database operations and their guarantees.

For today's lab, describe the boundary and its consequence. You do not need to build a synchronization service. Recognizing what a proposed design would require is part of sound beginner modeling.

[Sources]
- https://www.mongodb.com/docs/manual/data-modeling/
- Course textbook, Chapter 9, Worked Example: Compare Two Ticket Shapes.

## Slide 29

GitHub can edit text in the browser without a local Git installation. In your own repository, Add file and Create new file open the editor. Enter week_09_json_models.md as the filename. The dot md extension tells readers that this file uses Markdown.

The example shows a Markdown heading, followed by three backticks and the language name json. A second line of three backticks closes the code block. The JSON between those fences is data text. The fences belong to Markdown and are not part of the JSON itself. Your explanation goes outside the code block.

Preview shows the formatted Markdown. It can make the JSON easier to read by using code formatting, but it does not prove that the JSON is valid. Commit changes records the text in the repository's history. That action also does not validate the syntax or verify that the represented facts match the CSV.

For this assignment, download the finished file and submit that one file to Brightspace. A public repository is not required. If GitHub is unavailable, an ordinary local text editor can create the same Markdown file. Use only the synthetic course data, and keep database connection strings and passwords out of both the document and commit history.

[Sources]
- https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files
- Course Week 9 lab submission instructions.

## Slide 30

Atlas is the cloud management platform around our MongoDB deployment. The account and project let us manage resources and access. The cluster runs the database service. A database user supplies credentials for a database connection. The IP access list controls which source networks may attempt that connection. These are related components with different purposes.

Being signed into the Atlas website does not mean a Python program has authenticated to MongoDB. Likewise, adding an IP address does not replace a database password. Network permission and database authentication are separate checks. Remember the same distinction from our earlier work with remote PostgreSQL.

For course practice, use the Free option, also called M0 in some interfaces and documentation. Select only the free deployment and do not enter a payment card. If the interface offers paid options or a required setup step is unclear, stop and ask rather than purchasing a workaround. Keep credentials private and limit access to what the practice actually needs.

Add My Current IP Address refers to the network source Atlas sees for your browser connection. A later Colab runtime can have a different outbound address, so that setting does not automatically permit Colab. We will handle the actual client path when we connect. Today's required JSON lab works without any Atlas connection.

[Sources]
- https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/
- https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/
- https://www.mongodb.com/docs/atlas/security-add-mongodb-users/
- Setup documentation checked September 8, 2026. Interface labels can change.

## Slide 31

Your assigned case is ticket 1003. Its requester is user 103 and its assignee is user 201. Its three events are 5005, 5006, and 5007. Use the Metro Support CSV files to find the names, ticket values, event types, and timestamps. You do not need to convert the other rows.

Write two complete JSON objects in separate fenced blocks inside one Markdown file. The first design keeps users, tickets, and events separately and connects them by IDs. The second embeds useful related information or uses a hybrid shape. Preserve the same required facts in both designs so that the comparison is meaningful.

Below the examples, write a short paragraph explaining how the page finds the requester and events. Then consider a changed requester name and years of additional events. Choose a sensible shape for a page that shows only the five latest events while retaining the complete history. More than one design can satisfy that requirement, provided the meaning and growth rule are clear.

This is individual work in class. No SQL, MQL, or Python execution is required. Submit only the Markdown file in Brightspace, with the two examples and the paragraph together. The lab page is the authoritative statement of which facts to retain and what to submit.

[Sources]
- Course Week 9 lab, One Ticket, Two JSON Designs.
- Metro Support synthetic CSV dataset.

## Slide 32

The paragraph on this slide demonstrates how to explain a design choice without relying on a product slogan. It begins with an identity rule: a user ID remains stable when a name changes. It then describes a specific read, the ticket page, and considers a small recent-event preview. It finishes by naming the consequences of keeping history separately and maintaining a copied preview.

Notice the difference between describing a proposal and claiming a result. This paragraph says I considered embedding and I would keep the history separately. It does not claim that the author deployed a production system or measured a performance improvement. If we later implement and test the design, we can describe the actual operations and observations.

That distinction matters in a technical handoff and in an interview. You can explain work from a class honestly and still demonstrate useful reasoning. The strongest account identifies the problem, shows the representation or code, and explains a limitation you understood.

Today your concrete artifact is two JSON examples with the same selected facts. Next week, we will use MongoDB's query language to retrieve and change documents. Knowing the shape, identity, and meaning of the fields first will make those commands much easier to understand and check.

[Sources]
- Course-created example of technical design writing. It describes a proposal, not a measured deployment.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
