# Week 14: Polyglot Incident Response and Final Project Clinic

## The Week's Question

When PostgreSQL and MongoDB disagree, how do we identify the authoritative fact,
trace propagation, repair safely, and verify more than one record?

## What You Will Be Able to Do

- identify the authoritative owner of a duplicated fact;
- trace an operation through commit, event, consumer, and projection evidence;
- distinguish dual-write, outbox, retry, idempotency, and reconciliation concerns;
- write a concise incident update; and
- audit final-project operations evidence against the canonical rubric.

## Course OER

- [Module 14: Multiple databases multiply options and obligations](../textbook/module_14_polyglot.md)
- [Week 14 student deck](week_14_polyglot_incident.pptx)
- [Week 14 PDF handout](week_14_polyglot_incident.pdf)
- [Week 14 transcript](week_14_polyglot_incident_transcript.md)

## Day 1: Individual Polyglot Incident Room

Complete [Lab: Repair a stale MongoDB projection](lab_01_polyglot_incident.md).

Submit only `week_14_incident_report.md`.

## Day 2: Final Project Operations Clinic

Use the [canonical final project](../final_project.md) and its rubric. Work
individually on the highest-risk missing evidence: model, query, index, access,
backup/restore, verification, reliability tradeoff, or reproducibility.

Complete the checkpoint inside your existing project package. There is no separate
Week 14 project assignment and no alternate deliverable list.

## Optional Industry Extension: Duplicate-Event Chaos Test

This activity is optional, ungraded, and does not add a submission.

An idempotent consumer receives projection events in this order: version 17,
version 17 again, delayed version 16, and version 18. Write the accept/ignore rule
for each event using stable event IDs and source versions. Then propose one
reconciliation query and one metric that would reveal a paused or repeatedly
failing consumer. Explain why "exactly once" wording would hide rather than solve
the duplicate and ordering obligations.

## End-of-Week Self-Check

For every fact duplicated across systems, name its owner, propagation direction,
acceptable lag, reconciliation check, and recovery order.
