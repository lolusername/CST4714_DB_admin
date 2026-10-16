# Week 10: Basic MQL and Document Modeling - Spoken Transcript

## Slide 1

Welcome to Week 10. Look at the line in the middle of the slide: a support application must find and change the intended ticket. Not a ticket. The intended one.

Last week we took the same ticket facts and wrote them as different JSON shapes. We read them and argued about the design, but no database ever touched them. This week a database does. A resident opens the portal and needs to see their own ticket. An agent changes that ticket and must not change somebody else's request by accident.

On Day 1 we work in a small notebook, and every query prints a result we can check against six tickets we can actually see. You will meet a query that looks perfectly reasonable and answers the wrong question about an event array. And you will learn to tell finding a document apart from actually changing it. Why does that matter? Because one of the most confusing bug reports you will ever get is "the app said it worked, but nothing changed."

On Day 2 we turn those operations into a design question. A ticket page needs the current status and the recent events. But a person's contact details change on their own schedule, and event history keeps growing. Where each of those facts lives decides how much work every read and every update costs.

You are not building an application this week. And if your cloud connection is not ready, the notebook's local mode teaches the same queries.

## Slide 2

Here is the good news: you already know how to describe a query. Pick a source, pick the records, pick the fields, and maybe order and limit the result. Look at the table. The left column is the purpose, the middle is the SQL you know, and the right is the same idea in Python with PyMongo.

Choose a source. In SQL, FROM tickets. In our notebook, database, square bracket, tickets. That gives us a handle on the tickets collection, a Python object we send operations through. Choose records. Instead of WHERE status equals open, we write a dictionary: status, colon, open. Read the bottom line of the slide. A filter is a dictionary, not a SQL string. We hand that dictionary to find.

Choose output fields. The projection is another dictionary. A one beside ticket_id asks for that field. The zero beside underscore id hides MongoDB's own document identifier, which would otherwise come back by default. In our fixture, ticket_id and underscore id are two different identifiers. Order and restrict: sort on ticket_id with a one means ascending, and limit two returns two results.

Now the caution in the box. The concepts transfer, but some rules do not. Arrays are values inside documents, and a missing field does not behave exactly like a SQL null. So treat what you know from SQL as a starting point for reasoning, not a promise that only the punctuation changed.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 3

This is a capture of the Atlas interface from August 2026, with the names redacted. Look at the left side: the deployment shows up in the tree. Now look at the main workspace: it is still asking for a connection. Read the caption at the bottom. This is not a successful query result. I am showing it on purpose, because seeing your cluster in a website proves nothing about whether your Python program can query it.

Look at the four layers in the box. A project groups cloud administration settings and resources. A cluster is the database service actually running. Inside it, a database holds collections, and a collection holds BSON documents. Our notebook picks a fresh database name and works in a collection called tickets. We do not create a new cluster every time we run the notebook.

Two different logins are involved here, and people mix them up constantly. Your website account lets you manage the project. A database user authenticates your program's connection and carries the data permissions. Having one does not give you the other.

And there has to be a reachable network path. If the explorer never connected, an empty workspace does not mean your collection is empty. It means you have not asked yet. So the order is always the same: connect, choose the right database and collection, then run a query whose meaning you understand. Use this picture to locate the layers, not as a promise about where every button sits today.

Sources:
- course/textbook/figures/cloud_interfaces/atlas_data_explorer.png, course interface capture dated August 25, 2026.
- https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 4

Here is a trap that catches almost everyone the first time. Colab shows up in your browser, but your Python code does not run on your laptop. It runs on a remote runtime. So when Atlas offers a button to add your current IP address, it may add your laptop's address, while the connection actually arrives from somewhere else. Atlas refuses it.

