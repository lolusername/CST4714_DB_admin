# Midterm Guide Step by Step

CST4714 Database Administration · Companion to the [Metro Support midterm](midterm_project.md)

This guide walks through the midterm one part at a time. For each part it shows what to run, what you should see, and where the result goes in your README. It does not add or change any requirement. If this guide and the assignment ever seem to disagree, follow the assignment and ask me.

## The project in one paragraph

You run a small PostgreSQL database, prove what happened with real query results, and explain those results in your own words. The starter already builds the database, supplies the rollback example, and supplies the whole index experiment. On the recommended route, you write two small pieces of SQL: a requester join and a commit example. Everything else is recording and explaining results in README.md. You submit **midterm.sql** and **README.md** together in one ZIP by the deadline in Brightspace.

| Part | Already supplied | What you add | Where it goes |
|---|---|---|---|
| Setup | Three tables, seed data, count query | Run SECTION 1 once | Counts go in README Database checks |
| 1 Data and integrity | Constraints you can explain | The requester join; three controls explained | midterm.sql and README Database checks |
| 2 Transactions | The rollback example, 2A | Your commit example, 2B; six observed values | midterm.sql and README Transactions |
| 3 Blocking | The Week 5 notebook and its supplied trace | A written explanation | README Blocking |
| 4 One improvement | The whole index experiment, 4A to 4C | Recorded IDs, plan lines, size, and explanation | README One improvement |
| 5 Recovery | The Week 8 lesson and commands | A short recovery plan | README Recovery plan |

## Before you start

1. Save [midterm_starter.sql](midterm_starter.sql) as **midterm.sql** and [midterm_README_template.md](midterm_README_template.md) as **README.md**.
2. Work in your personal Supabase practice project, or in a local or instructor-provided PostgreSQL database. Never use a database that holds work you need to keep.
3. Know what the reset does. SECTION 1 runs `DROP SCHEMA IF EXISTS midterm_metro CASCADE`. It deletes everything in the midterm_metro schema, plus any object elsewhere that depends on it, then rebuilds the schema.
4. Run SECTION 1 once. After that, highlight one section and run only that section.
5. Do not rerun SECTION 1 partway through. It sets ticket 1004 back to low and removes your index. If you need a clean start, rerun SECTION 1, then repeat Parts 2 and 4 in order.

### Seeing every result

A web SQL editor, including the Supabase SQL Editor, may show only the result of the last statement in a run. That is fine for a single SELECT. It is a problem for the transaction blocks in Part 2, where you need the value inside the transaction.

