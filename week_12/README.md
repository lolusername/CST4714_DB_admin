# Week 12: Connect to Atlas and Recover a Ticket

## Week 12 recovery lesson — November 17 and 19

**Calendar correction:** Week 12 was November 17 and 19, 2026. The one-meeting Thanksgiving week is **Week 13, November 24**; use the [Week 13 lesson](../week_13/README.md) for that class. The recovery lesson below is retained as a condensed 100-minute Week 12 route, with one notebook exercise and one viewable Colab-link submission when assigned. It does not add a Thanksgiving-week assignment. Brightspace remains the source of actual due dates.

## What you will learn

Explain what an acknowledged write does and does not promise; distinguish a replicated copy from a retained recovery artifact; connect Colab to a real Atlas Free cluster; restore five documents to a separate collection; and repair a value that counts alone did not catch.

## Start here

- [Open the required Atlas notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_12/materials/notebooks/05_mongodb_atlas_recovery.ipynb) and save your own copy in Drive.
- [Required short lab: connect, recover, and verify](lab_02_mongodb_recovery.md).
- [Week 12 PowerPoint](week_12_mongodb_reliability.pptx), [PDF handout](week_12_mongodb_reliability.pdf), and [spoken transcript](week_12_mongodb_reliability_transcript.md).
- [Complete field and record reference](DATA_REFERENCE.md), also in the notebook before the first write.
- [Course corrections](../COURSE_CORRECTIONS.md) clarify dated screenshots and backup availability.
- **Before the recovery lesson:** read [Chapter 12](../Operating_Cloud_Databases.pdf), focusing on the replica/acknowledgment and logical-recovery sections. There is no separate reading report.

## Prepare the actual Atlas connection

Use your own **Free** cluster and a database user with `readWrite` on `cst4714_week12`. The notebook explains the difference between an Atlas login and database credentials. Add the **Colab runtime's** temporary IPv4 `/32` rule; do not authorize every IP. Use the hidden URI input or a Colab Secret. Never save a URI in code, output, or screenshots. No paid cluster, payment card, backup subscription, or API key is required.

The notebook uses real PyMongo requests. A successful ping is followed by a synthetic write/read and a Data Explorer check. It does not silently replace Atlas with `mongomock` when setup fails. If access is blocked, follow the instructor's actual Atlas demonstration and label observed outputs honestly while resolving your connection.

## Class sequence

| Time | Work |
|---|---|
| 0–25 minutes | One document, application/driver/server, replication, majority acknowledgment, and why replication is not historical recovery |
| 25–45 minutes | Atlas connection and five-ticket source: notebook Cells 01–04 |
| 45–65 minutes | Artifact, separate restore, and the wrong subject: Cells 05–06; retain the synthetic file with Cell 05b |
| 65–85 minutes | Individual short lab: repair ticket 1004 in Cell 07 and repeat-check in Cell 08 |
| 85–100 minutes | Explanation in Section 09, share/save, recovery limits, and project handoff |

The slide-to-cell route is explicit in the deck and transcript. Setup time comes before the 20-minute individual repair. No one is expected to provision an unfamiliar account and finish the entire exercise in 20 minutes.

## What to submit

**Submit your own saved Colab notebook's viewable sharing link in Brightspace.** Include the changed lookup, outputs, and 3–4-sentence explanation. Grant the instructor viewer access. Do not submit an `.ipynb` attachment, the starter link, a separate Lab 1 response, JSON file, or Atlas screenshot.

## Industry/Career Connection — GitLab's recovery incident

GitLab's account of its January 2017 PostgreSQL outage describes accidental deletion and problems with available recovery mechanisms. The platform differs from Atlas, but the operational responsibility is the same: retain a usable artifact, rehearse restoration, and check meaningful data values. Our five-ticket exercise practices those checks; it does not reproduce the production incident or prove a production recovery target. In a database administration interview, explain what you recovered and what your test did not establish.

[Read GitLab’s own postmortem](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/). Use this example during the lecture.

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 12 videos](videos/README.md).

- [Replica sets: oplog, lag, and elections](videos/01_replica_set_election.mp4) (1:24): A primary records ticket 1099 in its oplog and two secondaries copy it at different speeds. When the primary is lost, a voting majority can elect a new one, but two isolated survivors cannot.
- [Write concern, read preference, and read concern](videos/02_write_read_concern.mp4) (1:39): Follow submission-1099 while member C is cut off: which acknowledgments w:1, majority, and w:3 can collect, why a timeout means "unknown", and why a read from C can miss a write that A and B kept.
- [Replication is not backup: logical recovery](videos/03_logical_recovery.mp4) (1:31): A deletion replicates to every member, so only a separate artifact still holds the five tickets. Restore it into a separate target, then catch a wrong subject that the count and ID checks miss and repair it from the saved version.

<!-- videos:end -->

## Optional reference and limits

- [The former reliability decision exercise](lab_01_reliability_decisions.md) is optional, ungraded practice; it has no separate submission this week.
- [Full recovery notebook](materials/notebooks/05_mongodb_logical_recovery.ipynb) and [extended reference](reference_mongodb_recovery_extended.md) retain deeper reconstruction examples. Use the required Atlas route for class.
- [Legacy local short notebook](materials/notebooks/05_mongodb_logical_recovery_short.ipynb) provides a local mock for reference.
- Validator reconstruction is **not required this week**. It is optional reference; there is no next-week requirement implied.
- Free clusters have managed replicas but do not support the class forcing a primary failover. A normal ping/write does not test an election. [Free limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/).
- Atlas documents an optional billed Free-cluster backup subscription in private preview. Do not enable it. We use our own synthetic document artifact. [Current backup options](https://www.mongodb.com/docs/atlas/backup-restore-cluster/).
- This document file does not rebuild indexes, validators, users, or application configuration. Retain the runtime file outside Colab so you can restore it later.

The existing [final-project page](materials/assignments/final_project.md) remains the sole project requirements document. This week's work adds no project deliverable.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). The [static recovery illustration](illustrations/README.md) includes its editable Manim source. External materials keep their own terms.
