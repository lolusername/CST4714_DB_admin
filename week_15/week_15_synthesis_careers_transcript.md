# Week 15: Course Review, Demonstrations, and Career Communication - Spoken Transcript

## Slide 1

Welcome to Week 15, our last week together. I want to start with a report that looks wrong. Look at the three lines on the slide. Three active tickets. Two assigned tickets. One report to explain. The support dashboard says three tickets are active, but when you add up every staff member's active count, you get two. So is the database losing a ticket? Before anyone touches the code, we have to decide whether those two numbers should even be equal. A staff workload report and a full backlog report can both be correct and still be counting different things.

We will work this out with just four tickets, so every record stays visible. On the way we will touch almost everything from the semester: selecting rows, a left join, counting, a transaction we roll back, the same facts as JSON, and a restore whose row count matches even though a value is wrong.

Here is the plan. Day 1 is this worked review, and then you build one individual GitHub concept guide, which is a single README. Day 2 is final demonstrations and interview practice. Your demonstration slot follows the schedule in Brightspace, and slots may continue into the final exam meeting. The final-project assignment is still the source of its requirements. Nothing today adds extra reports or asks you to build a new application.

[Sources]
- Course textbook, Chapter 15, and Notebook 09: Four Tickets, Two Different Totals.

## Slide 2

Here is the frame for the whole review: six questions you can ask about any database system. They map onto the semester.

Purpose comes first. Which user, and which decision, does this support? It comes first because the same stored facts can support different decisions. A manager handing out today's work needs a different report from someone checking for an unassigned backlog, and "the SQL ran without an error" does not tell you which one you built. Model: what does one record mean, and how do identities connect? In our example, staff and tickets are different populations. Protect: which bad states and which unauthorized actions are refused? Those are two different things. A constraint can reject a bogus status, but it does not decide who is allowed to close a ticket. Perform: which query shapes matter, and what measured work supports them? An index decision needs a workload and a comparison, not just an index that exists. Recover: which failure do we tolerate, and how do we verify the restore? Reproduce: can someone else follow your setup without you handing them a password?

Read the line at the bottom. One ticket report connects data meaning with operational decisions. You can use these six as a path through your final demonstration. You do not need equal time on each one. Pick the ones your project actually tests.

[Sources]
- Course textbook, Chapter 15, system-review framework.

## Slide 3

This is our tool for Day 1, Notebook 09, Four Tickets, Two Different Totals. Choose Open in Colab on the weekly page and run the cells in order. Colab needs a Google sign-in, but you do not need an Atlas or Supabase account, a database password, or any package installation. Local Jupyter works too.

Look at the table. First row: SQLite runs inside Python, so this is real SQL with real constraints, a real rollback, and an isolated restore. But the database lives in memory, inside the notebook, completely separate from your Supabase project and your Atlas cluster. Why do it this way? Because today I want you changing things freely, and nothing you do here can damage a cloud project.

Second row: later cells turn the same ticket facts into Python dictionaries and JSON. Third row: the MongoDB pipeline you will see is a reference printed on the page. It is a comparable grouping, not a live Atlas connection. The notebook never sends it anywhere.

Let's be honest about the boundary. SQLite does not have PostgreSQL's roles, its lock behavior between sessions, or Supabase's request path, and it is not a replica set. We use it for query meaning, a constraint failure, rollback, and a small restore. Run it once in order, then go back to the assignment cell and change one input. There is no notebook submission.

[Sources]
- Notebook 09, setup and execution boundaries.
- https://docs.python.org/3/library/sqlite3.html

## Slide 4

Here is the entire dataset. Look at the left table first: three staff members, Agent 201, Agent 202, and Agent 203. One row per staff member. Now the right table: four tickets. Ticket 1 is assigned to 201 and open. Ticket 2 is also assigned to 201, but resolved. Ticket 3 is new and has NULL in assignee_id. Ticket 4 is assigned to 202 and open.

Read the definition at the bottom, because everything today depends on it. Active means new, open, or in_progress. So before we run a single query, we can predict the answer: tickets 1, 3, and 4 are active. That is three. Two of them have an assignee. Agent 203 is a real staff member with no tickets at all. Ticket 3 is a real ticket with no staff member at all. Both are legitimate. Nothing here is broken data.

