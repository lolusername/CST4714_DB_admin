# Week 10: Basic MQL and Document Modeling - Spoken Transcript

## Slide 1

Last week we represented the same ticket facts in different JSON shapes. We could read the text and discuss the design, but we had not yet asked a database to retrieve or change those facts. This week we take that next step. Our application is still the support portal. A resident needs to see the right ticket. An agent needs to change that ticket without accidentally changing someone else's request.

In our first meeting we will use a small notebook. Each query will have a visible result that we can compare with the supplied data. We will examine a query that appears reasonable but answers the wrong question about an event array. We will also distinguish finding a document from actually modifying it. Those distinctions are useful when an application reports that a request succeeded but the data looks unchanged.

In our second meeting we will connect these operations to modeling. A ticket page needs current status and recent events, but a person's contact information can change independently and event history can continue to grow. We will compare the work created by different document boundaries.

You do not need to create a complete application this week. The goal is to understand the data operations and explain one design choice using an actual workload. Local notebook mode remains available if your cloud connection is not ready.

## Slide 2

We already have a vocabulary for describing a database query. We choose a source, select the records we need, choose the fields to return, and sometimes order or limit the result. Those ideas are useful in MongoDB, even though the syntax and some semantics differ.

In the Python notebook, database followed by tickets in square brackets gives us a handle for the tickets collection. That handle is a Python object through which we send operations. A filter such as status equal to open is a dictionary. It is not a string containing a SQL WHERE clause. We pass the dictionary to the find method.

The projection is another dictionary. A one beside ticket_id asks for that field in the result. An explicit zero beside underscore id hides MongoDB's document identifier, which an inclusion projection otherwise returns by default. The ticket number and MongoDB's underscore id are separate identifiers in our fixture.

Sorting by ticket_id with one means ascending order. The limit selects how many matching results to return. We will put those pieces into complete Python expressions rather than trying to memorize this table alone.

The comparison has boundaries. Arrays are values within documents, and missing fields do not behave exactly like SQL nulls. A familiar concept is a starting point for reasoning, not a guarantee that punctuation is the only difference.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 3

This is an Atlas interface capture from August 2026. The deployment appears in the tree, but the main workspace still asks for a connection. That combination is worth understanding. Seeing a deployment in the management website does not establish that our Python program has successfully queried it.

An Atlas project groups cloud administration settings and resources. A cluster is the deployed database service. Within the database service, a database contains collections, and a collection contains BSON documents. Our notebook chooses a fresh database name and works in a collection called tickets. We are not creating a new cloud cluster for each notebook run.

The website login and the database user have different jobs. The website account lets a person manage the project according to their permissions. The database user authenticates a client connection and has permissions for database operations. Having one does not automatically mean that every action available to the other is allowed.

We also need a reachable network path. If the explorer has not connected, we cannot infer from an empty workspace that our application's collection is empty. We first establish the connection, select the intended database and collection, and then run a query whose meaning we understand.

The names in this capture are redacted. We are using it to locate the layers, not as a picture of a successful data operation or an exact promise about the placement of every current button.

Sources:
- course/textbook/figures/cloud_interfaces/atlas_data_explorer.png, course interface capture dated August 25, 2026.
- https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 4

A Colab notebook displays in your browser, but the Python code runs on a remote runtime. That distinction explains a common connection problem. The button that adds the current IP address in your laptop's Atlas browser may add your laptop's outgoing address. Atlas needs to allow the address from which the Python connection actually arrives.

The notebook therefore has a separate setup cell before the connection. If you choose Atlas mode, that cell asks a public IP service for the runtime's outgoing IPv4 address. It prints the address with slash thirty-two, which identifies one IPv4 address. It also prints a new practice database name. No database password is sent to the IP service.

In Atlas, add that printed address as a temporary entry and wait for it to become active. Use a database user with the required access to your practice database. Then copy the driver URI and enter it in the notebook's hidden prompt. Keep it out of ordinary source cells and printed output.

The connection cell sends ping. A response establishes that the server answered, but the later insert still has to succeed under the user's data permissions. Keep certificate verification enabled even when troubleshooting. A broad allow-everywhere rule or an insecure TLS option can conceal the real issue while weakening protection.

