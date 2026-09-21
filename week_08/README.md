# Week 8: Backup, Recovery, and the Midterm

## The Week's Question

Can we recreate a required database state somewhere safe and check that the
restored result works?

## What You Will Be Able to Do

- distinguish high availability, backup, restore, and disaster recovery;
- connect RPO and RTO to operational requirements;
- create and inspect a logical PostgreSQL dump;
- restore into a separate target and verify structure, data, and behavior; and
- integrate reproducibility, transactions, access or performance, and recovery in
  the midterm operations case.

## Before Class: Assigned Reading

Use [Chapter 8: A Backup Matters Only When Recovery Works](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read the recovery concepts through **Free-Tier Reality in This Course** and **Verify Structure, Data, and Behavior**. Use the command explanations as a reference while running the restore notebook.
- **Before Day 2:** read **Worked Example: A Recovery Runbook Entry** and **Safe Migrations and Recovery Are Connected**. Revisit the earlier chapters relevant to your midterm case.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Canonical midterm operations case](materials/assignments/midterm_project.md)
- [PostgreSQL backup and restore notebook](materials/notebooks/03_postgres_backup_restore.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_08/materials/notebooks/03_postgres_backup_restore.ipynb) for Lab 1; save a working copy in Drive.
- [Transactions and locks notebook](materials/notebooks/02_postgres_transactions_locks.ipynb), a midterm reference: [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_08/materials/notebooks/02_postgres_transactions_locks.ipynb)
- [Week 8 student deck](week_08_backup_restore_midterm.pptx)
- [Week 8 PDF handout](week_08_backup_restore_midterm.pdf)
- [Week 8 transcript](week_08_backup_restore_midterm_transcript.md)

## Day 1: Perform and Verify a Logical Restore

Complete [Lab: Backup, restore, and check the result](lab_01_backup_restore.md).

Submit only the completed `03_postgres_backup_restore.ipynb` notebook.

## Day 2: Midterm Operations Clinic

Use the [canonical midterm assignment](materials/assignments/midterm_project.md). The class reviews
the package run order, then students work individually on the Metro Support case.
Weekly instructions do not redefine the assignment.

Bring one concrete question and one working part of the project. Use the midterm
rubric to identify the highest-value next improvement.

## Optional Industry Extension: Restore Game-Day Go/No-Go

This activity is optional, ungraded, and does not add a submission.

Act as the operator receiving a backup with these facts: the dump command exited
successfully, the artifact has no recorded checksum, the source server version is
known, the proposed restore target is the production database, and no
post-restore query has been defined. Write a go/no-go decision, list the unsafe or
missing checks, and replace the target with a safer recovery rehearsal. Include
one warning about restoring an artifact from an untrusted source.

## End-of-Week Self-Check

Explain what a successful dump command proves, what it does not prove, and which
independent checks are required after restoration.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
