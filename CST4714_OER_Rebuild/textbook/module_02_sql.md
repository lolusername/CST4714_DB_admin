# Module 2: Relational Operations Become Testable SQL

## Operating Question

How can a query answer a real question while making it possible to check whether
the answer is trustworthy?

## Learning Outcomes

After this module, you can:

- explain rows, columns, keys, and relationships in a relational model;
- translate selection, projection, rename, product, join, union, and difference
  between relational-algebra notation and plain language;
- use `SELECT`, `WHERE`, `ORDER BY`, `JOIN`, `GROUP BY`, and aggregate functions;
- review subqueries, common table expressions, and safe `INSERT`, `UPDATE`, and
  `DELETE` patterns;
- reason about `NULL` without treating it as zero or an empty string;
- distinguish the written order of a query from its logical processing order; and
- verify a query with counts, boundary cases, and comparison queries.

## 1. A Relation Represents One Kind of Fact

The relational model organizes data into relations commonly presented as tables.
A row represents one occurrence, and each column represents one attribute of that
kind of occurrence. A key identifies a row. A foreign key records a relationship
by referring to a key in another table.

Metro Support separates:

- `users`: one row per person or staff account;
- `tickets`: one row per support request; and
- `ticket_events`: one row per recorded event in a ticket's history.

This separation avoids repeating a user's name and email in every ticket event.
It also creates work: a query must join related rows when the answer needs facts
from more than one table.

## 2. Relational Algebra Gives Us a Reasoning Vocabulary

Relational algebra describes how one or more input relations become an output
relation. The notation is less important than the habit of decomposing a question
into operations.

Assume `T` is the tickets relation and `U` is the users relation.

| Operation | Notation | Plain-language job | Common SQL form |
|---|---|---|---|
| selection | `sigma condition (T)` | keep rows meeting a condition | `WHERE` |
| projection | `pi columns (T)` | keep or compute selected attributes | `SELECT` |
| rename | `rho alias (T)` | give a relation or attribute a usable name | `AS` |
| Cartesian product | `T x U` | pair every row in one input with every row in the other | `CROSS JOIN` |
| theta/equi-join | `T join condition U` | pair only rows satisfying a relationship | `JOIN ... ON` |
| union | `R union S` | rows in either compatible relation | `UNION` |
| difference | `R - S` | rows in the first compatible relation but not the second | `EXCEPT` |

For readability, this module spells out the Greek operators in code-style text
instead of requiring special symbols. You should be able to recognize the usual
symbols, but you will be assessed on reasoning and translation.

### Example Translation

**Question:** Which high-priority tickets are still active, and what are their
subjects?

Reasoning:

1. select tickets where priority is high and status is active;
2. project the ticket identifier, subject, and status; and
3. sort for presentation, which is useful SQL behavior but not a core relational-
   algebra operation.

```text
pi ticket_id, subject, status (
  sigma priority = 'high' AND status in active_statuses (tickets)
)
```

```sql
SELECT ticket_id, subject, status
FROM metro_support.tickets
WHERE priority = 'high'
  AND status IN ('new', 'open', 'in_progress')
ORDER BY ticket_id;
```

### Algebra and SQL Are Related, Not Identical

Classical relational algebra uses sets: duplicate tuples do not occur, and
ordering is not part of a relation. SQL normally uses *bag* or multiset semantics,
so duplicate result rows can occur unless a key, grouping operation, `DISTINCT`,
or set operator changes that. SQL also includes `NULL` and three-valued logic,
which require reasoning beyond classical algebra.

This difference explains two important habits: always state the expected result
grain, and never assume row order without `ORDER BY`.

## 3. Start With a Precise Question

"Show tickets" is vague. "List open or in-progress high-priority tickets, newest
first, with the assigned agent's name" is testable. It identifies:

- the unit: one ticket per result row;
- the filter: selected statuses and high priority;
- the order: newest first;
- the relationship: ticket to assigned user; and
- the desired attributes.

Before writing SQL, state the expected grain: what does one result row mean?
Unexpected duplicates often reveal that the query changed grain.

## 4. Select, Filter, and Sort

```sql
SELECT ticket_id, subject, status, opened_at
FROM metro_support.tickets
WHERE status IN ('open', 'in_progress')
ORDER BY opened_at DESC;
```

`SELECT` names the output expressions. `FROM` identifies the source. `WHERE`
removes rows that do not meet the predicate. `ORDER BY` controls presentation.
Without `ORDER BY`, row order is not guaranteed, even when repeated runs appear
consistent.

Avoid `SELECT *` in durable work. Explicit columns document intent, reduce
unnecessary transfer, and make a query less vulnerable to later schema changes.

