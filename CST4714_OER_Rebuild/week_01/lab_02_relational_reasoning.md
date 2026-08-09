# Lab 2: Relational Reasoning Before SQL

## Purpose

Recover the relational-model ideas that make SQL understandable. You will reason
with small tables by hand before a DBMS performs the operations for you.

This is individual work completed in class. Submit one Markdown file.

## The Tiny Service Desk

### `users`

| user_id | name | role |
|---:|---|---|
| 1 | Ana | resident |
| 2 | Bo | agent |
| 3 | Cy | agent |

### `tickets`

| ticket_id | requester_id | assignee_id | priority | status |
|---:|---:|---:|---|---|
| 10 | 1 | 2 | high | open |
| 11 | 1 | null | low | new |
| 12 | 1 | 2 | high | resolved |

## 1. Describe the Relations

Create `week_01/relational_reasoning.md` in GitHub's online editor. Answer these
questions in the file:

1. What is the schema of `tickets`? List its attributes.
2. Copy one tuple from `tickets` and explain what real-world fact it represents.
3. Give a reasonable domain for `priority`.
4. Identify the primary key of each relation.
5. Identify two foreign-key relationships suggested by the data.
6. Is the table shown above a relation schema or a relation instance? Explain.

## 2. Predict Selection and Projection

Do not write SQL yet.

For each expression, write the exact output table and say what one output row
means.

```text
A = sigma priority = 'high' (tickets)

B = pi assignee_id (A)
```

Then answer:

- Does classical relational algebra keep both `2` values in `B`? Why?
- Would ordinary SQL `SELECT assignee_id ...` necessarily remove the duplicate?
- What SQL keyword could request duplicate removal?

## 3. Build a Join and a Difference

Manually create the output for:

```text
C = tickets join tickets.assignee_id = users.user_id users
```

Project only `ticket_id`, `status`, and `name` in your displayed result.

Then answer:

1. Why is ticket 11 absent from an inner join?
2. What would a left join display for its agent name?
3. The Cartesian product has how many row pairs before the join condition filters
   them? Show the multiplication.
4. Write the set of user IDs that appear as requesters but not as assignees. Name
   the relational operation that produces that answer.

## Submit One Thing

Commit `relational_reasoning.md` with the message
`Complete relational reasoning review`, then submit the file URL in Brightspace.

Your file is complete when it includes relation vocabulary, exact predicted
outputs, an explanation of set versus SQL bag behavior, the join result, and the
difference result.
