# Week 9: NoSQL Models and JSON - Spoken Transcript

## Slide 1

Welcome to Week 9. This is a turning point in the course. For eight weeks we have worked with tables, keys, queries, transactions, permissions, and backups in PostgreSQL. This week we ask a new question: what happens when the way an application uses its data suggests a different arrangement?

Look at the line on the slide. A ticket can have a requester, a changing status, and years of events. That is our Metro Support ticket, the same one we have been querying all term. We already know how to store it in three tables. Today we look at other ways to store it, and at what each way makes easy or hard.

Here is the plan. On Day 1 we get the vocabulary for several database models: key-value, wide-column, document, graph, and vector. We will work through small graph and vector examples by hand. You do not need any graph theory or machine learning background. On Day 2 we learn JSON from the punctuation up, and we build two complete versions of the same ticket.

Why go slowly? Because the lab this week is just three CSV files and a text editor. No database query, no Python, no Atlas connection. I want you to understand the shape of the data before we add another query language next week. If you can explain the shape, the commands will make sense.

[Sources]
- Course textbook, Chapter 9. Metro Support is the course-created synthetic dataset.

## Slide 2

Before we go anywhere new, let's carry three relational ideas forward, because we will need all three. Look at the table, one row at a time.

First row: a person has an identity. users.user_id is the primary key. Why does that matter? Because names change. Requester 101 can change their display name and still be user 101. If we used the name itself as the identity, an ordinary name change would break every place that refers to that person.

Second row: a ticket has a requester. tickets.requester_id refers to users. That column has a specific meaning: this is the person who asked for help. In our PostgreSQL schema, a foreign key checks that the user actually exists. Keep that in mind, because a JSON file by itself does not check anything.

Third row: a ticket has many events. Each event refers to its ticket through ticket_id. Keeping events in their own table lets history grow without adding columns to the ticket row.

Now read the note at the bottom. A document design still needs identity, relationships, and rules. When we put a requester object or an event list inside a ticket, the relationship has not disappeared. It has moved. The main change is where related facts live. We still have to decide what a name means and what has to stay consistent.

[Sources]
- Course textbook, Chapters 2, 3, and 9. Metro Support CSVs and PostgreSQL schema.

## Slide 3

Where did the word NoSQL come from? The history helps, because the term covers several very different ideas.

Start at the top of the table. In 1970, Codd published the relational model. His big idea was data independence: you describe the data logically, and you do not care how it sits on disk. We have relied on that every time we wrote a SELECT without telling PostgreSQL which disk pages to read.

Second row. An earlier use of the name NoSQL, by Carlo Strozzi, was for a relational system that simply did not use SQL. That is almost the opposite of how people use the word today. So the name alone is a poor technical definition.

Then two research papers. In 2006, Google described Bigtable, a sparse distributed map for very large structured datasets. In 2007, Amazon described Dynamo, a key-value store designed around staying available. Each one answered a specific workload at a specific scale. Neither one said that every small application should stop using relations.

The later NoSQL movement put many of these alternatives under one label. Today features overlap: a relational database can store JSON, and a document database can support transactions. So when you compare systems, name the actual model and operation, not the label. And read the note at the bottom: Dynamo the research system is not the same thing as today's DynamoDB cloud service.

[Sources]
- https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
- https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
- https://sources.debian.org/src/nosql/3.1-4/nosql.lsm/
- Course textbook, Chapter 9, historical discussion and references.

## Slide 4

Here is the most important phrase for the whole week: access pattern. Read the definition at the top. An access pattern is the data an application repeatedly reads or changes. That is much more specific than saying the app needs to be fast.

Look at the two examples. Opening ticket 1001 and its latest events is one pattern. It starts from one ticket and pulls in related information. Counting every event by type is another pattern. It starts from the whole population of events, across every ticket. A shape that makes the ticket page easy can make that report harder. That is not a contradiction. It just means we have two different access patterns.

Now the diagram. It starts with the workload question and branches to five families. Key-value is exact-key lookup. Wide-column is sparse rows organized by an access key. Document is a bounded, nested aggregate. Graph is relationship paths. Vector search finds semantic neighbors. Each family makes a different operation natural.

Treat this as a starting map, not a buying guide. We also need to know how often the data changes, how fast it grows, which rules matter, and what the team can actually run. And notice the last line: one application may benefit from more than one representation. But every extra store is one more system to secure, monitor, synchronize, and recover. The benefit has to pay for that work.

[Sources]
- Course textbook, Chapter 9. Course-created model map.

## Slide 5

Let's take the families one at a time, starting with the simplest: key-value.

