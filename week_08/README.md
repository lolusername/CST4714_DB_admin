# Week 8: Backup, Recovery, and the Midterm

## First in Class: The Midterm and What You Already Have

**Midterm due Tuesday, November 3, 2026.** Submit `midterm.sql` and `README.md` together in one ZIP in Brightspace.

We begin with the [midterm instructions](materials/assignments/midterm_project.md), SQL starter, and README template side by side. We will walk through the five parts, show where each result belongs, and answer questions before the recovery lesson. The project and rubric stay the same.

Keep your Week 7 lab work. Reuse your own research and explanations in the README, then revise them using your PostgreSQL results. The Week 7 research notebook remains separate classwork submitted through its Colab sharing link. An improvement you already selected remains valid. Complete one improvement only.

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

Read the [textbook corrections](../COURSE_CORRECTIONS.md) with the assigned sections.

Use [Chapter 8: A Backup Matters Only When Recovery Works](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read the recovery concepts through **Free-Tier Recovery** and **Verify Structure, Data, and Behavior**. Use the command explanations as a reference while running the restore notebook.
- **Before Day 2:** read **Worked Example: A Recovery Runbook Entry** and **Safe Migrations and Recovery Are Connected**. Revisit Chapter 3's **Keys Identify and Connect Facts** and **Constraints Reject Invalid States** for the midterm schema work. In class, identify the supplied schema's keys and three non-key integrity controls, then explain which invalid state each prevents. This refresh is part of midterm preparation, not another submission.

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

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 8 videos](videos/README.md).

- [RPO and RTO on the clock](videos/01_rpo_rto_clock.mp4) (1:29): A committed DELETE survives restarts and is copied to a replica, so recovery needs an earlier state. The chapter's 14:00 / 14:17 / 14:29 scenario shows a 17-minute data-loss window and a 12-minute recovery, missing both a 5-minute RPO and a 10-minute RTO.
- [Dump, restore, verify](videos/02_dump_restore_verify.mp4) (1:35): pg_dump captures one consistent snapshot, unlike CSVs downloaded at different moments. The archive is restored into a separate empty database, then checked with counts, a known ticket, and an expected constraint failure.
- [Point-in-time recovery with WAL](videos/03_wal_point_in_time.mp4) (1:20): A schematic of physical recovery: restore a base backup, then replay retained write-ahead log up to a target just before the harmful 14:17 DELETE. A single missing log segment stops the replay short of the target.

<!-- videos:end -->

## Day 1: Midterm Walkthrough, Then Backup and Restore

After the opening walkthrough and recovery lesson, complete the existing [Lab: Backup, restore, and check the result](lab_01_backup_restore.md).

Submit only the completed `03_postgres_backup_restore.ipynb` notebook.

Use the recovery lab to understand the steps for Part 5 of your midterm. The lab uses 3 users / 3 tickets / 5 events; the midterm uses 8 / 12 / 21. Write the midterm plan for `midterm_metro`, with its own expected results. Executing an additional restore for the midterm is optional.

## Day 2: Midterm Operations Clinic

Use the [canonical midterm assignment](materials/assignments/midterm_project.md). The class reviews
the package run order, then students work individually on the Metro Support case.
Weekly instructions do not redefine the assignment.

Bring your Week 7 writing, your current `midterm.sql` and `README.md`, and one concrete question. We will check how an observed result becomes an explanation in the README. Use the midterm
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
