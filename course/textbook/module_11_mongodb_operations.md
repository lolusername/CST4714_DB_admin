# MongoDB Operations Connect Pipelines, Rules, and Indexes

## Operating Question

How can a MongoDB workload transform documents, reject invalid states, and find
the intended records without examining everything?

## Learning Outcomes

After this module, you can:

- trace document grain through an aggregation pipeline;
- use `$match`, `$project`, `$unwind`, `$group`, `$sort`, and `$limit`;
- add focused schema validation with `$jsonSchema`;
- read basic `explain("executionStats")` measurements;
- connect a compound index to filter and sort order; and
- make a keep/remove/test-further recommendation with operational tradeoffs.

## A Pipeline Is an Ordered Document Transformation

An active-workload report asks a different question from a ticket lookup. It
needs to select active tickets, combine them into categories, count each group,
and order the summaries. A pipeline makes those transformations visible. The
important idea is not the number of operators: at every step, know what one
output document represents.

For a complete runnable example, use the
[aggregation and validation notebook](../notebooks/07_aggregation_validation.ipynb).
It starts with four synthetic tickets and does not require a retained database.
The examples in this chapter use `mongosh` JavaScript notation. In the Python
notebook, operator names and field names are quoted dictionary keys, and the
collection variable replaces `db.tickets`. A stage shown by itself is a fragment
to place inside an aggregation array, not a complete command.

### A Fresh Four-Ticket Case

For the shell examples, start a new disposable database with the complete fixture
below. This is a simplified teaching case, not the full twelve-ticket relational
dataset. Its categories and priorities match the notebook's summary exercise;
its event objects additionally include identifiers and dates for the later
validation example. It is independent of Chapter 10's practice database.

```javascript
const pipelinePracticeName = "cst4714_pipeline_" + ObjectId().toHexString().slice(-8);
db = db.getSiblingDB(pipelinePracticeName);
db.tickets.createIndex({ ticket_id: 1 }, { unique: true });
db.tickets.insertMany([
  {
    ticket_id: 1001, category: "streetlight", priority: "urgent", status: "open",
    subject: "Dark streetlight", assignee_id: 201,
    opened_at: ISODate("2026-02-01T00:00:00Z"),
    events: [
      { event_id: 5001, type: "created", at: ISODate("2026-02-01T00:00:00Z") },
      { event_id: 5002, type: "assigned", at: ISODate("2026-02-01T01:00:00Z") }
    ]
  },
  {
    ticket_id: 1002, category: "sanitation", priority: "high", status: "in_progress",
    subject: "Missed pickup", assignee_id: 202,
    opened_at: ISODate("2026-02-02T00:00:00Z"),
    events: [{ event_id: 5003, type: "created", at: ISODate("2026-02-02T00:00:00Z") }]
  },
  {
    ticket_id: 1003, category: "streetlight", priority: "urgent", status: "resolved",
    subject: "Lamp repaired", assignee_id: 201,
    opened_at: ISODate("2026-02-03T00:00:00Z"),
    events: [
      { event_id: 5005, type: "created", at: ISODate("2026-02-03T00:00:00Z") },
      { event_id: 5007, type: "resolved", at: ISODate("2026-02-03T02:00:00Z") }
    ]
  },
  {
    ticket_id: 1004, category: "streetlight", priority: "low", status: "new",
    subject: "Unassigned report", assignee_id: null,
    opened_at: ISODate("2026-02-04T00:00:00Z"), events: []
  }
]);
```

There are four tickets, but only three are active. The resolved urgent ticket
is deliberately present so a query that counts every urgent ticket gives the
wrong active-workload answer. The empty event array makes another boundary case
visible without requiring a large dataset.

An aggregation pipeline passes documents through stages. Each stage receives the
previous stage's output.

```javascript
db.tickets.aggregate([
  { $match: { status: { $in: ["new", "open", "in_progress"] } } },
  {
    $group: {
      _id: "$category",
      active_count: { $sum: 1 },
      newest_opened_at: { $max: "$opened_at" }
    }
  },
  { $sort: { active_count: -1, _id: 1 } }
])
```

Trace the grain:

1. input: one document per ticket;
2. after `$match`: zero or one output per input ticket, still one per active
   ticket;
3. after `$group`: one document per category; and
4. after `$sort`: same documents, new order.

