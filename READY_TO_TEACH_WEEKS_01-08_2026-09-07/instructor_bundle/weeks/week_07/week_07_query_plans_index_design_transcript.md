# Week 7: Query Plans and Index Design - Spoken Transcript

## Slide 1

A support queue displays twenty tickets. The page looks small, but that tells us almost nothing about how much work the database performed to build it. PostgreSQL might have inspected thousands of candidates, compared their opening times, and then returned the twenty that belong at the top. Today we will make that hidden work visible.

Our starting point is the SQL you already know. WHERE defines which tickets qualify. ORDER BY defines the requested order. LIMIT restricts the number returned. Those clauses describe the answer. A query plan describes a strategy for producing it. We can change that strategy by adding an appropriate index while leaving the application's question unchanged.

The first class is about reading that strategy carefully. We will distinguish estimated rows from observed rows, follow data through a scan and sort, and test whether a smaller result necessarily means less scanning. The second class is about changing the available access path. We will explain how an ordered index can help, measure a real example, and identify a case where that same index cannot supply the requested data.

The practical skill is a defensible recommendation. A developer needs to know which query benefits, whether its answer stayed correct, and what maintaining the index costs. A fast number alone does not answer those questions. We will use synthetic data in a disposable schema so the experiment is understandable and safe to repeat.

[Sources]
- Course Chapter 7 and Week 7 synthetic fixture.
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 2

Here is the complete question for the demonstration: return the twenty newest tickets whose status is in_progress. Each output row represents one ticket. We select the identifier, subject, and opening time so a staff member can recognize the request and see why it appears in the queue.

Read the SQL in terms of that question. FROM names the demonstration table. WHERE selects in-progress tickets. ORDER BY opened_at DESC requests later timestamps first. LIMIT 20 asks for at most twenty of those ordered matches. An index will not be allowed to change any of these requirements during the before-and-after comparison.

The first five identifiers in this fixture are 99906, 99905, 99904, 99903, and 99902. There are twenty in the full result. We keep the full ordered list before changing the database, then compare it afterward. A count of twenty by itself would miss a replacement of one ticket by another.

The table has distinct opening times because the fixture assigns them at two-minute intervals. That gives this exercise an unambiguous order. Real requests can arrive at the same timestamp, so a real queue may also need a stable tie-breaker such as ticket_id in its ORDER BY. We are not adding that second design problem to today's experiment.

Your individual lab uses the same kind of question for open tickets in a separate schema. The mechanism transfers, but your qualifying rows and final identifiers differ from this demonstration.

[Sources]
- Course performance_lab_setup.sql and locally executed Week 7 demonstration.
- https://www.postgresql.org/docs/15/indexes-ordering.html

## Slide 3

The test data contains one hundred thousand tickets. Five thousand are in progress, two thousand are open, three thousand are new, and ninety thousand are closed. These are deliberately uneven groups. A filter for one status can require very different amounts of work from a query that needs almost every row.

Our earlier twelve-ticket case was useful for checking joins, missing assignments, constraints, and exact answers. At that size, reading the whole table is usually inexpensive. Adding an index to twelve rows often teaches very little about the tradeoff. The larger fixture keeps the data understandable while making differences in access work visible.

The demonstration table is a separate copy named performance_demo.tickets. Your lab uses performance_lab.tickets. This separation lets the instructor show an index without silently changing the baseline for your own experiment. It also gives us an explicit cleanup boundary. Resetting this teaching schema is different from resetting an entire Supabase project.

The setup finishes with ANALYZE. In that standalone command, ANALYZE gathers statistics that help the planner estimate the distribution. It does not create an index. We will later distinguish it from the ANALYZE option inside EXPLAIN, which runs a query and measures its execution.

These rows are synthetic. They are not a sample of actual city requests, and their distribution does not establish what a production application needs. They give us a reproducible case for learning how to ask and test a performance question.

[Sources]
- Course performance_lab_setup.sql.
- https://www.postgresql.org/docs/15/planner-stats.html

## Slide 4

EXPLAIN is a prefix attached to a SQL statement. With plain EXPLAIN, PostgreSQL shows the strategy it plans to use and estimates the work. It does not execute the planned SELECT to produce its result. This lets us inspect the proposed access path before running the measured version.

