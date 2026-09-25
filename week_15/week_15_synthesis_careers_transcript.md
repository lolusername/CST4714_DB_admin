# Week 15: Course Review, Demonstrations, and Career Communication - Spoken Transcript

## Slide 1

Our final review begins with a report that looks suspicious. The support dashboard says three tickets are active. When we add the staff members' active-ticket counts, we get two. Before changing code, we need to decide whether those numbers should be equal. A staff workload report and a complete backlog report can both be correct while describing different populations. We will inspect four records so that every part of the explanation remains visible.

This example brings several course ideas together. We will use SQL to select tickets, follow a left join, and count matched records. We will temporarily change an assignment and roll it back. We will represent the same facts as documents, then look at a restore whose row count matches even though one value is wrong. The point is to explain a result through the records and the operations that produced it. The notebook gives us a small system we can change without touching a cloud project.

Today you will use one concept for an individual GitHub guide. A single README containing a small example and your explanation can be the complete artifact. On our second meeting, we will present final projects and practice explaining technical decisions in interviews. The final-project assignment remains the source of its requirements. The review and career practice do not create several additional reports or require a new web application.

[Sources]
- Course textbook, Chapter 15, and Notebook 09: Four Tickets, Two Different Totals.

## Slide 2

This diagram reconnects the questions we have asked throughout the course. Purpose comes first because the same stored facts can support different decisions. A manager assigning today's work needs a different report from someone checking whether the organization has an unassigned backlog. We cannot assess the report merely by asking whether its SQL ran without an error.

Model asks what one record means and how identities connect. In our example, staff and tickets are different populations. An assignment refers to a staff identity, while a missing assignment is represented explicitly. Protection includes both valid states and permitted actions. A constraint can reject an invalid status without deciding which employee has permission to close a ticket.

Performance concerns the work required by a particular query. An index decision needs a stable workload and a comparison, not just the existence of an index. Recovery asks which state can be reconstructed and how we check it. Finally, reproducibility asks whether another person can follow our setup, run the relevant operation, and understand its result without receiving our password.

You can use this diagram to organize a final demonstration. You do not need to speak equally long about every part. Choose a path through your own project that explains its purpose, one meaningful operation, and an operational decision. When a follow-up exposes a gap, identify the specific test that would resolve it.

[Sources]
- Course textbook, Chapter 15, system-review framework.

## Slide 3

We will use Notebook 09 for this review. Choose Open in Colab on the weekly page and run the cells in order. Colab requires a Google account and an internet connection; an Atlas or Supabase account is not needed. Local Jupyter works too. The code uses Python's SQLite interface, which is already available in the intended Python environment. There is no package-installation cell and no connection string to enter.

SQLite executes real SQL inside the Python process. The database in this notebook lives in memory. It is separate from your Supabase project and your Atlas cluster, so the example cannot accidentally change either of them. Closing the connection removes that in-memory database. The setup cell can create a fresh version if we want to repeat the exercise.

That simplicity has a clear boundary. SQLite does not reproduce PostgreSQL's role system, its multi-session lock behavior, or Supabase's authenticated request path. It does not run a MongoDB replica set. We use it here to inspect query meaning, a constraint failure, explicit rollback, and a small logical restore. Later cells convert records to Python dictionaries and JSON. A displayed MongoDB pipeline is a comparison, not an instruction that the notebook secretly sends to Atlas.

Each code cell has an explanation before it and an interpretation afterward. Run the notebook in order once. Then return to the controlled assignment cell to test one changed input. There is no separate notebook submission for today's review.

[Sources]
- Notebook 09, setup and execution boundaries.
- https://docs.python.org/3/library/sqlite3.html

## Slide 4

The left table contains three staff members. Priya has identity 201, Noah has identity 202, and Elena has identity 203. The right table contains four tickets. Ticket 1 belongs to Priya and is open. Ticket 2 also belongs to Priya, but it is resolved. Ticket 3 is new and has no assignee. Ticket 4 belongs to Noah and is open.

For this example, active means new, open, or in progress. Resolved is outside that category. We should therefore expect three active tickets before we run any query. Two of them have assignees. Elena is a legitimate staff member even though no ticket points to her. Ticket 3 is a legitimate ticket even though it does not point to any staff member.

