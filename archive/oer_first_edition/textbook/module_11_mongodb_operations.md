# Module 11: MongoDB Operations Connect Pipelines, Rules, and Indexes

## Operating Question

How can a MongoDB workload transform documents, reject invalid states, and find
the intended records without examining everything?

## Learning Outcomes

After this module, you can:

- trace document grain through an aggregation pipeline;
- use `$match`, `$project`, `$unwind`, `$group`, `$sort`, and `$limit`;
- add focused schema validation with `$jsonSchema`;
- read basic `explain("executionStats")` evidence;
- connect a compound index to filter and sort order; and
- make a keep/remove/test-further recommendation with operational tradeoffs.

## 1. A Pipeline Is an Ordered Document Transformation

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

## 2. Put Selective Work Early When It Preserves Meaning

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

## 3. `$unwind` Changes One Document Into Many

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

After unwind, the grain is one document per array element. A ticket with three
events produces three pipeline documents. This is like joining a one-to-many event
table: multiplication may be correct.

Use `preserveNullAndEmptyArrays` when the question should keep documents with no
array elements.

## 4. `$group` Creates One Document Per Group Key

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

## 5. Flexible Documents Benefit From Focused Validation

MongoDB schema validation can require types, allowed values, ranges, and selected
fields. It need not make every document identical.

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

MongoDB uses BSON type names such as `date`, not JSON string conventions, in
validation.

## 6. An Index Is Ordered Evidence for a Workload

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

## 7. Explain Shows Plan and Execution Evidence

```javascript
db.tickets.find({ status: "open" })
  .sort({ opened_at: -1 })
  .explain("executionStats")
```

Important beginner evidence includes:

- `nReturned`: documents returned;
- `totalDocsExamined`: documents inspected;
- `totalKeysExamined`: index keys inspected;
- `executionTimeMillis`: observed server execution time for this run; and
- winning-plan stages such as `COLLSCAN`, `IXSCAN`, `FETCH`, and `SORT`.

Explain output can differ by MongoDB version and query engine. Focus on documented
meaning rather than memorizing one nested path.

A collection scan is reasonable for a tiny collection or a query needing most
documents. An index scan is useful only when it reduces or orders relevant work.

## 8. Aggregations Can Use Indexes at the Beginning

An early `$match` and compatible `$sort` may use an index before stages reshape
documents. `$unwind` and `$group` can prevent later stages from using a source
collection index in the same way.

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
collection is evidence about that run, not a production capacity claim.

## 9. Validation and Indexing Solve Different Problems

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

## Practice

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

- MongoDB aggregation stages:
  <https://www.mongodb.com/docs/current/reference/operator/aggregation-pipeline/>
- MongoDB `$group`: <https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/>
- MongoDB schema validation: <https://www.mongodb.com/docs/manual/core/schema-validation/>
- MongoDB explain results: <https://www.mongodb.com/docs/manual/reference/explain-results/>
- MongoDB aggregation optimization:
  <https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/>
