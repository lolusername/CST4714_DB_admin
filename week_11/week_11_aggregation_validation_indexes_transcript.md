# Week 11: Aggregation, Validation, and MongoDB Index Design - Spoken Transcript

## Slide 1

Welcome to Week 11. Read the line in the middle of the slide: a request summary can look right and still count the wrong things. That is the warning for the whole week.

Picture a manager opening a dashboard that says three active requests. The page loaded, there were no errors, and three sounds reasonable. But neither of those facts tells you which requests were counted. A duplicate and a missing record can cancel each other out and leave a total that looks perfectly fine. You will watch exactly that happen on Day 1.

So on Day 1 we take four tickets, follow a summary through every stage of a MongoDB pipeline, and add a useful calculation. Then we require a real opening date whenever the application writes a ticket. The notebook gives you the starting code, so your job is understanding it and changing it, not building a connection from scratch.

On Day 2 we look at an ordered queue. The page shows twenty requests, but the database might look at thousands to find them. We add a compound index and check that the answer stays the same while the work goes down.

Chapter 11 covers all of this in more detail. By the end of the week you should be able to explain a result, say where a validation rule stops, and back an index decision with measurements instead of product claims.

Sources: Course textbook Chapter 11; Notebook 07; Week 11 assignments and implementation guide. The ticket cases are synthetic course examples.

## Slide 2

Let's start from something you already know. This is the SQL version of the summary we are about to build in MongoDB.

Read it top to bottom. FROM tickets is the source. The WHERE clause keeps tickets whose status is one of our three active values: new, open, or in progress. GROUP BY category combines the survivors by category. COUNT star counts the rows that landed in each group, and ORDER BY category makes the output order predictable.

Now look at the first line under the code: WHERE selects tickets, GROUP BY changes the unit of the result. That second half is the big idea. Before grouping, every row is a ticket. After grouping, every row is a category. That is why you cannot just add a ticket's subject to this output. Several tickets went into each row, so whose subject would it be?

MongoDB writes the same calculation as a list of stages, which you will see in a minute. The syntax changes, but your responsibility does not. You still have to know what reaches the grouping step. If you join events first, or expand an array, you end up counting events instead of tickets.

On our four tickets, this query gives one active sanitation ticket and two active streetlight tickets. Hold on to that answer, because we are going to check MongoDB against it.

Sources: Original course SQL example and four-ticket fixture. PostgreSQL SELECT documentation: https://www.postgresql.org/docs/current/sql-select.html

## Slide 3

Here are the four tickets in today's notebook, shown as a table so you can see the fields side by side. In the notebook they are documents, and each one also carries a subject and a small array of events.

Walk down the ID column with me. 1001 is an urgent streetlight ticket, open. 1002 is sanitation, in progress. 1003 is another urgent streetlight ticket, but it is resolved. 1004 is a new streetlight ticket with low priority. Our active definition keeps 1001, 1002, and 1004. Look at the note under the table: resolved ticket 1003 stays stored. Leaving a ticket out of a report is not the same as deleting it.

Now count a few things by eye, because these are the checks we will hold the pipeline to. Two active streetlight tickets. Only one of them, 1001, is urgent. The newest of them opened on February 4. None of that depends on writing an aggregation correctly, and that is exactly what makes it a good check.

Two cautions. This is a fresh case. Some IDs look like earlier course examples, but it replaces neither the Week 10 fixture nor the CSVs, so use today's values. And the dates on the slide are shortened for display. In the notebook they are real timezone-aware dates stored as BSON dates, and later we compare them with text that only looks like a date.

Sources: course/notebooks/07_aggregation_validation.ipynb, four-ticket fixture. PyMongo date handling: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/dates-and-times/

## Slide 4

This diagram is the whole Day 1 pipeline on one slide. Follow it left to right.

The tickets collection supplies 4 documents. $match keeps the 3 active tickets. $group turns them into 2 category summaries. $project renames fields, and $sort puts the categories A to Z.

Watch how the numbers change: 4, then 3, then 2. Those drops mean different things. Match removed an ineligible ticket from this query's stream. Group combined eligible tickets into summaries. Project and sort leave the count alone in this pipeline.

