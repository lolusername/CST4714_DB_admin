# Week 10 Basic MQL and Document Modeling

Word for word spoken script. Every slide section contains only words to say aloud. Preparation guidance is in the private instructor guide. Slides 1–20 cover Day 1, including the complete field reference on slides 7–9. Slides 21–31 cover Day 2, slide 32 contains videos, slides 33–35 contain static illustrations, and slide 36 compares the browser labs with Colab and links optional Data Explorer practice.

## Slide 1

Last week, we represented ticket data as JSON. Today we're going to query those documents and make a few controlled changes.

Imagine the lighting crew opening its work queue. It needs tickets that still need attention. If our query includes completed jobs, the crew gets the wrong list even though the code runs without an error. That's the kind of problem we'll learn to catch today.

We'll work with six tickets, so you can check each answer yourself. First we'll compare a familiar SQL query with its MongoDB equivalent. Then we'll query nested data and arrays, and finish by updating a disposable test ticket.

Keep the notebook open alongside the slides. For each important example, we'll predict the result together and then check what the notebook returns. Today we're connecting the notebook to your Atlas cluster. If a connection needs attention, we'll use the notebook's diagnostic category to identify the next check.

The modeling work comes next class. Today, let's get comfortable saying exactly what a query asks for and checking what a write actually changed.

## Slide 2

The structure of a query should feel familiar. We choose a collection, decide which documents qualify, choose the fields to return, and put the results in order.

In SQL, the WHERE clause describes the qualifying rows. Here, we pass a Python dictionary to find. A condition such as status equals open goes in that dictionary. MongoDB calls it a filter.

The projection controls which fields we see in the result. A one includes a field. We explicitly hide MongoDB's _id field with a zero because this example only needs the ticket number and status. The stored document keeps all its other fields.

We'll run the SQL and MongoDB versions over the same six tickets in a moment. Before we do, which part of the MongoDB query would you change if the question changed from open tickets to resolved tickets?

The filter. Changing the projection would change what we see about the tickets, but it wouldn't change which tickets qualify. Keep that distinction in mind when you adapt the query for the lab.

## Slide 3

This screenshot helps us locate the pieces of Atlas. It's a course capture from August 2026, so your screen may look a little different.

The project holds administration settings and resources. The cluster runs the database service. Within that service, a database contains collections, and collections contain documents. Our notebook uses a fresh practice database and a collection called tickets.

There are also two different kinds of account involved. Your Atlas website account lets you manage the service. A database user lets a program connect to the data. Signing into the website doesn't automatically give the notebook a working database connection.

In this capture, the workspace is still asking for a connection. We can't infer anything about the collection's contents from that empty area yet.

Today we're using Atlas, so the next slide explains how the connection comes from Colab's remote runtime. We'll verify the connection by sending ping, then try the fixture setup.

## Slide 4

Today we're connecting Colab to your Atlas cluster. Colab runs Python on a remote machine. Your browser is on your laptop, but the database connection comes from that runtime.

Run the setup cells and use the runtime IP address the notebook prints. Add it as a temporary Atlas access-list entry. The /32 suffix limits the entry to one IPv4 address. Adding your laptop's address instead won't necessarily allow the runtime through. Keep the printed practice database name when retrying setup so it still matches the database user's permission.

Enter the connection URI in the hidden prompt. Use a database user's credentials and keep TLS certificate verification enabled. If the connection fails, Setup C reports a diagnostic category. We'll use it to check the relevant setting, such as credentials, network access, DNS, or certificates, and then try again.

After fixing the setting, run the connection cell again. Once ping responds, we know the deployment answered. The fixture setup then tests permission to write the practice data.

The link below also leads to a short comparison with MongoDB University's guided browser labs and an optional Data Explorer practice. For today's Lab 1, keep your work in your saved Colab notebook.

## Slide 5

Before we run the examples, check the language of the cell you're using. Today's notebook is Python with PyMongo. Some textbook examples use mongosh, which uses JavaScript syntax.

Python uses None, True, and False. JSON uses null, true, and false. That difference is enough to cause an error if you paste a JSON example straight into a Python code cell.

