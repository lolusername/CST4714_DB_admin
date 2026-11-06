# Week 10 Basic MQL and Document Modeling

This transcript follows the Week 10 presentation in order. Use the numbered headings to find each explanation. Sections marked Reference (not spoken) provide sources for review.

## Slide 1

MongoDB stores data as documents. A document brings related fields together, and a collection holds many documents. Today we will learn how a query selects documents and how a write changes them.

We will use a small support-ticket example. A ticket is a request such as fixing a streetlight. Its status describes the workflow, and its priority describes importance. The numbers on the slides identify the example records. Every worked example includes the information needed to understand its result.

The first part of the week covers reading and changing documents in Python. The second part introduces creation in the MongoDB shell and then asks which related facts belong in one document. The lab follows the explanation and supplies its own setup instructions.

## Slide 2

The familiar SQL ideas still help. FROM chooses a source. WHERE decides which rows qualify. SELECT chooses output columns, and ORDER BY puts results in order.

In this MongoDB example, tickets names a collection. A filter is a structured set of conditions, such as status equals open. A projection chooses which fields the result contains. A one includes a field, and the zero for _id hides that identifier from the returned view.

Those choices do different jobs. A filter changes which documents qualify. A projection changes what we see about each matching document. Neither changes the stored data. Sorting and limiting then control the order and amount of output.

Python represents the filter and projection as dictionaries. Later, the MongoDB shell uses JavaScript object notation for the same underlying ideas.

## Slide 3

MongoDB is the database software. Atlas is a managed service that runs MongoDB in the cloud. A program can also communicate with a MongoDB deployment hosted elsewhere.

Within a deployment, a database organizes named collections, and each collection stores documents. A client program sends requests to the service. PyMongo is the library a Python program uses to communicate with MongoDB. Mongosh is an interactive shell for the same purpose.

The screenshot shows an Atlas administration screen. Signing into that website and connecting a program to the database are different activities. The website manages the service. The database connection authenticates a database user and applies that user's permissions.

That distinction explains why being able to see a cluster in a browser does not, by itself, establish that an application can read or write its data.

## Slide 4

A database connection joins a client program to a service. Four questions help explain what that connection requires. Where is the server? Can the client reach it? Which database user is the program acting as? What may that user do?

A notebook is a useful example of a client. The browser displays the page, but a runtime executes the Python code. When the runtime is hosted remotely, the database sees a connection from that remote computer.

Network reachability, authentication, and authorization describe different stages. A reachable service can still reject incorrect credentials. A recognized user can still lack permission to write a collection. TLS protects the connection in transit.

These concepts apply to a notebook, a website backend, or another application. The lab handout provides the actual connection steps when it is time to practice.

## Slide 5

The same operation looks a little different in different programming environments. Day 1 uses Python and PyMongo. Day 2 uses mongosh, the MongoDB shell.

Python writes a null value as None and Boolean values as True and False. The shell uses null, true, and false. PyMongo uses find_one and modified_count where the shell uses findOne and modifiedCount. The spelling changes, but the purpose stays the same.

MongoDB stores BSON, which supports types beyond ordinary JSON. A date is a good example. A quoted timestamp is text. A typed date represents a time value that date operations can use. The table shows one way to construct each.

In the Python examples, tickets stands for a PyMongo collection. The example's displayed source records tell us what is in that collection for that particular question.

## Slide 6

This table shows six illustrative support tickets. Each row gives us the information we need to distinguish two ideas: importance and workflow state.

Priority says how important the request is. Status says where it is in the process. The urgent water request is already resolved. The medium-priority lighting request is still in progress. A queue of unfinished work therefore needs a status condition, even when priority is also relevant.

The ticket numbers simply let us refer to specific rows. For example, 1005 labels a resolved sanitation request. Its high priority does not turn it back into unfinished work.

This is why the application question comes first. A report about urgent requests and a queue of work still to do can reasonably return different records from the same collection.

## Slide 7

Here is one complete account document. The outer braces hold named fields. Owner and status contain strings. Balance contains a number. The field names state what those values mean to the application.

The _id field identifies the document within its collection. This example supplies a string, account-7. MongoDB permits other identifier types and ordinarily generates an ObjectId when an insert does not supply _id. A person's name usually makes a poor identifier because different people can share a name and names can change.

A collection can hold many account documents. Flexible structure allows different document shapes, but the application still needs clear meanings and appropriate validation rules. MongoDB does not infer the meaning of balance or status from their names.

## Slide 8