Why does that NULL matter so much? Because it is the schema's way of saying "no assignment yet." It does not mean staff ID zero, it does not mean an empty name, and it is definitely not a reason to throw the ticket away. The notebook also turns on SQLite's foreign-key checking and adds a CHECK constraint on status. Those two choices let it tell an allowed unassigned ticket apart from a reference to a staff member who does not exist. Keep these two tables in your head. Every number today comes from them.

[Sources]
- Notebook 09, original synthetic staff and ticket fixture.

## Slide 5

First query: which tickets are active? Read it the way the database does. FROM tickets is the input. WHERE keeps the rows whose status is in our active set. SELECT picks the three columns we want to see. ORDER BY ticket_id makes the order predictable, so when you compare your output with mine, the rows line up.

The result is IDs 1, 3, and 4. Active-ticket count: 3. Ticket 2 is gone because it is resolved. Now look at ticket 3. It is still there, even with no assignee. Why? Because we never asked about assignment. The filter only looked at status.

This is the relational algebra from Week 2. Read the box. WHERE selects matching rows. That is selection. SELECT chooses columns. That is projection. SQL has extra wrinkles, like duplicates and NULL, so it is not identical to the math, but the last line holds here: the result still has one row per ticket. And because we kept ticket_id in the output, we can check exactly which tickets contributed. A count with no IDs behind it is much harder to argue about.

When you run this in Python, ticket 3's assignee prints as None. That is just Python's spelling of SQL NULL. The row was not lost. So say the population out loud: all tickets that are currently active, including unassigned ones. That sentence is what we compare against next.

[Sources]
- Notebook 09, active_sql.
- Course textbook, Chapters 2 and 15.

## Slide 6

Before we count anything, I want you to see the rows a left join actually produces. Staff is on the left. The matching rule has two parts: the assignee has to equal the staff ID, and the ticket has to be active.

First row: Agent 201 matches ticket 1, open. Ticket 2 also belongs to 201, but it is resolved, so it fails the active part and does not match. Second row: Agent 202 matches ticket 4. The third row is the interesting one. Agent 203 has no matching active ticket, but because staff is on the left, the join keeps that staff row anyway and fills the ticket columns with NULL.

That NULL row is a joined result row. It is not a ticket. Nobody inserted anything, and ticket 3 has not been assigned to Agent 203.

So where is ticket 3? Read the second line in the box. Its assignee is NULL, and NULL does not equal any staff ID, so it matches nobody. A left join promises to keep every row from the left side. It makes no promise about the right side. That is why I want you to look at which side is preserved and what the match rule is, instead of just remembering the words "left join."

Now predict: if Agent 201 had two active tickets, you would get two rows for that agent before grouping. Which brings us to the real question. Which column do we count?

[Sources]
- Course textbook, Chapter 15, worked SQL example.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 7

Here is the full staff report. Read it top to bottom. We select the agent ID and the name, plus COUNT of t.ticket_id as active_count. FROM staff on the left, LEFT JOIN tickets. The ON clause has the two-part match we just traced: the assignee equals the agent, and the status is active. Then GROUP BY the agent ID and name, and ORDER BY the agent ID.

Two choices make this report correct, and I want you to be able to explain both. First, the status test lives inside ON. Read the first line of the box. The ON condition defines a matching active ticket. Because "active" is part of what counts as a match, the left join can still keep a staff member with zero matches. And that is the question we were asked: every staff member, including zero.

Second, look at what we count. COUNT of a column skips NULLs. Agent 203's placeholder row has a NULL ticket_id, so it adds nothing. That is how we get a real zero without inventing a fake ticket.

One more detail. Why group by the ID and not just the name? Because two people can share a display name. Group only by name and you could quietly merge two people's workloads into one. The name is for reading. The ID is the identity.

In the notebook, this statement is saved as report_sql, so we can rerun the exact same report after we change the data.

[Sources]
- Notebook 09, report_sql.
- Course textbook, Chapters 2 and 15.

## Slide 8

And here is the result. Agent 201, one. Agent 202, one. Agent 203, zero. Add them up and you get two. Our first query said three active tickets. So which query is wrong?

Neither one. Look at the line across the middle: assigned active, 2. Unassigned active, 1. All active, 3. Two plus one is three. The difference is ticket 3, the unassigned one. The staff report did exactly what the join and the count asked for. It counts tickets that belong to staff, and ticket 3 belongs to nobody.