This is the document equivalent of reasoning about relational operations and SQL
logical order.

The expected groups are streetlight with two active tickets and newest opening
February 4, and sanitation with one and newest opening February 2. Ticket 1003
does not contribute because it was filtered out before grouping. The resolved
ticket remains stored in the collection: this pipeline reads data and does not
delete the filtered document. Pipelines can write through explicit stages such
as `$merge` or `$out`, but neither appears here.

The two uses of a dollar sign are worth separating. `$group` names an operator.
`"$category"` is an expression that reads the current document's category field.
Writing `"category"` instead would group every input under the same literal word.
In `$sum: 1`, the number is a contribution from each input document, so the
accumulator counts group members. In `$max: "$opened_at"`, each input contributes
its opening date and the accumulator keeps the largest.

## Put Selective Work Early When It Preserves Meaning

`$match` filters documents. When it appears early and matches an indexable query,
MongoDB may reduce work before later stages.

`$project` selects or computes fields:

```javascript
{
  $project: {
    _id: 0,
    ticket_id: 1,
    category: 1,
    event_count: { $size: { $ifNull: ["$events", []] } }
  }
}
```

Do not project fields away before a later stage needs them. Pipeline order is
meaning, not only optimization.

`$ifNull` supplies an empty array when `events` is missing or null. It does not
turn an arbitrary string into an array. The `$size` expression still needs an
array, which is why the fixture's shape and later validation matter. A defensive
expression must match a stated input contract rather than silently redefine bad
data.

## `$unwind` Changes One Document Into Many

```javascript
db.tickets.aggregate([
  { $match: { ticket_id: 1003 } },
  { $unwind: "$events" },
  {
    $project: {
      _id: 0,
      ticket_id: 1,
      event_type: "$events.type",
      event_at: "$events.at"
    }
  },
  { $sort: { event_at: 1 } }
])
```

After unwind, the grain is one document per array element. Ticket 1003 in this
chapter has two events, so this pipeline returns two rows ordered by their dates.
A ticket with three events would produce three. This is like joining a
one-to-many event table: multiplication may be correct.

Use `preserveNullAndEmptyArrays` when the question should keep documents with no
array elements.

### A Correct Total Can Hide an Incorrect Count

Consider the separate four-ticket fixture in the Week 11 notebook. Its active
tickets are 1001, 1002, and 1004. Their event-array lengths are 2, 1, and 0.

| Stream | Ticket IDs represented | Meaning of one document |
|---|---|---|
| after the active filter | 1001, 1002, 1004 | one active ticket |
| after ordinary unwind | 1001, 1001, 1002 | one event inside an active ticket |

Both streams contain three documents:

$$
N_{\text{tickets}} = 3,\qquad
N_{\text{events}} = 2 + 1 + 0 = 3.
$$

Yet ticket 1004 vanished and ticket 1001 contributes twice. Checking only the
grand total misses both mistakes. For a ticket report, aggregate before unwinding
or explicitly recover distinct ticket identity. For an event report, keep the
unwind and label the result as events. Preserving an empty array keeps ticket
1004 in the stream but still does not remove the duplicate contribution of 1001.

## `$group` Creates One Document Per Group Key

```javascript
{
  $group: {
    _id: "$events.type",
    event_count: { $sum: 1 },
    latest_event_at: { $max: "$events.at" },
    ticket_ids: { $addToSet: "$ticket_id" }
  }
}
```

`_id` is the group key in this stage. `$sum`, `$avg`, `$min`, `$max`, `$push`, and
`$addToSet` are common accumulators. `$group` does not guarantee output order; add
`$sort` when order matters.

Grouping is a blocking operation: it may need to receive all relevant inputs
before returning a group result. Filter unnecessary documents early.

Here `ticket_ids` is a set of distinct identifiers, while `event_count` counts
the incoming event records. One ticket can contribute several events but only
one member of that set. `$push` would instead retain repeated identifiers. Sets
do not establish a presentation order; explicitly sort any output where order
has meaning.

## Worked Example: Active Workload by Agent

```javascript
db.tickets.aggregate([
  {
    $match: {
      status: { $in: ["new", "open", "in_progress"] },
      assignee_id: { $exists: true, $ne: null }
    }
  },
  {
    $group: {
      _id: "$assignee_id",
      active_count: { $sum: 1 },
      urgent_count: {
        $sum: { $cond: [{ $eq: ["$priority", "urgent"] }, 1, 0] }
      }
    }
  },
  { $sort: { active_count: -1, _id: 1 } }
])
```

