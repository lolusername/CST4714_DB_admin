# Week 11: Aggregation, Validation, and MongoDB Index Design - Spoken Transcript

## Slide 1

This week we will work on a request summary that looks believable but can still be wrong. Imagine that a manager opens a dashboard and sees three active requests. The application responds successfully, and the number seems reasonable. Neither fact tells us which requests the dashboard actually counted. A duplicate can cancel out a missing record and leave a reassuring total.

Our first class follows the data closely enough to discover that mistake. We will begin with four tickets, trace a summary through its stages, and add a useful calculation. Then we will require a real opening date when the application writes a document. The notebook supplies the starting code so that the main work is understanding and modifying it, rather than building a connection library from scratch.

Our second class examines an ordered queue. A page needs only twenty requests, but the database might examine thousands to find them. We will compare a query before and after a compound index, preserving its result while changing how the database obtains it.

Chapter 11 explains the same ideas in more detail. The reading and the notebook are connected parts of the lesson. By the end, we should be able to explain a result, identify the boundary of a validation rule, and support an index decision with measurements rather than product claims.

Sources: Course textbook Chapter 11; Notebook 07; Week 11 assignments and implementation guide. The ticket cases are synthetic course examples.

## Slide 2

This SQL query gives us a familiar starting point. The source is the tickets table. The WHERE condition keeps records whose status belongs to our definition of active: new, open, or in progress. GROUP BY combines those surviving records by category. COUNT star counts the input rows in each category, and ORDER BY makes the displayed order predictable.

The important conceptual change happens at grouping. Before grouping, each row represents a ticket. After grouping, each row represents a category summary. A summary row cannot automatically retain a particular ticket's subject, because several different tickets may contribute to that row. We would need to decide what such a subject should mean before adding it.

MongoDB's aggregation pipeline will express this calculation through an ordered list of stages. The syntax changes, but our responsibility for defining the counted unit remains. In particular, counting rows after a one-to-many join can count related events rather than tickets. Expanding a document array can create a similar problem.

This query does not join any events, so the four-ticket case has a simple independent answer: one active sanitation ticket and two active streetlight tickets. We will carry that expected answer into the MongoDB example. Agreement between the two representations is useful here because we know exactly which records and which status definition each calculation uses.

Sources: Original course SQL example and four-ticket fixture. PostgreSQL SELECT documentation: https://www.postgresql.org/docs/current/sql-select.html

## Slide 3

These are the four documents in today's notebook, displayed as a table so that we can inspect the relevant fields together. The notebook also supplies subjects and small event arrays. These records are a fresh teaching case. Some identifiers resemble earlier course examples, but we should use today's values rather than assume that every earlier fixture is unchanged.

Ticket 1001 is an urgent streetlight request with status open. Ticket 1002 is a sanitation request in progress. Ticket 1003 is another urgent streetlight request, but it is resolved. Ticket 1004 is a new streetlight request with low priority. Our active definition includes the first, second, and fourth tickets. It excludes 1003 without deleting that ticket from storage.

There are therefore two active streetlight requests, but only one of them is urgent. The newest of those active streetlight requests opened on February fourth. These observations come directly from the source records. They give us checks that do not depend on getting an aggregation expression right.

The dates in this display are abbreviated for readability. The notebook constructs timezone-aware Python datetime values and the driver stores BSON dates. We will later compare those typed values with strings that merely look like dates. The display can look similar even when the stored types have different consequences for validation and application code.

Sources: course/notebooks/07_aggregation_validation.ipynb, four-ticket fixture. PyMongo date handling: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/dates-and-times/

## Slide 4

This diagram follows the summary from its source to its final display. The collection supplies four ticket documents. Match keeps the three active tickets. Group then creates two category summaries. Project gives those summaries the field names we want to return, and sort arranges them alphabetically by category.

The numbers change from four to three to two. Those changes mean different things. Match removes an ineligible ticket from this query's stream. Group combines eligible tickets into summaries. Project and sort leave the number of summaries unchanged in this particular pipeline.

