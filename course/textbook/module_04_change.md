# Safe Changes Are Planned and Verified

## Operating Question

How can a team change a database while limiting broken queries, bad data, long
locks, and changes that cannot be undone?

An application rarely stops existing when a new database requirement arrives.
Old clients continue to send requests, reports continue to run, and yesterday's
records must still mean what they meant yesterday. A migration is therefore a
transition between usable states, not merely the final `ALTER TABLE` statement.
We will use views and a newly required field to examine that transition, then
connect generated identifiers to what a transaction can and cannot roll back.

## Learning Outcomes

After this module, you can:

- use views to create a stable and limited query interface;
- explain identity columns and sequences without confusing them with row counts;
- inspect columns, constraints, views, and dependencies through metadata;
- plan a small migration using precheck, change, verification, and rollback; and
- apply an expand-migrate-contract pattern to a breaking change.

## A Database Change Has More Than One Audience

Adding a column may affect:

- existing rows that do not have a value;
- application code that selects or inserts columns;
- reports and views that depend on names or types;
- locks and query latency while the change runs;
- backup and recovery procedures;
- permissions and row-level policies; and
- people trying to understand the current schema.

The SQL statement is only one part of a migration. A professional change includes
intent, preconditions, execution, verification, and a response if the result is
wrong.

## Views Create a Query Interface

A view stores a query definition, not a separate copy of its result in the common
case.

This reading uses `chapter4_active_queue`. The classroom lab uses the separate
name `active_ticket_queue`, so you can run both examples without replacing one
with a different column layout. Chapter 6 reuses this reading's view.

```sql
CREATE OR REPLACE VIEW metro_support.chapter4_active_queue AS
SELECT
    t.ticket_id,
    t.category,
    t.priority,
    t.status,
    t.subject,
    t.opened_at,
    u.display_name AS assignee_name
FROM metro_support.tickets AS t
LEFT JOIN metro_support.users AS u
    ON u.user_id = t.assignee_id
WHERE t.status IN ('new', 'open', 'in_progress');
```

The view can:

- hide an underlying join;
- expose only approved columns;
- give a stable name to a common query; and
- separate a consumer's interface from some storage details.

A view is not automatically faster. PostgreSQL usually expands its query into the
outer query and plans the whole statement. A materialized view stores results and
requires refresh, which creates a freshness tradeoff.

### Follow a Read Through the View

On the full baseline, the active queue returns seven tickets, including the two
that do not yet have an assigned agent. The left join preserves those requests;
the `assignee_name` expression becomes null for them. The view does not turn
that null into a nonexistent user. An application can display "Unassigned" while
retaining the ticket's identity.

If we update a ticket's status to `resolved`, a subsequent ordinary view query
uses the current visible database state and stops including that ticket. There
is no separate queue table for us to synchronize. A materialized view is
different: it holds previously computed results, so an application needs a
refresh policy and an acceptable staleness limit. Both mechanisms can be useful,
but they have different meanings when someone asks whether the screen is current.

A view also does not automatically isolate secrets. Omitting email from a
reporting view helps define a narrower interface, but a role that can select
the underlying `users` table can still retrieve email directly. Chapter 6 tests
the combination of the view and the grants as the intended actor.

### Avoid `SELECT *` in Durable Views

Explicit columns make the contract visible. PostgreSQL expands `SELECT *` when
it defines a view: adding a base-table column later does **not** automatically
add that column to the existing view. However, recreating or replacing a view
from a `SELECT *` definition after the table changes can produce a different
interface. Naming the intended columns makes that review deliberate, especially
when the new column contains private information.

In PostgreSQL, `CREATE OR REPLACE VIEW` must preserve existing output column names,
order, and types, although it can append columns. Inserting a new column in the
middle of an established definition is not equivalent to appending it. A
consumer that depends on a name or position may break even if the new query
returns sensible values. For a genuinely incompatible interface, a separately
named version can let old and new consumers coexist while they migrate.