Look at the left box: session colon 8f21. That is the key. A browser shows up with a session token, so the application already knows the exact key. It asks for the value, and the value says user_id 101, expires_at October 20th at 19:30 UTC. That is a perfect key-value operation, because the lookup starts with a known identifier. One key in, one value out.

The note at the bottom says the value is conceptual notation. It is not a command and it is not JSON. We learn real JSON syntax on Day 2.

Now read the middle text. The request changes. An administrator wants every session belonging to user 101. We know the user ID, but we do not know that user's session keys. The arrangement that made the first lookup fast does nothing for this one. We would need a separate mapping from user IDs to session keys, an index the product supports, or a scan that could be expensive.

That is the lesson, and it comes back when we build indexes in MongoDB. Fast access by one key tells you nothing about a different access path. One more detail: an expiry field only stores a timestamp. Something still has to enforce the expiry rule, and some products offer automatic expiration to help.

[Sources]
- Course textbook, Chapter 9, Key-Value Store.
- https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

## Slide 6

Next, wide-column, in the style of Bigtable. Look at the row keys in the left column. Each key has two parts joined by a pound sign: a device name, then a timestamp. device07, then 2026-10-20 at 09:00. Why build the key that way? Because rows are kept in key order. All of device07's rows sit together, and inside that group the timestamps put the readings in time order.

Now look at the right column. The rows are sparse. The first device07 reading has only temperature, 21.4. The next one has temperature 21.6 and battery 78. device12 reports humidity, 61. Nobody had to fill in empty cells for every measurement that could exist.

Read the first line under the table. If our common question is "give me device07's readings for this hour," this key is a great starting point. It is a range over one prefix. But a cross-device battery report starts from a different attribute, battery, not device. Same data, different access pattern, and this key does not serve it directly.

Two cautions. This is an illustration, not a deployment recipe. Real key design has to think about how writes spread out and whether some keys get unusually busy. We come back to distribution and hot keys later in the course. And read the last line: wide-column storage is not the same idea as analytical columnar storage, even though both use the word column.

[Sources]
- https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
- Course textbook, Chapters 9 and 13.

## Slide 7

Now the family we will spend the rest of the course with: documents. Look at the dark box. One outer object describes ticket 1001. Its status is open. Inside it, requester is another object, user_id 101 with display name Requester 101. And tags holds a list, streetlight and safety. Don't worry about the punctuation yet. Day 2 teaches every brace and comma. For now, just look at what is inside what.

Why would we do this? If the ticket page always needs the ticket plus this small set of details, one document hands it over in a single read. But look at the title: bounded related data. That word bounded matters. Two tags is a small, predictable list. A history that grows for years is a very different thing to put inside a ticket.

Read the middle text. The nested requester is still a relationship. It points at user 101. And now there is a copy of the requester's name inside the ticket. So we have a question to answer: does that copy mean the current name, or the name when the ticket was opened? Those two meanings need different update rules, and we spend real time on that on Day 2.

Last thing. Read the bottom line. The tags are an added field, not a column copied from the CSV. Adding fields is fine, but always be clear which facts came from the source and which ones you introduced.

[Sources]
- https://www.mongodb.com/docs/manual/data-modeling/
- Course-created Metro Support example. The tags are illustrative additions.

## Slide 8

Graphs. Look at the diagram: four boxes, Portal, Identity, API, and Database, connected by arrows. In graph language the boxes are vertices, also called nodes, and the arrows are edges. On the right you see the formal notation, G equals V comma E. V is the set of vertices, four of them here. E is the set of edges, also four.

Read the note at the bottom. Each arrow means depends on. Portal depends on Identity and on API. Identity depends on Database. API depends on Database. Direction matters. The arrow from Portal to Identity does not say that Identity depends on Portal.

Two more words. Portal has an out-degree of two, because two edges leave it. Database has an in-degree of two, because two edges arrive at it. And Portal can reach Database two ways: through Identity or through API. Each route is two edges long. A connected sequence like that is called a path.

Why would anyone want a graph database? Because some questions are all about paths: which services depend on this one, which accounts share a device, what is three hops away. A graph model makes those paths an explicit part of the data. That does not mean a relational database cannot store edges; it can, with recursive queries. We are comparing convenience. And remember, this diagram shows dependencies, not a full failure model. Caches and redundancy can keep Portal running anyway.

[Sources]
- Course textbook, Chapter 9, Graph Database and the dependency example. This is a course-created directed graph.

## Slide 9

How do we actually walk that graph? The standard method is breadth-first search. Look at the table. We start at Portal, which is zero edges from itself. One edge out, we reach Identity and API. Two edges out, we reach Database. That is the whole traversal. Breadth-first means we finish every vertex at one distance before we move to the next distance. Level by level.

