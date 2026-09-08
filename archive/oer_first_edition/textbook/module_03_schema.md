# Module 3: A Schema Protects Meaning

## Operating Question

Which invalid states should the database refuse, even when an application has a
bug or a user imports a bad file?

## Learning Outcomes

After this module, you can:

- use PostgreSQL schemas as namespaces and permission boundaries;
- choose basic data types, primary keys, and foreign keys;
- apply `NOT NULL`, `UNIQUE`, `CHECK`, and referential actions intentionally;
- distinguish an integrity constraint from an index; and
- inspect database metadata instead of relying on memory.

## 1. "Schema" Has Two Related Meanings

A database schema can mean the overall structure of data: tables, columns,
relationships, constraints, and indexes. In PostgreSQL, a *schema* is also a named
namespace inside a database. `metro_support.tickets` identifies the `tickets`
table in the `metro_support` namespace.

Namespaces help:

- separate application objects from extensions or shared utilities;
- avoid name collisions;
- organize permissions; and
- make object ownership explicit.

PostgreSQL resolves unqualified names through `search_path`. In durable scripts,
schema-qualified names reduce ambiguity:

```sql
SELECT ticket_id, status
FROM metro_support.tickets;
```

## 2. Data Types Express Allowed Representation

A data type is the first integrity decision. Choose a type that represents the
domain and supports required operations.

| Need | Common PostgreSQL type | Reasoning |
|---|---|---|
| whole-number identifier | `integer` or `bigint` | numeric identity, efficient equality |
| arbitrary text | `text` | no invented length limit |
| exact money/measurement | `numeric(p,s)` | decimal precision rather than binary approximation |
| yes/no state | `boolean` | avoids multiple spellings |
| instant in time | `timestamptz` | stores an instant and converts display zones |
| calendar date | `date` | no implied time of day |
| structured flexible attribute | `jsonb` | queryable JSON when a relational column is not appropriate |

Do not choose a type only because the current sample fits. Ask what values should
exist and what operations must be correct.

## 3. Keys Identify and Connect Facts

A **primary key** uniquely identifies a row and is not null. A **foreign key**
requires a value to match a key in another table, unless the foreign-key column is
allowed to be null.

```sql
CREATE TABLE metro_support.tickets (
    ticket_id integer PRIMARY KEY,
    requester_id integer NOT NULL
        REFERENCES metro_support.users(user_id),
    assignee_id integer
        REFERENCES metro_support.users(user_id)
);
```

The nullable `assignee_id` represents a real state: a ticket may be unassigned.
The non-null `requester_id` states that every ticket must have a known requester.

### Referential Actions Are Business Decisions

What should happen if a user row is deleted?

- `RESTRICT` or `NO ACTION`: refuse deletion while dependent rows exist.
- `CASCADE`: delete or update dependent rows automatically.
- `SET NULL`: preserve the dependent row but remove the reference.

There is no universally correct action. Cascading a requester deletion into all
historical tickets would probably destroy important records. An anonymization
workflow or restricted deletion may be safer.

## 4. Constraints Reject Invalid States

### `NOT NULL`

Use when the fact must exist at row creation. Do not mark a field optional only
because imports are inconvenient.

### `UNIQUE`

Use when duplicate values would violate identity or a business rule:

```sql
ALTER TABLE metro_support.users
ADD CONSTRAINT users_email_unique UNIQUE (email);
```

### `CHECK`

Use a Boolean rule about one row:

```sql
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_priority_allowed
CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
```

```sql
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_close_after_open
CHECK (closed_at IS NULL OR closed_at >= opened_at);
```

Constraints should have meaningful names. An error mentioning
`tickets_priority_allowed` is more useful than one mentioning a generated name.

### Constraints Are Not a Complete Workflow Engine

A row-level `CHECK` can keep `closed_at` after `opened_at`. It cannot easily prove
that every status transition followed a multi-row workflow or external approval.
Use the database for durable invariants and choose application or procedural logic
for process rules that cross rows, time, or services.

## 5. An Index Is an Access Structure, Not the Rule Itself

An index stores an organized path to rows. It can accelerate matching, joining,
sorting, or uniqueness checks. It also consumes storage and adds work to inserts,
updates, deletes, backups, and maintenance.

