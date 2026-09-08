# Module 12: Reliability Is a Set of Explicit Promises

## Operating Question

When a managed document database has multiple nodes, which failures can it hide,
which data can a client read or lose, and which separate recovery artifact still
needs to exist?

## Learning Outcomes

After this module, you can:

- explain primary, secondary, oplog, election, and failover roles in a replica set;
- distinguish read preference, read concern, and write concern;
- describe the CAP tradeoff during a network partition without using "pick any
  two" as a product label;
- distinguish replication from backup;
- create a free-tier-appropriate MongoDB logical recovery plan; and
- connect a reliability promise to mechanism, failure, evidence, and limitation.

## 1. Reliability Begins With a Specific Promise

"Highly available" is incomplete. A useful promise identifies:

- operation: read, write, query, restore, or reconnect;
- failure: process crash, node loss, network partition, bad deployment, or
  deletion;
- acceptable behavior: continue, reject, retry, use older data, or recover later;
- time or data-loss objective; and
- evidence and limitation.

Example:

> A ticket write acknowledged with majority write concern should survive loss of a
> minority of voting data-bearing replica-set members, subject to the deployment's
> durability settings. This does not protect against a later authorized deletion,
> so a separate logical recovery artifact is required.

## 2. Replica Sets Copy an Ordered Change History

A MongoDB replica set contains members that maintain the same logical dataset.

- The **primary** accepts writes under normal operation.
- **Secondaries** replicate operations from the primary's oplog and apply them.
- The **oplog** is a bounded, ordered log of data changes used for replication.
- An **election** can choose a new primary when the old one is unavailable and a
  voting majority can agree.

Replication is asynchronous. A secondary can lag behind the primary. Election and
client reconnection take time, so failover is not instantaneous or invisible to
every operation. Drivers discover topology and retry only according to supported
settings and operation semantics.

Atlas Free uses a fixed three-node replica-set configuration, but students cannot
change its replication factor or run Atlas failover testing. We analyze topology
and client behavior rather than claiming to perform an unavailable test.

## 3. Write Concern Defines Required Acknowledgment

Write concern describes what acknowledgment a client waits for.

```javascript
db.tickets.insertOne(
  { ticket_id: 1099, status: "new", subject: "Write concern test" },
  { writeConcern: { w: "majority", wtimeout: 5000 } }
)
```

For a typical three-member replica set, `w: "majority"` requires acknowledgment
from a calculated majority of voting data-bearing members. Waiting for more
acknowledgments can improve the write's resilience to rollback but can add latency
or reduce successful writes when enough members are unavailable.

A write-concern timeout means the requested acknowledgment was not received in
time. It does not necessarily prove that no member applied the write. Applications
need idempotent identifiers, read-back strategy, and retry rules that avoid
creating duplicates.

Write concern is not backup retention. A majority-acknowledged deletion is still a
durable deletion.

## 4. Read Preference Chooses Eligible Members

Common read preference modes include:

- `primary`: read from the primary; default for normal driver reads;
- `primaryPreferred`: prefer primary, permit secondary under documented conditions;
- `secondary`: read from a secondary;
- `secondaryPreferred`: prefer a secondary, permit primary; and
- `nearest`: select among eligible members by latency window and tags.

Reading from a secondary can distribute some read work or serve locality goals,
but asynchronous replication means the result may be behind the primary. A
read-your-own-write workflow should not switch casually to a lagging secondary.

Read preference is routing. It is not the same as read concern.

## 5. Read Concern Defines Visibility Guarantees

Read concern controls the consistency and isolation properties of returned data.
For example, `local` can return data from the member without guaranteeing that a
majority has durably committed it; `majority` limits reads to majority-committed
data under its documented semantics.

The combined behavior depends on read preference, read concern, write concern,
sessions, and topology. Avoid describing a whole database as simply "consistent"
or "eventually consistent" without naming the operation and settings.

## 6. CAP Is a Partition-Time Tradeoff

The CAP theorem concerns a distributed read/write data object when messages
between parts of the system can be lost or delayed indefinitely.

- **Consistency** in the theorem is a single-copy/linearizable style guarantee,
  not the generic ACID consistency property.
- **Availability** means every request to a non-failing node eventually receives a
  response, not merely "the service is usually up."
- **Partition tolerance** addresses communication partitions between nodes.

When a partition separates nodes, a system cannot guarantee both that every
partition continues answering every request and that all answers behave like one
current copy. It must reject or delay some operations, permit potentially divergent
or stale behavior, or use a more specific compromise.

"Choose two of three" is misleading because a real distributed system cannot wish
network partitions away. The practical question is which operations remain
available during a partition and which consistency behavior they sacrifice or
preserve.

## 7. Replication Is Not Backup

Replication helps with member failure and service continuity. It can also replicate:

- an accidental deletion;
- a bad update;
- corrupted application data;
- an authorized destructive command; or
- an unwanted schema change.