Documents can contain more than simple values. Address is a nested object. Its city and country fields belong together. The path address.city names the city inside that object.

Tags is an array of strings. It holds the labels student and savings. Events is also an array, but each item is an object with its own fields. In the shown event, type is opened and actor_role is resident.

That difference matters when we query. Looking for one tag means looking for a value among the array items. Looking for several facts about one event means keeping those facts attached to the same item. Later examples show how to express that condition.

Nesting can make related facts convenient to read together. It also raises design questions about how large the document will grow and which facts change independently.

## Slide 9

These documents show three different stored shapes. Ticket 1 contains an assignee field with a null value. Ticket 2 leaves the field out altogether. Ticket 3 stores the name Ari.

The difference between an absent field and a present null value can matter to the application. An omitted field may mean the information was never collected. A null value may be an intentional statement that there is no assigned person. The application has to define that meaning.

MongoDB's equality filter for null matches both the null case and the missing case. In the shown data, assignee equals null therefore matches tickets 1 and 2. An additional existence condition can distinguish the cases. In Python, the corresponding null value is written None.

Reference (not spoken): MongoDB Manual, Query for Null or Missing Fields, https://www.mongodb.com/docs/manual/tutorial/query-for-null-fields/

## Slide 10

The source has two documents. One is open and high priority. The other is resolved and urgent. The query asks for an open document whose priority is either high or urgent.

MongoDB combines these two field conditions with AND. The dollar-in operator gives the allowed priority values. Ticket 1001 passes both conditions. Ticket 1003 passes the priority condition but fails the status condition, so it does not qualify.

The second argument is the projection. It returns ticket_id and status and hides _id. Priority helps select the document even though the result does not display it.

The result shown below the code follows directly from the two displayed source documents. The source collection keeps all its fields, including priority. A projection changes the returned view.

## Slide 11

The four source rows include the opening dates, so we can explain the order without looking elsewhere. Ticket 1003 is resolved and fails the filter. The remaining tickets opened on February 1, 2, and 4.

The minus one sorts opened_at in descending order, placing the newer date first. The ascending ticket number supplies a stable tie-break when opening times are equal. Limit two keeps at most two results. That gives 1006 followed by 1002. Ticket 1001 qualifies but falls beyond the two-result limit.

Find returns a cursor, an object the program reads to obtain the matching documents. A loop or a conversion to a list can consume it. Repeating a consumed query normally means asking for a new cursor.

The opening values here are stored dates, abbreviated on the slide for readability. Sorting and limiting affect the result, while all four source documents remain stored.

## Slide 12

This diagram includes the source records and shows the purpose of each query component. The active-status filter keeps open ticket 1001 and in-progress ticket 1006. It excludes resolved ticket 1003.

Projection then displays just the ticket number and status. The stored documents retain their other fields. Finally, descending ticket order places 1006 before 1001.

The diagram separates logical tasks to make the query easier to explain. It does not claim that the database physically executes every query in this illustrated order. The important distinctions are which documents qualify, which fields the application receives, and how the results are ordered.

## Slide 13

Both source documents are visible. Ari requested ticket 1001, and Bo requested ticket 1005. Both tickets carry the safety tag.

The first filter uses requester.name. The dotted path reaches the name inside the requester object. Only Ari's ticket qualifies, so that query returns 1001.

The second filter asks whether tags contains the value safety. MongoDB can match that scalar value against the array's elements. Both shown tickets contain it, so the result contains 1001 and 1005.

These queries illustrate different conditions over the same two documents. A nested object lets us address one named field. An array lets a single field hold several values that a query can inspect.

## Slide 14

The table shows the ticket's two events. Event 5001 records a resident creating the ticket. Event 5002 records an agent assigning it.

The filter asks for created somewhere in events.type and agent somewhere in events.actor_role. The ticket satisfies both conditions because those values exist in its array. They occur in different events.

That is enough for separate dotted conditions to match. It is not enough to establish that an agent created the ticket. Neither row says that. The next example puts both requirements inside a same-event condition.

Reference (not spoken): MongoDB Manual, $elemMatch, https://www.mongodb.com/docs/manual/reference/operator/query/elemmatch/

## Slide 15

The complete events array is shown above the query. The first event combines created with resident. The second combines assigned with agent.

Dollar-elemMatch asks whether one array item satisfies every condition inside it. This query requires created and agent together. Neither event has that pair, so the result is empty.

The same shown data also explains a positive example. If the type condition were assigned while the role stayed agent, the second event would meet both requirements and the ticket would qualify.