The method names differ too. In Python we use find_one and modified_count. In the shell you'll see findOne and modifiedCount. You don't need to memorize both spellings today. You do need to recognize which environment the example belongs in.

Dates deserve an extra check. A date-looking string is still text. Our fixture creates Python datetime values, and the driver stores them as BSON dates. A JSON sketch with a quoted timestamp doesn't do that conversion by itself.

If you get an error before a query runs, start by checking the language and the value types. The problem may be in the Python expression before MongoDB receives anything.

## Slide 6

Here are the six tickets we'll query. Take a moment to read the status and priority together.

Which tickets would qualify if I asked for active work with high or urgent priority? For this exercise, active means new, open, or in_progress.

Ticket 1001 qualifies. Ticket 1003 is urgent, but it's resolved. Ticket 1005 is high priority and also resolved. Priority tells us how important the request is. Status tells us where it is in the workflow. We need both when the question asks for both.

These documents are a small adaptation of last week's CSV case. They use selected fields, typed dates, and short nested objects and arrays. The event fields use the shorter names type and at here. An empty event array means this fixture supplies no events for that ticket, rather than making a claim about all of its real history.

We'll leave these six records intact during the write exercises and create a separate test ticket, 1099.

Before we write the first query, let’s look through the complete field reference on the next three slides. We’ll identify the ticket fields, the nested requester and event fields, and the practice markers so every name in the queries has a clear meaning.

## Slide 7

Before we query anything, let's look at the fields the notebook actually gives us. One document represents one ticket. This reference describes the supplied data. We haven't installed a validator that requires every future document to have this shape.

There are two identities. MongoDB generates _id when we insert a document without one. ticket_id is the case number that people use, such as 1001. The notebook creates a unique index on ticket_id so we don't accidentally keep two documents for the same case number. Those are separate fields with separate roles.

Category names the service area. Priority describes importance, while status describes the current workflow state. A high-priority ticket can already be resolved. That distinction is going to matter in the crew queue. Active is our grouping of new, open, and in_progress. There isn't an active field in these documents. Subject is the short description a person reads.

Opened_at records the opening time. Our notebook supplies a Python datetime value, which the driver stores as a BSON date. Extended JSON can display that typed date with a dollar-date wrapper. A quoted timestamp by itself is just a string. When we sort opened_at later, we're sorting actual date values.

The next slide shows the fields that contain related information, including the requester and the event history.

## Slide 8

Requester is an object inside the ticket. Its user_id identifies the requester in our case, and display_name gives us a readable label. The dotted path requester.user_id means we want the user_id field inside that object.

For Day 1, there isn't a separate users collection behind this example. The requester details are copied into each ticket. The number identifies a person logically, but MongoDB isn't following a foreign key to another record for us. Assignee_id works as a logical staff identifier too. Values 201 and 202 identify staff in the case. Ticket 1004 has a null assignee because nobody is assigned. In Python you'll see that null as None.

Tags is an array of strings. Ticket 1001 includes lighting and safety. Later, a filter for the value safety will ask whether that value occurs in the tags array.

Events is different. Each array element is a small object with several fields. We'll inspect those fields next. An empty events array on tickets 1005 and 1006 means that this teaching fixture leaves out their history. It doesn't tell us that those tickets never had events.

Our disposable test ticket also has a deliberately smaller shape. It starts without tags or assignee_id. A missing field is different from a field that is present with null. The later update adds assignee_id to that test document.

## Slide 9

Every event in this fixture has an event_id, a type, an actor_role, and an at value. Event_id identifies the event. Type tells us what happened. Actor_role says whether the actor was a resident or an agent. At records when it happened as a date.

For ticket 1001, event 5001 says created by a resident. Event 5002 says assigned by an agent. Keep those two objects separate as you read them. Later we'll see why finding created in one event and agent in another doesn't establish that an agent created the ticket.

The dotted names in the table are the paths we'll use in queries. The fields themselves sit inside each object in the events array. An event_id value there doesn't automatically have a uniqueness constraint. Our append example uses a filter to prevent adding its particular event twice.

