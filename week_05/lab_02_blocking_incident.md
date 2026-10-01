# Lab 2: The Query Finished, but Which Change Survived?

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_05/lab_02_blocking_incident.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_05/materials/notebooks/02_postgres_transactions_locks.ipynb)

A developer's status update waits while another session changes the same ticket.
Releasing that session lets the update finish. Does it matter whether we commit
or roll back the blocking transaction?

Work individually in class. Use only your personal course database. Submit one
completed notebook in Brightspace, with its short explanation in the notebook.

## Before the Experiment: Connect Colab to Supabase

**Lab 2 is the assignment. The notebook runs in Colab and connects to your
Supabase PostgreSQL database.** Your earlier use of Supabase's SQL editor does
not automatically connect Colab. Use your existing personal course project.

Follow **First-Time Setup: Colab and Supabase** near the top of the notebook.
It walks through saving a Colab copy, finding **Connect > Session pooler**,
replacing the password placeholder, adding `sslmode=require`, and entering the
URL at the hidden prompt. PowerPoint slides **20-22** show the same walkthrough.

Run code cells in order. Before continuing to the experiment, confirm:

- Section 1 prints **Opened Session A, Session B, and the diagnostic session.**
- Section 2 prints `Starting row: (1004, 'medium', 'open')`.

If a connection fails, stop before Section 2 and use the notebook's setup checks.
Today uses the disposable `lock_lab` table and does not require Day 1's event IDs.

## 1. Follow the Rollback Example

Click **Open in Colab** above and save a working copy in Drive. You can also
[download Notebook 02](materials/notebooks/02_postgres_transactions_locks.ipynb) for local Jupyter.
Use **Session pooler** in Supabase's Connect dialog, with the SSL setting described
in the notebook. Enter your URL only at the hidden credential prompt.

Set `USE_CLOUD = True` and leave `KEEP_A_CHANGE = False`. Run from top to bottom.
The notebook creates a disposable row, captures a real wait, rolls back A, and
lets B commit before the experiment cell ends. It also shows what an ordinary
reader could see while A's change was uncommitted.

**Where to look:** Section 4 runs the experiment. Section 5 displays the captured
blocker relationship. Section 6 prints the final row. Both runs should finish
successfully; this lab does not ask for a duplicate-key error.

In the final Markdown cell, keep the final priority and status. Identify B's
blocking PID from `pg_blocking_pids`, rather than guessing from which row of the
output appears first. Run the cleanup cell before the next experiment.

## 2. Change One Transaction Decision

Predict the final priority and status if A commits instead. Change only
`KEEP_A_CHANGE = True`, then rerun from the configuration cell through cleanup.
The setup recreates the same starting row; B's SQL is unchanged.

Complete the small comparison table in the notebook's final Markdown cell.
Explain why B can finish in both runs while the final priority differs.

If a connection is unavailable, interpret the notebook's supplied rollback trace
and predict the commit case. Label them **supplied trace** and **unexecuted
prediction**, respectively. Tell the instructor so a connection demonstration can
be arranged. This fallback practices interpretation, not live administration.

## 3. Explain the Result to the Developer

In that same Markdown cell, write a short update explaining which query waited,
what blocked it, how the transaction decision changed the stored data, and one
reason the classroom choice cannot be applied blindly to a real application.
Use one run's actual PIDs and blocking result, or label your supplied trace.

**Submit:** `02_postgres_transactions_locks.ipynb`, including the comparison and
short update. No screenshots, separate incident form, or additional report.
Confirm the connections are closed and `lock_lab` was removed. Remove any
accidentally saved credentials before submission.