That is why the notebook has a setup cell before the connection, and the table walks through it. Row one: if you choose Atlas mode, the cell asks a public IP service for the runtime's outgoing IPv4 address and prints it with slash thirty-two, which means exactly one address. It also prints a new practice database name. No database password goes to that IP service. Row two: in Atlas, add that printed address as a temporary entry and wait until it is active. Row three: use a database user, not your website login, and enter the driver URI in the hidden prompt, so it never sits in a source cell or in printed output.

Row four: the connection cell sends ping. A reply proves the server answered. The insert after it still has to pass the user's data permissions.

Read the box. Keep TLS verification on, and never allow access from everywhere. Those shortcuts hide the real problem and weaken protection. And if the cloud path is not working today, local mode teaches the same queries without an Atlas account.

Sources:
- https://www.mongodb.com/docs/atlas/security/ip-access-list/
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/

## Slide 5

This slide is here to save you an hour of confusion. Three things in this course look alike and run in different places. JSON is a text format. Python has dictionaries and lists with its own spelling. And mongosh is MongoDB's shell, which is JavaScript.

Look at the first two rows. In Python, a missing value is None with a capital N, and the Booleans are True and False with capitals. In JSON and in the shell they are lowercase: null, true, false. If you paste null into a Python cell, you do not get Python's missing value. You get an error.

The next two rows are operation names. PyMongo uses underscores: find_one, modified_count. The shell uses capitals in the middle: findOne, modifiedCount. Same operation, different host language. Our slides and notebook use Python. Chapter 10 labels its runnable shell examples, so run those in a shell, and do not paste them unchanged into Colab.

The last row matters most. A string that looks like a date is still just a string. Our Python fixture passes datetime objects with a UTC time zone through the driver, and MongoDB stores them as real BSON dates. In the shell, ISODate builds that kind of value. Neither call is legal strict JSON. That is the bottom line on the slide: MongoDB stores BSON, including typed dates that JSON strings do not create.

So when something fails, first ask which environment you are in. Plenty of apparent database errors are really language errors.

Sources:
- https://www.mongodb.com/docs/manual/reference/bson-types/
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 6

These are the six tickets the notebook's setup cell loads. Six is small on purpose. It is small enough that you can work out the right answer yourself before the program prints anything, and that gives you a second way to check a query instead of trusting whatever comes out.

Look at a few rows. Ticket 1001 is a high-priority streetlight request, and it is open. Ticket 1003 is urgent, the strongest priority on the slide, but look at its status: resolved. Ticket 1004 is new and low. Those combinations matter as soon as a filter mixes status and priority. A high or urgent priority does not, by itself, put a ticket in an active work queue. Keep an eye on 1003 and 1005, because each of them will be the ticket that teaches a lesson.

Read the note in the box. This is a small adaptation of the CSV case you used last week. It keeps selected fields, stores dates as Python datetime values so they become BSON dates, and adds nested requester details, tags, and short event arrays. The event fields are shortened to type and at, where the CSV says event_type and event_at. The notebook explains that mapping instead of pretending it imported every column unchanged.

Some event arrays are empty here. That tells you what this fixture supplies, not that the real ticket had no history.

Later we add ticket 1099, a clearly marked disposable record, so our write practice can never damage these six.

## Slide 7

Now a complete Python query, run after the notebook's connection and fixture cells.

Look at filter_doc. It is a dictionary with two conditions. Status must be in the list new, open, or in_progress. Priority must be in the list high or urgent. Both conditions have to hold for the same document. Think of it as one set of requirements a ticket must pass, not two separate searches whose results get combined later.

Watch what comes back. One line: ticket_id 1001, status open. Why only 1001? It is open, and it is high. Now look at 1003. It passes the priority condition, because it is urgent, but it fails the status condition because it is resolved. That is the first line in the box: both conditions must hold.

Next, the projection. Underscore id is zero, ticket_id and status are one, so that is all we see. But the projection does not remove category, priority, or the events from the stored document. It only shapes what this find returns.

The for loop walks the cursor that find gives us and prints each document. Here that is one dictionary.

