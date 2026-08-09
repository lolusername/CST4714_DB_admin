# Module 13: Scale Changes the Questions a System Must Answer

## Operating Question

When data or traffic grows, how do we decide whether to tune, scale up, partition,
or shard, and how can a small Python client expose the consequences?

## Learning Outcomes

After this module, you can:

- describe capacity using workload, storage, latency, throughput, and growth;
- distinguish vertical scaling, read replicas, partitioning, and sharding;
- explain the roles of shards, replica sets, config servers, and `mongos`;
- evaluate shard-key cardinality, frequency, monotonicity, and query targeting;
- compare ranged and hashed distribution; and
- connect to a cloud database from Python without saving credentials.

## 1. Capacity Planning Starts With a Workload

"Will this database scale?" has no answer without quantities and objectives.

Record:

- current and expected records or documents;
- average and high-percentile object size;
- read and write operations by query shape;
- peak versus average throughput;
- acceptable latency and error rate;
- working set versus available memory;
- index and backup growth;
- retention and deletion behavior; and
- expected growth horizon.

A beginner project should not fabricate enterprise traffic. It should state a
small current workload, one plausible growth scenario, and the first measurement
that would trigger a change.

## 2. Fix Waste Before Distributing It

Scaling options include:

- **query/model improvement:** reduce unnecessary work;
- **vertical scaling:** add CPU, memory, or faster storage to one node or tier;
- **caching:** avoid repeated work with an explicit freshness policy;
- **read replication:** serve selected reads from copies with consistency tradeoffs;
- **partitioning:** divide a logical dataset within one database system; and
- **sharding:** distribute parts of a collection or dataset across database nodes.

Horizontal distribution adds network failures, routing, rebalancing, cross-shard
operations, monitoring, and recovery complexity. Do not shard a bad query merely
to run the bad query on more machines.

## 3. MongoDB Sharding Distributes Collection Ranges

A sharded MongoDB cluster includes:

- **shards:** each shard stores part of the collection and is normally a replica
  set for availability;
- **config servers:** store cluster metadata and configuration;
- **`mongos`:** query routers that use metadata to target shards and merge results;
  and
- **chunks/ranges:** non-overlapping shard-key ranges assigned across shards.

The shard key is an indexed field or compound of fields that determines document
distribution. It becomes a long-lived architectural decision even though modern
MongoDB supports refinement and resharding.

Atlas Free cannot create a sharded cluster. Students analyze a candidate and
simulate distribution in open code rather than claiming to deploy the paid
architecture.

## 4. Four Shard-Key Questions

### Cardinality

How many distinct key values exist? A Boolean or five-value status field cannot
create many independently distributable ranges by itself.

### Frequency

How often does each value occur? A high-cardinality key can still be skewed if one
value dominates traffic or document count.

### Monotonicity

Does the key continually increase or decrease, such as a timestamp or sequential
identifier? Range sharding on a monotonic key can direct new writes toward the
chunk holding the current extreme, creating a hotspot.

### Query Targeting

Do common queries include the shard key? If a query does not provide enough shard-
key information, the router may broadcast it to multiple shards in a scatter-
gather operation.

An ideal candidate balances distribution and targeting. No single field property
guarantees both.

## 5. Ranged and Hashed Distribution Make Different Tradeoffs

### Ranged Sharding

Nearby shard-key values stay in nearby ranges. A query for a bounded range can be
targeted, but monotonic inserts or skew can concentrate load.

### Hashed Sharding

MongoDB hashes the shard-key value to distribute documents more evenly. This can
spread monotonic identifiers, but range queries on the original values lose
locality and may contact many shards.

Example:

- `{ neighborhood: 1, opened_at: 1 }` can support locality and targeted
  neighborhood-time queries but may skew if one neighborhood dominates.
- `{ ticket_id: "hashed" }` can distribute identifier writes but does not target a
  query that only filters neighborhood.

Choose from the actual query and write distribution.

## 6. Cross-Shard Operations Cost More Coordination

A request can be:

- **targeted:** routed to one shard or limited shard set using the shard key; or
- **scatter-gather:** sent broadly and merged by `mongos`.

