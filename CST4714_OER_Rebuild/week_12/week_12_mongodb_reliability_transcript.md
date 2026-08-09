# Week 12: MongoDB Reliability and Recovery Evidence - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: MongoDB Reliability and Recovery Evidence

This week asks a reliability question that sounds simple but is not: what does a database promise when a node, network path, client, or human action fails? We will answer by naming the operation, failure, mechanism, observed behavior, and limitation instead of using broad phrases such as highly available or safe.

We will study MongoDB replica sets, elections, write concern, read preference, read concern, and partition behavior. Then we will separate replication from backup by creating and verifying a collection-level logical recovery artifact. The same reasoning applies beyond MongoDB: a replicated service and a recoverable history solve different failure classes.

## Slide 2: A reliability promise needs five visible parts

A useful reliability promise begins with one operation. A ticket write and an analytics read can deserve different behavior. Next, name the failure. Loss of one member is different from a network partition, and both are different from an authorized deletion that every replica accepts.

Then state acceptable behavior. Should the operation continue, wait, reject, retry, return older data, or recover later? Only after those choices should we select a mechanism. Finally, define evidence and limitation. A successful read after reconnection may support client recovery, but it does not prove that an accidental deletion can be restored. This framework prevents a product feature from becoming a promise larger than the evidence.

## Slide 3: Replication and backup protect against different failures

Replication maintains current service state across members. If one member is unavailable, another member may continue or become primary when the election requirements are met. That is valuable for continuity, but the replicas are participating in the same active history.

When an authorized user deletes a collection, replication can faithfully copy that deletion. A backup or logical export preserves an earlier recoverable artifact outside the active state. It solves a different problem. The artifact alone is not recovery: we still need a compatible tool, a separate target, permission, time, and verification. Three replicas are not three independent backups.

## Slide 4: A replica set copies one ordered stream of changes

Under normal operation, the primary accepts writes. It records data changes in the oplog, a bounded ordered log used for replication. Secondaries fetch and apply those operations. Because that work is asynchronous, a secondary can temporarily be behind the primary.

If the primary becomes unavailable, eligible voting members may elect a new primary when a majority can agree. Election, topology discovery, and client reconnection take time. A driver can retry only according to supported settings and operation semantics. This architecture can hide some member failures, but it cannot promise that every request is uninterrupted or that every secondary read sees the newest acknowledged value.

## Slide 5: Write concern defines the acknowledgment a client waits for

Write concern tells the server what acknowledgment the client requires. A majority acknowledgment asks for confirmation from the calculated majority of voting data-bearing members under the deployment's documented rules. Waiting for more acknowledgment can improve resilience to rollback, but it can increase latency and reduce successful writes when enough members are unavailable.

A write-concern timeout creates an important application problem. It means the requested acknowledgment was not received before the deadline. The write may still exist on one or more members. Blindly repeating a non-idempotent request can create a duplicate. Applications need stable operation identifiers, safe retry rules, and a read-back strategy that can determine the outcome without assuming timeout means absence.

## Slide 6: Read preference selects a member; concern limits visibility

Read preference is a routing choice. Primary directs normal reads to the primary. Secondary or secondary-preferred can route eligible reads to secondaries, which may help certain locality or workload goals. Because replication is asynchronous, those reads may observe older state.

Read concern is a visibility choice. It defines which data is eligible to be returned under the product's consistency and isolation semantics. The two settings solve different questions and interact with sessions, write concern, and topology. A read-your-own-write workflow should not casually route the confirmation read to a lagging secondary simply because secondary reads sound scalable.

## Slide 7: A partition forces an operation-specific choice

During this partition, two voting members can still communicate with each other while the third member is isolated. The two-member side retains a voting majority and can agree on a primary. The isolated member cannot independently become a primary while preserving one authoritative current history.

This is the practical CAP question. During a communication partition, which operations remain available, and what consistency behavior do they preserve or sacrifice? CAP consistency is a single-copy style property, not the generic C in ACID. CAP availability means every request to a non-failing node receives a response, not that the service is usually online. We describe specific operation behavior instead of labeling the whole product with two permanent letters.

## Slide 8: Reliability settings should follow user expectations

The settings on this table are candidates tied to four different expectations. A confirmed ticket may justify majority acknowledgment because silent loss after a minority member failure would harm the user. The immediate confirmation read should avoid a route that can return a stale view of the just-completed action.

