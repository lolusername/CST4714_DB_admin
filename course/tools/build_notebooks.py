"""Build the public educational notebooks from reviewed source cells.

Notebook prose is CC BY-NC-SA 4.0. Notebook code is MIT licensed.
"""

import json
from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"


def markdown(text: str):
    if 'https://colab.research.google.com/assets/colab-badge.svg' in text:
        text = text.replace('![Open in Colab]', '![Open Colab]')
        badge_end = text.index('\n', text.index('colab-badge.svg'))
        text = (text[:badge_end] + '\n\nDownload this notebook, open Colab, and choose '
                '**File > Upload notebook**. The full draft course is distributed '
                'separately from the public Week 1 repository.\n' + text[badge_end:])
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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

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
check confirms how many rows loaded; inspecting identifiers and values answers
different questions.
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
## 10. Explain What the Results Establish

Write short answers in a new Markdown cell or your lab file:

1. Which query changed its result grain, and what did one output row represent?
2. Why did the left join preserve a row that the inner join removed?
3. What did the independent streetlight query confirm? What remains untested?
4. Which relational-algebra operation did `EXCEPT` express?
5. Which result confirms that the priority update was rolled back?

## Readiness Check

You are ready to continue when you can predict and explain the queries, not just
run them. If one section is unclear, edit its query, use smaller projections, and
inspect one identifier at a time.

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic example data CC0.
"""
        ),
    ]

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    full_setup = (ROOT / 'datasets/metro_support/postgres_setup.sql').read_text()
    full_setup = full_setup.replace(
        'SET search_path TO metro_support, public;',
        "SET schema = 'metro_support';",
    )
    notebook.cells.extend([
        markdown('''
## Use the Complete Week 2 Lab Dataset

The worked examples above deliberately used a smaller instance: 4 users, 6
tickets, and 9 events. The two Week 2 labs use **8 users, 12 tickets, and 21
events**. Run the next cell before doing either lab. It creates a separate
`metro_support` schema in this in-memory database and selects that schema.
Rerunning it resets only that practice schema.

The cell is the course's PostgreSQL setup with one DuckDB-specific change:
`SET schema` chooses the default namespace. The lab queries use full names such
as `metro_support.tickets`, so their target is explicit.
'''),
        code('con.execute("""\n' + full_setup + '\n""")\n'
             'con.sql("""SELECT \'users\' AS table_name, count(*) AS row_count FROM metro_support.users\n'
             "UNION ALL SELECT 'tickets', count(*) FROM metro_support.tickets\n"
             "UNION ALL SELECT 'ticket_events', count(*) FROM metro_support.ticket_events\n"
             'ORDER BY table_name""").show()'),
        markdown('''
### Run Your Lab Query

Add a code cell using this pattern and replace the SQL with your own SELECT:

```python
con.sql("""
SELECT ticket_id, subject
FROM metro_support.tickets
WHERE assignee_id IS NULL
ORDER BY ticket_id;
""").show()
```

This starter returns 1004 and 1009. For transaction commands use
`con.execute("BEGIN")` and `con.execute("ROLLBACK")`. Use `.sql(...).show()`
for the UPDATE with RETURNING and the verification SELECTs. Follow the weekly
lab for the one required submission; the notebook's earlier practice prompts
are discussion, not additional assignments.
'''),
    ])
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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

This notebook creates one controlled blocking relationship in a disposable schema,
identifies the blocked and blocking sessions, resolves the blocker, and verifies
the final row.

**The central idea:** a wait is a relationship between database sessions. Diagnose
that relationship before terminating or changing anything.

The cloud path asks for a temporary PostgreSQL URL with `getpass`, so the value is
not displayed or written into the notebook. A labeled transcript supports
interpretation when a connection is unavailable; it does not execute PostgreSQL.
"""
        ),
        markdown(
            """
## Before You Connect

1. Use a personal course database, never a production system.
2. In Supabase's **Connect** dialog, choose **Session pooler** for this exercise.
   It supports IPv4 and keeps each connection attached to a database session.
   Do not substitute the transaction-pooler endpoint: we are observing sessions.
3. Rotate the temporary password after class if required by your course policy.
4. Never paste a URL into a code or Markdown cell.

The URL must request `sslmode=require`, `verify-ca`, or `verify-full`; the
notebook rejects libpq's default `prefer` mode because it can fall back to an
unencrypted connection. For production, use `verify-full` with the Supabase CA
certificate. `require` encrypts the classroom connection but does not verify the
hostname. With a configured root certificate, libpq's `require` mode can also
check the CA; use `verify-full` when both CA and hostname verification are required.

