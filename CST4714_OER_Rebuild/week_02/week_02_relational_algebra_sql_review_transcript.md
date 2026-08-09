# Week 2: Relational Algebra and SQL Review Studio - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Relational Algebra and SQL Review Studio

This week is a major SQL and relational-model review. The course will not assume that syntax remembered from an earlier class is immediately available. We will rebuild it through a repeatable sequence: state the question, identify result grain, choose relational operations, predict the output, execute SQL, and verify the result.

The goal is not to race through every SQL feature. The goal is to recover the core language that administration depends on: filtering, projection, sorting, joins, grouping, subqueries, common table expressions, set operations, and safe data changes. Every query will produce evidence, not just an answer displayed on a screen.

## Slide 2: A correct query begins before the word SELECT

Many SQL mistakes are not grammar mistakes. The query runs, but its result has the wrong grain, duplicates, missing rows, or an unintended filter. Starting from `SELECT` encourages us to assemble clauses before the question is precise.

Instead, state the question and what one result row represents. Identify the source relations and operations. Predict stable identifiers, columns, and approximate count. Then write SQL. Verification comes after execution because a successful command proves only that the database accepted the syntax and completed the operation. It does not prove that the query answered the intended question. This sequence lets you recover syntax from meaning and diagnose results without guessing.

## Slide 3: Result grain controls how every clause should be read

Result grain is the fastest way to make a query understandable. A query that returns ticket identifiers, subjects, and priorities may remain at one row per ticket. Once ticket events are joined, a ticket can repeat because one result row may now represent one matching ticket-event pair.

Aggregation changes grain deliberately. Grouping by status produces one row per status group, not one row per ticket. Every selected expression must make sense at that grain: either it identifies the group or summarizes rows within the group. Before running a query, complete the sentence ‘one output row represents.’ After running it, inspect the identifiers or group keys that can confirm the claim.

## Slide 4: Relational operations map to SQL, but semantics still matter

This mapping is useful, but SQL is not a perfect spelling of mathematical relational algebra. Selection commonly becomes `WHERE`, and projection commonly becomes the column list after `SELECT`. A join becomes a `JOIN` with a condition that defines valid tuple pairs. Grouping creates a new grain and uses aggregate functions. Difference can appear as `EXCEPT` or as a carefully written `NOT EXISTS` condition.

The checks column matters because SQL tables and results often behave as bags, allowing duplicate rows. SQL also includes `NULL` and three-valued logic. Those features do not make SQL unrelational; they mean that translating an operation requires attention to the language's actual semantics.

## Slide 5: Selection and projection become WHERE and the column list

The comment records the expected result grain: one row per matching ticket. The `FROM` clause identifies the source relation. The `WHERE` predicate performs selection by retaining high-priority tuples. The column list performs projection by retaining only the ticket identifier, subject, and priority. `ORDER BY` changes presentation order; it does not change which rows belong to the result.

Before running this query, inspect the small fixture and predict the matching identifiers. After running it, compare those identifiers and the row count with the prediction. If the query returns unexpected rows, inspect the stored priority values and predicate. Do not add `DISTINCT`, because there is no join here that should multiply ticket rows.

## Slide 6: NULL means unknown or absent, not an ordinary value

`NULL` marks missing or unknown information. It is not the number zero, an empty string, or an ordinary value that equals itself. The predicate `assignee_id = NULL` does not become true for unassigned tickets. Use `IS NULL`.

Three-valued logic also affects negative predicates. If a status is `NULL`, then `status <> 'closed'` evaluates to unknown, not true. The `WHERE` clause retains only rows for which the predicate is true, so the unknown row is excluded. Whenever missing data matters, write small examples containing a known value, a different known value, and `NULL`. Predict each predicate instead of relying on an everyday-language interpretation of ‘not closed.’

## Slide 7: Sorting and limiting require a deterministic question

This query asks for the three newest active tickets. The `WHERE` clause defines active using an explicit set of status values. The `ORDER BY` clause sorts newest opening times first. The second sort key, `ticket_id`, makes ties deterministic when two tickets share an opening time. `LIMIT 3` is meaningful only after the order is defined.

Without `ORDER BY`, a database is free to return any three qualifying rows. Physical storage order is not a contract. Even with an order, decide how `NULL` values should be placed if the sort attribute permits them. State the business definition of active and newest instead of assuming the column names supply the complete meaning.

## Slide 8: An inner join keeps matching tuple pairs

The join condition `users.user_id = tickets.requester_id` defines valid pairs. User 101 matches two ticket tuples, so that user's attributes repeat in two result rows. User 102 matches one ticket. Because each ticket has one requester in this model, the result can still be described as one row per matching ticket. That claim depends on the relationship and constraints.

An inner join drops source tuples with no match. If a user has no ticket, that user does not appear. If a ticket contains an invalid requester identifier and no foreign key prevents it, that ticket also disappears from this join. Before interpreting a join, inspect both its condition and which unmatched source rows the join type retains or drops.

## Slide 9: Write the relationship in ON, then filter the result in WHERE

Read this query from the data relationships outward. `tickets` is named `t` and `users` is named `u`; aliases shorten references without changing the relations. The `ON` clause states that the requester's identifier in a ticket must match the user's identifier. The `WHERE` clause then keeps only open joined rows.

One output row represents one open ticket and its matching requester. The selected attributes support that grain: ticket identifier, ticket subject, and requester display name. Verify the result by first selecting open ticket identifiers from `tickets` alone, then confirming the requester identifier for each and looking up those users. That second reasoning path is slower but valuable for a small fixture.

## Slide 10: LEFT JOIN preserves the left side and marks missing matches

An inner join answers questions about matches. A left join answers questions that must preserve every tuple on the left, including those with no match. If tickets are on the left and agents are on the right, an unassigned ticket remains in a left-join result with `NULL` in the agent attributes.