The distinction matters for modeling. A staff primary key identifies a person in the staff table. The ticket primary key identifies a ticket. The optional foreign key connects those identities when an assignment exists. SQL NULL is how this schema represents the absent assignment. It is not the staff identity zero, an empty staff name, or an instruction to discard the ticket.

The notebook creates these rows directly so that we can inspect the complete example. It also enables SQLite foreign-key checking and defines a status constraint. Those choices make later changes meaningful. We can distinguish an allowed unassigned ticket from a reference to a staff member who does not exist.

[Sources]
- Notebook 09, original synthetic staff and ticket fixture.

## Slide 5

This first query asks for active tickets. The FROM clause identifies the input table. The WHERE condition keeps rows whose status belongs to our active set. The SELECT list chooses the fields we want to see. ORDER BY makes the displayed order predictable, which is useful when we compare results in a notebook or explain them to another person.

The result contains ticket identities 1, 3, and 4. Ticket 2 is resolved, so it does not satisfy the condition. Ticket 3 remains because its status is new. Its missing assignee is irrelevant to this filter. We did not ask whether a ticket had a staff assignment.

This reconnects selection and projection from relational algebra. Selection chooses rows according to a predicate. Projection chooses attributes. SQL has additional details, including duplicates and NULL, so the correspondence does not mean every SQL behavior is identical to a mathematical set operation. For this small query, each returned row still represents one ticket, and the selected ticket identity lets us verify exactly which tickets contributed.

In the Python output, the missing assignee appears as None. That is the Python value used for the SQL NULL we selected. It does not indicate that Python lost the row. Before comparing this count with another report, state the population in words: all tickets whose current status is active, including those with no assignment.

[Sources]
- Notebook 09, active_sql.
- Course textbook, Chapters 2 and 15.

## Slide 6

Before we aggregate anything, consider the rows that a staff-first left join produces. The matching condition requires both a matching assignee identity and an active ticket status. Priya matches ticket 1. Her resolved ticket 2 does not satisfy the active-status part. Noah matches ticket 4. Elena has no matching active ticket, but the left join preserves her staff row and fills the ticket fields with NULL.

That last row is a joined result row. It is not a newly created ticket. The database has not assigned ticket 3 to Elena, and it has not inserted anything into the tickets table. The NULL ticket fields let the query retain a staff member who has no match.

Where is ticket 3? Its assignee is NULL, so it does not equal any staff identity in the matching condition. A left join preserves the rows from its left input, which is staff here. It does not promise to preserve every row from the tickets input. That is why inspecting the direction and matching rule is more informative than remembering only the phrase left join.

If Priya had two active tickets, she would produce two matching rows before grouping. If another staff member had no tickets, that person would receive another NULL-extended row. These small variations help us predict which expression we should count. We want the matched ticket identity, not every row produced by the join.

[Sources]
- Course textbook, Chapter 15, worked SQL example.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 7

Here is the complete staff report. The selected staff identity and name identify the group. COUNT of the ticket identity calculates the number of matching tickets in that group. We group by both the identity and name, and we sort by identity for a stable display.

The ON condition has two parts. The assignee identity must equal the staff identity, and the ticket must have an active status. Both parts help decide whether a ticket is a match. Because this is a left join, a staff member with no qualifying ticket still appears. That preservation is part of the question we are answering: include every staff member, including those with zero active tickets.

COUNT of a column ignores NULL values in that column. Elena's joined row has a NULL ticket identity, so it contributes zero to this count. Priya and Noah each have one actual matched ticket identity. This gives us one, one, and zero without inventing a fake ticket or requiring a special row for Elena in the ticket table.

The identity in the grouping is important too. Two staff members could have the same display name. Grouping only by name could merge their workloads. A readable name is useful for the report, but it should not silently replace the entity's identity. In the notebook, report_sql holds this statement so we can rerun the unchanged report after a controlled data change.

[Sources]
- Notebook 09, report_sql.
- Course textbook, Chapters 2 and 15.

## Slide 8

The result is Priya one, Noah one, and Elena zero. Adding those counts gives two assigned active tickets. Our earlier query found three active tickets because it also included ticket 3, the unassigned ticket. We can reconcile the populations explicitly: two assigned active tickets plus one unassigned active ticket equals three active tickets altogether.

That explanation is different from saying the database lost a row. The staff report did exactly what its join and count requested. The issue is whether the dashboard describes the report clearly and whether the manager also needs to see the unassigned category. If the manager uses only this staff table as a complete backlog, the missing category becomes an application-design problem even though the SQL is valid.