Now look at the small labels under the stages: one per ticket, one per ticket, then one per category three times. That is the grain, and the line at the bottom defines it. Grain means what one result document represents. Why care? Because once you cross the group stage, a result is no longer a ticket. If a later stage treats a category summary as though it were still a complete ticket, you get nonsense, and MongoDB will not warn you.

In the notebook you run longer and longer pieces of this pipeline, so you can see the actual documents after match, after group, and at the end. You do not have to guess at the intermediate values. Notice also what is missing: there is no $unwind here. This report counts tickets, and in a few slides we will see what goes wrong when someone adds one.

Sources: Original editable course diagram, revised to the Notebook 07 fixture. Aggregation pipeline: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/

## Slide 5

Here is the first stage in Python. The variable active_filter is a filter document. Its key is status, and the $in operator checks whether the status is one of the three values in the list. Those strings have to match exactly what the data stores. A different spelling is simply a different value, and it would quietly fall out of the report.

Next we put that filter inside a $match stage and pass a one-stage list to aggregate. Wrapping the cursor in list gives us the result documents, and the print line pulls out the ticket IDs and sorts them so they are easy to compare. That sorted call is plain Python for display. It is not a MongoDB sort stage.

Look at the result: 1001, 1002, 1004. Exactly the three we predicted. Each one is still a complete ticket, with its subject, category, and events untouched.

Now read the line at the bottom. The collection still contains four tickets. $match changes this result stream without deleting stored data. That matters when you are troubleshooting. If a manager says a request vanished from the active queue, the first question is whether its status excluded it or whether it was actually deleted. You can look it up by its ID and find out. Nothing in this reporting pipeline writes back to the collection.

Sources: Notebook 07 fixture and pipeline. Match stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/match/

## Slide 6

Now the group stage. This is where the shape of the result changes.

Look at the _id line. In a group stage, _id is the grouping key, and here it is dollar category. The dollar sign means "read the category field from each incoming ticket." Tickets with the same category land in the same group. Then active_count uses $sum with the constant 1, so every ticket that reaches its group adds one. We are not adding up a field called one, and we are not counting the whole collection. Match already decided which tickets arrive here.

Now the table at the bottom, which shows why that dollar sign matters so much. With dollar category, you get sanitation 1 and streetlight 2, the same answer we worked out by hand. Drop the dollar sign and write just the string category, and every ticket gets the same constant key. The pipeline still runs. No error. You get one group called category with a count of 3.

That is the lesson of this slide. Running without an error only proves the expression was valid. It does not prove it answered the right question. So we compare the group keys and counts against the four tickets we know. And notice that we are not assuming any order yet. Grouping by itself does not promise that sanitation comes before streetlight.

Sources: Original fixture-derived results. Group stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/ Field paths: https://www.mongodb.com/docs/manual/core/field-paths/

## Slide 7

Now we assemble the full baseline pipeline. Four stages in a Python list: match, the group stage from the last slide, a project, and a sort. Each stage receives the output of the stage before it.

The project stage is the one people stumble on, so look closely. After grouping, _id holds the category value. Read the note at the bottom: the grouped _id holds a category value, it is not a ticket ID. So we copy it into a field with an honest name. Category gets dollar underscore id. The zero next to _id hides the original field, and the one next to active_count keeps the count we already calculated.

Then $sort with category 1 puts the categories in ascending order. Look at the result table: sanitation 1, then streetlight 2. That table is just what the pipeline returns. Nothing new was stored in the database.

Here is a warning that will matter in the lab. This project names the fields it returns, which makes it an inclusion projection. So if you add a new calculated field to group and forget to name it here, it gets calculated correctly and then quietly hidden. That is a frustrating bug, because nothing errors. In Lab 1 you add urgent count and newest opening, so you have to update the group stage and the project stage together, and keep active count while you do it.

Sources: Notebook 07 pipeline. Project stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/project/ Sort stage: https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/

## Slide 8

Now the manager wants more than a total. For each category: how many active tickets are urgent, and when did the newest one open? We can calculate both inside the same group stage, because group still sees the individual active tickets.

Look at urgent_count. It is a $sum again, but instead of adding a constant 1, it adds the result of a $cond. Read $cond like an if statement: if priority equals urgent, contribute 1, otherwise contribute 0. Add those up per category and you have the number of urgent tickets. In the streetlight group, ticket 1001 contributes 1 and ticket 1004 contributes 0.

