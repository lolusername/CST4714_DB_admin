# Lab: Can We Recover a Working Database?

A backup file exists. Can it actually recreate the database's records and rules?
Restore it somewhere separate and test the result.

Work individually in class. Submit one completed notebook.

## 1. Perform the Restore

Download [PostgreSQL Backup and Restore](../../notebooks/03_postgres_backup_restore.ipynb),
open [Colab](https://colab.research.google.com/), and use **File > Upload notebook**.
Run it in order. It creates an isolated PostgreSQL service and uniquely named
practice databases inside the runtime. No Supabase password is needed.

The notebook supplies a small three-table recovery fixture, creates a custom-format
`pg_dump` archive, and restores to a **different** database. Inspect the source and
restored results. The expected invalid-status insert should fail: that is a test
that the restored database still enforces the rule.

In **Your Check: Compare One Known Ticket**, run the supplied example for ticket
1001, then adapt it to ticket 1002 or 1003. Compare the subject, status, and
requester with that ticket's original `INSERT`, as well as between source and
restore. Row counts alone would not catch a changed subject or a swapped
requester. You may extend the query to test another meaningful property instead.

## 2. Explain What the Checks Establish

Replace the notebook's recovery-record prompts with a short account of the
restore: where you restored, what the supplied checks showed, what your extra
check showed, and one thing still untested. Explain which connection would change
if the source were Supabase rather than the temporary local service.

Keep the actual output with your explanation, then run the final cleanup cell.
It removes the practice databases and artifact folder and stops the Colab service.
Do not write a
second report or reproduce the output as screenshots.

**Submit:** the completed notebook. The archive is a runtime practice artifact;
you do not need to upload it with the assignment.