In the notebook, you also run the SQL version of this question over the same six tickets, and both identify ticket 1001. Your lab then changes the question to an active lighting and sanitation queue that includes medium-priority work, so you will change this filter and keep priority visible in the output.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 8

Same active statuses, but now we return the opening time along with the ticket number. Look at the sort. It is a list of two pairs. opened_at with negative one, so the newest opening comes first. Then ticket_id with positive one, as a tie breaker if two tickets opened at the same moment.

The limit is two. Watch the result: 1006, then 1004. Now notice what is missing. Ticket 1005 opened recently too, but it is resolved, so it never passed the filter. Sorting does not rescue a document that failed the predicate. The filter decides what qualifies, and only then does the sort put it in order.

find does not hand you a list. It hands you a cursor. We attach the sort and the limit to the cursor, and then the loop reads the results. Once the loop has gone through the cursor, it is used up. Loop over that same cursor again and you get nothing, because it does not rerun the query. That is the note at the bottom: to repeat a consumed query, call find again. For a small bounded result, wrapping it in list is convenient, and we do that on Day 2.

Why bother with a tie breaker? Without one, the order of ties depends on incidental storage order, and you cannot explain it or repeat it. And remember, sort and limit shape this result. They do not reorder or trim the collection.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 9

Two queries on this slide. The first one reaches into a nested document. Each ticket has a requester object, and inside it a user_id. The dotted name requester.user_id says: look inside requester for user_id. Notice it is in quotes. The dot belongs to MongoDB's path, so it is a string, not Python reaching into a variable called requester.

On our fixture, user 101 requested tickets 1001 and 1005, and that is what prints. You can confirm it by looking at the requester objects in the fixture yourself.

The second query searches the tags array. We write tags equals safety, as if tags were a single value. When the field is an array, MongoDB treats that as: does the array contain safety? The whole array does not have to equal the word safety. Tickets 1001 and 1005 both carry that tag.

Now read the result box. Both queries return 1001 and 1005, for different reasons. That agreement is a coincidence of this data. Tomorrow user 101 could open a ticket with no safety tag, or someone else could file a safety ticket. A query states a rule. The fixture is just one set of data we watch it run against.

Hold on to that idea, because the next slide makes it sharper. Once an array holds documents instead of plain words, two conditions can be satisfied by two different elements, unless we explicitly require one element to satisfy both.

Sources:
- https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
- https://www.mongodb.com/docs/manual/tutorial/query-arrays/

## Slide 10

Look at the small table first. Two events on ticket 1001, and they are two separate facts. Event 5001 says a resident created the ticket. Event 5002 says the ticket was assigned, and the actor was an agent. Neither row says an agent created the ticket.

Now the filter below. We named it wrong_question on purpose. It asks for events.type equal to created, and events.actor_role equal to agent. It reads like "an event where an agent created the ticket." Watch what happens: ticket 1001 matches. Read the result box. Ticket 1001 matches this filter, but no single event says an agent created it.

Why? With two separate dotted conditions, MongoDB is allowed to find created in one element and agent in another. Created comes from 5001. Agent comes from 5002. The document as a whole satisfies both conditions, so it qualifies.

Is MongoDB broken? No. The query is valid, and MongoDB did exactly what it defines. The mistake is ours: the query does not say what the application meant.

This is why the fixture keeps a resident-created event and a separate agent event in the same array. If every ticket had only one event, this filter would pass every test you ran, and the bug would wait for production. A small counterexample makes it visible.

You will see this pattern everywhere: product variants with sizes and prices, people with skills at different levels. When conditions describe one related object, the filter has to keep them together.

Sources:
- https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/

## Slide 11

Here is the fix. $elemMatch takes both conditions and puts them inside one requirement for a single array element. The question becomes: does the events array contain at least one event whose type is created and whose actor_role is agent, both in that same event?

Watch the result. An empty list. Every created event in this fixture has resident as its actor role, so no ticket has an agent-created event. The empty answer is the correct answer. An empty result is not automatically an error. We judge it against the question and the data.

