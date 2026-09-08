# Lab 1: Give an Analyst the Access They Need

An analyst needs ticket counts and statuses, but not residents' email addresses or
permission to edit requests. Build that boundary and test it as the analyst.

Work individually in class. Submit one SQL file in Brightspace. Use your own
PostgreSQL/Supabase practice project. Roles belong to the database server, so
do not run this setup in somebody else's or a shared project.

## 1. Set Up a Limited Role and View

Use the [Metro Support setup](../../datasets/metro_support/postgres_setup.sql) if
the practice data is missing. Run this as your project's administrative database
user:

```sql
CREATE ROLE metro_analyst_lab NOLOGIN;
GRANT metro_analyst_lab TO CURRENT_USER;

CREATE OR REPLACE VIEW metro_support.analyst_ticket_summary AS
SELECT ticket_id, category, priority, status, opened_at, closed_at
FROM metro_support.tickets;

GRANT USAGE ON SCHEMA metro_support TO metro_analyst_lab;
GRANT SELECT ON metro_support.analyst_ticket_summary TO metro_analyst_lab;
```

NOLOGIN makes a role for privileges rather than a new password. Granting it to
your current user lets you switch into it for the test. If the role already
exists from your own earlier attempt, inspect it or run the cleanup below
before starting again.

The view deliberately omits email and internal notes. The role receives no
permission on the base tables. Both choices matter.

## 2. Test as the Analyst

Execute each actor test as **one complete batch**. Do not set the role in one
web-editor execution and assume a later execution will reuse the same session.

Allowed test:

```sql
BEGIN;
SET LOCAL ROLE metro_analyst_lab;
SELECT current_user, ticket_id, status
FROM metro_support.analyst_ticket_summary ORDER BY ticket_id;
ROLLBACK;
```

You should be able to read 12 tickets under `metro_analyst_lab`. If Supabase's
editor shows only the final command status, use the Colab cell below to display
each result through one persistent connection. You do not need to install a
desktop client or rely on another person's screen.

Now run the same batch structure with the SELECT replaced by
`SELECT email FROM metro_support.users;`. It must fail with a permission error.
Run `ROLLBACK;` after an expected error if your client reports an aborted
transaction.

For the analyst's actual report, write a query against the **view** that returns
each `status` and its ticket count. Use `GROUP BY`, as in Week 2, and execute it
under `metro_analyst_lab` inside the same transaction pattern. The counts should
sum to 12. This verifies that the limited interface supports useful work without
granting the analyst direct access to the source tables. Add the query to the
Python `tests` list too if you use the display cell below.

Finally, use the same structure to try:

```sql
UPDATE metro_support.tickets SET priority = 'high' WHERE ticket_id = 1004;
```

It must also fail. The surrounding rollback protects the practice data even if
you discover an overly broad grant. Leave expected-failure batches commented in
your submitted file and record the short error, not an entire screen.

### Visible Results in Colab

Open a blank notebook in [Colab](https://colab.research.google.com/). Run this one
cell after the setup SQL. Copy your Supabase **session-pooler** connection URI
from Connect, including its database password, into the hidden prompt. The
session pooler provides an IPv4-compatible route when the direct host cannot be
reached. Do not use an API key or paste the URI into source code.

```python
%pip -q install "psycopg[binary]"
from getpass import getpass
import psycopg
from psycopg import sql

tests = [
    ("metro_analyst_lab", "SELECT current_user, ticket_id, status FROM metro_support.analyst_ticket_summary ORDER BY ticket_id"),
    ("metro_analyst_lab", "SELECT email FROM metro_support.users"),
    ("metro_analyst_lab", "UPDATE metro_support.tickets SET priority = 'high' WHERE ticket_id = 1004"),
]

# Each transaction rolls back, even if a write unexpectedly succeeds.
with psycopg.connect(getpass("Session-pooler URI (hidden): "),
                    sslmode="require", connect_timeout=10) as connection:
    for role, query in tests:
        try:
            with connection.transaction(force_rollback=True):
                connection.execute(sql.SQL("SET LOCAL ROLE {}").format(sql.Identifier(role)))
                cursor = connection.execute(query)
                print(role, cursor.fetchall() if cursor.description else cursor.rowcount)
        except psycopg.Error as error:
            print(role, "SQLSTATE", error.sqlstate, str(error).splitlines()[0])
```

Expect 12 rows, then two permission errors with SQLSTATE `42501`. An authentication
or network error is a setup problem, not a successful denial test. `sslmode=require`
encrypts this classroom connection; production server-identity verification uses
`verify-full` and the provider's CA configuration.

The Python cell only displays your SQL tests. Put the observed result and short
errors in your submitted SQL comments; this display notebook is not an additional
deliverable. The connection closes automatically when the `with` block exits.

## 3. Explain and Clean Up

In a few SQL-comment sentences, state what the analyst can do, which tests show
the boundary, and why testing only as the owner would give a misleading answer.

Run this cleanup as your administrative user after the tests:

```sql
REVOKE SELECT ON metro_support.analyst_ticket_summary FROM metro_analyst_lab;
REVOKE USAGE ON SCHEMA metro_support FROM metro_analyst_lab;
REVOKE metro_analyst_lab FROM CURRENT_USER;
DROP ROLE metro_analyst_lab;
```

**Submit:** `week_06_least_privilege.sql` containing setup, tests, your short
explanation, and cleanup. No password, screenshot, or additional report is needed.