Then newest_opening uses $max on opened_at. Because our dates are stored as real BSON dates, the biggest value is the latest moment. Notice what it gives you: the date itself, not the whole ticket that has that date. If someone wants the full newest ticket, that is a different design.

Read the note at the bottom. In the lab you add these two fields to the existing group stage instead of replacing active count, and you expose both of them in project. And because match still runs first, the resolved urgent ticket, 1003, never gets near these calculations. The report keeps its original meaning: one summary per category of active tickets.

Sources: Course worked extension. Conditional expression: https://www.mongodb.com/docs/manual/reference/operator/aggregation/cond/ Sum: https://www.mongodb.com/docs/manual/reference/operator/aggregation/sum/ Max: https://www.mongodb.com/docs/manual/reference/operator/aggregation/max/

## Slide 9

Here is what the extended summary should look like. Sanitation: 1 active, 0 urgent, newest opening February 2. Streetlight: 2 active, 1 urgent, newest opening February 4.

Here is the habit I want you to build. Explain the streetlight row without looking at any aggregation code. Its tickets are 1001 and 1004. Ticket 1001 is urgent and opened February 1. Ticket 1004 is low priority and opened February 4. Count them: two. Count the urgent one: one. Take the later date: February 4. If you can say that out loud from the source IDs, you actually understand the result, and you are not just trusting the output.

Now look at the caution at the bottom. Ticket 1003 is urgent and it is a streetlight ticket, but it is resolved, so it contributes to none of these totals. That ticket is in the fixture on purpose, as a trap. Suppose a mistake let 1003 into urgent count but kept it out of active count. Every number would still look plausible, but the columns would no longer describe the same set of tickets.

That is why checking a report means checking its definitions, not only its arithmetic. A column name does not tell you what was counted. In the lab's explanation cell, name the source IDs and the condition that selected them, including anything unexpected you had to fix.

Sources: Original calculations from Notebook 07's four-ticket fixture. No external operational dataset or measured production outcome is represented.

## Slide 10

Now a different question. Instead of tickets, we want events. Each ticket has an events array. Ticket 1001 has a created event and an assigned event. Ticket 1002 has one created event. And 1004, as the note at the bottom says, has an empty array.

$unwind takes a document with an array and emits one document per element. Then project keeps the ticket ID and reads the event's type, and sort orders by ticket ID and then by event type.

Look at the result table: 1001 assigned, 1001 created, 1002 created. Three rows. Two quick points. Assigned appears before created only because the sort is alphabetical. It does not mean the assignment happened first. And ticket 1004 is gone entirely. A default $unwind produces nothing for an empty array, so a ticket with no events contributes no rows.

This is a perfectly good operation when events are what you want to analyze. If you want to count event types, you need the individual events. The problem comes when you put this stage in front of a ticket count. A ticket with two events now shows up twice. And here is the sneaky part: every row still has a ticket_id field, so the output looks like ticket rows. Seeing that field does not mean each ticket appears once. You work out the grain from what the stage does and from the actual records, not from the column names.

Sources: Notebook 07 event arrays. Unwind behavior: https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

## Slide 11

Here is the trap in full, and it is the reason this week exists. Look at the table. Active tickets: 1001, 1002, 1004, total 3. Events on active tickets: 1001, 1001, 1002, total 3. Same total. A test that only checks the grand total passes, even though one ticket was counted twice and another disappeared.

It gets worse. Read the first note. Even the category totals match: streetlight 2, sanitation 1. But both streetlight rows in the event version are ticket 1001. So a check by category passes too.

What finally catches it? The urgent count. Ticket 1001 is urgent, and both of its event rows would add 1 to a conditional sum. So the broken report says two urgent streetlight requests, when only one active streetlight ticket is urgent. That is the manager's dashboard from slide 1: believable numbers built from the wrong tickets.

Now the second note. You might think preserving empty arrays fixes it. That brings back a row for 1004, but 1001 is still there twice. It does not turn an event stream back into a ticket stream. For this summary, the simple correct answer is to leave $unwind out. When a report really needs both, count tickets before expanding events, or deduplicate on a stable ticket key and decide how tickets with no events get in. Start from the population you mean to count.