So the real problem is not the SQL. It is whether the dashboard says what it is showing. If a manager looks at this staff table and treats it as the whole backlog, ticket 3 is invisible to them. That is an application design problem, even though every query is valid. Read the bottom line: a staff workload report needs a separate unassigned category to describe the full backlog. You could show an unassigned queue next to the staff counts, or add a clearly labeled unassigned row. What you must not do is assign the ticket to a made-up person just to make the sum match.

Here is the habit I want you to keep. When two totals disagree, define each population, then explain the gap with actual record IDs. It works the same way for event counts, document groups, restores, and synchronized copies.

[Sources]
- Notebook 09, active and staff query results.

## Slide 9

Now let's break the report on purpose, two different ways, because that is how you prove you understand the correct version.

Look at the table. The first row is our correct report: count ticket IDs, with the status test in ON. Agent 203 gets zero.

Second row: swap in COUNT star. COUNT star counts every row, including Agent 203's NULL placeholder. So Agent 203 gets one, for a ticket that does not exist. And here is the trap, in the box at the bottom. The COUNT star version totals 3. One plus one plus one. It matches the backlog, by accident. It did not find ticket 3. It counted a placeholder from a completely different population. If you only check the grand total, you would sign off on a wrong report. Check Agent 203's row and the error is obvious.

Third row: keep COUNT of ticket IDs, but move the status test into WHERE. Now the filter runs after the join. Agent 203's row has a NULL status, so the condition is not true, and WHERE throws the row away. Agent 203 is absent from the report entirely, which breaks the one thing the question asked for. On an outer join, filtering in ON and filtering in WHERE mean different things.

The notebook runs both broken versions next to the original. This is the counterexample technique: pick one small case, here a staff member with no tickets, that makes two similar queries disagree.

[Sources]
- Notebook 09, COUNT(*) and WHERE counterexamples.
- https://www.postgresql.org/docs/current/queries-table-expressions.html

## Slide 10

Now we change exactly one fact and watch what moves. Here is the SQL outline: BEGIN, assign ticket 3 to Agent 203, run the staff report and the active-ticket query again, then ROLLBACK.

Predict before you look. Ticket 3's status stays new, so it is still active. Now read the first result line. During the change: Agent 201, 1. Agent 202, 1. Agent 203, 1. All active: 3. Agent 203 went from zero to one, and the assigned total went from two to three. The active total did not move, because we did not open, resolve, insert, or delete anything. We only changed who the ticket belongs to.

Second line. After rollback: Agent 201, 1. Agent 202, 1. Agent 203, 0. All active, still 3. We are back where we started. That is why the change sits inside a transaction. You can run the cell as many times as you want and nothing piles up.

Look at the small note at the bottom. The notebook does not paste the ID into the SQL string. It binds a target ID through a placeholder, and it puts the rollback in a finally block, so the change is undone even if reading a result throws an error.

When you adapt this, try a different staff ID and predict which count moves and which total stays put. An ID that is not in the staff table should be rejected by the foreign key. And remember, this rollback is a rehearsal on disposable data.

[Sources]
- Notebook 09, TARGET_ASSIGNEE experiment.
- https://docs.python.org/3/library/sqlite3.html

## Slide 11

This transaction makes two moves, and they end up in different places. Read the table from the top.

Step one: assign ticket 3 to Agent 203. That is valid, so it succeeds, provisionally. Step two: set the status to finished. Our CHECK constraint only allows new, open, in progress, and resolved, so the database rejects finished, and Python reports an integrity error. We expected that error. Step three: ROLLBACK in the finally block. And here is the point. That rollback throws away the assignment too, even though the assignment was perfectly valid. Step four: read ticket 3 again. assignee_id is NULL, and status is new. Exactly where it started.

So we have two mechanisms doing two jobs. The constraint decides whether a value is acceptable. The transaction decides which changes become permanent together, or get undone together.

Now read the box at the bottom carefully, because this is easy to get wrong. It was our explicit rollback that undid the assignment. In SQLite, the failed statement by itself does not establish that the earlier statement was undone. PostgreSQL handles an error inside a transaction in its own way, which we studied earlier, so do not generalize one engine's behavior from this tiny example.

And name what you tested accurately. This was a constraint test with a rollback. It was not a permission test. Nobody switched users.

[Sources]
- Notebook 09, expected constraint failure and rollback.
- https://docs.python.org/3/library/sqlite3.html