Now look at the third box. The notebook also asks for a status_changed event whose actor is an agent. That version returns tickets 1002 and 1003. So $elemMatch is not a trick for making results disappear. It states that related conditions describe one element, and the data either has such an element or it does not.

One more boundary, in the last line. $elemMatch in the filter decides whether the ticket qualifies. It does not trim the events array in what comes back. If your projection includes the whole events field, a matching ticket still shows its other, nonmatching events. Shaping array output is a separate operation.

When you write your lab explanation, do not just repeat the phrase "same element." Use the event IDs and the field values. Say that created came from event 5001 and agent came from event 5002. A concrete pair of rows shows you understand why the two queries differ.

Sources:
- https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/

## Slide 12

Before we change anything, we need something safe to change. Never practice writes on data you care about.

Look at test_filter. Ticket 1099, plus two markers: test_record is True and course_fixture is cst4714. Why three conditions instead of just the ticket number? Because the filter should be far narrower than anything real tickets could share. A status or a category matches many tickets. These markers match only our test.

The next line, delete_many with that filter, clears out any earlier copy of the test record, and only the test record, in our private practice collection. Then insert_one creates it fresh, with status new and an empty events array. Notice the two asterisks before test_filter. That is Python dictionary unpacking, not a MongoDB operator. It copies the ticket number and both markers into the new document, so the document we insert carries exactly the identity our filter looks for.

This cell is a reset. Every time you run it, the experiment starts over. So when you test a repeated update in a minute, run the update cell twice without rerunning this one in between. Otherwise you keep recreating the starting state and never see the second case.

Read the boxes. The notebook also creates a unique index on ticket_id. MongoDB's own underscore id would not stop two documents from sharing ticket number 1099. The unique index does, so our target is unambiguous.

No sample database is changed. Never swap in an Atlas sample collection or your project data here.

## Slide 13

Now we change the test ticket. update_one with our exact test filter and a $set. The $set names two fields, status and assignee_id. It changes those two and leaves every other field in the document alone. That is very different from replacing the whole document with a smaller dictionary, which would quietly throw away everything you did not mention.

Look at the table. First execution: matched one, modified one, and the read-back says in_progress. The filter found test ticket 1099, the values were different, so it changed them.

Now watch what happens when I run the exact same cell again, with no reset in between. Matched one. Modified zero. Status still in_progress. The filter still finds the same document. But the document already holds the values $set asks for, so there is nothing to change.

Why does this matter? Because those two counts answer different questions. A modified count of zero, by itself, cannot tell you whether the filter found nothing or the values were already there. If you only look at modified_count, you will chase a bug that does not exist. So read matched_count too, and then read back the state the application actually cares about.

One more detail. These are document counts, not field counts. We changed two fields, status and assignee_id, in one document, and modified_count is one, not two. That is the habit for the rest of the course: never guess from an ambiguous zero.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/update/

## Slide 14

This update adds one more condition to the filter: status must be new. In plain words: change this test ticket to resolved, but only if it is still new. Remember, the previous slide already moved it to in_progress.

Watch the result. Zero, zero. Status remains in_progress. Compare that with the repeat on the last slide. There, the filter found the document and had nothing to change: one and zero. Here, no document satisfies the whole filter, so it never got that far: zero and zero. Read the box. The current document no longer satisfies status equals new.

Why would you want a write that can refuse itself? Picture two agents on the same ticket. One moves it to in_progress. The other, looking at an old screen, clicks resolve. Without the expected-state condition, the second click silently overwrites the first. With it, MongoDB rechecks the condition as part of the single-document write, and the stale action finds that its expectation no longer holds.

The application still needs a policy for that outcome. Reload the ticket, tell the user the state changed, or ask them to decide again. Do not treat every zero match as success. And read the last box: do not call it a broken connection either. A zero match is an application outcome to interpret.

