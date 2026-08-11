# Module 9: Documents Emerged From Changing Workloads

## Operating Question

If you designed a data system today, which relational ideas would you keep, what
might you change, and which workload would justify that change?

## Learning Outcomes

After this module, you can:

- explain why NoSQL emerged without claiming that relational databases became
  obsolete;
- compare key-value, wide-column, document, graph, and vector abstractions;
- write and validate strict JSON objects and arrays;
- distinguish JSON text from MongoDB's BSON document representation;
- represent the same CSV relationships in more than one valid JSON shape; and
- evaluate flexibility in terms of reads, writes, duplication, growth, and
  integrity.

## 1. Relational Databases Solved a Real Historical Problem

In 1970, E. F. Codd proposed the relational model as a way to separate logical data
relationships from physical storage details. Relations, keys, declarative queries,
constraints, and transactions remain powerful because they let many workloads ask
new questions while preserving shared meaning.

The later rise of NoSQL did not prove those ideas wrong. It reflected new pressures:

- globally distributed services;
- very high write or read throughput;
- data whose fields changed frequently;
- hierarchical objects moving through web applications;
- specialized traversals, sparse records, caches, and search; and
- engineering teams willing to trade generality for a workload-specific shape.

## 2. "NoSQL" Has More Than One Historical Meaning

Carlo Strozzi used the name NoSQL in 1998 for a relational DBMS that used Unix
tools rather than SQL. That system was still relational. Around 2009, the label
was reused for a meetup and a growing set of non-relational, often distributed
datastores. The later slogan "not only SQL" emphasizes coexistence, but it is not
a precise technical definition.

Important influences included:

- Google's 2006 Bigtable paper, which described a distributed structured store
  with a sparse, multidimensional data model; and
- Amazon's 2007 Dynamo paper, which described a highly available key-value system
  designed for an "always-on" service experience.

Products inspired by these systems made different choices. No single consistency,
schema, transaction, or query rule applies to every NoSQL database.

## 3. Choose an Abstraction for a Workload

### Key-Value Store

Model: a mapping from a unique key to a value.

```text
"session:8fd2" -> {"user_id": 101, "expires_at": "..."}
```

Strengths include direct lookup, caching, sessions, counters, and simple
partitioning. If the system cannot inspect fields inside the value efficiently,
questions that do not know the key become difficult. Redis is a widely used
example with richer value structures than a bare string map.

### Wide-Column Store

Model: rows located by a row key, with sparse or dynamic columns commonly grouped
into column families.

This abstraction suits large, distributed workloads organized around known access
keys and ranges, such as time-ordered events by device. Google Bigtable and
systems influenced by it demonstrate this family. It is not the same as an
analytical columnar file or warehouse merely because both use the word "column."

### Document Store

Model: self-describing, nested records addressed and queried by fields.

```json
{
  "ticket_id": 1001,
  "status": "open",
  "requester": {"user_id": 101, "name": "Maya Chen"},
  "tags": ["streetlight", "safety"]
}
```

Documents align naturally with objects and API payloads. Related facts read and
changed together can live together. The design must still address duplication,
unbounded arrays, shared ownership, validation, indexes, and access patterns.
MongoDB is the course's document database.

### Graph Database

A graph is commonly written `G = (V, E)`: a set of vertices and a set of edges.
Vertices represent entities; edges represent relationships. A property graph can
store attributes on both.

```text
(resident 101)-[REQUESTED]->(ticket 1001)-[ASSIGNED_TO]->(agent 201)
```

Basic graph ideas:

- **directed edge:** `A -> B` has a direction;
- **undirected edge:** connection has no direction for the model;
- **degree:** number of edges incident to a vertex;
- **path:** sequence of connected vertices and edges;
- **shortest path:** path minimizing edge count or a weight; and
- **connected component:** vertices reachable from one another under the chosen
  direction rules.

Graph databases are useful when the relationship path is the question: fraud
rings, dependency impact, network topology, recommendations, authorization paths,
or knowledge graphs. A graph is not automatically better for ordinary records
that are mostly retrieved by identifier.

