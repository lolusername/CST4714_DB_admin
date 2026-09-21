# Week 14: Polyglot Incident Response and Final Project Clinic

## The Week's Question

When PostgreSQL and MongoDB disagree, how do we identify the authoritative fact,
trace propagation, repair safely, and verify more than one record?

## What You Will Be Able to Do

- identify the authoritative owner of a duplicated fact;
- trace an operation through commit, event, consumer, and projection records;
- distinguish dual-write, outbox, retry, idempotency, and reconciliation concerns;
- write a concise incident update; and
- audit final-project operations work against the canonical rubric.

## Before Class: Assigned Reading

Use [Chapter 14: Multiple Databases Multiply Options and Obligations](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read through the worked incident, including the outbox, version-guard, and reconciliation explanations. The lab uses a supplied incident and a small Python model, not a new distributed deployment.
- **Before Day 2:** review **Identity and Access Cross the Boundary Too**, **Backup and Restore Need an Order**, and **A One-Database Design Is Often the Stronger Decision** for the project clinic.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Week 14 student deck](week_14_polyglot_incident.pptx)
- [Week 14 PDF handout](week_14_polyglot_incident.pdf)
- [Week 14 transcript](week_14_polyglot_incident_transcript.md)
- [Guided incident notebook](materials/notebooks/08_polyglot_incident.ipynb), using SQLite and Python with no account or installation
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_14/materials/notebooks/08_polyglot_incident.ipynb) for Lab 1; save a working copy in Drive.

## Day 1: Individual Polyglot Incident Room

Complete [Lab: Repair a stale MongoDB projection](lab_01_polyglot_incident.md).

Use the guided notebook for the live transaction demonstration and individual
duplicate/delayed-event experiment. Click **Open in Colab** above, or download
the linked notebook for local Jupyter. Then submit one Brightspace text incident
update with the broken and repaired results. No notebook attachment is required.

## Day 2: Final Project Operations Clinic

Use the [canonical final project](../week_12/materials/assignments/final_project.md) and its rubric. Work
individually on the highest-risk unfinished area: model, query, index, access,
backup/restore, verification, reliability tradeoff, or reproducibility.

Complete the checkpoint inside your existing project package. There is no separate
Week 14 project assignment and no alternate deliverable list.

## Optional Industry Extension: When Version Checks Are Not Enough

This activity is optional, ungraded, and does not add a submission.

The required lab uses complete-state events for one ticket. Now imagine version
17 says "add one item" and version 18 says "add two items." If 18 arrives first,
explain why ignoring 17 loses an effect even with a monotonic version guard.
Propose an ordered replay or reconciliation strategy and a missing-version alert.
Do not claim the dictionary model implements a concurrent production consumer.

## End-of-Week Self-Check

For every fact duplicated across systems, name its owner, propagation direction,
acceptable lag, reconciliation check, and recovery order.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