This is a small state-transition example, not a full concurrency or retry protocol. The skill is to say what the filter permits and compare that with what is stored when the write runs.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 15

$push appends a value to an array. Here the value is a small event document, event 5999, a status change by an agent. If I send an unconditional push twice, the array gets two copies. Giving the event an ID field does not make embedded array elements unique.

So look at the filter. Besides our test markers, it says events.event_id is $ne 5999, not equal. Only match this ticket if it does not already contain event 5999. First run: the event is not there, so the result is one and one. Now watch the second run. The guard no longer matches, so the result is zero and zero, and there is still exactly one event 5999. That is the line in the box: the filter refuses a second append.

Keep the scope precise, though. This protects this one operation on this one document. Other code that writes events has to follow compatible rules, and a real distributed event system has more failure and ordering problems than this.

Now read the bottom box, because it sets up Day 2. The status update on slide 13 and this append were separate writes. Each one is atomic for its document. But there is a gap between the two calls, and a reader in that gap could see the new status without the event that explains it.

Next meeting, we put a status change and an event append into one update. That is where queries meet document design.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 16

Deleting is where predicate discipline matters most, because there is no undo cell.

Look at the first line. Before deleting, we read the target with find_one and a small projection, so we can see exactly which document the filter identifies. Then delete_one with the same exact test filter. Watch the output. Deleted: 1. Remaining test record: None, because find_one returns None when nothing matches. Other tickets: 6. That last count is our scope check. We confirmed the target is gone and the six teaching tickets are untouched. They stay available for practice until the cleanup cell removes this run's practice collection.

Now run the same delete again. It reports zero. The filter is still valid and still narrow. Its target is simply gone already. That is an expected repeat result, not a syntax failure.

Read the caution box. An empty filter, a pair of empty braces, matches every document. delete_one with an empty filter removes some document, with no guarantee it is the one you meant. delete_many with an empty filter removes all of them. If the requirement is one specific ticket, the filter must say so.

The second half of the caution: a preview is not a lock. Between your find_one and your delete, another writer can change things. In this private exercise, we control the data. In a shared application, you need expected-state conditions or suitable transaction and concurrency rules. Previewing is a good habit, but it does not give you a transactional guarantee.

## Slide 17

Here is Lab 1. In the weekly guide it is called Find and Change the Right Document, and it all happens in one notebook. You already saw SQL and MongoDB both find ticket 1001 for the same question.

Now the question changes. The lighting and sanitation crews want their active tickets, newest first, with priority displayed. Keep the category condition in the starter, add the active-status condition, and add priority to the projection. Do not carry over the demo's high-or-urgent condition. Medium-priority work still needs a crew, and that condition would hide it.

Predict the order from the opening dates before you run anything. The finished queue is 1006, 1002, and 1001, in that order. Then explain ticket 1005. It is sanitation and high priority, but it is resolved, so including it would mix finished work into the crew's queue.

Next, compare the two array queries using the actual event objects. Then run the $set cell twice without rerunning the test insert: one and one, then one and zero. Compare that with the expected-state update. Read the changed test ticket, then run the targeted delete.

At the end of the notebook is a section called Results Record with the questions. Add a text cell under it, write your answers there, and say whether you used local mode or Atlas. Run cleanup, remove any saved credential, and if you used Atlas, remove the temporary IP rule. Submit the notebook. No screenshot.

## Slide 18

Welcome back. Last time we queried documents and watched what our writes actually did. Today we design the ticket page.

Look at the first box. The page needs the ticket's current status and only its latest events. Now read the second box. Contact details change independently, and the system still has to keep years of event history, including everything the page does not show.

Think about what that means. A resident fixes their email address once, and they expect every ticket page from then on to show the corrected value. If we had copied the email into every ticket they ever opened, that one correction becomes an update across many documents, and missing one leaves a wrong address on a page.