If the cloud path is unavailable, use local mode for the query lesson. We will distinguish that local exercise from having tested Atlas networking.

Sources:
- https://www.mongodb.com/docs/atlas/security/ip-access-list/
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/

## Slide 5

Several representations in this course resemble one another, so we need to keep their execution contexts clear. Strict JSON is a text format. Python has dictionaries and lists, with Python's own literals and function calls. Mongosh is a JavaScript-based database shell with its own helper functions.

In a Python dictionary, the missing-value literal is None, with a capital N. The Boolean literals are True and False. In JSON and JavaScript, the corresponding literals use lowercase spelling. Copying null into a Python cell does not turn it into the correct Python value.

The operation names also reflect the host tool. PyMongo uses find_one and modified_count with underscores. The shell uses findOne and modifiedCount. We will use Python in the slides and notebook. Chapter 10 explicitly labels its runnable shell listings, so the shell examples should run in a shell rather than being pasted unchanged into Colab.

Dates deserve particular attention. A string that looks like an ISO timestamp remains a string unless a conversion creates a typed date. Our Python fixture passes datetime objects through the driver. MongoDB stores those as BSON dates. In mongosh, ISODate constructs a date value. Neither function call is legal strict JSON.

The purpose is not to memorize every spelling now. Identify the environment first, then read the example in that environment. That habit prevents many apparent database errors that are really language errors.

Sources:
- https://www.mongodb.com/docs/manual/reference/bson-types/
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 6

These are the six tickets loaded by the notebook's setup cell. The table is small enough that we can reason about expected answers ourselves. That gives us a second way to check a query rather than accepting whatever the program prints.

Ticket 1001 is a high-priority streetlight request and is open. Ticket 1003 has urgent priority, but it is already resolved. Ticket 1004 is new and low priority. Those differences matter when a filter combines status and priority. A high or urgent priority alone does not establish that a ticket belongs in an active queue.

The notebook adapts the larger CSV case. It keeps selected fields, stores dates as Python datetime values for BSON conversion, and supplies nested requester details, tags, and small event arrays. Its event fields use the short names type and at. The original CSV uses event_type and event_at. The notebook explains that mapping rather than claiming it imported every original column unchanged.

Some event arrays are empty in this teaching fixture. That tells us which events the fixture supplies. It does not establish that the source ticket never had any history. A small example needs a stated scope just as a production dataset does.

We will later add ticket 1099 as a clearly marked disposable record. Keeping that test separate lets us check that an update or deletion leaves these six teaching tickets intact.

## Slide 7

This is a complete Python query to run after the notebook's connection and fixture cells. We first assign a dictionary to filter_doc. The status condition accepts new, open, or in_progress. The priority condition accepts high or urgent. Both field conditions must hold for one document to match.

That is why the result contains ticket 1001. It has status open and priority high. Ticket 1003 passes the priority condition but fails the status condition because it is resolved. Reading the filter as an intersection of requirements is more reliable than treating each line as an independent search whose results will somehow be combined later.

The projection contains underscore id with zero and two requested fields with one. The result therefore displays ticket_id and status. Those projection settings do not remove category, priority, or the event array from the stored document. They only control what this find operation returns.

The for loop iterates over the cursor from find and prints each returned document. On this fixture it prints one dictionary. If a filter returned three tickets, the loop would print three documents, still at the grain of one ticket per item.

For your own query change, choose a question that this fixture can answer and predict at least one returned ticket. The useful check is whether the selected fields and records answer that question, not whether the cell merely finishes without an exception.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 8

This query starts with the active statuses again, but now it returns opening time as well as ticket number. The sort expression contains two field-direction pairs. Opening time uses negative one, so later dates come first. Ticket number uses positive one as a tie breaker when two records have the same opening time.

The limit is two. In our fixture, the most recent active ticket is 1006, followed by 1004. Notice that 1005 has a recent opening time, but it is resolved and does not pass the filter. Sorting does not rescue a document that failed the predicate.

Find gives us a cursor. We configure that cursor with sorting and a limit before iterating. The loop then retrieves its results. After the loop has consumed the cursor, looping over that same exhausted cursor does not execute a new independent query. Calling find again creates another query cursor. For a small bounded result, converting a cursor to a list can also be convenient, as we will do in the page demonstration.