The label under each stage describes its grain. Grain is simply what one result represents. Before grouping, one result represents one ticket. After grouping, one result represents one category. This distinction explains why a later stage cannot treat the grouped results as though each were still a complete original ticket.

The notebook runs successively longer prefixes of the pipeline. That lets us see the actual documents after match, after group, and after the remaining stages. We do not need to infer every intermediate value from the final report. This pipeline intentionally has no unwind stage because the requested summary counts tickets. Later, we will expand events for a different purpose and see why inserting that operation into this report changes the calculation.

Sources: Original editable course diagram, revised to the Notebook 07 fixture. Aggregation pipeline: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/

## Slide 5

The first Python variable holds a filter document. The outer key names the status field. The in operator checks whether that field's value belongs to the supplied list. Each of our active status strings appears exactly as the fixture stores it. A different spelling would be a different value.

We place that filter inside a match stage and pass a one-stage list to aggregate. Converting the returned cursor to a list gives us the result documents for this small example. The final Python expression extracts their ticket identifiers and sorts those identifiers for an easy comparison. That Python sort is only a display convenience here. It is separate from a MongoDB sort stage.

The result is 1001, 1002, and 1004. Each surviving document still represents one complete ticket. Match has not changed their subjects, categories, or event arrays. The resolved ticket still exists in the collection and remains available to a different query.

This difference between selection and mutation matters when diagnosing an application. A request missing from an active queue might have an excluded status, rather than have been deleted. We can inspect the ticket directly by its unique identifier to distinguish those possibilities. For this lesson, all the stages in our reporting pipeline compute results without writing them back to the collection.

Sources: Notebook 07 fixture and pipeline. Match stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/

## Slide 6

The group stage introduces a new result structure. Its underscore-id expression defines the grouping key. Here the expression is dollar-category, which means to read the category field from each incoming ticket. Tickets with the same category value contribute to the same group.

Active count uses sum with the constant one. Every ticket reaching a group contributes one. We are not adding a stored field called one, and we are not counting every document in the original collection. The previous match stage already determined which tickets arrive here.

The dollar sign in the field expression is significant. With dollar-category, the output has a sanitation group containing one ticket and a streetlight group containing two. If we accidentally write the constant string category without the dollar sign, every active ticket receives the same grouping key. The pipeline can still run, but now it produces one group labeled category with a count of three.

That mistake illustrates why successful execution is only the beginning of a check. The database can evaluate a valid expression that answers the wrong question. We compare the group keys and counts with the four known input records. We also avoid assuming a display order at this stage, because grouping alone does not specify that sanitation must appear before streetlight.

Sources: Original fixture-derived results. Group stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/ Field paths: https://www.mongodb.com/docs/manual/core/field-paths/

## Slide 7

We now assemble the full baseline pipeline. The first stage selects active tickets. The second is the group stage we just defined. The project stage then shapes the grouped result for someone reading the report.

At this point underscore-id contains the category value chosen by group. It no longer means the original ticket document's identifier. The expression dollar-underscore-id reads that grouped value and assigns it to a clearly named category field. The zero beside underscore-id suppresses that field in the output. The one beside active count includes the count that already exists.

Finally, sort arranges the category values in ascending order. On our fixture, the result has sanitation with one active request, followed by streetlight with two. The table shows the fields returned by the pipeline, not an additional table stored in the database.

The pipeline is a Python list containing command dictionaries. Each stage receives the previous stage's output. If we later add a new calculated field to group, we also need to consider the projection. An inclusion projection can hide a correctly calculated value when that field is omitted from the requested output. The lab will give us a concrete reason to update both stages together: we will add urgent count and newest opening while retaining the original active count.

Sources: Notebook 07 pipeline. Project stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/ Sort stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/

## Slide 8

The manager now wants more than a total. The report should include the number of urgent active tickets and the latest opening date in each category. We can calculate both while the group stage still receives individual active tickets.