Verification: choose one agent ID and run a simple `find` with the same active
predicate. Count and inspect those tickets. The simpler query verifies one group
through a different path.

For the chapter fixture, agent 201 has one active ticket and one urgent active
ticket; agent 202 has one active ticket and no urgent active ticket. The `$cond`
expression contributes 1 when the priority is urgent and 0 otherwise. Resolved
ticket 1003 and unassigned ticket 1004 are outside this report. An absent agent
is not represented as a zero row, just as Chapter 2's assigned-only SQL grouping
did not produce all staff. Producing a complete staff roster would require that
roster as part of the query's starting population.

## Flexible Documents Benefit From Focused Validation

MongoDB schema validation can require types, allowed values, ranges, and selected
fields. It need not make every document identical.

The following is a stronger example than the notebook's initial three-field rule.
It assumes events carry `event_id`, `type`, and `at`, as in Chapter 10. Inspect or
migrate existing event objects before adopting it. Do not paste a stricter rule
onto unrelated data and assume the old documents now satisfy it. `required`
checks field presence; add property type rules when the event values themselves
must also have a particular type.

```javascript
db.runCommand({
  collMod: "tickets",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["ticket_id", "status", "priority", "subject", "opened_at"],
      properties: {
        ticket_id: { bsonType: ["int", "long"] },
        status: {
          enum: ["new", "open", "in_progress", "resolved", "closed"]
        },
        priority: {
          enum: ["low", "medium", "high", "urgent"]
        },
        subject: { bsonType: "string" },
        opened_at: { bsonType: "date" },
        events: {
          bsonType: "array",
          items: {
            bsonType: "object",
            required: ["event_id", "type", "at"]
          }
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

Existing documents must be audited before strict validation. A rule can be added
with different levels and actions for migration, but a warning-only policy is not
the same as rejection. Record the intended rollout.

Adding the rule does not scan and repair every existing document. `strict` and
`error` describe enforcement on relevant subsequent writes. A previously stored
invalid document may remain until it is identified and migrated. This differs
from assuming that successful configuration proves all historical data valid.

The supplied rule requires an event to *contain* `event_id`, `type`, and `at`, but
does not yet constrain their value types. The student's notebook task begins
with an even smaller rule and adds a required BSON opening date. A stronger
production rule can type-check event values too. Choose the invariant you need
and test both a valid and invalid write rather than declaring "schema validation
is on" as the result.

For example, after applying this chapter's rule, the following change should be
rejected with validation error code 121:

```javascript
db.tickets.updateOne(
  { ticket_id: 1004 },
  { $set: { opened_at: "2026-02-04T00:00:00Z" } }
)
```

The spelling looks like a date, but the proposed value is a string. Read ticket
1004 afterward and check that its BSON Date remains. In contrast, adding an
optional field such as `campus_zone: "west"` is permitted by this rule: focused
validation can protect core meaning while allowing intentional variation.

MongoDB uses BSON type names such as `date`, not JSON string conventions, in
validation.

## An Index Is an Ordered Access Path for a Workload

```javascript
db.tickets.createIndex({ status: 1, opened_at: -1 })
```

This compound index is ordered by status, then opening time within status. It may
support a query that filters one status and sorts newest first.

```javascript
db.tickets.find(
  { status: "open" },
  { ticket_id: 1, subject: 1, opened_at: 1 }
).sort({ opened_at: -1 }).limit(20)
```

Index order and query shape matter. An index adds storage and write work and can
complicate maintenance and backups. Avoid creating one index per field without a
workload.

MongoDB's `$sort` is not stable: equal sort-key values need not keep a repeatable
order. For deterministic pagination or a leaderboard, add a unique tie-breaker
such as `ticket_id` to both the sort and a compatible compound index.

## Explain Shows Plan and Execution Work

```javascript
db.tickets.find({ status: "open" })
  .sort({ opened_at: -1 })
  .limit(20)
  .explain("executionStats")