A deterministic tie breaker helps us explain an order instead of relying on incidental storage order. It is especially useful for repeated observations and pagination, although building a production pagination system requires further choices.

The sort and limit change the query result. They do not reorder the collection permanently or delete records beyond the limit.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/query/find/

## Slide 9

The first query reaches into a nested requester document. The dotted field name requester.user_id means that we look for user_id inside requester. The field name is a quoted string because the dot is part of the MongoDB path, not Python attribute access on a variable called requester.

On our fixture, user 101 requested tickets 1001 and 1005. The projection asks for only their ticket IDs. We can compare those IDs with the requester objects in the fixture to verify the relationship.

The second query searches the tags array. A scalar equality condition on that array field matches a document when its array contains the value safety. We do not need the entire array to equal the string safety. Here, tickets 1001 and 1005 both carry that tag, so the two queries happen to return the same IDs for different reasons.

That agreement does not make the conditions equivalent. A future ticket might belong to user 101 without a safety tag, or have the safety tag while belonging to a different requester. A database query states a rule, and the fixture is just one set of data against which we observe it.

The next example makes this distinction more important. Once an array contains documents, different conditions may be satisfied by different elements unless we explicitly require one qualifying element.

Sources:
- https://www.mongodb.com/docs/manual/tutorial/query-embedded-documents/
- https://www.mongodb.com/docs/manual/tutorial/query-arrays/

## Slide 10

Read the two event rows as separate facts. Event 5001 says that a resident created ticket 1001. Event 5002 says that an agent was associated with the assigned event. Neither row says that an agent created the ticket.

The tempting filter below asks for an events.type value equal to created and an events.actor_role value equal to agent. With these separate dotted predicates, MongoDB can find the created value in one element and the agent value in another element. The ticket satisfies both predicates at the document level.

If our actual application question was whether an agent created the ticket, that is the wrong answer. The query is syntactically valid and MongoDB is following its defined behavior. The error lies in how the query expresses the application's requirement.

This is why a small counterexample is valuable. If every ticket had just one event, the tempting filter might appear to work in every test. We deliberately keep a resident-created event and a distinct agent event in one array so the ambiguity becomes observable.

The same reasoning applies beyond support tickets. A product might have different sizes and prices in different variants. A person might have skills recorded at different proficiency levels. When multiple conditions describe the same related object, our filter must preserve that relationship between the conditions.

Sources:
- https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/

## Slide 11

The elemMatch operator puts the two conditions inside one requirement for an array element. We are asking whether the events array contains at least one element whose type is created and whose actor_role is agent. Both conditions must hold in that same event object.

The result is an empty list. That is the correct result for the supplied fixture because every supplied created event has resident as its actor role. An empty answer is not automatically an error. We judge it against the question and the data.

The notebook also asks for a status_changed event whose actor_role is agent. That version does match tickets 1002 and 1003. It shows that elemMatch is not simply a way to make results disappear. It expresses the requirement that related conditions describe one element, and the data may or may not contain such an element.

There is another boundary to remember. ElemMatch in this filter decides whether the ticket document qualifies. It does not automatically trim the returned events array to only the matching event. If the projection includes the full events field, the document can contain other events as well. Shaping array output is a separate operation.

In your explanation, use event IDs and field values rather than only repeating the phrase same element. A concrete pair of rows shows that you understand why the two queries differ.

Sources:
- https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/

## Slide 12

We need a safe target for write practice. This block uses ticket 1099 and requires two additional markers: test_record is true and course_fixture is cst4714. The filter is deliberately more specific than a status or category that several real tickets could share.

The first deletion resets only matching test records in our private practice collection. We then insert a new document in status new with an empty events array. The double asterisks copy the fields from test_filter into the new Python dictionary. That syntax is Python dictionary unpacking, not a MongoDB operator. It lets the inserted document carry the same identity and markers that the filter uses.

This setup is an explicit reset. If you run it again, you are starting the write experiment over. To observe a repeated update, run the update cell twice without rerunning this insertion cell between the two executions. Otherwise you would keep recreating the initial state and never observe the second case.

