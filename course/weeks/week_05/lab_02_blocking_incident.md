# Lab 2: The Query Finished, but Which Change Survived?

A developer's status update waits while another session changes the same ticket.
Releasing that session lets the update finish. Does it matter whether we commit
or roll back the blocking transaction?

Work individually in class. Use only your personal course database. Submit one
completed notebook in Brightspace, with its short explanation in the notebook.

## 1. Follow the Rollback Example

Open [Notebook 02](../../notebooks/02_postgres_transactions_locks.ipynb) in
[Colab](https://colab.research.google.com/) using **File > Upload notebook**.
Use **Session pooler** in Supabase's Connect dialog, with the SSL setting described
in the notebook. Enter your URL only at the hidden credential prompt.

Set `USE_CLOUD = True` and leave `KEEP_A_CHANGE = False`. Run from top to bottom.
The notebook creates a disposable row, captures a real wait, rolls back A, and
lets B commit before the experiment cell ends. It also shows what an ordinary
reader could see while A's change was uncommitted.

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