EXPLAIN with ANALYZE actually executes the statement and reports observations from that execution. In our case it runs a SELECT on synthetic tickets. It returns a plan report rather than the normal twenty-row result, which is why we ran the plain SELECT separately to capture the identifiers.

BUFFERS adds information about database page activity. A page holds data, and PostgreSQL maintains a cache of pages. We will use the counters to understand whether the chosen path touched many pages or very few. They are not a measurement of how many rows the browser displayed.

The important safety distinction is execution. EXPLAIN ANALYZE on an UPDATE performs the update. The word explain does not make a write harmless. A rollback can undo ordinary transactional row changes, but it does not undo every possible external effect or sequence allocation. We will analyze only the trusted SELECT statements in this lesson.

Plain EXPLAIN is also not a sandbox for arbitrary untrusted SQL: planning itself can require locks or evaluate eligible expressions. The relevant classroom habit is to know the statement and the environment before requesting either form. Here both are explicit and bounded.

[Sources]
- https://www.postgresql.org/docs/15/using-explain.html
- Course Chapter 7, EXPLAIN safety discussion.

## Slide 5

This is an abbreviated plan captured from the actual demonstration on local PostgreSQL 15. The indentation shows parent and child relationships. The Limit at the top receives rows from Sort. Sort receives rows from the sequential scan at the bottom.

Begin with that scan. Its filter keeps status equal to in_progress. It outputs five thousand qualifying rows and reports ninety-five thousand rows removed by the filter. There is one loop, so we do not need to multiply these values by repeated executions in this example. Together, the kept and rejected rows account for the hundred-thousand-row fixture.

Next, Sort must determine which opening times belong first. The reported top-N heapsort maintains a bounded set of the best candidates rather than fully sorting every candidate into a complete final sequence. That saves some sorting work. It still needs to examine the input because a newer ticket might occur later in the scan.

Finally, Limit accepts twenty rows. Notice that the sort also reports twenty actual output rows. That value describes what it delivered to its parent. It does not say that only twenty rows reached the sort. Its child tells us that five thousand candidates arrived.

We have omitted timing and some plan details here to make the row flow readable. We have not changed the recorded counts or invented a simpler dataset. Your current plan is the authority for your own run, even if a different version or setting chooses another strategy.

[Sources]
- Locally captured Week 7 plan, September 7, 2026.
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 6

The diagram separates three different quantities that are easy to collapse into one. The scan examines one hundred thousand rows. Of those, five thousand survive the status condition. The final queue contains twenty. Each number answers a different question about the same execution.

The arrows represent rows moving between database operators. They do not represent network messages, and the boxes do not represent separate database servers. The scan, sort, and limit are parts of one plan for one query.

Following the arrows upward, the scan supplies candidates to the sort. The sort finds the latest candidates in the requested order. The limit asks for only the first twenty. PostgreSQL can often stop a child when its parent has enough rows, but that does not remove work the child must do before it can know the correct first row. This particular sort has to consider all qualifying timestamps before it can identify the newest ones.

That is why the small result does not prove a small search. Imagine a stack of unsorted request cards. Keeping only the five newest cards on the desk as you inspect the stack uses little desk space, but you still inspect the stack. An ordered structure would change the situation because it would give you a justified place to begin.

This distinction prepares the index hypothesis. We want an access path that finds the qualifying tickets in the needed order, so PostgreSQL can satisfy the limit without first scanning and comparing all those unrelated rows.

[Sources]
- Course-authored row-flow explanation based on the captured Week 7 plan.
- https://www.postgresql.org/docs/15/indexes-ordering.html

## Slide 7

A plan line contains both predictions and observations. The estimated rows value comes from the planner's model. The actual rows value comes from this execution. They are not competing measurements of the same moment: the estimate is available before execution, while the actual value records what happened when the node ran.

In the captured scan, the estimate is close to five thousand and the observed output is exactly five thousand. That is a reasonable estimate. The plan still scans the whole table because accurate knowledge of how many rows match does not create a physical route to them. Statistics describe the distribution; an index provides another access structure.

The cost pair is also an estimate. The first number is startup cost, the predicted work before the node can produce its first row. The second estimates the cost of completing the node's full result. These are planner cost units, not milliseconds. The actual time fields use elapsed time from execution, so comparing the two numbers as if they used the same unit would be a mistake.

A large row-estimate mismatch can change which strategy looks attractive. That is a reason to investigate statistics, skew, or relationships among predicates. A small sampling difference is normal and does not justify a maintenance ritual.