### Vector Store or Vector Search

A vector represents an item as a point in a numeric space, often produced by a
machine-learning embedding model. Similar items should be near one another under a
chosen measure.

For vectors `a` and `b`, cosine similarity is:

```text
cosine_similarity(a, b) = (a dot b) / (||a|| * ||b||)
```

It measures the angle between nonzero vectors. Two vectors pointing in the same
direction have similarity near 1 even if one has larger magnitude. Euclidean
distance measures straight-line distance and is sensitive to magnitude. Cosine is
often useful when direction represents semantic pattern and vector length is not
the desired signal.

Exact nearest-neighbor search compares a query with every vector. Approximate
nearest-neighbor indexes trade some exactness for much faster search at scale.
Vector search may be a feature inside relational or document systems rather than
a completely separate database family. The operational questions remain: which
model produced the vector, how it is versioned, which distance measure matches the
meaning, how recall is evaluated, and how source records stay synchronized.

Product syntax is version-dependent. For example, MongoDB's
`$similarityCosine` aggregation expression is new in MongoDB 8.3, while the
verified Atlas Free baseline is MongoDB 8.0. The formula remains useful for
reasoning, but do not assume that operator exists: inspect the actual server
version and use a compatible vector-search feature or a small local calculation.

## 4. Specialized Models Trade Generality for Directness

| Workload question | Natural first model | Important tradeoff |
|---|---|---|
| fetch session by exact token | key-value | limited ad hoc field queries |
| write time-ordered device readings by device | wide-column | design tied to row key and access pattern |
| load a ticket with bounded nested details | document | duplication and document growth |
| find paths among accounts and devices | graph | relationship-oriented operations and new tooling |
| find semantically similar incident descriptions | vector search | approximate results and embedding lifecycle |
| enforce shared entities and flexible reporting | relational | joins and schema-change coordination |

Real systems can combine models. Each added store creates more access control,
monitoring, backup, synchronization, and expertise obligations. Polyglot design is
a cost-benefit decision, not a trophy.

## 5. JSON Became a Common Interchange Format

JavaScript Object Notation grew from JavaScript object-literal syntax and was
standardized as a minimal, textual, language-independent interchange format. The
current Internet standard is RFC 8259; ECMA-404 defines the syntax in parallel.
The registered media type is `application/json`.

JSON became popular because it is:

- compact enough for network exchange;
- readable and writable across many programming languages;
- natural for nested API data;
- easy to parse with standard libraries; and
- less verbose than XML for many application payloads.

Popularity does not make every JSON design good. A valid document can still have
ambiguous names, inconsistent types, duplicated facts, unsafe content, or no
versioning strategy.

## 6. JSON Has Six Value Kinds

A JSON value can be:

- object;
- array;
- string;
- number;
- `true` or `false`; or
- `null`.

Object names are strings. Objects are unordered collections of name/value pairs;
arrays are ordered sequences.

```json
{
  "ticket_id": 1001,
  "open": true,
  "closed_at": null,
  "priority": "high",
  "coordinates": [40.69, -73.99],
  "requester": {
    "user_id": 101,
    "display_name": "Maya Chen"
  }
}
```

Strict JSON requires double-quoted names and strings. It does not permit comments,
trailing commas, `undefined`, single-quoted strings, or native date values.

These are invalid:

```text
{'status': 'open'}                 # single quotes
{"status": "open",}             # trailing comma
{"opened_at": 2026-02-01T10:00Z} # unquoted timestamp
```

An application commonly encodes a date as an agreed string. MongoDB's BSON format
adds types such as date and ObjectId that are not native JSON types. Atlas and
drivers may display Extended JSON when representing those types as text.

## 7. Flexibility Means Multiple Shapes Are Possible

Three CSV tables can become many valid JSON designs.

### Referenced Collections

```json
{
  "ticket_id": 1001,
  "requester_id": 101,
  "assignee_id": 201,
  "status": "open"
}
```