One solution is to show an unassigned queue alongside staff workloads. Another is to design a combined report with an explicitly labeled unassigned category. The appropriate shape depends on the decision the interface supports. We should not assign the ticket to a nonexistent person just to make a sum match.

This is a useful operational habit: compare independently defined populations, then explain the difference through record identities. A total is informative only when we know what contributes to it. The same habit applies to event counts, document groups, restored records, and synchronized copies. In each case, a plausible number still needs a clear interpretation.

[Sources]
- Notebook 09, active and staff query results.

## Slide 9

Two small edits can make this report wrong in different ways. First, replacing COUNT of the ticket identity with COUNT star counts every joined row. Elena has one joined placeholder row, so COUNT star gives her one. That is an incorrect workload for Elena, even though the sum now happens to equal the backlog count of three.

This coincidence is why checking only a grand total can be dangerous. The report has not found the unassigned ticket. It has counted a placeholder belonging to a different population. Looking at Elena's result and the actual ticket identities reveals the error immediately.

The second edit moves the active-status test into WHERE after the join. Elena's ticket status is NULL in the unmatched row. The condition is not true for that row, so WHERE removes her. The output now omits a staff member whom the question required us to include. Filtering the right-side records in ON and filtering joined rows in WHERE have different meanings for an outer join.

The notebook runs both versions so you can compare them with the original. This is a counterexample technique: choose a small case that exposes the difference between two apparently similar queries. A staff member with no matching ticket is especially useful here. When you adapt this for your guide, explain the individual result as well as the total, rather than deciding correctness from whichever sum looks familiar.

[Sources]
- Notebook 09, COUNT(*) and WHERE counterexamples.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 10

Now we change one fact. Ticket 3 becomes assigned to Elena. We leave its status as new, so it remains active. During that change, Elena's active count becomes one. Priya and Noah still have one each. The assigned total becomes three, while the overall active-ticket total remains three because we have not opened, resolved, inserted, or deleted any ticket.

The SQL outline shows a transaction beginning before the update and a rollback after we inspect the reports. The notebook uses a Python value for the target staff identity and binds it through a question-mark placeholder. It also places rollback in a finally block so that the controlled change is undone even if reading a result raises an exception.

After rollback, the original unassigned state returns. Elena has zero again, and the assigned total returns to two. We can rerun the cell without accumulating assignments. That repeatability makes it useful for testing an explanation rather than changing a real workload.

Try a different existing staff identity when you are ready to adapt the example. Predict which individual count changes and which total stays fixed. The foreign key should reject an identity absent from staff. Our deliberate transaction is a rehearsal boundary, not an instruction to roll back arbitrary work in somebody else's database. It operates only on this notebook's disposable in-memory data.

[Sources]
- Notebook 09, TARGET_ASSIGNEE experiment.
- https://docs.python.org/3/library/sqlite3.html

## Slide 11

This second transaction makes two attempts. Assigning ticket 3 to Elena is valid. Changing its status to finished violates the CHECK rule, because our schema allows new, open, in progress, and resolved. The database rejects that invalid status, and Python reports an expected integrity error.

We then explicitly roll back the transaction. That rollback discards the earlier successful assignment as well. Reading ticket 3 afterward gives an unassigned ticket with status new. The result connects two separate mechanisms: a constraint decides whether a value is acceptable, while the transaction boundary determines which provisional changes become permanent or are undone together.

Be careful about the SQLite behavior here. A failed statement does not generally prove that every preceding statement in the same transaction has been undone. Our code establishes that outcome by issuing rollback. PostgreSQL has its own transaction-error behavior, which we studied earlier. We should not generalize every detail of one engine's error handling from this small local example.

This also gives us a precise communication example. We can say that we attempted an invalid status, observed a constraint rejection, rolled back the controlled transaction, and checked the remaining values. We cannot call that a permission test. The notebook did not switch users or test an unauthorized request. Naming the mechanism accurately helps another person understand both what worked and what we would need to test separately.

[Sources]
- Notebook 09, expected constraint failure and rollback.
- https://docs.python.org/3/library/sqlite3.html

## Slide 12

