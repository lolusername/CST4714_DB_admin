# Module 14: Multiple Databases Multiply Options and Obligations

## Operating Question

If one application uses PostgreSQL and MongoDB, which system owns each fact, how do
changes cross the boundary, and how can an incident be diagnosed without making
the systems disagree further?

## Learning Outcomes

After this module, you can:

- distinguish polyglot persistence from casual technology accumulation;
- assign one authoritative owner to each fact;
- compare synchronous dual writes, event-driven propagation, and reconciliation;
- identify consistency, security, backup, and observability obligations across
  systems;
- triage a cross-database incident from symptoms and evidence; and
- defend a one-platform or two-platform final-project choice.

## 1. Polyglot Persistence Is Workload-Based Specialization

A polyglot system uses different data technologies for different responsibilities.
For example:

- PostgreSQL owns users, permissions, and authoritative ticket state;
- MongoDB stores flexible, high-volume event detail or read-optimized ticket
  snapshots; and
- an object store holds attachments.

This can fit workloads well. It also creates more deployment, access, monitoring,
recovery, and consistency work. A small application should prefer one database
unless the second solves a specific problem worth that cost.

## 2. Every Fact Needs One Authoritative Owner

If both PostgreSQL and MongoDB contain `ticket.status`, answer:

- Which copy accepts the business update?
- Which copy is derived?
- How is the derived copy refreshed?
- How stale may it be?
- How is disagreement detected and repaired?
- Which copy is used during recovery?

Without an owner, "synchronize both" becomes an undefined circular obligation.
Duplication can be deliberate when one source is authoritative and the other is a
cache, projection, snapshot, or historical record.

## 3. Synchronous Dual Writes Create Partial-Failure Risk

Naive sequence:

1. update PostgreSQL;
2. update MongoDB; and
3. return success.

If step 1 commits and step 2 fails, the stores disagree. Reversing the order only
changes which partial outcome occurs. A distributed transaction protocol can
coordinate some systems but adds availability, latency, and operational cost and
is not generally supplied by two unrelated cloud APIs.

Do not hide the boundary behind a broad `try/except`. Record an operation ID,
preserve an authoritative result, and design retry or reconciliation.

## 4. Event-Driven Propagation Separates Commit From Projection

One pattern:

1. commit the authoritative relational change;
2. record an event describing that committed change;
3. a consumer applies it to a MongoDB projection; and
4. monitoring detects lag or failure.

The **transactional outbox** stores the business change and outgoing event in the
same local transaction. A relay publishes unsent events. This avoids the gap where
the business row commits but the event is never recorded.

The consumer should be idempotent: applying the same event twice should not create
duplicate effect. Use stable event IDs and record processed state or use an upsert
whose final state is deterministic.

Event-driven design trades immediate cross-store consistency for decoupling,
retries, and observable lag. State whether that is acceptable to the user.

## 5. Reconciliation Is a Designed Operation

Even a reliable pipeline needs a way to compare systems.

Useful checks include:

- counts by stable partition or date;
- missing authoritative identifiers;
- version or updated-at mismatches;
- hashes of canonical field sets;
- event offsets or last processed IDs; and
- samples of high-risk records.

Reconciliation output should identify an owner and repair direction. Blindly
copying the newest timestamp can be wrong when clocks, delayed events, or manual
repairs differ.

## 6. Identity and Access Cross the Boundary Too

A shared application user may map to:

- a Supabase Auth identity;
- PostgreSQL roles or RLS claims;
- an application service credential;
- an Atlas database user; and
- document-level owner identifiers.

Do not give browser clients powerful Atlas or Supabase service credentials. A
backend service can mediate access, but it must enforce authorization and retain
least privilege in both databases.

Audit evidence should correlate actions through a request or operation ID without
copying secrets or unnecessary personal data.

## 7. Backup and Restore Need an Order

Independent logical dumps taken at different moments may not represent one
application-consistent point. A recovery plan must state:

