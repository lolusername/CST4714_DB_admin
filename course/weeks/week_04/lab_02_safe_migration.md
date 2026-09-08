# Lab 2: Add a Field Without Inventing History

Metro Support will collect a request's source channel: web, phone, or mobile.
Old tickets have no reliable channel field. Some notes mention a mobile form,
so labeling all old tickets `web` would manufacture information.

Add the field while preserving what is known and what is unknown. Work
individually in class. Submit one SQL file in Brightspace.

## 1. Check the Starting State

Use the personal database and `active_ticket_queue` view from
[Lab 1](lab_01_views_identity.md). Do not rerun the dataset reset between these
labs. If needed, complete Lab 1's view section first; the identity experiment is
not a prerequisite for this lab.

```sql
SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'metro_support' AND table_name = 'tickets'
  AND column_name = 'source_channel';

SELECT count(*) FROM metro_support.tickets;
SELECT count(*) FROM metro_support.active_ticket_queue;
```

Expect no `source_channel` column, 12 tickets, and 7 active tickets. If the column
already exists, inspect your previous attempt instead of adding it a second time.

## 2. Rehearse the Change

Build the migration between BEGIN and ROLLBACK. Run the whole block together.

```sql
BEGIN;

ALTER TABLE metro_support.tickets ADD COLUMN source_channel text;

-- An explicit unknown preserves uncertainty in historical data.
UPDATE metro_support.tickets SET source_channel = 'unknown'
WHERE source_channel IS NULL;

-- Add a named CHECK allowing web, phone, mobile, or unknown.
-- Then make source_channel NOT NULL.
-- Give it DEFAULT 'unknown' so old writers that omit the field can still work.

SELECT source_channel, count(*)
FROM metro_support.tickets GROUP BY source_channel;

ROLLBACK;
```

Complete the three commented instructions. Use the
[Chapter 4 migration example](../../textbook/module_04_change.md) and the
[Week 3 constraint lab](../week_03/lab_02_integrity_constraints.md) as references.
Rerun the precheck: rollback should remove the new column entirely.

After a successful rehearsal, run the same block with **COMMIT** in place of
ROLLBACK. Append `source_channel` as the last column of the existing view using
CREATE OR REPLACE VIEW. Keep all existing columns, their order, and the LEFT JOIN.

## 3. Test the New Contract

Check that the view still contains 7 tickets, including 1004 and 1009.
Inspect the new column's nullability and default through `information_schema.columns`.

Run a valid update to `mobile` inside a transaction, inspect it, then roll back.
Test an invalid value such as `fax` separately and record the named constraint
error. Leave the expected-failure statement commented in your submitted file.

**Submit:** `week_04_safe_migration.sql` with the precheck, completed migration,
verification queries, and a short note explaining two decisions: why historical
rows use `unknown`, and why the default helps an older application keep writing.

Once real source-channel values exist, dropping the column would discard them.
Explain why a later repair may need to preserve current data rather than undo
the entire migration. No additional change-plan document is required.
