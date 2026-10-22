# Lab 2: Midterm Work Session in Supabase

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_08/lab_02_midterm_work_session.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_08/materials/notebooks/midterm_work_session.ipynb)

Connect Colab to your own Supabase project through the session pooler, run the
midterm starter step by step, see every result, and back up and restore your
midterm schema for real.

Work individually in class. Submit one completed notebook.

**This lab is classwork. It is not the midterm.** The midterm is still
`midterm.sql` and `README.md` in one ZIP in Brightspace, due **Tuesday,
November 3, 2026**. The [midterm page](materials/assignments/midterm_project.md)
has every requirement. This lab adds none.

## Before You Start

Have these ready:

1. **Your Supabase project and its database password.** No project yet? Create
   a free one at supabase.com and save the database password it asks for. Forgot
   the password? Reset it under **Project Settings > Database**.
2. **The session pooler connection string.** In your project, click **Connect**,
   choose **Session pooler**, and copy the URI. You will paste it, with your
   password, at the notebook's hidden prompt. Never paste it anywhere else.
3. **This notebook:** click **Open in Colab** above, then **File > Save a copy in
   Drive**.
4. **Your `midterm.sql` and `README.md`**, saved from the
   [starter](materials/assignments/midterm_starter.sql) and the
   [template](materials/assignments/midterm_README_template.md).

**Not using Supabase for the midterm?** If you chose another hosted PostgreSQL
service, paste its connection URI instead; the notebook warns and continues.
Colab cannot reach a database on your own computer, so if your midterm runs
locally, do this lab in a free Supabase project. Your midterm can stay local.

## Why the Session Pooler

| Connection | Host and port | Network | Today? |
|---|---|---|---|
| Direct | `db.[ref].supabase.co:5432` | IPv6 on the Free plan | No: Colab reaches only IPv4 |
| **Session pooler** | `aws-[n]-[region].pooler.supabase.com:5432` | IPv4 | **Yes** |
| Transaction pooler | same host, port `6543` | IPv4 | No: it hands the connection back after every transaction |

The session pooler gives you one database connection for your whole session,
so transactions and `pg_dump` behave as they would on a direct connection.

## What You Do (about 80 minutes)

Run the cells in order. Each step says what you should see.

| Step | Midterm part | What you do | You should see | Minutes |
|---|---|---|---|---:|
| 0 | Setup | Connect through the session pooler, install matching tools, load SECTION 1 of the starter | 8 users, 12 tickets, 21 ticket events | 10 |
| 1 | Part 1 | Fill in the requester join. Then test a NOT NULL rule and a CHECK rule with a write that should fail (a UNIQUE example is supplied) | 12 join rows; SQLSTATE 23502 and 23514 | 20 |
| 2 | Part 2 | Run the supplied rollback, then write the commit version | low, high, low; then low, medium, medium | 15 |
| 3 | Part 4 | Run the index experiment before and after | IDs 1011, 1007, 1001 both times; index about 16 kB | 15 |
| 4 | Part 5 | Write three checks first, then back up Supabase, restore the copy into a separate database in Colab, and compare | every check says MATCH | 15 |
| 5 | | Write where you are and your next step, then run cleanup | | 5 |

Part 3 (blocking) is not in this lab. Use the
[Week 5 notebook](materials/notebooks/02_postgres_transactions_locks.ipynb) or
its supplied trace.

As you go, copy your SQL into `midterm.sql` and your observed results into the
matching `README.md` section. Each notebook step names the section.

## If the Connection Fails

| If you see | It means |
|---|---|
| `Network is unreachable` or `could not translate host name` | You copied the direct connection, or the host has a typo. Copy the session pooler URI. |
| `password authentication failed` | Wrong password, or a special character is not encoded (`@` is `%40`, `#` is `%23`, `/` is `%2F`). |
| `Tenant or user not found` | The user must be `postgres.[ref]` and the host must match your region. Copy the URI again from **Connect**. |
| `timeout expired` | Your project may be paused. Restore it from the dashboard and wait a minute. |

## Be Honest About What You Ran

Step 4 backs up your Supabase project's `midterm_metro` and restores it into a
separate database in Colab. If your midterm database is this Supabase project,
that is an executed restore and you may report it as **observed**. If your
midterm runs somewhere else, it was a rehearsal, and your recovery plan for that
database stays a **proposed plan**.

## Submit

Keep the output, run the final cleanup cell, then download the notebook
(**File > Download > Download .ipynb**). Submit the completed notebook in
Brightspace. The backup file is not a submission. The cleanup leaves your
Supabase project as it is.