- which system is authoritative;
- backup cadence and recovery point for each;
- restore order;
- how derived data is rebuilt or reconciled;
- how events are replayed without duplication; and
- how traffic remains isolated until verification.

If MongoDB contains a rebuildable projection of PostgreSQL facts, restoring
PostgreSQL and regenerating the projection may be safer than treating both dumps
as equally authoritative.

## Worked Incident: Ticket State Disagrees

**Symptoms:** The resident portal shows ticket 1008 as `open`. The staff dashboard
shows `resolved`. The event feed contains a `ticket_resolved` event.

**Architecture:** PostgreSQL owns ticket state. An outbox relay updates a MongoDB
read projection used by the resident portal.

### Evidence Sequence

1. Query PostgreSQL ticket 1008 and its transaction/update time.
2. Query the outbox for the stable event ID and publish status.
3. Query consumer logs or checkpoint for that event ID.
4. Query the MongoDB projection's source version and event ID.
5. Check whether later events supersede it.

### Plausible Finding

PostgreSQL and the outbox committed. The consumer failed after receiving the event
but before updating the projection, and its retry queue is paused.

### Response

Resume or replay the idempotent consumer from the recorded event. Do not manually
edit both stores without recording the repair. Verify the MongoDB projection now
contains the authoritative version, the event is marked processed, lag returns to
normal, and no duplicate history was created.

### Limitation

This evidence supports one incident path. It does not prove every projection is
consistent; run the reconciliation check for the affected partition.

## 8. Observability Should Follow a Request Across Systems

Useful signals include:

- request or operation ID;
- authoritative commit result;
- outbox backlog and oldest age;
- consumer success/failure and retry count;
- projection version lag;
- query latency and error by datastore;
- connection-pool exhaustion; and
- backup age and last restore verification.

Logs without stable identifiers make cross-system timelines guesswork. Metrics
without user impact can also mislead. Connect technical evidence to the failed
operation.

## 9. A One-Database Design Is Often the Stronger Decision

Use one platform when:

- the workload fits its model and scale;
- the team is small;
- cross-store consistency would add risk;
- operational evidence is already difficult; or
- the second system is chosen only to appear advanced.

Use two when the workload benefit is concrete, ownership is explicit, propagation
and recovery are designed, and the team can operate both.

## Common Misconceptions

### "The same ID means the records are synchronized"

Identifiers support correlation. They do not prove field equality, ordering, or
successful propagation.

### "Events guarantee consistency"

Events create a mechanism. Delivery, ordering, idempotency, retries, lag, and
reconciliation determine behavior.

### "Two backups produce one consistent recovery point"

Independent artifacts can represent different moments. Ownership and replay order
must be part of the plan.

### "Polyglot means using as many databases as possible"

It means matching technologies to distinct needs while accepting the operating
cost.

## Practice

Create a responsibility table for a two-store inventory system. For inventory
quantity, product description, flexible event details, and user access, name the
authoritative store, derived copy if any, propagation path, acceptable staleness,
reconciliation check, and recovery order.

## Retrieval and Transfer

1. Why does each duplicated fact need one authoritative owner?
2. What partial failure occurs in synchronous dual writes?
3. How does a transactional outbox reduce one failure gap?
4. What makes an event consumer idempotent?
5. Why can two independent backups be application-inconsistent?
6. Which evidence would diagnose projection lag?

## Further Reading

- Martin Fowler, Polyglot Persistence:
  <https://martinfowler.com/bliki/PolyglotPersistence.html>
- Microsoft Azure Architecture Center, Transactional Outbox pattern:
  <https://learn.microsoft.com/azure/architecture/databases/guide/transactional-outbox-cosmos>
- AWS Prescriptive Guidance, Transactional Outbox pattern:
  <https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html>
- PostgreSQL logical decoding concepts:
  <https://www.postgresql.org/docs/current/logicaldecoding-explanation.html>
- MongoDB change streams: <https://www.mongodb.com/docs/manual/changeStreams/>