Predicate placement matters. A condition on the right table placed in `WHERE` can remove the `NULL` rows and accidentally turn the result into inner-join behavior. When the condition defines which right-side tuples may match while preserving unmatched left rows, place it in the `ON` clause. Always build a fixture containing at least one unmatched left tuple so the difference is visible.

## Slide 11: One-to-many joins can multiply rows without being wrong

Suppose ticket 1003 has three status events. Joining tickets to ticket events produces three rows containing ticket 1003. That repetition is the correct representation of three matching pairs. It becomes a counting error when a query uses `count(*)` and labels the result ‘number of tickets.’ The count is actually joined rows, which may mean events.

Repair begins with the question. To count events, joined rows may be correct. To count tickets that have events, group by ticket identity, use `count(distinct ticket_id)` with care, or use `EXISTS`, depending on the intended result. Do not use `DISTINCT` as a visual cleanup step before understanding why rows repeat.

## Slide 12: GROUP BY changes grain; HAVING filters groups

This query begins with ticket rows opened on or after the stated date. `WHERE` filters those source rows before grouping. `GROUP BY status` changes the grain to one result row per status value. `count(*)` summarizes the number of qualifying ticket rows in each group. `HAVING` then removes groups whose count is less than two.

A common error is selecting `subject` alongside `status` and `count(*)` without grouping or aggregating the subject. At one row per status, there may be many subjects and no single subject value represents the group. Every selected expression must either identify the group or summarize values inside it.

## Slide 13: Subqueries and CTEs can name intermediate reasoning

Subqueries and common table expressions are ways to compose relational results. A subquery can produce a set used by `IN`, answer an existence question with `EXISTS`, or act as a derived relation. A correlated subquery refers to the current outer row, so its semantics and potential cost deserve attention.

A common table expression, introduced with `WITH`, names an intermediate query. That name can make grain explicit: first compute one row per ticket with the latest event, then join that result to users. A CTE is not automatically a performance optimization. Use it to clarify reasoning, then inspect the actual plan when performance matters.

## Slide 14: Set operations combine compatible result shapes

Set operations combine query results with the same number of columns and compatible types. `UNION` returns rows that occur in either result and removes duplicate result rows. `UNION ALL` appends results and keeps duplicates, which is often faster and semantically correct when repeated rows matter. `INTERSECT` keeps rows present in both. `EXCEPT` keeps rows from the first result that are absent from the second.

Column names come from the first query, but positions determine compatibility. Relational union and difference operate on sets; SQL gives explicit choices about duplicates. For anti-join questions, compare `EXCEPT` and `NOT EXISTS`, especially when `NULL` can appear in compared values.

## Slide 15: Test a data change inside a transaction before keeping it

Data manipulation should be treated as an operation with scope and evidence. `BEGIN` creates an explicit transaction boundary. The update uses the primary key in its predicate, which makes the intended target narrow and checkable. The following `SELECT` verifies the row and value while the change is still uncommitted. `ROLLBACK` discards the transaction so the teaching fixture returns to its starting state.

In a real change, count the target rows before updating and inspect the command's affected-row result. A transaction is not a substitute for a correct predicate, backup, or authorization. It provides a boundary within which related actions can commit together or be rolled back before completion.

## Slide 16: Verification tests whether the result answers the question

Verification is not rerunning the same query and receiving the same wrong answer. Begin by restating result grain and inspecting stable identifiers. Compare the count with a prediction from the small fixture or with a simpler query that isolates one relationship.

A useful fixture includes edge cases. Test an unassigned ticket for left-join behavior, a `NULL` value for predicate behavior, several events for row multiplication, and a status that forms a small group. A second reasoning path may be a hand calculation, a different query shape, or an expected invariant. Finally, name the limit. Small-fixture correctness does not prove production performance, concurrency safety, authorization, or recovery.

## Slide 17: Lab 1: Complete the SQL query ladder

The first lab is individual and uses the Metro Support setup in an approved PostgreSQL environment. Work through the query ladder in order because each query adds one idea while the data remains familiar. Before each query, write a short grain comment and predict an identifier set or count.

Run the query and compare the result. If it differs, record what changed in your model or SQL. Do not erase every failed attempt; a concise corrected query and explanation can be stronger evidence than a perfect-looking final screenshot. Submit one SQL file containing the assigned queries, grain comments, and verification notes. The notebook provides an open DuckDB path when cloud PostgreSQL is unavailable.

## Slide 18: Lab 2: Join, summarize, and rehearse a safe change

The second lab is also individual. Begin with a relationship question and choose inner or left join based on whether unmatched left rows belong in the result. Account for repeated and missing rows using identifiers, not visual intuition.

Next, produce one grouped result. State what one group row represents, place source-row predicates in `WHERE`, and place aggregate predicates in `HAVING`. Finish with a narrow data change inside an explicit transaction. Verify the changed row and roll back. Submit one evidence record containing the SQL, selected outputs, and a short statement of what the checks prove and do not prove. No database URL or password belongs in the artifact.

## Slide 19: SQL fluency is recoverable when the result has a model

This review rebuilt SQL as relational reasoning rather than a list of clauses. Selection and projection control rows and attributes. Joins create matching pairs and can multiply rows. Left joins preserve unmatched tuples. Grouping creates a new result grain. Subqueries, CTEs, and set operations compose results. Transactions provide a safe rehearsal boundary for data changes.

The durable habit is to predict and verify. If a result is surprising, return to grain, relationship, `NULL`, duplicate behavior, predicate placement, and the fixture's edge cases. Next week we will use these query skills to inspect and build schemas. The course will continue retrieving SQL, so this is not the last opportunity to practice it.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