Urgent count uses a conditional expression inside sum. The equality expression compares the incoming priority field with the constant string urgent. Cond returns one when that comparison is true and zero otherwise. Sum adds those contributions for the category. On the active streetlight inputs, ticket 1001 contributes one and ticket 1004 contributes zero.

Newest opening uses max on the opening-date field. Because our fixture stores consistent BSON dates, the greatest value represents the latest instant among those inputs. This expression gives us the date itself. It does not automatically return the entire ticket that has that date. A request for the complete newest ticket would require a more specific design.

In the notebook, we will add these two expressions to the existing group stage rather than replace active count. We will also include urgent count and newest opening in project. The active filter remains at the beginning, so the resolved urgent ticket never contributes to the calculation. These edits make a useful extension while preserving the report's original meaning: one summary per category of active tickets.

Sources: Course worked extension. Conditional expression: https://www.mongodb.com/docs/manual/reference/operator/aggregation/cond/ Sum: https://www.mongodb.com/docs/manual/reference/operator/aggregation/sum/ Max: https://www.mongodb.com/docs/manual/reference/operator/aggregation/max/

## Slide 9

This table is the expected extended summary. Sanitation has one active ticket, zero urgent tickets, and a newest opening on February second. Streetlight has two active tickets, one urgent ticket, and a newest opening on February fourth.

We can explain the streetlight row without referring to the aggregation syntax at all. Its source identifiers are 1001 and 1004. The first is urgent and opened on February first. The second has low priority and opened on February fourth. Counting those records gives two, counting the urgent member gives one, and comparing their dates gives February fourth.

Ticket 1003 is useful because it can expose a mistake in the filter. It is urgent and belongs to streetlight, but its resolved status makes it ineligible for every calculation in this active summary. If we count it in urgent count but exclude it from active count, the columns no longer describe the same population.

Checking a report means checking those shared definitions as well as its arithmetic. A column name alone cannot establish what was counted. Our explanation should identify the included source records and the condition that selected them. In the lab, the notebook's explanation cell is where we connect those facts to the actual output from our modified pipeline, including any unexpected result we had to correct.

Sources: Original calculations from Notebook 07's four-ticket fixture. No external operational dataset or measured production outcome is represented.

## Slide 10

The events field is an array inside each ticket. Ticket 1001 contains a created event and an assigned event. Ticket 1002 contains one created event. Ticket 1004 has an empty array. We will now ask for event rows, which is a different unit from the ticket summary.

Unwind emits a document for each array element and makes that element available in place of the array within the pipeline. Project keeps the ticket identifier and reads the event's type. The final sort orders by ticket identifier and then by event type. That alphabetical order puts assigned before created for ticket 1001. It does not claim that assignment happened first in time.

The resulting identifiers are 1001, 1001, and 1002. Ticket 1004 contributes no row because this default unwind does not preserve its empty array. We now have three rows describing three events on active tickets.

The operation is useful when events are what we want to analyze. For example, counting event types requires access to individual events. But placing this stage before our ticket count would allow a ticket with several events to contribute several times. The output still has a ticket identifier field, so merely seeing that field does not mean each ticket appears once. We must interpret the grain from the operation and the actual records.

Sources: Notebook 07 event arrays. Unwind behavior: https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

## Slide 11

Here is the trap in full. The active-ticket list contains 1001, 1002, and 1004. The expanded event rows contain 1001, 1001, and 1002. Both lists have length three. A test that checks only the grand total would pass even though one ticket was duplicated and another disappeared.

This fixture is more deceptive than a simple inflated total. Both category counts also happen to match. The correct active-ticket report has two streetlight tickets and one sanitation ticket. The event rows also contain two streetlight rows and one sanitation row, but the two streetlight rows both belong to 1001.

Urgent count reveals the problem. Ticket 1001 is urgent, so both of its event rows would contribute to a conditional sum. The mistaken report would say two urgent streetlight requests when only one active streetlight ticket is urgent.