The final two fields belong to the ticket, outside the events array. Course_fixture marks the records supplied for this practice. Test_record appears only on disposable ticket 1099 and is True. The original six tickets don't have that field. We combine those markers with the ticket number when practicing writes so the target is very specific.

These event names differ slightly from the original CSV case. Event_type became type, and event_at became at. We also supply an actor role and omit some original columns. With those names and types clear, we can now read each query against the actual documents.

## Slide 10

Let's run the query we just predicted. The filter requires an active status and a high or urgent priority. A document has to satisfy both conditions.

The result is ticket 1001, with status open. That agrees with our reading of the fixture. The SQL version in the notebook returns the same ticket for the same question.

Notice that the filter uses priority even though the projection doesn't display it. A field can help decide whether a document qualifies without appearing in the result. Likewise, displaying a field doesn't make it a filter condition.

Now suppose the lighting crew says, "We also need our medium-priority jobs." What would happen if we kept this priority restriction?

We'd hide work that belongs in its queue. In your lab, the requirement changes to active streetlight or sanitation tickets. You'll keep the category condition from the starter, add an active-status condition, and display priority. Let the new question guide the changes you make to the query.

## Slide 11

This query asks for the two most recently opened active tickets. The filter chooses the active documents. The sort puts them in order, and the limit keeps the first two.

We sort opened_at descending, so newer dates come first. We also sort ticket_id ascending to break a tie if two tickets share an opening time.

The result is 1006, followed by 1004. Ticket 1005 doesn't appear even though it opened recently, because its resolved status fails the filter.

One practical detail: find returns a cursor. The loop reads through it. If you run another loop over that same consumed cursor, you may get no output. Call find again when you want to repeat the query. For a small result, converting it to a list can also be convenient.

Sorting and limiting affect the returned results. They don't rearrange the stored collection or delete the tickets beyond the limit. We'll use that distinction next class when a page shows recent events while the system retains the full history.

## Slide 12

Now we'll reach inside a document. The path requester.user_id means the user_id field inside requester. We pass that dotted path as a string in the filter.

For user 101, this fixture returns tickets 1001 and 1005. You can check their requester objects to confirm it.

The second query searches a simpler array. Asking for tags equal to safety matches a document when its tags array contains that value. The result happens to be the same two ticket IDs.

Would those queries always return the same tickets?

No. Another requester could open a ticket tagged safety, or requester 101 could open one without that tag. The two filters express different rules. This dataset happens to give them the same answer.

The next example uses an array of event documents. That's where we need to be more careful: two conditions can find their matches in different events, even when we intended them to describe one event.

## Slide 13

Let's read the two events on ticket 1001. Event 5001 records a resident creating the ticket. Event 5002 records an agent assigning it.

Did an agent create this ticket, according to either event?

No. Now consider the filter below. It asks for events.type equal to created and events.actor_role equal to agent. It looks plausible, but ticket 1001 matches it.

The created value comes from event 5001. The agent value comes from event 5002. Separate dotted conditions can find those values in different elements of the array. Both conditions are true somewhere in this ticket, even though no single event contains both values.

That explains why a successful query can still answer the wrong application question. We need to say that both conditions belong to the same event.

Before we change the filter, try explaining the mismatch using the two event IDs. Being specific about the data makes this much easier to reason through.

## Slide 14

We can express the intended question with $elemMatch. It asks whether at least one event satisfies all the conditions inside it.

Here those conditions are type created and actor_role agent. They have to hold in the same event. This time the result is an empty list. In this fixture, every created event belongs to a resident.

Let's change the question slightly. The notebook also asks for a status_changed event performed by an agent. That query returns tickets 1002 and 1003. So an empty result in the first example makes sense because of the data, rather than indicating that $elemMatch is failing.

There's one more distinction to keep clear. This use of $elemMatch is in the filter. It decides whether the ticket qualifies. If we return the whole events field, we still receive the ticket's other events too. Selecting documents and shaping the array we display are separate tasks.

For your explanation, use ticket 1001 and events 5001 and 5002 to show why the separate conditions match while the same-event condition doesn't.

## Slide 15

We're ready to practice writes. First we'll create a record we can safely change: ticket 1099.

