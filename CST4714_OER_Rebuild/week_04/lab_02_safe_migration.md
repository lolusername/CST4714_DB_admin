# Lab 2: Add a Required Field Safely

## Purpose

Practice a small expand-migrate-verify change rather than adding a required column
in one risky step.

This is individual work completed in class. Submit one SQL file.

## Scenario

Metro Support needs to record each ticket's source channel. Existing tickets came
from the web form. Future allowed values are `web`, `phone`, and `mobile`.

## 1. Write the Change Record

Create `week_04_safe_migration.sql`. Begin with comments containing:

- intent;
- precheck;
- ordered change;
- verification; and
- rollback or forward-fix decision.

Your precheck must prove that `source_channel` does not already exist and record
the current ticket count.

## 2. Expand, Migrate, and Verify

Write SQL that:

1. adds `source_channel` as nullable;
2. backfills existing rows with `web`;
3. verifies that no nulls or unexpected values remain;
4. adds a named allowed-values constraint;
5. makes the column `NOT NULL`; and
6. updates `active_ticket_queue` to expose the new field without using
   `SELECT *`.

Run the change in a transaction first and inspect the structure and data before
rolling back. Then run the reviewed version and commit it.

## 3. Prove the Result

Add queries that prove:

- the column type and nullability;
- the constraint definition;
- the distribution of channel values;
- the view still preserves every active ticket; and
- a valid new ticket can use `mobile` inside a rolled-back test transaction.

Include one commented invalid insert and record the short expected constraint
error after testing it separately.

## Submit One Thing

Submit `week_04_safe_migration.sql`. A reviewer should be able to identify intent,
run order, safety boundary, verification, and response if the change fails.