[Supabase connection methods](https://supabase.com/docs/guides/database/connecting-to-postgres)

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
KEEP_A_CHANGE = False  # First run: rollback A. Second run: set True to commit A.
print("Cloud path enabled:", USE_CLOUD)
'''
        ),
        markdown(
            """
## 1. Open Three Clearly Named Sessions

- **Session A** will update a row and deliberately remain uncommitted.
- **Session B** will attempt a competing update and wait.
- **Diagnostic session** will query PostgreSQL's activity and lock state.

Three connections make the roles visible. The diagnostic session does not cause
or resolve the block; it observes it.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    database_url = getpass("Paste the temporary PostgreSQL connection URL: ")

    try:
        sslmode = conninfo_to_dict(database_url).get("sslmode", "prefer")
    except psycopg.Error:
        database_url = None
        raise ValueError("The connection URL could not be parsed. Copy a fresh Session pooler URL.") from None
    if sslmode not in {"require", "verify-ca", "verify-full"}:
        database_url = None
        raise ValueError("Add sslmode=require or a stronger mode to the temporary URL.")

    session_a = session_b = diagnostic = None
    try:
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
    except psycopg.Error:
        for connection in (session_a, session_b, diagnostic):
            if connection is not None:
                connection.close()
        raise RuntimeError("Connection failed. Check project status, Session pooler URL, password, and SSL mode.") from None
    finally:
        database_url = None

    print("Opened Session A, Session B, and the diagnostic session.")
else:
    print("Cloud path skipped. Continue to the fallback transcript below.")
'''
        ),
        markdown(
            """
## 2. Create a Disposable Target

The table has one row. Its original state is `priority = medium` and
`status = open`. This deliberately simplified fixture differs from the full
Metro Support ticket. Recreating `lock_lab` resets only this exercise.
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

Session A will change the priority without committing. Read this statement and
predict what a second writer will do. The next experiment runs both sessions,
captures the waiting relationship, and releases the lock in the same cell. You
can study its saved results without leaving a database transaction open.

For the first run, `KEEP_A_CHANGE = False` discards A's proposed priority change.
After cleanup, change it to `True` and run again from the configuration cell.
Predict the second final row before running it. B's SQL stays the same.
"""
        ),
        code(
            r'''
session_a_sql = """
    UPDATE lock_lab.tickets
    SET priority = 'high'
    WHERE ticket_id = 1004
    RETURNING ticket_id, priority, status
"""
print("Session A will run this UPDATE without committing:")
print(session_a_sql)
'''
        ),
        markdown(
            """
## 4. Session B Starts a Competing Update

The notebook uses one small background thread because a blocked query cannot both
wait and let the same notebook cell collect diagnostics. The experiment captures
the real PostgreSQL lock relationship, ends A's transaction, and lets B commit
before the cell ends. `KEEP_A_CHANGE` chooses A's outcome. The `finally` block
rolls back any remaining transaction if the experiment fails.

You do not need to write threading code for this lab. Follow the SQL and the
transaction decisions. The small worker below allows B to wait while another
connection runs the diagnostic query.
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
        blocked_result["outcome"] = f"error: {type(error).__name__}"


diagnostic_sql = """
    SELECT pid, application_name, state, wait_event_type, wait_event,
           pg_blocking_pids(pid) AS blocking_pids,
           xact_start, clock_timestamp() - xact_start AS transaction_age,
           left(query, 90) AS query_sample
    FROM pg_stat_activity
    WHERE pid IN (%s, %s)
    ORDER BY application_name
"""
rows = []
columns = []
session_b_thread = None

if USE_CLOUD:
    try:
        with session_a.cursor() as cursor:
            cursor.execute("SET idle_in_transaction_session_timeout = '30s'")
            cursor.execute("SELECT pg_backend_pid()")
            a_pid = cursor.fetchone()[0]
            cursor.execute(session_a_sql)
            session_a_row = cursor.fetchone()
        # Psycopg began a transaction. A has not committed.
        with diagnostic.cursor() as cursor:
            cursor.execute("SELECT ticket_id, priority, status FROM lock_lab.tickets")
            reader_row = cursor.fetchone()
        with session_b.cursor() as cursor:
            cursor.execute("SELECT pg_backend_pid()")
            b_pid = cursor.fetchone()[0]
        # Ask PostgreSQL itself for PIDs, rather than a proxy's protocol identity.
        session_pids = (a_pid, b_pid)
        session_b_thread = threading.Thread(target=run_session_b_update)
        session_b_thread.start()

        # Capture the real wait instead of assuming it began after a fixed sleep.
        for attempt in range(100):
            with diagnostic.cursor() as cursor:
                cursor.execute(diagnostic_sql, session_pids)
                columns = [column.name for column in cursor.description]
                rows = cursor.fetchall()
            if any(row[0] == session_pids[1] and session_pids[0] in row[5] for row in rows):
                break
            time.sleep(0.05)
        else:
            raise RuntimeError("No blocking relationship was captured; rerun from setup.")
        if KEEP_A_CHANGE:
            session_a.commit()
        else:
            session_a.rollback()
    finally:
        # Always release A, even when diagnosis raises an error.
        session_a.rollback()
        if session_b_thread is not None:
            session_b_thread.join(timeout=20)
    if session_b_thread is not None and session_b_thread.is_alive():
        session_b.cancel()
        session_b_thread.join(timeout=5)
        raise RuntimeError("Session B did not finish; close the connections and rerun.")

    with diagnostic.cursor() as cursor:
        cursor.execute("SELECT ticket_id, priority, status FROM lock_lab.tickets")
        final_row = cursor.fetchone()
    assert blocked_result.get("outcome") == "committed after blocker released", blocked_result
    expected_priority = "high" if KEEP_A_CHANGE else "medium"
    assert final_row == (1004, expected_priority, "in_progress"), final_row
    print("A saw its uncommitted change:", session_a_row)
    print("An ordinary reader still saw:", reader_row)
    print("Captured a waiting writer, released A, and verified B's commit.")
    print("The next sections inspect the saved results. No lab row lock remains.")
else:
    print("Experiment skipped. Use the supplied transcript below.")
'''
        ),
        markdown(
            """
## 5. Ask PostgreSQL Who Is Blocking Whom

`pg_blocking_pids(pid)` directly reports the blocker relationship. The
wait event adds context. A PID identifies a session; it is not automatic
permission to terminate a process.

The query now selects only the two PIDs opened by this run. `%s` marks a value
supplied separately by Psycopg; it is not SQL you should replace by string
concatenation. `transaction_age` is measured at capture time. The waiter can
have `state = active` and still have `wait_event_type = Lock`.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    print("Snapshot captured while B was waiting:")
    for row in rows:
        print(f"\nSession {row[1]} (PID {row[0]})")
        for label, value in zip(columns[2:], row[2:]):
            print(f"  {label}: {value}")
else:
    print("Read the blocked and blocking PIDs in the fallback transcript.")
'''
        ),
        markdown(
            """
## 6. Resolve the Blocker and Verify the Final State

Both choices end A's transaction and release the row lock. Rollback discards its
priority change; commit keeps it. B then commits `status = in_progress` in either
case. Inspect both columns, not just whether B finished.
"""
        ),
        code(
            r'''
if USE_CLOUD:
    print("A's resolution:", "COMMIT" if KEEP_A_CHANGE else "ROLLBACK")
    print("Session B outcome:", blocked_result)
    print("Final row captured from a fresh statement:", final_row)
else:
    print("Compare A's discarded priority change with B's committed status change.")
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

Use this illustrative transcript when the cloud path cannot run. These are
teaching values, not measurements from your notebook. It represents the rollback
case. Predict the commit case separately; label that result as a prediction.

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

The transcript records one blocking relationship, the chosen resolution, and the
final state. It does not determine how a production application should choose
between waiting, rollback, cancellation, or termination.
"""
        ),
        markdown(
            """
## Your Comparison and Incident Update

Before the second run, keep the first final row here and predict the second.
After running again, replace the second observation with your result.

| A's decision | Predicted final priority/status | Observed final priority/status |
|---|---|---|
| ROLLBACK | Your prediction | Your result |
| COMMIT | Your prediction | Your result |

In the same cell, write a short update to the developer whose status update
appeared stuck. Use one run's PIDs and `pg_blocking_pids` result to explain the
wait, then explain why both runs let B finish but kept different priority values.
Name one reason you would not make the same commit/rollback decision blindly on
a real application. No separate incident form or report is required.

If you used the transcript, label the first row **supplied trace** and the second
**unexecuted prediction**. Do not describe that path as a live connection test.

Before submitting, remove any accidentally saved credential from source or output.

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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

This notebook performs a real PostgreSQL logical backup and restores it into a
different database. The databases are temporary and isolated, so the lab teaches
the full recovery sequence without risking a Supabase project.

**Recovery sequence:** source checks -> dump artifact -> artifact inspection ->
separate restore -> structure checks -> data checks -> behavior check.

No cloud credential is required. The final section translates the same procedure
to Supabase without storing a connection URL.

We use three users, three tickets, and five events: a smaller recovery example,
not the complete Metro Support dataset from earlier weeks. Both databases live on
the same temporary server. That isolates the restore from the source, but does
not protect either database against losing this notebook runtime.

**Your work:** run the example, adapt the supplied known-ticket check, and write
one short recovery account in this notebook. Keep its output, then run cleanup.
"""
        ),
        markdown(
            """
## 1. Prepare PostgreSQL in the Notebook Runtime

Google Colab does not start with a PostgreSQL server, so the next cell installs
the free PostgreSQL package when it detects Colab and starts a local service. On a
computer where PostgreSQL is already running, it uses the current local server.

For a local computer, use a disposable PostgreSQL installation and a local Unix
socket (`PGHOST` may name its socket directory). This notebook refuses remote
hosts. Do not point it at a cloud project or a shared production server.

The command prefix is shown explicitly. It changes only because Colab's local
server is owned by its `postgres` operating-system user.

The cells contain **Python** that launches PostgreSQL command-line programs.
`subprocess.run([program, option, value], check=True)` waits for that program and
stops the cell if it fails. `capture_output=True` keeps the result available for
comparison; `text=True` reads it as text. SQL appears inside quoted strings passed
to `psql`. These are three layers, not three versions of SQL.
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

if not IN_COLAB and os.environ.get("PGHOST", "") and not os.environ["PGHOST"].startswith("/"):
    raise RuntimeError("Use a local PostgreSQL Unix socket, not a remote host, for this practice notebook.")
if not IN_COLAB and (os.environ.get("PGSERVICE") or os.environ.get("PGHOSTADDR")):
    raise RuntimeError("Unset PGSERVICE and PGHOSTADDR so the local practice target is explicit.")

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
    PG_PREFIX + ["psql", "-X", "--set=ON_ERROR_STOP=on", "--dbname", "postgres",
                 "--tuples-only", "--no-align", "--command", "SHOW server_version_num"],
    check=True,
    text=True,
    capture_output=True,
)
server_version_num = int(server_version_result.stdout.strip())
server_major = server_version_num // 10000

candidate_directories = [
    Path(f"/usr/lib/postgresql/{server_major}/bin"),
    Path(f"/opt/homebrew/opt/postgresql@{server_major}/bin"),
    Path(f"/Applications/Postgres.app/Contents/Versions/{server_major}/bin"),
]
path_pg_dump = shutil.which("pg_dump")
if path_pg_dump:
    candidate_directories.append(Path(path_pg_dump).parent)

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
    if version_match and int(version_match.group(1)) == server_major:
        PG_BIN = candidate_directory
        break