Read the last line: those requirements influence the document boundary. Notice it does not say they choose it. There is no single correct document shape. The requirements tell us which costs to compare. Keeping related data together makes a read convenient and lets related changes happen in one atomic document write. Keeping a shared identity, or a growing history, separate makes independent changes and long retention easier.

Here is the plan. My live example uses a one-to-one relationship. Your individual practice uses one-to-many, and then you revise one ticket design for the latest-events requirement. We are not redoing last week's JSON exercise, and nobody is building a web application. The new skill is explaining how a shape serves real reads and updates.

## Slide 19

Here is a word you know from relational design: cardinality. It describes how many things can sit on each side of a relationship under the application's rules. Look at the table. Many tickets point to one requester. One ticket has many events. And in our small publisher example, we assume one publisher has one headquarters.

Now look at the third column, because that is where decisions come from. Ticket to requester: the shared user can change independently. Ticket to events: history can outgrow an embedded array. Publisher to headquarters: a small owned address can fit inside its publisher.

Notice what cardinality did not do. It did not choose the storage. Read the box. A one-to-one relationship could be fields in one document, a nested subdocument, or two referenced documents. And the word many is vague. Many could mean three fixed items or years of accumulating records, and those need very different designs.

So what does decide it? The second line of the box: ownership, reads, writes, and growth. For the requester, it is the independent identity and contact changes. For events, it is growth and the need to query history on its own. For the headquarters, it is a small object that is normally read together with the publisher.

And say your assumptions out loud. Real companies can have several offices. If we call this one-to-one, we mean the one designated headquarters, not every office. That is the relational reasoning you already know, carried into document design.

## Slide 20

The live resource for my demonstration is MongoDB University, Modeling Data Relationships, Lesson 3: Modeling One-to-One. I will work through its one-to-one material and its practice. Your assigned activity is Lesson 4, so you will apply the same reasoning to a different relationship.

Look at the small JSON document. A publisher, p7, named Example Press, with a headquarters object inside it: city New York, country US. The address is embedded in the publisher. When is that a good idea? If the application normally loads the address together with the publisher, and the address belongs only to this publisher under our stated assumption, keeping them in one document puts the related facts together and returns them in one read.

Another design could store the address as its own document and put an address identifier in the publisher. That could be right too, if the address had its own lifecycle, its own permissions, or its own queries. Being one-to-one does not forbid either shape.

To be clear, this document is our own small illustration, not the answer to the vendor's practice question. As we go through the lesson, I will connect its example to ownership and access.

Read the last line of the slide. The unit names matter. MongoDB University sometimes reuses the same video in a newer course package, so two differently named courses do not automatically mean two different activities. Our boundary today is explicit: one-to-one in my demonstration, one-to-many in your individual work.

Sources:
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-3-modeling-one-to-one/learn
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn

## Slide 21

Remember Day 1's gap, where the status change and the event append were two separate writes? Here is how to close it.

This runs on a fresh demonstration collection, where ticket 1001 is open. Look at the update document. It has two operators. $set changes the status to in_progress. $push appends event 5099, a status_changed event, to the embedded events array. Both in one call.

Because both changes are one write to one document, they are atomic together. That is the first line of the box. A reader never sees the new status without the event. On Day 1, by contrast, the status changed before the append ran.

Now look at the filter. It includes the expected state: status open. On the first run, the document matches and changes. Now watch me repeat it. The ticket is in_progress now, so the filter finds no open ticket 1001. Zero, zero, and no second event. That comes from the state condition, not from some rule that $push prevents duplicates. It does not.

Read the scope note. If the event lived in a separate document, changing the ticket and inserting the event would cross a document boundary, and we would have to coordinate them. MongoDB does support multi-document transactions, but they have costs and need the right deployment and application design.

So single-document atomicity is a real reason to embed. It is not a reason to grow one document forever or to copy every shared fact into it.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 22

A resident changes their email address. Look at the table and ask who owns each stored fact.