Now read the first note. A visited set prevents repeated visits. Both Identity and API lead to Database, but Database is one vertex, so we count it once. Why does that matter? In a bigger graph with a cycle, where A depends on B and B depends on A, a search without a visited set would go around forever.

Here is a useful property. When every edge costs the same, breadth-first search finds a path with the fewest edges. But look at the warning at the bottom. Fewest edges is not the same as least latency. If edges have weights, like milliseconds, a route with more hops can still be faster. The algorithm has to match what you mean by shortest.

Now flip the question. The database is having a problem; who might be affected? Follow the arrows backward. That gives Identity and API first, then Portal. But read the last line: a dependency path is not proof of an outage. Reachability gives you a list of candidates to investigate, not a verdict.

[Sources]
- Course textbook, Chapter 9, graph traversal discussion. The table derives directly from the four displayed edges.

## Slide 10

The last family is vectors, and this is where a lot of the current excitement is. A vector is just an ordered list of numbers. A two-dimensional vector has two numbers, like one and zero. A text embedding has many more numbers, and they come from a machine-learning model.

Look at the flow across the top. Incident text goes into an embedding model, and a numeric vector comes out. Now read the two sentences in the middle. "Lamp outside the library is flickering." "Streetlight repeatedly turns off and on." Almost no words in common, but they describe related problems. A suitable model can place those two descriptions near each other. Then a new report could pull up similar past incidents, even when people used different words.

Here is the division of labor, and it is easy to get wrong. The model makes the numbers. The database stores the vectors and retrieves nearby candidates. Creating a vector index does not train anything. And notice the word suitable. A model that works well on one kind of text may do worse on another, so we judge the results against the task instead of trusting numeric closeness blindly.

Now the bottom line on the slide: no embedding API key or vector deployment is required this week. Over the next few slides we use tiny, invented coordinates so we can see the geometry for ourselves. They are not real embeddings of these sentences.

[Sources]
- https://www.mongodb.com/docs/vector-search/
- Course textbook, Chapter 9. The incident descriptions are illustrative.

## Slide 11

Before we calculate, let's look at the picture. Both vectors start at the origin, the point zero zero at the bottom left. The green one is u. The orange one is v. They point in different directions and they have different lengths. Theta is the angle between u and v. It is not the angle to the horizontal axis.

Now the box on the right. Cosine of theta is u dot v, divided by the length of u times the length of v. Don't memorize it yet. On the next slide we compute every piece by hand. For now, focus on what it means. Look at the three lines underneath. Same direction gives cosine one. Perpendicular gives zero. Opposite directions give negative one. So cosine is a measure of direction.

Read the caption at the bottom. If you scale a vector by a positive factor, you change its length but preserve its direction. Double u, and it still points the same way. Why does that matter? Because cosine ignores length. A doubled u has exactly the same cosine with v as the original. The word positive matters: multiply by a negative number and the vector flips around, so the direction changes.

Two cautions. A negative cosine is not a negative probability, and a value near one does not prove two documents say the same thing. Also, a zero vector has no direction at all, so the formula breaks down.

[Sources]
- Course textbook, Chapter 9. Course-created vector geometry figure and elementary vector derivation.

## Slide 12

Let's do a complete calculation, every step. Look at the top line. Our query vector q is one, zero. Candidate a is ten, zero. Candidate b is one, one.

First, dot products. Multiply matching coordinates and add. For q and a: one times ten plus zero times zero. That is ten. For q and b: one times one plus zero times one. That is one.

Second, lengths. Square each coordinate, add them up, take the square root. The length of q is one. The length of a is ten. The length of b is the square root of two, because one squared plus one squared is two.

Third, divide. Read the result lines. For a: ten divided by one times ten. That is exactly one. For b: one divided by one times the square root of two, which is about 0.707. Higher cosine means more similar direction, so cosine ranks a first.

Why is a perfect? Look at it. a points along exactly the same line as q. It is just ten times farther from the origin, and cosine does not care about that. Hold on to that, because on the next slide we measure plain straight-line distance with the same three vectors and get the opposite ranking. And neither calculation will be wrong.

Last line on the slide: if a vector had zero length, the denominator would be zero, and cosine would be undefined.

[Sources]
- Course textbook, Chapter 9, Calculate a Small Example. Values are an original worked mathematical example, not measured embeddings.

## Slide 13

Same three vectors, different measure. Look at the formula at the top. Euclidean distance is the square root of the sum of the squared coordinate differences. It is the straight-line distance you would measure with a ruler.