The test filter includes its ticket number and two markers, test_record and course_fixture. We use that same narrow filter throughout the exercise so each operation clearly targets our disposable record.

The setup removes an earlier copy of that test record, if one exists, and inserts a fresh one with status new. The two asterisks copy the filter's fields into the Python dictionary we're inserting. That's Python dictionary unpacking.

The fixture also has a unique index on ticket_id. MongoDB's own _id identifies each document, but it wouldn't by itself prevent two documents from sharing a ticket number.

Run this setup once now. In the next example, we'll run the update twice. Leave the setup cell alone between those runs, because rerunning it would reset the record and change the experiment.

If your later results differ from ours, the first thing we'll check is which setup and update cells ran, and in what order.

## Slide 16

This update uses $set to change the status and assignee. The other fields stay in the document.

Before I run it, the status is new. The first run reports one matched document and one modified document. Reading it back shows in_progress.

What do you expect if I run exactly the same update again, without resetting the ticket?

We get one matched and zero modified. The filter still finds the ticket. It already has the requested values, so this run makes no further change.

Both numbers matter. A modified count of zero alone doesn't tell us whether the ticket was absent or already up to date. We need the matched count and a read-back to interpret the result.

These counts refer to documents. We changed two fields in one document, so the modified count is one.

Also keep $set distinct from replacing the whole document. A replacement can remove fields you leave out. Here, changing only the named fields is what we intended.

## Slide 17

The ticket is now in_progress. This next update asks to resolve it only if its status is still new.

Predict the counts before we run it.

Zero matched and zero modified. Ticket 1099 still exists, but it doesn't satisfy the whole filter. Its current status is different from the status the update required.

Compare that with our repeated $set. That was one matched and zero modified: the ticket qualified and already held the values. Here the ticket doesn't qualify at all.

An expected-state condition can help when someone acts on an old view of a ticket. The write checks the expected value as it runs. If that expectation no longer holds, the application can reload the ticket and let the user decide what to do next.

This example demonstrates one guarded state transition. It doesn't solve every concurrency problem. For today, the useful habit is to read the complete filter and compare it with the document's current state before interpreting a zero match.

## Slide 18

$push appends a value to an array. In this example, we're adding event 5999 to the test ticket.

If we sent an unconditional push twice, we could append the event twice. An event_id inside an array doesn't automatically make that value unique.

Our filter adds a guard: the ticket must not already contain event 5999. The first run matches and modifies one document. On the second run, that event is already present, so the filter matches nothing. We get zero and zero, and the array still contains one copy of the event.

That protection depends on this write's filter. Other code that appends events needs compatible rules too.

There's also a timing detail worth keeping for next class. We changed the status in one call and appended the event in another. Each write is atomic for the document, but those two calls are separate. A reader between them could see the changed status before the event is added.

Next class we'll combine related changes into one update and connect that to the document's design.

## Slide 19

We'll finish by deleting the disposable test record. First, find_one shows us the document identified by our test filter. Then delete_one uses that same filter.

After the first deletion, deleted_count is one. The next read returns None, and the count of the original teaching tickets is still six. Those checks tell us both that the target is gone and that our practice stayed within its intended scope.

Running the delete again reports zero because the record is already gone.

Be careful with an empty filter. It matches every document. With delete_one, that means one unspecified matching document can be deleted. With delete_many, it means all matching documents. Neither expresses our intention to remove only test ticket 1099.

Previewing the target is useful, but the preview doesn't lock it. Another writer could change data between a read and a delete. In shared applications, the write's conditions and concurrency rules still matter.

For this exercise, keep the narrow test filter exactly as supplied and verify the result before running the final cleanup.

## Slide 20

You now have the pieces for Lab 1. Open Find and Change the Right Document and work in your own copy of the notebook.

For the crew queue, keep the streetlight-or-sanitation category condition, add the active statuses, and display priority. The queue should include medium-priority work. Predict the ticket order from the fixture before you run your version.

When you check the result, pay particular attention to ticket 1005. Explain whether it belongs in a queue of work the crews still need to do.

Then compare the array filters using actual event IDs and values. Run the $set update twice without resetting the test ticket between runs. Compare those results with the expected-state update, read the document back, and complete the targeted deletion.

