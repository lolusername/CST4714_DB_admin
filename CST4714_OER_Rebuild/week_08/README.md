# Week 8: Backup, Recovery, and the Midterm

## The Week's Question

Can we recreate a required database state somewhere safe and prove that the
restored result works?

## What You Will Be Able to Do

- distinguish high availability, backup, restore, and disaster recovery;
- connect RPO and RTO to operational requirements;
- create and inspect a logical PostgreSQL dump;
- restore into a separate target and verify structure, data, and behavior; and
- integrate reproducibility, transactions, access or performance, and recovery in
  the midterm operations case.

## Read and Use

- [Module 8: A backup matters only when recovery works](../textbook/module_08_recovery.md)
- [Canonical midterm operations case](../midterm_project.md)
- [PostgreSQL backup and restore notebook](../notebooks/03_postgres_backup_restore.ipynb)
- [Open the notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/03_postgres_backup_restore.ipynb)
- [Week 8 student deck](week_08_backup_restore_midterm.pptx)
- [Week 8 PDF handout](week_08_backup_restore_midterm.pdf)
- [Week 8 transcript](week_08_backup_restore_midterm_transcript.md)

## Day 1: Perform and Verify a Logical Restore

Complete [Lab: Backup, restore, and prove it](lab_01_backup_restore.md).

Submit only the completed `03_postgres_backup_restore.ipynb` notebook.

## Day 2: Midterm Operations Clinic

Use the [canonical midterm assignment](../midterm_project.md). The class reviews
the package run order, then students work individually on the Metro Support case.
Weekly instructions do not redefine the assignment.

Bring one concrete question and one artifact that already runs. Use the midterm
rubric to identify the highest-value next improvement.

## Optional Industry Extension: Restore Game-Day Go/No-Go

This activity is optional, ungraded, and does not add a submission.

Act as the operator receiving a backup with these facts: the dump command exited
successfully, the artifact has no recorded checksum, the source server version is
known, the proposed restore target is the production database, and no
post-restore query has been defined. Write a go/no-go decision, list the unsafe or
missing evidence, and replace the target with a safer recovery rehearsal. Include
one warning about restoring an artifact from an untrusted source.

## End-of-Week Self-Check

Explain what a successful dump command proves, what it does not prove, and which
independent checks are required after restoration.
