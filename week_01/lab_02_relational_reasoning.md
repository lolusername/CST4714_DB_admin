# Lab 2: Relational Reasoning Before SQL

## Purpose

Use a tiny dataset to recover the relational-model ideas underneath SQL. This is
individual work completed in class. Submit one Markdown file.

## Tiny Service Desk

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

Create `week_01/relational_reasoning.md` in GitHub's browser editor and complete
the two parts below.

## Part A: Relations and Operations

1. List the attributes in the schema of `tickets`.
2. Copy one tuple and explain the real-world fact it represents.
3. Identify the primary key of each relation and two likely foreign keys.
4. Give a reasonable domain for `priority`.
5. Calculate the exact results of these expressions:

$$
A = \sigma_{priority = \text{'high'}}(tickets)
$$

$$
B = \pi_{assignee\_id}(A)
$$

For each result, state what one output tuple represents. Classical relational
algebra removes duplicate tuples; ordinary SQL keeps duplicates unless
`DISTINCT` is requested. Explain how that difference affects $B$.

## Part B: Relationships

Calculate this inner join by hand and display only `ticket_id`, `status`, and
`name`:

$$
C = tickets \bowtie_{tickets.assignee\_id = users.user\_id} users
$$

Then answer:

1. Why is ticket 11 absent from the inner join?
2. What would a left join display for ticket 11's agent name?
3. How many row pairs exist in $tickets \times users$ before the join condition
   filters them? Show the multiplication.
4. Which user IDs appear as requesters but not as assignees? Name the set
   operation used to find them.

## Submit One Thing

Commit `relational_reasoning.md` and submit its URL in Brightspace. One file is
enough; it should contain the relation vocabulary, calculated outputs, join
result, and short explanations.