Here is ticket 3 represented as JSON. The ticket identity is stored under underscore id. The assignee is null, and the status is new. The notebook builds similar dictionaries for all four tickets and serializes them as JSON text. SQL NULL appeared as Python None when we fetched rows, and JSON serialization represents that missing assignment with JSON null.

Those spelling differences belong to different languages. They do not indicate different business facts in this example. JSON property names and string values use double quotes. JSON null has no quotes, because it is a value rather than the text spelling of a value. The notebook uses a serializer so that it does not have to build JSON by concatenating strings.

The document still means one ticket. assignee_id remains a reference to staff rather than an embedded staff profile. Merely changing from a table row to a JSON object does not create a staff assignment, enforce a relationship automatically, or decide which records a report should include.

We previously considered embedding and referencing based on access patterns and update responsibilities. Those decisions remain relevant. For today's comparison, keeping the same facts and identities lets us isolate the reporting question. The notebook creates JSON in memory and displays it. It does not create a collection in Atlas, and it does not transfer credentials or account information anywhere.

[Sources]
- Notebook 09, document conversion.
- Course textbook, Chapters 9, 10, and 15.

## Slide 13

This MongoDB reference pipeline starts from tickets. The match stage keeps documents whose status belongs to the same active set used by our SQL query. The group stage uses assignee_id as the group key and adds one for each qualifying ticket. With the four supplied documents, identities 201 and 202 each have a count of one, and the null group also has a count of one.

There is no Elena group because there is no active ticket assigned to Elena. The pipeline starts from the ticket population. It has no input document representing a staff member with zero tickets. The unassigned ticket, however, is in that input, so it contributes to the null group. These results are consistent with the same underlying records we inspected earlier.

The displayed pipeline does not promise an output order. A sort stage would be needed if a particular display order were part of the requirement. The notebook executes a small Python grouping loop to illustrate the calculation without a cloud connection. That loop is not a MongoDB query engine or a substitute for testing MongoDB-specific behavior on a server.

To build a zero-inclusive staff report with documents, we would need to start with or combine the staff population deliberately. Changing query languages does not settle the population question for us. A useful explanation begins with the input records, the stage that changes their meaning, and the records absent from that input.

[Sources]
- Notebook 09, Python grouping and MQL reference.
- https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/

## Slide 14

Our restore example starts correctly. The notebook exports the SQLite database as SQL statements, creates a separate in-memory connection, and executes those statements there. Comparing the ordered ticket rows initially reports a match. We then deliberately change ticket 1 only in the restored copy, setting its status to resolved instead of open.

Both databases still contain four tickets. Ticket 3 remains unassigned in both. A row-count check therefore passes, even though the two versions of ticket 1 disagree. Comparing ordered identities and values detects the wrong status. The original database stays unchanged, and the restore cell can recreate its own target before repeating the experiment.

This reconnects our PostgreSQL and MongoDB recovery lessons. A successful command and the expected number of rows are useful checks, but neither establishes every relevant property of the restored system. We also need known records, types, relationships, and behavior appropriate to the artifact and platform. Permission and service configuration may require separate restoration or reconstruction.

The notebook's export lives only in a Python variable. It demonstrates a logical restore mechanism, but it is not a durable off-machine backup. Losing the notebook process would lose that variable too. When explaining your actual recovery work, distinguish the artifact you preserved, the target you reconstructed, and the checks you performed. The small example gives us a clear failure to reason about without pretending to reproduce a cloud disaster.

[Sources]
- Notebook 09, isolated SQLite restore and deliberate wrong-value comparison.
- Course textbook, Chapters 8, 12, and 15.

## Slide 15

The review notebook reconnects several ideas, but some claims need their original platform and request path. For access control, an administrator's successful read does not tell us whether the intended application user has the right access. A meaningful test uses that identity for an allowed operation and an operation that should be denied. An integrity constraint and an access policy answer different questions.

For performance, keep the query, parameters, dataset, and returned records consistent while you compare the plan and examined work. An index changes maintenance and storage costs too. A tiny example can show query meaning without supporting a claim about production latency. Use the earlier measured lab when describing your index investigation.

For recovery, reconstruct an isolated target and check relevant data and rules. The exact commands differ between PostgreSQL and MongoDB. A text export does not automatically carry every setting of the original service. For a system with two stores, identify which record owns a fact before deciding which copy should repair the other. Matching counts alone do not settle that question either.

