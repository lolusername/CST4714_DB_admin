# Lab 2: Midterm Work Session

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_08/lab_02_midterm_work_session.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_08/materials/notebooks/midterm_work_session.ipynb)

Run the midterm starter step by step, see every result, and leave class with
most of your midterm results recorded.

Work individually in class. Submit one completed notebook.

**This lab is classwork. It is not the midterm.** The midterm is still
`midterm.sql` and `README.md` in one ZIP in Brightspace, due **Tuesday,
November 3, 2026**. The [midterm page](materials/assignments/midterm_project.md)
has every requirement. This lab adds none.

## Before You Start

Have three things open:

1. This notebook: click **Open in Colab** above, then **File > Save a copy in
   Drive**.
2. Your `midterm.sql`, saved from the
   [starter](materials/assignments/midterm_starter.sql).
3. Your `README.md`, saved from the
   [template](materials/assignments/midterm_README_template.md).

No Supabase password is needed. The notebook runs PostgreSQL inside Colab. If
you have not set up a Supabase project, this notebook's PostgreSQL counts as a
local practice database for the midterm.

## What You Do (about 80 minutes)

Run the cells in order. Each step says what you should see.

| Step | Midterm part | What you do | You should see | Minutes |
|---|---|---|---|---:|
| 0 | Setup | Start PostgreSQL and load SECTION 1 of the starter | 8 users, 12 tickets, 21 ticket events | 5 |
| 1 | Part 1 | Fill in the requester join. Then test a NOT NULL rule and a CHECK rule with a write that should fail (a UNIQUE example is supplied) | 12 join rows; SQLSTATE 23502 and 23514 | 20 |
| 2 | Part 2 | Run the supplied rollback, then write the commit version | low, high, low; then low, medium, medium | 15 |
| 3 | Part 4 | Run the index experiment before and after | IDs 1011, 1007, 1001 both times; index about 16 kB | 15 |
| 4 | Part 5 | Write three checks first, then back up, restore into a separate database, and compare | every check says MATCH | 20 |
| 5 | | Write where you are and your next step, then run cleanup | | 5 |

Part 3 (blocking) is not in this lab. Use the
[Week 5 notebook](materials/notebooks/02_postgres_transactions_locks.ipynb) or
its supplied trace.

As you go, copy your SQL into `midterm.sql` and your observed results into the
matching `README.md` section. Each notebook step names the section.

## Be Honest About What You Ran

The Step 4 restore copies the **Colab practice database**. If your midterm
database is this notebook, you may report the restore as **observed**. If your
midterm database is in Supabase, the restore was a rehearsal, and your README
recovery plan for Supabase stays a **proposed plan**.

## Submit

Keep the output, run the final cleanup cell, then download the notebook
(**File > Download > Download .ipynb**). Submit the completed notebook in
Brightspace. The backup file is not a submission.