Now the calculation. For q and a, the horizontal difference is one minus ten, negative nine. The vertical difference is zero. Square and add, eighty-one. Square root, nine. For q and b, the horizontal difference is zero and the vertical difference is negative one. Square, add, square root, one. Smaller distance means closer, so Euclidean distance ranks b first.

So which one is right? Both. They answer different questions. Cosine compares direction and throws away a positive change in length. Distance cares about direction and length together. If length means something in your data, throwing it away loses information. If length varies for reasons that do not matter to the task, cosine may be the better choice.

Look at the last box, because there is a neat connection. If you divide each vector by its own length, every vector becomes length one. For those unit vectors, distance squared equals two minus two times cosine. So on the same normalized vectors, the biggest cosine is always the smallest distance, and the exact rankings agree, allowing for ties.

The takeaway is not that cosine wins. It is that the measure has to match the representation and the question you want the search to answer.

[Sources]
- Course textbook, Chapter 9, worked distance comparison and normalization identity.

## Slide 14

Comparing a query against every stored vector gets slow at scale. That is why many vector systems use approximate nearest-neighbor methods that trade some exactness for speed. So how do we know what we gave up? We measure recall.

Look at the box. The exact top five IDs are A, B, C, D, E. The approximate search returned A, C, E, F, G. Three of the five overlap: A, C, and E. So recall at five is three divided by five, which is 0.6. How much work you save and how many neighbors you miss depend on the data, the algorithm, and the settings. A tiny example like this proves nothing about production performance.

Read the middle text carefully. Recall measures agreement with the exact retrieval target. It does not tell us whether a person found those five results helpful, or whether the incident descriptions were even accurate. People still have to judge usefulness.

Now the bottom, which connects straight back to Week 6. Similarity does not grant permission to read a private ticket. The closest match to your query might be somebody else's ticket, and being similar does not mean the current user may read it. Access controls have to apply to vector search just like they apply to a SELECT. Read the last line: embedding choice, index settings, and access controls all affect the system. A useful vector feature needs all of them working together.

[Sources]
- https://www.mongodb.com/docs/vector-search/
- Course textbook, Chapter 9. The recall calculation uses an original five-ID example.

## Slide 15

Now let's put all the families side by side. Read the table across each row: a workload, a candidate model, and a cost to investigate.

A known session token points to key-value. The cost: finding sessions when you do not have their keys. One device's ordered readings point to wide-column. The cost: other query patterns, and hot keys. One ticket with bounded details points to a document. The cost: shared facts that get copied, and arrays that keep growing. Multi-hop dependencies point to a graph. The cost: how big a traversal gets, and what an edge actually means. Similar incident descriptions point to vector search. The cost: retrieval quality, and keeping track of model versions. And shared facts with changing reports still point to relational. Its cost: joins, and schema evolution.

I want you to look hardest at the third column. Anyone can name a candidate. The design skill is naming what the choice costs, and what you would need to measure before claiming it is better.

Read the note at the bottom. These are starting points. Products often support more than one model, and a small application is often better off using a feature inside the database it already runs than adding a whole new service. A sound recommendation has three parts: the operation, the candidate, and the cost it brings.

[Sources]
- Course textbook, Chapter 9, model comparison and access-pattern discussion.

## Slide 16

Let's use this vocabulary right now. Read the prompt. The support portal has two needs: a ticket page, and a report of event counts. Your job: choose a useful representation for the ticket page, then explain one consequence for the report or for changing a name. Do this on your own, in your notes. There is no separate submission.

Let me show you what a good answer sounds like. Say you choose a document that holds the ticket, the requester's name, and a few recent events. Great: the page gets everything together in one read. Now add the cost. If that requester name means the current name, then when the person changes it, the copy has to change too. And if you put every event inside every ticket, the event-count report has to dig through all those nested arrays, and the documents keep growing.

A relational answer is completely fair too. Keep users, tickets, and events separate. Each user has one authoritative row, and reports stay flexible. The cost there is that the page has to put the pieces back together with the right queries and indexes.

Read the last line on the slide. Keep the relational option available and justify any additional store. I am not looking for a complicated multi-database architecture. One clear choice, with one tradeoff explained, shows more understanding than a list of product names.

[Sources]
- Course-created design exercise based on Metro Support and Chapter 9.

## Slide 17

Welcome to Day 2. In our first meeting this week we compared database models by what an application reads and changes. Today we make the document idea concrete by writing JSON ourselves.

Look at the line on the slide. The same facts can appear in different document shapes. That is the whole day in one sentence, and it is why there will be more than one right answer in your lab.

