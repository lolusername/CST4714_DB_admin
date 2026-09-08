# Week 4: Expose and Change Data Safely

## The Week's Question

How can we create a stable data interface and change its underlying schema without
surprising users or losing the ability to verify and recover?

## What You Will Be Able to Do

- create a view with an explicit consumer-facing contract;
- use identity columns and explain why generated identifiers have gaps;
- inspect views, columns, defaults, constraints, and dependencies;
- rehearse a migration, check its result, and explain the repair boundary; and
- apply expand, migrate, verify, and contract reasoning to a small change.

## Before Class: Assigned Reading

Use [Chapter 4: Safe Changes Are Planned and Verified](../../textbook/module_04_change.md).

- **Before Day 1:** read **Views Create a Query Interface** through **Introspection Reveals the Actual State**. Trace the explicitly committed and rolled-back insertions. Reading examples use separate object names so they can coexist with the lab.
- **Before Day 2:** read from **What a Migration Must Establish** through **Verification Should Cover Structure and Meaning**. Focus on unknown historical values and compatibility with older clients.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Week 4 student deck](week_04_views_identity_safe_change.pptx)
- [Week 4 PDF handout](week_04_views_identity_safe_change.pdf)
- [Week 4 transcript](week_04_views_identity_safe_change_transcript.md)

## Day 1: Views, Identity, and Introspection

Use **slides 1-10**. The demonstration creates a requester view, reads all seven
active ticket results, and follows three identity allocations through their
commit or rollback decisions. In
[Lab 1: Build a stable query interface](lab_01_views_identity.md), adapt the view
to an optional assignee and explain the identity gap. The lab includes the
metadata queries needed to inspect both objects.

Submit only `week_04_views_identity.sql`.

## Day 2: Migration and Verification

Use **slides 11-21**. Follow the complete `source_channel` rehearsal, compare
before and after states, and test accepted and rejected values. Then complete
[Lab 2: Add a field without inventing history](lab_02_safe_migration.md), using
the slides and chapter as references. Continue in the same database from Day 1;
do not reset the dataset between these labs.

Submit only `week_04_safe_migration.sql`.

## Optional Industry Extension: Zero-Downtime Change Note

This activity is optional, ungraded, and does not add a submission.

Write a seven-sentence change note for replacing a legacy `priority_text` field
with a constrained `priority_code` while an older client still reads the original
field. Name the precondition, expand step, backfill, compatibility path,
verification query, rollback or forward-repair boundary, and remaining risk. The
challenge is to preserve both old and new readers during the change rather than
compressing the migration into one destructive command.

## End-of-Week Self-Check

Explain why a successful `ALTER TABLE` does not by itself confirm that existing
data, permissions, views, and application queries still work.