There is one further subtlety after indexing: a parent Limit can stop an index scan early. An estimate for the full matching range and twenty rows actually requested do not, by themselves, prove a bad estimate. Read the parent before judging the child.

[Sources]
- Locally captured Week 7 plan.
- https://www.postgresql.org/docs/15/planner-stats.html
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 8

Two more fields prevent misleading arithmetic. First, loops counts how often a node executes. For a repeated node, actual rows is an average per execution. The small arithmetic example here is illustrative: a node producing an average of three rows across one hundred loops produces about three hundred rows overall. That is not the same as three rows total.

Our queue scan has one loop, so its observed five thousand rows are already the total output for that node. In a nested-loop join, a child can execute many times and the multiplication becomes important. We will not create a complicated join benchmark just to practice that calculation.

Second, buffer hits and reads describe page accesses. A shared hit means PostgreSQL found the requested page in its shared buffer cache. A shared read means it requested a page from below that cache. The operating system may already have the page, so a read is not automatically a physical disk operation.

These counters do not count unique business records, and a page can be accessed more than once. Parent-node figures include work below them. Adding every parent's and child's counters can count the same work repeatedly. For a concise comparison, preserve the top-level totals and use child details to explain where work occurs.

The same caution applies to timing. Parent execution includes its children's work. We want an explanation of the plan, not a sum that double-counts the tree. Keep the plan structure attached to its numbers.

[Sources]
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 9

Selectivity is a fraction: the number of rows matching a condition divided by the number of rows in the table. For this nonempty fixture, five thousand divided by one hundred thousand is 0.05, or five percent. Our demonstration keeps five percent and rejects the other ninety-five percent at the scan.

Your open-ticket lab keeps two thousand out of one hundred thousand, which is two percent. That smaller fraction is a useful clue that a suitable index might avoid considerable unrelated work. It is not a guarantee that any index will help. We also need to consider the requested order, returned columns, table pages, and the cost of following the available index.

Compare that with closed tickets, which make up ninety percent of the fixture. A query retrieving most of those rows may reasonably scan the table rather than repeatedly follow index entries to many table locations. A query needing only the newest few closed tickets could still benefit from the right ordered path. The LIMIT and ORDER BY remain part of the question.

The fraction is a simple model you can calculate from GROUP BY counts. We do not need advanced probability to use it. We do need to state what the numerator represents: all rows matching the predicate, not merely the twenty returned after the limit.

The denominator also matters. The same twenty-row output can arise from twenty candidates or twenty million candidates. Selectivity connects the condition to the data distribution rather than to the size of the screen.

[Sources]
- Course performance fixture and Chapter 7 selectivity definition.
- https://www.postgresql.org/docs/15/indexes-ordering.html

## Slide 10

The table already has an index for its primary key. Here we ask for the subject of ticket 99906. That is a different workload from asking for the latest in-progress queue. The equality condition on a unique ticket identifier identifies at most one row.

In the local plan, PostgreSQL uses the primary-key index to locate that row and returns the subject. The result is Synthetic ticket 99906. This is a useful index-supported question, and it helps us avoid a misleading diagnosis of the earlier sequential scan. The table did not lack every index. Its existing index served a different access pattern.

For the queue, knowing the primary-key order does not directly organize rows by status and opening time as an application contract. Our generated identifiers happen to increase with time, but a primary key does not generally promise that relationship. We should design for the actual predicates and ordering instead of relying on an accident of the sample generator.

A sequential scan and an index scan are therefore choices to interpret, not grades to award. The queue baseline scans broadly because it lacks the demonstrated ordered subset path. The unique lookup uses the existing primary-key path because it fits that question.

When a developer asks whether a table has an index, the more useful follow-up is which query the index supports. We can now give that question a concrete answer using two queries against the same data rather than a memorized rule about node names.

[Sources]
- Actual Week 7 primary-key lookup and local plan.
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 11

The queue example uses a scan, sort, and limit. Other SQL from earlier weeks can produce different plan operators. A node describes a kind of work, so recognizing a few names helps connect the plan to the query you wrote.

A nested-loop join takes a row from one input and looks for matches in the other. If it can make a cheap indexed lookup for each of a few outer rows, that can work well. If a large outer input repeatedly triggers expensive inner work, the loops field becomes important. Nested loop is an algorithm name, not an automatic performance failure.

