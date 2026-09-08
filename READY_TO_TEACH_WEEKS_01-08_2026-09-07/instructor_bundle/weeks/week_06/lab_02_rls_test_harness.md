# Lab 2: Two Residents, Different Visible Tickets

Both residents may read the tickets table, but each should see only their own
requests. Use row-level security (RLS) to make the same query return different
rows for different database roles.

Work individually in your personal PostgreSQL/Supabase practice database.
Submit one SQL file in Brightspace.

## 1. Create the Small Test Case

Run as the project's administrative database user:

```sql
CREATE ROLE resident_101_lab NOLOGIN;
CREATE ROLE resident_102_lab NOLOGIN;
GRANT resident_101_lab, resident_102_lab TO CURRENT_USER;
CREATE SCHEMA security_lab;
CREATE TABLE security_lab.resident_tickets (
    ticket_id integer PRIMARY KEY,
    owner_role text NOT NULL,
    subject text NOT NULL
);
INSERT INTO security_lab.resident_tickets VALUES
    (1, 'resident_101_lab', 'Broken bench'),
    (2, 'resident_101_lab', 'Dark streetlight'),
    (3, 'resident_102_lab', 'Missed pickup'),
    (4, 'resident_102_lab', 'Leaking hydrant');
GRANT USAGE ON SCHEMA security_lab TO resident_101_lab, resident_102_lab;
GRANT SELECT ON security_lab.resident_tickets TO resident_101_lab, resident_102_lab;
```

If you already created these objects in your own project, run the cleanup at the
end before repeating the lab. The schema contains only this four-row exercise.

## 2. Add the Rule and Test Both People

Here is the policy:

```sql
ALTER TABLE security_lab.resident_tickets ENABLE ROW LEVEL SECURITY;
CREATE POLICY read_own_tickets ON security_lab.resident_tickets
FOR SELECT TO resident_101_lab, resident_102_lab
USING (owner_role = current_user);
```

Table SELECT permission allows the action; the RLS policy filters which rows the
action can see. Before running the next test, predict its ticket IDs.

Run the actor, query, and rollback together in one batch:

```sql
BEGIN;
SET LOCAL ROLE resident_101_lab;
SELECT current_user, ticket_id, subject
FROM security_lab.resident_tickets ORDER BY ticket_id;
ROLLBACK;
```

Repeat the batch for `resident_102_lab`. Expect IDs **1, 2** for the first
resident and **3, 4** for the second. Keep both actor queries in your file.
If your web editor hides intermediate SELECT results, reuse the
[Colab result-display cell from Lab 1](lab_01_least_privilege.md#visible-results-in-colab).
Replace its `tests` list with the following and run the complete cell. Each query
runs inside its own rolled-back transaction on the same connection.

```python
tests = [
    ("resident_101_lab", "SELECT current_user, ticket_id, subject FROM security_lab.resident_tickets ORDER BY ticket_id"),
    ("resident_102_lab", "SELECT current_user, ticket_id, subject FROM security_lab.resident_tickets ORDER BY ticket_id"),
]
```

Run the query again as the administrative table owner. Explain why seeing all
four rows in that context does not show that the resident policy failed.

Now test a direct lookup: as `resident_101_lab`, add `WHERE ticket_id = 3` to
the SELECT before `ORDER BY`. Expect **zero rows**, not a permission error.
The query can read the table, but the policy hides the other resident's row.

Make one change as the administrative user: write an `INSERT` for ticket **5**,
owned by **`resident_102_lab`**, with a subject of your choice. Reuse the column
order in the setup. Predict and rerun both resident queries. Resident 101 should
still see **1, 2**, while resident 102 now sees **3, 4, 5**. The policy must work
for a new row without being rewritten as a list of ticket numbers. An existing
ticket 5 means you already ran this step; inspect it rather than inserting a
duplicate or resetting the whole class dataset.

## 3. Explain the Real Application Connection

Write a short update to the application developer in your SQL comments. State
which IDs each resident could see before and after your new row, and what the
direct lookup returned. Explain why those results are stronger than testing
only as the owner. Finish by naming the remaining real-application test: a
request with each resident's own verified login token.

A real Supabase application normally uses the shared `authenticated` database
role and `auth.uid()` from the user's JWT, rather than one PostgreSQL role per
resident. Its ownership column would store the user's UUID. The SQL Editor's
administrative role does not substitute for that resident's request.

This lesson deliberately uses database roles so the visibility rule is easy to
observe. It does not build a login system. Use the
[Supabase explanation in Chapter 6](../../textbook/module_06_security.md)
to connect the two identity models.

After testing, clean up:

```sql
DROP SCHEMA security_lab CASCADE;
REVOKE resident_101_lab, resident_102_lab FROM CURRENT_USER;
DROP ROLE resident_101_lab;
DROP ROLE resident_102_lab;
```

**Submit:** `week_06_rls_test.sql` with setup, policy, your new row and tests,
the short developer update, and cleanup. No separate report is required.
