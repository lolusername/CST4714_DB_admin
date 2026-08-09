# Week 7: Query Plans, Measurements, and Index Design - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Query Plans, Measurements, and Index Design

This week changes performance work from intuition into an experiment. A query plan describes how PostgreSQL intends to execute a statement. `EXPLAIN ANALYZE` adds measured execution evidence. Neither output should be reduced to a rule such as ‘index scan good’ or ‘sequential scan bad.’

We will begin with the query and a repeatable baseline, read plans from their most deeply indented operations outward, compare estimated and actual rows, and form one index hypothesis. Then we will change one thing, remeasure, and decide whether the observed benefit justifies write, storage, cache, and maintenance costs.

## Slide 2: Performance begins with a workload question

‘Add an index to make the table faster’ is not a useful recommendation. Tables are not fast or slow by themselves. A workload includes query predicates, joins, ordering, grouping, frequency, concurrency, and data distribution. The objective may be lower response latency, fewer reads, better throughput, or more predictable high-percentile behavior.

The evidence must match the objective. A classroom plan can reveal access method, row estimates, loops, and buffer use, but one warm-cache execution does not establish production tail latency. State the scope precisely. We will use a deterministic 100,000-row fixture so before-and-after evidence is comparable without pretending that it simulates an enterprise workload.

## Slide 3: A controlled experiment changes one cause at a time

Begin with a question such as ‘Can an index reduce work for active tickets in one category ordered by opening time?’ Capture the exact SQL and baseline plan. Record table size and whether `ANALYZE` statistics are current. Run enough comparable observations to avoid building a claim on one accidental timing.

The hypothesis predicts a mechanism: a compound index may narrow the predicate and provide useful order, reducing scanned rows or an explicit sort. Add only that change, then rerun the same statement. The decision considers the observed benefit and the cost imposed on writes, storage, cache, maintenance, and other queries. A result of ‘do not keep this index’ is a successful experiment when the evidence supports it.

## Slide 4: Read a plan from the leaves toward the final result

A plan is a tree. The deepest child nodes access or produce rows first. Here, PostgreSQL scans tickets and users, builds a hash structure on one input, joins matching rows, and then sorts the joined output. The parent node consumes rows produced by its children.

Read each node with four questions: what rows enter, what operation occurs, how many rows leave, and how many times the node loops. The top node is the final output, not necessarily the place where most work occurs. A visually prominent sort may be cheap if only a few rows reach it, while a deeply indented scan repeated many times can dominate total work.

## Slide 5: EXPLAIN ANALYZE adds actual execution evidence

Plain `EXPLAIN` shows the planner's estimates without executing the statement. Adding `ANALYZE` executes the statement and reports actual timing and row counts. That distinction matters for writes: `EXPLAIN ANALYZE UPDATE` really updates unless protected and rolled back. This course uses safe `SELECT` statements on a deterministic fixture.

`BUFFERS` reports block activity for plan nodes. Shared hits mean needed blocks were already in PostgreSQL's shared buffer cache; reads indicate blocks requested from lower storage layers, though operating-system caching still affects physical behavior. Preserve the exact SQL and full text plan. A cropped node name removes the estimates, actual rows, loops, and context needed to interpret it.

## Slide 6: Estimates guide planning; actuals reveal execution

Planner costs are unitless estimates used to compare candidate plans. They are not milliseconds. Estimated rows come from statistics and assumptions about value distribution and predicate relationships. The planner chooses the plan with the lowest estimated total cost under its model.

`EXPLAIN ANALYZE` reports actual rows and time for this execution. Compare estimated and actual row counts at each node, while accounting for loops. A large mismatch can result from stale statistics, skew, correlated columns, parameter values, or model limitations. The response may be to refresh statistics, improve statistics, rewrite the query, or change the model. An index does not automatically repair a bad cardinality estimate.

## Slide 7: Sequential and index access are choices, not grades

A sequential scan is not a failure. If a table is small or a query needs most rows, reading the relation broadly may cost less than traversing an index and visiting many table pages. PostgreSQL evaluates estimated costs rather than following a rule that an available index must be used.