Here is the plan, from the list. First, syntax and types: the six kinds of values and the punctuation that holds them together. Then two worked designs for ticket 1001. One keeps users, tickets, and events in separate arrays connected by IDs. The other puts the related facts inside the ticket. Both hold exactly the same facts, so we compare the arrangement and not different information.

Then a quick orientation. I will show you GitHub's browser editor, which can hold your Markdown explanation and your JSON in one file. And I will walk through Atlas, separating the account, the database user, and the network access list. Neither tool is needed to reason about a JSON shape.

Then the individual lab. You take a different ticket, write two designs, and explain the tradeoff. No SQL, MQL, or Python today. Why? Because next week we start running database commands, and I want them to operate on shapes you can already explain.

[Sources]
- Course Week 9 guide and individual CSV-to-JSON lab.

## Slide 18

JSON stands for JavaScript Object Notation. The notation grew out of JavaScript, but JSON is not tied to JavaScript. Read the first line under the example: JavaScript, Python, and other languages can exchange the same text. A Python service can send JSON, a browser can read it, and each one turns it into its own kind of values.

Look at the timeline. In 2006, RFC 4627 documented JSON. In 2014, RFC 7159 revised the interoperability rules. In 2017, RFC 8259 became the Internet standard. Why all the revisions? Because when two different programs exchange data, they need to agree exactly on what it means. Standards are how that agreement gets written down.

Now the small example: ticket_id 1001, status open. The same grammar can nest objects and arrays, and read the second line, objects and arrays directly express nested API responses. That is why JSON shows up in APIs, logs, and configuration. It is text, so you can read it, and almost every language has a parser. That still does not make it ideal for every job.

Now read the bottom line, because it is the boundary for the whole week. JSON describes data. It does not execute a query or provide a database. It does not store anything durably and it does not check a foreign key. Keep those layers apart, and later it will be clear what Atlas, MongoDB, and a Python driver each do.

[Sources]
- https://www.rfc-editor.org/info/rfc4627/
- https://www.rfc-editor.org/info/rfc7159/
- https://www.rfc-editor.org/info/rfc8259/

## Slide 19

JSON has six kinds of values, and that is all. Look at the table, one row at a time.

An object holds named members, like status colon open, inside curly braces. An array holds an ordered list of values, like streetlight and safety, inside square brackets. A string is quoted text, like open in double quotes. A number is a numeric value, like 1001, with no quotes. A Boolean is true or false. Notice the table says two literals in one value kind. True and false are two spellings of the same kind, so we count six kinds, not seven. That matches the textbook. And null is its own explicit value.

A few rules worth knowing. Inside an object, every name must be a string. Don't rely on the order of members in an object to mean anything. If order matters, like an event history you want shown in sequence, use an array, because an array keeps its order. An array can technically mix kinds, but an application will usually want every element to have the same structure.

Now read the line at the bottom. Any JSON value can be the top level. A single number is a complete JSON text. But our lab deliberately uses one object at the top of each design, because that makes the two designs easy to package and compare. That is an assignment choice, not a JSON rule.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- Course textbook, Chapter 9, JSON Has Six Value Kinds.

## Slide 20

Let's read a real example, piece by piece. The outer curly braces make one object. Each line inside is a name, a colon, and a value.

ticket_id is the number 1004, no quotes. subject is Broken bench slat, a string, so it is in double quotes. status is new, also a string. Now look at assignee_id. Its value is null, with no quotes. That matters. If I wrote null inside quotes, it would be a string of four letters, not an explicit null.

Then tags. It opens with a square bracket and closes with one, so it is an array. Inside are two strings, parks and bench, with a comma between them.

Now look at the punctuation box. Curly braces enclose an object. Square brackets enclose an array. A colon connects a name to its value. A comma separates neighbors. And notice where the commas are not: there is no comma after the last member, tags. That is the mistake people make most often.

Read the note at the bottom. Names and strings use double quotes, and indentation shows containment. Indentation is for human readers. It makes it easy to see what is inside what, but the braces and brackets are what actually define the structure. And the tags are an illustrative addition to ticket 1004, not a column from the CSV. In your lab, keep the required source facts first, and be clear about anything you add.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- Metro Support ticket 1004. Tags are illustrative additions.

## Slide 21

Here is a repair you will make yourself, probably more than once. Look at the first line: a curly brace, then status and open in single quotes, then a comma, then the closing brace. It looks like a Python dictionary, and Python would accept it. JSON will not.

Read the reasons. There are two separate errors. First, single quotes. JSON names and strings must use double quotes. Second, the comma after the final member. JSON does not allow a trailing comma. Now look at the repaired line. Double quotes, no final comma. Valid.

Why point out that there are two? Because when a parser fails, it reports the first place it got stuck. Fix that one and it may stop at the next. One error message does not mean everything else is fine.