```

Important beginner measurements include:

- `nReturned`: documents returned;
- `totalDocsExamined`: documents inspected;
- `totalKeysExamined`: index keys inspected;
- `executionTimeMillis`: observed server execution time for this run; and
- winning-plan stages such as `COLLSCAN`, `IXSCAN`, `FETCH`, and `SORT`.

Explain output can differ by MongoDB version and query engine. Focus on documented
meaning rather than memorizing one nested path.

A collection scan is reasonable for a tiny collection or a query needing most
documents. An index scan is useful only when it reduces or orders relevant work.

Read the counts together. A hypothetical plan returning 20 documents after
examining 10,000 is doing a different amount of work from one returning the same
20 after examining 20 documents and 20 index keys. The ratio of documents examined
to documents returned is 500 in the first case and 1 in the second. That ratio
is undefined for zero returned documents and is not a complete cost model: an
index-only result, a complex sort, and repeated cached runs need context too.
Check record identity before comparing speed.

On this chapter's four-document fixture, the open-only query returns one ticket,
not twenty. The limit is a maximum, and a scan can be a reasonable choice. Use
the assigned MongoDB University performance activity for a larger prepared
workload rather than concluding that the small local fixture demonstrates
production index performance.

## Aggregations Can Use Indexes at the Beginning

An early `$match` and compatible `$sort` may use an index before stages reshape
documents. `$unwind` and `$group` can prevent later stages from using a source
collection index in the same way.

For example, an index on `category` does not precompute `active_count` for every
possible filter. Sorting grouped results by that newly computed count still
concerns the grouped stream. Likewise, moving `$limit: 20` before a workload
group would count only twenty input tickets, not compute the complete workload
and then choose the twenty largest groups. A cheaper computation is useful only
when it answers the same question.

```javascript
db.tickets.explain("executionStats").aggregate([
  { $match: { status: "open" } },
  { $sort: { opened_at: -1 } },
  { $limit: 20 },
  { $project: { ticket_id: 1, subject: 1, opened_at: 1 } }
])
```

Compare plans before and after the candidate index while keeping the pipeline
identical.

Atlas Free does not allow aggregation disk spill and currently limits in-memory
sort work to 32 MB. Keep course fixtures bounded, filter early, and use a
compatible index when ordering matters. A fast result on a tiny teaching
collection describes that run, not production capacity.

## Validation and Indexing Solve Different Problems

- Validation answers: may this document state exist?
- Indexing answers: how can the DBMS find or order matching documents?
- Aggregation answers: how should input documents become output documents?

One feature does not replace the others. A fast query can return inconsistent
data; valid data can still be expensive to scan.

## Common Misconceptions

### "A pipeline stage is a table"

Each stage produces a document stream. The shape and grain can change repeatedly.

### "Schema validation removes flexibility"

Focused rules preserve intentional variation while rejecting known invalid types
or values.

### "Docs examined should always be zero"

Some queries need document fields not covered by an index. The useful comparison
depends on returned results and workload.

### "Moving `$match` first is always correct"

Only move a predicate before a transformation when it has the same meaning on the
earlier document shape.

## Study, Cleanup, and Practice

Before Day 1, read the pipeline and validation sections. Before Day 2, read from
"An Index Is an Ordered Access Path for a Workload" through "Validation and
Indexing Solve Different Problems." The weekly labs assign the notebook change,
the specific external performance activity, and the video response. The
broader design exercise below is optional study practice.

If you ran the shell fixture, remove only its uniquely named practice database:

```javascript
db.getSiblingDB(pipelinePracticeName).dropDatabase()
```

Design a pipeline for one row-like output per category containing active ticket
count, urgent count, and newest opening time. Annotate the grain after every stage,
then propose one index for its first stages and one validation rule for its input.

## Retrieval and Transfer

1. Which pipeline stage commonly changes one document into many?
2. What does `_id` mean inside `$group`?
3. Why audit existing documents before strict validation?
4. How do `COLLSCAN` and `IXSCAN` differ?
5. Which three execution counts help evaluate selectivity?
6. Why should a performance comparison keep the pipeline identical?

## Further Reading

- [MongoDB aggregation stages](https://www.mongodb.com/docs/current/reference/operator/aggregation-pipeline/)
- [MongoDB `$group`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/)
- [MongoDB schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [MongoDB explain results](https://www.mongodb.com/docs/manual/reference/explain-results/)
- [MongoDB aggregation optimization](https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/)
