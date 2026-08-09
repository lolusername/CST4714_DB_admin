# Retrieval and Exit Prompt Bank

## How to Use This Bank

These are short, ungraded learning prompts, not additional assignments. Select
three retrieval prompts near the start of a meeting and one exit prompt near the
end. Students should first answer from memory, then compare reasoning with the
module, a worked example, or live feedback.

The prompts deliberately return to earlier ideas. That spacing helps students
retrieve SQL, evidence, security, and recovery concepts after the week in which
they were introduced. Do not grade spelling or polished prose. Look for the
concept named in each prompt's **signal** and use aggregate patterns to decide
whether to reteach.

## Week 1: Responsibility and Relational Thinking

### Opening Retrieval

1. Distinguish data, a database, a DBMS, and a managed database service using one
   example. **Signal:** separates stored facts, software, and provider service.
2. If a managed provider keeps hardware running, name one responsibility that
   still belongs to the customer. **Signal:** avoids “cloud means no customer
   responsibility.”
3. In the relation `tickets(ticket_id, requester_id, status)`, what does one tuple
   represent? **Signal:** states row grain before syntax.

### Later Retrieval

1. Describe selection and projection without using SQL keywords. **Signal:** rows
   versus attributes.
2. What common attribute could join `tickets` to `users`, and what relationship
   would the result express? **Signal:** matching identifier and result meaning.
3. What four details make a technical observation reproducible? **Signal:**
   environment, action, observed result, interpretation.

### Exit Options

- A cloud query failed. Name one provider-side possibility, one customer-side
  possibility, and the first evidence you would inspect.
- Write one relational-algebra expression or plain-language operation for “open
  ticket identifiers and subjects.”

## Week 2: Major SQL Review

### Opening Retrieval

1. What does one result row represent in a query joining tickets and users?
   **Signal:** result grain rather than table names.
2. Predict whether `WHERE status <> 'closed'` includes a row whose status is
   `NULL`. **Signal:** three-valued logic.
3. Why can a one-to-many join increase row count? **Signal:** one parent repeats
   for matching child rows.

### Later Retrieval

1. When must a selected expression appear in `GROUP BY`? **Signal:** aggregate
   versus grouping expression.
2. Distinguish `WHERE` and `HAVING`. **Signal:** row filter before grouping versus
   group filter after aggregation.
3. Why test an `UPDATE` inside a transaction before committing? **Signal:** inspect
   affected scope and retain rollback option.

### Exit Options

- Give two different checks that could increase confidence in a join result.
- Translate relational difference into a SQL form and name one duplicate-related
  difference between mathematical relations and SQL tables.

## Week 3: Schema, Constraints, and Metadata

### Opening Retrieval

1. What bad state can a primary key prevent? **Signal:** duplicate or missing row
   identity.
2. What does a foreign key protect, and what does it not prove? **Signal:**
   referential existence, not full business correctness.
3. Name one reason to inspect metadata before changing a table. **Signal:** current
   constraints, types, dependencies, or indexes.

### Later Retrieval

1. Compare `NOT NULL`, `CHECK`, `UNIQUE`, and `FOREIGN KEY` by the kind of invalid
   state each rejects. **Signal:** distinct integrity roles.
2. Why is an expected failure useful evidence? **Signal:** proves a rule is
   enforced, not merely declared.
3. Why can an unnecessary index make a system worse? **Signal:** write, storage,
   and maintenance cost.

### Exit Options

- Name one rule that belongs in the database even if the application also checks
  it, and explain why.
- A constraint command succeeded. What test would show that it protects the
  intended rule?

## Week 4: Views and Safe Change

### Opening Retrieval

1. What is a view, and how can it stabilize an interface? **Signal:** named query
   and abstraction boundary.
2. Why should a migration have a precondition? **Signal:** verifies expected
   starting state.
3. Distinguish a reversible change from a destructive change. **Signal:** ability
   to restore prior behavior/data without unsupported assumptions.

### Later Retrieval

1. Put expand, migrate, verify, and contract in a safe order. **Signal:** additive
   compatibility before removal.
2. Why can renaming a column break clients even when the database accepts it?
   **Signal:** dependencies outside the table definition.
3. What should a postcondition prove? **Signal:** intended state and preserved
   behavior/data.

### Exit Options

- Write a five-line change record: precondition, change, verification, rollback,
  and remaining risk.
- Explain one situation in which a compatibility view is safer than an immediate
  client-wide rename.

## Week 5: Transactions, MVCC, and Locks

### Opening Retrieval

1. Distinguish commit and rollback. **Signal:** durable transaction versus
   discarded uncommitted work.
2. What does atomicity promise? **Signal:** transaction effects occur together or
   not at all, within the defined transaction.
3. Why are two database sessions needed to observe blocking? **Signal:** concurrent
   actors with independent transaction state.

### Later Retrieval

1. What can an open transaction retain even when a user appears idle? **Signal:**
   locks, snapshots, resources, or uncommitted changes.
