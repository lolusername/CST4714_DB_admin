# Module 10: MongoDB Models the Way an Application Reads

## Operating Question

How can we query documents safely and choose which related facts belong in one
document?

## Learning Outcomes

After this module, you can:

- distinguish an Atlas project, cluster, database, collection, and document;
- read common BSON values and Extended JSON representations;
- perform beginner `insert`, `find`, `update`, and `delete` operations;
- query nested fields and arrays with MQL operators;
- choose embedding or referencing from access patterns, growth, and ownership; and
- verify a write by inspecting matched, modified, and final document evidence.

## 1. Atlas and MongoDB Are Different Layers

- **MongoDB** is the document database system and query model.
- **Atlas** is MongoDB's managed cloud platform.
- An **Atlas project** organizes clusters, users, access, and services.
- A **cluster** is a deployed MongoDB service. Atlas Free uses a fixed three-node
  replica set with plan limitations.
- A **database** contains collections.
- A **collection** contains BSON documents.
- A **document** is a field/value structure with an `_id` identifier.

To connect, a learner normally creates a database user, configures temporary
network access, and selects a connection method. Atlas account identity, database
user identity, and application identity are separate.

## 2. BSON Extends JSON's Types

MongoDB stores BSON, a binary document format. BSON supports nested documents and
arrays plus types such as ObjectId and Date.

```javascript
{
  _id: ObjectId("65c2f56f1d4a9d7d3c101001"),
  ticket_id: 1001,
  opened_at: ISODate("2026-02-01T23:10:00Z")
}
```

This is `mongosh` representation, not strict JSON. Extended JSON supplies text
forms for BSON types when data crosses JSON-only tools. Preserve types during
import, export, and application conversion.

## 3. Create Documents Intentionally

```javascript
use cst4714_metro_support

db.tickets.insertOne({
  ticket_id: 1001,
  category: "streetlight",
  priority: "high",
  status: "open",
  subject: "Streetlight dark near bus stop",
  requester: {
    user_id: 101,
    display_name: "Maya Chen"
  },
  assignee_id: 201,
  opened_at: ISODate("2026-02-01T23:10:00Z"),
  tags: ["lighting", "safety"]
})
```

`insertOne` returns an acknowledgment and inserted identifier. That is write
evidence, but verify by reading the identifier and important fields.

Use a unique course database name. Do not practice destructive commands in the
sample databases supplied by Atlas or in another student's collection.

## 4. Read With Filters and Projections

```javascript
db.tickets.find(
  { status: { $in: ["new", "open", "in_progress"] } },
  { _id: 0, ticket_id: 1, priority: 1, status: 1, subject: 1 }
).sort({ opened_at: -1 })
```

The first document is the filter. The second is the projection. A projection that
includes selected fields normally uses `1`; `_id` is included by default unless
explicitly excluded.

Common comparison and logical operators include:

- `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`;
- `$in`, `$nin`;
- `$and`, `$or`, `$not`; and
- `$exists`.

```javascript
db.tickets.find({
  priority: { $in: ["high", "urgent"] },
  closed_at: { $exists: false }
})
```

Missing and `null` are distinct modeling states, though some query forms can match
both. State which one the workload means.

## 5. Query Nested Fields and Arrays

Dot notation reaches nested fields:

```javascript
db.tickets.find({ "requester.user_id": 101 })
```

An equality condition on an array field matches when the array contains the value:

```javascript
db.tickets.find({ tags: "safety" })
```

For multiple conditions that must match the same embedded array element, use
`$elemMatch`:

```javascript
db.tickets.find({
  events: {
    $elemMatch: {
      type: "status_changed",
      "actor.role": "agent"
    }
  }
})
```

Without `$elemMatch`, separate predicates can be satisfied by different elements,
which may answer a different question.

## 6. Update With Operators, Not Accidental Replacement

```javascript
db.tickets.updateOne(
  { ticket_id: 1001, status: "open" },
  {
    $set: { status: "in_progress", assignee_id: 202 },
    $push: {
      events: {
        event_id: 5099,
        type: "status_changed",
        at: new Date(),
        actor_id: 202
      }
    }
  }
)
```

The filter is part of write safety. Including the expected current status can
prevent changing a document that has already moved to another state.

Inspect `matchedCount` and `modifiedCount` in driver results, then read the final
document. A matched document can remain unmodified when the new value equals the
old value.