Preserving empty arrays would retain a row for 1004, but it would leave both rows for 1001. That option does not turn an event stream back into a unique-ticket stream. For our report, the simplest correct approach is to count tickets before expanding events, or avoid expansion entirely. More complex reports can deliberately deduplicate by a stable ticket key, but they must also decide how tickets with no events enter the result. The needed operation follows from the intended population.

Sources: Original counterexample and computed identity lists from Notebook 07. Related mechanism: https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

## Slide 12

A report is easier to interpret when its input types have clear rules. MongoDB allows us to define a focused document validator rather than assume that every document must have an identical complete structure. The baseline rule in our notebook requires a ticket identifier, a recognized status, and a subject. Other fields can still appear.

Required means that a named field must exist. That declaration alone does not tell us whether its value has an appropriate type. A type rule describes the value. A date type rule, for example, distinguishes a BSON date from text that happens to contain a date-like sequence of characters.

An enum restricts a field to a supplied set of values. Our status list includes new, open, in progress, resolved, and closed. It prevents an unsupported value such as almost done. It does not establish which transition is allowed from a previous status. A system that must prevent reopening a closed ticket needs an additional application or database rule designed around that transition.

These distinctions keep the scope of a rule understandable. Requiring a BSON date does not prove that the ticket really opened at that instant. A date in the distant future could still have the correct type. We will implement the small, explicit rule that this lab needs, then describe both its protection and its limits.

Sources: Schema validation: https://www.mongodb.com/docs/manual/core/schema-validation/ Specify allowed field values: https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/#std-label-schema-validation-json

## Slide 13

This dictionary describes the baseline validator. The outer jsonSchema key tells MongoDB which kind of rule document we are supplying. The object type applies to the document itself. The required list names the fields that must be present, and properties describes the constraints on particular fields.

Ticket identifiers may use either of the listed BSON integer types. Status must match one of the strings in the enum. Subject must be a string. Notice that category, priority, events, and opening date do not appear in the required list yet. The rule deliberately leaves those fields optional at this point in the exercise.

We are writing Python, but the dictionary is a description of MongoDB's validation behavior. Python does not start rejecting database inserts simply because we created a variable called validator. A separate command installs the rule on the collection. This is similar to writing a SQL constraint statement in an editor versus executing it against a database.

We also should not treat this as interchangeable with every standard JSON Schema implementation. MongoDB's bsonType vocabulary includes database-specific values such as date and the integer types shown here. The driver translates our Python dictionary into the command sent to MongoDB. Understanding that boundary helps us distinguish a Python syntax error, an unsupported command, a permission failure, and an actual rejected document.

Sources: Notebook 07 baseline validator. JSON Schema validation: https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/

## Slide 14

The new requirement has two parts. We add opened-at to the required list, and we give that property the BSON date type. If we added only the property rule, a document could omit the field. If we added only the required declaration, a document could include a value of the wrong type.

The first three Python lines modify the dictionary. They are an equivalent way to make the edits that the notebook asks us to place in the original validator cell. Assigning the complete required list also avoids appending the same field repeatedly when we rerun this demonstration.

The command then installs the revised validator on tickets. CollMod changes collection settings. Strict and error specify the enforcement behavior used in this lesson. Our Atlas database user must have permission for this operation, separately from permission to connect or read documents. A successful ping does not establish that permission.

This command is for a real MongoDB connection. The notebook's default local mode uses mongomock, which does not enforce the collection validator. Its code explicitly skips installation rather than pretend that a printed message proves server behavior. All four baseline tickets already contain dates, so our small fixture is compatible with the added rule. On an existing application collection, we would inspect old data and plan a migration before tightening a rule that could affect later writes.

Sources: Notebook 07 date extension. collMod: https://www.mongodb.com/docs/manual/reference/command/collMod/ Validation level: https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/

## Slide 15

The test set includes one allowed document and three documents that differ in specific ways. The allowed document has a new status and a real date. The invalid-status document uses almost done. The text-date document contains date-shaped text instead of a BSON date. The final document omits the opening date entirely.