2. Distinguish “slow” from “blocked.” **Signal:** work progressing versus waiting
   on another resource/transaction.
3. Name evidence that identifies both the waiting and blocking sessions. **Signal:**
   session/lock metadata and query/transaction context.

### Exit Options

- Write a neutral incident update with impact, evidence, mitigation, verification,
  and prevention.
- Why is terminating a database session a mitigation rather than a root-cause
  explanation?

## Week 6: Identity, Permissions, and Row-Level Security

### Opening Retrieval

1. Define least privilege as an actor-action-resource statement. **Signal:**
   minimum necessary scope.
2. Distinguish authentication and authorization. **Signal:** identity proof versus
   allowed action.
3. Why is a successful administrator query weak evidence about an application
   user's permissions? **Signal:** different execution identity and bypass scope.

### Later Retrieval

1. What two tests form a useful permission test pair? **Signal:** expected allow
   and expected deny.
2. How can a row-level policy differ from a table-level grant? **Signal:** same SQL
   action, restricted row visibility or modification.
3. Why must a service-role secret stay out of browser code and notebooks?
   **Signal:** privileged bearer credential exposure.

### Exit Options

- Write one minimal access rule and one test that would falsify your claim that it
  is minimal.
- Explain the relationship among Supabase Auth identity, PostgreSQL roles, token
  claims, and RLS without treating them as the same object.

## Week 7: Query Plans and Index Experiments

### Opening Retrieval

1. What is the difference between estimated and actual plan evidence? **Signal:**
   planner prediction versus measured execution.
2. What does a sequential scan mean, and why is it not automatically bad?
   **Signal:** full relation access can be cheapest for small/broad queries.
3. Why record a baseline before adding an index? **Signal:** comparison and causal
   claim.

### Later Retrieval

1. What do rows, loops, and execution time reveal together? **Signal:** work per
   node and repeated work.
2. Why might PostgreSQL ignore a valid index? **Signal:** cost estimate, selectivity,
   table size, statistics, or query shape.
3. Name two costs of keeping an index. **Signal:** writes, storage, cache,
   vacuum/maintenance, build time.

### Exit Options

- Complete: question, baseline, hypothesis, one change, remeasurement, decision.
- A query became faster once. What additional evidence would you need before
  claiming the index caused a durable improvement?

## Week 8: Backup, Restore, and Midterm Synthesis

### Opening Retrieval

1. Why is a backup file not yet recovery evidence? **Signal:** successful separate
   restore and behavioral verification required.
2. Distinguish RPO and RTO. **Signal:** tolerable data-loss window versus recovery
   duration objective.
3. Why restore to a different database? **Signal:** protects source and tests
   independence.

### Later Retrieval

1. What can a logical dump preserve, and what managed configuration may remain
   outside it? **Signal:** schema/data versus provider identity/network/settings.
2. Name five restore checks stronger than “the command exited successfully.”
   **Signal:** structure, counts/identity, types/constraints, relationships,
   meaningful behavior.
3. Why record tool and server versions? **Signal:** compatibility and
   reproducibility.

### Exit Options

- State one recovery promise, the artifact that supports it, the verification
  test, and one remaining risk.
- Identify the strongest and weakest evidence in your midterm package and explain
  why.

## Week 9: NoSQL History, Models, and JSON

### Opening Retrieval

1. Why did nonrelational systems emerge even though relational databases remained
   useful? **Signal:** workload/distribution/evolution tradeoffs, not replacement.
2. Match key-value, document, graph, and vector models to one suitable question
   each. **Signal:** workload-model fit.
3. Which JSON values are valid: string, number, Boolean, null, array, object?
   **Signal:** syntax and type inventory.

### Later Retrieval

1. Why can two different JSON structures both represent the same CSV relations?
   **Signal:** representation choices depend on access/update patterns.
2. What relationship information can be lost during careless CSV-to-JSON
   conversion? **Signal:** identity, cardinality, references, or provenance.
3. Distinguish Euclidean distance and cosine similarity in plain language.
   **Signal:** magnitude-sensitive geometric distance versus direction/orientation.

### Exit Options

- Choose one data-model family for a stated problem and name the question it makes
  easy plus the operation it makes harder.
- Show one valid embedded JSON design and one referenced design for the same two
  CSV tables; state one tradeoff.

## Week 10: MQL and Document Modeling

### Opening Retrieval

1. What is the MongoDB equivalent of choosing a database and collection before a
   query? **Signal:** database/collection context.
2. Distinguish a query filter from a projection. **Signal:** document selection
   versus returned fields.
3. Why can an array require `$elemMatch`? **Signal:** multiple conditions must
   apply to the same array element.

### Later Retrieval

1. When does embedding make a read easier? **Signal:** bounded related data read
   together.
2. When does referencing reduce update risk? **Signal:** shared/unbounded/
   independently changing source of truth.
3. What do `matchedCount` and `modifiedCount` prove differently? **Signal:** target
   found versus value changed.

### Exit Options

