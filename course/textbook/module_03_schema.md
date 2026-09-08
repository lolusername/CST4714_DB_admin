# A Schema Protects Meaning

## Operating Question

Which invalid states should the database refuse, even when an application has a
bug or a user imports a bad file?

Imagine receiving three CSV files that produce the right report today. That does
not yet tell us whether tomorrow's import can contain two records for the same
ticket, an impossible date, or a request assigned to a person who does not exist.
A schema turns selected assumptions into rules the DBMS can enforce. Choosing
those rules requires understanding the facts, not simply selecting a type from
a menu.

## Learning Outcomes

After this module, you can:

- use PostgreSQL schemas as namespaces and permission boundaries;
- choose basic data types, primary keys, and foreign keys;
- explain how dependencies and normalization reduce inconsistent copies of facts;
- apply `NOT NULL`, `UNIQUE`, `CHECK`, and referential actions intentionally;
- distinguish an integrity constraint from an index; and
- inspect database metadata instead of relying on memory.

## "Schema" Has Two Related Meanings

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

## Dependencies Explain Why We Separate Tables

Suppose a ticket table repeats the requester's current name and email on every
row. Maya has three tickets. When her email changes, one row is updated and two
are not. The database now offers conflicting answers to the question "what is
Maya's current email?" The problem is not that repetition is visually untidy.
The same fact has several independently writable representations.

A *functional dependency* expresses a rule about which attributes determine
others. Under our account model, one `user_id` determines one current display
name and email:

$$
\text{user\_id} \to
\{\text{display\_name},\text{email}\}.
$$

This means that two valid rows with the same user ID cannot disagree about those
attributes. It is a rule about every permitted instance, not a pattern proved by
today's eight rows. If every ticket in a tiny sample happens to have a different
category, that coincidence does not make category a valid ticket identifier.

A *superkey* determines the entire row. A *candidate key* is a minimal superkey:
removing any attribute from it would lose that property. We choose one candidate
as the primary key. Additional business identities may be protected with unique
constraints. The word minimal concerns the included attributes, not whether the
numeric values are small.

### Insertion, Update, and Deletion Anomalies

Repeating current account details in a ticket table creates several problems.
An update can change one copy and leave others behind. Inserting an account may
require inventing a ticket merely to have somewhere to store the account's
attributes. Deleting the person's last ticket may delete the only remaining
record of the account. These are update, insertion, and deletion anomalies.

We separate `users` from `tickets` so each current account fact has one
authoritative location. Tickets store the identifying reference. We can join
the relations when a report needs both. That join has a computational cost, but
it also reconstructs a combined view without making every combined view a new
independently writable copy.

### A Brief Normalization Review

First normal form is conventionally taught as using one value from the declared
domain in each attribute rather than repeating groups such as `event1`, `event2`,
and `event3`. A variable-length history should not require adding another column
every time an event occurs. PostgreSQL can legitimately store arrays or `jsonb`;
their availability does not decide whether a nested value is the best way to
represent a particular relationship.

Second normal form addresses partial dependencies on a composite candidate key.
For a table keyed by `(ticket_id, tag_id)`, a tag's current label depends on
`tag_id`, not on the whole assignment pair. Store the label in a tag relation
rather than repeating it for every ticket that uses the tag.

Third normal form further limits dependencies that let non-key facts determine
other non-key facts. In the repeated-requester example, `ticket_id` determines
`requester_id`, and requester identity determines the current email. Keeping the
email in `users` avoids storing that dependency repeatedly in `tickets`. The
formal 3NF condition is: for every nontrivial dependency $X\to A$, either $X$ is
a superkey or $A$ belongs to a candidate key. This qualification matters when a
relation has several overlapping candidate keys. Boyce-Codd normal form uses the
stricter requirement that each nontrivial determinant be a superkey.

For this course, the practical goal is to recognize where a current fact has
multiple writable copies and explain a sensible decomposition. Decompositions
should be *lossless*: joining the pieces through the intended keys must recover
the original facts without inventing combinations. In Metro Support, each
ticket's non-null requester points to one uniquely identified user, so joining
that reference retrieves one requester record per ticket.