Now the last box. Comments are not allowed in standard JSON. Neither are NaN or Infinity. And the number 01, with a leading zero, is not a valid number. If an identifier really is spelled zero one, write it as a string in quotes.

Read the last line too. A permissive parser may accept extensions. Python's default json parser accepts NaN and Infinity, for example. So "my parser accepted it" does not prove the data is portable to other programs. Use standard syntax and unique names. And never use eval to read JSON text you don't trust. Parsing data and running code are very different risks.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- https://docs.python.org/3/library/json.html#standard-compliance-and-interoperability

## Slide 22

These four little examples look almost the same, and they mean four different things. Look at the table.

An empty object, just two braces, has no assignee property at all. The second one has assignee_id, and its value is null. The third has an events array with nothing in it. The fourth has estimated_cost set to the number zero.

Why fuss over this? Because an application has to decide what each one means, and JSON does not decide for you. Read the first line at the bottom. One application might treat a missing assignee and a null assignee as the same thing. Another might use missing to mean "we didn't ask for that field" and null to mean "we asked, and nobody is assigned." You have to read or define that contract.

The empty events array has the same problem. Read the second line. It tells you what this response contains. It does not tell you whether the ticket really has no history, whether a filter removed every event, or whether the response just left history out on purpose.

And zero is a number, not a missing amount. An estimated cost of zero might be a real estimate. No estimated_cost field at all might mean nobody has made an estimate yet. These differences decide which documents match a filter and what an update changes. That is exactly where they will matter when we start writing MQL next week.

[Sources]
- Course textbook, Chapter 9, Missing, Null, Empty, and Zero Are Different.

## Slide 23

Look at the example at the top: opened_at, and then a value in quotes. That value is a JSON string. It follows an agreed timestamp format, and the Z at the end means UTC. But JSON itself has no date type. To JSON, that is just text. It does not convert it to a date, and it does not check that the date is real.

Now read the middle text. MongoDB does not store JSON text. It stores BSON, which supports additional types, including Date and ObjectId. So who decides whether that timestamp becomes a real Date? The driver or the import step that sends the data. If you insert plain text, do not assume MongoDB quietly turns every date-looking string into a Date. There is also a format called Extended JSON for writing BSON types as JSON text, and we will meet it with real stored documents. In today's lab, dates stay as strings, so you can focus on structure.

Two more rules, in the last box. Use unique member names inside an object. If a name appears twice, different parsers can disagree about which value wins. And keep IDs as strings when their exact spelling matters, like a code with a leading zero, or a very large number another language cannot represent exactly.

Last line: a valid document can still violate the application's data contract. Valid syntax is only the first check. The application still needs meaningful names, expected types, and rules about acceptable values.

[Sources]
- https://www.rfc-editor.org/info/rfc8259/
- https://www.mongodb.com/docs/manual/reference/bson-types/
- Course textbook, Chapter 9.

## Slide 24

Now the worked example. Everything for the next few slides comes from these rows of the Metro Support CSVs. Look at the table.

From users.csv: user 101 is Requester 101, and user 201 is Agent 201. From tickets.csv: ticket 1001, Streetlight dark near bus stop, status open, requester 101, assignee 201. From ticket_events.csv, two events for this ticket: 5001, created, February 1st at 23:10 UTC, and 5002, assigned, February 2nd at 14:05 UTC.

Read the first line at the bottom. Both upcoming examples preserve these facts: the ticket's values, both users' IDs and names, and both events' IDs, types, and timestamps. Why so strict? Because if one design quietly dropped an event, it would look simpler just because it lost data. That is not a fair comparison. We want to compare the arrangement, not the amount of information.

Other CSV columns are left out on purpose. A user's email address, for example, is not needed to compare two ticket-page shapes. Leaving out an out-of-scope column is a decision. Dropping a fact you promised to keep is a mistake.

And the last line: the student lab uses a different ticket, 1003, with three events. I am showing you the method on 1001. You will apply it yourself to 1003, so the worked example does not do your lab for you.

[Sources]
- course/datasets/metro_support/users.csv
- course/datasets/metro_support/tickets.csv
- course/datasets/metro_support/ticket_events.csv

## Slide 25

Here is the first design: referenced. Look at the whole thing first. It is one JSON object, and inside it are three arrays: users, tickets, and events. Read the note at the bottom. One JSON object packages three arrays, and this file is not yet a MongoDB database. It is a package of text. It does not create three collections, and we are not importing it anywhere yet.

