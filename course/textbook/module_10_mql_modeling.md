# MongoDB Models the Way an Application Reads

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
- verify a write by inspecting matched and modified counts plus the final document.

## Atlas and MongoDB Are Different Layers

The JSON designs from Chapter 9 were text representations. This chapter puts
documents in a database and asks observable questions: which document matched,
which field changed, and whether the stored shape supports the application.
MQL, MongoDB Query Language, is the family of document-shaped query and update
expressions used by MongoDB. The shell and the Python driver express those
operations with slightly different host-language syntax.

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

The hierarchy is useful when troubleshooting. An Atlas project can exist with
no deployed database service. A working deployment can contain a database with
no application collections yet. Selecting a database name in a shell does not
necessarily create persistent data; writing data or explicitly creating a
collection does. Finally, an Atlas website login does not supply the database
password used by a Python connection.

![Figure 10.1: Atlas Data Explorer can see a free deployment yet still ask the user to connect. Deployment state, database credentials, and network access are separate prerequisites. Organization, project, and deployment names are redacted. Interface captured August 25, 2026.](figures/cloud_interfaces/atlas_data_explorer.png){#fig-atlas-data-explorer width=94%}

In this captured interface, the deployment appears in the left tree while the
workspace requests a connection. That screen alone does not identify the cause.
Check deployment readiness and the selected connection path before interpreting
an empty workspace as missing application data. For Python, also check the
database user, network access list, DNS/TLS path, and requested database name.

### Connect From the Machine That Runs the Code

A Colab notebook runs Python on a remote runtime, not on your laptop. Atlas sees
that runtime's outgoing public IP address. Adding your laptop's IP does not
necessarily allow Colab to connect. The
[Week 10 notebook](../notebooks/04_atlas_mql_modeling.ipynb) shows the runtime IP,
uses a temporary narrow access-list entry, prompts for the connection URI with
`getpass`, and sends a `ping` before attempting the lesson's data operations.

The `mongodb+srv://` connection scheme uses DNS service records to discover
servers; it is not an HTTP URL to open as a web page. Use the connection string
generated for the actual deployment and URL-encode reserved characters in a
password embedded in that string. Do not print the URI to diagnose it. A TLS
handshake error has more than one possible cause; disabling certificate checks
does not establish that the intended server is reachable and correctly trusted.

When the class exercise ends, remove its temporary access-list entry and close
the connection. The notebook has a local document-query alternative for students
without a working cloud route. That alternative teaches the stated CRUD and
array behavior, not Atlas networking or production durability.

## BSON Extends JSON's Types

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

The string `"2026-02-01T23:10:00Z"` and a BSON Date are different stored types.
They may look alike in a display while behaving differently in date operations
or validation. BSON Date represents an instant with millisecond resolution; keep
an original time-zone name separately if it has business meaning. `_id` is the
document identifier. Our `ticket_id` is a domain identifier retained from the
course case, so we explicitly protect it from duplication too.

Shell notation such as `ISODate(...)` creates a typed value. It is not legal
inside a strict JSON file. Python instead uses a `datetime` value through its
driver. Read the label on each listing before choosing where to run it.

## Create Documents Intentionally

The chapter's runnable listings use **mongosh**, MongoDB's JavaScript shell, on
a personal practice deployment. The assigned notebook teaches the same concepts
in Python, with its own fresh fixture. Do not mix shell commands into Python
cells. This opening block selects a newly named disposable database, creates a
unique domain-key index, and inserts one complete teaching document.

```javascript
const practiceName = "cst4714_book_" + ObjectId().toHexString().slice(-8);
db = db.getSiblingDB(practiceName);
db.tickets.createIndex({ ticket_id: 1 }, { unique: true });

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
  tags: ["lighting", "safety"],
  events: [
    {
      event_id: 5001, type: "created", actor_role: "resident",
      at: ISODate("2026-02-01T23:10:00Z")
    },
    {
      event_id: 5002, type: "assigned", actor_role: "agent",
      at: ISODate("2026-02-02T14:05:00Z")
    }
  ]
})
```

`insertOne` returns an acknowledgment and inserted identifier. That is one write
result, but verify by reading the identifier and important fields.

The unique `ticket_id` index means rerunning only the insertion rejects a second
ticket 1001. Without it, two documents could have different generated `_id`
values but the same course ticket number. Rerunning the entire opening block
creates another practice database; clean up the previous one rather than leaving
unused databases behind. Continue the remaining listings in this same shell and
practice database.

This teaching document adapts the CSV case rather than importing its columns
automatically. The embedded event field `type` corresponds to CSV `event_type`,
and `at` corresponds to `event_at`. `actor_role` is an added teaching field that
makes the array counterexample visible. A field does not acquire a new name or
type merely because it moves from a table to a document: an application or import
step must make that transformation deliberately.

Use a unique course database name. Do not practice destructive commands in the
sample databases supplied by Atlas or in another student's collection.

## Read With Filters and Projections

```javascript
db.tickets.find(
  { status: { $in: ["new", "open", "in_progress"] } },
  { _id: 0, ticket_id: 1, priority: 1, status: 1, subject: 1 }
).sort({ opened_at: -1 })
```

The first document is the filter. The second is the projection. A projection that
includes selected fields normally uses `1`; `_id` is included by default unless
explicitly excluded.

Read the query in words: keep tickets whose status belongs to the active set;
return only the listed fields; order the results by opening time, newest first.
`-1` requests descending order and `1` ascending order. Projection and sorting
do not change stored documents. You can sort using `opened_at` even though this
find projection does not display that field. With an inclusion projection,
do not mix arbitrary field exclusions; `_id: 0` is the usual permitted exception.

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

In the inserted example `closed_at` is absent. The filter
`{ closed_at: { $exists: false } }` finds absent fields. `{ closed_at: null }`
matches both absent fields and explicit null values, while
`{ closed_at: { $type: 10 } }` selects an explicit BSON null. That difference
matters when "not included in this document" is distinct from "known not to have
closed." MQL is not simply SQL with different punctuation; compare the actual
operator semantics.

For basic comparisons, `$gt` means greater than, `$gte` greater than or equal,
`$lt` less than, and `$lte` less than or equal. For example,
`{ ticket_id: { $gte: 1000 } }` asks for IDs at least 1000. `$in` asks whether a
value is among the supplied alternatives. Several top-level field conditions
must all hold unless an explicit logical operator combines them differently.

## Query Nested Fields and Arrays

Dot notation reaches nested fields:

```javascript
db.tickets.find({ "requester.user_id": 101 })
```

A scalar equality condition on an array field matches when the array contains
that value:

```javascript
db.tickets.find({ tags: "safety" })
```

Suppose the question is "did an agent create this ticket?" The example contains
a resident-created event and an agent-assigned event. This tempting query matches
the ticket even though no single event says an agent created it:

```javascript
db.tickets.find({
  "events.type": "created",
  "events.actor_role": "agent"
})
```

For multiple conditions that must match the same embedded array element, use
`$elemMatch`:

```javascript
db.tickets.find({
  events: {
    $elemMatch: {
      type: "created",
      actor_role: "agent"
    }
  }
})
```

Without `$elemMatch`, separate predicates can be satisfied by different elements,
which may answer a different question.

Here `$elemMatch` is part of the **filter**. It decides which ticket documents
qualify; it does not trim the returned `events` array to the matching element.
For example, filtering for an agent-assigned event returns ticket 1001 with both
of its stored events unless a separate projection changes the output. MongoDB
also has an `$elemMatch` projection operator, whose different role should not be
confused with the query predicate used here.

Before the later update, the first query returns ticket 1001 and the second
returns no document. The empty result is correct. This counterexample is more
informative than two queries that happen to agree on a fixture with only one
event. The Week 10 notebook supplies a similar contrast on its own small data.

## Update With Operators, Not Accidental Replacement

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
        actor_id: 202,
        actor_role: "agent"
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

For the first run here, expect one match and one modification. Rerunning this
same update finds no match because ticket 1001 is no longer `open`. That is the
expected-state condition doing useful work, not a connection failure. It also
prevents this particular repeated operation from appending event 5099 again.
This is a bounded example, not a complete retry design for arbitrary failures.

In mongosh the result fields use names such as `matchedCount`; PyMongo uses
`matched_count` and `modified_count`. The meanings are related, but the property
spelling belongs to the language's driver. Always read the final document when
checking the intended state.

`replaceOne` replaces the document's other contents while preserving the immutable
identifier. Omitted fields can disappear. `updateOne` with update operators
changes selected fields; a plain replacement object is not silently accepted as
an operator update. Choose the operation intentionally rather than assuming
replacement means "merge these fields."

## Delete With the Same Predicate Discipline

Create a clearly marked disposable record first. Without this insertion, the
later deletion correctly affects zero documents.

```javascript
db.tickets.insertOne({
  ticket_id: 1099, status: "new", subject: "Deletion practice",
  test_record: true
})
```

Preview the exact predicate:

```javascript
db.tickets.find({ ticket_id: 1099, test_record: true })
```

Then delete the exact disposable record:

```javascript
db.tickets.deleteOne({ ticket_id: 1099, test_record: true })
```

Verify `deletedCount` is one and the final `find` is empty. Repeating the delete
returns zero because the record is already absent. An empty filter `{}` matches
every document: `deleteOne({})` can remove an arbitrary matching document, while
`deleteMany({})` removes all matches. Neither is a substitute for identifying the
record you intended to delete.

## Single-Document Atomicity Shapes Modeling

MongoDB write operations are atomic at the single-document level. Embedding facts
that must change together can make an invariant easier to maintain. Multi-document
transactions exist, but they add coordination and should not substitute for a
workload-aware model.

Atomicity is not the only criterion. A document also needs bounded growth,
reasonable duplication, useful access paths, and a clear owner.

The update above changed current state and appended its embedded event in one
document operation. Another reader does not see only half that write. If events
live in a separate collection, the same application operation crosses a document
boundary and needs a considered coordination strategy. Conversely, putting every
event from every year in one ticket is not justified merely by the convenience
of atomicity. The model must account for growth and competing updates too.

## Embed When the Data Belongs and Travels Together

Embedding is often appropriate when related data:

- is read with the parent most of the time;
- is updated atomically with the parent;
- has a clear ownership relationship;
- is not independently shared across many parents; and
- remains bounded within the document.

An address snapshot on an order or a small set of ticket classification fields can
fit this pattern.

Distinguish **ownership** from mere association. A ticket's small set of
classification answers may be owned by that ticket. A resident's current account
profile belongs to the resident and is shared by many tickets. Copying that
profile everywhere makes each future correction a multi-document update problem.
An explicitly named historical snapshot is different: it intentionally records
what was known at one time and need not change with the current profile.

## Reference When Identity or Growth Is Independent

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

A reference is not an automatically enforced foreign key. Storing
`requester_id: 101` does not by itself require that user 101 exists in another
collection. The application must coordinate reference creation, deletion, and
validation where the relationship matters. This is a direct comparison with
Chapter 3, not an argument that either model is always superior.

## Worked Example: Decide the Event Boundary

Access patterns:

1. retrieve a ticket summary by ID;
2. display the latest two events, newest first;
3. append events frequently;
4. retain years of history; and
5. aggregate event types across all tickets.

Options:

- **Embed all events:** direct ticket read and single-document append, but unbounded
  growth and cross-ticket analysis become concerns.
- **Reference all events:** bounded ticket and independent event-wide queries, but
  the ticket page needs another query or aggregation.
- **Hybrid:** authoritative events remain separate; ticket embeds a bounded recent
  summary. Reads improve, but synchronization logic and duplicate semantics must
  be documented.

A beginner project should choose the simplest option that supports the stated
workload. Hybrid duplication is not automatically advanced or better.

### A Complete Referenced Page

The following `mongosh` examples continue in the disposable database selected
earlier. They create `page_tickets`, `people`, and `history` as a second model of
ticket 1001's initial state. They do not migrate or synchronize the earlier
`tickets` collection. Keeping the two examples separate lets us compare their
behavior without silently changing the first experiment.

Create one authoritative person and one ticket that refers to that person:

```javascript
db.people.createIndex({ user_id: 1 }, { unique: true });
db.page_tickets.createIndex({ ticket_id: 1 }, { unique: true });
db.people.insertOne({
  user_id: 101, display_name: "Maya Chen",
  email: "maya.chen@example.org"
});
db.page_tickets.insertOne({
  ticket_id: 1001, requester_id: 101, status: "open",
  subject: "Streetlight dark near bus stop"
});
```

The unique indexes protect each collection's domain identifier. They do not
enforce the reference between collections. The email is stored on the person,
so a ticket does not contain another supposed current copy to maintain.

Each history document carries its own ticket reference. These two timestamps
and event IDs match the initial CSV case:

```javascript
db.history.createIndex({ event_id: 1 }, { unique: true });
db.history.insertMany([
  {
    event_id: 5001, ticket_id: 1001, event_type: "created",
    event_at: ISODate("2026-02-01T23:10:00Z")
  },
  {
    event_id: 5002, ticket_id: 1001, event_type: "assigned",
    event_at: ISODate("2026-02-02T14:05:00Z")
  }
]);
```

This representation retains the CSV field names `event_type` and `event_at`,
unlike the shorter names in the embedded example. The parent ticket needs no
array containing every event ID. Moving complete events out while retaining an
ever-growing parent ID array would still leave a growing parent document.
Run each insertion block once in this fresh database. Repeating an insertion
rejects a duplicate domain key; it does not silently replace the earlier data.

Read the page in three operations. First, retrieve the ticket:

```javascript
db.page_tickets.findOne(
  { ticket_id: 1001 },
  { _id: 0, ticket_id: 1, requester_id: 1, status: 1, subject: 1 }
)
```

It returns ticket 1001 with `requester_id: 101` and `status: "open"`. The
application takes that requester ID and looks up the person's current details:

```javascript
db.people.findOne(
  { user_id: 101 },
  { _id: 0, display_name: 1, email: 1 }
)
```

Finally, retrieve only this ticket's latest two history records:

```javascript
db.history.find(
  { ticket_id: 1001 },
  { _id: 0, event_id: 1, event_type: 1, event_at: 1 }
).sort({ event_at: -1, event_id: -1 }).limit(2)
```

The returned IDs are 5002, then 5001. `event_at` sets the chronological order;
the unique `event_id` breaks equal-time ties deterministically. Here the IDs
happen to increase with time, but an identifier is not a substitute for the
event timestamp. `limit(2)` restricts this result, not the stored history.

The constants make the read path visible. A real page handler would use the ID
from its first result rather than hard-code 101. It would also handle a missing
ticket or person explicitly. Successful lookup in this fixture does not prove
that every possible reference in an application exists.

An index can support the history filter and ordering:

```javascript
db.history.createIndex({ ticket_id: 1, event_at: -1, event_id: -1 })
```

The first field groups index entries for a ticket. Within that group, the next
fields provide the requested newest-first order. This is a candidate access
path, not a speed measurement. Chapter 11 explains how to inspect the plan and
work counts. A two-event collection is too small to demonstrate production
performance, and the index has its own storage and update cost.

### A Contact Correction and a New Event

Change the person's email without rewriting ticket documents:

```javascript
db.people.updateOne(
  { user_id: 101 },
  { $set: { email: "maya.updated@example.org" } }
)
```

Expect one matched and one modified person. Rerun the person lookup to see the
new email, then rerun the ticket lookup: its reference remains 101 and it still
has no copied email field. Repeating the same correction reports one match and
zero modifications. A separate `requester_name_at_open` snapshot would have a
different purpose and would not automatically change with the current profile.

Now append a new synthetic follow-up event, created for this experiment rather
than copied from the original CSV:

```javascript
db.history.insertOne({
  event_id: 5998, ticket_id: 1001, event_type: "note_added",
  event_at: ISODate("2026-02-03T12:00:00Z")
})
```

Repeating the latest-two query now returns 5998 and 5002. Event 5001 remains in
the collection. Check the distinction between retained history and displayed
history directly:

```javascript
db.history.countDocuments({ ticket_id: 1001 })
```

The result is 3. No growing array or event-ID list was added to `page_tickets`.
If the application must coordinate an event with a ticket status change, however,
those separate documents introduce a different problem from this independent
note append. The three page reads also do not promise one atomic snapshot across
all collections. State the required consistency before choosing a transaction,
a retry/reconciliation design, or an acceptable delay between related changes.

### Growth and the Cost of a Convenient Preview

MongoDB limits a BSON document to 16 MiB, or 16,777,216 bytes. There is no universal
safe event count: event sizes, field names, and array overhead vary. An embedded
history can become inconvenient well before it reaches the hard size limit,
especially when a page needs only a small part of it. Fifty thousand events is
a useful design stress question, not a claim that every such document exceeds
the limit.

A hybrid model might keep all events in `history` and copy only two recent
summaries into the ticket. The copied preview needs a maintenance rule. An
out-of-order arrival should be compared by event time; an edited or deleted event
may require a refreshed preview. The application must decide whether a temporarily
stale preview is acceptable and how it recovers from an interrupted update.
For this beginner workload, the referenced read is easier to explain and verify.
A hybrid is worth considering only when its extra maintenance solves a measured
need.

These choices also occur in relational systems. PostgreSQL supports arrays and
JSON values, and SQL does not force every application into third normal form.
Normalization remains useful for reasoning about dependencies and update
anomalies; workload analysis remains useful for choosing reads and storage.
The important comparison is the consequence of a specific design, not a claim
that one product has flexible data while the other cannot.

## More Than One Model Can Be Valid

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
both matched and modified counts.

## Study, Cleanup, and Practice

Before Day 1, read the connection, BSON, CRUD, and array-query sections. Before
Day 2, read from "Single-Document Atomicity Shapes Modeling" through the event
boundary example. The assigned labs use the course notebook and the specified
MongoDB University units; the scenario below is optional self-study.

If you ran the shell examples, remove only the database created by their opening
block and then leave the shell. This does not delete your Atlas deployment.

```javascript
db.getSiblingDB(practiceName).dropDatabase()
```

For a tutoring scheduler, compare embedded and referenced appointment notes. State
the read pattern, write pattern, ownership, growth, duplication, and one query for
each design.

## Retrieval and Transfer

1. How do an Atlas project and a MongoDB database differ?
2. Why is an ObjectId not a native JSON type?
3. When does `$elemMatch` matter?
4. Why should an update filter include the expected current state?
5. Which five conditions support embedding?
6. Which workload or growth pattern would make a referenced events collection preferable?

## Further Reading

- [MongoDB CRUD operations](https://www.mongodb.com/docs/manual/crud/)
- [MongoDB query documents](https://www.mongodb.com/docs/manual/tutorial/query-documents/)
- [MongoDB data modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [MongoDB embedding and references](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)
- [MongoDB array-element matching](https://www.mongodb.com/docs/manual/reference/operator/query/elemMatch/)
- [MongoDB single-document atomicity](https://www.mongodb.com/docs/manual/core/write-operations-atomicity/)
- [MongoDB sort support from indexes](https://www.mongodb.com/docs/manual/tutorial/sort-results-with-indexes/)
- [MongoDB BSON document limits](https://www.mongodb.com/docs/manual/reference/limits/)
- [PostgreSQL arrays](https://www.postgresql.org/docs/current/arrays.html)
- [PostgreSQL JSON types and document design](https://www.postgresql.org/docs/current/datatype-json.html)
- [MongoDB University, free data-modeling course](https://learn.mongodb.com/learn/course/introduction-to-mongodb-data-modeling)