A backup or logical export creates recoverable history outside the active replica
state. Recovery still needs a target, procedure, credentials, compatibility, and
verification.

## 8. Atlas Free Requires Manual Logical Recovery

Current Atlas documentation states that native Atlas backups are unavailable for
Free clusters. Free clusters also do not support sharded-cluster creation or
primary-failover testing. The documented backup alternative is `mongodump` and
`mongorestore`.

```bash
mongodump \
  --uri="$MONGODB_URI" \
  --db=cst4714_metro_support \
  --archive=metro_support.archive.gz \
  --gzip
```

Inspect the command exit status, file size, hash, and tool output. Enter the URI at
runtime; do not commit it.

Restore into a different database name:

```bash
mongorestore \
  --uri="$MONGODB_RESTORE_URI" \
  --archive=metro_support.archive.gz \
  --gzip \
  --nsFrom='cst4714_metro_support.*' \
  --nsTo='cst4714_metro_support_restore.*'
```

Review current Database Tools compatibility. Logical dumps include collection
documents, metadata/options, and index definitions within documented behavior, but
cluster users, project network rules, and every Atlas configuration are not simply
recreated by restoring one database dump.

## 9. `mongoexport` Is Useful but Narrower

`mongoexport` produces JSON or CSV data suitable for interchange. It is helpful
for a collection-level exercise or migration, but it is not a complete backup
system. It may not preserve BSON type fidelity, collection options, validators,
indexes, privileges, or a consistent multi-collection point by itself.

The course reliability notebook uses a transparent JSON export/restore to teach
the evidence sequence, then explicitly compares it with `mongodump`. The narrower
artifact must not be mislabeled.

## 10. Verify a MongoDB Restore

### Structure and Rules

```javascript
db.getCollectionNames()
db.getCollectionInfos({ name: "tickets" })
db.tickets.getIndexes()
```

Confirm collections, validators, and required indexes.

### Data and Relationships

```javascript
db.tickets.countDocuments({})
db.ticket_events.countDocuments({})
db.tickets.countDocuments({ status: "open" })
```

Trace known identifiers and check for references with no target when the model uses
references.

### Behavior

Run one meaningful aggregation and one expected validation failure in the restore
target. If recovery scope includes application access, test a temporary read and
write using a least-privilege credential.

### Limitation

Counts and one query do not prove every document value, historical moment,
permission, or application path is correct.

## Worked Example: Reliability Decision Matrix

**Workload:** a resident submits a ticket and immediately sees confirmation. A
short delayed analytics report is acceptable. A confirmed ticket should not be
silently lost after one member failure.

| Decision | Choice | Reason | Cost/limit |
|---|---|---|---|
| ticket write | majority acknowledgment with bounded timeout | stronger resilience for confirmed write | latency and possible timeout ambiguity |
| confirmation read | primary with appropriate concern/session behavior | avoid stale immediate confirmation | primary read load |
| analytics read | secondary-preferred where acceptable | stale report is tolerable | data can lag |
| accidental deletion | logical backup/restore | replication copies deletion | recovery point and restore time depend on export schedule |

The choices follow user expectations, not a universal strongest-setting rule.

## Common Misconceptions

### "Three nodes means three backups"

Replicas share the active history and can reproduce destructive changes. Backup is
a separate artifact and recovery process.

### "Majority write concern means the write definitely failed on timeout"

The acknowledgment condition timed out. The write may exist on some members. The
application needs safe retry and verification logic.

### "Secondary reads are always faster"

Topology, latency, lag, indexes, workload, and routing determine behavior. They may
be stale and are not automatically faster.

### "CAP says every database picks two letters forever"

The tradeoff is about behavior during a network partition under specific formal
definitions.

## Practice

Write a reliability matrix for a small inventory system. Include one critical
write, one stale-tolerant read, one partition scenario, one accidental deletion,
and one restore verification. For every choice, name a mechanism and limitation.

## Retrieval and Transfer

1. What is the oplog's role in a replica set?
2. How do write concern and read preference differ?
3. Why can a write-concern timeout produce an ambiguous application outcome?
4. What CAP decision appears only during a partition?
5. Why does a replica not replace a backup?
6. Which Atlas Free limits change the Week 12 lab design?

## Further Reading

- MongoDB replication: <https://www.mongodb.com/docs/manual/replication/>
- Replica-set read and write semantics:
  <https://www.mongodb.com/docs/manual/applications/replication/>
- MongoDB write concern: <https://www.mongodb.com/docs/manual/reference/write-concern/>
- MongoDB read concern: <https://www.mongodb.com/docs/manual/reference/read-concern/>
- Atlas Free limits: <https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/>
- MongoDB `mongodump`: <https://www.mongodb.com/docs/database-tools/mongodump/>
- Gilbert and Lynch, CAP formalization:
  <https://people.cs.rutgers.edu/~rmartin/teaching/spring04/cs553/BrewersConjecture-SigAct.pdf>