## Slide 12

Here is the same ticket 3, now as JSON. Look at the three fields. _id is 3. assignee_id is null. status is new. The notebook does this for all four tickets.

Notice how the spelling changes as we move between languages. In SQL it was NULL. When Python fetched the row, it became None. Now in JSON it is null, lowercase, with no quotes, because it is a value, not the text "null." Three spellings, one fact: there is no assignment. The notebook uses a JSON serializer for this instead of gluing strings together, which is how you avoid broken quotes.

Now read the box. Each document still means one ticket. assignee_id remains a reference to a staff member, not an embedded staff profile. And the last line is the one I care about most: changing the representation does not assign ticket 3 to a staff member. Moving from a row to a document does not create relationships, does not enforce them, and does not decide which records a report includes. Those are still your design decisions.

We talked about embedding versus referencing when we did document modeling, and that reasoning still applies. Today we keep the same facts and the same IDs on purpose, so the only thing that changes is the representation. That isolates the reporting question. And to be clear, this JSON lives in memory. Nothing is sent to Atlas.

[Sources]
- Notebook 09, document conversion.
- Course textbook, Chapters 9, 10, and 15.

## Slide 13

Here is the comparable grouping in MongoDB. Read the pipeline. The match stage keeps documents whose status is in the same active set we used in SQL. Then the group stage uses assignee_id as the group key and adds one for each ticket.

Look at the results. 201 has 1. 202 has 1. And null has 1. That null group is ticket 3, the unassigned ticket. It is in the input, so it gets counted, just under null.

Now the important line: there is no Agent 203 group. Why not? Because this pipeline starts from tickets. There is no input document for a staff member with zero tickets, so there is nothing to group. Compare that with the SQL report, which started from staff and kept Agent 203. Same records, different starting population, different answer. Switching query languages did not settle the population question for us. If you wanted a zero-inclusive staff report here, you would have to start from the staff population, or combine the two on purpose.

Also notice that group order is unspecified. If the order matters to the reader, add a sort stage.

And read the bottom box honestly. This pipeline is a reference for a collection containing these four documents. The notebook actually runs a small Python grouping model that does the same calculation. It is not MongoDB and it is not Atlas, so it does not test any server behavior.

[Sources]
- Notebook 09, Python grouping and MQL reference.
- https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/

## Slide 14

This slide is about why a row count is not a restore check. The notebook exports the SQLite database as SQL statements, builds a separate in-memory database, and runs those statements there. The first comparison says everything matches. Then the notebook does something deliberate: it changes ticket 1 only in the restored copy, from open to resolved.

Read the table. Number of tickets: 4 in the source, 4 in the copy. Ticket 3's assignment: NULL and NULL. So a count check passes. But look at the middle row. Ticket 1 is open in the source and resolved in the copy. If you only counted rows, you would call this restore good, and a manager would see a closed ticket that is actually still open.

What catches it? Comparing the ordered IDs and their values. That is the second line in the box. The original database is never touched, and the cell rebuilds its own target before you rerun it.

This connects back to our recovery work in PostgreSQL and MongoDB. A successful restore command and the right number of rows are useful signals, but you also need known records, relationships, and rules. Permissions and service settings may need their own rebuild.

Now read the last line. The SQL dump lives in memory, in a Python variable. It demonstrates the mechanism, but it is not a durable off-machine backup. If the notebook process dies, the dump dies with it.

[Sources]
- Notebook 09, isolated SQLite restore and deliberate wrong-value comparison.
- Course textbook, Chapters 8, 12, and 15.

## Slide 15

Our notebook covers a lot, but some claims need the real platform. This table points each concern back to the kind of test you already ran in your completed course work.

Access: read as the intended user, then attempt a forbidden action. Why both? Because an administrator's successful read tells you nothing about what the application user can do. And remember that a CHECK constraint is not an access policy. They answer different questions.

Performance: compare the same query and the same returned records before and after an index. Keep the query, the parameters, and the data fixed, or the comparison means nothing. An index also costs storage and write work. A four-row example can show query meaning, but it cannot support a claim about speed, so use your measured lab for that.

Recovery: check the isolated restore's data and its required rules, the way we did on the last slide, but on the real engine.

Multiple stores: compare authoritative IDs and values with the derived copy. Decide which store owns a fact before deciding which copy repairs the other.

