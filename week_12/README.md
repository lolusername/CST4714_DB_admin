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

Use [Chapter 12: Reliability Is a Set of Explicit Promises](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read the replica-set, acknowledgment, read-control, and CAP sections. Explain the A/B/C partition case without changing a real deployment.
- **Before Day 2:** read from **Replication Is Not Backup** through **Verify a MongoDB Restore**. Distinguish BSON-aware data recovery from restoring indexes, validators, and project configuration.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [15-minute logical recovery notebook — today's Day 2 lab](materials/notebooks/05_mongodb_logical_recovery_short.ipynb)
- [Original full recovery notebook — optional reference](materials/notebooks/05_mongodb_logical_recovery.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_12/materials/notebooks/05_mongodb_logical_recovery_short.ipynb) for the short Lab 2; save a working copy in Drive.
- [Week 12 student deck](week_12_mongodb_reliability.pptx)
- [Week 12 PDF handout](week_12_mongodb_reliability.pdf)
- [Week 12 transcript](week_12_mongodb_reliability_transcript.md)

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 12 videos](videos/README.md).

- [Replica sets: oplog, lag, and elections](videos/01_replica_set_election.mp4) (1:24): A primary records ticket 1099 in its oplog and two secondaries copy it at different speeds. When the primary is lost, a voting majority can elect a new one, but two isolated survivors cannot.
- [Write concern, read preference, and read concern](videos/02_write_read_concern.mp4) (1:39): Follow submission-1099 while member C is cut off: which acknowledgments w:1, majority, and w:3 can collect, why a timeout means "unknown", and why a read from C can miss a write that A and B kept.
- [Replication is not backup: logical recovery](videos/03_logical_recovery.mp4) (1:31): A deletion replicates to every member, so only a separate artifact still holds the five tickets. Restore it into a separate target, then catch a wrong subject that the count and ID checks miss and repair it from the saved version.

<!-- videos:end -->

## Free External References

- [Atlas Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/)
- [MongoDB Atlas Backup and Recovery course](https://learn.mongodb.com/learn/course/mongodb-atlas-backup-recovery/lesson-1-back-up-and-recover-an-atlas-free-tier/learn)

## Day 1: Build a Reliability Promise

Use **slides 1-16**. Follow one request from the primary's write through oplog
replication, acknowledgment, and the next read. Compare what A and B can do while
C is isolated, then work through separate recovery-point and recovery-time
examples. The Atlas screen explains why the free path needs a retained logical
artifact rather than a paid backup feature.

Complete [Lab 1: Match user expectations to replica and recovery decisions](lab_01_reliability_decisions.md).

Submit one Brightspace text response: a confirmation/read policy and the supplied
recovery-timeline analysis. No live failover or cluster reconfiguration is needed.

The final project is introduced through the
[canonical final-project page](materials/assignments/final_project.md). Use project work
to choose a scenario and its important reads/writes in your existing project
notes, rather than making another Week 12 submission.

## Day 2: Export, Restore Elsewhere, and Verify

For the **one-hour class**, use **slides 17–24** for the core recovery explanation
and the short notebook's numbered cells **01–07** for the demonstration. Briefly
use slides **25/28** to distinguish data from rules; the remaining full-lab
activities are optional today.
The five-ticket fixture matches the longer course example.

Complete [Lab 2: Recover one ticket in 15 minutes](lab_02_mongodb_recovery.md).

**Today's short-lab directions supersede the longer assignment wording on
slide 29 and in the older deck transcript.** Use ticket **1004**, the short
notebook, and a **viewable Colab link** for submission. The deck's Atlas setup,
rule-reconstruction, and PostgreSQL archive-comparison activities are optional
reference, not extra tasks for today's lab.

Run the supplied `mongomock` setup, inspect Extended JSON, restore the five
saved documents into a separate target, and diagnose the wrong subject on
ticket **1004**. Change one line to select its saved document, repair it, and
repeat the repair to check that five tickets remain. Finish with a **2–3 sentence**
explanation. No Atlas account or validator exercise is required today.

A document file does not restore index definitions, validators, or application
configuration. Recognize that limitation; the longer reconstruction and testing
activities remain [optional reference](reference_mongodb_recovery_extended.md).

**Submit a shared, viewable Colab notebook link in Brightspace. Do not submit an
`.ipynb` attachment.** Keep the failed check, repaired outputs, and explanation in
your saved Drive copy.

For support with the lab's explanation, use [Writing About Database Decisions](materials/assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

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

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
