# Transactions Coordinate Competing Work

## Operating Question

When two sessions read and change the same data, how can we predict what each
session sees, identify who is waiting, and resolve the situation without guessing?

## Learning Outcomes

After this module, you can:

- define a transaction boundary and demonstrate `COMMIT` and `ROLLBACK`;
- connect atomicity, consistency, isolation, and durability to observable behavior;
- explain snapshots and row versions at a beginner level;
- distinguish normal waiting, blocking, and deadlock;
- use PostgreSQL activity and blocking state to identify session relationships;
  and
- resolve a controlled blocking incident safely and verify the result.

## A Transaction Is a Unit of Decision

A transaction groups database statements into one unit that either commits or
rolls back.

Consider a repair desk assigning an unassigned request to Noah. The application
needs to change the ticket's current assignee and add an event saying who made
that change. If the ticket update succeeds but the history insert fails, the
current state and the history disagree. Each statement can be valid SQL, and
each table can satisfy its own constraints, while the application operation is
still incomplete. A transaction lets the application define that larger unit.

Start with the smaller boundary below. It uses the supplied Metro Support data
and ends with rollback so reading the example does not permanently change the
fixture. Run the block as a whole in your own practice database.

```sql
BEGIN;

UPDATE metro_support.tickets
SET assignee_id = 202,
    status = 'in_progress'
WHERE ticket_id = 1004
RETURNING ticket_id, assignee_id, status;

ROLLBACK;
```

Many clients use **autocommit**: each statement becomes its own transaction unless
you explicitly begin one. An explicit transaction creates a review point, but it
also keeps locks and snapshots alive until the transaction ends. "I forgot to
commit" is operationally meaningful.

The `RETURNING` row is visible to the transaction that made the change. It is not
a commit receipt. After this block, a fresh query should still show ticket 1004
as unassigned and `new`. Replacing the last statement with `COMMIT` keeps the
change, but only do that when the exercise asks for it. The Day 1 lab works in
separate disposable copies so its committed example does not alter this source.

### Keeping State and History Together

This second example adds the history event. It assumes the original fixture:
ticket 1004 is `new` and event 5998 does not exist.

```sql
BEGIN;

UPDATE metro_support.tickets
SET assignee_id = 202, status = 'in_progress'
WHERE ticket_id = 1004 AND status = 'new'
RETURNING ticket_id, assignee_id, status;

INSERT INTO metro_support.ticket_events
    (event_id, ticket_id, actor_id, event_type, old_status,
     new_status, note, event_at)
VALUES
    (5998, 1004, 202, 'status_changed', 'new',
     'in_progress', 'Assigned to Noah for follow-up', now());

SELECT event_id, ticket_id, new_status
FROM metro_support.ticket_events WHERE event_id = 5998;
ROLLBACK;
```

Inside the transaction, both changes can be inspected. Outside it after rollback,
neither remains. If the insert violates a constraint, PostgreSQL reports an error
and the transaction enters a failed state. End it with `ROLLBACK`; do not keep
issuing ordinary statements and assume that the earlier update committed.

There is an important boundary to this protection. An `UPDATE` matching zero rows
is **not** an SQL error. A real application must check that the intended ticket
was changed before accepting the history event and committing. The `status =
'new'` condition protects the proposed transition, but it does not automatically
tell later application code to stop when the condition matches nothing. The
database cannot infer the meaning of "assign this previously unassigned request"
from an arbitrary list of successful statements.

### What Rollback Does Not Undo

Rollback covers transactional database changes. It does not retract an email
already sent, undo an external API call, or reclaim every sequence value. Chapter
4's identity example showed a sequence gap after rollback. Chapter 14 returns to
external messages: an application must coordinate them with database commits
rather than assume that a transaction spans every service it calls.