Sources: Original counterexample and computed identity lists from Notebook 07. Related mechanism: https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/

## Slide 12

Let's switch from reading data to protecting it on the way in. A report is only as trustworthy as its inputs, and MongoDB lets us attach a validator to a collection that describes which documents are allowed.

Look at the table, because each rule checks one thing and leaves something else alone. Required checks that the field exists. It says nothing about its type or value. bsonType date checks that the value is a real BSON date. It does not check whether that date is plausible. Enum checks that a value belongs to a list. It does not check whether a status change is allowed.

Why spend time on that last column? Because people overclaim what a rule does. Our status list is new, open, in progress, resolved, and closed. It stops a value like almost done. But it cannot stop someone from reopening a closed ticket, because that depends on what the status was before. That needs a separate rule in the application or the database. Dates are the same: a date in the distant future still has the right type.

The note at the bottom matters too. A focused schema can allow additional fields. Our baseline requires ticket_id, status, and subject, and other fields can still appear. Flexibility is the point of a document database, and validation does not have to take it away. We write the small rule this lab needs, and then we say honestly what it protects and what it does not.

Sources: Schema validation: https://www.mongodb.com/docs/manual/core/schema-validation/ Specify allowed field values: https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/#std-label-schema-validation-json

## Slide 13

Here is the baseline validator as a Python dictionary. Let's read it from the outside in.

The outer key, $jsonSchema, tells MongoDB what kind of rule this is. bsonType object applies to the document itself. The required list names the three fields that must be present: ticket_id, status, and subject. Then properties sets rules for individual fields. ticket_id can be either of two BSON integer types, int or long. Status has to be one of the five strings in the enum. Subject has to be a string.

Notice what is not required yet: category, priority, events, and the opening date. That is deliberate. Your lab job is to add one of them.

Now read the note at the bottom, because it trips people up. A Python variable by itself does not install a server validator. Creating a dictionary called validator does nothing to the database. It is like typing a SQL constraint into an editor and never running it. A separate command installs it, and you will see that command on the next slide.

One more thing. This looks like standard JSON Schema, but it is MongoDB's version. Words like date and long in bsonType are MongoDB-specific. Knowing where Python ends and MongoDB begins helps you diagnose problems. A Python syntax error, an unsupported command, a permission failure, and a rejected document are four different messages with four different fixes.

Sources: Notebook 07 baseline validator. JSON Schema validation: https://www.mongodb.com/docs/manual/core/schema-validation/specify-json-schema/

## Slide 14

The new rule says every ticket needs a real opening date. Look at the title: that takes two declarations, and here is why.

The second line puts opened_at in the required list. The third line says opened_at must be a BSON date. If you only wrote the type rule, a document could leave the field out entirely. If you only wrote the required rule, a document could put text in it. You need both. Also notice that we assign the whole required list instead of appending to it. That way, rerunning the cell does not add opened_at twice.

Then comes the command that actually installs it. collMod changes settings on the tickets collection. Validation level strict and validation action error are the enforcement we use in this lesson: writes get checked against the rule, and a bad document is refused.

Two practical points. First, collMod needs its own permission, separate from connecting or reading. A database user with only the ordinary read and write role cannot run it, and a successful ping does not prove you have it. Second, read the comment and the note at the bottom. This command is for a real MongoDB connection. Local mongomock mode does not enforce validators, so the notebook skips the install instead of pretending.

Our four tickets already have dates, so they fit the new rule. On a real collection, you would inspect the old data and plan a migration before tightening a rule like this.

Sources: Notebook 07 date extension. collMod: https://www.mongodb.com/docs/manual/reference/command/collMod/ Validation level: https://www.mongodb.com/docs/manual/core/schema-validation/specify-validation-level/

## Slide 15

Now we test the rule with one document that should pass and three that should fail, each different in one specific way. Look at the table.

1099 has status new and a real BSON date: accept. 1100 has status almost_done: reject, invalid status. 1101 has an opened_at that is text shaped like a date: reject, incorrect type. 1102 has no opened_at at all: reject, missing field.

Why change only one thing per document? Because when a rejection comes back, you want to know exactly which condition caused it. That is also why each test gets its own ID. If you reused an ID, you could get a duplicate key error and mistake it for a validation failure. And the test cell cleans up its records afterward, so your summary stays a four-ticket exercise.