A hash join prepares a lookup structure from one input and probes it with matching keys from another. Think back to joining tickets with their requesters. The SQL describes matching identifiers. A hash join is one way to perform that match; it is not a different definition of which request belongs to which person.

An aggregate consumes rows and produces summaries. A GROUP BY status count reduces the ticket rows into a few status groups. The number of summary rows can be small even when many input rows had to be read. That is the same distinction between input work and output size that appeared in our queue.

The chapter introduces additional nodes, including bitmap and index-only scans. You do not need to memorize every node or tune joins in today's lab. Begin with the actual query and identify what each visible operator contributes to its answer.

[Sources]
- Course Chapter 2 join and grouping examples; Chapter 7 plan vocabulary.
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 12

Your first lab uses the open queue in performance_lab, not the demonstration's in-progress queue. Start with the supplied setup so earlier indexes cannot silently change your baseline. The setup creates the same hundred thousand tickets and confirms that two thousand are open.

Run the query before explaining it. Then compare plain EXPLAIN with EXPLAIN ANALYZE and BUFFERS. Identify the scan, any sort, and the final limit. Use the scan's actual qualifying and rejected rows to explain why a twenty-row answer can require much more work. Keep the relevant plan lines beside the SQL so the meaning is visible without another report.

Then make one small change: replace LIMIT 20 with LIMIT 5. Predict which part of the plan should change before executing it. A smaller output does not automatically give PostgreSQL an ordered way to find the newest rows. Compare your scan's output and rows removed, not just the new five-row root result. Restore the twenty-row limit when you finish this comparison.

The final comment proposes an index mechanism without creating it yet. Explain how putting status and opening time into a useful order could change the scan or sort work. The next class will test that idea.

There is one individual SQL submission. The prediction, observation, and explanation belong together because they describe the same experiment. If your plan differs, describe it accurately. Matching a pictured node name is less important than understanding the work PostgreSQL actually performed.

[Sources]
- Course Week 7 Lab 1.
- Locally executed twenty-row and five-row student cases.

## Slide 13

We now move from observing a strategy to changing the structures available to the planner. Last class, a small output still required a broad scan and a comparison of all matching timestamps. An index can help when its ordering lets PostgreSQL begin in a useful place and stop after it has enough rows.

Before creating one, keep the query fixed. The demonstration still asks for twenty newest in-progress tickets. Its selected columns, predicate, ordering, and limit are unchanged. We retain the original ordered identifiers so that a faster but different answer cannot slip through the comparison.

The first idea today is how an ordered search structure works. Then we will distinguish a composite key from a partial index. A composite index orders by more than one column. A partial index stores entries only for rows satisfying its defined condition. These are different design choices, and neither is automatically the right answer for every query.

The instructor's experiment uses a partial index for the in-progress queue. Your individual experiment uses a composite index for the open queue. Both ask whether the mechanism avoids unnecessary work, but they do not install the same object or return the same requests.

We will also measure storage and explain the boundary of the test. Keeping an index means maintaining an additional structure as data changes. A read experiment can support a read-benefit claim; it does not establish the cost of a production write workload. A useful recommendation makes both points clear.

[Sources]
- Course Week 7 two-day learning sequence.
- https://www.postgresql.org/docs/15/indexes-multicolumn.html
- https://www.postgresql.org/docs/15/indexes-partial.html

## Slide 14

A B-tree index organizes keys into pages so a search can choose a smaller key range instead of checking every record. An internal page contains separators that guide the search to an appropriate child. Leaf entries keep the keys in order and lead to the matching table rows. The diagram is a simplified model, not a dump of PostgreSQL's physical pages.

The useful property is branching. A page can point toward many smaller ranges. Repeating that choice narrows the search quickly, so a large index can remain relatively shallow. In a simplified balanced model with roughly b children per internal page and N keys, depth grows on the order of log base b of N. We read that as the number of repeated divisions needed to reduce the search range. We are not using it to predict milliseconds.

The index and the table are distinct storage structures. For an ordinary index scan, an entry helps locate a row in the table. Finding the key is not the same as having every requested subject or other output value already available in the index.

Ordered neighboring entries also matter. After finding the relevant range, PostgreSQL can move through keys in order. That is what can make a newest-first queue efficient when the index matches its condition and requested ordering.

This structure still has costs. It consumes pages and must remain consistent when relevant data changes. The question is whether its useful navigation saves enough work on important queries to justify maintaining it.