`replaceOne` replaces the document except for immutable `_id`; update operators
modify selected fields. Do not omit `$set` accidentally when the intent is a
partial change.

## 7. Delete With the Same Predicate Discipline

Preview first:

```javascript
db.tickets.find({ ticket_id: 1099, test_record: true })
```

Then delete the exact disposable record:

```javascript
db.tickets.deleteOne({ ticket_id: 1099, test_record: true })
```

Verify `deletedCount` and a final `find`. Avoid an empty filter such as `{}` unless
the documented intent is to affect every document in an isolated collection.

## 8. Single-Document Atomicity Shapes Modeling

MongoDB write operations are atomic at the single-document level. Embedding facts
that must change together can make an invariant easier to maintain. Multi-document
transactions exist, but they add coordination and should not substitute for a
workload-aware model.

Atomicity is not the only criterion. A document also needs bounded growth,
reasonable duplication, useful access paths, and a clear owner.

## 9. Embed When the Data Belongs and Travels Together

Embedding is often appropriate when related data:

- is read with the parent most of the time;
- is updated atomically with the parent;
- has a clear ownership relationship;
- is not independently shared across many parents; and
- remains bounded within the document.

An address snapshot on an order or a small set of ticket classification fields can
fit this pattern.

## 10. Reference When Identity or Growth Is Independent

Referencing is often appropriate when related data:

- has its own lifecycle and queries;
- is shared by many parents;
- grows without a practical bound;
- changes frequently and should have one source of truth; or
- participates in many-to-many relationships.

Long-lived ticket events may be a separate collection because history grows and
cross-ticket event reports are important. A ticket can store `requester_id` and a
historical requester-name snapshot only if the authoritative versus snapshot
semantics are explicit.

## Worked Example: Decide the Event Boundary

Access patterns:

1. retrieve a ticket summary by ID;
2. display the five latest events;
3. append events frequently;
4. retain years of history; and
5. aggregate event types across all tickets.

Options:

- **Embed all events:** direct ticket read and single-document append, but unbounded
  growth and cross-ticket analysis become concerns.
- **Reference all events:** bounded ticket and efficient event-wide queries, but
  the ticket page needs another query or aggregation.
- **Hybrid:** authoritative events remain separate; ticket embeds a bounded recent
  summary. Reads improve, but synchronization logic and duplicate semantics must
  be documented.

A beginner project should choose the simplest option that supports the stated
workload. Hybrid duplication is not automatically advanced or better.

## 11. More Than One Model Can Be Valid

Data modeling is a testable hypothesis. Document:

- most important reads;
- atomic writes;
- expected array or document growth;
- duplicated facts and their owner;
- required indexes;
- integrity rules; and
- one operation the design makes harder.

Then create representative documents and query them. A diagram without a workload
is not enough.

## Common Misconceptions

### "MongoDB stores JSON exactly"

MongoDB stores BSON. Tools render BSON values using `mongosh` or Extended JSON
forms.

### "Embedding is denormalization, so it is always faster"

It can reduce reads but increase size, duplication, update cost, and growth risk.
Measure the actual workload.

### "One collection should contain every kind of document"

Flexibility permits variation; it does not remove the need for cohesive ownership,
indexes, validation, and predictable queries.

### "`modifiedCount: 0` means the filter failed"

The document may have matched but already contained the requested value. Inspect
both matched and modified evidence.

## Practice

For a tutoring scheduler, compare embedded and referenced appointment notes. State
the read pattern, write pattern, ownership, growth, duplication, and one query for
each design.

## Retrieval and Transfer

1. How do an Atlas project and a MongoDB database differ?
2. Why is an ObjectId not a native JSON type?
3. When does `$elemMatch` matter?
4. Why should an update filter include the expected current state?
5. Which five conditions support embedding?
6. What evidence would make a referenced events collection preferable?

## Further Reading

- MongoDB CRUD operations: <https://www.mongodb.com/docs/manual/crud/>
- MongoDB query documents: <https://www.mongodb.com/docs/manual/tutorial/query-documents/>
- MongoDB data modeling: <https://www.mongodb.com/docs/manual/data-modeling/>
- MongoDB embedding and references:
  <https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/>
- MongoDB University, free data-modeling course:
  <https://learn.mongodb.com/learn/course/introduction-to-mongodb-data-modeling>