Now trace the connections. In users, there are two records: 101, Requester 101, and 201, Agent 201. In tickets, ticket 1001 has requester_id 101 and assignee_id 201. Those are numbers, not names. So to show the requester's name on the page, you go find the user whose user_id is 101. That is a lookup, just like a join.

Now the events. Each one carries ticket_id 1001. That field is what ties the event to its ticket. Event 5001 is created, event 5002 is assigned, and both timestamps are there. Nothing is replaced with dots. Both promised events are present.

Why choose this shape? It looks a lot like our three CSV tables. Each user's name appears exactly once. If Requester 101 changes their display name, we update one user record instead of every ticket-shaped copy. The cost is on the read side. The ticket page has to gather facts from three places and put them together. Hold that thought, because the next design flips that tradeoff.

[Sources]
- Course-created JSON representation of Metro Support ticket 1001 and events 5001 and 5002.
- Course textbook, Chapter 9, referenced design discussion.

## Slide 26

Here is the same ticket, embedded. Look at how the shape changed. The ticket itself is now the outer object: ticket_id 1001, the subject, status open. Requester is a nested object, user 101, Requester 101. Assignee is a nested object, user 201, Agent 201. And the events array, 5001 created and 5002 assigned, now lives inside the ticket.

Did you notice what is missing from each event? ticket_id. We dropped it, because the containing ticket already says whose events these are. Read the first note at the bottom: the containing ticket identifies the events' owner. Each event_id still identifies its event, though. If we ever copy an event somewhere else, we have to bring the ticket context along with it.

Now compare with the last slide. Same ticket, same subject, same status, same two users, same two events, same timestamps. The information is identical. Only the arrangement changed.

So what did we buy? The ticket page gets everything in one document read. No lookups. What did we pay? Read the second note. The document carries copies of the two names. If user 101 appears in many ticket documents, and those copies mean the current name, one name change becomes synchronization work across all of them. And the events array needs a growth rule. Two events fit comfortably here. Years of events inside one document is a different decision.

[Sources]
- Course-created alternate JSON representation of the same Metro Support facts.
- https://www.mongodb.com/docs/manual/data-modeling/

## Slide 27

That copied name deserves its own slide, because there is more than one right answer. Look at the table. Each row is a different meaning for the copied name, and each meaning has a different consequence when Requester 101 changes it.

First row: the copy means the current display name. Then every copy must eventually match the authoritative user record. Updating the one user record does not update the copies by itself. Something has to, under a consistency rule you have written down.

Second row: the copy means the name when the ticket opened. Then keeping the old name is correct, deliberately. It is history. Give the field a name that says so, like requester_name_at_open, so nobody updates it by mistake later.

Third row: keep only the user ID, no copied name. Then there is nothing to go stale. The cost is that the read has to look up the authoritative user record to get the current name.

Now read the two lines at the bottom. A stale current name is an inconsistency. A documented historical snapshot preserves a different fact. Those two can contain the exact same text, and one is a bug while the other is correct. The difference is what you said the field meant before the change happened. You can't relabel a stale value as history after the fact. Your lab paragraph should make that kind of reasoning visible.

[Sources]
- Course textbook, Chapter 9, Snapshot Plus Reference and Flexible Schema Is Still a Schema.

## Slide 28

What about a ticket that piles up years of history? Here is a hybrid design. Look at the two boxes. On the left, the ticket document holds the ticket ID and status, plus at most five recent events, for a fast ticket-page preview. On the right, separate event records, each linked by ticket_id, hold all retained events. That separate history can grow on its own and feed reports.

Why five? It is a deliberate application rule. It keeps the page small. But careful: the limit is for the preview, not for the history. When the sixth event arrives, the preview drops its oldest entry, and the separate history still keeps that event according to the retention rules. The bound must never turn into an accidental deletion policy.

Now read the bottom note, because convenience is never free. A copied recent-event list needs a refresh rule. What should a reader see when a new event has been written but the preview has not caught up yet? A version or a timestamp can make that visible.

And the last line: this design does not make changes across separate documents automatically atomic. Writing the event and updating the preview are two writes, and choosing a hybrid shape does not coordinate them for you. Later lessons cover the actual database guarantees. For today's lab, just name that boundary and its consequence. You don't need to build a synchronization service.

[Sources]
- https://www.mongodb.com/docs/manual/data-modeling/
- Course textbook, Chapter 9, Worked Example: Compare Two Ticket Shapes.

## Slide 29

Now let me show you where you will write the lab. GitHub can edit text right in your browser, with no Git installed. Read the path at the top. In your own repository, choose Add file, then Create new file. Name it week_09_json_models.md. The dot md says this is a Markdown file.