[Sources]
- Course Chapter 7 B-tree model.
- https://www.postgresql.org/docs/15/indexes-ordering.html
- https://www.postgresql.org/docs/15/indexes-index-only-scans.html

## Slide 15

A composite index has more than one ordering key. For the lab's proposed index, status is first and opened_at is second in descending order. Read that as groups organized by status, with newest opening times first inside each group.

The small table illustrates the ordering rule. Its dates are schematic, not rows from the performance fixture. Within the open group, the later date comes before the earlier one. Across different status groups, the index is not simply a list of every ticket sorted by opening time. The leading key still separates the groups.

An equality condition fixing status to open makes one group relevant. Inside that group, the date key supplies the requested order. PostgreSQL can then consider walking the newest matching entries rather than gathering and sorting every open ticket. That is the mechanism your individual experiment will test.

If a query asks for every status together ordered only by opening time, the same argument no longer applies. Dates in different status groups may need to be combined. That does not mean a later index column can never help on its own. Planner capabilities and distributions matter; newer PostgreSQL versions include skip-scan cases. Our experiment does not rely on them.

The subject is not included in this two-column key. An ordinary index scan still retrieves the requested table values. A wider covering index is another possible design, but we will not add it without a workload reason. Start with the smallest candidate whose mechanism you can explain and test.

[Sources]
- https://www.postgresql.org/docs/15/indexes-multicolumn.html
- https://www.postgresql.org/docs/18/indexes-multicolumn.html
- https://www.postgresql.org/docs/15/indexes-index-only-scans.html

## Slide 16

The demonstration uses a different design: a partial index. Its key is opened_at in descending order, and its WHERE clause says which table rows have entries in the index. Only in-progress tickets belong to this index. That is five thousand rows in our fixture rather than all one hundred thousand.

The WHERE clause in CREATE INDEX does not delete the other tickets or change the table's definition of valid statuses. It defines the subset represented by this particular search structure. Closed, new, and open tickets remain in the table and remain available to queries through other paths.

For the demonstration query, every requested row satisfies the index's condition. Within that subset, the key order matches newest first. The hypothesis is therefore specific: this index can supply the relevant rows in the needed order and may eliminate the separate sort and broad status-filtering scan.

We captured the baseline twice before running CREATE INDEX. The fixture already has current statistics. We are not refreshing statistics, rewriting the query, or changing the row count at the same time as this index addition. Caches and background activity can still vary, so repeated observations remain important.

CREATE INDEX is appropriate for this disposable classroom table. On a busy production table, index creation also needs a deployment plan because building the structure consumes resources and ordinary index creation can interfere with writes. The lesson demonstrates the access mechanism; it is not authorization to run the same deployment command on an arbitrary live service.

[Sources]
- https://www.postgresql.org/docs/15/indexes-partial.html
- Course instructor demonstration and local execution.

## Slide 17

The new plan still begins with Limit because the application's result limit has not changed. Its child is now an Index Scan using the partial index we created. There is no separate Sort node in this captured execution.

The index contains in-progress entries in the requested opening-time order. PostgreSQL can begin with the newest relevant entry, retrieve the requested row values, and continue until the parent has twenty rows. The observed scan therefore outputs twenty rows before the limit stops further work. This is different from the baseline sort, which first had to consider five thousand candidates.

The full ordered list of ticket identifiers is unchanged. That is a necessary check. A query that returned twenty newer tickets from all statuses could look fast and plausible while violating the staff member's requirement. We preserved the original predicate as well as the count.

Notice that an index does not require every condition to appear as a separate runtime Filter line. The partial index itself contains only rows meeting its defined predicate. Its eligibility follows from the query condition. Reading the index definition is therefore part of understanding the plan.

This plan is an observation from the documented local fixture. PostgreSQL is free to choose another suitable plan when statistics, data, settings, or the query change. We do not force it to use an index to obtain a desired screenshot. We explain the selected strategy and compare the actual answer and work. Here the observed mechanism matches the hypothesis.

[Sources]
- Captured Week 7 indexed demonstration plan and identifier comparison.
- https://www.postgresql.org/docs/15/indexes-partial.html
- https://www.postgresql.org/docs/15/indexes-ordering.html

## Slide 18