## 5. SQL's Logical Order

SQL is written in a human-readable order but reasoned about approximately as:

1. `FROM` and `JOIN` build the source rows.
2. `WHERE` filters individual rows.
3. `GROUP BY` forms groups.
4. aggregate calculations summarize each group.
5. `HAVING` filters groups.
6. `SELECT` produces output expressions.
7. `ORDER BY` sorts the result.
8. `LIMIT` restricts the returned rows.

This explains why a `SELECT` alias is often unavailable in `WHERE`: the filter is
logically evaluated before the output alias exists.

## 6. Join Related Facts

```sql
SELECT
    t.ticket_id,
    t.subject,
    u.display_name AS assignee_name
FROM metro_support.tickets AS t
LEFT JOIN metro_support.users AS u
    ON u.user_id = t.assignee_id
ORDER BY t.ticket_id;
```

An `INNER JOIN` returns only matching pairs. A `LEFT JOIN` preserves every row
from the left side and supplies `NULL` for missing right-side values. Because two
tickets are unassigned, an inner join would silently remove them. The join type is
therefore a statement about the question, not just syntax.

### A Join Is a Filtered Product

A Cartesian product pairs every row in one relation with every row in another.
With 12 tickets and 8 users, the product has 96 pairs. An equi-join keeps only
pairs whose key values match. Thinking of a join as product plus selection makes a
missing join condition easier to recognize.

### Diagnose Duplicate Rows

Joining one ticket to many events changes the grain from one row per ticket to one
row per matching event:

```sql
SELECT t.ticket_id, t.subject, e.event_type, e.event_at
FROM metro_support.tickets AS t
JOIN metro_support.ticket_events AS e
    ON e.ticket_id = t.ticket_id
WHERE t.ticket_id = 1003
ORDER BY e.event_at;
```

Three rows for ticket 1003 are correct because it has three events. Adding
`DISTINCT` would hide the evidence rather than answer why the rows multiplied.

## 7. `NULL` Means Missing or Inapplicable

`NULL` is not zero, blank text, or a normal value. Comparisons with `NULL` do not
evaluate to true:

```sql
-- Incorrect: this does not find unassigned tickets.
WHERE assignee_id = NULL

-- Correct.
WHERE assignee_id IS NULL
```

Three-valued logic includes true, false, and unknown. This matters for filters,
constraints, joins, and aggregates. `count(*)` counts rows. `count(assignee_id)`
counts only rows where that expression is not null.

## 8. Group and Aggregate

```sql
SELECT
    category,
    count(*) AS ticket_count,
    count(closed_at) AS closed_timestamp_count
FROM metro_support.tickets
GROUP BY category
ORDER BY ticket_count DESC, category;
```

After grouping, every selected expression must either identify the group or
summarize it. The result grain is now one row per category.

Use `HAVING` for a condition on a group:

```sql
SELECT category, count(*) AS ticket_count
FROM metro_support.tickets
GROUP BY category
HAVING count(*) >= 3;
```

## Worked Example: Agent Workload Without Losing Unassigned Tickets

**Question:** For every agent, how many currently active tickets are assigned?

First define "active" as `new`, `open`, or `in_progress`. The result should have
one row per agent, including an agent with zero active tickets.

```sql
SELECT
    u.user_id,
    u.display_name,
    count(t.ticket_id) AS active_ticket_count
FROM metro_support.users AS u
LEFT JOIN metro_support.tickets AS t
    ON t.assignee_id = u.user_id
   AND t.status IN ('new', 'open', 'in_progress')
WHERE u.role = 'agent'
GROUP BY u.user_id, u.display_name
ORDER BY active_ticket_count DESC, u.display_name;
```

Why is the ticket-status condition in `ON` rather than `WHERE`? A `WHERE`
condition on `t.status` would remove the null-extended row for an agent with no
matching active ticket, making the left join behave like an inner join for this
purpose.

Why `count(t.ticket_id)` instead of `count(*)`? The left join produces one row for
an agent with no match, but `t.ticket_id` is null in that row. Counting the ticket
identifier correctly yields zero.

## 9. Subqueries and CTEs Name Intermediate Relations

A subquery produces a relation used by another query. A common table expression,
or CTE, gives that intermediate result a name.

```sql
WITH active_tickets AS (
    SELECT ticket_id, assignee_id, priority
    FROM metro_support.tickets
    WHERE status IN ('new', 'open', 'in_progress')
),
agent_counts AS (
    SELECT assignee_id, count(*) AS active_count
    FROM active_tickets
    WHERE assignee_id IS NOT NULL
    GROUP BY assignee_id
)
SELECT u.display_name, a.active_count
FROM agent_counts AS a
JOIN metro_support.users AS u
    ON u.user_id = a.assignee_id
ORDER BY a.active_count DESC, u.display_name;
```