- Write one MQL filter for a nested field or array and state its expected result
  grain.
- Defend embedding or referencing using one read pattern, one update pattern, and
  one growth assumption.

## Week 11: Aggregation, Validation, and MongoDB Indexes

### Opening Retrieval

1. In an aggregation pipeline, why does stage order matter? **Signal:** each stage
   transforms the next stage's input and cost.
2. What does `$group` change about result grain? **Signal:** one output per group
   key rather than source document.
3. What bad state can schema validation reject? **Signal:** explicit document
   shape/type/value rule.

### Later Retrieval

1. Why place a selective `$match` early when semantics allow it? **Signal:** reduce
   downstream documents/work.
2. How can an index support a filter and sort? **Signal:** compound key order and
   query shape.
3. What evidence would justify keeping a MongoDB index? **Signal:** explain or
   measured workload evidence plus cost.

### Exit Options

- Describe one pipeline as input grain, stage-by-stage transformation, and output
  grain.
- Explain what validation protects, what it cannot repair, and how you would test
  one expected rejection.

## Week 12: Replication, Reliability, and MongoDB Recovery

### Opening Retrieval

1. Distinguish replication and backup. **Signal:** availability/current copies
   versus independent recoverable history/artifact.
2. What happens after a primary becomes unavailable in a healthy replica set?
   **Signal:** election/failover with limits, not zero interruption.
3. Why can an accidental delete replicate successfully? **Signal:** replication
   copies valid writes, including mistakes.

### Later Retrieval

1. What do write concern and read concern influence? **Signal:** acknowledgment
   durability and read consistency/visibility.
2. What does Canonical Extended JSON preserve that ordinary JSON may blur?
   **Signal:** BSON type information.
3. Which metadata may be absent from a document-only export? **Signal:** indexes,
   validators, users, network rules, and other configuration.

### Exit Options

- Rewrite “the cloud prevents data loss” as a testable promise with mechanism,
  failure case, and verification.
- Name a separate restore target and five checks that would convince you the
  restored MongoDB data is usable.

## Week 13: Capacity, Sharding, and Integration

### Opening Retrieval

1. Distinguish scaling up, read replication, partitioning, and sharding. **Signal:**
   resource, copy, local division, and distributed ownership differences.
2. What does `mongos` do? **Signal:** routes using cluster metadata and merges
   results.
3. Why might a monotonic ranged shard key create a write hotspot? **Signal:** new
   extreme values target one current range.

### Later Retrieval

1. Why is high cardinality insufficient for choosing a shard key? **Signal:**
   frequency, monotonicity, targeting, updates.
2. What tradeoff does hashed distribution make? **Signal:** even placement versus
   original-value range locality.
3. What makes a data import idempotent? **Signal:** stable key and upsert/conflict
   behavior or controlled reset.

### Exit Options

- Recommend “do not shard yet” or one candidate using measured cardinality,
  frequency, targeting, and a tradeoff.
- A script reports 75 inserts. Name three checks needed before calling the import
  trustworthy.

## Week 14: Polyglot Data and Incident Boundaries

### Opening Retrieval

1. What is a source of truth? **Signal:** authoritative owner for a fact, not just
   a copy.
2. Why can dual writes leave stores inconsistent? **Signal:** partial success and
   no single atomic boundary.
3. Distinguish stale data from incorrect source data. **Signal:** synchronization
   lag versus authoritative error.

### Later Retrieval

1. What evidence helps locate whether an incident begins in PostgreSQL, MongoDB,
   or synchronization code? **Signal:** per-boundary identifiers, timestamps,
   counts, logs, or queries.
2. When is a polyglot design justified? **Signal:** distinct workload advantage
   exceeds synchronization/operation cost.
3. Why should a repair name ownership before copying values? **Signal:** prevents
   repeated conflict and unclear correction direction.

### Exit Options

- Draw or describe a two-store data flow with source of truth, copy, identifier,
  failure point, and verification.
- Recommend consolidation or continued polyglot use with one workload benefit and
  two operating costs.

## Week 15: Synthesis, Portfolio, and Interviews

### Opening Retrieval

1. Name one artifact that proves each of these verbs: build, restrict, diagnose,
   recover. **Signal:** observable evidence, not self-rating.
2. What makes a technical README reproducible? **Signal:** purpose, environment,
   ordered steps, expected results, verification, limitations.
3. Why should an interview result include evidence? **Signal:** credible impact
   and reasoning.

### Later Retrieval

1. Use Situation-Task-Action-Result-Reflection to outline one course story.
   **Signal:** personal action, evidence, and learning.
2. What production limitation should accompany a classroom project claim?
   **Signal:** scope and uncertainty without dismissing the work.
3. How would you explain the difference between knowing a command and operating a
   system? **Signal:** observe, decide, verify, recover, communicate.

### Exit Options

- State one course claim you can make in an interview, the artifact supporting it,
  and the limitation you would disclose.
- Identify the next database skill you would build and the smallest artifact that
  could prove it.