Now we deliberately change the question as a separate counterexample. The query asks for open tickets rather than in-progress tickets. The partial index still contains only in-progress entries. It cannot supply the complete open queue because those requested rows are not represented in it.

This is not an index failure. It is the design boundary we chose. A structure optimized for one subset can be useful without serving every other subset. In the captured local plan, the open query returns to a scan and sort because this partial index is not an eligible complete access path for that question.

The distinction is logical before it is about speed. A query using a partial index must have a condition that guarantees its required rows lie within the indexed subset. The planner must also be able to establish that relationship. More complicated predicates and parameterized statements can require additional care, which the chapter identifies as an advanced design consideration.

Keep this counterexample out of the before-and-after timing comparison. We changed the query, so it would be misleading to compare its runtime directly with the earlier in-progress query and attribute every difference to the index. It answers a different diagnostic question: what workload does this index cover?

Your composite-index lab explores another way to organize status and time. Its structure represents all status groups rather than just the in-progress subset. That broader coverage has a different storage footprint and different useful query conditions. The lab asks you to explain the design you actually measured.

[Sources]
- Actual Week 7 nonmatching-query plan.
- https://www.postgresql.org/docs/15/indexes-partial.html

## Slide 19

An index is a stored object, so we can measure its size. This query asks PostgreSQL for the byte size of the named demonstration index. In the captured local build it occupies 131,072 bytes, which is 128 kibibytes. The binary unit uses 1,024 bytes per kibibyte. Your environment may allocate a different amount.

This measurement is more specific than saying the index uses some space. It is also narrower than a complete cost analysis. The number does not measure the table's total storage, every related file, the cost of a backup, or the amount of time a future insert will take.

When a row begins to satisfy the partial-index condition, its entry must be represented. When an indexed timestamp changes, the search structure must remain consistent with the new value. PostgreSQL has optimizations for some update cases, so saying every update always rewrites every index would be inaccurate. The general tradeoff is that another maintained structure adds work that a read-only experiment does not quantify.

There can also be cache competition and maintenance complexity. An index retained for one rarely used query might occupy resources that would be more useful elsewhere. These costs are reasons to identify the workload, not reasons to reject every index.

For the lab recommendation, distinguish an observation from a consideration. You can report the space you measured. You can identify possible write overhead that still needs a suitable test. Do not present an unmeasured write slowdown as an experimental result.

[Sources]
- Captured Week 7 index-size query.
- Course Chapter 7 index-cost discussion.
- https://www.postgresql.org/docs/15/indexes-index-only-scans.html

## Slide 20

The comparison brings the observations together without reducing the experiment to one speedup ratio. We have the same query, the same hundred thousand source rows, and the same twenty output identifiers. The deliberate structural change is the partial index.

Before the change, the local plan scans the table, filters ninety-five thousand rows, and compares the remaining five thousand timestamps. Afterward, the ordered index supplies the twenty requested rows without a separate sort. That is a mechanism we can explain from the SQL and index definition.

The buffer counters also shrink substantially in this fixture. Read their labels carefully: shared hits and shared reads are page-access counters at the reported plan level. They are not unique ticket counts, and shared reads are not automatically disk operations. We do not add parent and child counters together to manufacture a larger total.

The timing rows preserve two observations on each side rather than selecting only the smallest number. These are database execution observations from a local teaching run, not browser response times, service guarantees, or a measurement of simultaneous users. Instrumentation, cache state, scheduling, and background activity can affect small timings.

The value of the table is that the observations agree with an understood change in work. The result stays correct, the sort disappears, and the access path can stop early. If your own table did not show that pattern, a careful test-further recommendation would be better than claiming the pictured improvement happened to your database.

[Sources]
- Week 7 captured local before/after plans, repeated runs, and result comparisons.
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 21

A useful comparison holds the question steady while changing the proposed cause. The SQL text matters: selected columns, filtering, ordering, and limit should remain the same on both sides of the index experiment. The underlying rows should also remain unchanged, or a smaller dataset might be the real reason for less work.

Statistics are another possible cause. Our setup already ran ANALYZE before the baseline. We do not run another statistics refresh between the baseline and index measurement. If statistics were badly stale, investigating and refreshing them could be a separate experiment rather than an invisible second change.

Repeat observations on both sides. The first run may find pages in a different cache state from a later run. A second run is not a complete scientific benchmark, but it keeps us from treating one accidental measurement as a guarantee. Record enough of the plan to explain the result, not every possible counter in a separate spreadsheet.