The notebook tests these records separately, using distinct identifiers. That separation helps us connect a rejection to the condition we intended to test. It also avoids confusing a duplicate-key error with a validation failure. The test cell clears its own temporary identifiers and removes test records afterward so that our four-ticket summary remains a four-ticket exercise.

The text-date and missing-date cases activate after we have added and reinstalled the date rule. Before that change, the baseline schema did not require a date, so we should not claim that those inputs failed for violating a rule that did not exist.

In Atlas mode, the database actually attempts each insert. A document-validation error is different from a network or authorization error. In local mode, the notebook supplies a clearly labeled trace for us to interpret. We can explain the expected decision from the rule, but we cannot describe that interpretation as a live server test. The learning goal is precise reasoning about the input and rule, with an accurate account of which execution path we used.

Sources: Notebook 07 test cell. Handling invalid documents: https://www.mongodb.com/docs/manual/core/schema-validation/handle-invalid-documents/

## Slide 16

Lab 1 stays within one notebook. We will extend the active-ticket summary, add the required opening-date rule, and explain the counting error using the source identifiers. The submission is the completed notebook with our changes, outputs, and the short explanation in its existing explanation cell. There is no separate report or repository to create.

The default local path lets us begin the aggregation work immediately after package installation. If we choose Atlas, the notebook prints the public IPv4 address of the runtime that executes our code. In Colab, that runtime is on Google's infrastructure, so it can differ from the address of the laptop running the browser. The temporary slash-thirty-two rule allows that individual IPv4 address. The database URI belongs in the hidden prompt rather than in a visible code cell.

When the experiment is finished, the cleanup cell drops the tickets collection in this notebook's uniquely named practice database and closes the client. It does not delete an Atlas project or shut down the cluster. We also remove the temporary network rule that we added for this runtime.

The explanation should describe the streetlight inputs, the effect of expanding events, and the date rule's boundary. If a result differs from the expected calculation, we can use the fixture and intermediate output to locate the cause before changing several expressions at once.

Sources: Week 11 Lab 1 and Notebook 07. Atlas IP access list: https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 17

Our second class begins with a different application view. Instead of a category summary, a queue displays the newest twenty open requests. This sounds like a small read because the application receives only twenty documents. However, the database may need to examine many candidates and order them before it can identify those twenty.

We will first make the requested result precise. Open is the filter. Opening date determines recency, and ticket identifier resolves a tie between equal dates. The projection includes the fields that the page needs to show. Keeping those choices fixed makes a before-and-after index comparison meaningful.

The instructor's demonstration uses synthetic course data in a separate practice collection. The MongoDB University activity that follows uses its own guided environment and task. We are using the first example to understand the mechanism, then applying that understanding in a distinct lab.

We will look at returned documents, examined documents, examined index keys, and the plan operations. A smaller amount of database work can support an index decision, but those counts do not directly tell us how long a cloud page will take to load. Network delay, cache state, and competing work can affect elapsed time. Our claim will remain tied to what the experiment actually measures and to whether the ordered results stay correct.

Sources: Course implementation guide, Day 2 sort demonstration. Explain overview: https://www.mongodb.com/docs/manual/reference/method/cursor.explain/

## Slide 18

The live example contains ten thousand synthetic tickets. Every fifth record has status open, giving us two thousand open tickets. The other eight thousand are resolved. Each record has a unique ticket identifier, an opening date, and a short synthetic subject. The opening dates advance by one minute from February first, 2026.

These regular values make it possible to check the result independently. In the supplied setup, ticket identifiers increase as the dates advance. The newest open identifier is 39995, followed by 39990. Twenty open results end at identifier 39900. The query's explicit date and identifier sort still defines its order rather than relying on insertion order.

The fixture is larger than the Day 1 case for a reason. Four records are enough to understand a count, but they give us little room to see the difference between inspecting a collection and using a selective ordered access path. Here there are many irrelevant resolved tickets and many eligible open tickets beyond the twenty displayed.