An hourly dashboard may tolerate slight lag and could justify a secondary-oriented route if measurement supports it. Accidental deletion needs a separate recovery artifact because replication can copy the deletion. None of these choices is universally strongest. Each has latency, availability, staleness, storage, scheduling, or operational cost. The decision is credible only when its mechanism and limitation are stated.

## Slide 9: Lab 1: Match expectations to reliability decisions

Complete this lab individually. Use the four Metro Support expectations to build one decision matrix. For each row, name the operation, user impact, relevant setting or mechanism, expected failure or timeout behavior, verification evidence, and limitation. Confirm current Atlas Free constraints with the linked official page and record the date checked.

Then analyze the stated partition in precise terms. Finish the same file with one short final-project workload checkpoint naming two reads, one write, and one failure or recovery concern. The canonical final-project page remains the only source of final requirements. Submit one file and keep every credential, project identifier, and network detail out of it.

## Slide 10: Recovery is a procedure, not a file

Day two turns the reliability distinction into recovery practice. We will create a transparent collection-level logical export, restore it to a different database and collection, and verify that the recovered data still answers meaningful questions.

This educational JSON artifact is deliberately inspectable, but it is narrower than a complete database backup. We will compare it with `mongodump` and `mongorestore`, which can preserve additional database metadata within documented behavior. The point is not to call every copied file a backup. The point is to name scope accurately and prove the parts that were restored.

## Slide 11: Extended JSON preserves BSON meaning that JSON cannot

Ordinary JSON has a small set of value types. MongoDB stores BSON, which can distinguish values such as ObjectId, date, decimal, binary, and several numeric forms. If an export turns every special value into a plain string or generic number, the restored document may look similar while behaving differently in comparisons, sorting, validation, or application code.

MongoDB Extended JSON provides representations that carry BSON type meaning through JSON-compatible text. The recovery notebook uses canonical Extended JSON so the serialized artifact is transparent while preserving those meanings. Verification must still inspect restored types rather than assuming that valid JSON implies faithful BSON recovery.

## Slide 12: A recovery drill closes the loop from source to evidence

A recovery drill begins by naming scope. Which database and collection are represented, and which parts of the system are outside the artifact? Export the data and record whether the operation completed, the file size, and a hash that can identify the exact bytes later.

Restore into a separate target so the source remains available for comparison. Verify more than row count: trace stable identifiers, inspect restored BSON types, run a meaningful query, and test one expected validation behavior where the scope supports it. End with omissions. A collection export does not automatically preserve all indexes, validators, users, network settings, multi-collection consistency, or point-in-time history.

## Slide 13: JSON recovery and mongodump cover different scopes

The notebook's Extended JSON path is useful because every step is visible. Students can inspect serialization, hash the artifact, restore to a new target, and compare identifiers and types. Its narrowness must be stated: it is not a complete database backup simply because it can recover documents.

`mongodump` and `mongorestore` are the documented database-tools path for logical backups and restores, including supported collection metadata and index definitions. Their compatibility, namespace mapping, credentials, and tool versions still matter. Neither path recreates every Atlas project setting, database user, network rule, or external secret. A recovery plan must account for both data artifacts and environment configuration.

## Slide 14: Lab 2: Restore MongoDB data and verify the claim

Complete this lab individually in the provided notebook. The default offline path executes the full export, restore, and verification sequence with an in-memory fixture. If you use Atlas, enter the URI only at runtime through the hidden prompt, use uniquely named temporary targets, and remove temporary network access after class.

Record artifact size and SHA-256, then verify counts, stable identifiers, BSON types, one query, and one expected validation failure. Complete the comparison with `mongodump` and state the artifact's limitations. Before submission, search the notebook source and outputs to confirm that no connection string, password, project identifier, or IP address was stored.

## Slide 15: Reliable systems make failure behavior and recovery evidence explicit

This week separated several ideas that are often collapsed. Write concern changes required acknowledgment. Read preference changes eligible routing. Read concern changes visibility semantics. Replica-set elections can restore a writable primary when a voting majority can agree, but failover is not instantaneous and partitions force operation-specific tradeoffs.

Replication protects continuity against some member failures while also copying destructive changes. Recovery needs a separate artifact, target, procedure, credentials, and verification. A strong reliability statement names operation, failure, acceptable behavior, mechanism, evidence, and limitation. Next week we will use the same discipline for scale, capacity, sharding, and safe data integration.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
