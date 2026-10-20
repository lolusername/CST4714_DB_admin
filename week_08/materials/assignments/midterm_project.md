# Midterm Project: Metro Support

CST4714 Database Administration · Individual project · 30% of the course grade

**This page is the whole midterm.** It explains what to do, what you should see, what to write, how to submit, and how it is graded.

## The midterm at a glance

- **What it is:** a project you complete on your own time. It is not an in-class exam.
- **What you do:** run a small PostgreSQL database we give you, add two short pieces of SQL, and record and explain what happened.
- **What you submit:** two files, **midterm.sql** and **README.md**, together in one ZIP in Brightspace.
- **When it is due:** **Tuesday, November 3, 2026**, two weeks after the October 20 clarification. Submit the ZIP in Brightspace. We introduce the project in Week 7 and teach the recovery part in Week 8.
- **Who does it:** you, individually. You do not need a web application, a new dataset, or a presentation.
- **Not the midterm:** the Week 7 Colab research notebook. That is classwork with its own Brightspace link.

| Part | You show that you can | Where it goes |
|---|---|---|
| 1 | Check the data and explain three integrity rules | midterm.sql and README.md |
| 2 | Roll back one change and commit another | midterm.sql and README.md |
| 3 | Explain one blocking incident from Week 5 | README.md |
| 4 | Test one improvement, normally an index | midterm.sql and README.md |
| 5 | Plan a recovery from a backup, after Week 8 | README.md |

## How your Week 7 lab carries forward

This is the same project introduced in Week 7. The five parts, starter database, rubric, and two-file submission stay the same. Keep the work you have already completed.

Reuse your own Week 7 research and writing in the matching README sections. Revise predictions after you run the PostgreSQL experiments: label what you observed, what you inferred, and what came from a supplied trace. The research notebook prepares you for the project; its analysis does not replace the SQL results required below. Its separate classwork submission remains a Colab sharing link.

For the recommended index route, the starter supplies the database, count query, rollback example, and index experiment. You add the requester join and commit example, run the experiments, and fill in the README. The five parts below are sections of that same submission. In Week 8, add the recovery plan. You do not need to redo the research lab or start a different project.

## Before you start

