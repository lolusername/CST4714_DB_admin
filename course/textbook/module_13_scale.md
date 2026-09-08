# Scale Changes the Questions a System Must Answer

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

## Capacity Planning Starts With a Workload

The word scale can describe several different changes. A table can grow while
traffic stays low. Traffic can grow while the dataset stays small. A once-per-day
report can become an interactive request whose user will not wait. These cases
stress storage, throughput, and response time differently. Buying more capacity
before identifying the pressure may increase cost without improving the user
experience.

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

**Throughput** is completed work per unit time, such as requests per second.
**Latency** is the time one request takes. A system can finish many requests per
second while some users wait a long time. A percentile describes that spread:
the 95th-percentile latency is a value at or below which roughly 95 percent of
the measured requests fall, under the stated calculation method. It is not the
average, and it says nothing about requests omitted from the measurement.

The **working set** is the data and index pages an active workload repeatedly
uses. A database larger than memory can still serve a small hot working set
efficiently. Conversely, adding many speculative indexes can crowd useful pages
out of cache. Before changing architecture, connect the observed pressure to
the actual query mix and data distribution.

## Fix Waste Before Distributing It

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

Replication and sharding are especially easy to confuse. Replicas maintain
copies of a logical dataset so a service can tolerate member failure or serve
eligible reads elsewhere. Shards hold different portions of a dataset. In a
sharded MongoDB deployment, each shard can itself be replicated. Adding three
replicas of one dataset is not the same as dividing that dataset into three
independently placed portions.

## MongoDB Sharding Distributes Collection Ranges

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

## Four Shard-Key Questions

### Cardinality

How many distinct key values exist? A Boolean or five-value status field cannot
create many independently distributable ranges by itself.

If 75 records have 75 distinct CVE identifiers but only five distinct date-added
values, those candidate fields have different cardinalities. This describes
the sample's distribution, not how often users will query any particular record.
Always separate a measured record distribution from an assumed traffic pattern.

### Frequency

How often does each value occur? A high-cardinality key can still be skewed if one
value dominates traffic or document count.

Hashing a repeated value does not split its occurrences among arbitrary shards:
the same input value produces the same hash value. A key with a million identical
values therefore retains that concentration under hashing. A more varied full
key may be necessary; "hashed" is not a repair for every skewed model.

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

## Ranged and Hashed Distribution Make Different Tradeoffs

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

Imagine sorting cards by neighborhood and date. A neighborhood/date-range
question can identify a contiguous region of that arrangement. Shuffling the
cards by a stable hash of ticket ID distributes nearby IDs but loses that date
locality. The analogy explains the tradeoff; actual MongoDB placement also uses
chunks, routing metadata, and balancing. A classroom bucket simulation is not
an implementation of the server's hash function or placement algorithm.

## Cross-Shard Operations Cost More Coordination

A request can be:

- **targeted:** routed to one shard or limited shard set using the shard key; or
- **scatter-gather:** sent broadly and merged by `mongos`.

Cross-shard aggregations, transactions, uniqueness, and resharding can add network
and coordination cost. A design can still use them; the cost should be visible.

## Worked Example: Evaluate Metro Support Candidates

Hypothetical workload, not a measurement of the small supplied fixture:

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

## Python Makes the Client Contract Visible

A driver connection includes network routing, TLS, authentication, server
selection, timeouts, and query behavior. Keep the first program small.

A **driver** is the library that speaks the database protocol from a programming
language. Installing it does not create a database or authorize access. The
following examples assume the driver is installed and an existing personal
practice database contains the stated data. The
[integration notebook](../notebooks/06_public_data_capacity_integration.ipynb)
includes installation, a bounded source, setup, and cleanup when you need the
complete start-to-finish path.

### MongoDB Atlas

```python
from getpass import getpass
from pymongo import MongoClient
from pymongo.server_api import ServerApi

mongodb_uri = getpass("Atlas connection URI: ")
database_name = input("Existing practice database name: ").strip()
with MongoClient(
    mongodb_uri,
    server_api=ServerApi("1", strict=True, deprecation_errors=True),
    serverSelectionTimeoutMS=10000,
    timeoutMS=10000,
) as client:
    client.admin.command("ping")
    tickets = client[database_name]["tickets"]
    for ticket in tickets.find(
        {"status": "open"}, {"_id": 0, "ticket_id": 1}
    ).limit(20):
        print(ticket)
```

Do not add `tlsInsecure=True` as a routine fix. It disables certificate validation
and can hide the real issue. Check the URI, current driver, system time, network
access list, DNS, and supported TLS path.

The `with` block closes the client when the example finishes or raises an error.
The query reads at most twenty matching documents and makes no changes. A
successful ping with an empty result can mean that the database name is wrong,
the collection is absent, or no ticket is open. Check the intended source and a
known identifier instead of interpreting an empty loop as proof of a successful
import. Remove the temporary runtime IP rule when cloud practice is finished.

### PostgreSQL/Supabase

```python
from getpass import getpass
import psycopg
from psycopg.conninfo import conninfo_to_dict

database_url = getpass("PostgreSQL connection URL: ")
sslmode = conninfo_to_dict(database_url).get("sslmode", "prefer")
if sslmode not in {"require", "verify-ca", "verify-full"}:
    raise ValueError("Add sslmode=require or a stronger mode to the URL.")

with psycopg.connect(database_url, connect_timeout=10) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT count(*) FROM metro_support.tickets")
        print(cursor.fetchone())
```

On a network without direct IPv6 connectivity, use the provider's current IPv4-
compatible session-pooler URI rather than changing database code randomly.
`sslmode=require` prevents an unencrypted fallback but does not verify server
identity. For production, use `verify-full` with the provider's CA certificate.