This is still a controlled teaching dataset rather than a production benchmark. Real ticket systems can have different status distributions, date patterns, document sizes, and concurrent traffic. Those differences can change plan choices and measured work. We will learn a repeatable comparison method without treating this particular result as a guarantee for every Atlas deployment.

Sources: Original 10,000-record fixture in course/instructor/implementation_guide.md. Counts and expected identifiers derive from its generator.

## Slide 19

This code runs in mongosh, so its spelling differs from the Python notebook. Const declares JavaScript variables, and toArray reads the cursor into an array for this small result. The concepts are the same ones we used with PyMongo: a filter, a projection, an order, and a limit.

The filter requests only documents whose status equals open. The projection returns ticket identifier, opening date, and subject while excluding the internal underscore-id. The order sorts dates descending. If two dates are equal, it sorts ticket identifiers descending within that tied date. Our unique ticket identifiers make that tie-break order unambiguous for this dataset.

The limit returns at most twenty documents after applying the requested query and order. It does not promise that MongoDB examined only twenty source documents. Without an appropriate ordered access path, the server may inspect the full collection and evaluate many eligible candidates to determine which twenty belong first.

We save the normal result as beforeRows so that we can compare it with the result after index creation. Looking only at a plan could miss a changed filter or projection. A fair comparison keeps the query semantics and fixture fixed. The lesson's code uses this fresh collection rather than another student's database, and the setup includes the unique ticket-key index separately from the compound index we are about to add.

Sources: Course sort demonstration. Cursor sort: https://www.mongodb.com/docs/manual/reference/method/cursor.sort/ Cursor limit: https://www.mongodb.com/docs/manual/reference/method/cursor.limit/

## Slide 20

The candidate index follows the structure of our queue query. Its first field is status, which the query fixes to one value. Within that status range, opening dates descend. Ticket identifiers descend within equal dates. That order lets the database seek the open range and read candidates in the order the page requests.

The index has a descriptive name, open by recent, but the name has no filtering effect. The command does not include a partial-filter expression. It creates index entries for all tickets in this collection, including resolved tickets. The query condition selects the open portion of the index when the planner uses it.

Field order matters because a compound index provides a particular ordering. Merely including all three field names somewhere in an index does not establish that it supports every ordering on those fields. If the workload changes to a queue across all statuses, we must reconsider the leading status field and inspect the new plan.

For this example, we are reasoning from an equality condition followed by the requested sort. We will still check explain rather than assume that creating a candidate guarantees the planner will choose it. The index also brings a maintenance cost. We are adding another structure that the database must store and update when relevant data changes. Its benefit depends on the queries that use it.

Sources: Course sort query and observed local plan. Index-supported sorting: https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/ Compound indexes: https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/

## Slide 21

Explain with execution statistics gives us information about the plan and its execution work. The command on this slide uses the same filter, projection, sort, and limit as the normal queue read. We run the corresponding command before index creation and again afterward, so the comparison concerns one workload.

Returned documents tells us how many results the plan produced. Documents examined counts document examinations during execution, and keys examined counts examined index entries. These quantities describe different kinds of work. Twenty keys examined is not interchangeable with twenty complete documents examined, and zero keys examined can mean that a collection scan avoided indexes entirely.

The winning plan describes the chosen operations. Plan output is nested, and its exact structure can vary with server version and execution engine. In this lesson, we look for the relevant scan, sort, and fetch operations instead of memorizing one fixed JSON path for every possible plan.

The normal beforeRows and afterRows queries remain important. Explain output is a diagnostic result, rather than the twenty ticket documents that the application displays. We compare those ordinary query results to confirm that the index experiment preserved the same ordered identifiers and requested field values. Then we interpret the execution statistics. This keeps result correctness separate from the amount of work required to obtain it.

Sources: Explain results and stage meanings: https://www.mongodb.com/docs/manual/reference/explain-results/ Course implementation guide's fixed query comparison.

## Slide 22