Ordering is another part of the contract to state explicitly. A view's rows are
not inherently in a guaranteed presentation order. A consumer that needs the
newest requests should request `ORDER BY opened_at DESC, ticket_id` in its own
query rather than infer an ordering from earlier observations.

## Identity Columns and Sequences Generate Values

An identity column asks PostgreSQL to generate a value, usually from a sequence:

```sql
CREATE TABLE metro_support.chapter4_change_notes (
    note_id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    change_name text NOT NULL,
    recorded_at timestamptz NOT NULL DEFAULT now()
);
```

Generated identifiers are not row counts. Gaps are normal because sequence values
may be consumed by rolled-back transactions, failed inserts, caching, or manual
allocation. Do not promise consecutive numbers or infer how many rows exist from
the largest identifier.

`chapter4_change_notes` is a reading-only practice table; the lab creates its own
`change_notes` table. Create this table once in your disposable course database.
If it already exists, inspect its rows rather than expecting a new sequence to
start at 1.

`GENERATED ALWAYS` resists explicit values unless overridden. `GENERATED BY
DEFAULT` permits an explicit value. Choose according to import and ownership
needs.

### Why a Rollback Leaves a Gap

Suppose the table above has just been created and its identity sequence has not
been used. Run this sequence against that practice table:

```sql
BEGIN;
INSERT INTO metro_support.chapter4_change_notes (change_name)
VALUES ('Initial view') RETURNING note_id;
COMMIT;

BEGIN;
INSERT INTO metro_support.chapter4_change_notes (change_name)
VALUES ('Rehearsal that will not be retained') RETURNING note_id;
ROLLBACK;

BEGIN;
INSERT INTO metro_support.chapter4_change_notes (change_name)
VALUES ('Approved revision') RETURNING note_id;
COMMIT;

SELECT note_id, change_name
FROM metro_support.chapter4_change_notes ORDER BY note_id;
```

