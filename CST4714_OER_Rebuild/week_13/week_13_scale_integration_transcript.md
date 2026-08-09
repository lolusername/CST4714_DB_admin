# Week 13: Capacity, Sharding, and Python Integration - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Capacity, Sharding, and Python Integration

This week connects two skills that often appear separately: reasoning about scale and writing a small client that moves real data safely. Scale is not a yes-or-no property of a database. It is a relationship among workload, data volume, latency, throughput, growth, cost, and operating complexity.

We will compare tuning, vertical scaling, replication, partitioning, and sharding. We will evaluate candidate shard keys without pretending that a free Atlas deployment is a sharded cluster. Then a Python notebook will inspect a small public cybersecurity dataset, test distribution assumptions, load one chosen platform or the offline path, and verify more than an insert count.

## Slide 2: A capacity claim needs quantities and a time horizon

A claim such as ‘MongoDB scales’ or ‘PostgreSQL will be too slow’ has no usable scope. Begin with quantities. How many records exist now? How large is the working set and each important index? Which query shapes dominate? What are average and peak reads and writes? Which latency and error objectives matter to users?

Then add a time horizon. A beginner project does not need fabricated enterprise traffic. It can state a small present workload, one plausible growth scenario, and one trigger for reevaluation. For example: if the newest-open-ticket query exceeds a measured latency objective at ten times the current fixture, inspect its plan and working set before adding infrastructure.

## Slide 3: Scale the bottleneck only after locating it

The first step is measurement, not architecture. A slow request may be scanning unnecessary rows, sorting without support, returning too much data, or waiting on another transaction. Adding nodes does not remove those causes and can make them harder to observe.

After removing waste, vertical scaling may be the simplest next step when the workload still fits one database node or tier. Caching and read replicas can serve selected reads, but they add freshness and invalidation decisions. Partitioning or sharding distributes data and work, while also adding routing, rebalancing, network failure, cross-partition coordination, backup, and monitoring obligations.

## Slide 4: Replication and sharding solve different growth problems

Replication places copies of the logical dataset on multiple members. It supports availability and can support selected read routing under explicit consistency tradeoffs. Each data-bearing member still stores the replica-set data rather than owning only one disjoint part of a sharded collection.

Sharding divides a collection's shard-key ranges across shards. Each shard is normally itself a replica set, so a production sharded architecture combines distribution and replication. Atlas Free gives us a replica-set environment but does not let us create a sharded cluster. We will analyze and simulate distribution rather than claiming experience with a paid deployment we did not operate.

## Slide 5: A sharded cluster routes requests through metadata

Applications connect through `mongos`, a query router. The router consults cluster metadata maintained by the config server replica set. It uses shard-key ranges to target one shard, a limited shard set, or every relevant shard, then merges results when necessary.

Each shard stores part of the collection and is normally a replica set for availability. Chunks or ranges can move as the cluster balances distribution. This architecture creates durable operating obligations: routing health, metadata health, balancing, cross-shard operations, recovery order, and cost. The shard key is central because it controls both where documents live and which queries can avoid broad scatter-gather work.

## Slide 6: A shard-key candidate must answer four questions

Cardinality asks how many distinct values exist. A Boolean field or a five-value status field cannot create many independent ranges by itself. Frequency asks how evenly the values and traffic are distributed. A field can have millions of values while one tenant or category still dominates the workload.

Monotonicity asks whether new values continually increase or decrease. Range sharding on a timestamp or sequence can send new writes toward the range containing the current extreme. Targeting asks whether common queries include the shard key. A query missing the needed key prefix may be broadcast. A good candidate balances distribution and targeting; high cardinality alone is not enough.

## Slide 7: Ranged and hashed distribution trade locality for spread

Ranged sharding preserves order. Nearby shard-key values stay in nearby ranges, so a bounded range query can be routed efficiently when it contains the key. The same locality can create hotspots when a key is monotonic or one range receives disproportionate traffic.

Hashed sharding transforms the value for distribution. It can spread sequential identifiers more evenly, but a range query on the original value no longer maps to one contiguous hash range. That query may contact many shards. The choice follows real query and write patterns. Even distribution is not sufficient when every important query becomes scatter-gather.

## Slide 8: Candidate keys reveal different risks in the same dataset