These are the observations from the supplied ten-thousand-ticket example on local MongoDB 8.0.29. Before the compound index, the query returned twenty documents after examining ten thousand documents and zero index keys. Its relevant operations included a collection scan and a sort. After the index, it returned the same twenty documents while examining twenty documents and twenty keys, using an index scan and document fetches.

The difference is consistent with the access path we designed. The collection scan has to consider the source population. The ordered index lets this particular query reach open tickets in the required order and stop after obtaining the requested result count.

The measurements are bounded by this fixture, query, index set, and server execution. They do not mean that every index-assisted query examines exactly as many keys as it returns. Other filters or data distributions can require additional examination. We also should not turn the ratio of ten thousand to twenty into a claim of a five-hundred-times runtime speedup. These are work counts, not elapsed-time measurements.

The normal-query comparison confirmed matching ordered identifiers and field values. That matters because a query returning different tickets could appear faster for the wrong reason. Our conclusion is that this index reduced the measured search and ordering work for this defined queue while preserving the requested output.

Sources: Executed local course sort demonstration on MongoDB 8.0.29. Explain metric definitions: https://www.mongodb.com/docs/manual/reference/explain-results/ This is not an Atlas production benchmark.

## Slide 23

The after plan still includes fetch operations. That is expected for our projection. The index contains status, opening date, and ticket identifier, but the page also asks for subject. MongoDB must retrieve the matching documents to obtain that field. Using an index does not imply that every returned value comes directly from index entries.

A covered query can obtain the needed information from an appropriate index without fetching the documents. Our example deliberately does not make that claim. It shows that an index can be useful even when the plan still fetches the twenty documents the application needs.

We could consider adding another field to an index for a specific workload, but adding every projected field automatically would be a poor general rule. Wider indexes occupy more space, and the database must maintain their entries. A subject that changes frequently would also affect an index that stores it. The right decision depends on the read benefit and the cost of maintaining the structure.

For the current experiment, the improvement comes from finding eligible tickets in the needed order rather than scanning and sorting the full set of candidates. Fetching those selected documents is compatible with that benefit. In a design discussion, we can say exactly which work improved and which work remains, instead of describing the query as simply optimized without qualification.

Sources: Covered-query requirements: https://www.mongodb.com/docs/manual/core/query-optimization/#covered-query Index costs: https://www.mongodb.com/docs/manual/core/write-performance/

## Slide 24

We return briefly to the four-ticket fixture to see a correctness boundary on optimization. The first pipeline matches status open, sorts by newest opening, and limits the result to one. Only ticket 1001 has status open in this case, so that pipeline returns 1001.

The second pipeline sorts all tickets first, takes the newest one, and only then checks whether it is open. The newest ticket is 1004. Its status is new, not open, so the final match removes it and the result is empty. Both pipelines are valid, but they answer different questions.

The first asks for the newest member of the open-ticket population. The second asks whether the newest ticket in the whole population happens to be open. Moving the limit changed the population that remained available for the filter. The fact that the second pipeline handles fewer rows at its final stage does not make it a correct replacement.

A similar issue arises with a filter on a calculated group count. That field does not exist on the original input tickets. We cannot simply move its test before the grouping operation that creates it. MongoDB can perform safe optimizer transformations internally, but our manual revisions still need semantic checks. Small counterexamples are useful because they expose an incorrect rewrite without requiring a large performance test.

Sources: Original four-ticket counterexample. Pipeline optimization and dependency boundaries: https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/

## Slide 25

The week's mechanisms address different responsibilities. Aggregation computes the report. Validation restricts the documents that writes may produce under the installed rule. Index design supplies an access path that can change the work required by a query. Combining them in one application does not make their guarantees interchangeable.

The duplicated-ticket report could run quickly through an index and still be wrong. A date rule could reject a string while allowing a correctly typed but implausible future date. An index could improve the newest-open queue without changing whether a ticket's status belongs in the allowed list.

Installing a validator also does not rewrite every old document to satisfy the new rule. An existing application needs an explicit inspection and migration plan when its data requirements change. Our notebook avoids that larger migration problem by starting with a small, compatible practice fixture and separate test identifiers.