Now read the box. SQLite here does not reproduce Supabase row-level security, PostgreSQL lock diagnosis, or Atlas replication. If your demonstration makes one of those claims, back it with the earlier lab. And if a test has not run yet, call it a proposed next check. That lets your audience tell your completed work apart from your plans.

[Sources]
- Course textbook, Chapters 6, 7, 8, 12, 14, and 15.
- Canonical final-project assignment.

## Slide 16

Now we shift to your Day 1 lab, the concept guide. This is what one looks like, and it all fits in a single README.

Look at the title: "Why an active ticket is absent from a staff report." It is a question, and a concrete one. That is much better than a title like "SQL Joins," because it tells the reader exactly which puzzle they are about to understand. Under it, one sentence saying the example uses a left join and one unassigned ticket. Then a section called Example and result, with the small setup, the query, and the output. Then Explanation, where you explain the preserved population and the example you changed.

Read the box at the bottom. This is README structure, not a completed submission, so please do not just copy it. Your contribution is the explanation of a small change you understand. You could assign the unassigned ticket to someone else, add another staff member with no tickets, or compare the two COUNT expressions. Or pick a different concept from the course entirely.

The second line of the box lists what else a reader needs: the tool, the run order, cleanup, one limit, and source credit. If your example uses this notebook, say that it runs with Python and SQLite. Each of those can be one sentence. You do not need separate files for setup, evidence, and reflection.

[Sources]
- Week 15 individual GitHub concept lab.
- Course textbook, Chapter 15.

## Slide 17

Here is how to build the guide entirely in the browser. No terminal, and no Git installed on your machine.

Read the steps. Create a repository with a README, or open one you own. Open README.md and select the pencil icon. You need permission to change that repository. If you try to edit somebody else's, GitHub will offer to start a proposed contribution instead, and you do not need that.

Third step: code goes inside fenced blocks. Look at the example on the right. Three backticks and the word sql, then the query on its own line, then three backticks to close the block. The language label tells GitHub how to color the code. It does not run the code, and it does not check that it is right. That is still your job.

Then use Preview. Make sure the code stays inside its block, the expected result is clearly labeled, and your links work. Then Commit changes, with a message that says what you did. A commit records a version of the file. It does not turn a predicted result into an observed one.

If the repository is public, open the link while signed out to make sure it works. If you keep it private, give me access, and if you are not sure which account to add, ask me in class. And never put a password or service key in the README to make an example easier to run. Use a clearly marked placeholder.

[Sources]
- https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files
- Week 15 individual GitHub concept lab.

## Slide 18

Here is the lab itself. It is individual work, and we do it in class.

Read the four lines. Choose one concept and a small example. You can start from the review notebook, or use another course exercise you completed. Change one input or query, predict what will happen, then explain the result in your own words. Why predict first? Because explaining a result you predicted shows you understand the mechanism, not just that you ran a cell. Put the example and the explanation in one README. Then review the files before you share them: no credentials, no real personal data, and any cleanup touches only your example's disposable data.

If your guide is a worked explanation that you did not execute, label the result as predicted. That is a valid guide. Just do not word it as if you ran something you did not run. And if you adapted course material, keep its credit and license notice.

Now the submission box. Submit one public or instructor-accessible URL in Brightspace, with one sentence naming the concept and the result. That is the whole submission. A separate notebook, a presentation, or a full application is not required. And if an account or accessibility barrier keeps you off GitHub, the lab allows a local Markdown or code file instead. Talk to me in class rather than inventing another assignment.

[Sources]
- Week 15 individual GitHub concept lab.

## Slide 19

This starts the Day 2 material: final demonstrations. Your requirements come from the canonical final-project assignment, not from this slide. Your demonstration slot follows the schedule in Brightspace, and demonstrations may run across our Week 15 meetings and the final exam meeting, so we are not trying to fit everyone into one class.

Read the three lines. A user problem. A model and query you can explain. An operational decision you tested. That is the arc. Start with who needs what. For a support system, maybe staff need a current queue and a manager needs a workload summary. Show just enough of the model to explain one relationship or one document boundary. Then show a query whose result matters to that user, and say what one output row or document means.

Then show one operational decision: an index comparison, an allowed and denied access test, or a restore and how you verified it. Tie the decision to the workload, and state the limitation that matters.