One timing point. The text-date and missing-date cases only appear after you add and reinstall the date rule. Before that, the schema did not require a date, so you cannot say those documents broke a rule that did not exist yet.

Now read the last line on the slide. Atlas executes validation. Local mode supplies a labeled trace to interpret. On Atlas, the database really attempts each insert, and a validation error looks different from a network or authorization error. In local mode, you reason about what the rule would do. That is good work, but say which path you used, and never call a trace a live server test.

Sources: Notebook 07 test cell. Handling invalid documents: https://www.mongodb.com/docs/manual/core/schema-validation/handle-invalid-documents/

## Slide 16

Here is Lab 1, and it all lives in one notebook, Notebook 07. Extend the summary with urgent count and newest opening, add the required opening-date rule, and use ticket IDs to explain the array-counting error. Submit the completed notebook in Brightspace, individually. Your explanation goes in the notebook's existing explanation cell. There is no separate report or repository.

You can stay in local mode and start the aggregation work as soon as the packages install. If you choose Atlas, look at the middle box. The notebook prints the public IPv4 address of the runtime running your code. In Colab that runtime is on Google's infrastructure, so it is not your laptop's address. You allow that one address as a temporary slash 32 entry. Your connection string goes into the hidden prompt, never into a visible cell, and you leave TLS verification on.

When you finish, run the cleanup cell. Look at the code: drop_collection on tickets, then close the client. Read the note under it. It drops only this practice collection. It does not delete your Atlas project or shut down your cluster. Then go back to Atlas and remove the temporary IP rule, because an access rule you forgot about is an open door.

In your explanation, cover the streetlight inputs, the effect of expanding events, and where the date rule stops. If a number does not match, use the four tickets and the intermediate output to find the cause before you change several expressions at once.

Sources: Week 11 Lab 1 and Notebook 07. Atlas IP access list: https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 17

Welcome back. Day 2 starts from a different screen. Instead of a category summary, picture a queue that shows the newest open requests.

Read the slide. A queue displays 20 requests. The database may examine many more. That sounds like a small read, because the application only gets twenty documents back. But to know which twenty are newest, the database may have to look at every candidate and sort them first. The page size tells you nothing about the work.

Before we touch performance, we pin down exactly what the result is. Status open is the filter. Opening date decides what counts as newest. Ticket ID breaks ties when two dates are equal. And the projection names the fields the page shows. We keep all of that fixed, because a before-and-after comparison only means something if the question stays the same.

As the second box says, we compare the same ordered results before and after an index. I demonstrate on synthetic course data in a separate practice collection. Then you complete a separate MongoDB University sort lab in its own guided environment. My demo is for understanding the mechanism. The lab is where you apply it.

We will measure documents returned, documents examined, index keys examined, and the plan operations. Less work supports an index decision, but those counts do not tell you how fast a cloud page loads. Network delay, cache state, and other traffic all affect time. So our claims stay tied to what we measured.

Sources: Course implementation guide, Day 2 sort demonstration. Explain overview: https://www.mongodb.com/docs/manual/reference/method/cursor.explain/

## Slide 18

Here is the dataset for my live demonstration. Look at the table. A collection called sort_tickets in a new practice database. Ten thousand synthetic tickets, each with a unique ID. Two thousand are open and eight thousand are resolved, because every fifth ticket is open. And the opening dates go up one minute at a time, starting February 1, 2026, in UTC.

Why such regular data? Because it lets us check the answer independently. In my setup, ticket IDs increase as the dates advance. So I can tell you in advance that the newest open ticket is 39995, the next one is 39990, and the twentieth result is 39900. If the query returns anything else, something is wrong. The query still sorts explicitly by date and ID, though. We never rely on the order the documents happened to be inserted.

Read the note at the bottom. The four-ticket case explains correctness. This larger case makes query-plan work visible. With four documents, scanning everything is instant and nothing looks different. Here, there are thousands of irrelevant resolved tickets, and far more open tickets than the twenty we display, so a poor access path actually shows up in the numbers.