Cross-shard aggregations, transactions, uniqueness, and resharding can add network
and coordination cost. A design can still use them; the cost should be visible.

## Worked Example: Evaluate Metro Support Candidates

Workload:

- writes arrive across neighborhoods;
- dashboards filter neighborhood and recent opening time;
- support staff retrieve exact ticket IDs; and
- one central neighborhood produces 45 percent of tickets.

| Candidate | Distribution | Targeting | Risk |
|---|---|---|---|
| `status` | very low cardinality | helps status query only | jumbo/hot values |
| `opened_at` ranged | high and monotonic | good time ranges | latest-write hotspot |
| `ticket_id` hashed | likely even writes | exact ID target | neighborhood/time reports scatter |
| `(neighborhood, ticket_id hashed component)` | spreads within neighborhood | neighborhood queries can target a subset depending on full key | more complex routing and index |

The table does not produce a universal winner. It identifies what data and query
measurements are needed before deployment.

## 7. Python Makes the Client Contract Visible

A driver connection includes network routing, TLS, authentication, server
selection, timeouts, and query behavior. Keep the first program small.

### MongoDB Atlas

```python
from getpass import getpass
from pymongo import MongoClient

mongodb_uri = getpass("Atlas connection URI: ")
client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
client.admin.command("ping")

tickets = client["cst4714_metro_support"]["tickets"]
for ticket in tickets.find({"status": "open"}, {"_id": 0, "ticket_id": 1}):
    print(ticket)
```

Do not add `tlsInsecure=True` as a routine fix. It disables certificate validation
and can hide the real issue. Check the URI, current driver, system time, network
access list, DNS, and supported TLS path.

### PostgreSQL/Supabase

```python
from getpass import getpass
import psycopg

database_url = getpass("PostgreSQL connection URL: ")
with psycopg.connect(database_url) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM metro_support.tickets")
        print(cursor.fetchone())
```

On a network without direct IPv6 connectivity, use the provider's current IPv4-
compatible pooler URI rather than changing database code randomly.

## 8. Import in Small, Verifiable Batches

Before loading a public dataset:

1. inspect license, source, retrieval date, columns, types, nulls, duplicates, and
   size;
2. select a small subset tied to a question;
3. convert dates and missing values intentionally;
4. write a batch;
5. check acknowledged or row-count evidence; and
6. query a known sample and total.

An import script should be rerunnable or explicitly idempotent. Stable natural
keys, upserts, a reset option in a disposable collection, or a recorded batch ID
can prevent accidental duplicates.

## 9. Scaling Also Scales Operations

More nodes or stores mean more:

- credentials and network rules;
- metrics and alerts;
- backup components and restore order;
- version compatibility;
- failure combinations;
- cost controls; and
- people who must understand the system.

A capacity recommendation should include the operating cost, not only throughput.

## Common Misconceptions

### "High cardinality makes a perfect shard key"

Frequency, monotonicity, query targeting, and update behavior also matter.

### "Hashed sharding makes every query faster"

It can improve distribution while turning range or non-key queries into broad
operations.

### "A free replica set lets us practice sharding"

Replication and sharding solve different problems. Atlas Free does not support a
sharded cluster.

### "If a script inserted rows, the import worked"

Verify counts, known identifiers, types, and a question-driven query. Handle
partial failure and reruns.

## Practice

Evaluate three shard-key candidates for an event dataset: timestamp, device ID,
and hashed event ID. For each, record cardinality, frequency, monotonicity, two
query patterns, and likely distribution. Recommend what to measure next rather
than inventing a final production answer.

## Retrieval and Transfer

1. How do vertical scaling and sharding differ?
2. What does `mongos` do?
3. Why can a monotonic ranged shard key create a hotspot?
4. What is a scatter-gather query?
5. What tradeoff does hashed distribution make?
6. Which two connection practices protect credentials and TLS verification?

## Further Reading

- MongoDB sharding: <https://www.mongodb.com/docs/manual/sharding/>
- MongoDB shard keys: <https://www.mongodb.com/docs/manual/core/sharding-shard-key/>
- MongoDB choose a shard key:
  <https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/>
- PyMongo getting started: <https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/>
- Psycopg documentation: <https://www.psycopg.org/psycopg3/docs/>
