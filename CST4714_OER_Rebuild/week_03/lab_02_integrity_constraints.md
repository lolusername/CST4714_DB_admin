# Lab 2: Reject Bad States

## Purpose

Turn two stable business rules into named database constraints and prove that the
schema accepts valid data while rejecting invalid data.

This is individual work completed in class. Submit one SQL file.

## 1. Inspect Before Constraining

Create `week_03_integrity_build.sql`. Begin with queries that list every distinct
`status` and `priority` value and its count. Compare the values with these rules:

- priority must be `low`, `medium`, `high`, or `urgent`;
- status must be `new`, `open`, `in_progress`, `resolved`, or `closed`.

Add a comment explaining why existing data must be checked before adding a
constraint.

## 2. Add and Verify the Rules

Add two meaningfully named `CHECK` constraints to `metro_support.tickets`.

Then add metadata queries that show each constraint name and definition. Prepare
two invalid inserts as commented-out SQL: one with an invalid priority and one
with an invalid status.

Run each invalid statement separately in the SQL editor and copy only the short,
redacted error text into a comment below it. Leave the invalid statements
commented in the submitted file so the file can run from top to bottom.

Finally, run a valid insert inside a transaction, use `RETURNING` to inspect it,
and roll it back. This proves the constraints do not reject every new row.

## 3. Record an Index Candidate

Metro Support frequently lists active tickets newest first. Create this candidate
index:

```sql
CREATE INDEX tickets_status_opened_idx
ON metro_support.tickets (status, opened_at DESC);
```

Query `pg_indexes` to prove that it exists. Add a comment stating:

- the exact query pattern it is intended to support; and
- one cost it adds.

Do not claim the index improved performance yet. Week 7 will measure plans on a
large enough table.

## Submit One Thing

Submit `week_03_integrity_build.sql`. It must include prechecks, two constraints,
metadata verification, two documented expected failures, one rolled-back valid
insert, and one explicitly hypothetical index decision.