The notebook has also created a unique index on ticket_id. MongoDB's generated underscore id alone would not prevent two documents from sharing our domain ticket number. Protecting ticket_id makes the intended one-ticket target unambiguous within this exercise.

Everything here belongs to a new practice collection. Do not substitute an Atlas sample collection or your final project's production data for this disposable target.

## Slide 13

Now we call update_one with the exact test filter and a set operator. The set operator names status and assignee_id. It changes those fields while keeping the other fields in the document. This is different from replacing the whole document with a smaller dictionary.

The first execution finds test ticket 1099 in its initial state and changes the two values. The result reports one matched document and one modified document. The follow-up read shows status in_progress.

Run the same update again, with no intervening reset. The identity and test markers still match the same document, so matched_count is one. But the document already contains the values requested by set. There is no new change to make, so modified_count is zero. The status still reads in_progress.

Those counts answer different questions. A zero modified count alone cannot tell us whether the filter found nothing or the requested values were already present. We inspect matched_count too, then read the state that the application actually cares about.

These counts are document counts, not numbers of individual fields changed. Changing status and assignee_id in one document does not produce a modified count of two. We still modified one document. This distinction will help us interpret write results in larger applications without guessing from an ambiguous zero.

Sources:
- https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/update/

## Slide 14

This operation adds status new to the identity and marker conditions. It expresses an expected current state: change this test ticket to resolved only if it is still new. Our previous operation already moved the document to in_progress.

The result is therefore zero matches and zero modifications. The status remains in_progress. Unlike the preceding repeated set, this request did not find a document satisfying its complete filter. It did not find the document and decide that the replacement value was already present.

An expected-state predicate can be useful when two application actions might otherwise overwrite each other. MongoDB rechecks the condition as part of the single-document write. If an earlier action has already changed the state, a later action with the old expectation can observe that it no longer applies.

The application still needs a policy for that outcome. It might reload the ticket, report that the state changed, or ask the user to reconsider the action. We should not silently treat every zero match as success. Nor should we call every zero match a broken network connection.

This is a small state-transition example, not a complete concurrency or retry protocol. The important beginner skill is to describe what the filter permits and then compare that permission with the state actually stored when the write runs.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 15

The push operator appends a value to an array. Our value is a small event document. If we sent an unconditional push twice, the array could contain two copies of that event. The fact that an event has an ID field does not automatically make the elements in an embedded array unique.

This filter therefore also requires that events.event_id is not 5999. On the first execution, the array lacks that event ID, so one document matches and changes. After the append, repeating the same request finds no document satisfying the guard. The second result is zero and zero, and there is still just one event 5999.

That behavior is useful, but keep its scope precise. It protects this single-document example from appending the same identified event again through this operation. Other writers need to follow compatible rules, and a complete distributed event system has additional failure and ordering concerns.

Also notice that the earlier status update and this append are two different operations. Each individual operation is atomic for its document, but there is a gap between the two calls. A reader in that gap could see the new status without the new event.

In the next meeting we will combine a status change and an embedded event append in one update. That connection between operations and document boundaries is one of the reasons modeling belongs in a database-administration course.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 16

The deletion uses the same exact test filter. First we read the target with a small projection, so the displayed identity is easy to inspect. Then delete_one removes one matching document. The result reports one deletion, and the follow-up find_one returns None because the test record is absent.

We also count the other course fixture tickets. There should still be six. That comparison gives us a simple scope check in addition to checking that the unwanted test record disappeared. The six records are still available for query practice until the final cleanup cell removes this run's practice collection.

Repeating the same delete reports zero. The filter is still narrow and valid, but its target has already gone. That is another example of an expected repeat result rather than a syntax failure.

Avoid an empty filter when the requirement is to delete one particular ticket. An empty dictionary matches every document. Delete_one with an empty filter can remove some matching record without establishing that it is the intended one. Delete_many with an empty filter removes all matching records.

Finally, a preview query is not a lock. Another writer can act between the preview and deletion. In this private exercise we control the fixture. In a shared application, expected-state conditions and suitable transaction or concurrency rules may be necessary. Previewing is a useful habit, but it does not itself create a transactional guarantee.

## Slide 17