This is elemMatch in a filter. It selects documents. It does not automatically remove other events from a returned events array. Selecting documents and shaping their displayed content remain separate choices.

Reference (not spoken): MongoDB Manual, $elemMatch, https://www.mongodb.com/docs/manual/reference/operator/query/elemmatch/

## Slide 16

The illustration compares the same two events under two filters. Created belongs to event 5001. Agent belongs to event 5002.

Separate dotted conditions can take their matching values from those different events. Dollar-elemMatch requires one event to satisfy both conditions. Neither row can do that for created and agent.

The event numbers are labels for the two visible rows. The conclusion depends on the combinations of type and actor role within each row.

## Slide 17

An update needs a target and a change. This example starts with one document whose ticket_id is 1099, whose status is new, and whose events array is empty.

The first argument to update_one is the filter. It identifies the shown ticket. The second argument describes the change. Dollar-set puts in_progress into the status field.

After the operation, the ticket number and empty events array remain. Updating selected fields preserves fields that the operation does not mention. Replacing the whole document is a different operation and can remove fields omitted from the replacement.

The number 1099 simply identifies this example ticket. The example assumes one document with that ticket number. An application can use a unique identifier or a unique index when it needs that guarantee.

## Slide 18

This slide states the starting record above the command. Its status is new, and it has no assignee field. The update targets that ticket and sets status to in_progress and assignee_id to 202. Here 202 is a staff identifier.

The first request finds one document and changes it, so the counts are one matched and one modified. The counts describe documents, even though the operation changed two fields.

Repeating the identical request leaves the filter unchanged. It still finds the ticket. The requested values are already stored, so the counts become one matched and zero modified.

A zero modified count therefore needs interpretation. It can mean the document already held the requested values. The matched count and a read-back help distinguish that situation from a filter that found nothing.

## Slide 19

The before state, first update, and repeat all appear in this picture. The ticket begins with status new and no assignee. The first set operation changes both fields.

Repeating the same request still matches the ticket because its identity has not changed. It makes no further modification because the requested values are already present. Matched stays one while modified becomes zero.

This is an example of a repeat that leaves the stored state unchanged. An append or an increment can behave differently, so the operation itself matters when we reason about retries.

## Slide 20

The current document at the top already has status in_progress. The filter asks for the same ticket number and status new. Both conditions must hold.

The ticket number matches, but the status does not. No document satisfies the complete filter, so the operation reports zero matched and zero modified. The status stays in_progress.

This differs from the repeated set example. There, the document qualified but already contained the requested values. Here, the current state prevents the write from qualifying at all.

A condition on the expected current value can protect a state transition when a user acts on an older view. The application must then decide how to handle the failed match, such as reading the current record again.

Reference (not spoken): MongoDB Manual, Atomicity and Transactions, https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 21

The diagram places the stored state beside the update's required state. The saved ticket is in_progress. The write requires new. The mismatch prevents the requested change to resolved.

The ticket still exists. A conditional update can match zero documents because one of its conditions no longer holds. That makes a zero match useful application evidence rather than enough information to diagnose a connection problem.

The appropriate response depends on the application. It may reload the record and let the person decide based on its current state.

## Slide 22

The source document begins with an empty events array. Dollar-push appends the event object shown in the command. Its event_id, 5999, identifies the event in this example.

The filter also says that events.event_id must not equal 5999. The dollar-ne condition therefore allows the first append when the event is absent. That request matches and modifies one document.

Afterward, the array contains event 5999. Repeating the same request fails the filter and reports zero matched and zero modified. The array keeps one copy.

An ID field inside an array does not create uniqueness by itself. This particular write protects its repeat through the filter. Other writers need compatible rules if the application requires the same protection.

## Slide 23

The source collection contains exactly the two displayed tickets. The target filter identifies 1099. Delete_one removes one matching document, so the first count is one.

A read using that target then returns None in Python. Ticket 1001 remains because it did not match the target. A repeat of the same deletion reports zero because no matching document remains.

Delete_one and delete_many differ in scope. One removes a single match. Many removes every match. An empty filter matches every document, so neither method should be interpreted without reading its filter.

A preview read can help explain the intended target, but it is a separate request. It does not lock the record against another writer between the read and the deletion.

## Slide 24

The lecture has introduced the concepts that Lab 1 practices. The handout and notebook provide the full dataset, connection choices, and setup steps.

