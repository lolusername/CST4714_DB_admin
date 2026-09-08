# Retrieval and Exit Prompt Bank

## How to Use This Bank

These are short, ungraded learning prompts, not additional assignments. Select
three retrieval prompts near the start of a meeting and one exit prompt near the
end. Students should first answer from memory, then compare reasoning with the
module, a worked example, or live feedback.

The prompts deliberately return to earlier ideas. That spacing helps students
retrieve SQL, diagnosis, security, and recovery concepts after the week in which
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
  possibility, and the first observation you would inspect.
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
2. What does a foreign key protect, and what does it not establish? **Signal:**
   referential existence, not full business correctness.
3. Name one reason to inspect metadata before changing a table. **Signal:** current
   constraints, types, dependencies, or indexes.

### Later Retrieval

1. Compare `NOT NULL`, `CHECK`, `UNIQUE`, and `FOREIGN KEY` by the kind of invalid
   state each rejects. **Signal:** distinct integrity roles.
2. Why is an expected failure a useful test? **Signal:** demonstrates that a rule is
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
3. What should a postcondition check? **Signal:** intended state and preserved
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
3. Name observations that identify both the waiting and blocking sessions. **Signal:**
   session/lock metadata and query/transaction context.

### Exit Options

- Write a neutral incident update with impact, observations, mitigation, verification,
  and prevention.
- Why is terminating a database session a mitigation rather than a root-cause
  explanation?

## Week 6: Identity, Permissions, and Row-Level Security

### Opening Retrieval

1. Define least privilege as an actor-action-resource statement. **Signal:**
   minimum necessary scope.
2. Distinguish authentication and authorization. **Signal:** identity proof versus
   allowed action.
3. Why does a successful administrator query not establish an application
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

1. What is the difference between an estimated plan and actual execution measurements? **Signal:**
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
- A query became faster once. What additional measurements would you need before
  claiming the index caused a durable improvement?

## Week 8: Backup, Restore, and Midterm Synthesis

### Opening Retrieval

1. Why is a backup file not yet a usable recovery process? **Signal:** successful separate
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
- Identify the strongest and weakest checks in your midterm package and explain
  why.