if PG_BIN is None:
    raise RuntimeError(
        f"For this same-server restore, install PostgreSQL client major version {server_major} "
        "to match the server, then rerun this cell."
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

The SQL is ordinary `CREATE TABLE` and `INSERT`. A unique suffix prevents a new
run from overwriting someone else's database. In Colab, the private artifact
folder is owned by the local `postgres` user so that user can create the dump.
The folder remains private; making it writable by everyone is unnecessary.
"""
        ),
        code(
            r'''
from uuid import uuid4
import tempfile

# Each run owns new database names and a separate artifact directory.
if "SOURCE_DB" in globals():
    raise RuntimeError("Run the final cleanup cell before creating another practice database.")
run_id = uuid4().hex[:8]
SOURCE_DB = "cst4714_recovery_source_" + run_id
RESTORE_DB = "cst4714_recovery_restore_" + run_id
ARTIFACT_DIR = Path(tempfile.mkdtemp(prefix="cst4714-recovery-"))
if IN_COLAB:
    shutil.chown(ARTIFACT_DIR, user="postgres", group="postgres")
SETUP_FILE = ARTIFACT_DIR / "metro_support_setup.sql"
DUMP_FILE = ARTIFACT_DIR / "metro_support.dump"

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

subprocess.run(PG_PREFIX + [CREATEDB, SOURCE_DB], check=True)
subprocess.run(
    PG_PREFIX
    + [PSQL, "-X", "--set=ON_ERROR_STOP=on", "--dbname", SOURCE_DB, "--file", str(SETUP_FILE)],
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

Expected source counts are 3 users, 3 tickets, and 5 events. The three tickets have
different statuses. We record table names, the named status constraint, a check
for missing requesters, and a grouped report as the source baseline. An `assert`
stops the cell if the complete result differs from the expected result.
"""
        ),
        code(
            r'''
source_check_sql = """
SELECT 'table=' || table_name
FROM information_schema.tables
WHERE table_schema = 'metro_support' AND table_type = 'BASE TABLE'
ORDER BY table_name;
SELECT 'users=' || count(*) FROM metro_support.users;
SELECT 'tickets=' || count(*) FROM metro_support.tickets;
SELECT 'ticket_events=' || count(*) FROM metro_support.ticket_events;
SELECT 'constraint=' || conname
FROM pg_constraint
WHERE conname = 'tickets_status_allowed'
  AND conrelid = 'metro_support.tickets'::regclass;
SELECT 'orphan_tickets=' || count(*)
FROM metro_support.tickets AS t
LEFT JOIN metro_support.users AS u ON u.user_id = t.requester_id
WHERE u.user_id IS NULL;
SELECT 'status:' || status || '=' || count(*)
FROM metro_support.tickets GROUP BY status ORDER BY status;
"""

expected_baseline = [
    "table=ticket_events", "table=tickets", "table=users",
    "users=3", "tickets=3", "ticket_events=5",
    "constraint=tickets_status_allowed", "orphan_tickets=0",
    "status:in_progress=1", "status:open=1", "status:resolved=1",
]

source_check = subprocess.run(
    PG_PREFIX + [PSQL, "-X", "--set=ON_ERROR_STOP=on", "--tuples-only", "--no-align",
                 "--dbname", SOURCE_DB, "--command", source_check_sql],
    check=True,
    text=True,
    capture_output=True,
)
print(source_check.stdout.strip())
assert source_check.stdout.strip().splitlines() == expected_baseline
'''
        ),
        markdown(
            """
## 4. Create the Logical Backup Artifact

`pg_dump --format=custom` creates an archive for `pg_restore`. The schema option
limits the archive to `metro_support`. This is not a backup of server roles or
other databases. All three related tables come from a consistent source snapshot.

For a custom archive, ownership suppression belongs on **pg_restore**, not
pg_dump. We omit grants at export and omit original ownership at restore so the
classroom example does not depend on identical roles. Restoring application
access would require a separate, reviewed permissions procedure.
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
assert len(dump_bytes) > 0
'''
        ),
        markdown(
            """
## 5. Inspect the Artifact Before Restoring

`pg_restore --list` reads the archive table of contents. Seeing the expected
schema, tables, data, constraints, and indexes confirms the archive inventory;
only a separate restore tests whether PostgreSQL can use it.

A checksum can detect whether a file changed when compared with a trusted earlier
checksum. It does not prove the source was correct, complete, or safe. A dump can
contain executable SQL; use only the archive created by this notebook here.
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
For this small restore, `--single-transaction` also prevents a failed operation
from leaving a partly restored set of transactional objects. It does not remove
preexisting target objects; start with the empty database created below.
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
        "--single-transaction",
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
# Run exactly the same SQL against a different database.
restore_check = subprocess.run(
    PG_PREFIX + [PSQL, "-X", "--set=ON_ERROR_STOP=on", "--tuples-only", "--no-align",
                 "--dbname", RESTORE_DB, "--command", source_check_sql],
    check=True,
    text=True,
    capture_output=True,
)
print(restore_check.stdout.strip())
assert restore_check.stdout.strip().splitlines() == expected_baseline
assert restore_check.stdout == source_check.stdout
print("The complete baseline and restored results agree.")
'''
        ),
        markdown(
            """
## 8. Verify Behavior With an Expected Failure

A restored table can contain rows while missing an integrity rule. This insert
must fail because `almost_done` is not an allowed status. A disconnected server
or a misspelled table would also produce an error, but neither proves the rule
works. We require PostgreSQL error code **23514** (check violation) and the exact
constraint name. The attempted write is inside a transaction that cannot commit.
"""
        ),
        code(
            r'''
invalid_insert = subprocess.run(
    PG_PREFIX
    + [
        PSQL,
        "-X",
        "--set=ON_ERROR_STOP=on",
        "--set=VERBOSITY=verbose",
        "--dbname",
        RESTORE_DB,
        "--command",
        """
        BEGIN;
        INSERT INTO metro_support.tickets
            (ticket_id, requester_id, status, subject)
        VALUES
            (1099, 101, 'almost_done', 'Constraint restore test');
        ROLLBACK;
        """,
    ],
    check=False,
    text=True,
    capture_output=True,
)

print("Constraint-test exit code:", invalid_insert.returncode)
print(invalid_insert.stderr.strip())
assert invalid_insert.returncode != 0, "The invalid status was not rejected."
assert "23514" in invalid_insert.stderr, "This was a different SQL failure, not a check violation."
assert '"tickets_status_allowed"' in invalid_insert.stderr

after_test = subprocess.run(
    PG_PREFIX + [PSQL, "-X", "--set=ON_ERROR_STOP=on", "--tuples-only", "--no-align",
                 "--dbname", RESTORE_DB, "--command",
                 "SELECT count(*) FROM metro_support.tickets WHERE ticket_id = 1099;"],
    check=True, text=True, capture_output=True,
)
assert after_test.stdout.strip() == "0"
print("The named status rule rejected the write; test ticket 1099 was not retained.")
'''
        ),
        markdown(
            """
## Your Check: Compare One Known Ticket

Counts would stay the same if a ticket's subject or requester changed. The query
below therefore compares one ticket's values and its requester's name. The loop
runs the same query once against the source and once against the restore.

First run the example for ticket 1001. Then change `CHECK_TICKET_ID` to **1002 or
1003** and run it again. Read that ticket's original `INSERT` above and check that
the result matches the intended record, not just the other database. Explain what
your check would catch that the counts would miss. You can extend the selected
columns if you want to test a different meaningful property; no new report is needed.
"""
        ),
        code(
            r'''
CHECK_TICKET_ID = 1001  # Change to 1002 or 1003 for your check.
assert CHECK_TICKET_ID in (1001, 1002, 1003)
known_ticket_sql = f"""
SELECT t.ticket_id, t.status, t.subject, u.display_name AS requester
FROM metro_support.tickets AS t
JOIN metro_support.users AS u ON u.user_id = t.requester_id
WHERE t.ticket_id = {CHECK_TICKET_ID};
"""

known_results = []
for database_name in (SOURCE_DB, RESTORE_DB):
    result = subprocess.run(
        PG_PREFIX + [PSQL, "-X", "--set=ON_ERROR_STOP=on", "--tuples-only", "--no-align",
                     "--dbname", database_name, "--command", known_ticket_sql],
        check=True, text=True, capture_output=True,
    )
    print(database_name, "->", result.stdout.strip())
    known_results.append(result.stdout.strip())

assert known_results[0] and known_results[0] == known_results[1]
print("This ticket's selected values match in source and restore.")
'''
        ),
        markdown(
            r"""
## Connection Reference: What Changes for Supabase?

Supabase Free projects do not receive the automatic database backups described
for paid plans. A course recovery plan therefore uses a logical connection and
runtime credential. The database tools stay the same; the host, port, user,
database, and TLS configuration change. This reference is not another required
cloud task. Never use the remote source as the restore target.

Obtain non-password `PGHOST`, `PGPORT`, `PGUSER`, and `PGDATABASE` values from
the approved connection panel. `--password` prompts rather than placing the
password in a visible connection URL:

```bash
pg_dump --format=custom --schema=metro_support --no-privileges \
  --host="$PGHOST" --port="$PGPORT" --username="$PGUSER" \
  --dbname="$PGDATABASE" --password --file=metro_support.dump
```

Use the current Supabase connection guidance. A direct endpoint may require IPv6;
the **session pooler** offers an IPv4-compatible path. Use the documented TLS
configuration; do not disable certificate verification to fix an unreachable
network. Use a matching-major client. Chapter 8 supplies the separate
`RESTORE_PGHOST`, `RESTORE_PGPORT`, `RESTORE_PGUSER`, and `RESTORE_PGDATABASE`
restore command with `--single-transaction`, `--no-owner`, and `--no-privileges`.
This schema archive does not include all Supabase Auth, Storage, or project settings.

Official free resources:

- <https://supabase.com/docs/guides/platform/backups>
- <https://supabase.com/docs/guides/database/connecting-to-postgres>
- <https://www.postgresql.org/docs/current/backup-dump.html>
"""
        ),
        markdown(
            """
## Recovery Record: Complete Before Submission

Write a short recovery account in this cell. Name the separate restore target,
summarize the supplied checks, explain your additional known-record check, and
identify one thing still untested. State which connection would change if
Supabase were the source. Use the results already above; do not copy them into
another table or create a second report.

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic data CC0.
"""
        ),
        markdown(
            """
## Finish: Remove Only This Run's Practice Resources

After completing your check and recovery account, keep the output in the notebook
and run this cell. It removes the two uniquely named practice databases and their
temporary artifact folder. The dump is not a submission or a retained recovery
copy. In Colab it also stops the service started for this practice; on your own
computer it leaves the preexisting PostgreSQL service running.

If an earlier cell fails, fix the stated problem or use this cleanup before
starting a fresh run. Do not substitute the name of a database you already use.
"""
        ),
        code(
            r'''
for database_name in (RESTORE_DB, SOURCE_DB):
    assert database_name in (
        "cst4714_recovery_source_" + run_id,
        "cst4714_recovery_restore_" + run_id,
    )
    subprocess.run(
        PG_PREFIX + [DROPDB, "--if-exists", database_name],
        check=True, text=True, capture_output=True,
    )

shutil.rmtree(ARTIFACT_DIR)
if IN_COLAB:
    subprocess.run(["service", "postgresql", "stop"], check=True)
del SOURCE_DB, RESTORE_DB
print("Removed this run's practice databases and artifact folder.")
print("Colab practice service stopped." if IN_COLAB else "Existing local service left running.")
'''
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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

This notebook introduces MongoDB through direct, visible operations. You will
insert a small synthetic fixture, query nested fields and arrays, update one test
document, interpret write results, and compare embedded and referenced shapes.

The default path uses `mongomock`, an in-memory teaching substitute. It supports
the operations used here but does not reproduce Atlas networking, indexes'
performance, durability, or every MongoDB feature. The same query cells also run
against Atlas. You do not need to complete both paths.

Run the cells in order. The supplied data cell is setup, not code you need to
memorize. After the worked query, you will change one filter and projection.
"""
        ),
        markdown(
            """
## Connection Setup

For local mode, leave `USE_ATLAS = False` and run the setup cells. No account or
network rule is needed. Installing the packages still requires internet access.

For Atlas, use your own **Free** cluster. Set `USE_ATLAS = True` below and run
the first setup cell to obtain this runtime's public IPv4 address and a practice
database name. Colab runs Python on Google's computer, so **Add Current IP** in
your laptop's browser may add the wrong address. The optional IP check contacts
the public ipify service; it sends no database credentials.

Do not set `tlsInsecure=True`. A TLS error is a signal to check the current driver,
URI, DNS, network rule, system time, and certificate path.
"""
        ),
        code(
            r'''
%pip -q install "pymongo>=4.13,<5" "mongomock>=4.3,<5"
'''
        ),
        code(
            r'''
from datetime import datetime, timezone
from getpass import getpass
from ipaddress import IPv4Address
from urllib.request import urlopen
from uuid import uuid4

import mongomock
from pymongo import MongoClient
from pymongo.server_api import ServerApi

USE_ATLAS = False  # Choose one path; the query cells are the same.
DATABASE_NAME = "cst4714_mql_" + uuid4().hex[:8]
print("Practice database:", DATABASE_NAME)

if USE_ATLAS:
    try:
        with urlopen("https://api.ipify.org", timeout=10) as response:
            runtime_ip = str(IPv4Address(response.read().decode().strip()))
        print("Temporary Atlas IP access-list entry:", runtime_ip + "/32")
    except Exception:
        raise RuntimeError(
            "The runtime IP check failed. Retry this cell or use local mode; "
            "do not replace the rule with access from everywhere."
        ) from None
'''
        ),
        markdown(
            """
**Atlas only: pause here before the connection cell.** In your Atlas project,
open **Network Access / IP Access List**, add the printed address as a temporary
entry, and wait for it to become active. A `/32` rule allows one IPv4 address.
If the runtime restarts or its outgoing route changes, check the address again.

In **Database Access**, use a database user with read/write access to the printed
practice database. This is different from your Atlas website login. In the
cluster's **Connect > Drivers** instructions, select Python and copy the URI.
Replace the password placeholder with that database user's password. Reserved
password characters inside a URI need percent encoding; do not paste a password
into a code cell. Enter the finished URI only in the hidden prompt below.

`MongoClient` creates a connection manager. `ping` sends an actual command and
checks that the deployment responds. Successful ping does not prove permission
to insert or delete documents; the following cells test those operations.

Use a fresh practice name only after cleaning up the previous run. The database
and collection variables below are handles; the first write creates stored data.
"""
        ),
        code(
            r'''
client = None
mongodb_uri = None
if USE_ATLAS:
    try:
        mongodb_uri = getpass("Paste your Atlas driver URI (hidden): ")
        client = MongoClient(
            mongodb_uri,
            tls=True,
            tlsInsecure=False,
            server_api=ServerApi("1", strict=True, deprecation_errors=True),
            serverSelectionTimeoutMS=10000,
            timeoutMS=10000,
        )
        client.admin.command("ping")
        print("MongoDB responded to ping.")
    except Exception:
        if client is not None:
            client.close()
        raise RuntimeError(
            "Atlas connection failed. Check deployment readiness, database "
            "user/password, the runtime IP rule, driver URI, and DNS/TLS. "
            "Keep certificate verification enabled. Local mode remains available."
        ) from None
    finally:
        mongodb_uri = None  # Do not retain a second copy of the URI in this variable.
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

Every course document carries `course_fixture: "cst4714"`. Rerunning this data cell
replaces only those marked records in this run's private `tickets` collection.
The last cell removes that entire practice collection and closes the client.
Do not put personal or project data in this temporary collection.

The six tickets use BSON dates through Python `datetime` values, nested requester
documents, tag arrays, and embedded event arrays. This is a small teaching
adaptation of the CSV case: `event_type` becomes `type`, `event_at` becomes `at`,
and the supplied `actor_role` describes the actor. It is not a lossless import
of every CSV column. Empty arrays on 1005 and 1006 mean this fixture omits their
history, not that the original tickets never had events.
"""
        ),
        code(
            r'''
tickets.delete_many({"course_fixture": "cst4714"})
tickets.create_index("ticket_id", unique=True)

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

The result grain is one document per matching ticket. The first dictionary is
the filter: every listed field condition must hold. `$in` supplies alternatives
for one field. The second dictionary is the projection: `1` includes a field,
while `_id: 0` suppresses the otherwise included identifier. These choices change
the returned view, not the stored document.

`find` returns a cursor that the `for` loop reads. This example orders by opening
time descending. The six-ticket fixture has one active high/urgent ticket: 1001.
Ticket 1003 is urgent but resolved, so it does not pass the status filter.
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

First inspect a counterexample. Ticket 1001 has a resident-created event and a
different agent-assigned event. Separate dotted predicates for `created` and
`agent` can match those different events. A request for an event *created by an
agent* must require both conditions on the same element.
"""
        ),
        code(
            r'''
separate_elements = {
    "course_fixture": "cst4714",
    "events.type": "created",
    "events.actor_role": "agent",
}
same_element = {
    "course_fixture": "cst4714",
    "events": {"$elemMatch": {"type": "created", "actor_role": "agent"}},
}
print("Separate conditions:", [d["ticket_id"] for d in tickets.find(separate_elements)])
print("Same event required:", [d["ticket_id"] for d in tickets.find(same_element)])
# Expect [1001, 1002, 1003] versus []. No fixture event was created by an agent.

print("Status changes made by an agent:")
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

This cell resets only test ticket 1099, then inserts it in state `new`. Rerunning
the setup cell starts this small write experiment again without making duplicates.
The unique index prevents two documents from sharing one ticket number.
"""
        ),
        code(
            r'''
test_filter = {"ticket_id": 1099, "test_record": True, "course_fixture": "cst4714"}
tickets.delete_many(test_filter)
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
'''
        ),
        markdown(
            """
Run the next cell **twice without rerunning the insertion cell**. `$set` changes
only its named fields. The first execution should report `1 1`: one match and one
modified document. The second should report `1 0`: the same document already has
the requested values. The read-back checks what is actually stored.
"""
        ),
        code(
            r'''
first_update = tickets.update_one(
    test_filter,
    {"$set": {"status": "in_progress", "assignee_id": 202}},
)
print("Matched/modified:", first_update.matched_count, first_update.modified_count)
print(tickets.find_one(test_filter, {"_id": 0, "ticket_id": 1, "status": 1, "assignee_id": 1}))
'''
        ),
        markdown(
            """
Now compare an **expected-state filter**. This operation asks to change a ticket
only while it is `new`. Our ticket is already `in_progress`, so `0 0` is correct.
An empty match is different from a match whose values did not change.
"""
        ),
        code(
            r'''
stale_update = tickets.update_one(
    {**test_filter, "status": "new"},
    {"$set": {"status": "resolved"}},
)
print("Expected-state filter matched/modified:", stale_update.matched_count, stale_update.modified_count)
print("Status is still:", tickets.find_one(test_filter)["status"])

'''
        ),
        markdown(
            """
## 6. Append One Event and Read Back the Final Document

`$push` appends to the array. This example also requires event 5999 to be absent.
Rerunning the cell therefore does not append the same event again. That narrow
guard works for this one document; it is not a complete event-processing system.

This append and the earlier status change are **two separate writes**. A reader
between them could see the new status without the event. Day 2 shows how one
update can change status and append an embedded event atomically.
"""
        ),
        code(
            r'''
event_update = tickets.update_one(
    {**test_filter, "events.event_id": {"$ne": 5999}},
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
print(tickets.find_one(test_filter, {"_id": 0}))
'''
        ),
        markdown(
            """
## 7. Delete Only the Disposable Record

The predicate includes both the identifier and the safety marker. The final query
confirms cleanup.
"""
        ),
        code(
            r'''
print("Preview:", tickets.find_one(test_filter, {"_id": 0, "ticket_id": 1}))
delete_result = tickets.delete_one(test_filter)
print("Deleted count:", delete_result.deleted_count)
print("Remaining test record:", tickets.find_one(test_filter))
print("Other fixture tickets:", tickets.count_documents({"course_fixture": "cst4714"}))
'''
        ),
        markdown(
            """
## 8. Compare Two Models

These are partial design sketches, not additional database writes. The referenced
event stores `ticket_id`; the parent does not need a list that grows by one ID
for every event. Day 2 develops the read and update consequences.
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
}
referenced_event = {"event_id": 5001, "ticket_id": 1001, "type": "created"}

print("Embedded sketch:", embedded_ticket)
print("Referenced sketch:", referenced_ticket)
print("Separate event sketch:", referenced_event)
'''
        ),
        markdown(
            """
## Results Record: Complete Before Submission

In a short explanation, name your changed filter/projection and one returned
ticket, explain the array counterexample using actual IDs, and interpret the
first and repeated write counts, compared with the expected-state filter. Explain why the delete targeted only the test
record. If you used local mode, say so; no Atlas account task is required on that
path. Day 2's assignment develops the model comparison further.

Before submitting, remove any accidentally saved credential from source or output.

**License:** prose CC BY-NC-SA 4.0; code MIT; synthetic data CC0.
"""
        ),
        code(
            r'''
try:
    database.drop_collection("tickets")
    print("Removed the tickets collection from this run's practice database.")
finally:
    client.close()
    mongodb_uri = None
print("The database client is closed. Later lessons supply fresh fixtures.")
if USE_ATLAS:
    print("In Atlas, remove the temporary IP rule and any class-only database user.")
    print("This cleanup does not delete or stop your Free cluster.")
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
# MongoDB Document Recovery and Collection Rules

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

Five synthetic tickets have been exported. We will restore them elsewhere, then
find an error that a correct count and a correct date type both miss. Your change
repairs one document from the saved artifact. We also restore the collection's
rules and test whether they work.

Keep all work and your short recovery recommendation in this notebook. The file
you produce contains document data, not a complete Atlas project backup.
`mongodump` and `mongorestore` cover a broader logical recovery scope.
"""
        ),
        markdown('''
## Connection or Local Practice

Keep `USE_ATLAS = False` for local practice with `mongomock`, an in-memory library.
It can run this document recovery exercise and enforce a unique index, but cannot
enforce MongoDB's server-side schema validator. We label that difference below.
Package installation still requires internet access.

For Atlas, use your existing Free cluster and set the switch to `True`. Colab runs
on Google's computer, not your laptop. The next cell contacts ipify without your
database credentials and prints the runtime's IPv4 address. Add that `/32` address
to Atlas temporarily. **Add Current IP** in your laptop browser can add the wrong
address. Do not enable access from everywhere.
'''),
        code(
            r'''
%pip -q install "pymongo>=4.13,<5" "mongomock>=4.3,<5"
'''
        ),
        code(
            r'''
from datetime import datetime, timezone
from getpass import getpass
from ipaddress import IPv4Address
import hashlib
import json
from pathlib import Path
from pprint import pprint
from urllib.request import urlopen
from uuid import uuid4

import mongomock
from bson import json_util
from bson.json_util import CANONICAL_JSON_OPTIONS
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from pymongo.server_api import ServerApi

USE_ATLAS = False
DATABASE_SUFFIX = uuid4().hex[:8]
SOURCE_DB = f"cst4714_recovery_source_{DATABASE_SUFFIX}"
RESTORE_DB = f"cst4714_recovery_restore_{DATABASE_SUFFIX}"
EXPORT_FILE = Path(f"/tmp/cst4714_tickets_{DATABASE_SUFFIX}.json")
print("Source:", SOURCE_DB)
print("Restore target:", RESTORE_DB)

if USE_ATLAS:
    try:
        with urlopen("https://api.ipify.org", timeout=10) as response:
            runtime_ip = str(IPv4Address(response.read().decode().strip()))
        print("Temporary Atlas IP access-list entry:", runtime_ip + "/32")
    except Exception:
        raise RuntimeError(
            "The runtime IP check failed. Retry or use local mode; "
            "do not open access from everywhere."
        ) from None
'''
        ),
        markdown('''
**Atlas only: pause before the next cell.** In **Network Access / IP Access List**,
add the printed address as a temporary entry and wait for it to become active.
Your database user needs read/write access, collection creation, index creation,
and `collMod` permission for the two printed practice databases. That user is
different from your Atlas website login. Ask for help scoping these permissions
rather than weakening an existing collection or a shared project.

In **Connect > Drivers**, choose Python and copy the driver URI. Replace its
password placeholder and percent-encode reserved password characters. Enter the
finished URI only into the hidden prompt. The code keeps certificate verification
enabled and clears the URI variable afterward. A successful `ping` proves a
response, not permission for every later operation.

Run configuration once per experiment, and clean up before starting a fresh run.
The data cells may be repeated in order. They reset only the `tickets` collections
inside these newly named practice databases, never a project collection.
'''),
        code('''
client = None
mongodb_uri = None
if USE_ATLAS:
    try:
        mongodb_uri = getpass("Atlas driver URI (hidden): ")
        client = MongoClient(
            mongodb_uri, tls=True, tlsInsecure=False, tz_aware=True,
            server_api=ServerApi("1", strict=True, deprecation_errors=True),
            serverSelectionTimeoutMS=10000, timeoutMS=10000,
        )
        client.admin.command("ping")
        print("MongoDB responded to ping.")
    except Exception:
        if client is not None:
            client.close()
        raise RuntimeError(
            "Atlas connection failed. Check the runtime IP rule, database "
            "credentials, driver URI, deployment state, and DNS/TLS. "
            "Keep certificate verification enabled; local mode is available."
        ) from None
    finally:
        mongodb_uri = None
else:
    client = mongomock.MongoClient(tz_aware=True)
    print("Local document recovery. Server validation will not execute.")
'''
        ),
        markdown(
            """
## 1. Save Five Tickets and Recover Them Elsewhere

The source collection has a focused validator in Atlas and a compound index. The
local library supports the documents and indexes but not server-side validation.
The unique `ticket_id` index prevents two documents from claiming the same ticket
number. The compound index supports the status-and-date workload from Week 11.
Neither index is part of an ordinary ticket document.
"""
        ),
        code(
            r'''
source_database = client[SOURCE_DB]
# Reset only this notebook's source collection when repeating its setup.
source_database.drop_collection("tickets")

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
    source_database.create_collection(
        "tickets", validator=ticket_validator,
        validationLevel="strict", validationAction="error",
    )
else:
    source_database.create_collection("tickets")
    print("Offline path: server-side $jsonSchema validation is not implemented by mongomock.")

source_tickets = source_database["tickets"]
source_tickets.create_index("ticket_id", unique=True, name="unique_ticket_id")
source_tickets.create_index(
    [("status", ASCENDING), ("opened_at", DESCENDING)], name="status_by_date"
)

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
pprint(list(source_tickets.find({}, {"_id": 0}).sort("ticket_id", 1)))
'''
        ),
        markdown(
            """
### The Document File and Its Limits

Canonical Extended JSON preserves BSON type information such as dates and ObjectId
values in a JSON-compatible representation. File size and SHA-256 identify the
exact artifact; the separate restore determines whether it can be used. The
manifest printed below describes the expected collection and its rules. It stays
in the notebook, separately from the document file. That distinction matters if
someone gives you the JSON file alone.

`json.loads` recognizes JSON syntax but leaves `$date` as a dictionary.
`json_util.loads` understands MongoDB's type markers. A UTC datetime and a string
containing a date are different stored values. For this fixture, BSON stores
dates to millisecond precision. The same stored date may display in another
timezone without representing a different instant.
"""
        ),
        code(
            r'''
documents_to_export = list(source_tickets.find({}).sort("ticket_id", ASCENDING))
JSON_OPTIONS = CANONICAL_JSON_OPTIONS.with_options(tz_aware=True)
expected_canonical = json_util.dumps(
    documents_to_export, json_options=JSON_OPTIONS, sort_keys=True
)
export_text = json_util.dumps(
    documents_to_export,
    json_options=JSON_OPTIONS,
    indent=2,
)
EXPORT_FILE.write_text(export_text + "\n", encoding="utf-8")

export_bytes = EXPORT_FILE.read_bytes()
export_sha256 = hashlib.sha256(export_bytes).hexdigest()
print("Artifact:", EXPORT_FILE)
print("Bytes:", len(export_bytes))
print("SHA-256:", export_sha256)
print("First 300 characters:\n", export_text[:300])

manifest = {
    "collection": "tickets",
    "document_count": 5,
    "ticket_ids": [1001, 1002, 1003, 1004, 1005],
    "sha256": export_sha256,
    "indexes": source_tickets.index_information(),
    "validator": ticket_validator,
    "server_validator_installed": USE_ATLAS,
}
pprint(manifest)
plain_json = json.loads(export_text)
print("Plain JSON parser gives:", type(plain_json[0]["opened_at"]).__name__)
'''
        ),
        markdown(
            """
### A Separate Restore Target

The restore database name is different from the source. Parsing with `json_util`
reconstructs BSON-aware Python values before insertion. We verify the file hash
and parse it **before** resetting the disposable restore collection. A hash match
means these bytes match the recorded digest; it does not prove that the export
was complete, came from a trustworthy source, or represents a consistent live
multi-collection moment. These five source documents are not changing during export.
"""
        ),
        code(
            r'''
restore_bytes = EXPORT_FILE.read_bytes()
assert hashlib.sha256(restore_bytes).hexdigest() == manifest["sha256"]
restored_documents = json_util.loads(restore_bytes.decode("utf-8"), json_options=JSON_OPTIONS)
assert len(restored_documents) == manifest["document_count"]
assert [doc["ticket_id"] for doc in restored_documents] == manifest["ticket_ids"]
parsed_canonical = json_util.dumps(
    restored_documents, json_options=JSON_OPTIONS, sort_keys=True
)
assert parsed_canonical == expected_canonical

restore_database = client[RESTORE_DB]
assert RESTORE_DB != SOURCE_DB
restore_database.drop_collection("tickets")
restore_tickets = restore_database["tickets"]
restore_result = restore_tickets.insert_many(restored_documents)
print("Restored documents:", len(restore_result.inserted_ids))
print("Restore count:", restore_tickets.count_documents({}))
'''
        ),
        markdown(
            """
### A Verification Baseline

The expected active IDs are 1001, 1002, and 1004. The other tickets are resolved,
not missing. We compare complete values as well as count, identifiers, and types.
The full comparison serializes values with the same Canonical Extended JSON
options and sorted field names. This also distinguishes an integer from a double
that displays the same numeric value. For this small fixture we can inspect every
saved document; a large production
dataset needs a verification strategy appropriate to its size and invariants.
"""
        ),
        code(
            r'''
source_ids = [
    doc["ticket_id"]
    for doc in source_tickets.find({}, {"_id": 0, "ticket_id": 1}).sort("ticket_id", 1)
]
restore_ids = [
    doc["ticket_id"]
    for doc in restore_tickets.find({}, {"_id": 0, "ticket_id": 1}).sort("ticket_id", 1)
]
print("Source IDs:", source_ids)
print("Restore IDs:", restore_ids)
assert source_ids == restore_ids == manifest["ticket_ids"]

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
assert [doc["ticket_id"] for doc in active] == [1001, 1002, 1004]
restored_canonical = json_util.dumps(
    list(restore_tickets.find({}).sort("ticket_id", 1)),
    json_options=JSON_OPTIONS, sort_keys=True,
)
assert restored_canonical == expected_canonical
print("All five restored documents match the saved values.")
'''
        ),
        markdown('''
## 2. Diagnose and Repair a Misleading Restore

A migration after restoration replaced one ticket's subject with incorrect text.
The mistake still satisfies the schema: the subject remains a string. Predict
which checks below will notice it. Choose `1001` or `1004` in the next cell.
This deliberately changes the disposable **restore target**, not the source or
the saved artifact. You are testing a recovery check, not simulating replication.
'''),
        code('''
DAMAGED_TICKET = 1001  # You may choose 1004 instead.
assert DAMAGED_TICKET in (1001, 1004)
restore_tickets.update_one(
    {"ticket_id": DAMAGED_TICKET},
    {"$set": {"subject": "Text replaced by an incorrect migration"}},
)

current_documents = list(restore_tickets.find({}).sort("ticket_id", 1))
print("Correct count:", len(current_documents) == manifest["document_count"])
print("Correct IDs:", [doc["ticket_id"] for doc in current_documents] == manifest["ticket_ids"])
print(
    "All dates are datetime:",
    all(isinstance(doc["opened_at"], datetime) for doc in current_documents),
)
current_canonical = json_util.dumps(current_documents, json_options=JSON_OPTIONS, sort_keys=True)
print("All document values match:", current_canonical == expected_canonical)

# Build the lookup from documents parsed from the verified artifact, not a new source query.
saved_by_id = {doc["ticket_id"]: doc for doc in restored_documents}
print("Saved subject:", saved_by_id[DAMAGED_TICKET]["subject"])
print("Restored subject:", restore_tickets.find_one({"ticket_id": DAMAGED_TICKET})["subject"])
'''),
        markdown('''
### Your Repair

The current database is wrong, so use the saved version as the recovery source.
Replace `None` below with `saved_by_id[DAMAGED_TICKET]`. Read the two arguments
to `replace_one`: the first selects one ticket, and the second is its complete
replacement document. The saved `_id` still identifies that same document.

Run the cell and verify that all five documents match again. Rerunning this
repair should not insert a sixth ticket. Explain why the first three checks
above passed even when the restored subject was wrong. If you want to repeat
with the other ticket, repair the first one before making another change.
'''),
        code('''
recovery_document = None  # Replace None with the saved document described above.

if recovery_document is None:
    print("Repair not completed: choose the saved document, then rerun this cell.")
else:
    assert recovery_document["ticket_id"] == DAMAGED_TICKET
    repair = restore_tickets.replace_one({"ticket_id": DAMAGED_TICKET}, recovery_document)
    assert repair.matched_count == 1

repaired_canonical = json_util.dumps(
    list(restore_tickets.find({}).sort("ticket_id", 1)),
    json_options=JSON_OPTIONS, sort_keys=True,
)
all_values_recovered = repaired_canonical == expected_canonical
print("All document values recovered:", all_values_recovered)
print("Ticket count:", restore_tickets.count_documents({}))
'''),
        markdown(
            """
## 3. Restore Rules and Test Their Behavior

Collection indexes and validators are database metadata. The document-only export
did not recreate them automatically. MongoDB creates the `_id_` index itself.
Our separate setup instructions, not the JSON document file, supply the unique
ticket key, compound index, and validator. Rerunning this rule cell is safe.
"""
        ),
        code(
            r'''
print("Restore indexes before repair:", sorted(restore_tickets.index_information()))
print("On the first document-only restore, only the automatic _id_ index exists.")

restore_tickets.create_index("ticket_id", unique=True, name="unique_ticket_id")
restore_tickets.create_index(
    [("status", ASCENDING), ("opened_at", DESCENDING)], name="status_by_date"
)

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

print("Restore indexes after repair:", sorted(restore_tickets.index_information()))
'''
        ),
        markdown(
            """
### Allowed and Rejected Writes

First a valid test document must succeed. Then a duplicate ticket number must
fail, even with a different `_id`. Atlas additionally tests an invalid status,
a string date, and a missing date. Error 121 means document validation failed;
error 11000 means a unique index rejected a duplicate. Other errors are not
evidence that these rules worked. All temporary test documents are removed.

Local mode tests the unique index, but its schema results are a **supplied trace
to interpret**, not results from your runtime. A validator also cannot detect
every wrong value: the damaged subject above was still a permitted string.
"""
        ),
        code(
            r'''
valid_document = {
    "ticket_id": 1099,
    "status": "new",
    "priority": "low",
    "subject": "Temporary allowed write",
    "opened_at": datetime(2026, 2, 6, tzinfo=timezone.utc),
}
test_ids = [1099, 1100, 1101, 1102]
try:
    restore_tickets.insert_one(valid_document)
    print("Valid document accepted.")
    duplicate = dict(saved_by_id[1001])
    duplicate.pop("_id")  # Different internal ID, same ticket_id.
    try:
        duplicate_result = restore_tickets.insert_one(duplicate)
    except DuplicateKeyError:
        print("Duplicate ticket_id rejected by the unique index: 11000.")
    else:
        restore_tickets.delete_one({"_id": duplicate_result.inserted_id})
        raise AssertionError("The unique ticket_id index did not reject a duplicate.")

    cases = [
        ("Invalid status", {**valid_document, "ticket_id": 1100, "status": "almost_done"}),
        ("Date stored as text", {**valid_document, "ticket_id": 1101, "opened_at": "2026-02-06"}),
        ("Missing date", {
            key: value for key, value in valid_document.items() if key != "opened_at"
        }),
    ]
    cases[2][1]["ticket_id"] = 1102
    for label, document in cases:
        document.pop("_id", None)  # insert_one added an _id to valid_document.
        if USE_ATLAS:
            try:
                restore_tickets.insert_one(document)
            except OperationFailure as error:
                if error.code != 121:
                    raise
                print(label, "rejected. MongoDB error code:", error.code)
            else:
                raise AssertionError(label + " unexpectedly accepted.")
        else:
            print(
                "Supplied trace, NOT a result from this runtime:",
                label, "would be rejected with code 121.",
            )
finally:
    restore_tickets.delete_many({"ticket_id": {"$in": test_ids}})

assert restore_tickets.count_documents({}) == 5
print("Temporary test documents removed; five practice tickets remain.")
'''
        ),
        markdown(
            """
### How This Compares With a Database Dump

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
the recovery sequence and the limitations of a narrower artifact.
"""
        ),
        markdown(
            """
## Your Recovery Recommendation

If a colleague handed you only the JSON file, what could you recover, and what
else would you ask for before reopening the application? Write a short answer
using one actual result, one separately recreated rule or index, and a comparison
with Week 8's PostgreSQL archive. Include why the wrong subject passed the count
check and how you recovered it. Name whether server validation ran in Atlas or
you interpreted the supplied local trace. Do not claim to have tested failover.

The comparison table above is supplied reading, not another submission task.
Before submitting, remove any accidentally saved credential from source or output.
"""
        ),
        markdown('''
Replace this paragraph with your short recovery recommendation. This is the only
written response; keep it in the notebook with your completed repair and outputs.
'''),
        markdown('''
## Cleanup

Run this cell after finishing. It removes only the two practice `tickets`
collections and this run's temporary JSON file, then closes the Python client.
Other collections are left alone. No exported file needs to be submitted.

If you used Atlas, remove the temporary IP access-list entry in the dashboard.
Closing a Python client does not shut down an Atlas cluster. Leave shared
deployments and other projects untouched. Remove the runtime-IP cell output
before submitting, along with any credential accidentally entered in source.
'''),
        code(
            r'''
source_database.drop_collection("tickets")
restore_database.drop_collection("tickets")
EXPORT_FILE.unlink(missing_ok=True)
client.close()
print("Removed both practice collections and the temporary file; client closed.")
'''
        ),
        markdown('''
## Further Reading

- [PyMongo Extended JSON](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/data-formats/extended-json/)
- [MongoDB schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [Atlas Free limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
- [mongodump](https://www.mongodb.com/docs/database-tools/mongodump/) and [mongorestore](https://www.mongodb.com/docs/database-tools/mongorestore/)
- [Atlas IP access list](https://www.mongodb.com/docs/atlas/security/ip-access-list/)

Course prose: CC BY-NC-SA 4.0. Code: MIT. Synthetic fixture: CC0.
'''),
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

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

This notebook uses a small teaching snapshot of the U.S. Cybersecurity and
Infrastructure Security Agency's Known Exploited Vulnerabilities catalog. It
connects four skills: evaluating a source, checking data quality, reasoning about
distribution, and loading records without creating duplicates.

**By the end, you will be able to:**

- identify source, retrieval, transformation, and use limits before importing;
- check nulls, duplicates, identifiers, and dates;
- compare cardinality, frequency, monotonicity, and query targeting;
- explain range and hashed distribution with measured results;
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
selection. It is a compact classroom fixture, not a current vulnerability-
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
from uuid import uuid4

from pymongo import MongoClient
from pymongo.server_api import ServerApi
import psycopg
from psycopg import sql
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

A successful JSON parse does not establish that the records are suitable for a
database. We check missing values, duplicate identifiers, and ISO date values
first.
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
print("This describes input order, not production write order.")
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

Use these questions to interpret the output before loading. They are discussion
prompts, not a separate written submission:

1. **Current scale:** This sample contains ___ records and is/is not large enough
   to justify sharding because ___.
2. **Candidate results:** ___ has ___ distinct values; its largest value holds
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

# Keep these names while rerunning a load cell. A new setup run starts fresh.
run_id = uuid4().hex[:8]
atlas_database_name = "cst4714_public_data_" + run_id
postgres_schema = "cst4714_data_" + run_id
atlas_client = None
rows = [
    (
        record["cveID"], record["vendorProject"], record["product"],
        record["vulnerabilityName"], record["dateAdded"], record["dueDate"],
        record["knownRansomwareCampaignUse"], json.dumps(record["cwes"]),
    )
    for record in records
]

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
"""
        ),
        markdown(
            """
### Import Into the Existing SQLite Table

The previous cell creates the practice environment. The next cell loads records
into that **same** environment. Run this import cell twice without recreating the
connection. The primary key identifies a vulnerability; `ON CONFLICT` updates it
instead of appending a duplicate.
"""
        ),
        code(
            """
if LOAD_SQLITE:
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
    if atlas_client is not None:
        atlas_client.close()
    atlas_uri = getpass("Atlas connection URI (hidden): ")
    atlas_client = MongoClient(
        atlas_uri,
        server_api=ServerApi("1", strict=True, deprecation_errors=True),
        serverSelectionTimeoutMS=10000,
        timeoutMS=10000,
    )
    atlas_client.admin.command("ping")

    atlas_collection = atlas_client[atlas_database_name]["kev_sample"]
    atlas_collection.create_index("cveID", unique=True)
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

The next cell creates a uniquely named practice schema. `sql.Identifier` quotes
that schema name correctly; `%s` placeholders are for **values**, not table names.
`SET LOCAL search_path` applies only within each explicit connection transaction.
We set it again when verifying through a new connection instead of assuming the
provider will reuse the previous session.
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
            cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
                sql.Identifier(postgres_schema)))
            cursor.execute(sql.SQL("SET LOCAL search_path TO {}").format(
                sql.Identifier(postgres_schema)))
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kev_sample (
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
                INSERT INTO kev_sample VALUES
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

These checks do not establish completeness of the full live catalog, correct
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
            cursor.execute(sql.SQL("SET LOCAL search_path TO {}").format(
                sql.Identifier(postgres_schema)))
            cursor.execute("SELECT count(*) FROM kev_sample")
            postgres_count = cursor.fetchone()[0]
            cursor.execute(
                "SELECT cve_id, vendor_project, product FROM kev_sample WHERE cve_id = %s",
                (known_id,),
            )
            postgres_known = cursor.fetchone()
            cursor.execute('''
                SELECT vendor_project, count(*) AS vulnerability_count
                FROM kev_sample
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

Write a short explanation of the question you asked, why your key choice fits
or does not fit it, and what happened when you reran the import into the same
target. Use two capacity measurements and one verification result already shown
above. Acknowledge the historical subset and one limitation of your analysis.
Do not reproduce every output in a second report.

Before submitting, remove any accidentally saved credential from source or output.
"""
        ),
        markdown(
            """
## Final-Project Transfer

This checkpoint does not add or redefine final-project deliverables. Use the
final-project assignment supplied in Brightspace or the course package.

Consider these prompts during project work. No additional written response is
required:

1. My project could use a public or synthetic dataset about ___.
2. The source of truth should be ___ because ___.
3. My first scale trigger would be measured as ___.
4. Before scaling, I would verify ___ and improve ___ because ___.

If you used a cloud path, close the client and remove temporary broad network
access after class. The cleanup cell removes only this notebook's Atlas fixture
database and PostgreSQL schema whose unique names were generated for this run.
"""
        ),
        code(
            """
if LOAD_ATLAS:
    atlas_client.drop_database(atlas_database_name)
    print("Removed this run's Atlas database:", atlas_database_name)
    atlas_client.close()
    print("Closed the Atlas client. Review and narrow temporary network access.")
    atlas_uri = None
if LOAD_POSTGRES:
    with psycopg.connect(postgres_url, connect_timeout=10) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(
                sql.Identifier(postgres_schema)))
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


def build_aggregation_validation() -> None:
    notebook = nbf.v4.new_notebook(metadata={
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
        "colab": {"name": "07_aggregation_validation.ipynb", "provenance": []},
        "license": "Notebook prose CC BY-NC-SA 4.0; code MIT",
    })
    notebook["cells"] = [
        markdown('''
# From Tickets to a Reliable Summary

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

A manager wants the number of active requests in each category. A pipeline can
answer that question, but an innocent-looking array operation can inflate the
counts. We will see the error, explain it, and keep invalid statuses out of new
documents.

This is a fresh four-ticket teaching case, not the complete 12-ticket CSV dataset.
You do not need Week 10's database. The default runs aggregation locally with
`mongomock`. Atlas runs the same pipeline on MongoDB and additionally enforces
the collection validator. The local library does **not** implement that server
feature; its validation section is a clearly labeled trace to interpret.
'''),
        markdown('''
## Connection or Local Practice

Keep `USE_ATLAS = False` to begin without an account. Package installation still
requires internet access. For Atlas, use your own existing Free cluster and set
the switch to `True`. The next cell prints a new practice database name and this
runtime's public IPv4 address. It contacts ipify without database credentials.

Colab runs on Google's computer, not your laptop. **Add Current IP** in your
laptop's browser can therefore add the wrong address. Use the printed `/32`
address, which allows one IPv4 address. Do not open access from everywhere.
'''),
        code('%pip -q install "pymongo>=4.13,<5" "mongomock>=4.3,<5"'),
        code('''
from datetime import datetime, timezone
from getpass import getpass
from ipaddress import IPv4Address
from pprint import pprint
from urllib.request import urlopen
from uuid import uuid4

import mongomock
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from pymongo.server_api import ServerApi

USE_ATLAS = False
database_name = "cst4714_pipeline_" + uuid4().hex[:8]
print("Practice database:", database_name)

if USE_ATLAS:
    try:
        with urlopen("https://api.ipify.org", timeout=10) as response:
            runtime_ip = str(IPv4Address(response.read().decode().strip()))
        print("Temporary Atlas IP access-list entry:", runtime_ip + "/32")
    except Exception:
        raise RuntimeError(
            "The runtime IP check failed. Retry or use local mode; "
            "do not open access from everywhere."
        ) from None
'''),
        markdown('''
**Atlas only: pause before connecting.** In **Network Access / IP Access List**,
add the printed address as a temporary entry and wait for it to become active.
Recheck after a runtime restart or an outgoing IP change. Your database user is
different from your Atlas website login. It needs read/write access to this
practice database and permission to modify its collection validator (`collMod`).
Ask the instructor to help scope that permission rather than changing a shared
collection or disabling validation. Local mode remains available.

In **Connect > Drivers**, select Python and copy the driver URI. Replace its
password placeholder; reserved characters in the password need URI percent
encoding. Enter the finished URI only in the hidden prompt, never a code cell.
`ping` tests whether MongoDB responds, not whether every later operation is
authorized. Keep TLS verification enabled. Check the runtime IP, database user,
URI, deployment state, and current driver if connection fails.

Run setup once per experiment. Clean up before creating a new practice name.
These handles select a database and collection; the first write stores data.
'''),
        code('''
client = None
mongodb_uri = None
if USE_ATLAS:
    try:
        mongodb_uri = getpass("Atlas driver URI (hidden): ")
        client = MongoClient(
            mongodb_uri, tls=True, tlsInsecure=False,
            server_api=ServerApi("1", strict=True, deprecation_errors=True),
            serverSelectionTimeoutMS=10000, timeoutMS=10000,
        )
        client.admin.command("ping")
        print("MongoDB responded to ping.")
    except Exception:
        if client is not None:
            client.close()
        raise RuntimeError(
            "Atlas connection failed. Check the runtime IP rule, database "
            "credentials, driver URI, deployment state, and DNS/TLS. "
            "Keep certificate verification enabled; local mode is available."
        ) from None
    finally:
        mongodb_uri = None
else:
    client = mongomock.MongoClient()
    print("Local aggregation practice. Server validation will not execute.")

database = client[database_name]
tickets = database["tickets"]
'''),
        markdown('''
## 1. Read the Four Tickets Before Querying

Each document is one ticket. `events` is a list of events **inside** that ticket.
An empty list is valid. A resolved ticket still exists but does not belong in an
active workload count. In this course, active means `new`, `open`, or `in_progress`.

Predict the active IDs and the number of active tickets in each category from
the fixture. This gives us a check independent of our aggregation syntax.
'''),
        code('''
fixture = [
    {"ticket_id": 1001, "category": "streetlight", "status": "open",
     "priority": "urgent", "subject": "Dark streetlight", "assignee_id": 201,
     "opened_at": datetime(2026, 2, 1, tzinfo=timezone.utc),
     "events": [{"type": "created"}, {"type": "assigned"}]},
    {"ticket_id": 1002, "category": "sanitation", "status": "in_progress",
     "priority": "high", "subject": "Missed pickup", "assignee_id": 202,
     "opened_at": datetime(2026, 2, 2, tzinfo=timezone.utc),
     "events": [{"type": "created"}]},
    {"ticket_id": 1003, "category": "streetlight", "status": "resolved",
     "priority": "urgent", "subject": "Lamp repaired", "assignee_id": 201,
     "opened_at": datetime(2026, 2, 3, tzinfo=timezone.utc),
     "events": [{"type": "created"}, {"type": "resolved"}]},
    {"ticket_id": 1004, "category": "streetlight", "status": "new",
     "priority": "low", "subject": "Flickering lamp", "assignee_id": None,
     "opened_at": datetime(2026, 2, 4, tzinfo=timezone.utc), "events": []},
]
# Reset only this notebook's collection when repeating the fixture cell.
tickets.create_index("ticket_id", unique=True)
tickets.delete_many({})
tickets.insert_many(fixture)
pprint(list(tickets.find({}, {"_id": 0, "ticket_id": 1, "category": 1, "status": 1})))
'''),
        markdown('''
## 2. Build a Summary One Stage at a Time

`$match` selects input documents. `$group` creates one output for each distinct
group key. `$sum: 1` adds one for each input reaching that group, regardless of
how many documents existed before earlier stages.

The dollar sign in `"$category"` means read that field's value. The string
`"category"` without the dollar would group every input under one constant label.
`$project` chooses the final shape, and `$sort` makes display order predictable.
'''),
        code('''
active_filter = {"status": {"$in": ["new", "open", "in_progress"]}}

pipeline = [
    {"$match": active_filter},  # Input/output: one ticket per document.
    {"$group": {"_id": "$category", "active_count": {"$sum": 1}}},
    {"$project": {"_id": 0, "category": "$_id", "active_count": 1}},
    {"$sort": {"category": 1}},  # Output: one summary per category.
]

for end in range(1, len(pipeline) + 1):
    result = list(tickets.aggregate(pipeline[:end]))
    print("After", list(pipeline[end - 1])[0], ":", len(result), "documents")
    pprint(result)
'''),
        markdown('''
### Your Change: Urgent Work and Newest Request

Add two outputs to the existing `$group` and expose them in `$project`:

```python
"urgent_count": {"$sum": {"$cond": [{"$eq": ["$priority", "urgent"]}, 1, 0]}},
"newest_opening": {"$max": "$opened_at"}
```

`$cond` chooses 1 or 0 per input ticket. `$max` keeps the largest date. Explain why
the resolved urgent ticket must not contribute to this **active** summary. Run
the modified pipeline and check streetlight by looking back at its ticket IDs.
Keep the active-count result when you add the two new fields.
'''),
        code('''
# Edit these stages with the two expressions above, then rerun this cell.
my_pipeline = [
    {"$match": active_filter},
    {"$group": {"_id": "$category", "active_count": {"$sum": 1}}},
    {"$project": {"_id": 0, "category": "$_id", "active_count": 1}},
    {"$sort": {"category": 1}},
]
my_result = list(tickets.aggregate(my_pipeline))
pprint(my_result)

# An independent count checks the original report, not the new fields yet.
streetlight_count = tickets.count_documents({**active_filter, "category": "streetlight"})
print("Independent active streetlight count:", streetlight_count)
assert streetlight_count == 2
'''),
        markdown('''
## 3. Discover a Counting Trap

Suppose we insert `$unwind: "$events"` before grouping. It produces one document
per array element. A ticket with two events now contributes twice; a ticket with
an empty array disappears unless we request preservation.

Predict the ticket IDs in the output. The total number of documents can
accidentally match the ticket count even when the report is wrong.
'''),
        code('''
event_rows = list(tickets.aggregate([
    {"$match": active_filter},
    {"$unwind": "$events"},
    {"$project": {"_id": 0, "ticket_id": 1, "event_type": "$events.type"}},
    {"$sort": {"ticket_id": 1, "event_type": 1}},
]))
pprint(event_rows)
print("Active ticket IDs:", [row["ticket_id"] for row in tickets.find(active_filter)])
print("Unwound row IDs:", [row["ticket_id"] for row in event_rows])
'''),
        markdown('''
For a ticket count, group the tickets without unwinding. For an **event** count,
unwinding is appropriate, but label the report as events. Preserving empty arrays
does not undo duplication for tickets with multiple events. SQL joins can cause
the same change of grain; remember the ticket-to-event relationship from Week 2.

## 4. Require Valid Statuses Without Requiring Every Field

A validator applies to writes. It does not summarize data or make a query faster.
This schema requires a numeric ticket ID, an allowed status, and a subject.
Other fields may exist without being required. That is controlled flexibility.

The validator below is a MongoDB command document. It is not Python's type system
and is not identical to standard JSON Schema. BSON adds types such as `date`.
'''),
        code('''
validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["ticket_id", "status", "subject"],
        "properties": {
            "ticket_id": {"bsonType": ["int", "long"]},
            "status": {"enum": ["new", "open", "in_progress", "resolved", "closed"]},
            "subject": {"bsonType": "string"},
        },
    }
}

if USE_ATLAS:
    database.command({"collMod": "tickets", "validator": validator,
                      "validationLevel": "strict", "validationAction": "error"})
    print("MongoDB now checks new inserts and updates.")
else:
    print("Validator defined but NOT installed: mongomock has no server validation.")
'''),
        markdown('''
### Your Change: Opening Date

Require `opened_at`, and give it `{"bsonType": "date"}` in `properties`. Edit the
validator cell and rerun it. All four baseline tickets already have BSON dates.

The next test cell includes an allowed date, a date written as text, and a
missing date. A string that looks like a date is not a BSON date. The text and
missing cases should be rejected only after you add and reinstall your date rule.

Installing validation does not retroactively delete or repair existing invalid
documents. Inspect existing records before tightening a live collection. This
fresh practice fixture avoids an accidental migration of somebody else's data.
'''),
        code('''
valid_test = {"ticket_id": 1099, "status": "new", "subject": "Validation test",
              "opened_at": datetime(2026, 2, 5, tzinfo=timezone.utc)}
invalid_tests = [
    ("Invalid status", {**valid_test, "ticket_id": 1100, "status": "almost_done"}),
]
date_rule_added = (
    "opened_at" in validator["$jsonSchema"]["required"]
    and validator["$jsonSchema"]["properties"].get("opened_at") == {"bsonType": "date"}
)
if date_rule_added:
    invalid_tests += [
        ("Date stored as text", {**valid_test, "ticket_id": 1101,
                                "opened_at": "2026-02-05T00:00:00Z"}),
        ("Missing date", {"ticket_id": 1102, "status": "new", "subject": "No date"}),
    ]
else:
    print("Date rule not enabled yet. Edit and rerun the validator cell, then this test.")

if USE_ATLAS:
    try:
        # These IDs belong only to this test, so repeating it starts cleanly.
        tickets.delete_many({"ticket_id": {"$in": [1099, 1100, 1101, 1102]}})
        tickets.insert_one(valid_test)
        print("Valid insert accepted:", tickets.count_documents({"ticket_id": 1099}))
        for label, document in invalid_tests:
            try:
                tickets.insert_one(document)
            except OperationFailure as error:
                if error.code != 121:
                    raise
                print(label + " rejected. MongoDB error code:", error.code)
            else:
                raise AssertionError(label + " was accepted. Inspect the installed validator.")
    finally:
        tickets.delete_many({"ticket_id": {"$in": [1099, 1100, 1101, 1102]}})
else:
    print("Trace to interpret, NOT a result from this runtime:")
    print("Valid insert accepted: 1")
    for label, document in invalid_tests:
        print(label + " rejected. MongoDB error code: 121")
'''),
        markdown('''
## Explain Your Result

In this one cell, write a short response:

- Give your streetlight summary, including urgent count and newest opening.
  Identify the source tickets that support it.
- Explain why the unwound rows are unsuitable for counting requests, even though
  their total equals the number of active tickets in this fixture.
- Describe your opening-date rule. Name whether you executed MongoDB validation
  or interpreted the supplied trace. Explain both the text-date and missing-date
  outcomes, and one rule the validator still does not
  enforce (for example, whether an assignee ID exists in another collection).

Optional extension: add a set of non-null assignee IDs or count events by type.
These are extensions, not more required deliverables.

'''),
        markdown('''
## Your Explanation

Replace this paragraph with your response. Keep it in this notebook; no separate
report is needed.
'''),
        markdown('''
## Cleanup

The next cell deletes only `tickets` in the uniquely named practice database.
Run it when finished and remove the temporary Atlas IP entry in the dashboard.
A closed Python connection does not stop or delete an Atlas cluster. Do not delete
a shared cluster or another project's data. Do not put project data in this
practice collection.
'''),
        code('''
database.drop_collection("tickets")
client.close()
print("Removed this run's practice collection and closed its client.")
'''),
        markdown('''
## Further Reading

- [MongoDB aggregation pipeline](https://www.mongodb.com/docs/manual/core/aggregation-pipeline/)
- [Unwind behavior](https://www.mongodb.com/docs/manual/reference/operator/aggregation/unwind/)
- [Schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/)
- [Atlas IP access list](https://www.mongodb.com/docs/atlas/security/ip-access-list/)

Course prose: CC BY-NC-SA 4.0. Code: MIT. Synthetic fixture: CC0.
'''),
    ]
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    nbf.write(notebook, NOTEBOOK_DIR / "07_aggregation_validation.ipynb")


def main() -> None:
    build_relational_sql_review()
    build_transactions_locks()
    build_postgres_backup_restore()
    build_atlas_mql_modeling()
    build_mongodb_logical_recovery()
    build_public_data_capacity_integration()
    build_aggregation_validation()


if __name__ == "__main__":
    main()