Look at the second box. Present from your notebook, code, or prepared results. A new deck is optional. Keep a saved-output fallback in case the connection fails, and if you use it, say that it is a saved result. Never show a secrets page or paste a credential on the projector. A controlled result explained clearly beats improvising a risky account change in front of the room.

[Sources]
- Canonical final-project assignment, Presentation and Submission sections.
- Course textbook, Chapter 15.

## Slide 20

Here is what a complete query explanation sounds like, using our review example. Read it with me.

"The support manager needs to see staff workload, including zero." That is the user need. "I kept staff on the left and counted matching ticket IDs." That is the query decision, and notice it is really two decisions, not one. "The result was Agent 201 1, Agent 202 1, Agent 203 0." That is a concrete result, with names and numbers. "Ticket 3 was still active but unassigned, so I identified it as a separate part of the backlog." That is the implication for the report.

Notice the sequence: need, decision, result, implication. It is short, and it invites good follow-up questions. What if a staff member has two tickets? What if ticket 3 gets reassigned? What if the status test moves into WHERE? You can answer every one of those by following the same four tickets and testing one change. That is the payoff of choosing a small example you fully understand.

Now read the box at the bottom. This describes the four-row review example. In your final demonstration, describe your own project and the output you actually observed. You do not need to memorize this paragraph. What you need is to make the link between your question, your code, and your result just as clear as it is here.

[Sources]
- Notebook 09, report and counterfactual results.
- Course textbook, Chapter 15.

## Slide 21

Let's turn the same work into a resume bullet. Look at the first one: "Used SQL in a database class." That names a topic. A reader learns nothing about what you can actually do.

Now the second one. "Diagnosed a zero-inclusive staff report with SQL joins and NULL-aware counts, then tested an assignment change to distinguish the assigned workload from the full backlog." It names an investigation, the techniques, and a result. And notice what it does not do. It does not invent a percentage or a dramatic business impact. When your result is a corrected interpretation or a reproducible counterexample, say exactly that. If you have a real measured result from another lab, use that one, with its real context.

Read the box. Use this wording only after doing and understanding the work. And name the actual environment. This review ran in SQLite inside Python. It does not become a Supabase deployment just because Supabase was part of the course. If you ran the equivalent SQL against your own PostgreSQL project, say that.

Here is the test for any bullet. An interviewer can point at any phrase and say "tell me about that." Can you explain what NULL-aware counting means? Why the join keeps Agent 203? What the assignment experiment changed? If yes, keep the bullet. If you only watched the work, leave it off.

[Sources]
- Course textbook, Chapter 15, portfolio and resume writing.
- Notebook 09, executed review example.

## Slide 22

Interviewers often ask, "Tell me about a problem you investigated." STAR-R gives your answer a shape: situation, task, action, result, and reflection. Let's walk the table.

Situation: the backlog count was 3, but staff counts summed to 2. Task: explain the discrepancy without hiding a ticket, and without assigning it to the wrong person. Action: I traced the matched rows of the left join and tested an assignment inside a transaction. Result: the unassigned ticket explained the gap, and rollback restored the starting state. Reflection: the report needs a named unassigned category for the whole backlog.

Why the extra R? Because reflection is where you show judgment. Anyone can describe what they did. Saying what you would change in the design is what makes an interviewer believe you would handle it well on the job.

Notice that the result is observable. Three versus two, and then explained. That is what makes the story believable. It is a small classroom experiment, and that is fine. Say so. A specific small story beats a vague big one.

Read the line at the bottom. Practice your own version individually, in your notes, using one thing you completed. This is not another submission. And remember that the outline is the start of a conversation, not a speech that ends it. Expect a follow-up question, which is exactly what the next slide is about.

[Sources]
- Course textbook, Chapter 15, STAR-R framework.
- Notebook 09, assignment and rollback experiment.

## Slide 23

Here is a typical follow-up: "What changes if ticket 3 is assigned to Agent 203?" Let's answer it the way I want you to answer every follow-up. Start with the one fact that changes, and follow it through.

Ticket 3's assignee becomes 203. Its status stays new, so it is still active. Now read the answer on the slide. Agent 203's count changes from 0 to 1, because the join now finds a qualifying ticket. The assigned total changes from 2 to 3. The active total stays 3, because no ticket changed status, and nothing was inserted or removed. Agents 201 and 202 keep their count of one each. And rolling back restores the earlier assignment and report: Agent 203 back to zero, and the assigned total back to two.