Use the Results Record section for your short explanation. Say whether you used local mode or Atlas, and include what your results showed. Run cleanup after you've recorded the evidence you need. Atlas users should also remove the temporary IP rule.

Submit the completed notebook with your changes and outputs. Today's submission doesn't need an extra report or screenshot. I'll circulate while you work.

## Slide 21

Last class, we practiced querying documents and checking write results. Today we'll use those operations to design a ticket page.

The page needs a ticket's current status and recent events. The system also needs to retain older history and let a resident correct their contact details in one place.

Suppose that resident changes their email address. If we copied it into every ticket, we'd have to locate and update each copy to keep every page current. A shared user record gives us a single place for that correction, with an extra retrieval step when we build the page.

We'll compare those kinds of consequences throughout the class. Keeping related facts together can simplify a read and allow one atomic document update. Keeping independently changing facts or growing history separate can make other operations easier.

I'll demonstrate a one-to-one relationship. You'll work through the one-to-many activity and then revise a ticket design for the new page requirements. The aim is to explain how the shape supports the work the application actually does.

## Slide 22

Cardinality describes how many things can participate on each side of a relationship. A requester may have many tickets. A ticket may have many events. In our publisher example, we assume one designated headquarters per publisher.

Those descriptions help us understand the relationships, but they don't settle where to store the data.

For example, a headquarters address could be embedded in its publisher or stored separately with a reference. We'd ask whether it belongs only to that publisher, whether the application normally reads them together, and whether the address needs independent updates or access rules.

For an event history, we also need to ask what "many" means. A fixed list of three items is different from records that accumulate for years.

As we work through the examples, say the assumptions aloud. Our headquarters relationship is one-to-one because we're talking about one designated headquarters. We aren't claiming that a publisher can have only one office. Clear assumptions keep the model tied to the requirement we're actually discussing.

## Slide 23

For my demonstration, we'll use MongoDB University's Modeling Data Relationships course, Lesson 3, Modeling One-to-One. Your individual activity uses Lesson 4, Modeling One-to-Many, including its Practice.

Before opening the lesson, let's use this small publisher document to frame the decision. Example Press has an embedded headquarters address. If that address belongs to this publisher and is usually read with it, embedding makes the complete information available in one document read.

We could store the address separately instead. That may make sense if it has independent access rules or operations. The one-to-one relationship allows either design; the application's needs help us choose.

This publisher document is our own illustration. We'll follow the external lesson's example when we open its activity.

If the platform is unavailable, we can still work through the chapter's examples and discuss the same choices. For your submission, follow the Lab 2 fallback and say which material you used. You don't need to complete an entire course or earn a badge for this week's task.

## Slide 24

On Day 1, we changed a status and appended an event in separate calls. Here we put both changes in one update to one document.

For this example, I have a separate demonstration collection with ticket 1001 in the open state. The update uses $set for the new status and $push for event 5099. MongoDB applies those changes atomically within that document, so another reader won't see a partially applied version of this write.

The filter also requires status open. The first run reports one matched and one modified. After that, the status is in_progress. Repeating the same command reports zero and zero, so it doesn't append another event.

That repeat behavior comes from the expected-state filter. $push itself doesn't prevent duplicates.

If the event lived in another document, the operation would cross a document boundary. We would need to decide how to coordinate the ticket change and event creation. Multi-document transactions are available with suitable deployment and application design, but they add considerations of their own.

This is one concrete benefit of embedding. We'll weigh it alongside growth and independent access requirements.

## Slide 25

Let's separate a current fact from a historical fact.

The ticket's requester_id records which person opened it. That identifier can stay the same when the person changes their email address. If the page promises current contact information, we can retrieve it from one authoritative user document.

A field named requester_name_at_open has a different purpose. It records the name shown when the ticket opened. Keeping that old value after a later name change can be correct because the field intentionally preserves history.

The problem comes when we copy a value without stating which meaning it has. Someone reading a field called email may assume it's current, even if no process keeps the copy up to date.

For the lab's requirement, keep current contact details in one authoritative user record and explain how the page reaches it. A historical snapshot is optional and needs a clear purpose.