Normalization does not forbid every purposeful copy. A ticket may need the
address reported **at the time of submission**, even after a resident moves.
That historical address is a different fact from the account's current address.
A document summary used for faster reads may also copy current data, provided
we identify its owner and update policy. Chapters 10 and 14 revisit those
deliberate choices. A label such as "denormalized" is not an explanation by itself.

## Data Types Express Allowed Representation

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

An instant and a calendar label are different facts. `timestamptz` lets us compare
the instant at which two events occurred even if clients display different time
zones. It does not retain the user's original zone name. If the application must
schedule "9 a.m. in New York" on future dates, keep the relevant zone or scheduling
rule too. A ZIP code may look numeric but is often better stored as text because
leading zeroes are significant and arithmetic on the value has no meaning.

## Keys Identify and Connect Facts

A **primary key** uniquely identifies a row and is not null. A **foreign key**
requires a value to match a key in another table, unless the foreign-key column is
allowed to be null.

The following reduced definition illustrates those rules. The complete baseline
already has a `tickets` table, so do not execute this `CREATE TABLE` again after
loading it.

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

The assignee foreign key establishes that a user exists, not that the user has
role `agent`. Assigning resident 101 would satisfy this particular reference.
That is a useful example of a valid database state that may still violate a
business rule we have not encoded. A richer design could separate eligible staff
into a referenced relation. Application authorization and Chapter 6's permissions
address other parts of the problem; none should be assumed from the foreign key
alone.

### Referential Actions Are Business Decisions

What should happen if a user row is deleted?

- `RESTRICT` or `NO ACTION`: refuse deletion while dependent rows exist.
- `CASCADE`: delete or update dependent rows automatically.
- `SET NULL`: preserve the dependent row but remove the reference.

There is no universally correct action. Cascading a requester deletion into all
historical tickets would probably destroy important records. An anonymization
workflow or restricted deletion may be safer.

## Constraints Reject Invalid States

### `NOT NULL`

Use when the fact must exist at row creation. Do not mark a field optional only
because imports are inconvenient.

### `UNIQUE`

Use when duplicate values would violate identity or a business rule:

```sql
-- The supplied baseline already declares email NOT NULL UNIQUE.
-- Inspect the existing rule instead of adding a second copy.
SELECT conname, pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'metro_support.users'::regclass
  AND contype = 'u';
```

By default, PostgreSQL uniqueness does not treat two nulls as the same value.
The baseline avoids that issue for email by also requiring a value. If a different
design needs null to participate in uniqueness as one shared missing value,
PostgreSQL 15 and later support `UNIQUE NULLS NOT DISTINCT`. Choose the intended
meaning rather than assuming every SQL system makes the same choice.

### `CHECK`

Use a Boolean rule about one row:

```sql
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_priority_allowed
CHECK (priority IN ('low', 'medium', 'high', 'urgent'));
```

```sql
-- This equivalent date rule already exists in the supplied baseline.
-- The statement illustrates its definition; do not add a redundant copy.
ALTER TABLE metro_support.tickets
ADD CONSTRAINT tickets_close_after_open
CHECK (closed_at IS NULL OR closed_at >= opened_at);
```

Constraints should have meaningful names. An error mentioning
`tickets_priority_allowed` is more useful than one mentioning a generated name.

A `CHECK` rejects false, but accepts true **or unknown**. Thus `CHECK (score >= 0)`
does not prohibit a null score. Add `NOT NULL` if the value itself is required.
This differs from `WHERE`, which retains only true. The same three-valued logic
has different consequences at a filter and at a constraint boundary.

### Constraints Are Not a Complete Workflow Engine

A row-level `CHECK` can keep `closed_at` after `opened_at`. It cannot easily prove
that every status transition followed a multi-row workflow or external approval.
Use the database for durable invariants and choose application or procedural logic
for process rules that cross rows, time, or services.