Keep in mind that this is a controlled teaching dataset, not a production benchmark. Real systems have different status mixes, document sizes, and traffic, and those can change the plan. What you are learning is a comparison method you can repeat, not a guarantee about every Atlas deployment.

Sources: Original 10,000-record fixture in course/instructor/implementation_guide.md. Counts and expected identifiers derive from its generator.

## Slide 19

This is the queue query, and notice that it is mongosh, so it is JavaScript, not Python. The note at the bottom says so: Day 2 live code uses mongosh JavaScript, and Notebook 07 uses Python. Const declares a variable, and toArray reads the cursor into an array. The ideas are the same ones you used in PyMongo: a filter, a projection, an order, and a limit.

Walk through it. The filter is status open. The projection returns ticket_id, opened_at, and subject, and hides _id. The order is opened_at minus one, newest date first, then ticket_id minus one. Look at the first note on the right: that second key resolves tied dates. Since our IDs are unique, the order is never ambiguous. Without a tie-breaker, two tickets with the same date could come back in either order, and two runs of the same page might not agree.

Now the second line of that note, which is the important one. A limit caps returned rows, not necessarily examined documents. Limit 20 promises you at most twenty results. It does not promise that MongoDB only looked at twenty. Without a suitable ordered access path, it may scan the whole collection and sort the open candidates to figure out which twenty come first.

Last, we save the normal result as beforeRows. After we add the index we compare the actual results, not just the plans, so we know the answer did not change.

Sources: Course sort demonstration. Cursor sort: https://www.mongodb.com/docs/manual/reference/method/cursor.sort/ Cursor limit: https://www.mongodb.com/docs/manual/reference/method/cursor.limit/

## Slide 20

Here is the candidate index. Look at its field order, because the order is the whole design. Status ascending, then opened_at descending, then ticket_id descending. The table explains each position.

Status comes first because our query fixes it to one value. Equality on status means the database can jump straight to the open section of the index. Inside that section, entries are already sorted by date, newest first, and inside any tied date, by ticket ID descending. That is exactly the order the page asks for. So the database can seek to the open tickets, read them in order, and stop once it has twenty, with no separate sort.

That is why field order matters. Having the right three field names somewhere in an index is not enough. A compound index provides one specific ordering. If the queue changed to show all statuses, a leading status field would no longer fit, and you would rethink the index and check the new plan.

Read the note at the bottom. The name, open_by_recent, is just a label. It does not make this a partial index. There is no filter expression, so every ticket gets an entry, including all the resolved ones.

Two more things. Creating an index does not guarantee the planner chooses it, so we check with explain. And an index is not free. It takes storage and has to be updated when the data changes, so it earns its place only through the queries that use it.

Sources: Course sort query and observed local plan. Index-supported sorting: https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/ Compound indexes: https://www.mongodb.com/docs/manual/core/indexes/index-types/index-compound/

## Slide 21

Now we ask MongoDB to show its work. This is the same query, with the same filter, projection, sort, and limit, but it ends in explain with executionStats. Read the first note under the code: the same command runs before index creation in the live example. I run it before and after, so both measurements describe one workload.

Look at the printjson block. It pulls out four things. nReturned is how many results the plan produced. totalDocsExamined is how many documents the server looked at. totalKeysExamined is how many index entries it read. And winningPlan describes the operations it chose.

Those are different kinds of work, so do not mix them up. Twenty keys examined is not the same as twenty full documents examined. And zero keys examined can mean a collection scan that never used an index at all.

The plan output is nested, and its exact shape changes with the server version and execution engine. So do not memorize one JSON path. Look for the scan, the sort, and the fetch operations.

Now the second note: compare the normal query results as well as both execution plans. Explain gives you a diagnostic, not the twenty tickets the page displays. So we also compare beforeRows and afterRows, to confirm the same ordered IDs and field values came back. Correctness first, then work. If you only look at plans, you can miss a change in what the query answers.

Sources: Explain results and stage meanings: https://www.mongodb.com/docs/manual/reference/explain-results/ Course implementation guide's fixed query comparison.

## Slide 22

Here are the actual measurements, observed on local MongoDB 8.0.29 with the supplied synthetic data. Look at the table row by row.

Returned documents: 20 before, 20 after. Documents examined: 10,000 before, 20 after. Index keys examined: 0 before, 20 after. Main plan operations: COLLSCAN plus SORT before, IXSCAN plus FETCH after.

