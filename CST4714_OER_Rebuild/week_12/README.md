# Week 12: Reliability and Restore Evidence in Atlas

## The Week's Question

Which reliability promise does a replica set support, and which separate evidence
is needed to recover from a destructive change?

## What You Will Be Able to Do

- explain primary, secondary, oplog, election, and failover roles;
- distinguish write concern, read preference, and read concern;
- apply CAP only to behavior during a partition;
- explain why replication is not backup;
- perform a collection-level logical export and restore to a separate target; and
- describe when `mongodump` is required instead of a JSON interchange export.

## Course OER

- [Module 12: Reliability is a set of explicit promises](../textbook/module_12_reliability.md)
- [MongoDB logical recovery notebook](../notebooks/05_mongodb_logical_recovery.ipynb)
- [Open the notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/05_mongodb_logical_recovery.ipynb)
- [Week 12 student deck](week_12_mongodb_reliability.pptx)
- [Week 12 PDF handout](week_12_mongodb_reliability.pdf)
- [Week 12 transcript](week_12_mongodb_reliability_transcript.md)

## Free External References

- [Atlas Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
- [MongoDB Atlas Backup and Recovery course](https://learn.mongodb.com/learn/course/mongodb-atlas-backup-recovery/lesson-1-back-up-and-recover-an-atlas-free-tier/learn)

## Day 1: Build a Reliability Promise

Complete [Lab 1: Match user expectations to replica and recovery decisions](lab_01_reliability_decisions.md).

Submit only `week_12_reliability_decision.md`.

The final project is introduced through the
[canonical final-project page](../final_project.md). This week adds only the
one-paragraph workload checkpoint; it does not redefine final deliverables.

## Day 2: Export, Restore Elsewhere, and Verify

Complete [Lab 2: MongoDB logical recovery evidence](lab_02_mongodb_recovery.md).

Submit only the completed `05_mongodb_logical_recovery.ipynb` notebook.

## Optional Industry Extension: Ticket-Sale Partition Tabletop

This activity is optional, ungraded, and does not add a submission.

A ticket-sale service loses communication with a minority of replica-set members
during a high-demand release. Write one promise for purchase writes and one for
inventory reads. Choose a write concern, read preference, and read concern only
after stating whether stale availability or overselling is the greater risk.
Describe the expected client behavior during the partition, the role of
idempotency on retry, and why a later backup is still a separate requirement.

## End-of-Week Self-Check

Explain why a three-node Atlas Free replica set can help with node failure while
still requiring a manual recovery artifact for an accidental deletion.
