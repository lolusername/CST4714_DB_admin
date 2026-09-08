# Module 5: Transactions Coordinate Competing Work

## Operating Question

When two sessions read and change the same data, how can we predict what each
session sees, identify who is waiting, and resolve the situation without guessing?

## Learning Outcomes

After this module, you can:

- define a transaction boundary and demonstrate `COMMIT` and `ROLLBACK`;
- connect atomicity, consistency, isolation, and durability to observable behavior;
- explain snapshots and row versions at a beginner level;
- distinguish normal waiting, blocking, and deadlock;
- use PostgreSQL activity and blocking evidence to identify session relationships;
  and
- resolve a controlled blocking incident safely and verify the result.

## 1. A Transaction Is a Unit of Decision

A transaction groups database statements into one unit that either commits or
rolls back.

```sql
BEGIN;

UPDATE metro_support.tickets
SET assignee_id = 202,
    status = 'in_progress'
WHERE ticket_id = 1004
RETURNING ticket_id, assignee_id, status;

-- Choose one after verification.
COMMIT;
-- ROLLBACK;
```

Many clients use **autocommit**: each statement becomes its own transaction unless
you explicitly begin one. An explicit transaction creates a review point, but it
also keeps locks and snapshots alive until the transaction ends. "I forgot to
commit" is operationally meaningful.

## 2. ACID Describes Guarantees, Not a Product Label

### Atomicity

All changes in a transaction commit together or none remain. If assigning a
ticket and recording its event must be one operation, put them in one transaction.

### Consistency

A transaction moves the database between states that satisfy enforced rules.
Consistency is not magic correctness: the database can enforce only the
constraints and transaction logic it has been given.

### Isolation

Concurrent transactions behave according to an isolation model. Isolation does
not always mean that every transaction runs as though completely alone. Different
levels permit different observations and may require retries.

### Durability

After a successful commit, the DBMS promises the change survives failures within
its documented durability model. Durability is not the same as indefinite
retention or protection from an authorized later deletion. Backups and recovery
still matter.

## 3. Concurrency Creates Useful Work and New Questions

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

## 4. MVCC Lets Readers and Writers Coexist

PostgreSQL uses multi-version concurrency control, or MVCC. An update creates a
new row version rather than overwriting the only copy in place. A transaction
reads versions visible to its snapshot.

This design often allows readers and writers to proceed without blocking one
another. It does not mean there are no locks. Writers competing for the same row
can wait, schema changes can take strong locks, and long transactions can prevent
old row versions from being cleaned up.

`VACUUM` helps reclaim or mark reusable space from obsolete versions and supports
transaction-ID safety. Routine vacuuming is normal database maintenance, not
evidence that PostgreSQL is broken.

## 5. Isolation Levels Change Visibility and Retry Behavior

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

## 6. Waiting Is a Relationship Between Sessions

If Session A updates ticket 1004 and remains open, Session B's attempt to update
the same row waits. Session B is blocked; Session A is the blocker.

Waiting can be correct. It prevents two writers from silently overwriting the same
row version. The problem is an unexpectedly long wait, an unknown transaction,
or an impact that violates the service objective.

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
UPDATE metro_support.tickets
SET status = 'in_progress'
WHERE ticket_id = 1004;
```

Session B waits because the target row is already being changed by the uncommitted
transaction in Session A.

## 7. Diagnose From a Third Session

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

The process identifier is evidence, not permission to terminate a session. First
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

## 8. Deadlock Is Different From One-Way Blocking

A deadlock forms a cycle: Session A holds something Session B needs while Session
B holds something Session A needs. Neither can proceed. PostgreSQL detects the
cycle and aborts one transaction so the other can continue.

Applications should handle the error and retry the entire transaction when safe.
Design can reduce deadlocks by touching resources in a consistent order and
keeping transactions short.

Do not create uncontrolled deadlocks in a shared environment. A controlled
two-row exercise belongs in a dedicated practice schema with explicit cleanup.

## 9. Safe Incident Communication

A useful update separates observation from inference:

> Ticket updates are waiting. At 14:12 UTC, PID 8124 was waiting on a transaction
> lock and `pg_blocking_pids` identified PID 8071. The blocking transaction began
> at 14:06 UTC from the course SQL editor. We rolled back the controlled Session A
> change, Session B completed, and a fresh query confirmed ticket 1004 is
> `in_progress` with its original priority. We will add a transaction timeout and
> shorten the workflow before repeating the test.

Avoid "the database froze" when the evidence shows one lock relationship.

## Common Misconceptions

### "Readers never block and writers never wait under MVCC"

MVCC reduces many read/write conflicts. Row writes, explicit locks, and schema
changes can still block.

### "The oldest query is always the blocker"

Age is a clue. Use blocking relationships and lock evidence, not age alone.

### "Killing the blocked session fixes the cause"

The blocked session is the waiter. Terminating it may remove the symptom while
the blocking transaction remains open.

### "Serializable means no errors"

Serializable execution can abort a transaction to preserve the guarantee. Correct
applications expect and safely retry those failures.

## Practice

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

- PostgreSQL transactions: <https://www.postgresql.org/docs/current/tutorial-transactions.html>
- PostgreSQL transaction isolation: <https://www.postgresql.org/docs/current/transaction-iso.html>
- PostgreSQL explicit locking: <https://www.postgresql.org/docs/current/explicit-locking.html>
- PostgreSQL monitoring statistics: <https://www.postgresql.org/docs/current/monitoring-stats.html>
- PostgreSQL routine vacuuming: <https://www.postgresql.org/docs/current/routine-vacuuming.html>