Inside the cursor block, pass changing **values** as parameters rather than
building SQL by joining strings. This fragment uses the already opened cursor:

```python
requested_status = "open"
cursor.execute(
    "SELECT ticket_id FROM metro_support.tickets WHERE status = %s ORDER BY ticket_id",
    (requested_status,),
)
print(cursor.fetchall())
```

The `%s` is a driver placeholder; it is not an invitation to apply Python string
formatting. The separate one-item tuple carries the value. The driver keeps data
from becoming SQL syntax. Do not put quotes around the placeholder. Table and
column **names** are identifiers, not values; dynamic identifiers require a
different composition mechanism such as `psycopg.sql.Identifier`.
[Psycopg parameter guide](https://www.psycopg.org/psycopg3/docs/basic/params.html)

## Import in Small, Verifiable Batches

Before loading a public dataset:

1. inspect license, source, retrieval date, columns, types, nulls, duplicates, and
   size;
2. select a small subset tied to a question;
3. convert dates and missing values intentionally;
4. write a batch;
5. check acknowledged-write results or row counts; and
6. query a known sample and total.

An import script should be rerunnable or explicitly idempotent. Stable natural
keys, upserts, a reset option in a disposable collection, or a recorded batch ID
can prevent accidental duplicates.

**Idempotent** means repeating an operation has the same intended final effect
as doing it once. An import keyed by a stable CVE identifier can update or keep
that record on a second run rather than insert another copy. It must still define
what happens if the source changes or a run stops partway through. Resetting an
empty table before every import is a useful test setup, but it does not
demonstrate idempotency: rerun the import against its existing output to test that
property.

### Inspect the Public Source Before Loading It

The course provides a documented 75-record selection from CISA's Known Exploited
Vulnerabilities catalog. Its metadata records a July 2026 source version and
retrieval, so it is a reproducible teaching snapshot, not a current operational
security feed. A CVE identifies a vulnerability record; `dateAdded` describes
catalog inclusion, not necessarily the date a vulnerability was discovered or
first exploited. The sample selects the first source records, not a random
sample of all software vulnerabilities.

Download [kev_sample.json](../datasets/cisa_kev_sample/kev_sample.json) and place it
beside this Python exercise, or upload it through Colab's Files panel. Unlike CSV,
the JSON file preserves the CWE list as an array. The outer object contains
source metadata; the actual records are inside its `vulnerabilities` array.

```python
import json
from collections import Counter

with open("kev_sample.json", encoding="utf-8") as source_file:
    source = json.load(source_file)

records = source["vulnerabilities"]
ids = set()
dates = Counter()
for record in records:
    ids.add(record["cveID"])
    dates[record["dateAdded"]] += 1

print("Source version:", source["catalogVersion"])
print("Records:", len(records))
print("Distinct CVE identifiers:", len(ids))
print("Distinct date-added values:", len(dates))
print("Most frequent dates:", dates.most_common(3))
```

`set` keeps distinct identifiers; `Counter` counts how often each date occurs.
The two cardinalities and the largest date counts give different information
about candidate keys. None of these counts ranks vendors by security quality or
measures traffic to a future application. A key can spread records well while
one popular record still receives most requests.

The integration notebook takes this inspected source through one selected
database path, a repeat import, and a question-driven query. Using both cloud
platforms is optional. The learning target is an understandable, repeatable
client-to-database workflow, not accumulating accounts.

## Scaling Also Scales Operations

More nodes or stores mean more:

- credentials and network rules;
- metrics and alerts;
- backup components and restore order;
- version compatibility;
- failure combinations;
- cost controls; and
- people who must understand the system.

A capacity recommendation should include the operating cost, not only throughput.

A simple first-pass storage projection makes assumptions explicit. If the system
starts with $D_0$ bytes, grows by $g$ bytes per day, retains $r$ days of new data,
and carries an overhead multiplier $m$ for indexes, replication, and working
space, then:

$$
D_{\text{projected}} = (D_0 + gr)m.
$$

This is not a vendor-sizing formula. It is a transparent baseline that reviewers
can challenge: growth may be nonlinear, compression varies, replicas multiply
physical storage, and peak working space can dominate a migration or index build.

For example, retaining an initial 100 MiB plus 20 MiB of new data per day for
30 days gives 700 MiB before overhead. An assumed factor of two gives 1,400 MiB.
One MiB is 1,048,576 bytes; one MB is 1,000,000 bytes. Keep units explicit when
comparing a measurement with a service quota. The multiplier is an assumption
to refine, not a promise that every platform charges or accounts for replicas
in that way. This formula also assumes the initial data is retained; an actual
retention policy may expire some of it.

An appropriate beginner recommendation might be: "Our current data is small, so
I would first measure the largest documents, index size, and the busiest query.
If retained growth approaches the free quota, I would shorten justified
retention, remove unnecessary copies, or evaluate another capacity tier before
considering sharding." It names a next measurement without inventing enterprise
load or treating a paid upgrade as part of the assignment.

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

## Study and Practice

Before Day 1, read the capacity and distribution sections through the candidate
comparison and the public-source inspection example. Before Day 2, read the Python, import, and storage
projection sections. The assigned notebook provides complete setup and cleanup;
the candidate analysis below is optional practice rather than another report.

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

- [MongoDB sharding](https://www.mongodb.com/docs/manual/sharding/)
- [MongoDB shard keys](https://www.mongodb.com/docs/manual/core/sharding-shard-key/)
- [MongoDB choose a shard key](https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/)
- [PyMongo getting started](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/)
- [Psycopg documentation](https://www.psycopg.org/psycopg3/docs/)