First row: requester_id 101. The ticket stores the relationship. When the email changes, the ID stays the same, because the person did not change. Second row: the current email for user 101. That belongs in one authoritative user document, so a correction updates one user record, once. The page reads the ticket, takes the requester ID, and reads that user's current contact details. That costs one extra read, and in exchange we avoid maintaining copies of a fact we promised is current. That is the note at the bottom: a copied current email would introduce another value to maintain.

The third row is the interesting one: requester_name_at_open. Suppose the business needs to keep the name shown when the request opened. That field is a deliberate historical snapshot. If the person later changes their display name, the snapshot keeping its original value is correct. It is not stale. It means something different.

The mistake is mixing those meanings without saying so. A field the application presents as the current email must follow the current-contact rule. A historical snapshot should be named as historical, the way this one says at_open. The database cannot read your intention from a vaguely named string.

One last point. Storing requester_id 101 does not create a foreign key. Nothing guarantees that user 101 exists. The application needs its own rules for creating, updating, and deleting related identities.

## Slide 23

Now the event history. Look at the two JSON snippets. The ticket on top keeps its own fields: ticket_id 1001, requester_id 101, status open. The event below is a separate record, event 5002, with its own ticket_id pointing back to 1001.

The direction of the reference matters. Read the first line of the box: each event points to its ticket, and the parent does not need an ever-growing ID list. If we put an array of every event ID inside the ticket, we would just move the growth problem from event objects to event IDs. When each child carries ticket_id instead, a new event is a new document in the event collection, and the ticket stays bounded. To get one ticket's history, we query the events by ticket_id.

Notice the field names here, event_type and event_at. Those are the source-case names from the CSV. Then read the second line of the box. This is a JSON sketch, so the timestamp is text. In the runnable page demo, the driver stores event_at as a BSON date from a Python datetime. That way we sort by a real date, not by strings we hope share a format.

And a reference only names a relationship. It does not enforce referential integrity, it does not create an index, and it does not load the other document for you.

The next slide does the actual reads, and shows the extra read-side work this simple referenced design costs.

## Slide 24

Here is the ticket page assembled from referenced data, in three reads. Line one finds ticket 1001. Line two reads the person whose user_id equals the ticket's requester_id. Then the history query finds events whose ticket_id matches, and keeps only the two most recent.

Look at the sort: event_at descending, with event_id descending as the tie breaker. Then limit two. That limit caps what the page shows. It does not delete older events. History stays complete in the collection.

Watch the output in the box: open, Requester 101, then event IDs 5002 and 5001. Our worked ticket has only two events, so you see both. Your lab ticket has three events, and there the difference between displaying recent history and retaining full history becomes visible.

Two honest caveats. First, this code assumes the ticket and the person exist in the fixture. A real application has to handle a missing ticket or a broken reference instead of indexing into None. Second, read the next line of the box: three reads assemble one page, and they are not one atomic snapshot. A contact change or a ticket update could land between reads. Whether that matters depends on what the page promises.

Last line. An event index that starts with ticket_id and then the ordering fields can support this read. That is a design candidate, not a measured performance claim, because our collection is tiny. We will keep connecting queries, indexes, and observed work in later lessons.

## Slide 25

How should event history be stored? The table gives three defensible answers, and in each one something grows.

First row: embed every event. The ticket document grows with each event. The page gets everything in one read, and a status change plus an append can be one atomic update. But that same document keeps getting bigger.

How big can it get? Read the box. A BSON document has a 16 MiB size limit. Do not treat that as a target. Large documents, frequent updates, and pages that only want a small slice of history get awkward long before the hard limit. And the limit does not translate into a maximum number of events, because events vary in size.

Second row: keep all events separate. What grows is the number of event documents, and the ticket stays bounded. The page does a ticket read plus a bounded history query, and a report can query events across tickets. The cost is extra retrieval, and coordination when one operation changes both a ticket and an event.

Third row: a hybrid. The authoritative history lives separately, and the ticket carries a small capped copy of recent events. Convenient for the page. But read the last box: that copy needs an explicit refresh and stale-data policy. Copying data always creates work.