Index scans are valuable when the key order and query shape let the engine avoid substantial work. A covering or index-only plan may reduce heap access when visibility permits, but it still has conditions and costs. Judge the plan using row fraction, buffers, loops, ordering, and measured objective. The plan node name alone cannot support a keep-or-drop recommendation.

## Slide 8: Lab 1: Read the plan before changing anything

Complete this lab individually on the deterministic performance fixture. Run the assigned query and preserve the complete text plan. State the result grain and fixture size. Read from the leaf nodes upward and annotate actual rows, loops, buffers, access method, and any sort or join.

Identify where the most relevant work occurs and compare estimated with actual rows. Then state one testable hypothesis, such as a compound index that may narrow the predicate and satisfy ordering. Do not create the index in this lab. The submission is one baseline plan with interpretation, which prevents the next class from inventing a before state after the change.

## Slide 9: An index is justified by the workload it improves and the cost it adds

On the second day, we turn the baseline into an index experiment. PostgreSQL B-tree indexes order key values and row locations in a way that can support equality, ranges, and compatible ordering. Compound indexes are ordered by their defined columns, so column order must follow actual predicates and sort behavior rather than a slogan.

We will create one candidate, refresh or confirm statistics as appropriate, and rerun the same query. The evidence should show what changed in access, sort, rows removed, buffers, or runtime. The decision will also name write and storage costs and the limitations of the classroom fixture.

## Slide 10: Compound index order should reflect the query shape

A compound B-tree index has an ordered key. Equality predicates on leading columns can narrow the key range. A later date column may provide the requested ordering within each leading-key combination. The exact value depends on selectivity and the set of status values.

Included columns can allow an index to carry returned values without placing them in the ordering key, potentially supporting index-only access. Wider indexes consume more storage and write work, and index-only scans still depend on visibility information. This table is a hypothesis guide, not a universal formula. Create the smallest candidate supported by the actual query and measure its behavior.

## Slide 11: Compare the mechanism, not only the elapsed-time number

Elapsed time matters, but it is noisy and incomplete. Compare the plan mechanism. Did the access path change? Did an explicit sort disappear because the index supplied order? Did rows removed by filter decrease? Did buffer activity move or shrink? Did loops change?

Then compare repeatable runtime under similar conditions and preserve the actual result, because a faster wrong query is not an improvement. If the plan remains a sequential scan, the planner may correctly estimate that the predicate is broad, the table is small, or the index costs more. The candidate can still be rejected as unnecessary.

## Slide 12: Keeping an index creates continuing operational work

An index that improves one read can slow writes and consume storage or cache. Updating an indexed column modifies both table and index structures. Creating an index on a large production table can consume time, I/O, and locking or concurrent-build resources. Every retained index becomes an object to monitor and maintain.

Check whether another existing index already covers the prefix or workload. Name the query that justifies the object and the conditions under which it should be reconsidered. The classroom fixture supports a mechanism claim at its scale. It does not establish production concurrency, data skew, high-percentile latency, or future value distribution. Those limits belong in the recommendation.

## Slide 13: Lab 2: Test one index hypothesis

Complete the index experiment individually. Use the baseline from Lab 1 and write a specific prediction. Create only the assigned or justified candidate, preserve its exact definition, and rerun the identical query. Confirm the returned identifiers remain correct.

Compare access method, sort, estimated and actual rows, loops, buffers, and repeatable runtime. Recommend keep or drop. A keep decision names the read benefit and at least one write, storage, or maintenance cost. A drop decision explains why the candidate did not reduce the relevant work. Submit one before-and-after recommendation, then remove the candidate if the lab directs cleanup.

## Slide 14: Performance claims require a baseline, mechanism, and tradeoff

This week replaced plan folklore with an evidence cycle. A workload question and objective define the test. The baseline records the exact query, fixture, plan, and conditions. Estimates describe the planner's model; actual rows, loops, buffers, and timing describe one execution. Sequential and index access are choices with context, not grades.

An index hypothesis predicts which work should shrink. Remeasurement shows whether the mechanism changed while the result remained correct. The final recommendation includes ongoing costs and limits. Next week the evidence cycle becomes even stricter: a backup artifact will not count as recovery until it restores into a separate target and passes behavioral checks.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
