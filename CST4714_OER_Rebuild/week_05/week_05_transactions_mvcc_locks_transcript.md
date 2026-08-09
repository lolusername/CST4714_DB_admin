# Week 5: Transactions, MVCC, and Lock Evidence - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Transactions, MVCC, and Lock Evidence

This week introduces the point at which a database stops looking like one sequence of commands. Two sessions can read and write at the same time, hold different transaction state, and wait on one another. The visible symptom may be ‘the query is slow,’ while the actual cause is an open transaction holding a lock.

We will first predict commit and rollback outcomes. Then we will use a controlled two-session incident to connect ACID, MVCC, locks, waiting evidence, mitigation, and verification. The goal is not to memorize every lock mode. The goal is to identify which session is waiting, which session owns the conflicting work, and what evidence supports a safe response.

## Slide 2: ACID names transaction properties, not unlimited guarantees

Atomicity means the effects inside the transaction boundary commit together or are rolled back. It does not combine actions that were never placed in the same transaction. Consistency is often misunderstood as ‘the database always contains correct facts.’ The engine enforces declared rules and transaction semantics; applications can still commit logically wrong but valid data.

Isolation controls how concurrent transactions observe and affect one another, with behavior determined by the isolation level and operations. Durability means acknowledged committed effects survive the failures covered by the database's mechanisms and configuration. It is not the same as backup, geographic resilience, or immunity from an authorized delete. Precise scope makes the acronym useful.

## Slide 3: A transaction moves through observable states

An explicit transaction begins with `BEGIN`. Reads and writes occur under a transaction snapshot and acquire locks as needed. The exact snapshot and visibility behavior depend on the isolation level. Inside the transaction, the session can inspect its own uncommitted changes.

`COMMIT` completes the transaction and makes its effects durable according to the database configuration. `ROLLBACK` discards uncommitted changes. Closing a browser tab or query editor is not the conceptual transaction command, even if a client eventually disconnects and the server rolls back. An idle session can remain inside a transaction, retaining locks or an old snapshot. Operational evidence must come from server transaction state, not from whether a human appears active.

## Slide 4: Predict commit and rollback before running the commands

The first session updates ticket 1002 inside an explicit transaction. That session sees its own new priority when it selects the row. Another session's observation depends on isolation and whether the first transaction has committed. Under the usual read-committed behavior, the second session continues to see the last committed version until the update commits, although a conflicting write may wait.

If the first session commits, the new value becomes the current committed version. If it rolls back, the uncommitted version disappears and the previous value remains. Predict all three observations before running the sequence. This separates transaction state from interface behavior and makes later blocking evidence easier to interpret.

## Slide 5: Two sessions can hold different state at the same moment

Session A and Session B have independent connections and transaction state. Session A can update ticket 1002 and leave the transaction open. PostgreSQL retains the uncommitted row version and a row-level lock that protects conflicting changes.

Session B may still read the last committed version because MVCC allows many readers to avoid waiting on writers. If Session B attempts a conflicting update, it may wait for Session A to commit or roll back. This is why ‘MVCC means there are no locks’ is incorrect. MVCC improves concurrency by managing versions and visibility, while locks still coordinate conflicting operations and schema changes.

## Slide 6: Lab 1: Predict and verify transaction outcomes

Complete this lab individually using two clearly labeled sessions when available. Before running each case, write the predicted value inside Session A, the predicted value in Session B, and the final value after completion.

Run one commit case and one rollback case on the disposable ticket row. Use stable identifiers and copied query output. If a second live connection is unavailable, the lab's static transcript supports the same predictions. Submit one record that compares prediction and observation. State the isolation assumption and do not interpret a browser window as transaction evidence.

## Slide 7: A waiting query and an expensive query need different responses

On the second day, we investigate a controlled blocking incident. A query can take a long time because it is performing expensive work, because it is waiting for another transaction, or because both conditions occur. Those causes require different evidence and different mitigations.

