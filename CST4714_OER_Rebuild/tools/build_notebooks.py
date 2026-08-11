"""Build the public educational notebooks from reviewed source cells.

Notebook prose is CC BY-NC-SA 4.0. Notebook code is MIT licensed.
"""

import json
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"


def markdown(text: str):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text: str):
    return nbf.v4.new_code_cell(text.strip())


def build_relational_sql_review() -> None:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "01_relational_sql_review.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    }

    notebook["cells"] = [
        markdown(
            """
# Relational Model and SQL Review Studio

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/01_relational_sql_review.ipynb)

This notebook rebuilds the SQL ideas that later database-administration work
depends on. It is intentionally direct: each code cell runs SQL, and each
Markdown section explains what the result means.

**By the end, you will be able to:**

- translate selection, projection, join, difference, and grouping into SQL;
- state what one result row represents;
- predict where duplicate rows and `NULL` values come from;
- verify a query with a second reasoning path; and
- test a data change inside a transaction without keeping it.

The data is synthetic. No account, password, or cloud connection is required.
"""
        ),
        markdown(
            """
## How to Use This Notebook

Run cells from top to bottom. Before each query cell, read the prediction prompt
and say what you expect. After the result appears, compare it with your prediction.

We use DuckDB because it runs a relational SQL engine inside the notebook. The
course's cloud database is PostgreSQL, so some administrative syntax will differ,
but the relational reasoning and review queries here transfer directly.
"""
        ),
        code(
            """
# Install DuckDB in the notebook runtime. This does not create an online account.
%pip -q install duckdb
"""
        ),
        code(
            """
import duckdb

# This database exists only in the notebook session. Closing the runtime removes it.
con = duckdb.connect()
print("DuckDB is ready:", duckdb.__version__)
"""
        ),
        markdown(
            """
## 1. Create a Small Relational Instance

A **relation schema** names the attributes and their domains. A **relation
instance** is the current set of tuples. In SQL, we define tables and then insert
rows.

The setup cell is longer than later cells because it creates all three relations.
You do not need to memorize it. Notice the primary keys and the identifiers that
connect tickets to users and events to tickets.
"""
        ),
        code(
            """
con.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    display_name VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    neighborhood VARCHAR NOT NULL
);

CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    requester_id INTEGER NOT NULL,
    assignee_id INTEGER,
    category VARCHAR NOT NULL,
    priority VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    subject VARCHAR NOT NULL,
    opened_at TIMESTAMP NOT NULL
);

CREATE TABLE ticket_events (
    event_id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL,
    actor_id INTEGER NOT NULL,
    event_type VARCHAR NOT NULL,
    event_at TIMESTAMP NOT NULL
);

INSERT INTO users VALUES
    (101, 'Maya Chen', 'resident', 'Harbor'),
    (102, 'Luis Rivera', 'resident', 'Northside'),
    (201, 'Priya Shah', 'agent', 'Central'),
    (202, 'Noah Williams', 'agent', 'Northside');

INSERT INTO tickets VALUES
    (1001, 101, 201, 'streetlight', 'high', 'open',
     'Streetlight dark near bus stop', '2026-02-01 23:10:00'),
    (1002, 102, 202, 'sanitation', 'medium', 'in_progress',
     'Missed recycling pickup', '2026-02-02 15:45:00'),
    (1003, 101, 201, 'water', 'urgent', 'resolved',
     'Low water pressure', '2026-02-03 12:05:00'),
    (1004, 102, NULL, 'parks', 'low', 'new',
     'Broken bench slat', '2026-02-04 17:20:00'),
    (1005, 101, 202, 'sanitation', 'high', 'resolved',
     'Overflowing corner bin', '2026-02-05 14:00:00'),
    (1006, 102, 201, 'streetlight', 'medium', 'in_progress',
     'Flickering lamp outside library', '2026-02-06 01:30:00');

INSERT INTO ticket_events VALUES
    (5001, 1001, 101, 'created', '2026-02-01 23:10:00'),
    (5002, 1001, 201, 'assigned', '2026-02-02 14:05:00'),
    (5003, 1002, 102, 'created', '2026-02-02 15:45:00'),
    (5004, 1002, 202, 'status_changed', '2026-02-03 13:30:00'),
    (5005, 1003, 101, 'created', '2026-02-03 12:05:00'),
    (5006, 1003, 201, 'status_changed', '2026-02-03 14:25:00'),
    (5007, 1003, 201, 'status_changed', '2026-02-03 19:40:00'),
    (5008, 1004, 102, 'created', '2026-02-04 17:20:00'),
    (5009, 1005, 202, 'status_changed', '2026-02-05 20:15:00');
''')

print("Created users, tickets, and ticket_events.")
"""
        ),
        markdown(
            """
### Verify Before Querying

Expected counts come from the setup: 4 users, 6 tickets, and 9 events. A count
check proves the number of rows loaded; it does not prove that every value is
correct.
"""
        ),
        code(
            """
con.sql('''
SELECT 'users' AS relation_name, count(*) AS row_count FROM users
UNION ALL
SELECT 'tickets', count(*) FROM tickets
UNION ALL
SELECT 'ticket_events', count(*) FROM ticket_events
ORDER BY relation_name;
''').show()
"""
        ),
        markdown(
            """
## 2. Selection Keeps Rows; Projection Keeps Attributes

Relational-algebra reasoning:

```text
pi ticket_id, subject, priority (
  sigma priority = 'high' (tickets)
)
```

SQL writes projection in `SELECT` and selection in `WHERE`. Before running the
next cell, predict the number of rows and the three output attributes.
"""
        ),
        code(
            """
con.sql('''
SELECT ticket_id, subject, priority
FROM tickets
WHERE priority = 'high'
ORDER BY ticket_id;
''').show()
"""
        ),
        markdown(
            """
### Your Turn: Change One Predicate

Run the starter query. Then change it so the result contains active tickets with
either `medium` or `high` priority. In this course, active means `new`, `open`, or
`in_progress`. Predict the result grain before you edit.
"""
        ),
        code(
            """
# Grain: one row per ticket.
# Edit the predicates, run the query, and compare with your prediction.
con.sql('''
SELECT ticket_id, priority, status, subject
FROM tickets
WHERE status IN ('open', 'in_progress')
  AND priority IN ('medium', 'high')
ORDER BY opened_at;
''').show()
"""
        ),
        markdown(
            """
## 3. SQL Usually Preserves Duplicates

Classical relational algebra uses sets. SQL query results usually use bag
semantics. Priya is assigned to three tickets, so projecting only `assignee_id`
can repeat her identifier.
"""
        ),
        code(
            """
print("Ordinary projection:")
con.sql("SELECT assignee_id FROM tickets ORDER BY assignee_id;").show()

print("Projection with duplicate removal:")
con.sql("SELECT DISTINCT assignee_id FROM tickets ORDER BY assignee_id;").show()
"""
        ),
        markdown(
            """
`DISTINCT` is correct only when the question asks for unique values. It should not
be used to hide rows created by an incorrect join.

Also notice the missing assignee. `NULL` is not zero or an empty string. Test it
with `IS NULL`, not `= NULL`.
"""
        ),
        code(
            """
con.sql('''
SELECT ticket_id, subject
FROM tickets
WHERE assignee_id IS NULL;
''').show()
"""
        ),
        markdown(
            """
## 4. A Join Pairs Related Tuples

A Cartesian product of 6 tickets and 4 users contains 24 pairs. The join condition
keeps pairs where `tickets.assignee_id = users.user_id`.

Predict why the result below has five rows rather than six.
"""
        ),
        code(
            """
con.sql('''
SELECT
    t.ticket_id,
    t.subject,
    u.display_name AS assignee_name
FROM tickets AS t
JOIN users AS u
    ON u.user_id = t.assignee_id
ORDER BY t.ticket_id;
''').show()
"""
        ),
        markdown(
            """
An inner join removes ticket 1004 because its assignee is unknown. If the question
requires every ticket, use a left join. The left-side ticket remains and the
right-side attributes become `NULL` when no match exists.
"""
        ),
        code(
            """
con.sql('''
SELECT
    t.ticket_id,
    t.subject,
    u.display_name AS assignee_name
FROM tickets AS t
LEFT JOIN users AS u
    ON u.user_id = t.assignee_id
ORDER BY t.ticket_id;
''').show()
"""
        ),
        markdown(
            """
## 5. One-to-Many Joins Change the Grain

A ticket can have many events. The next result is one row per event, not one row
per ticket. Predict how many rows ticket 1003 will produce, then run the query.
"""
        ),
        code(
            """
con.sql('''
SELECT t.ticket_id, t.subject, e.event_id, e.event_type, e.event_at
FROM tickets AS t
JOIN ticket_events AS e
    ON e.ticket_id = t.ticket_id
WHERE t.ticket_id = 1003
ORDER BY e.event_at;
''').show()
"""
        ),
        markdown(
            """
Three rows are correct because the result grain is one event. If a report needs
one row per ticket, aggregate the events or choose one event intentionally. Do not
add `DISTINCT` until you understand the grain.
"""
        ),
        markdown(
            """
## 6. Grouping Changes the Grain

The next result is one row per category. `count(*)` counts tickets in each group.
Conditional aggregation counts only tickets whose status is unresolved.
"""
        ),
        code(
            """
con.sql('''
SELECT
    category,
    count(*) AS ticket_count,
    count(*) FILTER (
        WHERE status IN ('new', 'open', 'in_progress')
    ) AS unresolved_count,
    max(opened_at) AS latest_opened_at
FROM tickets
GROUP BY category
ORDER BY unresolved_count DESC, category;
''').show()
"""
        ),
        markdown(
            """
### Verify a Group Independently

The grouped query is compact, so verify one category with a simpler filtered
query. This is a different reasoning path, not the same query copied twice.
"""
        ),
        code(
            """
con.sql('''
SELECT ticket_id, status
FROM tickets
WHERE category = 'streetlight'
ORDER BY ticket_id;
''').show()
"""
        ),
        markdown(
            """
## 7. Difference Answers "In the First, Not the Second"

`EXCEPT` is SQL's set-difference operator. The next question asks for users who
appear as requesters but not as assignees.
"""
        ),
        code(
            """
con.sql('''
SELECT requester_id AS user_id
FROM tickets
EXCEPT
SELECT assignee_id
FROM tickets
WHERE assignee_id IS NOT NULL
ORDER BY user_id;
''').show()
"""
        ),
        markdown(
            """
## 8. A CTE Names an Intermediate Relation

Read the query from the inside out. `active_tickets` is a named intermediate
relation. The outer query joins that result to users and groups by agent.
"""
        ),
        code(
            """
con.sql('''
WITH active_tickets AS (
    SELECT ticket_id, assignee_id
    FROM tickets
    WHERE status IN ('new', 'open', 'in_progress')
)
SELECT
    u.display_name,
    count(a.ticket_id) AS active_ticket_count
FROM users AS u
LEFT JOIN active_tickets AS a
    ON a.assignee_id = u.user_id
WHERE u.role = 'agent'
GROUP BY u.user_id, u.display_name
ORDER BY active_ticket_count DESC, u.display_name;
''').show()
"""
        ),
        markdown(
            """
## 9. Preview, Change, Return, Verify, Roll Back

Before changing data, use the intended predicate in a `SELECT`. Then use a
transaction and `RETURNING`. This notebook rolls the change back, so the original
state returns.
"""
        ),
        code(
            """
print("Preview the exact target:")
con.sql('''
    SELECT ticket_id, priority
    FROM tickets
    WHERE ticket_id = 1006;
''').show()

con.execute("BEGIN")

print("Change visible inside the transaction:")
con.sql('''
    UPDATE tickets
    SET priority = 'high'
    WHERE ticket_id = 1006
    RETURNING ticket_id, priority;
''').show()

con.execute("ROLLBACK")

print("Original state restored after rollback:")
con.sql('''
    SELECT ticket_id, priority
    FROM tickets
    WHERE ticket_id = 1006;
''').show()
"""
        ),
        markdown(
            """
## 10. Explain What the Evidence Proves

Write short answers in a new Markdown cell or your lab file:

1. Which query changed its result grain, and what did one output row represent?
2. Why did the left join preserve a row that the inner join removed?
3. What did the independent streetlight query verify? What did it not prove?
4. Which relational-algebra operation did `EXCEPT` express?
5. What evidence shows that the priority update was not kept?

## Readiness Check

You are ready to continue when you can predict and explain the queries, not just
run them. If one section is unclear, edit its query, use smaller projections, and
inspect one identifier at a time.

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic example data CC0.
"""
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "01_relational_sql_review.ipynb"
    nbf.write(notebook, output)


def build_transactions_locks() -> None:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "02_postgres_transactions_locks.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    }

    notebook["cells"] = [
        markdown(
            """
# PostgreSQL Transactions and Lock Diagnosis

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/02_postgres_transactions_locks.ipynb)

This notebook creates one controlled blocking relationship in a disposable schema,
identifies the blocked and blocking sessions, resolves the blocker, and verifies
the final row.

**The central idea:** a wait is a relationship between database sessions. Diagnose
that relationship before terminating or changing anything.

The cloud path asks for a temporary PostgreSQL URL with `getpass`, so the value is
not displayed or written into the notebook. The fallback path supplies a complete
incident transcript when a cloud connection is unavailable.
"""
        ),
        markdown(
            """
## Before You Connect

1. Use a personal course database, never a production system.
2. In Supabase, prefer the session-pooler URI if your network cannot reach the
   direct IPv6 endpoint.
3. Rotate the temporary password after class if required by your course policy.
4. Never paste a URL into a code or Markdown cell.

The URL must request `sslmode=require`, `verify-ca`, or `verify-full`; the
notebook rejects libpq's default `prefer` mode because it can fall back to an
unencrypted connection. For production, use `verify-full` with the Supabase CA
certificate. `require` encrypts the classroom connection but does not verify the
CA or hostname.

Set `USE_CLOUD` to `True` only when you are ready. It remains `False` in the public
notebook so all non-cloud cells can run safely without credentials.
"""
        ),
        code(
            r'''
%pip -q install "psycopg[binary]"
'''
        ),
        code(
            r'''
from getpass import getpass
import threading
import time

import psycopg
from psycopg.conninfo import conninfo_to_dict

USE_CLOUD = False  # Change to True during the in-class cloud lab.
print("Cloud path enabled:", USE_CLOUD)
'''
        ),
        markdown(
            """
## 1. Open Three Clearly Named Sessions

- **Session A** will update a row and deliberately remain uncommitted.
- **Session B** will attempt a competing update and wait.
- **Diagnostic session** will query PostgreSQL's activity evidence.

Three connections make the roles visible. The diagnostic session does not cause
or resolve the block; it observes it.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    database_url = getpass("Paste the temporary PostgreSQL connection URL: ")

    sslmode = conninfo_to_dict(database_url).get("sslmode", "prefer")
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        raise ValueError("Add sslmode=require or a stronger mode to the temporary URL.")

    session_a = psycopg.connect(
        database_url, application_name="cst4714_session_a", connect_timeout=10
    )
    session_b = psycopg.connect(
        database_url, application_name="cst4714_session_b", connect_timeout=10
    )
    diagnostic = psycopg.connect(
        database_url, application_name="cst4714_diagnostic", connect_timeout=10
    )
    diagnostic.autocommit = True

    print("Opened Session A, Session B, and the diagnostic session.")
else:
    print("Cloud path skipped. Continue to the fallback transcript below.")
'''
        ),
        markdown(
            """
## 2. Create a Disposable Target

The table has one row. Its original state is `priority = medium` and
`status = open`. Recreating the schema makes the exercise repeatable.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    with diagnostic.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS lock_lab CASCADE")
        cursor.execute("CREATE SCHEMA lock_lab")
        cursor.execute("""
            CREATE TABLE lock_lab.tickets (
                ticket_id integer PRIMARY KEY,
                priority text NOT NULL,
                status text NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO lock_lab.tickets (ticket_id, priority, status)
            VALUES (1004, 'medium', 'open')
        """)
        cursor.execute("SELECT * FROM lock_lab.tickets")
        print("Starting row:", cursor.fetchone())
else:
    print("Setup skipped because USE_CLOUD is False.")
'''
        ),
        markdown(
            """
## 3. Session A Holds an Uncommitted Row Change

Session A changes the priority but does not commit. PostgreSQL holds the row-level
write conflict until the transaction ends.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    with session_a.cursor() as cursor:
        cursor.execute("BEGIN")
        cursor.execute("""
            UPDATE lock_lab.tickets
            SET priority = 'high'
            WHERE ticket_id = 1004
            RETURNING ticket_id, priority, status
        """)
        print("Session A sees:", cursor.fetchone())
    print("Session A remains open and uncommitted.")
else:
    print("Session A step skipped.")
'''
        ),
        markdown(
            """
## 4. Session B Starts a Competing Update

The notebook uses one small background thread because a blocked query cannot both
wait and let the same notebook cell continue to collect diagnostics. The thread
contains only Session B's query; all database actions remain visible below.
"""
        ),
        code(
            r'''
blocked_result = {}

def run_session_b_update():
    try:
        with session_b.cursor() as cursor:
            cursor.execute("SET statement_timeout = '15s'")
            cursor.execute("""
                UPDATE lock_lab.tickets
                SET status = 'in_progress'
                WHERE ticket_id = 1004
                RETURNING ticket_id, priority, status
            """)
            blocked_result["row"] = cursor.fetchone()
        session_b.commit()
        blocked_result["outcome"] = "committed after blocker released"
    except Exception as error:
        session_b.rollback()
        blocked_result["outcome"] = f"error: {type(error).__name__}: {error}"


if USE_CLOUD:
    session_b_thread = threading.Thread(target=run_session_b_update)
    session_b_thread.start()
    time.sleep(1)
    print("Session B update started. Thread still waiting:", session_b_thread.is_alive())
else:
    print("Session B step skipped.")
'''
        ),
        markdown(
            """
## 5. Ask PostgreSQL Who Is Blocking Whom

`pg_blocking_pids(blocked.pid)` directly reports the blocker relationship. The
wait event adds context. A PID is evidence, not automatic permission to terminate
a process.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    diagnostic_sql = """
        SELECT
            blocked.pid AS blocked_pid,
            blocked.application_name AS blocked_app,
            blocked.wait_event_type,
            blocked.wait_event,
            pg_blocking_pids(blocked.pid) AS blocking_pids,
            blocker.pid AS blocking_pid,
            blocker.application_name AS blocking_app,
            blocker.xact_start AS blocker_transaction_start,
            left(blocked.query, 90) AS blocked_query
        FROM pg_stat_activity AS blocked
        CROSS JOIN LATERAL unnest(pg_blocking_pids(blocked.pid)) AS p(blocking_pid)
        JOIN pg_stat_activity AS blocker
          ON blocker.pid = p.blocking_pid
        WHERE blocked.datname = current_database()
          AND blocked.application_name = 'cst4714_session_b'
    """
    with diagnostic.cursor() as cursor:
        cursor.execute(diagnostic_sql)
        columns = [description.name for description in cursor.description]
        rows = cursor.fetchall()
    print(columns)
    for row in rows:
        print(row)
else:
    print("Diagnostic query skipped.")
'''
        ),
        markdown(
            """
## 6. Resolve the Blocker and Verify the Final State

This controlled exercise rolls back Session A. That releases its row lock without
keeping the priority change. Session B can then finish and commit its status
change. A fresh diagnostic query verifies which values remain.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    session_a.rollback()
    print("Rolled back Session A.")

    session_b_thread.join(timeout=20)
    print("Session B outcome:", blocked_result)

    with diagnostic.cursor() as cursor:
        cursor.execute("SELECT ticket_id, priority, status FROM lock_lab.tickets")
        final_row = cursor.fetchone()
    print("Final row from a fresh statement:", final_row)
else:
    print("Resolution step skipped.")
'''
        ),
        markdown(
            """
## 7. Close Connections and Remove the Disposable Schema

Cleanup is part of the operation. It prevents an old practice lock or test table
from becoming a later mystery.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    with diagnostic.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS lock_lab CASCADE")

    session_a.close()
    session_b.close()
    diagnostic.close()
    database_url = None
    print("Closed all sessions and removed lock_lab.")
else:
    print("No cloud resources were opened.")
'''
        ),
        markdown(
            """
## Offline Fallback Incident Transcript

Use this transcript when the cloud path cannot run. It represents the same
controlled experiment:

```text
Starting row: (1004, 'medium', 'open')

Session A PID 7310, application cst4714_session_a
Transaction began: 2026-03-05 18:42:10+00
Uncommitted query: UPDATE lock_lab.tickets SET priority = 'high'
                   WHERE ticket_id = 1004

Session B PID 7332, application cst4714_session_b
State: active
wait_event_type: Lock
wait_event: transactionid
pg_blocking_pids(7332): {7310}
Query: UPDATE lock_lab.tickets SET status = 'in_progress'
       WHERE ticket_id = 1004

Action: ROLLBACK issued in Session A.
Session B outcome: committed after blocker released.
Final row: (1004, 'medium', 'in_progress')
```

The transcript proves one blocking relationship, the chosen resolution, and the
final state. It does not prove how a production application should choose between
waiting, rollback, cancellation, or termination.
"""
        ),
        markdown(
            """
## Incident Record: Complete Before Submission

Edit this cell with your own cloud evidence or the fallback transcript.

**Blocked session:** [PID, application name, wait event, and query]

**Blocking session:** [PID, application name, and transaction start]

**Relationship evidence:** [the exact `pg_blocking_pids` result]

**Resolution:** [what ended the blocking transaction and why that action was safe
in this lab]

**Final verification:** [the final row and which change remained]

**Limitation:** [one thing this controlled test does not prove about production]

**Credential check:** I confirm that no connection URL, password, or key appears
in this notebook source or output. [replace with yes after checking]

**License:** prose CC BY-NC-SA 4.0; code MIT.
"""
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "02_postgres_transactions_locks.ipynb"
    nbf.write(notebook, output)


def build_postgres_backup_restore() -> None:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "03_postgres_backup_restore.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    }

    notebook["cells"] = [
        markdown(
            """
# PostgreSQL Logical Backup, Restore, and Verification

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/03_postgres_backup_restore.ipynb)

This notebook performs a real PostgreSQL logical backup and restores it into a
different database. The databases are temporary and isolated, so the lab teaches
the full evidence chain without risking a Supabase project.

**Evidence chain:** source checks -> dump artifact -> artifact inspection ->
separate restore -> structure checks -> data checks -> behavior check.

No cloud credential is required. The final section translates the same procedure
to Supabase without storing a connection URL.
"""
        ),
        markdown(
            """
## 1. Prepare PostgreSQL in the Notebook Runtime

Google Colab does not start with a PostgreSQL server, so the next cell installs
the free PostgreSQL package when it detects Colab and starts a local service. On a
computer where PostgreSQL is already running, it uses the current local server.

The command prefix is shown explicitly. It changes only because Colab's local
server is owned by its `postgres` operating-system user.
"""
        ),
        code(
            r'''
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess

IN_COLAB = "COLAB_RELEASE_TAG" in os.environ

if IN_COLAB and shutil.which("pg_dump") is None:
    subprocess.run(["apt-get", "-qq", "update"], check=True)
    subprocess.run(
        ["apt-get", "-qq", "install", "-y", "postgresql", "postgresql-client"],
        check=True,
    )

if IN_COLAB:
    subprocess.run(["service", "postgresql", "start"], check=True)

PG_PREFIX = ["sudo", "-u", "postgres"] if IN_COLAB else []
print("Running in Colab:", IN_COLAB)
print("PostgreSQL command prefix:", PG_PREFIX or "current local user")

readiness = subprocess.run(
    PG_PREFIX + ["pg_isready"],
    check=True,
    text=True,
    capture_output=True,
)
print(readiness.stdout.strip())

server_version_result = subprocess.run(
    PG_PREFIX + ["psql", "--tuples-only", "--no-align", "--command", "SHOW server_version_num"],
    check=True,
    text=True,
    capture_output=True,
)
server_version_num = int(server_version_result.stdout.strip())
server_major = server_version_num // 10000

candidate_directories = []
path_pg_dump = shutil.which("pg_dump")
if path_pg_dump:
    candidate_directories.append(Path(path_pg_dump).parent)
candidate_directories.extend(
    [
        Path(f"/Applications/Postgres.app/Contents/Versions/{server_major}/bin"),
        Path(f"/usr/lib/postgresql/{server_major}/bin"),
    ]
)

PG_BIN = None
for candidate_directory in candidate_directories:
    candidate_dump = candidate_directory / "pg_dump"
    if not candidate_dump.exists():
        continue
    version_text = subprocess.run(
        [str(candidate_dump), "--version"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    version_match = re.search(r"(\d+)(?:\.\d+)?", version_text)
    if version_match and int(version_match.group(1)) >= server_major:
        PG_BIN = candidate_directory
        break

if PG_BIN is None:
    raise RuntimeError(
        f"PostgreSQL server major version {server_major} needs pg_dump {server_major} "
        "or newer. Install a compatible PostgreSQL client and rerun this cell."
    )

PSQL = str(PG_BIN / "psql")
CREATEDB = str(PG_BIN / "createdb")
DROPDB = str(PG_BIN / "dropdb")
PG_DUMP = str(PG_BIN / "pg_dump")
PG_RESTORE = str(PG_BIN / "pg_restore")

print("Server major version:", server_major)
print("Compatible client directory:", PG_BIN)
print(subprocess.run([PG_DUMP, "--version"], check=True, text=True, capture_output=True).stdout.strip())
'''
        ),
        markdown(
            """
## 2. Create a Source Database

The source and restore databases have visibly different names. The setup contains
keys, relationships, a status constraint, and a few rows so later checks can test
more than counts.
"""
        ),
        code(
            r'''
SOURCE_DB = "cst4714_recovery_source"
RESTORE_DB = "cst4714_recovery_restore"
SETUP_FILE = Path("/tmp/cst4714_metro_support_setup.sql")
DUMP_FILE = Path("/tmp/cst4714_metro_support.dump")

setup_sql = """
CREATE SCHEMA metro_support;

CREATE TABLE metro_support.users (
    user_id integer PRIMARY KEY,
    display_name text NOT NULL,
    role text NOT NULL
);

CREATE TABLE metro_support.tickets (
    ticket_id integer PRIMARY KEY,
    requester_id integer NOT NULL REFERENCES metro_support.users(user_id),
    status text NOT NULL CONSTRAINT tickets_status_allowed
        CHECK (status IN ('new', 'open', 'in_progress', 'resolved', 'closed')),
    subject text NOT NULL
);

CREATE TABLE metro_support.ticket_events (
    event_id integer PRIMARY KEY,
    ticket_id integer NOT NULL REFERENCES metro_support.tickets(ticket_id),
    event_type text NOT NULL
);

INSERT INTO metro_support.users VALUES
    (101, 'Maya Chen', 'resident'),
    (102, 'Luis Rivera', 'resident'),
    (201, 'Priya Shah', 'agent');

INSERT INTO metro_support.tickets VALUES
    (1001, 101, 'open', 'Streetlight dark near bus stop'),
    (1002, 102, 'in_progress', 'Missed recycling pickup'),
    (1003, 101, 'resolved', 'Low water pressure');

INSERT INTO metro_support.ticket_events VALUES
    (5001, 1001, 'created'),
    (5002, 1001, 'assigned'),
    (5003, 1002, 'created'),
    (5004, 1003, 'created'),
    (5005, 1003, 'status_changed');
"""

SETUP_FILE.write_text(setup_sql, encoding="utf-8")

for database_name in (RESTORE_DB, SOURCE_DB):
    subprocess.run(
        PG_PREFIX + [DROPDB, "--if-exists", database_name],
        check=True,
        text=True,
        capture_output=True,
    )

subprocess.run(PG_PREFIX + [CREATEDB, SOURCE_DB], check=True)
subprocess.run(
    PG_PREFIX
    + [PSQL, "--set=ON_ERROR_STOP=on", "--dbname", SOURCE_DB, "--file", str(SETUP_FILE)],
    check=True,
    text=True,
    capture_output=True,
)
print("Created source database:", SOURCE_DB)
'''
        ),
        markdown(
            """
## 3. Record the Source State

Expected source counts are 3 users, 3 tickets, and 5 events. We also inspect the
named status constraint. These checks become the baseline for the restored target.
"""
        ),
        code(
            r'''
source_check_sql = """
SELECT 'users=' || count(*) FROM metro_support.users;
SELECT 'tickets=' || count(*) FROM metro_support.tickets;
SELECT 'ticket_events=' || count(*) FROM metro_support.ticket_events;
SELECT 'constraint=' || conname
FROM pg_constraint
WHERE conname = 'tickets_status_allowed';
"""

source_check = subprocess.run(
    PG_PREFIX + [PSQL, "--tuples-only", "--no-align", "--dbname", SOURCE_DB, "--command", source_check_sql],
    check=True,
    text=True,
    capture_output=True,
)
print(source_check.stdout.strip())
'''
        ),
        markdown(
            """
## 4. Create the Logical Backup Artifact

`pg_dump --format=custom` creates an archive for `pg_restore`. `--no-owner` and
`--no-privileges` make the classroom restore less dependent on identical roles,
but they also mean ownership and grants need a separate recovery plan.
"""
        ),
        code(
            r'''
if DUMP_FILE.exists():
    DUMP_FILE.unlink()

subprocess.run(
    PG_PREFIX
    + [
        PG_DUMP,
        "--format=custom",
        "--schema=metro_support",
        "--no-owner",
        "--no-privileges",
        "--file",
        str(DUMP_FILE),
        SOURCE_DB,
    ],
    check=True,
)

dump_bytes = DUMP_FILE.read_bytes()
dump_sha256 = hashlib.sha256(dump_bytes).hexdigest()
print("Dump path:", DUMP_FILE)
print("Dump size in bytes:", len(dump_bytes))
print("SHA-256:", dump_sha256)
'''
        ),
        markdown(
            """
## 5. Inspect the Artifact Before Restoring

`pg_restore --list` reads the archive table of contents. Seeing the expected
schema, tables, data, constraints, and indexes is useful evidence, but it still
does not prove that restoration succeeds.
"""
        ),
        code(
            r'''
archive_list = subprocess.run(
    PG_PREFIX + [PG_RESTORE, "--list", str(DUMP_FILE)],
    check=True,
    text=True,
    capture_output=True,
)

important_lines = [
    line
    for line in archive_list.stdout.splitlines()
    if any(term in line for term in ("SCHEMA", "TABLE ", "TABLE DATA", "CONSTRAINT", "INDEX"))
]
print("\n".join(important_lines))
'''
        ),
        markdown(
            """
## 6. Restore Into a Different Database

The destination is empty and separate. `--exit-on-error` prevents an archive with
an early failure from looking successful merely because later items continued.
"""
        ),
        code(
            r'''
subprocess.run(PG_PREFIX + [CREATEDB, RESTORE_DB], check=True)

restore_result = subprocess.run(
    PG_PREFIX
    + [
        PG_RESTORE,
        "--exit-on-error",
        "--no-owner",
        "--no-privileges",
        "--dbname",
        RESTORE_DB,
        str(DUMP_FILE),
    ],
    check=True,
    text=True,
    capture_output=True,
)

print("Restored into separate database:", RESTORE_DB)
print("Restore exit code:", restore_result.returncode)
'''
        ),
        markdown(
            """
## 7. Verify Structure, Data, and Relationships

The following checks ask different questions:

- Do all three tables exist?
- Do row counts match the source baseline?
- Are there tickets with a missing requester relationship?
- Does a meaningful report return the expected grouped result?
"""
        ),
        code(
            r'''
restore_check_sql = """
SELECT 'tables=' || count(*)
FROM information_schema.tables
WHERE table_schema = 'metro_support' AND table_type = 'BASE TABLE';

SELECT 'users=' || count(*) FROM metro_support.users;
SELECT 'tickets=' || count(*) FROM metro_support.tickets;
SELECT 'ticket_events=' || count(*) FROM metro_support.ticket_events;

SELECT 'orphan_tickets=' || count(*)
FROM metro_support.tickets AS t
LEFT JOIN metro_support.users AS u ON u.user_id = t.requester_id
WHERE u.user_id IS NULL;

SELECT status || '=' || count(*)
FROM metro_support.tickets
GROUP BY status
ORDER BY status;
"""

restore_check = subprocess.run(
    PG_PREFIX + [PSQL, "--tuples-only", "--no-align", "--dbname", RESTORE_DB, "--command", restore_check_sql],
    check=True,
    text=True,
    capture_output=True,
)
print(restore_check.stdout.strip())
'''
        ),
        markdown(
            """
## 8. Verify Behavior With an Expected Failure

A restored table can contain rows while missing an integrity rule. This insert
must fail because `almost_done` is not an allowed status. We treat the nonzero
command result as expected evidence and print only the final error line.
"""
        ),
        code(
            r'''
invalid_insert = subprocess.run(
    PG_PREFIX
    + [
        PSQL,
        "--set=ON_ERROR_STOP=on",
        "--dbname",
        RESTORE_DB,
        "--command",
        """
        INSERT INTO metro_support.tickets
            (ticket_id, requester_id, status, subject)
        VALUES
            (1099, 101, 'almost_done', 'Constraint restore test');
        """,
    ],
    check=False,
    text=True,
    capture_output=True,
)

print("Expected nonzero exit code:", invalid_insert.returncode)
error_lines = [line for line in invalid_insert.stderr.splitlines() if line.strip()]
print("Expected constraint evidence:", error_lines[-1] if error_lines else "no error text")
assert invalid_insert.returncode != 0, "The restored status constraint did not reject invalid data."
'''
        ),
        markdown(
            """
## 9. Compare and Clean Up

The source and restore evidence should agree on required counts. Cleanup removes
the temporary databases only after all verification has finished. The dump file
remains in `/tmp` until the notebook runtime ends.
"""
        ),
        code(
            r'''
assert "users=3" in source_check.stdout and "users=3" in restore_check.stdout
assert "tickets=3" in source_check.stdout and "tickets=3" in restore_check.stdout
assert "ticket_events=5" in source_check.stdout and "ticket_events=5" in restore_check.stdout
assert "orphan_tickets=0" in restore_check.stdout

print("Required source and restore checks agree.")

for database_name in (RESTORE_DB, SOURCE_DB):
    subprocess.run(
        PG_PREFIX + [DROPDB, "--if-exists", database_name],
        check=True,
        text=True,
        capture_output=True,
    )

print("Removed temporary source and restore databases.")
'''
        ),
        markdown(
            """
## 10. Translate the Procedure to Supabase

Supabase Free projects do not receive the automatic database backups described
for paid plans. A course recovery plan therefore uses a logical connection and
runtime credential, for example:

```bash
pg_dump --format=custom --no-owner --no-privileges \
  --file=project.dump "$DATABASE_URL"

pg_restore --exit-on-error --no-owner --no-privileges \
  --dbname="$RESTORE_DATABASE_URL" project.dump
```

Use the current Supabase connection guidance. A direct endpoint may require IPv6;
the session pooler offers an IPv4-compatible path in many networks. The source and
restore URLs must point to different, approved targets. Enter URLs at runtime,
never in the notebook.

Official free resources:

- <https://supabase.com/docs/guides/platform/backups>
- <https://supabase.com/docs/guides/database/connecting-to-postgres>
- <https://www.postgresql.org/docs/current/backup-dump.html>
"""
        ),
        markdown(
            """
## Recovery Record: Complete Before Submission

**Failure scope:** [what this artifact is intended to recover]

**Artifact:** [format, file name, size, and abbreviated checksum]

**Safety boundary:** [how the restore target differs from the source]

**Five checks:** [two structure, two data/relationship, and one behavior check]

**What the checks do not prove:** [one limitation]

**Supabase translation:** [which connection path you would use and how you would
enter the source and restore URLs without saving them]

**RPO/RTO implication:** [what backup frequency and restore practice would be
needed for a stated requirement]

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic data CC0.
"""
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "03_postgres_backup_restore.ipynb"
    nbf.write(notebook, output)


def build_atlas_mql_modeling() -> None:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "04_atlas_mql_modeling.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    }

    notebook["cells"] = [
        markdown(
            """
# MongoDB Atlas, Basic MQL, and Document Modeling

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/04_atlas_mql_modeling.ipynb)

This notebook introduces MongoDB through direct, visible operations. You will
insert a small synthetic fixture, query nested fields and arrays, update one test
document, interpret write evidence, and compare embedded and referenced shapes.

The default path uses an in-memory MongoDB-compatible library. Set `USE_ATLAS` to
`True` only in class when your free Atlas cluster, database user, and temporary
network rule are ready.
"""
        ),
        markdown(
            """
## Atlas Connection Checklist

1. Use a Free cluster; no paid tier is required.
2. Create a database user distinct from your Atlas website account.
3. Add only the temporary network access needed for class and narrow or remove it
   afterward.
4. Copy the current driver connection URI.
5. Enter the URI only through `getpass` below.

Do not set `tlsInsecure=True`. A TLS error is a signal to check the current driver,
URI, DNS, network rule, system time, and certificate path.
"""
        ),
        code(
            r'''
%pip -q install pymongo mongomock
'''
        ),
        code(
            r'''
from datetime import datetime, timezone
from getpass import getpass

import mongomock
from pymongo import MongoClient
from pymongo.server_api import ServerApi

USE_ATLAS = False  # Change to True only when your Atlas setup is ready.
DATABASE_NAME = "cst4714_metro_support_practice"  # Make unique in a shared project.

if USE_ATLAS:
    mongodb_uri = getpass("Paste the temporary Atlas URI: ")
    client = MongoClient(
        mongodb_uri,
        server_api=ServerApi("1", strict=True, deprecation_errors=True),
        serverSelectionTimeoutMS=10000,
        timeoutMS=10000,
    )
    print("Atlas ping:", client.admin.command("ping"))
else:
    client = mongomock.MongoClient()
    print("Using the offline in-memory MongoDB-compatible path.")

database = client[DATABASE_NAME]
tickets = database["tickets"]
'''
        ),
        markdown(
            """
## 1. Load a Small, Reproducible Fixture

Every course document carries `course_fixture: "cst4714"`. Cleanup filters on that
marker instead of dropping an entire database. The fixture uses BSON dates through
Python `datetime` values, nested requester documents, tag arrays, and embedded
event arrays.
"""
        ),
        code(
            r'''
tickets.delete_many({"course_fixture": "cst4714"})

fixture = [
    {
        "ticket_id": 1001,
        "category": "streetlight",
        "priority": "high",
        "status": "open",
        "subject": "Streetlight dark near bus stop",
        "requester": {"user_id": 101, "display_name": "Maya Chen"},
        "assignee_id": 201,
        "opened_at": datetime(2026, 2, 1, 23, 10, tzinfo=timezone.utc),
        "tags": ["lighting", "safety"],
        "events": [
            {"event_id": 5001, "type": "created", "actor_role": "resident",
             "at": datetime(2026, 2, 1, 23, 10, tzinfo=timezone.utc)},
            {"event_id": 5002, "type": "assigned", "actor_role": "agent",
             "at": datetime(2026, 2, 2, 14, 5, tzinfo=timezone.utc)},
        ],
        "course_fixture": "cst4714",
    },
    {
        "ticket_id": 1002,
        "category": "sanitation",
        "priority": "medium",
        "status": "in_progress",
        "subject": "Missed recycling pickup",
        "requester": {"user_id": 102, "display_name": "Luis Rivera"},
        "assignee_id": 202,
        "opened_at": datetime(2026, 2, 2, 15, 45, tzinfo=timezone.utc),
        "tags": ["recycling"],
        "events": [
            {"event_id": 5003, "type": "created", "actor_role": "resident",
             "at": datetime(2026, 2, 2, 15, 45, tzinfo=timezone.utc)},
            {"event_id": 5004, "type": "status_changed", "actor_role": "agent",
             "at": datetime(2026, 2, 3, 13, 30, tzinfo=timezone.utc)},
        ],
        "course_fixture": "cst4714",
    },
    {
        "ticket_id": 1003,
        "category": "water",
        "priority": "urgent",
        "status": "resolved",
        "subject": "Low water pressure",
        "requester": {"user_id": 103, "display_name": "Amina Yusuf"},
        "assignee_id": 201,
        "opened_at": datetime(2026, 2, 3, 12, 5, tzinfo=timezone.utc),
        "tags": ["water", "building"],
        "events": [
            {"event_id": 5005, "type": "created", "actor_role": "resident",
             "at": datetime(2026, 2, 3, 12, 5, tzinfo=timezone.utc)},
            {"event_id": 5006, "type": "status_changed", "actor_role": "agent",
             "at": datetime(2026, 2, 3, 14, 25, tzinfo=timezone.utc)},
            {"event_id": 5007, "type": "status_changed", "actor_role": "agent",
             "at": datetime(2026, 2, 3, 19, 40, tzinfo=timezone.utc)},
        ],
        "course_fixture": "cst4714",
    },
    {
        "ticket_id": 1004,
        "category": "parks",
        "priority": "low",
        "status": "new",
        "subject": "Broken bench slat",
        "requester": {"user_id": 104, "display_name": "Jordan Bell"},
        "assignee_id": None,
        "opened_at": datetime(2026, 2, 4, 17, 20, tzinfo=timezone.utc),
        "tags": ["parks"],
        "events": [
            {"event_id": 5008, "type": "created", "actor_role": "resident",
             "at": datetime(2026, 2, 4, 17, 20, tzinfo=timezone.utc)}
        ],
        "course_fixture": "cst4714",
    },
    {
        "ticket_id": 1005,
        "category": "sanitation",
        "priority": "high",
        "status": "resolved",
        "subject": "Overflowing corner bin",
        "requester": {"user_id": 101, "display_name": "Maya Chen"},
        "assignee_id": 202,
        "opened_at": datetime(2026, 2, 5, 14, 0, tzinfo=timezone.utc),
        "tags": ["sanitation", "safety"],
        "events": [],
        "course_fixture": "cst4714",
    },
    {
        "ticket_id": 1006,
        "category": "streetlight",
        "priority": "medium",
        "status": "in_progress",
        "subject": "Flickering lamp outside library",
        "requester": {"user_id": 102, "display_name": "Luis Rivera"},
        "assignee_id": 201,
        "opened_at": datetime(2026, 2, 6, 1, 30, tzinfo=timezone.utc),
        "tags": ["lighting", "library"],
        "events": [],
        "course_fixture": "cst4714",
    },
]

insert_result = tickets.insert_many(fixture)
print("Inserted documents:", len(insert_result.inserted_ids))
print("Verified fixture count:", tickets.count_documents({"course_fixture": "cst4714"}))
'''
        ),
        markdown(
            """
## 2. Filter, Project, and Sort

The result grain is one document per matching ticket. The projection excludes
`_id` and returns only fields needed for the question.
"""
        ),
        code(
            r'''
active_high_priority = tickets.find(
    {
        "course_fixture": "cst4714",
        "status": {"$in": ["new", "open", "in_progress"]},
        "priority": {"$in": ["high", "urgent"]},
    },
    {"_id": 0, "ticket_id": 1, "priority": 1, "status": 1, "subject": 1, "opened_at": 1},
).sort("opened_at", -1)

for document in active_high_priority:
    print(document)
'''
        ),
        markdown(
            """
### Your Turn

Modify the next filter to choose a different status set or category, and modify the
projection to add exactly one useful field. State the expected result grain before
running it.
"""
        ),
        code(
            r'''
# Grain: one document per matching ticket.
for document in tickets.find(
    {"course_fixture": "cst4714", "category": "streetlight"},
    {"_id": 0, "ticket_id": 1, "category": 1, "status": 1, "subject": 1},
).sort("ticket_id", 1):
    print(document)
'''
        ),
        markdown(
            """
## 3. Query a Nested Field and an Array

Dot notation reaches `requester.user_id`. Equality against an array field matches
when the array contains that value.
"""
        ),
        code(
            r'''
print("Tickets requested by user 101:")
for document in tickets.find(
    {"course_fixture": "cst4714", "requester.user_id": 101},
    {"_id": 0, "ticket_id": 1, "requester.display_name": 1, "status": 1},
):
    print(document)

print("\nTickets tagged safety:")
for document in tickets.find(
    {"course_fixture": "cst4714", "tags": "safety"},
    {"_id": 0, "ticket_id": 1, "tags": 1},
):
    print(document)
'''
        ),
        markdown(
            """
## 4. `$elemMatch` Requires Conditions on the Same Array Element

The question asks for one event whose type is `status_changed` **and** whose actor
role is `agent`. `$elemMatch` prevents one array element from satisfying the type
while a different element satisfies the actor condition.
"""
        ),
        code(
            r'''
for document in tickets.find(
    {
        "course_fixture": "cst4714",
        "events": {
            "$elemMatch": {"type": "status_changed", "actor_role": "agent"}
        },
    },
    {"_id": 0, "ticket_id": 1, "events": 1},
):
    print(document)
'''
        ),
        markdown(
            """
## 5. Verify Matched and Modified Counts

The lab inserts one clearly marked test document. The first `$set` changes it. The
second identical `$set` still matches the document but has no new value to write.
"""
        ),
        code(
            r'''
test_document = {
    "ticket_id": 1099,
    "category": "parks",
    "priority": "low",
    "status": "new",
    "subject": "Disposable MQL test",
    "requester": {"user_id": 101, "display_name": "Maya Chen"},
    "opened_at": datetime.now(timezone.utc),
    "events": [],
    "test_record": True,
    "course_fixture": "cst4714",
}
tickets.insert_one(test_document)

first_update = tickets.update_one(
    {"ticket_id": 1099, "test_record": True, "status": "new"},
    {"$set": {"status": "in_progress", "assignee_id": 202}},
)
print("First update matched/modified:", first_update.matched_count, first_update.modified_count)

second_update = tickets.update_one(
    {"ticket_id": 1099, "test_record": True, "status": "in_progress"},
    {"$set": {"status": "in_progress", "assignee_id": 202}},
)
print("Repeated update matched/modified:", second_update.matched_count, second_update.modified_count)
'''
        ),
        markdown(
            """
## 6. Append One Event and Read Back the Final Document

`$push` appends to the array. In a production event flow, use a stable event ID and
idempotency rule so a retry cannot append the same event twice.
"""
        ),
        code(
            r'''
event_update = tickets.update_one(
    {"ticket_id": 1099, "test_record": True},
    {
        "$push": {
            "events": {
                "event_id": 5999,
                "type": "status_changed",
                "actor_role": "agent",
                "at": datetime.now(timezone.utc),
            }
        }
    },
)
print("Event append matched/modified:", event_update.matched_count, event_update.modified_count)
print(tickets.find_one({"ticket_id": 1099}, {"_id": 0}))
'''
        ),
        markdown(
            """
## 7. Delete Only the Disposable Record

The predicate includes both the identifier and the safety marker. The final query
proves cleanup.
"""
        ),
        code(
            r'''
delete_result = tickets.delete_one({"ticket_id": 1099, "test_record": True})
print("Deleted count:", delete_result.deleted_count)
print("Remaining test record:", tickets.find_one({"ticket_id": 1099, "test_record": True}))
'''
        ),
        markdown(
            """
## 8. Compare Two Models

These are design sketches, not additional database writes.
"""
        ),
        code(
            r'''
embedded_ticket = {
    "ticket_id": 1001,
    "requester": {"user_id": 101, "display_name": "Maya Chen"},
    "events": [{"event_id": 5001, "type": "created"}],
}

referenced_ticket = {
    "ticket_id": 1001,
    "requester_id": 101,
    "event_ids": [5001],
}

print("Embedded sketch:", embedded_ticket)
print("Referenced sketch:", referenced_ticket)
'''
        ),
        markdown(
            """
## Evidence Record: Complete Before Submission

**Modified filter and projection:** [what you changed and what one result document
represented]

**Nested/array reasoning:** [which query used dot notation and why `$elemMatch` did
or did not matter]

**Write evidence:** [interpret the first and repeated matched/modified counts]

**Delete safety:** [why the exact predicate could not delete the fixture broadly]

**Model choice:** [embed or reference events for one stated access pattern, with
growth and duplication tradeoff]

**Atlas control:** [if used, name one database-user or network control and how you
narrowed or removed it]

**Credential check:** I confirm no URI or password appears in notebook source or
output. [replace with yes]

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic data CC0.
"""
        ),
        code(
            r'''
client.close()
print("Client closed. Baseline fixture retained for the next course lab when Atlas was used.")
'''
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "04_atlas_mql_modeling.ipynb"
    nbf.write(notebook, output)


def build_mongodb_logical_recovery() -> None:
    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "05_mongodb_logical_recovery.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    }

    notebook["cells"] = [
        markdown(
            """
# MongoDB Logical Export, Separate Restore, and Verification

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/05_mongodb_logical_recovery.ipynb)

This notebook creates a collection-level canonical Extended JSON artifact, restores
it under a different database name, and verifies identifiers, counts, BSON date
types, a meaningful query, indexes, and validation behavior.

The exercise is intentionally transparent. It is **not** mislabeled as a complete
Atlas backup. Atlas Free does not provide native backups; `mongodump` and
`mongorestore` are the documented database-level tools.
"""
        ),
        code(
            r'''
%pip -q install pymongo mongomock
'''
        ),
        code(
            r'''
from datetime import datetime, timezone
from getpass import getpass
import hashlib
from pathlib import Path

import mongomock
from bson import json_util
from bson.json_util import CANONICAL_JSON_OPTIONS
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import OperationFailure
from pymongo.server_api import ServerApi

USE_ATLAS = False  # Change only in the in-class Atlas lab.
DATABASE_SUFFIX = "offline"  # Use a unique suffix before enabling Atlas.

if USE_ATLAS:
    if DATABASE_SUFFIX == "offline":
        raise ValueError("Replace DATABASE_SUFFIX with a unique course value before using Atlas.")
    mongodb_uri = getpass("Paste the temporary Atlas URI: ")
    client = MongoClient(
        mongodb_uri,
        server_api=ServerApi("1", strict=True, deprecation_errors=True),
        serverSelectionTimeoutMS=10000,
        timeoutMS=10000,
    )
    print("Atlas ping:", client.admin.command("ping"))
else:
    client = mongomock.MongoClient()
    print("Using the offline in-memory MongoDB-compatible path.")

SOURCE_DB = f"cst4714_recovery_source_{DATABASE_SUFFIX}"
RESTORE_DB = f"cst4714_recovery_restore_{DATABASE_SUFFIX}"
EXPORT_FILE = Path("/tmp/cst4714_tickets_canonical_extjson.json")
print("Source:", SOURCE_DB)
print("Restore target:", RESTORE_DB)
'''
        ),
        markdown(
            """
## 1. Create the Source Collection and Operational Rules

The source collection has a focused validator in Atlas and a compound index. The
offline library supports the documents and index but not server-side validation,
so the notebook labels that limitation rather than pretending the feature ran.
"""
        ),
        code(
            r'''
client.drop_database(SOURCE_DB)
client.drop_database(RESTORE_DB)
source_database = client[SOURCE_DB]

ticket_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["ticket_id", "status", "priority", "subject", "opened_at"],
        "properties": {
            "ticket_id": {"bsonType": ["int", "long"]},
            "status": {"enum": ["new", "open", "in_progress", "resolved", "closed"]},
            "priority": {"enum": ["low", "medium", "high", "urgent"]},
            "subject": {"bsonType": "string"},
            "opened_at": {"bsonType": "date"},
        },
    }
}

if USE_ATLAS:
    source_database.create_collection("tickets", validator=ticket_validator)
else:
    source_database.create_collection("tickets")
    print("Offline path: server-side $jsonSchema validation is not implemented by mongomock.")

source_tickets = source_database["tickets"]
source_tickets.create_index([("status", ASCENDING), ("opened_at", DESCENDING)])

source_documents = [
    {"ticket_id": 1001, "status": "open", "priority": "high",
     "subject": "Streetlight dark near bus stop",
     "opened_at": datetime(2026, 2, 1, 23, 10, tzinfo=timezone.utc)},
    {"ticket_id": 1002, "status": "in_progress", "priority": "medium",
     "subject": "Missed recycling pickup",
     "opened_at": datetime(2026, 2, 2, 15, 45, tzinfo=timezone.utc)},
    {"ticket_id": 1003, "status": "resolved", "priority": "urgent",
     "subject": "Low water pressure",
     "opened_at": datetime(2026, 2, 3, 12, 5, tzinfo=timezone.utc)},
    {"ticket_id": 1004, "status": "new", "priority": "low",
     "subject": "Broken bench slat",
     "opened_at": datetime(2026, 2, 4, 17, 20, tzinfo=timezone.utc)},
    {"ticket_id": 1005, "status": "resolved", "priority": "high",
     "subject": "Overflowing corner bin",
     "opened_at": datetime(2026, 2, 5, 14, 0, tzinfo=timezone.utc)},
]
source_tickets.insert_many(source_documents)

print("Source count:", source_tickets.count_documents({}))
print("Source indexes:", sorted(index["name"] for index in source_tickets.list_indexes()))
'''
        ),
        markdown(
            """
## 2. Create and Inspect Canonical Extended JSON

Canonical Extended JSON preserves BSON type information such as dates and ObjectId
values in a JSON-compatible representation. File size and SHA-256 help identify
the exact artifact; they do not prove it can be restored.
"""
        ),
        code(
            r'''
documents_to_export = list(source_tickets.find({}).sort("ticket_id", ASCENDING))
export_text = json_util.dumps(
    documents_to_export,
    json_options=CANONICAL_JSON_OPTIONS,
    indent=2,
)
EXPORT_FILE.write_text(export_text + "\n", encoding="utf-8")

export_bytes = EXPORT_FILE.read_bytes()
export_sha256 = hashlib.sha256(export_bytes).hexdigest()
print("Artifact:", EXPORT_FILE)
print("Bytes:", len(export_bytes))
print("SHA-256:", export_sha256)
print("First 300 characters:\n", export_text[:300])
'''
        ),
        markdown(
            """
## 3. Restore Into a Different Database

The restore database name is different from the source. Parsing with `json_util`
reconstructs BSON-aware Python values before insertion.
"""
        ),
        code(
            r'''
restore_database = client[RESTORE_DB]
restore_tickets = restore_database["tickets"]

restored_documents = json_util.loads(EXPORT_FILE.read_text(encoding="utf-8"))
restore_result = restore_tickets.insert_many(restored_documents)
print("Restored documents:", len(restore_result.inserted_ids))
print("Restore count:", restore_tickets.count_documents({}))
'''
        ),
        markdown(
            """
## 4. Verify Data, Identity, Type, and Behavior

Counts are only one check. We compare ticket identifiers, inspect the restored
date type, and run the active-ticket question.
"""
        ),
        code(
            r'''
source_ids = [doc["ticket_id"] for doc in source_tickets.find({}, {"_id": 0, "ticket_id": 1}).sort("ticket_id", 1)]
restore_ids = [doc["ticket_id"] for doc in restore_tickets.find({}, {"_id": 0, "ticket_id": 1}).sort("ticket_id", 1)]
print("Source IDs:", source_ids)
print("Restore IDs:", restore_ids)
assert source_ids == restore_ids

restored_sample = restore_tickets.find_one({"ticket_id": 1001})
print("Restored opened_at type:", type(restored_sample["opened_at"]).__name__)
assert isinstance(restored_sample["opened_at"], datetime)

active = list(
    restore_tickets.find(
        {"status": {"$in": ["new", "open", "in_progress"]}},
        {"_id": 0, "ticket_id": 1, "status": 1},
    ).sort("ticket_id", 1)
)
print("Active restored tickets:", active)
'''
        ),
        markdown(
            """
## 5. Identify What the JSON Artifact Omitted

Collection indexes and validators are database metadata. The document-only export
did not recreate them automatically.
"""
        ),
        code(
            r'''
print("Restore indexes before repair:", sorted(index["name"] for index in restore_tickets.list_indexes()))
print("Expected: only the automatic _id_ index before manual recreation.")

restore_tickets.create_index([("status", ASCENDING), ("opened_at", DESCENDING)])

if USE_ATLAS:
    restore_database.command(
        "collMod",
        "tickets",
        validator=ticket_validator,
        validationLevel="strict",
        validationAction="error",
    )
    print("Recreated index and server-side validator in the restore target.")
else:
    print("Recreated index. Offline path records, but cannot enforce, the server validator.")

print("Restore indexes after repair:", sorted(index["name"] for index in restore_tickets.list_indexes()))
'''
        ),
        markdown(
            """
## 6. Test Validation Behavior

Atlas should reject the invalid status after the validator is recreated. The
offline path performs an explicit rule check and labels it as application-level
simulation, not database enforcement.
"""
        ),
        code(
            r'''
invalid_document = {
    "ticket_id": 1099,
    "status": "almost_done",
    "priority": "low",
    "subject": "Expected validation failure",
    "opened_at": datetime.now(timezone.utc),
}

if USE_ATLAS:
    try:
        restore_tickets.insert_one(invalid_document)
        raise AssertionError("Atlas accepted a document the recreated validator should reject.")
    except OperationFailure as error:
        print("Expected Atlas validation error code:", error.code)
else:
    allowed_statuses = {"new", "open", "in_progress", "resolved", "closed"}
    simulated_valid = invalid_document["status"] in allowed_statuses
    print("Offline application-level validation result:", simulated_valid)
    assert not simulated_valid
'''
        ),
        markdown(
            """
## 7. Compare This Artifact With `mongodump`

| Concern | Canonical Extended JSON exercise | `mongodump` / `mongorestore` |
|---|---|---|
| selected document values | yes | yes |
| BSON type representation | preserved through Extended JSON when parsed correctly | native BSON archive |
| collection options/validator | not recreated automatically | collection metadata/options within documented behavior |
| index definitions | not recreated automatically | included in dump metadata |
| Atlas database users and network rules | no | no, managed separately |
| multi-collection point consistency | not established by this one-collection script | depends on topology, options, and documented tool behavior |

For an Atlas Free database-level backup, use current compatible MongoDB Database
Tools and the documented `mongodump`/`mongorestore` process. This notebook teaches
the recovery evidence sequence and the limitations of a narrower artifact.
"""
        ),
        markdown(
            """
## Recovery Record: Complete Before Submission

**Source and separate target:** [record both names]

**Artifact:** [path, bytes, and abbreviated SHA-256]

**Five checks:** [count, identifiers, type, meaningful query, and rule/index check]

**Omissions:** [which metadata and managed configuration did not travel]

**Atlas Free constraint:** [state the current backup limitation and official
alternative]

**Production next step:** [compatible Database Tools, retention, automation,
restore schedule, or broader verification]

**Credential check:** I confirm no URI or password appears in source or output.
[replace with yes]

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic data CC0.
"""
        ),
        code(
            r'''
client.drop_database(SOURCE_DB)
client.drop_database(RESTORE_DB)
client.close()
print("Removed the disposable source and restore databases and closed the client.")
'''
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "05_mongodb_logical_recovery.ipynb"
    nbf.write(notebook, output)


def build_public_data_capacity_integration() -> None:
    fixture_path = ROOT / "datasets" / "cisa_kev_sample" / "kev_sample.json"
    fixture_json = json.dumps(json.loads(fixture_path.read_text(encoding="utf-8")))

    notebook = nbf.v4.new_notebook()
    notebook["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3"},
        "colab": {
            "name": "06_public_data_capacity_integration.ipynb",
            "provenance": [],
        },
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT; source data terms retained",
    }

    notebook["cells"] = [
        markdown(
            """
# Public Data, Capacity, and Cloud Integration

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/06_public_data_capacity_integration.ipynb)

This notebook uses a small teaching snapshot of the U.S. Cybersecurity and
Infrastructure Security Agency's Known Exploited Vulnerabilities catalog. It
connects four skills: evaluating a source, checking data quality, reasoning about
distribution, and loading records without creating duplicates.

**By the end, you will be able to:**

- identify source, retrieval, transformation, and use limits before importing;
- check nulls, duplicates, identifiers, and dates;
- compare cardinality, frequency, monotonicity, and query targeting;
- explain range and hashed distribution with measured evidence;
- load records idempotently into SQLite, Atlas, or PostgreSQL; and
- verify more than a successful connection or insert count.

The default path is fully offline and requires no account. Cloud paths are
optional and prompt for credentials only at runtime.
"""
        ),
        markdown(
            """
## Resource and License Boundary

The notebook prose and code are course OER. The CISA records come from an official
U.S. government feed and are not represented as original course data. The
embedded snapshot preserves source metadata and a description of the field
selection. It is compact classroom evidence, not a current vulnerability-
management source.

Official feed:
<https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>
"""
        ),
        code(
            """
# SQLite is built into Python. PyMongo and Psycopg support optional cloud paths.
%pip -q install pymongo "psycopg[binary]"
"""
        ),
        code(
            """
from bisect import bisect_right
from collections import Counter
from datetime import date
from getpass import getpass
from hashlib import sha256
import json
import sqlite3
import urllib.request

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import psycopg
from psycopg.conninfo import conninfo_to_dict

print("Notebook libraries are ready.")
"""
        ),
        markdown(
            """
## 1. Choose the Versioned Snapshot or Current Feed

`USE_LIVE_FEED` is `False` by default. That makes the class result reproducible
and keeps the notebook usable during an outage. Change it to `True` only when you
intend to inspect the current official feed. Current results will differ from the
versioned teaching snapshot.
"""
        ),
        code(
            "OFFLINE_SNAPSHOT = json.loads(r'''" + fixture_json + "''')\n\n"
            "USE_LIVE_FEED = False\n"
            "OFFICIAL_FEED = \"https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json\"\n\n"
            "if USE_LIVE_FEED:\n"
            "    with urllib.request.urlopen(OFFICIAL_FEED, timeout=30) as response:\n"
            "        source_package = json.load(response)\n"
            "    source_mode = \"current official feed\"\n"
            "else:\n"
            "    source_package = OFFLINE_SNAPSHOT\n"
            "    source_mode = \"embedded versioned teaching snapshot\"\n\n"
            "print(\"Source mode:\", source_mode)\n"
            "print(\"Catalog version:\", source_package.get(\"catalogVersion\") or source_package.get(\"sourceCatalogVersion\"))\n"
            "print(\"Source release time:\", source_package.get(\"dateReleased\") or source_package.get(\"sourceDateReleased\"))\n"
            "print(\"Retrieval time:\", source_package.get(\"retrievedAt\", \"live request in this runtime\"))\n"
            "print(\"Source URL:\", source_package.get(\"sourceUrl\", OFFICIAL_FEED))"
        ),
        markdown(
            """
### Normalize Only the Fields Used by This Lesson

The live feed contains more fields than the teaching snapshot. We intentionally
select the same compact fields in both paths. This is a modeling decision, not a
claim that omitted fields are unimportant.
"""
        ),
        code(
            """
raw_records = source_package.get("vulnerabilities", [])

# Keep the lesson small even when the current feed is selected.
records = []
for raw in raw_records[:75]:
    records.append({
        "cveID": raw.get("cveID"),
        "vendorProject": raw.get("vendorProject"),
        "product": raw.get("product"),
        "vulnerabilityName": raw.get("vulnerabilityName"),
        "dateAdded": raw.get("dateAdded"),
        "dueDate": raw.get("dueDate"),
        "knownRansomwareCampaignUse": raw.get("knownRansomwareCampaignUse"),
        "cwes": raw.get("cwes") or [],
    })

print("Selected records:", len(records))
print("Selected fields:", list(records[0]))
print("Example record:\\n", json.dumps(records[0], indent=2))
"""
        ),
        markdown(
            """
## 2. Audit Before Loading

A successful JSON parse does not prove the records are suitable for a database.
We check missing values, duplicate identifiers, and ISO date values first.
"""
        ),
        code(
            """
fields = list(records[0])
null_counts = {
    field: sum(record.get(field) in (None, "") for record in records)
    for field in fields
}
cve_counts = Counter(record["cveID"] for record in records)
duplicate_ids = sorted(cve_id for cve_id, count in cve_counts.items() if count > 1)

invalid_dates = []
for record in records:
    for field in ("dateAdded", "dueDate"):
        try:
            date.fromisoformat(record[field])
        except (TypeError, ValueError):
            invalid_dates.append((record["cveID"], field, record[field]))

print("Null counts:", null_counts)
print("Duplicate CVE IDs:", duplicate_ids)
print("Invalid ISO dates:", invalid_dates)
assert records and not duplicate_ids and not invalid_dates
"""
        ),
        markdown(
            """
### Ask a Question Before Choosing a Database Shape

Our first question is: **Which vendors occur most often in this selected
snapshot?** This describes the sample, not all vulnerabilities and not a vendor's
security quality. The limited sample and source order matter.
"""
        ),
        code(
            """
vendor_counts = Counter(record["vendorProject"] for record in records)
print("Five most frequent vendors in this selected sample:")
for vendor, count in vendor_counts.most_common(5):
    print(f"  {vendor}: {count}")
"""
        ),
        markdown(
            """
## 3. Measure Candidate Distribution Keys

We compare four candidates:

- `vendorProject` can target vendor questions but may be skewed;
- `dateAdded` supports time questions but may be monotonic;
- `cveID` is highly distinct but does not target vendor questions; and
- `(vendorProject, product)` can divide some vendor groups further.

High cardinality alone is not enough. A useful decision also considers frequency,
write order, and actual query shapes.
"""
        ),
        code(
            """
candidate_values = {
    "vendorProject": [record["vendorProject"] for record in records],
    "dateAdded": [record["dateAdded"] for record in records],
    "cveID": [record["cveID"] for record in records],
    "vendorProject + product": [
        (record["vendorProject"], record["product"]) for record in records
    ],
}

print(f"{'candidate':28} {'distinct':>8} {'ratio':>8} {'largest value share':>20}")
for name, values in candidate_values.items():
    frequencies = Counter(values)
    distinct = len(frequencies)
    largest_share = max(frequencies.values()) / len(values)
    print(f"{name:28} {distinct:8d} {distinct / len(values):8.2f} {largest_share:20.2%}")

dates_in_source_order = [record["dateAdded"] for record in records]
descending_date_order = all(
    left >= right for left, right in zip(dates_in_source_order, dates_in_source_order[1:])
)
print("\\nDate-added values are monotonic descending in source order:", descending_date_order)
print("This is an input-order observation, not proof of production write order.")
"""
        ),
        markdown(
            """
## 4. Simulate Range and Hashed Placement

This is not a sharded MongoDB deployment. It is a deterministic thought
experiment that makes two tradeoffs visible.

For the range simulation, the oldest 80 percent establishes three date boundaries
and the newest 20 percent acts like later writes. A monotonic time key tends to
place those later writes in the current high range. For the hash simulation,
SHA-256 maps CVE IDs into four teaching buckets. MongoDB uses its own hashing and
balancing behavior; these buckets only illustrate distribution.
"""
        ),
        code(
            """
chronological = sorted(records, key=lambda record: record["dateAdded"])
split_at = max(1, int(len(chronological) * 0.80))
historical = chronological[:split_at]
later_writes = chronological[split_at:]

historical_dates = sorted(record["dateAdded"] for record in historical)
range_boundaries = [
    historical_dates[int(len(historical_dates) * fraction)]
    for fraction in (0.25, 0.50, 0.75)
]
range_buckets = Counter(
    bisect_right(range_boundaries, record["dateAdded"])
    for record in later_writes
)
hash_buckets = Counter(
    int(sha256(record["cveID"].encode("utf-8")).hexdigest(), 16) % 4
    for record in later_writes
)

print("Historical date boundaries:", range_boundaries)
print("Later-write range buckets:", dict(sorted(range_buckets.items())))
print("Later-write teaching hash buckets:", dict(sorted(hash_buckets.items())))
print("Later records tested:", len(later_writes))
assert sum(range_buckets.values()) == len(later_writes)
assert sum(hash_buckets.values()) == len(later_writes)
"""
        ),
        markdown(
            """
### Record a Capacity Recommendation

Complete these statements before loading:

1. **Current scale:** This sample contains ___ records and is/is not large enough
   to justify sharding because ___.
2. **Candidate evidence:** ___ has ___ distinct values; its largest value holds
   ___ percent of the sample.
3. **Query targeting:** The main question filters/groups by ___, so ___ would or
   would not help route that question.
4. **Tradeoff:** Range distribution preserves ___ but risks ___; hashed
   distribution improves ___ but weakens ___.
5. **Decision:** Do not shard yet, or select ___ only under the stated future
   workload, because ___.
"""
        ),
        markdown(
            """
## 5. Load One Target Idempotently

The default is SQLite. It gives every student a complete database path without an
account. You may additionally enable Atlas or PostgreSQL. Cloud paths prompt for
the URI and never print it.

An **idempotent** load can be rerun without adding duplicate logical records. We
use `cveID` as the stable key and an upsert or conflict update on each target.
"""
        ),
        code(
            """
LOAD_SQLITE = True
LOAD_ATLAS = False
LOAD_POSTGRES = False

if LOAD_SQLITE:
    con = sqlite3.connect(":memory:")
    con.execute('''
        CREATE TABLE IF NOT EXISTS kev_sample (
            cve_id TEXT PRIMARY KEY,
            vendor_project TEXT NOT NULL,
            product TEXT NOT NULL,
            vulnerability_name TEXT NOT NULL,
            date_added TEXT NOT NULL,
            due_date TEXT NOT NULL,
            ransomware_use TEXT,
            cwes_json TEXT NOT NULL
        )
    ''')

    rows = [
        (
            record["cveID"], record["vendorProject"], record["product"],
            record["vulnerabilityName"], record["dateAdded"], record["dueDate"],
            record["knownRansomwareCampaignUse"], json.dumps(record["cwes"]),
        )
        for record in records
    ]
    con.executemany('''
        INSERT INTO kev_sample VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (cve_id) DO UPDATE SET
            vendor_project = excluded.vendor_project,
            product = excluded.product,
            vulnerability_name = excluded.vulnerability_name,
            date_added = excluded.date_added,
            due_date = excluded.due_date,
            ransomware_use = excluded.ransomware_use,
            cwes_json = excluded.cwes_json
    ''', rows)
    con.commit()
    print("SQLite upsert completed.")
"""
        ),
        markdown(
            """
### Optional Atlas Path

Before enabling this cell, create or open an Atlas Free project, create a database
user, and add only the temporary network access required for the runtime. Use the
current `mongodb+srv://` connection string. Do not add `tlsInsecure=True`; fix the
URI, network access, driver, DNS, or TLS cause instead.
"""
        ),
        code(
            """
if LOAD_ATLAS:
    atlas_uri = getpass("Atlas connection URI (hidden): ")
    atlas_client = MongoClient(
        atlas_uri,
        server_api=ServerApi("1", strict=True, deprecation_errors=True),
        serverSelectionTimeoutMS=10000,
        timeoutMS=10000,
    )
    atlas_client.admin.command("ping")

    atlas_collection = atlas_client["cst4714_public_data"]["kev_sample"]
    for record in records:
        atlas_collection.replace_one({"cveID": record["cveID"]}, record, upsert=True)

    print("Atlas upsert completed. Observed count:", atlas_collection.count_documents({}))
else:
    print("Atlas path skipped. Set LOAD_ATLAS = True only when you intend to connect.")
"""
        ),
        markdown(
            """
### Optional Supabase/PostgreSQL Path

Copy the current PostgreSQL connection URL from your provider and enter it when
prompted. If a notebook network cannot reach the direct IPv6 endpoint, use the
provider's current IPv4-compatible session-pooler URL. Do not place the URL in a
Markdown or code cell. Add `sslmode=require` or a stronger mode. For production,
use `verify-full` with the Supabase CA certificate; `require` encrypts traffic but
does not verify the CA or hostname.
"""
        ),
        code(
            """
if LOAD_POSTGRES:
    postgres_url = getpass("PostgreSQL connection URL (hidden): ")
    sslmode = conninfo_to_dict(postgres_url).get("sslmode", "prefer")
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        raise ValueError("Add sslmode=require or a stronger mode to the temporary URL.")
    with psycopg.connect(postgres_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("CREATE SCHEMA IF NOT EXISTS cst4714_oer")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cst4714_oer.kev_sample (
                    cve_id text PRIMARY KEY,
                    vendor_project text NOT NULL,
                    product text NOT NULL,
                    vulnerability_name text NOT NULL,
                    date_added date NOT NULL,
                    due_date date NOT NULL,
                    ransomware_use text,
                    cwes jsonb NOT NULL
                )
            ''')
            cursor.executemany('''
                INSERT INTO cst4714_oer.kev_sample VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s::jsonb)
                ON CONFLICT (cve_id) DO UPDATE SET
                    vendor_project = excluded.vendor_project,
                    product = excluded.product,
                    vulnerability_name = excluded.vulnerability_name,
                    date_added = excluded.date_added,
                    due_date = excluded.due_date,
                    ransomware_use = excluded.ransomware_use,
                    cwes = excluded.cwes
            ''', rows)
        connection.commit()
    print("PostgreSQL upsert completed.")
else:
    print("PostgreSQL path skipped. Set LOAD_POSTGRES = True only when you intend to connect.")
"""
        ),
        markdown(
            """
## 6. Verify the Import

We verify four things:

1. expected and observed counts;
2. one known stable identifier;
3. a grouped question tied to the reason for loading; and
4. rerun behavior through the primary key and upsert.

These checks still do not prove completeness of the full live catalog, correct
authorization, backup readiness, performance under load, or production fitness.
"""
        ),
        code(
            """
known_id = records[0]["cveID"]

if LOAD_SQLITE:
    observed_count = con.execute("SELECT count(*) FROM kev_sample").fetchone()[0]
    known_row = con.execute(
        "SELECT cve_id, vendor_project, product FROM kev_sample WHERE cve_id = ?",
        [known_id],
    ).fetchone()
    grouped = con.execute('''
        SELECT vendor_project, count(*) AS vulnerability_count
        FROM kev_sample
        GROUP BY vendor_project
        ORDER BY vulnerability_count DESC, vendor_project
        LIMIT 5
    ''').fetchall()

    print("Expected count:", len(records))
    print("Observed SQLite count:", observed_count)
    print("Known identifier check:", known_row)
    print("Grouped result:", grouped)
    assert observed_count == len(records) and known_row is not None

if LOAD_ATLAS:
    atlas_known = atlas_collection.find_one(
        {"cveID": known_id}, {"_id": 0, "cveID": 1, "vendorProject": 1, "product": 1}
    )
    atlas_grouped = list(atlas_collection.aggregate([
        {"$group": {"_id": "$vendorProject", "vulnerability_count": {"$sum": 1}}},
        {"$sort": {"vulnerability_count": -1, "_id": 1}},
        {"$limit": 5},
    ]))
    print("Atlas known identifier check:", atlas_known)
    print("Atlas grouped result:", atlas_grouped)
    assert atlas_collection.count_documents({}) == len(records) and atlas_known

if LOAD_POSTGRES:
    with psycopg.connect(postgres_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) FROM cst4714_oer.kev_sample")
            postgres_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT cve_id, vendor_project, product FROM cst4714_oer.kev_sample WHERE cve_id = %s",
                (known_id,),
            )
            postgres_known = cursor.fetchone()
            cursor.execute('''
                SELECT vendor_project, count(*) AS vulnerability_count
                FROM cst4714_oer.kev_sample
                GROUP BY vendor_project
                ORDER BY vulnerability_count DESC, vendor_project
                LIMIT 5
            ''')
            postgres_grouped = cursor.fetchall()
    print("PostgreSQL observed count:", postgres_count)
    print("PostgreSQL known identifier check:", postgres_known)
    print("PostgreSQL grouped result:", postgres_grouped)
    assert postgres_count == len(records) and postgres_known
"""
        ),
        markdown(
            """
## Submission Record

Complete this record in the notebook:

**Source and snapshot:** [official source, live or embedded mode, catalog version,
retrieval/release date, and why this is only a teaching subset]

**Quality evidence:** [record count, null result, duplicate result, and date result]

**Capacity evidence:** [one candidate's cardinality and largest-value share;
range/hash observation; recommendation and tradeoff]

**Target and idempotency:** [SQLite, Atlas, or PostgreSQL; stable key and upsert
behavior]

**Verification:** [expected/observed count, known identifier, grouped question,
and one thing these checks do not prove]

**Credential check:** I confirm no URI, password, token, or API key appears in
cell source or output. [replace with yes]
"""
        ),
        markdown(
            """
## Final-Project Transfer

This checkpoint does not add or redefine final-project deliverables. Use the
[canonical final project](../final_project.md).

Write four sentences:

1. My project could use a public or synthetic dataset about ___.
2. The source of truth should be ___ because ___.
3. My first scale trigger would be measured as ___.
4. Before scaling, I would verify ___ and improve ___ because ___.

If you used a cloud path, close the client and remove temporary broad network
access after class. The cleanup cell removes only this notebook's Atlas fixture
IDs and the disposable `cst4714_oer` PostgreSQL schema.
"""
        ),
        code(
            """
if LOAD_ATLAS:
    fixture_ids = [record["cveID"] for record in records]
    deleted = atlas_collection.delete_many({"cveID": {"$in": fixture_ids}})
    print("Deleted Atlas fixture documents:", deleted.deleted_count)
    atlas_client.close()
    print("Closed the Atlas client. Review and narrow temporary network access.")
    atlas_uri = None
if LOAD_POSTGRES:
    with psycopg.connect(postgres_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA IF EXISTS cst4714_oer CASCADE")
        connection.commit()
    postgres_url = None
    print("Removed the disposable PostgreSQL schema and cleared the URL variable.")
if LOAD_SQLITE:
    con.close()
    print("Closed the disposable SQLite database.")
"""
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    output = NOTEBOOK_DIR / "06_public_data_capacity_integration.ipynb"
    nbf.write(notebook, output)


def main() -> None:
    build_relational_sql_review()
    build_transactions_locks()
    build_postgres_backup_restore()
    build_atlas_mql_modeling()
    build_mongodb_logical_recovery()
    build_public_data_capacity_integration()


if __name__ == "__main__":
    main()