To see every result in order, use a `psql` session connected to your practice database, or this short Colab helper. Open a blank [Colab notebook](https://colab.research.google.com/) and run this cell once. At the hidden prompt, paste your Supabase **Connect > Session pooler** URI with your database password in place of the placeholder. Encode special characters in the password as the Week 5 blocking notebook explains, for example `@` as `%40`. The prompt hides the URI, so it is not saved in the notebook; never paste it into a code or text cell.

```python
%pip -q install "psycopg[binary]>=3.2,<4"
from getpass import getpass
import psycopg

connection = psycopg.connect(
    getpass("Session-pooler URI (hidden): "),
    sslmode="require", connect_timeout=10, autocommit=True,
)

def run_sql(sql_text):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_text, prepare=False)
            while True:
                if cursor.description:
                    print([column.name for column in cursor.description])
                    print(cursor.fetchall())  # [] means a result with zero rows.
                else:
                    print(cursor.statusmessage)
                if not cursor.nextset():
                    break
    except psycopg.Error as error:
        connection.execute("ROLLBACK")
        print("SQLSTATE", error.sqlstate, error.diag.message_primary)
```

Then put one complete block, such as all of 2A, in a new cell between triple quotes: `run_sql("""paste the block here""")`. The helper prints each result in order, so for 2A you see low, then high, then low. Run `connection.close()` when you finish. The helper only displays results; it is not part of your submission.

Keep each transaction together in one run. Do not split BEGIN from its COMMIT or ROLLBACK to reveal a middle result, because separate editor runs may use different connections.

For the README's environment line, `SELECT version();` prints your PostgreSQL version. Describe your environment in words. Never paste a password or connection string.

## Part 1 Load and check the data

**Step 1. Run SECTION 1.** Its last result is the count query. You should see:

| table_name | row_count |
|---|---:|
| users | 8 |
| tickets | 12 |
| ticket_events | 21 |

If your counts differ, rerun SECTION 1 before going further.

**Step 2. Write the requester join.** Replace the TODO comment that asks for it with your query. Each ticket's `requester_id` matches a `user_id` in users. Use this shape and fill in the join condition:

```sql
SELECT t.ticket_id, u.display_name AS requester
FROM midterm_metro.tickets AS t
JOIN midterm_metro.users AS u ON ________ = ________
ORDER BY t.ticket_id;
```

A correct join returns **12 rows**, one per ticket. The first row is 1001 with Requester 101. The last row is 1012 with Requester 104. Any count other than 12 means the join condition needs another look.

**Step 3. Record and explain.** In README **Database checks**, record your counts and what your join returned. Then name three non-key integrity controls that already exist in the starter, give the column each one protects, and explain what bad data each one prevents. Primary keys and foreign keys (`REFERENCES`) are keys, so choose from these:

| Control | Where it is in the starter |
|---|---|
| NOT NULL | Many columns, for example `tickets.subject` |
| UNIQUE | `users.email` |
| CHECK | tickets: `closed_at IS NULL OR closed_at >= opened_at` |

A complete explanation names the control, the column, and the bad data it stops. For example: *NOT NULL on tickets.subject rejects a ticket whose subject is missing, meaning NULL. Without it, a ticket could enter the queue with no recorded problem.* Write your three in your own words.

Optional: you can show a control working with an expected-error test, such as inserting a second user with an existing email. Keep that test commented out in midterm.sql so the file still runs from top to bottom.

## Part 2 Roll back, then commit

Ticket 1004 starts with priority **low**.

**Step 1. Run 2A as one block.** It reads the value, starts a transaction, changes the priority to high, reads it again, rolls back, and reads it a third time.

**Step 2. Write 2B.** Replace the 2B TODO with the same six statements, changing `'high'` to `'medium'` and `ROLLBACK` to `COMMIT`. Run it as one block.

**Step 3. Fill in the Transactions table.** If you run 2A and then 2B after a fresh setup, you should observe:

| Test | Before | Inside the transaction | After rollback or commit |
|---|---|---|---|
| Rollback | low | high | low |
| Commit | low | medium | medium |

Then explain the difference in a few sentences: what your own session saw inside each transaction, what ROLLBACK did, and what COMMIT did. Record the values you actually observed. If you ran the blocks in a different order, record your values and explain them.

Leave the committed **medium** in place. Your recovery checks rely on it.

## Part 3 Explain one blocking incident

Part 3 adds nothing to midterm.sql. Everything goes in README **Blocking**.

**Step 1. Choose and label your evidence source** on the template's Evidence source line:

- **my live run** if you run the [Week 5 notebook](../notebooks/02_postgres_transactions_locks.ipynb) again;
- **my saved Week 5 run** if you use the results you saved in Week 5;
- **supplied trace analysis** if you use the notebook's Offline Fallback Incident Transcript.

All three paths are graded with the same reasoning criteria. Do not describe the supplied trace as a live run.

**Step 2. Record six things:**

1. the diagnostic SQL, which is the `pg_stat_activity` query that calls `pg_blocking_pids(pid)`;
2. the blocked session's PID;
3. the blocking session's PID;
4. the row involved;
5. the action that released the block;
6. the final values of that row.

**How to read the diagnostic output.** The blocked session is waiting, so its `wait_event_type` is `Lock`. Its `blocking_pids` value lists the PID it is waiting for, and that PID belongs to the blocker. The notebook's own example: when `pg_blocking_pids(7332)` returns `{7310}`, session 7332 is waiting for session 7310.

**Step 3. Explain the final row.** Say which change survived, which did not, and why. The Week 5 notebook uses `lock_lab`, whose ticket 1004 starts at **medium** and **open**. Those values differ from the midterm database, so take them from the notebook.

Include the notebook in your ZIP only if you changed its code. Screenshots are optional and earn no extra credit.

## Part 4 Test one improvement

The recommended route is the index experiment in the starter. Its query lists the newest open tickets.

**Step 1. Section 4A, before the index.** Highlight the SELECT alone and run it. Save the ordered ticket IDs. Then highlight the `EXPLAIN (ANALYZE, BUFFERS)` statement alone and run it. Save its output.

**Step 2. Section 4B.** Create the index once. If PostgreSQL says the index already exists, it was created earlier, possibly before your 4A baseline. Unless you are sure 4A ran first, run the starter's `DROP INDEX` line, then repeat 4A, 4B, and 4C.

**Step 3. Section 4C, after the index.** Run the same SELECT and the same EXPLAIN again, one at a time. Then run the size query.

On PostgreSQL 16, with fresh setup data, the starter produced:

| Evidence | Before the index | After the index |
|---|---|---|
| Ordered IDs | 1011, 1007, 1001 | 1011, 1007, 1001 |
| Scan line in the plan | Seq Scan on tickets | Seq Scan on tickets |
| index_bytes | not applicable | 16384, which is 16 kB |

Your timings and cost numbers will differ. Your IDs and scan type should match.

**Why the plan may not change.** All 12 tickets fit on one 8 kB table page. Reading that page directly is cheaper than reading the index and then the table, so PostgreSQL keeps a sequential scan. An honest explanation of an unchanged plan can earn full credit. A faster time or an Index Scan is not required. Do not add fake rows or change planner settings to force a result.

**Cost numbers can change when the plan does not.** Building an index also updates PostgreSQL's estimate of how many rows the table holds. The costs after 4B may therefore be lower even though the plan still says Seq Scan. Compare the scan type, such as Seq Scan, Index Scan, or Bitmap Heap Scan, rather than the cost.

**Step 4. Write README One improvement.** Include:

- the ordered IDs before and after;
- the relevant plan lines, at least the scan line from each plan;
- the measured index size;
- the problem the index is meant to address;
- whether your plan changed;
- whether the result stayed the same;
- one cost of keeping the index, such as its storage or the extra work on each insert and on updates that change an indexed column;
- the short recommendation the starter's TODO mentions: keep or drop the index, and why.

Keep the index for your recovery plan and final checks.

**Alternative routes.** Instead of the index, you may complete one alternative already covered in class: a least-privilege grant, an RLS policy test, or a safe schema change. Show the relevant before and after checks and explain one tradeoff. Complete one improvement only.

## Part 5 Write a recovery plan after Week 8

Write this after the [Week 8 backup and restore lab](../../lab_01_backup_restore.md). It is one README section, about a page at most. Executing the restore is optional.

Set the Status line to **proposed plan** unless you actually ran the restore. Then cover:

1. **Source:** the database you used and the schema **midterm_metro**.
2. **Backup:** a logical export of that schema. The Week 8 command, adapted to this project:

   ```bash
   pg_dump --format=custom --schema=midterm_metro --no-privileges \
     --host="$PGHOST" --port="$PGPORT" --username="$PGUSER" \
     --dbname="$PGDATABASE" --password --file=midterm_metro.dump
   ```

3. **Artifact:** the file the backup creates, such as midterm_metro.dump.
4. **Destination:** a separate, empty database, never the source, on a PostgreSQL server of the same or a newer major version. A new database on a local server or a second Supabase practice project are examples. A new schema in the same database is not a separate destination, because the archive recreates midterm_metro by name.
5. **Restore:** for example, with Chapter 8's restore command:

   ```bash
   pg_restore --host="$RESTORE_PGHOST" --port="$RESTORE_PGPORT" \
     --username="$RESTORE_PGUSER" --dbname="$RESTORE_PGDATABASE" \
     --password --single-transaction --no-owner --no-privileges \
     --exit-on-error midterm_metro.dump
   ```

6. **At least three checks, each with an expected result.** Useful checks for this project:

   | Check | Expected result |
   |---|---|
   | Row counts | 8 users, 12 tickets, 21 ticket_events |
   | Requester relationships | The requester join returns 12 rows |
   | Committed value | Ticket 1004 has priority medium |
   | Index | midterm_tickets_status_opened_idx exists on midterm_metro.tickets |

7. **Limits:** what this backup leaves out. Examples include roles and passwords, grants skipped by `--no-privileges`, original ownership skipped by `--no-owner`, other schemas, Supabase Auth, Storage, and project settings, and any change made after the dump.

Keep placeholders such as `$PGHOST` in the README. Never write a real password or connection string there. If you run the commands, use client tools that match your server's major version, as in Week 8.

## Finish and submit

- Replace every bracketed prompt in the README template.
- **Run order:** explain how someone else would run midterm.sql from the top, the order of the sections, and what the SECTION 1 reset deletes.
- **References and assistance:** name the starter, notebooks, documentation, and any assistance you used. Explain your own changes and observations.
- Label observations and predictions. An observation is a value from your own output. A prediction or proposal is something you did not run.
- Keep expected-error tests commented out in midterm.sql.
- Put **midterm.sql** and **README.md** in one ZIP and submit it in Brightspace by the posted deadline. Include the Week 5 notebook only if you changed its code.

## Expected results at a glance

| Check | Expected result |
|---|---|
| Counts after setup | 8 users, 12 tickets, 21 ticket_events |
| Requester join | 12 rows, from 1001 with Requester 101 to 1012 with Requester 104 |
| Rollback test | low, then high, then low |
| Commit test | low, then medium, then medium |
| Newest open tickets, before and after the index | 1011, 1007, 1001 |
| Plan on 12 rows | Seq Scan on tickets before and after; costs may change |
| Index size | 16384 bytes, which is 16 kB, on PostgreSQL 16 |
| State to keep for recovery checks | Ticket 1004 at medium, index present |

These values help you check your work. Your README reports what your own run showed.

## Reuse

See the [licenses](../LICENSE.md) and [source attributions](../ATTRIBUTIONS.md). External resources retain their own terms.