These are useful final-project review prompts. Choose the operation that your project actually implements and explain its result. If a test has not run, identify it as a proposed next check. That lets your audience distinguish your completed work from your plan while keeping the technical discussion specific and useful.

[Sources]
- Course textbook, Chapters 6, 7, 8, 12, 14, and 15.
- Canonical final-project assignment.

## Slide 16

A concept guide can fit in one README. The title on this example names a concrete question: why an active ticket can be absent from a staff report. The opening tells the reader which idea the example teaches. The example section supplies the small dataset, the query, and the relevant output. The explanation connects that output to the preserved population and the matching rule.

The text on this slide is a structure to fill, not a completed submission. Your contribution is the explanation of a small variation that you understand. You might assign the unassigned ticket to a different person, add a staff member with no tickets, or compare the two count expressions. Another course concept is equally valid if you can show its mechanism clearly.

A reader also needs enough environment information to reproduce the example. If your code uses this notebook, say that it runs with Python and SQLite. If it requires PostgreSQL or MongoDB, identify that requirement instead. Explain the run order, what the operation can change, and how to clean up the disposable objects. These can be concise sentences within the same guide.

Include a limitation and source credit. You do not need separate documents for setup, evidence, reflection, and a runbook. A small script or notebook can help when the code is easier to run as a file, but code inside well-labeled Markdown fences is a valid option for this lab.

[Sources]
- Week 15 individual GitHub concept lab.
- Course textbook, Chapter 15.

## Slide 17

GitHub lets you write this guide in the browser. Create a repository and include a README, or open a repository you already own. Open README.md and select the pencil icon to edit it. You need permission to change the repository. Editing a file in somebody else's repository may instead start a proposed contribution, which is unnecessary for this assignment.

Markdown headings and code fences make the file readable. A heading begins with a hash sign followed by a space. A code fence begins with three backticks and a language name such as sql or python. Put the code on the following lines, then end the block with another line of three backticks. The language label helps GitHub format the code, but it does not execute the program or verify its correctness.

Use Preview to inspect the rendered guide. Check that the code stays inside its block, that the expected result is clearly labeled, and that any links point to the intended material. Commit changes with a short message describing the update. A commit records a version of the file. It does not make an untested result become an observed result.

For public work, inspect the published page while signed out. For private work, give the instructor access through the repository's collaboration settings. Never put a password or service key into the README to make an example easier to run. A runtime prompt or a clearly marked placeholder is the appropriate boundary.

[Sources]
- https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
- Week 15 individual GitHub concept lab.

## Slide 18

The final in-class lab is individual work. Choose one database concept and develop a small example that teaches it. You can begin with the review notebook or use another course exercise that you completed. Change one input or query, predict its effect, and explain the resulting behavior in your own words. The purpose is to make the mechanism understandable to another beginner.

A single README can contain the whole guide. Include the example, its result, and the explanation, with the environment and safe run order. State cleanup, one limitation, and any source you adapted. A separate notebook or code file is optional. You do not need a full application, a slide deck, or a second reflection report.

If the guide is a static worked explanation rather than an executed demonstration, label the result as predicted. A carefully checked explanation is valid, but its wording should not imply that you ran a cloud operation you did not run. If you adapt course material, keep its relevant attribution and license notice. Your own changed example and explanation should be easy to identify.

Before sharing, review the files and saved outputs for secrets or real personal information. Submit the public or instructor-accessible URL in Brightspace with one sentence naming the concept and result. If an account or accessibility barrier prevents GitHub use, we can use the equivalent private file path described in the lab rather than inventing another assignment.

[Sources]
- Week 15 individual GitHub concept lab.

## Slide 19

Our second meeting focuses on your final demonstrations. Use the canonical final-project assignment for the required work and the demonstration length. You can present from your notebook, code, and prepared results. You do not need to build a new presentation just to introduce a project that already has a clear executable explanation.

Begin with the user problem. For a support system, perhaps staff need a current queue and managers need a workload summary. Show enough of the model to explain one relationship or document boundary. Then choose a query whose result matters to that user. Explain what one output row or document means and why the result answers the question.

Next, show an operational decision from your project. That might be an index comparison, an allowed and denied access test, or a recovery procedure and its verification. Connect the decision to the workload rather than presenting a list of features. State the limitation that matters for interpreting the result and the improvement you would test next.