Events can remain separate documents containing `ticket_id`. Shared users have one
source of truth, but reading a full ticket history requires additional queries or
a join-like operation.

### Embedded Ticket

```json
{
  "ticket_id": 1001,
  "status": "open",
  "requester": {
    "user_id": 101,
    "display_name": "Maya Chen"
  },
  "events": [
    {
      "event_id": 5001,
      "type": "created",
      "at": "2026-02-01T23:10:00Z"
    }
  ]
}
```

One read can return the ticket and history. The document duplicates requester
display data and can grow without bound if events continue forever.

### Snapshot Plus Reference

```json
{
  "ticket_id": 1001,
  "requester_id": 101,
  "requester_name_at_open": "Maya Chen",
  "recent_events": [
    {"event_id": 5002, "type": "assigned"}
  ]
}
```

This design intentionally keeps a historical snapshot and a reference. It needs a
rule explaining which field is authoritative and how recent events are bounded.

The right question is not "Which JSON is correct?" It is "Which shape makes the
important reads and atomic changes direct while keeping duplication, growth, and
integrity manageable?"

## 8. Flexible Schema Is Still a Schema

Even if the database accepts different fields, applications assume names, types,
and structures. That assumed contract is a schema. If one document stores
`priority: "high"` and another stores `priority: 3`, every query and client must
handle both or fail.

Flexibility helps when variation is intentional and understood. It is harmful when
variation is accidental. MongoDB supports schema validation for established
invariants, which Module 11 applies.

## Worked Example: Compare Two Ticket Shapes

**Access patterns:**

1. show a ticket with its five most recent events;
2. append one event when status changes;
3. report event counts across all tickets by event type; and
4. preserve history for years.

Embedding every event makes the first two operations direct and single-document
atomic. Unbounded growth and the cross-ticket report become concerns. Keeping all
events separate supports long history and cross-ticket aggregation but requires a
second query for the ticket page.

A plausible beginner design references a separate authoritative events collection
and optionally embeds a small, explicitly bounded recent-event summary. The
important part is documenting the boundary, not maximizing nesting.

## Common Misconceptions

### "NoSQL means no schema"

The schema may be implicit, flexible, or validated selectively. Applications
still depend on structure.

### "JSON supports dates"

Strict JSON does not have a date type. A string convention or an extended storage
format supplies date semantics.

### "Embedding removes relationships"

It represents a relationship through containment. Ownership, duplication, and
growth still need decisions.

### "Vector similarity understands meaning"

Similarity reflects a model, data, metric, and index. It is an engineered estimate
that must be evaluated for the task.

## Practice

Using the three Metro Support CSV files, sketch two JSON designs:

1. a referenced design; and
2. an embedded or hybrid design.

For each, state one read it improves, one update it complicates, one duplicated or
growing field, and one rule that should be validated.

## Retrieval and Transfer

1. Why is the 1998 use of "NoSQL" different from the later movement?
2. Which data-model family makes paths a first-class question?
3. How do cosine similarity and Euclidean distance differ?
4. Which JSON value kinds exist?
5. Why is a valid JSON document not necessarily a good data model?
6. What workload evidence would support embedding ticket events?

## Further Reading

- RFC 8259, JSON: <https://www.rfc-editor.org/info/rfc8259/>
- Debian's preserved package record for Carlo Strozzi's NoSQL RDBMS:
  <https://sources.debian.org/src/nosql/3.1-4/nosql.lsm/>
- Google, *Bigtable* paper: <https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/>
- Amazon, *Dynamo* paper: <https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store>
- Martin Fowler and Pramod Sadalage, NoSQL key points:
  <https://martinfowler.com/articles/nosqlKeyPoints.html>
- MongoDB data modeling: <https://www.mongodb.com/docs/manual/data-modeling/>
- MongoDB `$similarityCosine` versioned reference:
  <https://www.mongodb.com/docs/manual/reference/operator/aggregation/similaritycosine/>
- MongoDB Vector Search: <https://www.mongodb.com/docs/vector-search/>