We will identify the waiting session and the blocking session using PostgreSQL activity and lock information. We will also inspect transaction age and query text. The response is not automatically to terminate the blocker. First establish ownership, impact, and whether commit, rollback, cancellation, or termination is safe. Then verify that the waiting work progresses and document why the transaction remained open.

## Slide 8: MVCC reduces some conflicts; locks still protect coordination

Multi-version concurrency control gives transactions a visibility rule over row versions. A reader can often see a committed version while another transaction holds an uncommitted update. That reduces reader-writer blocking and supports consistent snapshots under the selected isolation level.

Locks remain necessary. Two transactions cannot both finalize incompatible updates to the same row without coordination. Table and schema operations also need stronger locking. Old row versions require vacuum cleanup, and long-running transactions can delay that cleanup. MVCC and locks are not competing explanations. They work together: versions control visibility, while locks coordinate operations that cannot safely proceed at the same time.

## Slide 9: Slow work consumes resources; blocked work waits

A slow query may be actively doing large amounts of work. Its plan, buffers, row counts, CPU, and elapsed time help locate the cost. A blocked query is different: it cannot proceed until another owner releases a conflicting resource.

Adding an index does not release a lock. Terminating a blocker does not make an inherently expensive query efficient. Begin with activity and wait evidence. If the session is waiting on a lock, identify the blocker and its transaction state. If it is active, inspect its plan and workload. Real incidents can include both: a query performs work and later waits. The evidence should separate phases rather than forcing one label.

## Slide 10: PostgreSQL can identify waiting and blocking sessions

`pg_stat_activity` reports current session state, wait information, transaction and query start times, and query text subject to permissions. `pg_blocking_pids(pid)` returns process identifiers that block the selected session. Together, the queries can identify a waiting session and candidate blockers.

A process identifier is not an explanation. Inspect whether the blocker is active, idle in transaction, or performing expected work. Review transaction age, application name where available, and the affected operation. Query text may contain sensitive values, so handle and redact evidence appropriately. Never terminate a session in a shared environment simply because its PID appears in a result. Establish impact and ownership first.

## Slide 11: A blocking incident record separates response from diagnosis

The incident record begins with impact because not every lock wait is harmful. State which user action or service promise is affected. Evidence then identifies the waiter, blocker, wait type, transaction age, and relevant query or application context.

Mitigation restores service. The safest choice may be asking the owner to commit or roll back. Cancellation or termination requires authority and an understanding of uncommitted work. Verification proves that the waiter proceeds and checks the resulting data state. Prevention addresses the lifecycle: shorter transactions, explicit completion, lock timeout, a smaller batch, application retry design, or monitoring for idle-in-transaction sessions. Mitigation is not the root cause by itself.

## Slide 12: Lab 2: Diagnose a controlled blocking incident

Complete the incident individually in the course fixture or the notebook's static fallback. Do not create blocking in a shared production table. Label both sessions and record the expected blocking operation before running it.

Identify the waiting PID, blocking PID, wait event, transaction start, and relevant query. Choose mitigation based on ownership and the disposable context. Verify that the waiting command completes or is safely canceled and inspect the ticket value afterward. Submit one neutral status update with impact, evidence, mitigation, verification, and prevention. Avoid blaming a person or claiming certainty beyond the observed transaction state.

## Slide 13: Concurrency becomes manageable when state and ownership are visible

This week connected transactions, MVCC, locks, and incident response. Transactions define commit and rollback boundaries. MVCC controls visibility across row versions. Locks coordinate operations that cannot proceed together. A session can appear idle to a person while remaining open on the server and retaining important state.

A useful incident response distinguishes an expensive query from a waiting query, identifies the waiter and blocker, establishes ownership, chooses a safe mitigation, and verifies both progress and data. Next week we will apply the same identity and evidence discipline to permissions and row-level security. The central question will change from ‘who is blocking?’ to ‘who should be allowed to do what?’

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
