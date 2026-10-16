# Corrections to the Course Materials

Updated October 9, 2026. These corrections are included in the refreshed
[textbook PDF](Operating_Cloud_Databases.pdf) and current weekly materials.
The current weekly lab pages give the required work; the textbook also supports
independent study, where companion notebooks may be optional.

## Appendix C setup in Supabase SQL Editor

Earlier PDFs relied on `SET search_path` from an earlier request. A later
SQL Editor request may use another session, so an unqualified `INSERT INTO users`
can fail or target the wrong schema.

The refreshed Appendix C qualifies every baseline table reference with
`metro_support.`. Run those blocks in order; they can use separate connections.

Use the complete [Metro Support setup SQL](week_02/data/postgres_setup.sql) as
**one execution** in your personal practice database as an alternative to the
printed baseline blocks. It resets `metro_support`; use it only when starting
fresh, not between steps of an unfinished migration or lab. Expect 8 users,
12 tickets, and 21 events.

If using an older PDF, download the refreshed copy or use the linked setup SQL.

## Chapter 4 and Week 5 transaction results

A web editor may show only the last result of a block. Keep each transaction in
one execution; do not split BEGIN and ROLLBACK across separate browser requests.
Use a persistent `psql` session for the textbook examples or the
[Week 5 result-display helper](week_05/lab_01_transaction_outcomes.md#show-transaction-results-in-colab)
to see each SELECT and UPDATE result. An empty UPDATE result is not an SQL error.

## Chapter 5 sessions and PIDs

A session is a database conversation on a connection. PostgreSQL uses a server
process, called a backend, to serve it. Its **PID** is a process identifier, not
a user or ticket identifier. `SELECT pg_backend_pid();` returns the backend PID
for the current connection. A waiting session's `pg_blocking_pids` list identifies
its blockers. Use IDs observed in your own run, not numbers from an example.

## Chapter 13 encrypted PostgreSQL connection

Copy the Session pooler URI from Supabase's Connect panel. Replace the password
placeholder and percent-encode reserved characters in the password. If `sslmode`
is absent, append `?sslmode=require`, or `&sslmode=require` when the URI already
has query parameters. Retain an existing `verify-ca` or `verify-full` setting.
Use this corrected example after loading the Metro Support fixture:

```python
from getpass import getpass
import psycopg
from psycopg.conninfo import conninfo_to_dict

database_url = getpass("PostgreSQL connection URL (hidden): ")
try:
    try:
        parameters = conninfo_to_dict(database_url)
    except psycopg.ProgrammingError:
        raise ValueError("Malformed connection URI. Check password encoding.") from None
    sslmode = parameters.get("sslmode", "prefer")
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        raise ValueError("Add sslmode=require to the URI query parameters.")
    with psycopg.connect(database_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SET LOCAL statement_timeout = '10s'")
            cursor.execute("SELECT count(*) FROM metro_support.tickets")
            print(cursor.fetchone())
except psycopg.Error as error:
    raise RuntimeError(
        f"PostgreSQL read failed ({type(error).__name__}, "
        f"SQLSTATE {error.sqlstate or 'not supplied'}). Check the session-pooler URL, "
        "database password, TLS mode, and existing practice table."
    ) from None
finally:
    database_url = None
```

`require` encrypts the classroom connection. Production server identity checking
uses `verify-full` and the provider's CA configuration. Do not share the URI.

## Open the current notebooks

The refreshed PDF links to the corrected notebook snapshot. Weekly pages also
open the current notebooks, especially [Week 5](week_05/README.md),
[Week 8](week_08/README.md), and [Week 13](week_13/README.md).
The recovery notebook now preserves every verification result with PostgreSQL 14.
For the public-data notebook, finish the vendor/product comparison before setting
`RUN_CLEANUP = True`; the ordinary Run all leaves the practice database open.

Older downloaded handouts may use earlier synthetic display names. Current
handouts and datasets use the updated labels. Compare stable numeric IDs and
the data loaded for your exercise; changing a display name does not change a
record's identity. Do not reset completed work merely to change names.

## Schedule and submissions

The syllabus now matches the Fall Week 3 views/migration lesson and Week 4 SQL
reporting lesson. Week 3 and the Week 8 review include keys and constraints.
For Week 5 Lab 2, submit the sharing link to your completed saved Colab copy and
give the instructor viewer access, as the lab page explains.

Follow the [Week 13 holiday plan](week_13/README.md#fall-2026-holiday-week-plan)
and the final project's Brightspace demonstration schedule. These adjustments
add no separate graded reports or checkpoint submissions. For Supabase Free,
submit reproducible final-project files; no paid Dashboard role is required.

Prose: CC BY-NC-SA 4.0. Code: MIT. See the course license notices.