For a beginner project, choose the simplest design that meets the requirement. A hybrid is not a required upgrade. An accurately explained referenced model can be the stronger answer.

Sources:
- https://www.mongodb.com/docs/manual/reference/limits/

## Slide 26

When you recommend a model, say what it actually does. Look at the first box. A separate user record means a contact correction happens once. Separate event records mean complete history is kept without enlarging the ticket. Those are concrete consequences for our workload, and you can check them.

Now the cost, in the same box. The page has to retrieve the related records, and those independent reads can see different moments if writes happen in between. If the page needs one consistent version of everything, the application needs stronger coordination than the three plain reads we just ran. If a slightly behind recent-events preview is acceptable, the application should state that promise rather than deliver it by accident.

The second box applies the same rigor to vendors. Workloads matter in PostgreSQL too. PostgreSQL supports arrays and JSON. SQL systems do not force every schema into third normal form. Normalization is a design discipline, not a setting applied automatically to every table. And joins are not inherently unacceptable. Their cost depends on the query, the data, and the indexes.

Likewise, MongoDB's flexible documents do not remove the need to define what fields mean and to enforce rules. Read the last line: neither a SQL table nor a MongoDB collection chooses a good model for us.

So in your design response, name one benefit and the work required to get it. That says far more than calling a model flexible, modern, or scalable.

Sources:
- https://www.postgresql.org/docs/current/arrays.html
- https://www.postgresql.org/docs/current/datatype-json.html
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 27

Here is Lab 2. In the weekly guide it is called Design the Ticket Page. Start with the link at the top: MongoDB University, Modeling Data Relationships, Lesson 4, Modeling One-to-Many, including its Practice. The Week 10 guide links directly to both. My demo used Lesson 3, so you are not repeating my activity. No complete course badge is needed.

Then the design work, in the middle box. Revise one JSON design for ticket 1003. Use the same CSV facts from last week, with a new requirement. The page shows only the latest two events, newest first. The system retains the entire history. And the current contact details are editable in one authoritative user record.

You are not writing two competing JSON files or building an application. Show one representative ticket document. If related facts live somewhere else, include one small example of that related document, so the relationship is clear.

Then write a short explanation to the developer who will build the page. Name the two event IDs the page should show. Explain how the page retrieves them, and where a contact change happens. And tell them how your design behaves if this ticket eventually has fifty thousand events.

Read the bottom box. Submit it all as one Brightspace text response: the JSON, the explanation, and the Lesson 4 Practice progress image. If the platform or your account is unavailable, use the chapter's worked examples and say so in the same response. Do not invent a score.

Sources:
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1

## Slide 28

Last slide: how you talk about this work. Read the paragraph in the middle. It is one way to describe this week's skill in an interview or a team meeting.

It starts with something specific. "I tested a document query against a small fixture." Then it names a real mistake, the array filter whose conditions matched different events, and says how it was caught: a counterexample. That beats "I know MongoDB."

Next it connects write counts with a read-back. You can now explain three different outcomes. A request that changed a document. A request whose values were already there. And a request whose expected-state filter no longer matched.

Then it explains a modeling choice in application terms. Shared contact details and growing history have different requirements, and the description admits the extra reads and consistency tradeoffs instead of promising that one shape is always faster.

Read the first line of the bottom box: describe the experiment you actually performed. If you used local mode, say you tested the query logic locally. Do not imply you operated a production Atlas service or measured performance at scale. If you did connect to Atlas, you can also describe the separate database user, the runtime IP rule, and the secure connection setup.

And the second line. Next week we aggregate results across documents and enforce document rules. Keep the same habit: state the question, identify the unit of data, predict an observable result, and check what the system actually did.

## Slide 29

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Querying inside documents: arrays and $elemMatch (1:12); Did the write do what you meant? (1:06); Embed or reference? Let the workload decide (1:21). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 10 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