Keep a saved-output fallback in case the connection fails during your demonstration. Say that it is a saved result and identify its context. Do not expose a secrets page or paste a credential into the projector view. The audience should be able to follow the database reasoning even if the cloud dashboard is unavailable. Presenting a controlled result clearly is more useful than improvising a risky account change in front of the room.

[Sources]
- Canonical final-project assignment, Presentation and Submission sections.
- Course textbook, Chapter 15.

## Slide 20

Here is a complete explanation of our review query. The support manager needs to see staff workload, including staff with zero active tickets. I keep staff on the left of the join and make active status part of the matching condition. I count matching ticket identities rather than all joined rows. The result is Priya one, Noah one, and Elena zero.

I then compare that assigned workload with the active-ticket query. The latter also contains ticket 3, which has no assignee. That record explains the difference between the staff total of two and the complete active total of three. If the manager needs the full backlog, I would show an explicitly labeled unassigned category instead of pretending every active ticket belongs to a staff member.

Notice the sequence. It gives the user need, the query decision, a concrete result, and the implication for the report. It also leaves room for a technical follow-up. Someone can ask what happens if a staff member has two tickets, if a ticket is reassigned, or if the active-status condition moves to WHERE. We can answer by following the same records and testing one change.

This particular explanation belongs to the four-row review example. In your final demonstration, use the corresponding facts and observed output from your own project. You do not need to memorize this paragraph. You need to make the relationship between your question, code, and result equally clear.

[Sources]
- Notebook 09, report and counterfactual results.
- Course textbook, Chapter 15.

## Slide 21

The first statement says only that you used SQL in a class. It names a topic but gives a reader little basis for understanding your skill. The second statement names an investigation: diagnosing a zero-inclusive staff report with joins and NULL-aware counts, then testing an assignment change to distinguish the staff workload from the full backlog.

That is a useful resume bullet if it describes work you actually did and understand. It identifies a technical action and a result without inventing a dramatic business impact. You do not need a percentage improvement when your result was a corrected interpretation or a reproducible counterexample. If you have a measured performance result from another lab, use its actual context and comparison rather than borrowing one for this example.

The environment should be accurate. This review ran in SQLite inside Python. It does not become a Supabase deployment simply because Supabase was part of the course. If you independently ran the equivalent SQL against your PostgreSQL project, describe that work and its result. A project label or education section can make the classroom context clear without weakening a precise technical statement.

An interviewer may ask you to explain any term in the bullet. Be ready to show what NULL-aware counting means, why the join preserves Elena, and what the assignment experiment changed. Choose a statement whose details you can discuss, rather than a longer list that includes work you only watched or planned.

[Sources]
- Course textbook, Chapter 15, portfolio and resume writing.
- Notebook 09, executed review example.

## Slide 22

STAR-R gives an incident explanation a useful order: situation, task, action, result, and reflection. Here is one way to tell the review story. A dashboard showed a backlog of three active tickets, but the staff workload counts summed to two. My task was to explain the difference without hiding an active ticket or assigning it to the wrong person.

I traced the matched rows of the left join and compared them with the active-ticket population. I tested an assignment change inside a transaction and read the report before rolling that change back. The unassigned ticket explained the original gap. Assigning it to Elena changed the staff total without changing the number of active tickets, and rollback restored the starting state.

My reflection was that a complete backlog view needs an explicitly labeled unassigned category. A report can execute successfully and still be misunderstood if its population is unclear. In a real application, I would also check the interface labels and the other workflows that consume the report.

This story is grounded in a small classroom experiment, and that context is enough. The action is specific, and the result is observable. Practice an equivalent outline individually using one thing you completed. You can keep it in your notes or concept guide. It is not another graded submission. The outline supports conversation, so expect a follow-up rather than treating the opening answer as a script that must end the discussion.

[Sources]
- Course textbook, Chapter 15, STAR-R framework.
- Notebook 09, assignment and rollback experiment.

## Slide 23

Suppose the interviewer asks what changes if ticket 3 is assigned to Elena. Begin with the fact that changes: its assignee identity becomes 203. Its status remains new, so it stays in the active-ticket population. The staff join now finds a qualifying ticket for Elena, and her count changes from zero to one.

Priya and Noah keep their counts of one. The staff total rises from two to three, while the overall active total remains three. No ticket was inserted or removed, and no status changed. The controlled rollback returns ticket 3 to the unassigned state, which returns Elena's count to zero and the assigned total to two.