The lab asks for an active lighting and sanitation queue, an explanation of array matching, and evidence from repeated and conditional updates. The small examples in the lecture explain how to reason about those operations. The lab's own records determine its actual results.

Submit the completed notebook with its short results record. Use the handout's guidance for recovery and cleanup. I will help with the workspace and commands during the lab.

## Slide 25

CRUD names four basic operations: create, read, update, and delete. The first part of the week explained queries and changes to existing documents. Now we will make the creation step explicit.

Imagine Ari opens a new account. The application submits an account document. MongoDB acknowledges the write and supplies an identifier. A separate read then retrieves the stored document so the application can inspect its values.

These examples use mongosh, the MongoDB shell. The source data, command, and result appear together. After the examples, the lab provides a workspace for practicing the same ideas.

## Slide 26

The accounts collection starts empty. The document between braces contains two facts: owner is Ari and status is open. InsertOne adds that one document to the collection.

The shell stores the response in a variable called saved. The displayed response includes acknowledged, which is true, and insertedId, which identifies the inserted document. The long hexadecimal value is an example ObjectId. MongoDB generates different IDs for different inserts.

An acknowledgment tells us about the write request. It does not display the account's stored owner and status. The next example uses the returned identifier to read that account.

Reference (not spoken): MongoDB Manual, insertOne, https://www.mongodb.com/docs/manual/reference/method/db.collection.insertone/

## Slide 27

FindOne asks for one document matching a filter. This filter uses the insertedId from the preceding response as the stored document's _id. The result includes that same ID, owner Ari, and status open.

The read-back shows the stored values as well as the identifier. This connects a write response to the document the application wanted to create.

InsertMany accepts an array of documents. The shown array contains one account for Bo and one for Cam. Starting with Ari's one stored account, one successful call adds two documents and leaves three accounts in total.

The difference is the input shape: one document for insertOne, an array of documents for insertMany. Both are create operations.

References (not spoken): MongoDB Manual, findOne and insertMany, https://www.mongodb.com/docs/manual/reference/method/db.collection.findone/ and https://www.mongodb.com/docs/manual/reference/method/db.collection.insertmany/

## Slide 28

The source ticket is shown in the first comment: its status is open and its events array is empty. The filter requires that ticket number and the open status.

One update changes the status to in_progress and appends event 5099. Atomic means those changes apply together as one document write. The operation does not leave just one of its two changes committed in that document.

The first successful write changes the status. A repeated request then fails the open-status condition, producing zero matched and zero modified without adding the event again.

The guarantee here covers one document. If status and history were in separate documents, the application would need a suitable way to coordinate the writes, such as a transaction when the requirements call for it.

Reference (not spoken): MongoDB Manual, Atomicity and Transactions, https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 29

A current fact and a historical snapshot answer different questions. Current contact information tells the application how to reach a person now. A name-at-opening field tells it what name was recorded when a ticket began.

A shared user document gives current contact details one authoritative home. Correcting an email address there changes one record. A ticket can retain requester_id to identify the related person while that person's contact details change.

A historical snapshot intentionally keeps an older value. That can be useful when the application needs to reconstruct what it knew at an earlier time. The field name and rules should make that historical meaning explicit.

A copied email field without a refresh policy is ambiguous. Readers may assume it is current. References also require application rules for missing or deleted related records because MongoDB does not automatically enforce a relational foreign key.

## Slide 30

The first document describes a ticket. The second describes an event and includes the ticket number it belongs to. The event can grow the history by becoming another document in the history collection.

This arrangement leaves the parent ticket's size unchanged as events accumulate. The application retrieves related history by querying for the ticket number. It does not need to append every event ID to an ever-growing list on the ticket.

The timestamp in this JSON sketch is readable text. A production model can store a typed BSON date for chronological operations. The following worked query assumes typed dates.

A reference records a relationship. Fetching the related documents, indexing the query, and handling missing relationships are additional design responsibilities.

## Slide 31

All records needed for this example are shown. The ticket is open and identifies requester 101. The matching person is Ari. The history contains three events for this ticket, at nine, ten, and eleven on the same day.

The history query filters by ticket number. It sorts event_at descending, so eleven comes before ten and nine. Event_id supplies a descending tie-break if two times are equal. Limit two returns events 5003 and 5002.

The page can display open, Ari, and those two events. Event 5001 remains in storage. Limiting a read does not delete older history.

The page obtains the ticket, the related person, and the selected history. Separate reads are straightforward, but if the page requires all three to reflect one coordinated state, that consistency requirement needs an explicit design.