```sql
CREATE INDEX tickets_status_opened_idx
ON metro_support.tickets (status, opened_at DESC);
```

This index may support a workload that filters status and requests recent rows.
It is not automatically useful for every query involving either column. Column
order, selectivity, table size, and the query plan matter. Week 7 develops the
evidence needed to decide.

A primary key or `UNIQUE` constraint normally creates a supporting unique index,
but the concepts differ. The constraint states a rule. The index is a mechanism
PostgreSQL can use to enforce or access data.

## 6. Managed PostgreSQL Still Leaves Schema Design to You

Supabase operates PostgreSQL infrastructure and adds services, but it cannot know
what `priority` values your system should accept or whether deleting a user should
remove tickets. The platform may expose a table editor, yet the SQL definition is
the durable artifact.

Use the dashboard to inspect and learn. Preserve schema changes in ordered SQL
files so another environment can be rebuilt and reviewed.

## Worked Example: Audit the Metro Support Baseline

The setup script accepts any text for `status`. That creates plausible but
inconsistent states:

```sql
UPDATE metro_support.tickets
SET status = 'IN PROGRESS'
WHERE ticket_id = 1002;
```

The update succeeds even though existing data uses `in_progress`. Reports that
filter the expected value may silently miss the row.

### Step 1: Inspect Existing Values

```sql
SELECT status, count(*)
FROM metro_support.tickets
GROUP BY status
ORDER BY status;
```

### Step 2: Normalize Before Constraining

```sql
UPDATE metro_support.tickets
SET status = lower(replace(status, ' ', '_'));
```

### Step 3: Add the Invariant

```sql
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_status_allowed
CHECK (status IN ('new', 'open', 'in_progress', 'resolved', 'closed'));
```

### Step 4: Verify With an Expected Failure

```sql
INSERT INTO metro_support.tickets (
    ticket_id, requester_id, category, priority, status, subject, opened_at
) VALUES (
    1099, 101, 'parks', 'low', 'almost_done', 'Constraint test', now()
);
```

The expected constraint error is evidence that the database rejects the bad
state. Run the test inside a transaction and roll it back if any part succeeds.

## 7. Inspect Metadata Instead of Guessing

The catalog is data about the database. `information_schema` offers portable
views; PostgreSQL's `pg_catalog` exposes deeper implementation details.

```sql
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'metro_support'
  AND table_name = 'tickets'
ORDER BY ordinal_position;
```

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'metro_support'
  AND tablename = 'tickets';
```

Metadata queries are more trustworthy than remembering what a dashboard displayed
or assuming a script ran.

## Common Misconceptions

### "The application validates it, so the database does not need to"

Imports, scripts, future services, bugs, and administrator actions can bypass one
application. Database constraints protect every write path.

### "More constraints are always better"

An incorrect rule can reject valid business states and make change difficult. Add
constraints for stable invariants, name them, test existing data, and plan change.

### "Every foreign key should cascade"

Cascade is convenient but may erase more than intended. Choose based on lifecycle
and audit requirements.

## Practice

Audit `metro_support.tickets` and propose:

1. one value-set constraint;
2. one nullability decision;
3. one referential-action decision; and
4. one candidate index tied to a stated query.

For each proposal, name the bad state or workload it addresses and one tradeoff.

## Retrieval and Transfer

1. What is the difference between a PostgreSQL schema and a table definition?
2. Why does a foreign key permit null unless the column is also `NOT NULL`?
3. How is a `UNIQUE` constraint conceptually different from an index?
4. What evidence proves that a new constraint is working?
5. Which Metro Support rule is too complex for a simple row-level `CHECK`, and
   why?

## Further Reading

- PostgreSQL data definition: <https://www.postgresql.org/docs/current/ddl.html>
- PostgreSQL constraints: <https://www.postgresql.org/docs/current/ddl-constraints.html>
- PostgreSQL schemas: <https://www.postgresql.org/docs/current/ddl-schemas.html>
- PostgreSQL indexes: <https://www.postgresql.org/docs/current/indexes.html>
- Supabase database overview: <https://supabase.com/docs/guides/database/overview>