The first lab stays in one notebook. Begin with its worked query and then change one filter so it answers a different question about the six tickets. Add one useful field to the projection. Choose a returned ticket and explain why it belongs in that answer.

Next, compare the array predicates using the actual event objects. The useful part is the difference between a resident-created event and a separate agent event in one ticket. Your explanation should connect the data to the observed query results.

For the write experiment, run the set cell twice without rerunning test insertion. Observe one match and one modification, then one match with no modification. Compare those with the expected-state update, which does not match the already changed ticket. Run the targeted deletion and inspect the remaining data.

Complete the notebook's short explanation cell rather than creating a separate report. Include whether you used the local path or Atlas so your account of the experiment is accurate. Both paths support the required query lesson, but only the Atlas path tests your hosted connection.

Before finishing, run cleanup and remove any accidentally saved credential. If you used Atlas, also remove the temporary network entry and any class-only database user when no longer needed. You submit the completed notebook. There is no additional screenshot or repository task for this lab.

## Slide 18

We now have a way to ask documents questions and observe their changes. Today we use that understanding to design the ticket page. The page needs the ticket's current status and recent events. The system also needs to keep the full history, including events the page does not currently display.

A resident's contact information has a different pattern of change. The resident might correct an email address once and expect future ticket pages to use the corrected value. If we copied the current email into every ticket, the update requirement would cross many documents.

Those requirements do not point to a single universal document shape. They tell us which costs we should compare. Putting related data together can make a read convenient and can bring related changes into one atomic document write. Keeping a shared identity or growing history separate can make independent changes and retention easier.

The live example will use one-to-one relationships. Your individual practice will use one-to-many relationships and then revise one ticket design for the latest-events requirement. We will not repeat the complete JSON exercise from last week or ask you to build a full web application. The new work is explaining how the chosen shape serves concrete reads and updates.

## Slide 19

Cardinality describes how many entities can participate on each side of a relationship under the application's rules. Many tickets may refer to one requester. One ticket may have many events. In the small publisher example, we will assume that a publisher has one headquarters and that the headquarters belongs to that publisher.

These statements describe relationships, not storage decisions. A one-to-one relationship can appear as fields inside one document, a nested subdocument, or separate referenced documents. A one-to-many relationship might involve a small fixed set or years of accumulating records. The word many does not tell us which of those situations applies.

For a requester, the independent user identity and contact changes matter. For ticket events, the growth and the need to query history independently matter. For one owned headquarters address, a bounded nested object can be convenient when the publisher details are normally read together.

We should also make assumptions explicit. A company could have more than one location. If we call the relationship one-to-one, we must be clear that the field means the one designated headquarters in this example, not every office the company operates.

This is familiar relational reasoning carried into document design. We still ask what each entity means and how the relationships work. We then choose the document boundary using the reads, writes, ownership, and expected growth rather than cardinality alone.

## Slide 20

The live MongoDB University resource is Lesson 3, Modeling One-to-One, in Modeling Data Relationships. We will use that lesson's one-to-one material and its practice as the instructor example. Your assigned interactive activity is Lesson 4, so you will apply the reasoning to a different relationship.

This small publisher document illustrates a possible shape. The headquarters address lives as an object inside the publisher. If the application normally loads that address with the publisher, and the address belongs only to this publisher under our stated assumptions, the embedding can keep the relevant facts together.

Another design could store the address separately and put an address identifier in the publisher document. That could be reasonable if the address had an independent lifecycle, permissions, or queries that justified the separation. Merely having a one-to-one relationship does not forbid either representation.

The example text here is our own small illustration, not the supplied answer to a vendor practice question. As we work through the live resource, we will connect its example to these ownership and access considerations.

The unit names matter. MongoDB University sometimes reuses a video in a newer course package. Choosing two differently named courses does not automatically give us two different activities. Our boundary today is explicit: one-to-one practice in the demonstration, one-to-many practice for your individual work.

Sources:
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-3-modeling-one-to-one/learn
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn

## Slide 21

This fresh demonstration collection contains ticket 1001 in status open. The update document has both a set operator and a push operator. Set changes the current status to in_progress. Push appends the status-change event to the embedded events array.