The inserts return 1, 2, and 3, but the final table contains rows 1 and 3. The
second row was rolled back. Its sequence allocation was not. With multiple
sessions, reclaiming a number every time one transaction aborts would complicate
independent allocation. A sequence provides generated values without promising
an uninterrupted count of committed rows. The
[PostgreSQL sequence documentation](https://www.postgresql.org/docs/current/functions-sequence.html)
describes this non-rollback behavior.

The explicit commit boundaries matter when an editor sends this entire listing
as one batch. The first row must be committed before the rehearsal begins;
otherwise a client-side batch can place earlier statements in the transaction
that is later rolled back. Transaction boundaries are part of the example, not
just formatting.

On a table already used in a previous run, the exact numbers will be higher.
The interpretation remains the same: use `count(*)` to count rows, and use keys
to identify them. Requirements for consecutive invoice or receipt numbers need
a separately designed business process; an identity column is not that process.
Likewise, explicitly importing a large ID does not automatically advance the
underlying sequence to that value. Imports need a deliberate sequence check.

## Introspection Reveals the Actual State

Before changing an object, query the system that will be changed.

### Find Columns and Defaults

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'metro_support'
  AND table_name = 'tickets'
ORDER BY ordinal_position;
```

### Find Constraints

```sql
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'metro_support'
  AND table_name = 'tickets'
ORDER BY constraint_type, constraint_name;
```

### Find Views That Mention a Table

```sql
SELECT table_schema, table_name, view_definition
FROM information_schema.views
WHERE view_definition ILIKE '%metro_support.tickets%';
```

Text search is a useful first pass, not a complete dependency model. PostgreSQL
catalogs and tools can expose more precise dependencies. The key habit is to
inspect rather than assume.

## What a Migration Must Establish

For a small migration, be able to explain:

1. **Intent:** what user or operating need justifies the change?
2. **Precheck:** what must be true before execution?
3. **Change:** what ordered SQL creates the new state?
4. **Verification:** what proves structure and data are correct?
5. **Rollback or forward fix:** how will the team respond if verification fails?

Not every production migration can be rolled back instantly. A forward fix may be
safer after data has been transformed. State the boundary honestly.

## Worked Example: Add a Public Status Label Safely

Metro Support wants user-facing labels such as "In progress" while preserving the
machine value `in_progress`.

### Risky Approach

Rename or replace the stored values immediately. Existing queries, constraints,
and integrations may expect the old values.

### Expand

Add a view with a derived label while preserving the source column:

```sql
CREATE OR REPLACE VIEW metro_support.public_ticket_status AS
SELECT
    ticket_id,
    subject,
    status AS status_code,
    CASE status
        WHEN 'new' THEN 'New'
        WHEN 'open' THEN 'Open'
        WHEN 'in_progress' THEN 'In progress'
        WHEN 'resolved' THEN 'Resolved'
        WHEN 'closed' THEN 'Closed'
        ELSE 'Unknown'
    END AS status_label,
    opened_at,
    closed_at
FROM metro_support.tickets;
```

### Verify

```sql
SELECT status_code, status_label, count(*)
FROM metro_support.public_ticket_status
GROUP BY status_code, status_label
ORDER BY status_code;
```

Check that every known code has one intended label and that the total count equals
the base table count.

### Migrate Consumers

Update a report or application to read the view. Observe before removing or
renaming any old interface.

### Contract Later

Only after all consumers are confirmed should an obsolete interface be removed.
In this case, keeping both code and label is useful, so contraction may not be
needed.

## Transactional DDL Helps, but Locks Still Matter

Many PostgreSQL data-definition statements can run inside a transaction:

The next example rehearses the required-field change from the Week 4 lab. Begin
with the practice baseline before `source_channel` exists. Historical tickets
have no structured channel field. Some event notes mention mobile submission,
so it would be false to label every old ticket `web`. We use `unknown` to mean
that the structured value was not captured. More detailed backfilling would
require a reviewed, record-specific source.

```sql
BEGIN;
SET LOCAL lock_timeout = '2s';
SET LOCAL statement_timeout = '10s';

ALTER TABLE metro_support.tickets
ADD COLUMN source_channel text;

UPDATE metro_support.tickets
SET source_channel = 'unknown'
WHERE source_channel IS NULL;

ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_source_channel_allowed
CHECK (source_channel IN ('web', 'phone', 'mobile', 'unknown'));

ALTER TABLE metro_support.tickets
ALTER COLUMN source_channel SET DEFAULT 'unknown',
ALTER COLUMN source_channel SET NOT NULL;

-- Inspect before choosing COMMIT or ROLLBACK.
SELECT source_channel, count(*)
FROM metro_support.tickets
GROUP BY source_channel;

ROLLBACK;
```

The grouped result inside this rehearsal is `unknown`, 12. After rollback, the
new column and its constraint no longer exist. To retain the migration, repeat
the verified block and deliberately choose `COMMIT` instead. Do not run the
creation block repeatedly against an already migrated table.

The default has a particular purpose: an older client that inserts an explicit
list of the old columns can still create a row. Its omitted channel receives
`unknown`. An explicit null is different from an omitted field and fails the
new not-null rule. A new client should provide the actual channel. After all
writers are upgraded, we can reconsider whether the default still serves a
useful purpose. Adding a default is an application-compatibility decision, not
just a way to make an error disappear.

Rollback protects atomicity, but an `ALTER TABLE` may still acquire a strong lock
and block other work while the transaction remains open. Production-safe change
planning considers table size, lock duration, statement timeout, maintenance
windows, and compatibility with live clients.

### A Safer Pattern for Large Tables

For a required new value:

1. add a nullable column;
2. deploy writers that populate it;
3. backfill old rows in controlled batches;
4. verify no nulls remain;
5. add or validate a constraint; and
6. remove old behavior only after consumers migrate.

The exact feature support and lock behavior depend on the PostgreSQL version.
Consult current official documentation for a production plan.

### Before Commit and After Commit Are Different Repair Boundaries

During our small rehearsal, rollback restores the prior database state. After a
deployment commits and new mobile requests arrive, dropping `source_channel`
would erase newly collected facts. That may be technically possible but is not
an adequate recovery plan. A forward repair could correct the view definition
or writer behavior while retaining channel data.

The same distinction applies to a destructive transformation. If a script
replaces detailed values with a coarse category, reversing its SQL does not
reconstruct the discarded detail. Preserve a verified source or choose a
non-destructive transition when that information matters. A rollback plan must
describe the state and data it recovers, rather than merely name an opposite
command.

The timeouts in the classroom block are guardrails for this small experiment.
`lock_timeout` limits waiting to acquire a lock; `statement_timeout` limits a
statement's elapsed execution. A timeout can leave the current transaction
aborted, requiring rollback. Their appropriate production values depend on the
workload and operational policy. They do not make a long migration intrinsically
safe or eliminate the need to understand its locks.

## Verification Should Cover Structure and Meaning

Run the following checks while the migrated column exists, either inside the
rehearsal before its rollback or after an intentionally committed migration.
After rollback, the column's absence is the expected result.

Structural check:

```sql
SELECT column_name, is_nullable
FROM information_schema.columns
WHERE table_schema = 'metro_support'
  AND table_name = 'tickets'
  AND column_name = 'source_channel';
```

Data check:

```sql
SELECT count(*) AS missing_source_count
FROM metro_support.tickets
WHERE source_channel IS NULL;
```

Behavior check:

```sql
BEGIN;
INSERT INTO metro_support.tickets (
    ticket_id, requester_id, category, priority, status, subject, opened_at
) VALUES (
    1098, 101, 'parks', 'low', 'new', 'Old-client compatibility test', now()
)
RETURNING ticket_id, source_channel;
ROLLBACK;
```

With our compatibility default, this insert succeeds and returns `unknown` for
the channel. The rollback removes the test ticket. A second test that explicitly
supplies a null channel should fail the not-null rule. If we later remove the
default, this omitted-field insertion will fail too, so that change requires
knowing that old writers have been upgraded.

## Common Misconceptions

### "A successful migration statement proves the application is safe"

The structure may have changed while existing queries, permissions, or data are
wrong. Verify at multiple layers.

### "Sequences should never have gaps"

Sequences allocate values efficiently, not gapless business numbering. A primary
key or unique constraint enforces uniqueness in the stored table, including
against explicit values or later sequence resets.

### "A view is a backup"

A normal view stores a query definition. It depends on underlying objects and
does not preserve deleted data.

## Practice

For the assigned Week 4 labs, read **Views Create a Query Interface** through
**Introspection Reveals the Actual State** before Day 1. Before Day 2, read the
migration sections, especially the historical-channel and old-client examples.
The resolution-summary problem below is optional transfer practice.

Plan a change that adds `resolution_summary` for resolved or closed tickets.
Write:

1. the intent;
2. one data precheck;
3. an expand step;
4. two verification queries; and
5. a rollback or forward-fix decision.

Do not make the field required in the same step that creates it. Explain why.

## Retrieval and Transfer

1. What problem does a view solve that a base table does not?
2. Why can a generated identity value contain gaps?
3. Name the five parts of a small change record.
4. Why does transactional DDL not eliminate operational risk?
5. A new required column will be added to ten million rows. Which expand-migrate-
   contract steps reduce risk?

## Further Reading

- [PostgreSQL views](https://www.postgresql.org/docs/current/sql-createview.html)
- [PostgreSQL identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
- [PostgreSQL information schema](https://www.postgresql.org/docs/current/information-schema.html)
- [PostgreSQL `ALTER TABLE`](https://www.postgresql.org/docs/current/sql-altertable.html)
- [Supabase database migrations](https://supabase.com/docs/guides/deployment/database-migrations)