We can check that explanation by running the report and active-ticket query before, during, and after the transaction. The important comparison is the same queries against one deliberately changed fact. If we also changed status or inserted rows, we would need to account for those effects separately.

This is how a follow-up can become an opportunity to reason. You do not have to produce an unfamiliar command immediately. State the assumption, follow the data through the operation, predict the result, and identify a way to test it. If the question changes a property your experiment did not cover, say so. A precise next test is more useful than confidently applying an unrelated rule from memory.

[Sources]
- Notebook 09, controlled assignment experiment.
- Course textbook, Chapter 15, follow-up questions.

## Slide 24

If someone asks whether you would choose PostgreSQL or MongoDB, begin with the workload. Suppose appointments connect known clients with shared time slots and require rules about valid relationships. Relational tables, keys, and transactions are a reasonable starting design. Preventing overlapping appointments would still require an explicit scheduling rule and a tested implementation. Merely choosing PostgreSQL does not automatically prevent every conflict.

Now suppose the workload stores variable form snapshots that are usually read as complete records. A document model may fit that access pattern, provided we define identity, validation, and the update behavior. We would still consider how large the records can become and whether any shared facts need an authoritative location.

Neither example makes the format an exclusive product capability. PostgreSQL can store JSON, and MongoDB can represent references. The decision includes query shapes, relationships, transaction boundaries, access, growth, and recovery. The simplest design that meets those needs is a sensible starting point.

If the system genuinely has both responsibilities, a second store can be justified, but it adds synchronization and recovery work. Our previous incident showed why a derived copy can lag behind an accepted source update. Explain what benefit would justify that cost and what measurement could change your decision. A beginner can give a thoughtful design answer by stating assumptions and tradeoffs without claiming experience operating every alternative at scale.

[Sources]
- Course textbook, Chapters 9, 10, 14, and 15.
- Canonical final-project platform options.

## Slide 25

The table connects course actions with workplace responsibilities. Correcting a report and checking its population can matter in application support or data analysis. Testing a permission boundary supports database administration and security work. Comparing query plans can matter to backend development as well as database performance. Restoring a separate target and checking it belongs to operational recovery, while repeatable imports connect with data integration.

These responsibilities overlap. A small organization may assign several of them to one person, while a larger organization may distribute them across specialized roles. The O*NET database-administrator profile is one reference for the vocabulary of database changes, access, performance, and recovery. It does not mean one introductory course satisfies every requirement of every job with that title.

When you read a posting, connect one requested action to a specific piece of your work. If it mentions troubleshooting, identify the incident you investigated and the query or observation that supported your diagnosis. If it mentions automation, identify a repeatable import or restore procedure rather than listing Python by itself. Then separate completed experience from a skill you want to develop next.

The final GitHub guide can help because it gives you a small example to discuss. It should be understandable and technically specific even to somebody who was not in our class. A useful portfolio item does not have to demonstrate every responsibility in this table. Depth in one clearly explained workflow gives a reader something concrete to evaluate.

[Sources]
- https://www.onetonline.org/link/summary/15-1242.00
- Course textbook, Chapter 15, skill matrix.

## Slide 26

Choose your next learning project from a specific gap rather than a long list of product names. If a role asks for operational scripting, you might automate a logical restore into a disposable target. The script could check known record identities and values, verify a required constraint, and report a failed check clearly. That builds on a workflow you have already studied while adding one new responsibility.

Begin with a manual procedure that you understand. Identify what can change, what must remain untouched, and how you will recognize success or failure. Then automate one part. A script that reliably reports a mismatch is useful even when the example dataset is small. You can later extend it with scheduling, monitoring, or a larger fixture as separate learning steps.

Keep the explanation alongside the code. Name the environment, input, observed result, and remaining limitation. If an experiment fails, record what failed and the next diagnostic question. That record can become an interview example because it shows how you investigate, not only which tool you opened.

Across this course, the recurring work has been to define data meaning, choose a mechanism, predict behavior, and check the actual result. SQL and MQL syntax will continue to evolve, and workplaces will use different platforms. Your ability to explain a query population, a transaction boundary, an access decision, or a recovery check gives you a way to approach those unfamiliar systems deliberately.

[Sources]
- Course textbook, Chapter 15, next-skill planning.
- Course recovery and integration notebooks.

## License

Original course prose is licensed under CC BY 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