Read each CTE as a named step in relational reasoning. A CTE can improve clarity,
but it is not automatically faster. PostgreSQL's optimizer and version determine
how it is planned.

Set operators express union and difference when inputs have compatible columns:

```sql
-- Users who requested a ticket but are not assigned to any ticket.
SELECT requester_id AS user_id
FROM metro_support.tickets
EXCEPT
SELECT assignee_id
FROM metro_support.tickets
WHERE assignee_id IS NOT NULL;
```

`UNION` removes duplicate rows. `UNION ALL` preserves them and avoids duplicate-
elimination work when set semantics are not required.

## 10. Review Safe Data Changes

Queries read state; data-manipulation statements change it.

```sql
INSERT INTO metro_support.ticket_events (
    event_id, ticket_id, actor_id, event_type, old_status, new_status, note, event_at
) VALUES (
    5099, 1001, 201, 'note_added', 'open', 'open',
    'Replacement lamp requested', now()
);
```

Before an `UPDATE` or `DELETE`, write the same predicate as a `SELECT` and inspect
the target keys:

```sql
SELECT ticket_id, priority
FROM metro_support.tickets
WHERE category = 'streetlight'
  AND priority = 'medium';

BEGIN;

UPDATE metro_support.tickets
SET priority = 'high'
WHERE category = 'streetlight'
  AND priority = 'medium'
RETURNING ticket_id, priority;

ROLLBACK;
```

`RETURNING` shows affected rows. A transaction creates a decision point. Neither
replaces a correct predicate or independent verification.

Use the same discipline for deletion:

```sql
BEGIN;

DELETE FROM metro_support.ticket_events
WHERE event_id = 5099
RETURNING event_id, ticket_id;

-- Verify the intended row and then choose COMMIT or ROLLBACK.
ROLLBACK;
```

Never practice broad destructive statements in a shared or production database.

## 11. Verification Is a Second Query or Reasoning Path

Use at least one of these methods:

- **Known total:** compare grouped counts with the total number of source rows.
- **Boundary case:** inspect an unassigned ticket, a null value, or a user with no
  match.
- **Simpler query:** verify one result category with a direct filtered count.
- **Uniqueness check:** compare total rows with distinct keys at the expected grain.
- **Manual sample:** trace one identifier across source tables.

For the workload query, verify Priya Shah directly:

```sql
SELECT ticket_id, status
FROM metro_support.tickets
WHERE assignee_id = 201
  AND status IN ('new', 'open', 'in_progress');
```

The verification query is intentionally less abstract. Independent reasoning is
more valuable than repeating the same logic in a different format.

## Common Misconceptions

### "No rows means the query worked"

No rows could mean no data matches, the filter is wrong, a join removed records,
or the setup failed. Verify source counts and test one known identifier.

### "A join connects tables automatically"

SQL joins use the condition you write. A missing or incorrect condition can create
a Cartesian product or pair unrelated records.

### "`DISTINCT` fixes duplicates"

`DISTINCT` removes identical output rows. It does not fix an incorrect grain or
relationship and may hide a modeling or join error.

## Practice

First express the required operations in plain language or relational-algebra
notation. Then write a query that returns one row per neighborhood with:

- the number of resident users;
- the number of tickets they requested; and
- the most recent ticket opening time.

Before running it, predict which joins are required and whether a left join is
necessary. After running it, verify one neighborhood with a simpler query.

## Retrieval and Transfer

1. How do selection and projection differ?
2. Why is a join related to a Cartesian product?
3. What does one row in a query result represent?
4. Why can a left join return more rows than the left table?
5. What is the difference between `WHERE` and `HAVING`?
6. Why does `column = NULL` not work as expected?
7. When does `UNION ALL` express the intended result better than `UNION`?
8. What should you do before running an `UPDATE` or `DELETE`?
9. A report suddenly doubles its row count after an events table is joined. What
   should you inspect before adding `DISTINCT`?

## Further Reading

- PostgreSQL `SELECT`: <https://www.postgresql.org/docs/current/sql-select.html>
- PostgreSQL table expressions and joins:
  <https://www.postgresql.org/docs/current/queries-table-expressions.html>
- PostgreSQL aggregate functions:
  <https://www.postgresql.org/docs/current/functions-aggregate.html>
- *Database Design - 2nd Edition*, Chapter 8:
  <https://opentextbc.ca/dbdesign01/chapter/chapter-8-entity-relationship-model/>
