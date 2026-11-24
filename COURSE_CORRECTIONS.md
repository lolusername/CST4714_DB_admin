# Corrections to the Course Materials

Updated November 24, 2026. The [textbook PDF](Operating_Cloud_Databases.pdf)
includes the earlier October corrections and the updated Chapter 12 Atlas backup
availability explanation. The class-plan and submission changes belong here
and in the weekly materials; the textbook remains an independent study resource.
The current weekly lab pages give the required work; the textbook also supports
independent study, where companion notebooks may be optional.

## Calendar correction: Thanksgiving is Week 13

Week 12 was November 17 and 19, 2026. Week 13 meets only Tuesday, November 24;
Thursday, November 26 is closed. The [Week 13 page](week_13/README.md) has the
required real-Atlas CISA import, verification, and short grouping lab. Submit
one viewable Colab link; there is no separate report or recovery assignment.

The [Week 12 recovery lesson](week_12/README.md) and its
[Atlas notebook](week_12/materials/notebooks/05_mongodb_atlas_recovery.ipynb)
remain available as a condensed reference route. Earlier labels that called
Week 12 Thanksgiving week were incorrect. Its older written and mock-database exercises remain available as optional references.

The notebook's connection check and synthetic write/read take place on Atlas.
Use the replica-set and election illustrations to trace the steps of failover. Save the recovery artifact outside the Colab runtime before ending it.

## Chapter 12 Atlas backup availability

The older statement that native Atlas backups are unavailable on every Free
cluster is no longer current. MongoDB now documents an optional, billed Free
Cluster Backup subscription in private preview; it may not appear for every
account. The course uses the free manual backup exercise.
The class uses a retained logical export and verifies a restore into a separate
practice collection. See [MongoDB's current backup options](https://www.mongodb.com/docs/atlas/backup-restore-cluster/).

The dated Atlas screenshot in Chapter 12 illustrates the earlier account state.
Use the screenshot to locate the setting, then check the current status in the teaching account. The Free tier
still does not support user-triggered primary failover tests or a sharded cluster;
see the [current Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/).

## Notebook submissions

When the weekly assignment requires a completed notebook, hand in its
**viewable Colab link**. Retain the required results
and explanation in your own saved Drive copy. When a notebook supports a written response or project, submit the item named on the lab page.

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
to see each SELECT and UPDATE result. An empty UPDATE result means no rows were returned. Inspect the filter, role, and starting state.

## Chapter 5 sessions and PIDs

A session is a database conversation on a connection. PostgreSQL uses a server
process, called a backend, to serve it. Its **PID** identifies the database process. `SELECT pg_backend_pid();` returns the backend PID
for the current connection. A waiting session's `pg_blocking_pids` list identifies
its blockers. Use the process IDs observed in your session.

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
handouts and datasets use the updated labels. Use stable numeric IDs to identify the records in the data loaded for your exercise. Do not reset completed work merely to change names.

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