## Slide 32

The table compares what grows when events arrive. If every event is embedded, the ticket document grows. That can make a combined read and one-document update convenient, but a long-lived history can become large.

A BSON document has a 16 MiB maximum size. That is a hard ceiling, and documents can become inconvenient long before reaching it. The limit does not translate into a fixed number of events because event sizes vary.

Separate history documents let the number of events grow while the ticket stays bounded. The page retrieves the history it needs. A hybrid can also keep a small recent-events copy on the ticket, but that copy needs refresh rules and an explanation of what happens when it is stale.

Reference (not spoken): MongoDB Manual, BSON Document Size, https://www.mongodb.com/docs/manual/reference/limits/

## Slide 33

Document boundaries affect concrete application work. A shared user record gives a contact correction one place to happen. Separate event documents let history grow without enlarging the ticket. An embedded group of facts can make a combined read or atomic update convenient.

Every choice brings a cost. References require retrieval and relationship handling. Copies require refresh rules. Related facts split across documents may require coordination when the application promises consistency.

These questions also apply to PostgreSQL, which supports arrays and JSON as well as tables. The database product does not choose a sound model for us. We start with the operations, ownership, and growth we need to support, then choose a representation whose consequences we can explain.

## Slide 34

Open the first lab link on this screen. It goes straight to the MongoDB exercise in Instruqt. Select Launch, wait for the workspace, then select Start. The first challenge is Insert a Document. The student handout below the launch link has your instructions and the second lab. If the browser workspace has not opened after five minutes, use the Day 2 notebook in the handout. You can also use the notebook if the activity won't let you run or change a command.

Keep a short lab log. Which collection did you query? What did the command return? Change one condition, run the query again, and record what happened. If nothing matches, keep that result and explain what you think the filter ruled out.

At minute 75, check your lab record. You have twenty minutes to finish any commands or fill in what you observed. If your record is ready and you want to explore the ticket design, try the optional Chapter 10 response.

Part A is the required submission. Paste it into one Brightspace text entry before you leave. If you write Part B, add it to the same entry. I'll come around while you get started.

## Slide 35

The required submission is the Part A lab record. It identifies the workspace reached, describes an insert and read-back, and explains what happened when a filter changed.

A useful record connects a command to the result actually observed. If a command failed, the record should identify the last successful result rather than inventing output.

Submit that record as one Brightspace text entry. The Chapter 10 response in Part B is optional and can go underneath Part A in the same entry.

## Slide 36

These three short videos review the week's examples. The first follows the array query and shows why conditions can match different events. The second compares write results and shows how a status change and an event can happen in one atomic update. The third compares embedding and referencing for a ticket page.

Each video is silent, with captions on screen. The diagrams are illustrations of the operations we've discussed. They aren't measurements of database performance.

You can use the videos to review a point that still feels unclear. Download the PowerPoint and open it in desktop PowerPoint to play the embedded videos from this slide. The weekly folder also has the individual MP4 files and subtitles. The PDF contains still thumbnails.

As you watch, follow one ticket through the example. Ask which document qualifies, what changes, and what evidence shows that the result is the one we intended.

## Slide 37

For Day 2, start with the Week 10 Lab 2 handout. It has the current activity links and the Day 2 notebook. If a browser workspace won't open within five minutes, or it won't let you try your own commands, move to the notebook and keep your results there.

The other two links are optional if you want to revisit the browser orientation or Atlas Data Explorer from Day 1. If you'd like to try the optional Chapter 10 response, follow the writing prompt in the Lab 2 handout.

## Slide 38

Cardinality describes how many entities can relate to one another. A requester may have many tickets, while a ticket may have many events. Both are one-to-many relationships, but their storage needs can differ.

Current contact details have an independent owner and may be shared by many ticket pages. A historical event belongs to a history that can keep growing. A small headquarters address may be read and changed together with its publisher.

Cardinality helps describe those relationships. Read patterns, ownership, changes, and growth then help determine whether to embed or reference the related facts.

## Slide 39

This complete document describes Example Press and one headquarters address. The address is small, belongs to the publisher in this model, and is usually read with the publisher. Embedding it gives the application those facts together.

If an address had a separate owner, an independent lifecycle, or many records that needed to share its current value, a reference could be useful. The decision depends on the operations and responsibilities the application needs to support.

This one-to-one example complements the growing event history. The words one and many describe relationships, while ownership and workload help choose the stored shape.

## License

Original course prose is licensed under CC BY-NC 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