Look at the line at the bottom. Explain the mechanism, then identify the query or experiment that checks it. Here, that means running the report and the active-ticket query before, during, and after the transaction. Same queries, one deliberately changed fact.

Why does this matter in an interview? Because you do not have to produce some unfamiliar command on the spot. State your assumption, follow the data through the operation, predict the result, and name the test. If the question changes something your experiment did not cover, say so. A precise next test is worth more than a confident rule you half remember.

[Sources]
- Notebook 09, controlled assignment experiment.
- Course textbook, Chapter 15, follow-up questions.

## Slide 24

Another classic interview question: "Would you choose PostgreSQL or MongoDB?" The honest answer starts with the workload, and then you actually say what the workload is. Look at the table.

First row: appointments share clients and time slots. Lots of shared facts, relationships, and rules about what is valid. So a reasonable starting design is relational tables, keys, constraints, and transactions. But be careful. Choosing PostgreSQL does not automatically stop overlapping appointments. You would still need an explicit scheduling rule, and you would test it.

Second row: variable form snapshots that are read as complete records. That access pattern fits a document model, as long as you define clear identity and validation, and think about how large the documents can grow.

Third row: both responsibilities exist. Then a second store might be justified, but only if its benefit pays for the synchronization and recovery work. You saw that cost last week in our incident, where a derived copy fell behind an accepted update in the source.

Now read the bottom box. PostgreSQL can store JSON. MongoDB can reference documents. So "my data is JSON" does not decide anything. A format label alone does not decide which system fits. The decision comes from query shapes, relationships, transactions, access, growth, and recovery. State your assumptions and your tradeoffs. That is a strong answer, even without years of experience running both systems.

[Sources]
- Course textbook, Chapters 9, 10, 14, and 15.
- Canonical final-project platform options.

## Slide 25

This table connects work you did in this course to responsibilities you will see in job postings. Read across each row.

Correct a report and verify its population: that is application support and data analysis. Test a permission boundary: database administration and security support. Compare plans and index costs: backend development and database performance. Restore and check a separate target: database operations and recovery. Load data repeatedly without duplicate identities: data integration and engineering.

Now read the box at the bottom, because it keeps you honest. These responsibilities overlap across roles. At a small company, one person might do all five. At a large one, they are split across teams. The O*NET profile for database administrators is a good reference for this vocabulary. But one course does not establish all the requirements of a job, and nobody expects it to.

So here is how to use a posting. Pick one action it asks for and connect it to one specific piece of your work. If it says troubleshooting, name the incident you investigated and the query that supported your diagnosis. If it says automation, name a repeatable import or restore, not just "Python." Then separate what you have done from what you want to learn next.

Your GitHub guide helps here. It is one small example you can discuss in depth, and depth in one clearly explained workflow gives a reader something real to evaluate.

[Sources]
- https://www.onetonline.org/link/summary/15-1242.00
- Course textbook, Chapter 15, skill matrix.

## Slide 26

Last slide. What do you learn next? My advice is to choose one gap in a role that interests you, not a list of product names.

Read the three lines. Choose one gap. Build one small experiment that addresses it. Describe the result and the next question it raises.

Look at the example. If a role asks for operational scripting, you could automate a logical restore into a disposable target, check known records and constraints, and report a failure clearly. Why is that a good project? Because it builds on a workflow you already understand, the restore check from slide 14, and adds exactly one new responsibility, automation. Start with the manual procedure. Know what can change, what must stay untouched, and what success and failure look like. Then automate one piece. A script that reliably reports a mismatch is useful even on a small dataset. Scheduling and monitoring can come later, as separate steps.

Keep the explanation next to the code: the environment, the input, the observed result, and the limit. If it fails, write down what failed and your next question. That record is an interview story.

Read the last line. Keep expanding a workflow you can explain rather than adding tool names. That has been the whole course: define what the data means, choose a mechanism, predict, and check the actual result. Syntax and platforms will change. That habit transfers. Thank you for a great semester.

[Sources]
- Course textbook, Chapter 15, next-skill planning.
- Course recovery and integration notebooks.

## Slide 27

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Four tickets, two totals: the course in one report (1:32); From lab evidence to a portfolio bullet (1:11); Presenting a technical decision (1:19). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 15 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