Because both changes are part of one write to one document, they form an atomic document update. A reader does not observe only half of this particular write. That is different from Day 1's two separate calls, where the status changed before the append ran.

The filter includes the expected current state open. On the first execution, the demonstration document matches and changes. Repeating the update no longer matches because its state is in_progress. The repeat does not append a second copy of the event. This follows from the specific state condition and operation, not from a universal rule that push prevents duplicates.

If the event lived in another document, changing the ticket and inserting that event would cross a document boundary. We would need to decide how to coordinate them. MongoDB supports multi-document transactions, but using them has costs and requires an appropriate deployment and application design. We are not implementing that full mechanism in this beginner example.

Single-document atomicity is one modeling consideration. It does not justify growing one document without limit or copying every shared fact into it. We need to consider those requirements together.

Sources:
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 22

Consider a resident who changes their email address. The ticket's requester ID should not change, because the person's identity has not changed. The current email belongs in an authoritative user record if the requirement is to correct it in one place.

The page can read the ticket, obtain the requester ID, and read that user's current contact information. This requires another retrieval, but it avoids maintaining many copies of a fact that the application promises is current.

A historical name has a different meaning. Suppose a business needs to retain the name shown when a request opened. A field named requester_name_at_open can deliberately record that snapshot. Keeping its original value after the person changes their current display name may be correct. We should not call that historical field stale simply because it differs from the current profile.

The error is to mix the meanings without stating them. A field that the application presents as the current email should follow the current-contact rule. A historical snapshot should be named and explained as historical. The database cannot infer which interpretation the designer intended from a vaguely named string alone.

A reference also does not create an automatic foreign key. Storing requester_id 101 does not by itself guarantee that a user document with that ID exists. The application needs an appropriate rule for creating, updating, and deleting related identities.

## Slide 23

Here the ticket keeps its own fields and requester ID. Each event is a separate record with a ticket_id that identifies the ticket it belongs to. When a new event arrives, the system can add another event document without adding one more event object to the ticket itself.

Notice that the ticket does not need an array listing every event ID. Such an array would move the growth problem rather than eliminate it. If every child event carries ticket_id, we can query the event collection for one ticket's history. The parent remains bounded even while the number of event records grows.

The example shows event 5002 and uses the source-case field names event_type and event_at. It is a JSON sketch, so the timestamp is a string. In the runnable page demonstration, the driver stores event_at as a BSON date using a Python datetime. That allows us to sort consistently by a typed date rather than relying on every string following a compatible format.

A reference names a relationship. It is not the same as automatically enforcing referential integrity, automatically creating an index, or automatically loading the referenced document. Those are separate design and implementation responsibilities.

The next slide performs the actual retrievals. It will show the extra work needed to assemble a page from related records, which is the main read-side tradeoff of this simple referenced design.

## Slide 24

This demonstration reads the ticket page in three steps. First it finds ticket 1001. Next it reads the person identified by that ticket's requester_id. Finally it queries history records whose ticket_id matches the ticket and returns only the two most recent ones.

The history sort orders event_at descending, with event_id descending as a tie breaker. Limit two caps the number returned to the page. It does not delete older events from the collection. Our worked ticket has two events, so the displayed order is 5002 followed by 5001. Your lab ticket has three events, which makes the difference between displaying recent history and retaining full history observable.

The example assumes the ticket and person exist in the supplied fixture. A real application should handle a missing ticket or a broken reference rather than indexing into None. The simple demonstration lets us focus on the intended data path before adding every production error branch.

These reads also occur separately. A concurrent contact change or ticket update could happen between them, so this code does not provide one atomic snapshot across all three collections. Whether that matters depends on what the page promises.

An index beginning with ticket_id and then the ordering fields can support this history access pattern. It is a design candidate, not a measured performance claim for our tiny collection. We will continue connecting queries, indexes, and actual observed work in later lessons.

## Slide 25

There are several defensible ways to handle event history. Embedding every event makes the ticket and its history convenient to read together, and a related status change and append can be one document update. But each event enlarges the same ticket document.

MongoDB's maximum BSON document size is sixteen mebibytes. We should not treat that limit as a performance target. Large documents, frequent updates, and the need to inspect only a small part of history can become awkward before the hard limit is reached. The limit also does not translate into one universal maximum number of events, because event sizes vary.

