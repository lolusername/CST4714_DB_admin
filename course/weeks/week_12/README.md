# Week 12: Reliability and Logical Recovery in Atlas

## The Week's Question

Which reliability promise does a replica set support, and which separate recovery
steps are needed after a destructive change?

## What You Will Be Able to Do

- explain primary, secondary, oplog, election, and failover roles;
- distinguish write concern, read preference, and read concern;
- apply CAP only to behavior during a partition;
- explain why replication is not backup;
- recover a document from a saved artifact when count and type checks miss a
  wrong value;
- perform a collection-level logical export and restore to a separate target; and
- describe when `mongodump` is required instead of a JSON interchange export.

## Before Class: Assigned Reading

Use [Chapter 12: Reliability Is a Set of Explicit Promises](../../textbook/module_12_reliability.md).

- **Before Day 1:** read the replica-set, acknowledgment, read-control, and CAP sections. Explain the A/B/C partition case without changing a real deployment.
- **Before Day 2:** read from **Replication Is Not Backup** through **Verify a MongoDB Restore**. Distinguish BSON-aware data recovery from restoring indexes, validators, and project configuration.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [MongoDB logical recovery notebook](../../notebooks/05_mongodb_logical_recovery.ipynb)
- [Open Colab](https://colab.research.google.com/), then **File > Upload notebook** using the downloaded file above.
- [Week 12 student deck](week_12_mongodb_reliability.pptx)
- [Week 12 PDF handout](week_12_mongodb_reliability.pdf)
- [Week 12 transcript](week_12_mongodb_reliability_transcript.md)

## Free External References

- [Atlas Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
- [MongoDB Atlas Backup and Recovery course](https://learn.mongodb.com/learn/course/mongodb-atlas-backup-recovery/lesson-1-back-up-and-recover-an-atlas-free-tier/learn)

## Day 1: Build a Reliability Promise

Complete [Lab 1: Match user expectations to replica and recovery decisions](lab_01_reliability_decisions.md).

Submit one Brightspace text response: a confirmation/read policy and the supplied
recovery-timeline analysis. No live failover or cluster reconfiguration is needed.

The final project is introduced through the
[canonical final-project page](../../assignments/final_project.md). Use project work
to choose a scenario and its important reads/writes in your existing project
notes, rather than making another Week 12 submission.

## Day 2: Export, Restore Elsewhere, and Verify

Complete [Lab 2: MongoDB logical recovery](lab_02_mongodb_recovery.md).

The notebook begins with five fresh tickets. Inspect how Extended JSON stores
their BSON types, restore the data into a separate target, and diagnose a wrong
subject that leaves the count and IDs unchanged. Repair one ticket from its
saved version. Then compare document recovery with the separate reconstruction
and testing of indexes and validation rules. The no-account path remains available.

Submit only the completed `05_mongodb_logical_recovery.ipynb` notebook.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

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