The CISA Known Exploited Vulnerabilities subset gives us concrete fields to examine. Status-like fields have low cardinality. Date added has many values and can support time questions, but new records arrive at the newest end. A hashed vulnerability identifier may distribute documents well and target exact lookups, while vendor or time questions can scatter.

A compound candidate beginning with vendor or project may serve vendor-oriented questions, but real frequency matters because a few vendors can dominate. This table does not select a production key. It identifies measurements, query patterns, and risks. Recommending not to shard yet is valid when the dataset and workload do not justify the added system.

## Slide 9: Day 1 studio: Measure distribution before recommending scale

Work individually in the Week 13 notebook. Begin with the bundled, versioned CISA sample so the class has a reliable offline path. If the current public feed is available, compare its retrieval date and structure before using it. Record source, terms, selected fields, nulls, duplicate vulnerability identifiers, date conversion, and one question the subset can answer.

Then evaluate each candidate key from actual measurements. Run the deterministic range and hash simulations and explain what the bucket counts do and do not model. Recommend one candidate or recommend not sharding yet. The goal is a defensible decision based on this workload, not a claim that a simulated bucket is a real sharded deployment.

## Slide 10: A small client should expose every important boundary

Day two uses a small Python client to make data integration visible. Large helper libraries can hide the exact connection, transformation, write, and verification steps that beginners need to understand. The notebook keeps those steps direct and heavily explained.

You may choose Atlas, Supabase or PostgreSQL, both for an explicitly different experiment, or the complete offline SQLite path. The learning outcome is not a successful cloud screenshot. It is the ability to explain how the client authenticated, how source fields became database values, how reruns avoid duplication, and which checks support the import claim.

## Slide 11: The client contract differs, but safe connection habits transfer

For Atlas, the URI describes topology discovery, TLS, authentication, and options. Enter it at runtime through the hidden prompt, then ping before any write. Do not add `tlsInsecure=True` as a routine fix because that disables certificate validation and can conceal the real problem. Check the URI, driver, system time, DNS, Atlas network access, and current supported TLS path.

For PostgreSQL or Supabase, the connection URL identifies host, port, database, role, TLS behavior, and often a connection mode. If a Colab environment cannot reach a direct IPv6 address, use the provider's current IPv4-compatible pooler URI instead of changing SQL code randomly. In both systems, stable keys and upsert behavior make a rerun deliberate rather than duplicative.

## Slide 12: A trustworthy import has a visible before and after

Inspect before loading. Record the source and data-use terms, understand the fields, measure size, identify nulls and duplicates, and choose a small subset tied to an answerable question. Transform explicitly so dates, missing values, and field names do not change by accident.

Connect at runtime, test the connection, and identify the exact disposable target. Write a small idempotent batch using a stable vulnerability identifier. Verification should compare expected and observed counts, retrieve one known identifier, inspect representative types, and answer one grouped question. These checks support scope, but they do not prove that every source value, permission, or future rerun is correct.

## Slide 13: Lab: Public data capacity and cloud integration

Complete the notebook individually. Choose one platform path that you can operate safely today. Cloud credentials belong only in the hidden runtime prompt. The offline SQLite path is a complete evidence path when cloud access is blocked, not a lesser blank fallback. If you choose both cloud systems, each must have a distinct ownership or modeling purpose rather than duplicating rows for appearance.

Load records idempotently by vulnerability identifier. Verify expected and observed count, one known identifier, representative types, and one grouped question. Explain what those checks do not prove. Finish the notebook's short final-project checkpoint without redefining the final assignment, then confirm that no URI, password, key, token, private host, or output containing one remains.

## Slide 14: Scale decisions connect workload evidence to operating cost

This week replaced the vague question ‘does it scale?’ with measurable workload, objective, and growth assumptions. We compared query and model improvement, vertical scaling, replication, partitioning, and sharding. A shard key must balance cardinality, frequency, monotonicity, and query targeting; even distribution alone does not guarantee efficient access.

The Python notebook made the client contract visible across source inspection, credential-safe connection, explicit transformation, idempotent write, and multi-part verification. Scaling also scales credentials, metrics, backups, failure combinations, and cost. Next week we will examine those obligations when one application uses more than one database and a derived copy becomes stale.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