So before the index, MongoDB read all ten thousand documents, kept the open ones, and sorted them to find the newest twenty. After the index, it walked into the open section in the right order and stopped after twenty entries. That is the access path we designed on slide 20.

Now read the notes, because they keep us honest. First, both runs return the same ordered IDs and field values. That matters, because a query that returns different tickets can look faster for the wrong reason. Second, these work counts do not establish a 500-times runtime speedup. Ten thousand divided by twenty is five hundred, and it is very tempting to say that. But we measured work, not elapsed time.

These numbers also belong to this fixture, this query, and this set of indexes. Do not expect every indexed query to examine exactly as many keys as it returns. Other filters and data distributions can need more. Our conclusion is narrower and stronger: this index cut the search and ordering work for this defined queue while keeping the answer the same.

Sources: Executed local course sort demonstration on MongoDB 8.0.29. Explain metric definitions: https://www.mongodb.com/docs/manual/reference/explain-results/ This is not an Atlas production benchmark.

## Slide 23

After the index, the plan still has FETCH in it. Is that a problem? No. Look at the first box. The index contains status, opened_at, and ticket_id. But the page also needs subject, and subject is not in the index. So for each matching entry, MongoDB goes to the document to get it. Using an index does not mean every returned value comes from the index.

A query that never has to touch the documents, because everything it needs is in the index, is called a covered query. Read the third box: this result uses an index without being a covered query. And that is fine. The big win was finding the right twenty tickets in order, instead of scanning and sorting the whole collection. Fetching those twenty documents afterward fits perfectly well with that benefit.

So why not put subject in the index too? Look at the second box. The extra index occupies storage, and inserts and changes to indexed values also have to maintain the index entries. A wider index costs more space and more write work. If subjects get edited often, every edit now touches the index as well. Adding every field to every index would be a bad general rule.

The right decision weighs what the read gains against what it costs to keep the structure up to date. In a design discussion, say exactly which work improved and which work remains, instead of calling the query optimized and stopping there.

Sources: Covered-query requirements: https://www.mongodb.com/docs/manual/core/query-optimization/#covered-query Index costs: https://www.mongodb.com/docs/manual/core/write-performance/

## Slide 24

Back to our four tickets for a correctness check on optimization. Look at the table. Two pipelines built from the same three operations, just in a different order.

The first: match open, sort newest, limit 1. Only ticket 1001 has status open, so it returns 1001.

The second: sort newest, limit 1, then match open. Sort all four and the newest is 1004. The limit keeps only 1004. Then match checks for open, but 1004 has status new, not open, so it gets removed. The result is nothing.

Read the note under the table. Both pipelines run successfully. They answer different questions. The first asks for the newest open ticket. The second checks whether the newest ticket of any status happens to be open. Moving the limit changed which tickets were still around for the filter to see. And yes, the second one handles fewer documents at its last stage. That does not make it a correct replacement.

The last note gives you a second version of the same trap. A filter on a calculated group count also needs that count to exist first. The count is not on the original tickets, so you cannot move that filter in front of the group that creates it.

MongoDB's optimizer does make safe rearrangements internally. But when you rearrange a pipeline by hand, the meaning is your responsibility. A tiny counterexample like this one catches a wrong rewrite without any large performance test.

Sources: Original four-ticket counterexample. Pipeline optimization and dependency boundaries: https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/

## Slide 25

Let's put the week together. Look at the title: a faster query can still be incorrect. Then look at the table: three mechanisms, and what each experiment establishes.

Aggregation: the summary counts the intended ticket identities. Validation: specified new inputs pass or fail a document rule. Index and explain: a chosen access path changes measured query work. Using all three in one application does not make their guarantees interchangeable.

Make it concrete. The duplicated-ticket report from Day 1 could run quickly through a good index and still be wrong. The date rule rejects a string, but it accepts a correctly typed date far in the future. And our index helps the newest-open queue without checking whether a status belongs on the allowed list. Read the first note: an index cannot repair a duplicated count or an invalid date.

The second note is about timing. Installing validation does not rewrite old documents. A real collection with changing requirements needs someone to inspect the existing data and plan a migration. We sidestepped that with a small fixture that already fit the rule, plus separate test IDs.