Look at the example in the middle. A Markdown heading, Referenced design. Then three backticks and the word json. That opens a code block. Then the JSON itself: ticket_id 1004, assignee_id null. Then three backticks again to close it. The backticks belong to Markdown. They are not part of your JSON. And your explanation goes below the JSON block, outside the fences.

Now read the bottom carefully, because people get this wrong. Preview checks the Markdown display. It makes the JSON look nice in a code box. Commit changes saves the text in your repository's history. Neither step validates the JSON syntax, and neither checks that your facts match the CSV. That part is your job, so reread your quotes, commas, and brackets before you submit.

Then download the file and submit it to Brightspace. A public repository is not required, and if GitHub is unavailable, any plain text editor can make the same Markdown file. Use only the synthetic course data, and never put a password or connection string in the file or in your commit history.

[Sources]
- https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files
- Course Week 9 lab submission instructions.

## Slide 30

Next week we connect to MongoDB Atlas, so let's get the pieces straight today. Look at the table. Four components, four different jobs.

The Atlas account and project are how you manage the cloud deployment. The free cluster runs the actual database service, with free-tier limits. A database user is what authenticates a database connection. And the IP access list permits a source network to attempt that connection.

Why separate them so carefully? Because being signed into the Atlas website does not mean your Python program is authenticated to the database. And adding your IP address does not replace a database password. Network permission and authentication are two different checks. You saw the same split in the Week 6 triage table: network unreachable is a different failure from password authentication failed.

Read the instructions in the middle. Choose Free, which some screens call M0, and only the access your practice needs. Do not enter a payment card, and never publish your credentials. If a screen offers a paid option or a step is unclear, stop and ask me instead of paying your way around it.

One trap to know about. Add My Current IP Address adds the address Atlas sees from your browser. A Colab runtime can have a different outbound address, so that setting does not automatically let Colab in. We will handle that when we connect. And look at the last line: today's JSON lab needs no cloud connection at all.

[Sources]
- https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/
- https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/
- https://www.mongodb.com/docs/atlas/security-add-mongodb-users/
- Setup documentation checked September 8, 2026. Interface labels can change.

## Slide 31

Here is your lab: one ticket, two JSON designs. Read the input at the top. Your case is ticket 1003. Requester 103. Assignee 201. Events 5005, 5006, and 5007. Open the Metro Support CSVs and find the names, ticket values, event types, and timestamps for exactly those rows. Ignore everything else.

Now the work. In one Markdown file, write two complete JSON objects in two separate fenced json blocks. The first is a referenced design, with users, tickets, and events arrays connected by IDs, like slide 25. The second is embedded or hybrid, with useful related information inside the ticket, like slide 26. Both designs must keep the same required facts. If one design is missing a fact, the comparison stops being fair.

Below the JSON, write a short paragraph. How does the ticket page find the requester and the events in each design? Then, what happens when the requester changes their name, and when the ticket collects years of events? Keep all three events in both designs, and describe what gets harder. You don't have to solve the growth problem yet. Next week brings a new requirement: a page that shows only the latest two events, while keeping all history and contact details in one place.

This is individual work in a text editor, with no SQL, MQL, or Python. Submit week_09_json_models.md to Brightspace, with both examples and the paragraph in that one file. The lab page is the authoritative list of facts to keep.

[Sources]
- Course Week 9 lab, One Ticket, Two JSON Designs.
- Metro Support synthetic CSV dataset.

## Slide 32

Let's finish with how to explain a design decision, because that skill outlasts any one product. Read the paragraph on the slide with me.

It starts with an identity rule: I kept user IDs so a name change would not change identity. Then it names a specific read: for the ticket page, I considered embedding a small set of recent events. Then a consequence: I would keep the complete history separately because it continues to grow. And it ends with the cost: a recent-event copy would need a refresh rule, so readers could tell an up-to-date preview from an older one. Rule, read, consequence, cost. That is the pattern I want in your lab paragraph.

Notice the wording, too. It says I considered, and I would keep. It does not say I deployed this and it got faster. Nobody measured anything, so the paragraph does not claim a result. That honesty matters in a technical handoff and in a job interview. You can describe class work truthfully and still show strong reasoning. The best answers name the problem, show the representation, and explain a limitation you understood.

Read the bottom of the slide. The lab practices this reasoning with concrete JSON: two examples holding the same facts. Next week we use MQL, MongoDB's query language, to retrieve and change documents. Because you already know the shape and meaning of every field, those commands will be much easier to read and to check.

[Sources]
- Course-created example of technical design writing. It describes a proposal, not a measured deployment.

## Slide 33

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Same facts, two shapes (1:16); Strict JSON, from the punctuation up (1:20); What embedding costs over time (1:21). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 9 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