Also remember that requester_id is a reference we interpret. MongoDB doesn't automatically enforce a foreign key for it. The application needs rules for missing or deleted related records.

## Slide 26

Here the event is its own document, with ticket_id pointing to its parent ticket.

That direction matters. When another event arrives, we can insert another history document without adding another item to the ticket. We don't need an ever-growing list of event IDs inside the parent.

To retrieve the history, we query the event collection for the ticket ID. That keeps the ticket's size bounded while allowing the number of history records to grow.

The sketches use event_type and event_at, matching the source case. Their quoted timestamps are readable JSON text. In the runnable demo, Python datetime values become BSON dates so the query can order them as dates.

A reference doesn't fetch anything automatically. It also doesn't create an index or enforce the relationship. Those are separate parts of the design.

The next slide assembles a page from these separate records. As we walk through it, count the reads and notice what the application now has to handle when a related document is missing.

## Slide 27

We're now looking at an alternative version of the ticket page. Its separate fixture still has ticket 1001 in the open state.

This page uses three reads. We retrieve the ticket, retrieve its requester, and then query the event collection for that ticket's two most recent events.

The event query sorts event_at descending and uses event_id descending as a tie breaker. The limit returns two events. It leaves the rest of the history stored in the collection.

For this worked ticket, the output shows status open, Requester 101, and events 5002 then 5001. It only has two events. Your lab ticket has three, so you'll need to distinguish the two events displayed from the complete history retained.

These reads also have limits. The example assumes the ticket and requester exist. An application needs to handle a missing result instead of treating None as a document. And three independent reads don't automatically represent one shared instant if writes happen between them.

An index beginning with ticket_id and followed by the ordering fields is a candidate for supporting the history query. We haven't measured performance at scale here, so describe it as a design candidate rather than a benchmark result.

## Slide 28

Let's compare what grows in each design.

If we embed every event, the ticket document gets larger whenever history grows. A read can retrieve the whole ticket and its events, and related changes can fit in one atomic document update. But a page that needs only two events may be attached to a very large history.

A BSON document has a 16 MiB limit. That's a hard ceiling, not a sensible design target or a fixed number of events. Event sizes vary.

If events live separately, the collection gains documents while the ticket stays bounded. We gain independent history queries and take on extra retrieval and coordination work.

A hybrid can keep authoritative history separately and a small recent-events copy on the ticket. That can help the page, but someone must define how the copy stays current and what happens when it falls behind.

For this lab, a clear referenced design is a perfectly reasonable choice. Choose the simplest model you can explain that satisfies the page, contact-update, and history-retention requirements.

## Slide 29

When you explain a modeling decision, connect it to an operation.

For example: keeping current contact details in one user document means an email correction changes one authoritative record. Keeping history in separate event documents means new events don't enlarge the ticket. Those are specific benefits we can trace through the model.

Then explain the cost. The page retrieves related records, and independent reads may observe changes made at different times. If the application promises a consistent view across all of them, it needs a suitable coordination strategy.

Use the same care when comparing database systems. PostgreSQL supports arrays and JSON too. A relational system doesn't automatically normalize a schema for us, and joins aren't inherently unacceptable. Their cost depends on the data, query, and indexes.

MongoDB's flexible documents likewise need clear field meanings and rules. Choosing the product doesn't make those decisions for us.

In your response, name a requirement, explain the document boundary you chose, and describe the work that choice creates for the application. That gives the developer something concrete to evaluate.

## Slide 30

For Lab 2, complete Lesson 4, Modeling One-to-Many, and its Practice activity. My demonstration used Lesson 3. The weekly page links to both, so check the lesson number before starting.

Then revise one design for ticket 1003 using last week's case facts. The page needs its latest two events, newest first. The system must retain all history, and current contact details must be editable in one authoritative user record.

Show a representative ticket document. If related data lives elsewhere, include a small related-document example so the relationship is visible.

Write a short explanation for the developer implementing the page. Name the event IDs the page should display, explain how it retrieves them, and say where a contact correction happens. Also explain how the design handles fifty thousand events for this ticket.