Keeping all events separately leaves the ticket bounded. The page retrieves a limited, ordered subset of history, and a report can query events across tickets. The cost is extra retrieval and coordination when an application operation changes both the ticket and an event record.

A hybrid could keep the authoritative history separately and copy a small recent-event preview into the ticket. The preview needs a cap and a refresh rule. We must decide what happens when its refresh fails or arrives late. Copying data introduces work even when the read becomes convenient.

For a beginner project, choose the simplest design that meets the stated requirement. A hybrid is not a required upgrade or a sign that a project is more sophisticated. An accurately explained referenced model can be a stronger solution.

Sources:
- https://www.mongodb.com/docs/manual/reference/limits/

## Slide 26

A modeling recommendation should explain a concrete consequence. Keeping the authoritative user record separate means that a contact correction updates one place. Keeping complete event history separate means that each new event increases the event collection rather than the ticket document. Those are useful properties for the stated workload.

They also have costs. The page must retrieve related records, and independent reads can observe different moments if concurrent writes occur. If the page requires a consistent version of all those facts, the application needs a stronger coordination approach than the three plain reads we just showed. If eventual consistency is acceptable for a recent-events preview, the application should state that promise rather than accidentally delivering it.

We should apply the same rigor to vendor comparisons. Relational database design also considers workloads. PostgreSQL supports arrays and JSON, and SQL systems do not force every schema to be in third normal form. Normalization is a design discipline, not a setting imposed automatically on every table. Joins have costs that depend on the query, data, and indexes; they are not inherently unacceptable.

Likewise, MongoDB's flexible document structure does not remove the need to define meaning or enforce rules. We can appreciate the benefits of each system without treating an introductory vendor simplification as a universal technical fact.

In your design response, name a benefit and the work required to obtain it. That is more informative than simply calling a model flexible, modern, or scalable.

Sources:
- https://www.postgresql.org/docs/current/arrays.html
- https://www.postgresql.org/docs/current/datatype-json.html
- https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 27

Your individual MongoDB University activity is Lesson 4, Modeling One-to-Many, including its Practice activity. The weekly guide has direct links to both the lesson and practice page. The instructor example used Lesson 3, so you are not repeating the same assigned activity. A complete course badge is not required.

After the practice, revise one JSON design for ticket 1003. Use the same CSV facts you met last week, but apply the new requirement: the page displays only the latest two events, newest first, while the system retains the entire history. The current contact details must be editable in one authoritative user record.

You are not writing two new competing JSON files or building a web application. Show one representative ticket document. If related facts live elsewhere, include a small example of that related document so the relationship is understandable. In a short explanation to the developer implementing the page, name the two event IDs the page should show and explain the retrieval and contact-update path. Also explain how the design behaves if the ticket eventually has fifty thousand events.

Submit the JSON and explanation as one Brightspace text response, with the Lesson 4 Practice progress image. If the external platform or account access fails, use the chapter's worked examples and state that substitution in the same response. The design work still matters, but there is no need to invent a score or complete the entire vendor course.

Sources:
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn
- https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1

## Slide 28

This is one way to describe the skill in a professional conversation. It begins with something specific: testing a query against a fixture. It names an actual mistake, the array predicate that can combine conditions from different events, and explains how a counterexample exposed that mistake.

The description then connects write-result counts with a follow-up read. That is more credible than saying only that you know CRUD. You can explain the difference between a request that changed a document, a request whose desired values were already present, and a request whose expected-state filter no longer matched.

Finally, it explains a modeling decision in terms of the application. Shared contact details and growing event history create different requirements. A good answer acknowledges the extra reads and consistency choices rather than promising that one representation is always faster.

Adapt that language to what you actually performed. If you used the local teaching substitute, say that you tested the query logic locally. Do not imply that you operated a production Atlas service or measured large-scale performance. If you successfully connected to Atlas, you can also describe the separate database user, runtime IP rule, and secure connection setup you used.

The next lesson builds on these foundations. We will aggregate results across documents and enforce document rules. Keep the same habit: state the question, identify the unit of data, predict an observable result, and check what the system actually did.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