A rollback should be verified, not merely assumed. Figure 5.1 shows a reversible
browser exercise that creates a temporary table, inserts one row, rolls the
transaction back, and then asks PostgreSQL whether the temporary relation still
exists. The returned `true` means `to_regclass(...) IS NULL`: the relation is no
longer present.

![Figure 5.1: A Supabase SQL Editor transaction test verifies that rollback removed the temporary relation. The query changes no persistent course data. Account identifiers are redacted. Interface captured August 25, 2026.](figures/cloud_interfaces/supabase_sql_rollback.png){#fig-supabase-rollback width=68%}

This is stronger than a green "success" message because the final `SELECT`
checks the postcondition independently. Supabase may still display a heuristic
RLS warning for a `CREATE TABLE` statement; in this controlled example the table
is temporary and the transaction is rolled back. A persistent application table
would require an explicit access-policy decision.

## ACID Describes Guarantees, Not a Product Label

### Atomicity

All changes in a transaction commit together or none remain. If assigning a
ticket and recording its event must be one operation, put them in one transaction.

### Consistency

A transaction moves the database between states that satisfy enforced rules.
Consistency is not magic correctness: the database can enforce only the
constraints and transaction logic it has been given.

In this use of the word, consistency means maintaining application invariants,
such as a valid ticket status and a matching history event. Later chapters use
"consistency" when comparing observations across replicas. The same word refers
to different questions; a valid state is not automatically an immediately visible
state on every machine.

### Isolation

Concurrent transactions behave according to an isolation model. Isolation does
not always mean that every transaction runs as though completely alone. Different
levels permit different observations and may require retries.

### Durability

After a successful commit, the DBMS promises the change survives failures within
its documented durability model. Durability is not the same as indefinite
retention or protection from an authorized later deletion. Backups and recovery
still matter.

## Concurrency Creates Useful Work and New Questions

Without concurrency, a database would waste time while one client thinks,
communicates, or waits for input. With concurrency, two sessions may:

- read the same row;
- update different rows;
- compete to update the same row;
- make decisions from different snapshots; or
- acquire resources in opposite orders.

Common anomaly names include dirty read, nonrepeatable read, phantom, lost update,
and serialization anomaly. PostgreSQL's implementation and isolation levels
determine which can occur. The practical questions are:

1. what did each transaction read?
2. what did each transaction change?
3. which transaction is waiting, and on whom?
4. which outcome can the application accept?

The names become useful when attached to a situation. A **dirty read** would show
another transaction's uncommitted assignment. A **nonrepeatable read** shows an
old assignment on one query and a newly committed assignment on a later query.
A **phantom** concerns the membership of a result: the next active-ticket query
includes a newly committed request. These are not all the same error. For a live
queue, seeing a newly committed ticket may be exactly what the application wants.
For two parts of one financial report, changing the visible data between queries
may be unacceptable.

## MVCC Lets Readers and Writers Coexist

PostgreSQL uses multi-version concurrency control, or MVCC. An update creates a
new row version rather than overwriting the only copy in place. A transaction
reads versions visible to its snapshot.

This design often allows readers and writers to proceed without blocking one
another. It does not mean there are no locks. Writers competing for the same row
can wait, schema changes can take strong locks, and long transactions can prevent
old row versions from being cleaned up.

`VACUUM` helps reclaim or mark reusable space from obsolete versions and supports
transaction-ID safety. Routine vacuuming is normal database maintenance; it does
not by itself mean that PostgreSQL is broken.

Think of a row version as a value with visibility conditions, not a second ticket
the user should count. While Noah's assignment is uncommitted, an ordinary reader
can still see the previously committed ticket. After commit, a later snapshot can
see the new version. Old snapshots may still need the old version, which is one
reason a long-running transaction can interfere with cleanup even if it is not
actively changing rows. MVCC is not a built-in historical reporting API: obsolete
versions are eventually reclaimed rather than kept as a permanent event history.

## Isolation Levels Change Visibility and Retry Behavior

PostgreSQL supports:

- **Read Committed**, the default: each statement receives a snapshot at statement
  start. Two selects in one transaction may see different committed data.
- **Repeatable Read:** the transaction keeps a stable snapshot for ordinary
  reads; conflicting patterns may produce an error rather than an inconsistent
  result.
- **Serializable:** PostgreSQL attempts behavior equivalent to some serial order;
  applications must be prepared to retry serialization failures.

PostgreSQL treats Read Uncommitted as Read Committed. Do not infer behavior only
from a generic isolation-level chart; consult the DBMS documentation.

Stronger isolation is not simply "better." It can increase coordination,
abort/retry behavior, and application complexity. Choose based on the invariant.

### Read the Same Row Twice

Here is a reasoning example, not an instruction to leave browser sessions open.
Both sessions start from ticket 1004 with priority `low`.

| Order | Session A | Session B |
|---:|---|---|
| 1 | begins a transaction and reads `low` | not yet changing the row |
| 2 | remains open | changes priority to `high` and commits |
| 3 | reads the same ticket again | has finished |
| 4 | ends its transaction | has finished |

With PostgreSQL Read Committed, A's second read can show `high`: the second
statement gets a new snapshot. With Repeatable Read, A's ordinary second read
still shows `low`: its transaction uses the snapshot established by its first
non-control statement. B's commit was not lost; it is simply outside A's snapshot.
A new transaction can see it. If A now tries to update a row changed since that
Repeatable Read snapshot, a serialization failure may require A to retry.
[PostgreSQL isolation behavior](https://www.postgresql.org/docs/current/transaction-iso.html)

### A Stable Snapshot Is Not Every Business Rule

Suppose Priya and Noah are both on call, and the rule is "at least one agent must
remain on call." Each transaction reads that the other agent is available and
then changes only its own agent to off call. Under snapshot isolation, the writes
can target different rows and both commit, leaving nobody on call. There was no
dirty read, and each transaction's view was stable, but the shared rule failed.
This pattern is called **write skew**.

The point is not to memorize another name. Identify whether the rule concerns
one row or a relationship among several decisions. A design can coordinate on a
shared locked record or use serializable transactions with a retry path. The
right choice depends on the actual invariant. Merely adding `BEGIN` and `COMMIT`
around a read-then-write program does not establish serial execution.

## Waiting Is a Relationship Between Sessions

If Session A updates ticket 1004 and remains open, Session B's attempt to update
the same row waits. Session B is blocked; Session A is the blocker.

Waiting can be correct: competing row writes must coordinate. It does not by
itself prevent a stale application value from overwriting a newer value after
the wait ends. The problem may be an unexpectedly long wait, an unknown
transaction, or a write that no longer satisfies the application's condition.

The two-session SQL below explains the mechanism. Use it only with two persistent
connections to a disposable practice database and release Session A promptly.
Separate web-editor tabs are not guaranteed to represent persistent independent
database sessions. For the assigned exercise,
[Notebook 02](../notebooks/02_postgres_transactions_locks.ipynb) creates the wait,
captures it, and releases it within one cell. Reading its output does not leave
another query blocked.

### Session A

```sql
BEGIN;

UPDATE metro_support.tickets
SET priority = 'high'
WHERE ticket_id = 1004;

-- Leave this transaction open only during the controlled lab.
```

### Session B

```sql
BEGIN;
SET LOCAL statement_timeout = '15s';
UPDATE metro_support.tickets
SET status = 'in_progress'
WHERE ticket_id = 1004;
COMMIT;
```

Session B waits because the target row is already being changed by the uncommitted
transaction in Session A.

If Session B times out, issue `ROLLBACK` in B and release A before retrying the
exercise. A timeout is a bound on waiting, not evidence that the blocking
transaction was automatically removed.

## Diagnose From a Third Session

`pg_stat_activity` exposes server processes and current activity. Access may be
limited by role and managed-service policy.

```sql
SELECT
    pid,
    usename,
    state,
    wait_event_type,
    wait_event,
    xact_start,
    query_start,
    left(query, 100) AS query_sample
FROM pg_stat_activity
WHERE datname = current_database()
ORDER BY xact_start NULLS LAST, query_start;
```

Use `pg_blocking_pids` to ask PostgreSQL for the relationship:

```sql
SELECT
    blocked.pid AS blocked_pid,
    blocked.wait_event_type,
    blocked.wait_event,
    pg_blocking_pids(blocked.pid) AS blocking_pids,
    left(blocked.query, 100) AS blocked_query
FROM pg_stat_activity AS blocked
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;
```

The process identifier is a diagnostic clue, not permission to terminate a session. First
identify the user, transaction age, query, application, impact, and owner.

## Worked Example: Resolve the Controlled Block

1. Confirm that Session B is waiting and record its PID.
2. Record the blocking PID returned by `pg_blocking_pids`.
3. Return to Session A and decide whether its change is valid.
4. Use `ROLLBACK` in the controlled lab to release the row lock without keeping
   the priority change.
5. Observe Session B finish.
6. Query ticket 1004 from a fresh session and record the final priority and status.

The final state proves which change remained. The activity view proves the
blocking relationship. Neither alone tells the complete incident story.

## Deadlock Is Different From One-Way Blocking

A deadlock forms a cycle: Session A holds something Session B needs while Session
B holds something Session A needs. Neither can proceed. PostgreSQL detects the
cycle and aborts one transaction so the other can continue.

Applications should handle the error and retry the entire transaction when safe.
Design can reduce deadlocks by touching resources in a consistent order and
keeping transactions short.

Do not create uncontrolled deadlocks in a shared environment. A controlled
two-row exercise belongs in a dedicated practice schema with explicit cleanup.

## Safe Incident Communication

A useful update separates observation from inference:

> Ticket updates are waiting. At 14:12 UTC, PID 8124 was waiting on a transaction
> lock and `pg_blocking_pids` identified PID 8071. The blocking transaction began
> at 14:06 UTC from the course SQL editor. We rolled back the controlled Session A
> change, Session B completed, and a fresh query confirmed ticket 1004 is
> `in_progress` with its original priority. We will add a transaction timeout and
> shorten the workflow before repeating the test.

Avoid "the database froze" when the system views show one lock relationship.

## Common Misconceptions

### "Readers never block and writers never wait under MVCC"

MVCC reduces many read/write conflicts. Row writes, explicit locks, and schema
changes can still block.

### "The oldest query is always the blocker"

Age is a clue. Use blocking relationships and lock state, not age alone.

### "Killing the blocked session fixes the cause"

The blocked session is the waiter. Terminating it may remove the symptom while
the blocking transaction remains open.

### "Serializable means no errors"

Serializable execution can abort a transaction to preserve the guarantee. Correct
applications expect and safely retry those failures.

## Study and Practice

The [Week 5 guide](../weeks/week_05/README.md) identifies assigned reading and
links the required individual labs. The following timeline is optional
self-study, not an additional report.

Draw a timeline for Session A and Session B in the worked example. Mark:

- transaction start;
- snapshot or statement reads;
- row update;
- wait start;
- rollback; and
- final verification.

Then write one query you would run in the third session and one conclusion it can
support.

## Retrieval and Transfer

1. Why can an explicit transaction be both safer and riskier than autocommit?
2. What does MVCC mean for row updates?
3. How does one-way blocking differ from deadlock?
4. Which function directly identifies PostgreSQL blocking PIDs?
5. Why must a serializable application be able to retry?
6. What final check proves which ticket state remained after the incident?

## Further Reading

- [PostgreSQL transactions](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html)
- [PostgreSQL monitoring statistics](https://www.postgresql.org/docs/current/monitoring-stats.html)
- [PostgreSQL routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html)
