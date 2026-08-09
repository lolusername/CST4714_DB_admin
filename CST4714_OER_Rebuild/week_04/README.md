# Week 4: Expose and Change Data Safely

## The Week's Question

How can we create a stable data interface and change its underlying schema without
surprising users or losing the ability to verify and recover?

## What You Will Be Able to Do

- create a view with an explicit consumer-facing contract;
- use identity columns and explain why generated identifiers have gaps;
- inspect views, columns, defaults, constraints, and dependencies;
- write a five-part migration record; and
- apply expand, migrate, verify, and contract reasoning to a small change.

## Read and Use

- [Module 4: Safe changes are planned and verified](../textbook/module_04_change.md)
- [Week 4 student deck](week_04_views_identity_safe_change.pptx)
- [Week 4 PDF handout](week_04_views_identity_safe_change.pdf)
- [Week 4 transcript](week_04_views_identity_safe_change_transcript.md)

## Day 1: Views, Identity, and Introspection

Complete [Lab 1: Build a stable query interface](lab_01_views_identity.md).

Submit only `week_04_views_identity.sql`.

## Day 2: Migration With Evidence

Complete [Lab 2: Add a required field safely](lab_02_safe_migration.md).

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

Explain why a successful `ALTER TABLE` does not by itself prove that existing
data, permissions, views, and application queries still work.