PostgreSQL does not support cross-table queries inside a `CHECK` as a general
integrity mechanism. A function that happens to look at another table does not
make the dependency safely maintained when that other table changes. Use foreign
keys or another explicitly coordinated mechanism for cross-row requirements.
The [PostgreSQL constraints reference](https://www.postgresql.org/docs/current/ddl-constraints.html)
documents these null and cross-row distinctions.

## An Index Is an Access Structure, Not the Rule Itself

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
facts and measurements needed to decide.

A primary key or `UNIQUE` constraint normally creates a supporting unique index,
but the concepts differ. The constraint states a rule. The index is a mechanism
PostgreSQL can use to enforce or access data.

## Managed PostgreSQL Still Leaves Schema Design to You

Supabase operates PostgreSQL infrastructure and adds services, but it cannot know
what `priority` values your system should accept or whether deleting a user should
remove tickets. The platform may expose a table editor, yet the SQL definition is
the durable artifact.

Use the dashboard to inspect and learn. Preserve schema changes in ordered SQL
files so another environment can be rebuilt and reviewed.

![Figure 3.1: Supabase Table Editor with no tables displayed in the selected public namespace. Custom schemas may contain other tables. Account identifiers are redacted. Interface captured August 25, 2026.](figures/cloud_interfaces/supabase_table_editor.png){#fig-supabase-table-editor width=68%}

The graphical editor helps reveal tables and columns, while the durable
definition states names, types, defaults, keys, checks, and referential actions
in reviewable SQL. An ordered setup script also makes the schema reproducible in
another environment.

## Worked Example: Audit the Metro Support Baseline

The setup script accepts any text for `status`. That creates plausible but
inconsistent states:

The next steps are a worked migration on a fresh practice baseline, before the
Week 3 status constraint has been added. Do not run the entire chapter as one
script; some listings are definitions or deliberate failures. In particular,
keep expected-error statements separate from a normal successful run.

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

For this known spelling error, map the identified invalid value explicitly.
Do not apply a broad text transformation and assume all resulting words represent
approved states. An unknown value should be investigated rather than silently
reinterpreted.

```sql
UPDATE metro_support.tickets
SET status = 'in_progress'
WHERE ticket_id = 1002 AND status = 'IN PROGRESS'
RETURNING ticket_id, status;
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

The expected constraint error confirms that the database rejects the bad state.
Run the test inside a transaction and roll it back if any part succeeds.

## Inspect Metadata Instead of Guessing

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
application. Enforced database constraints apply regardless of which ordinary
client issues a write. An administrator who can alter or remove the rules is a
different trust boundary; constraint design does not replace access control.

### "More constraints are always better"

An incorrect rule can reject valid business states and make change difficult. Add
constraints for stable invariants, name them, test existing data, and plan change.

### "Every foreign key should cascade"

Cascade is convenient but may erase more than intended. Choose based on lifecycle
and audit requirements.

## Practice

The assigned Week 3 labs use this chapter to inspect the actual baseline and then
add priority/status rules with valid and invalid tests. Before Day 1, read through
**Keys Identify and Connect Facts**, including the normalization review. Before
Day 2, read **Constraints Reject Invalid States** and the worked status repair.
The broader proposals below are optional study practice.

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
4. What test confirms that a new constraint is working?
5. Which Metro Support rule is too complex for a simple row-level `CHECK`, and
   why?

## Further Reading

- Andy Pavlo, Carnegie Mellon University,
  [**Functional Dependencies**](https://15445.courses.cs.cmu.edu/fall2017/notes/04-notes-functionaldependencies.pdf)
  and [**Normal Forms**](https://15445.courses.cs.cmu.edu/fall2017/notes/05-notes-normalforms.pdf)
  (2017 lecture notes).
  These free notes extend the dependency and decomposition discussion; they are
  external readings rather than course-authored material.
- [PostgreSQL data definition](https://www.postgresql.org/docs/current/ddl.html)
- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [PostgreSQL schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [Supabase database overview](https://supabase.com/docs/guides/database/overview)