1. Save [midterm_starter.sql](midterm_starter.sql) as **midterm.sql** and [midterm_README_template.md](midterm_README_template.md) as **README.md**.
2. Work in your personal Supabase practice project, or a local or instructor-provided PostgreSQL database. Use a dedicated practice database.
3. SECTION 1 of the starter resets the **midterm_metro** schema. Running it deletes earlier work in that schema and any objects that depend on it. Save your SQL and notes before you rerun it.
4. Run SECTION 1 once. After that, select and run only the section you need. Never rerun SECTION 1 between the two halves of an experiment.
5. The Supabase SQL Editor may show only the last result of a run. To see every result of a transaction block, use psql or the [Colab helper](#see-every-result-colab-helper) at the end of this page.

The starter already contains the three tables, all the data, the rollback example, and the index experiment. You may use this supplied code. Your work is to complete the marked sections, record what actually happened, and explain the results in your own words.

## Part 1: Check the data

**Do**

1. Run SECTION 1. It builds the three tables and runs a count query.
2. Replace the TODO below the counts with a query that joins each ticket to its requester. A ticket's `requester_id` matches a `user_id` in users. Use the full names `midterm_metro.tickets` and `midterm_metro.users`, and fill in the join condition:

```sql
SELECT t.ticket_id, u.display_name AS requester
FROM midterm_metro.tickets AS t
JOIN midterm_metro.users AS u ON ______ = ______
ORDER BY t.ticket_id;
```

**You should see**

- Counts: **8 users, 12 tickets, 21 ticket events.**
- Join: **12 rows**, one per ticket, from 1001 with Requester 101 to 1012 with Requester 104.

**Write in README, section "Database checks"**

- Your actual counts and what your join returned.
- Three existing **non-key** integrity controls. For each, give the control, its column, and the bad data it prevents. The starter has NOT NULL, UNIQUE, and CHECK examples; primary keys and foreign keys do not count. You do not need to redesign the tables or add constraints.

Keep the setup and both verification queries in midterm.sql.

## Part 2: Roll back, then commit

Ticket **1004** starts with priority **low**.

**Do**

1. Run SECTION 2A as one block. This supplied example changes the priority to high inside a transaction, checks it, rolls back, and checks again.
2. Replace the 2B TODO with the same six statements, but change `'high'` to `'medium'` and `ROLLBACK` to `COMMIT`. Run it as one block.
3. Keep each transaction in one session: run each BEGIN through its final SELECT together.

**You should see** (running 2A, then 2B, after a fresh setup)

| Test | Before | Inside the transaction | After rollback or commit |
|---|---|---|---|
| Rollback | low | high | low |
| Commit | low | medium | medium |

**Write in README, section "Transactions"**

- The six values you actually observed, in the table the template provides.
- Why the final values differ.

Leave the committed **medium** in place. Simple updates are enough; adding ticket events is not required.

## Part 3: Explain one blocking incident

**Do**

Use your Week 5 results, or run the controlled example again in the [Week 5 blocking notebook](../notebooks/02_postgres_transactions_locks.ipynb). If you cannot connect, use the supplied trace near the end of that notebook. Nothing for this part goes in midterm.sql.

**Write in README, section "Blocking"**

- **Evidence source:** my live run, my saved Week 5 run, or **supplied trace analysis**. If you use the supplied trace, explain the trace; do not claim a live run. Both paths are graded on the same reasoning.
- **Diagnostic SQL:** the `pg_stat_activity` query that calls `pg_blocking_pids`.
- **Blocked and blocking session IDs:** the blocked session waits with `wait_event_type` Lock, and its `blocking_pids` value lists the session it is waiting for.
- **The row involved, the action that released the block, and the final row values.**

The notebook uses a table called **lock_lab**. Its ticket 1004 starts at medium and open, not low and new, so read its values carefully. Include the notebook only if you changed its code. Screenshots are optional and earn no extra credit.

## Part 4: Test one improvement

The recommended route is the index experiment already in the starter. Its query lists the newest open tickets.

**Do**

1. **SECTION 4A:** run the SELECT alone and save the ordered ticket IDs. Then run the `EXPLAIN (ANALYZE, BUFFERS)` statement alone and save its plan.
2. **SECTION 4B:** create the index on (status, opened_at DESC, ticket_id DESC) once. The last key breaks timestamp ties. If PostgreSQL says the index already exists, run the starter's DROP INDEX line and repeat 4A to 4C.
3. **SECTION 4C:** run the identical SELECT and EXPLAIN again, then the size query.

**Example results** (a PostgreSQL 16 run; your scan choice, timings, costs, and index size can differ)

| Evidence | Before the index | After the index |
|---|---|---|
| Ordered IDs | 1011, 1007, 1001 | 1011, 1007, 1001 |
| Scan in the plan | Seq Scan on tickets | Seq Scan on tickets |
| index_bytes | not applicable | 16384, which is 16 kB |

With only 12 tickets, PostgreSQL may keep a sequential scan and timings may barely change. **That is a correct result.** An honest explanation can earn full credit; a faster time or an Index Scan is not required. Do not add fake rows or change planner settings to force a result. Cost numbers can drop after CREATE INDEX even when the plan stays the same, so compare the scan type.

**Write in README, section "One improvement"**

- The ordered IDs, the relevant plan lines, and the index size.
- The problem the index is meant to address.
- Whether your plan changed, and whether the result stayed the same.
- One cost of keeping the index. The starter also asks for a short recommendation: keep or drop it.

Your recommendation may be **keep** or **drop** if you support it with your results. For this practice submission, leave the index in the database and in midterm.sql so your recovery plan can check that it returns. Keeping it for that check does not change your recommendation about whether this tiny workload needs it.

**Other routes:** instead of the index, you may choose one alternative covered in class: a least-privilege grant, an RLS policy test, or a safe schema change. Show the relevant before and after checks and explain a tradeoff. Complete **one** improvement only. If you already chose an alternative in Week 7, keep that choice. Replace the index-specific prompts in the README with checks for your chosen change; you do not also owe an index experiment. The 100,000-row classroom demonstration is optional practice, not a second midterm database.

## Part 5: Write a recovery plan, after Week 8

Wait for the Week 8 [backup and restore lesson](../../lab_01_backup_restore.md). Then add a short recovery section to your README, about one page at most. **Running the restore is optional.** A logical export is enough; do not depend on a paid backup feature.

**Write in README, section "Recovery plan"**

1. **Status:** proposed plan, unless you actually ran the restore.
2. **Source:** your database and the schema **midterm_metro**.
3. **Backup:** the logical backup command or interface steps, and the backup file's name. The Week 8 command, adapted to this project:

   ```bash
   pg_dump --format=custom --schema=midterm_metro --no-privileges \
     --host="$PGHOST" --port="$PGPORT" --username="$PGUSER" \
     --dbname="$PGDATABASE" --password --file=midterm_metro.dump
   ```

4. **Destination:** a separate, empty restore database, never the source, on the same or a newer PostgreSQL version.
5. **Restore:** the restore command or steps, for example:

   ```bash
   pg_restore --host="$RESTORE_PGHOST" --port="$RESTORE_PGPORT" \
     --username="$RESTORE_PGUSER" --dbname="$RESTORE_PGDATABASE" \
     --password --single-transaction --no-owner --no-privileges \
     --exit-on-error midterm_metro.dump
   ```

6. **At least three checks, each with its expected result,** such as:

   | Check | Expected result |
   |---|---|
   | Table counts | 8 users, 12 tickets, 21 ticket events |
   | Requester relationships | the join returns 12 rows |
   | Ticket 1004 | priority medium |
   | The added index | midterm_tickets_status_opened_idx exists |

   If you chose a different improvement, replace the index check with an appropriate check for that change. The three-check minimum stays the same.

7. **Limits:** what the backup leaves out, such as roles or grants.

Clearly separate a check you planned from a result you actually observed. Never write a real password or connection string.

## Submit

- [ ] midterm.sql has the setup, both verification queries, the rollback and commit work, and your improvement.
- [ ] Expected-error tests, if you wrote any, are commented out so the file runs from top to bottom.
- [ ] README.md explains run order and environment, your actual results, blocking, the improvement, and the recovery plan.
- [ ] Every prompt in the template is replaced.
- [ ] No passwords, connection strings, API keys, or service-role keys appear anywhere.
- [ ] Both files are in **one ZIP**, uploaded to Brightspace by **Tuesday, November 3, 2026**. Add the Week 5 notebook only if you changed its code.

## Grading: 100 points

| Area | Points | What I will check |
|---|---:|---|
| Reproducible schema and data integrity | 25 | Setup runs, counts and relationships are checked, and you explain three controls |
| Transactions and blocking diagnosis | 25 | Rollback and commit outcomes are verified; the blocking explanation matches the evidence |
| Workload based improvement | 20 | One change has a reason, relevant before/after checks, and a stated tradeoff |
| Recovery readiness | 15 | The plan uses a separate destination and at least three meaningful checks |
| Documentation and communication | 15 | Another person can follow the two files; results are clear and secrets are absent |

Use the code and notebooks we have already worked with. A small working project with clear explanations is enough.

## See every result: Colab helper

Use this when your editor shows only the last result of a transaction block. Open a blank [Colab notebook](https://colab.research.google.com/) and run this cell once. At the hidden prompt, paste your Supabase **Connect > Session pooler** URI with your database password in place of the placeholder. Encode special characters in the password, for example `@` as `%40`. The prompt hides the URI, so it is never saved in the notebook.

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

Then put one complete block, such as all of 2A, in a new cell: `run_sql("""paste the block here""")`. It prints each result in order. Run `connection.close()` when you finish. The helper is not part of your submission.

## Reuse

See the [licenses](../LICENSE.md) and [source attributions](../ATTRIBUTIONS.md). External resources retain their own terms.