When actual and estimated rows differ, read the parent. An indexed path may estimate the full qualifying range while a Limit asks for only twenty rows. That difference alone does not establish bad statistics. Compare the meaning of the measurements before trying to repair them.

If the index already exists, do not add an identical one with another name. Reset only the disposable fixture or remove the known candidate before collecting a new baseline. A before state collected after the index was installed is not a baseline for the change you claim to be testing.

[Sources]
- Course Week 7 experiment protocol.
- https://www.postgresql.org/docs/15/planner-stats.html
- https://www.postgresql.org/docs/15/using-explain.html

## Slide 22

A developer-facing recommendation can be brief and technically meaningful. The example names the in-progress queue, reports unchanged identifiers, and explains that the ordered partial index removed the separate sort in the observed plan. It gives the measured index size and states what the experiment has not established.

That is stronger than saying the database is faster. A database supports many questions and changes. We tested one particular read pattern with a known distribution. We did not test every query, concurrent writes, a cloud network, or a production service objective.

The recommendation also connects the benefit to an ongoing responsibility. If the application stops using the in-progress queue, or the meaning of that queue changes, the partial index may no longer earn its space. A future review should consider its actual workload rather than retaining it merely because it was once created.

The update is addressed to the person who maintains the application. State what was tested, what changed, and what remains uncertain. Ordinary language is appropriate as long as the technical claim is precise. In this case, the measured storage belongs in the result, while write overhead belongs in the proposed next test.

Keep, remove, and test further are all possible conclusions. Their quality depends on their support. A cautious conclusion is not automatically better, and a confident conclusion is not automatically stronger. The useful answer connects the specific data and query to an observed mechanism, then identifies what would need checking before a broader deployment decision.

[Sources]
- Course-authored example recommendation based on the Week 7 demonstration.
- Course critical-writing prompt 5.

## Slide 23

Your second individual lab tests the open queue using a composite index. Reset performance_lab with the supplied setup so you begin without a leftover candidate. Run the original twenty-row SELECT and capture its identifiers. Run the analyzed plan twice before making the index change.

The candidate has status first and opened_at descending second. Before executing its CREATE INDEX statement, explain how fixing status to open makes one ordered group relevant. Then create that one index and rerun the identical query and analyzed plan twice. Do not change the predicate or carry over the five-row limit from the first lab.

Compare the exact result identifiers first. Then compare the scan and sort work and the relevant row or buffer observations. The setup already supplied statistics, so another ANALYZE command is not part of this comparison. Use your actual output even if the planner chooses something different from the demonstration.

Measure the candidate's storage with the supplied query. Your short comment to the developer recommends keeping, removing, or investigating the index further. It includes a result check, an explanation of changed work, and a cost. Name unmeasured write overhead as something to investigate rather than a number you observed.

Everything belongs in one SQL file. If you choose removal, save your observations before dropping the named candidate. Keeping it in this disposable lab schema is also acceptable; the documented fixture reset removes it on a later run. There is no separate benchmark report or screenshot collection.

[Sources]
- Course Week 7 Lab 2 and critical-writing prompt 5.
- Locally executed composite-index student experiment.

## Slide 24

We began with a small queue and discovered a larger search behind it. The central skill is now to separate the answer from the work required to produce it. Twenty returned tickets did not mean twenty examined tickets, and an available primary-key index did not automatically solve a status-and-time query.

We followed rows through a plan, distinguished estimates from observations, and interpreted a top-N sort without mistaking its output for its input. We then used ordered index structure to explain a different strategy. The unchanged identifiers established that the structural change preserved the requested answer.

The partial-index counterexample also matters. The same object that supported the in-progress queue could not supply the open queue because it excluded those rows by design. A useful index is justified by a workload, not by its mere existence. Your composite-index experiment applies that reasoning to another access pattern.

These are practical administration skills: define the problem precisely, prepare a safe baseline, make a bounded change, inspect its consequences, and communicate a supported recommendation. None requires claiming that a classroom timing represents production capacity.

Next week we apply the same standard to backup and recovery. A file called a backup is a promising artifact, but it does not establish that the data can be restored and used. We will restore into a separate target and check behavior. Just as a faster number needed a correctness check today, a backup will need a real recovery check before it supports the claim we want to make.

[Sources]
- Course Chapters 7 and 8.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