Submit the JSON, explanation, and Lesson 4 Practice progress image in one Brightspace text response. Redact account details. If the platform is unavailable, use the chapter's worked examples and state that substitution. No full-course badge or additional application is required.

## Slide 31

You now have a small database experiment you can describe precisely.

You compared a query with the expected answer from a fixture. You found a case where conditions matched different array elements. You checked whether a write found a document, whether it changed anything, and what the document contained afterwards.

You also used a page's requirements to explain a document boundary. You can describe why current contact details belong in one place and why a growing history may need separate records, along with the retrieval and consistency work that introduces.

When you talk about the exercise, stay within what you actually tested. If you used local mode, say you tested the query logic locally. If you used Atlas, you can also explain your connection setup. Neither exercise establishes production performance or experience operating a large service.

Next week we'll aggregate results and enforce document rules. Keep bringing the same questions: what exactly are we asking, what result do we expect, and what evidence tells us the operation did what we intended?

## Slide 32

These three short videos review the week's examples. The first follows the array query and shows why conditions can match different events. The second compares write results and shows how a status change and an event can happen in one atomic update. The third compares embedding and referencing for a ticket page.

Each video is silent, with captions on screen. The diagrams are illustrations of the operations we've discussed. They aren't measurements of database performance.

You can use the videos to review a point that still feels unclear. Download the PowerPoint and open it in desktop PowerPoint to play the embedded videos from this slide. The weekly folder also has the individual MP4 files and subtitles. The PDF contains still thumbnails.

As you watch, follow one ticket through the example. Ask which document qualifies, what changes, and what evidence shows that the result is the one we intended.

## Slide 33

Both conditions appear somewhere in ticket 1001, but they belong to different events. Event 5001 supplies created, and event 5002 supplies agent.

The separate dotted conditions can therefore match the ticket. The $elemMatch version requires one event to supply both values. Neither event does, so ticket 1001 doesn't match that version.

Trace each condition to the event that supplies it. On the left, the two matches come from different events. On the right, neither event can meet both conditions. That is the difference our filter needs to express.

## Slide 34

Compare the first update with its repeat. Test ticket 1099 starts with status new and no assignee. The first $set finds it and changes its status and assignee. Repeating that same $set still finds it, but the values are already there. Matched stays one, while modified becomes zero.

These are selected fields from the document. Both operations still use the complete test filter, including the course and test-record markers. When we repeat this update, the ticket still meets the filter. In the expected-state example, the status condition changes which documents qualify. We need to distinguish those situations when we interpret a zero modified count.

## Slide 35

The write asks for ticket 1099 with status new. The saved ticket is already in_progress. Since the complete filter doesn't match, the requested change to resolved doesn't run.

The ticket can exist while a conditional update matches nothing. That distinction is the point of the example. The application can reload the current document and decide how to respond. The code expresses that expectation in the filter, and the two zero counts show that no document met it.

The diagram shows the ticket number and status condition. The complete test filter also keeps the test_record and course_fixture markers.

## Slide 36

We have two browser workspaces available, and it's helpful to know what each one is for.

The introductory MongoDB University lab provides an IDE in your browser, connected to an Atlas cluster. An IDE is a workspace where you write and run code. That introduction teaches you how to use the workspace without installing a local development environment. Think of it as a guided practice sandbox: read the lesson, try the operation, and inspect what happens.

Colab has a similar learning rhythm, but our work lives in a Python notebook that you save and edit. Today that notebook connects to your own Atlas cluster. Its optional mongomock mode is an in-memory simulation for practicing the query logic. It doesn't create an Atlas connection.

The second link is extra practice with databases, collections, and documents in Atlas Data Explorer. Data Explorer gives you a graphical way to work with those objects. Sign in or enroll to open the practice, then follow that lesson's current instructions for its account, tools, and data. Different lessons may use different environments, so the introductory IDE doesn't tell us exactly what this exercise will provide.

We may work through this optional practice together in class to become more familiar with the database and collection interface. You still complete Lab 1 in your Colab notebook. As you move between the interfaces, keep asking the same question: which database and collection am I working in, and what changed when I ran that operation?

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