This distinction helps us diagnose failures in a sensible order. We define the required output and verify its input records. We check the constraints that protect relevant assumptions. Then we compare access paths for the correct workload. An optimization is useful only in relation to an answer the application actually needs. In a review with another developer, we can discuss each claim separately and show the corresponding query result, rule test, or plan measurement rather than present one successful run as proof of everything.

Sources: Original course synthesis based on the executed fixture, validation tests, and sort experiment. Chapter 11, Validation and Indexing Solve Different Problems.

## Slide 26

The individual performance activity is MongoDB University's Improving Performance of Sort Stages lab-only course. The Week 11 guide and Lab 2 assignment link to that exact activity. This is separate from the synthetic sort-tickets example in our live demonstration. We are applying the same reasoning to the guided exercise rather than submitting the demonstration as though we completed the external lab.

During the activity, the useful details are the requested filter and order, the index that supports them, and the plan behavior. The completion image needs the lab title and completion status or score. Personal account information should be removed from the image before it enters the submission.

If the external activity is unavailable, the assignment supplies a plan-comparison fallback. Its numbers form a teaching case to interpret. The response must label that path rather than describe the supplied numbers as a personal measurement or imply that the University activity was completed.

The performance work and the inventory video response go into one Brightspace text submission. We do not need another repository, a Markdown report, or a separate packet. The objective is to explain a database decision with enough detail that another person can understand the intended workload and a cost of the choice. Completing an online activity is useful practice, while the explanation shows what we understood from it.

Sources: Week 11 Lab 2. Exact external activity: https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only The provider controls its account-gated interface and completion requirements.

## Slide 27

The inventory case gives us an application context for a short design recommendation. Rather than recap every part of the video, we will identify one decision that the presenter actually demonstrates and connect it to a concept we have studied. A timestamp or a clearly identifiable scene makes the example easy to locate.

The response should explain what the application needs to read or change, how the chosen representation or operation supports that work, and what becomes harder as a result. A reference can create an additional read. A copied value can create maintenance work. An event-oriented design can require care with ordering or repeated processing. Those are possible analytical connections, not claims that the video necessarily demonstrates each one.

We also need to separate observation from recommendation. If we propose a new index after watching the case, we should call it our proposal. We should not attribute it to the presenter unless the video actually shows it. The same distinction applies to a validation rule or a change in document structure.

The final response is two hundred to three hundred words in Brightspace, with the lab completion image or labeled fallback in that same submission. One sentence should describe how we would communicate the decision to a developer or operations teammate. The task practices technical explanation grounded in a specific example, rather than general praise for a product.

Sources: Week 11 Lab 2. Assigned video: https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13 This script introduces the response method and does not assert unverified video details.

## Slide 28

This paragraph models a way to describe the week's work in an interview. It identifies the calculation, the error we found, the input rule we tested, and the comparison behind an index choice. It gives another person something concrete to discuss. A statement such as I know MongoDB would leave all of those details unspecified.

We should adapt the account to the work we actually completed. Someone who used the local validation trace can say that they interpreted how the rule would classify the test inputs. Someone who executed the inserts against MongoDB can describe the observed acceptances and rejections. Watching an instructor compare plans is also different from independently conducting that comparison. Accurate scope makes an example more credible, not less useful.

A follow-up discussion can refer to the small fixture. We can explain how matching totals hid different ticket identifiers, why a date-shaped string failed the BSON rule, or why the query still fetched documents after using an index. Those explanations demonstrate understanding of the mechanism behind the code.

Before leaving the practice environment, we finish the notebook cleanup and remove any temporary Atlas network rule we added. The instructor's separate sort collection has its own cleanup. Next week, we will examine replication, consistency, and recovery. A query can return the right result today while the application still needs a plan for node failure, delayed replicas, or an accidental deletion tomorrow.

Sources: Original career-communication example tied to Week 11 work. Notebook 07 and the implementation guide define their respective cleanup boundaries.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