So when something is wrong, work in order. Define the output you need and check it against the source records. Check the rules that protect your assumptions. Then compare access paths for that correct workload. When you review this with another developer, show the query result, the rule test, and the plan measurement separately. One successful run is not proof of everything.

Sources: Original course synthesis based on the executed fixture, validation tests, and sort experiment. Chapter 11, Validation and Indexing Solve Different Problems.

## Slide 26

Here is Lab 2, part one. Look at the name in the first box: MongoDB University, Improving Performance of $sort stages, Lab Only. Open it from the exact link in the Week 11 guide and the Lab 2 assignment, so you land on the right activity.

Look at the middle box. You complete it individually and keep one redacted completion image. Redacted means you remove your personal account details before the image goes into a submission. It should show the lab title and your completion status or score. And this lab is separate from my sort_tickets demonstration. You are applying the same reasoning to a new exercise, not handing in my demo as if it were your lab.

While you work, pay attention to three things: the filter and sort the lab asks for, the index that supports them, and how the plan behaves.

What if the external site will not load, or you cannot get in? Read the last box. Use the assignment's labeled plan-comparison fallback. It gives you two illustrative plans, and you explain why one does less search and sort work, and one cost of keeping its index. Label it as the fallback. Those numbers are a teaching case, not your own measurement, so do not present them as yours or imply that you finished the University lab.

The image or the fallback goes in one Brightspace text submission together with your video response. No repository, no Markdown file, and no separate packet.

Sources: Week 11 Lab 2. Exact external activity: https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only The provider controls its account-gated interface and completion requirements.

## Slide 27

Lab 2, part two, is the inventory case. The video is Building an Event-Driven Inventory Platform: A Case Study, and the link is in Week 11 Lab 2.

Do not summarize the whole video. Look at the middle box. Write 200 to 300 words identifying one decision the presenter actually demonstrates. Connect a specific moment to a concept from class, such as embedding, referencing, event data, aggregation, validation, or indexes, and explain a tradeoff. A timestamp or a clearly identifiable scene lets your reader find what you mean.

What does a good tradeoff sound like? Say what the application needs to read or change, how the design supports that, and what gets harder. A reference can mean an extra read. A copied value can mean extra maintenance. An event-driven design can raise questions about ordering or repeated processing. Those are connections you might look for, not claims about what the video shows.

Now read the bottom box. Separate what the presenter shows from a change you propose. If you watch the case and think an index would help, that is your proposal. Do not credit it to the presenter unless the video shows it.

Include one sentence on how you would communicate the decision to a developer or operator. If the video is unavailable, the lab gives you a written case to use instead, labeled as the written case fallback. It all goes in the same Brightspace text submission as the lab image. No Markdown file.

Sources: Week 11 Lab 2. Assigned video: https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13 This script introduces the response method and does not assert unverified video details.

## Slide 28

Last slide. Read the paragraph in the box. It is one way to describe this week's work in an interview. Notice what makes it work. It names the calculation, the error you caught, the input rule you tested, and the comparison behind an index choice. That gives an interviewer four concrete things to ask you about. Compare it with "I know MongoDB," which gives them nothing.

Now read the line under it: adapt this account to the work you actually completed. If you used the local validation trace, say you interpreted the rule. If you ran the inserts against MongoDB, you can describe the actual acceptances and rejections. And watching me compare plans is different from running that comparison yourself. Being accurate about scope makes you more believable, not less.

The follow-up questions will come back to the small details. Be ready to explain how matching totals hid different ticket IDs, why a date-shaped string failed the BSON date rule, or why the query still fetched documents after using an index. Those answers show you understand the mechanism, not just the code.

Before you leave, finish the notebook cleanup and remove any temporary Atlas network rule you added. My sort collection gets its own cleanup.

Next week: replication, consistency, and recovery after data loss. A query can return the right answer today, and the application still needs a plan for a failed node, a delayed replica, or an accidental deletion tomorrow.

Sources: Original career-communication example tied to Week 11 work. Notebook 07 and the implementation guide define their respective cleanup boundaries.

## Slide 29

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Follow the documents through a pipeline (1:11); Schema validation: which documents may exist? (1:05); Did the index change the work? (1:18). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 11 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
