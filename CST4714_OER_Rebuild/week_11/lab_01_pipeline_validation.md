# Lab 1: Trace a Pipeline and Reject One Invalid Document

## Purpose

Build one useful aggregation, annotate how its grain changes, and add a focused
validator that preserves intentional flexibility.

This is individual work completed in class. Submit one MongoDB JavaScript file.

## 1. Build and Verify the Pipeline

Continue with your Week 10 `tickets` collection. Create
`week_11_pipeline_validation.mongodb.js` in GitHub's online editor.

Write a pipeline that returns one result document per category with:

- active ticket count;
- urgent active count;
- newest opening date; and
- a sorted set of assigned agent IDs where present.

Use an early `$match`, then `$group`, `$project`, and `$sort`. Before each stage,
add a comment stating the input and output grain.

Verify one category with a simpler `find` or `countDocuments` query and explain
what that check does not prove.

## 2. Add Focused Validation

Create or modify a validator requiring:

- numeric `ticket_id`;
- allowed `status` and `priority` values;
- string `subject`;
- BSON date `opened_at`; and
- when `events` exists, an array whose items require event ID, type, and date.

Inspect existing documents before using strict/error behavior. Test one valid
insert in a disposable record and delete it. Test one invalid status separately,
record the short validation error in a comment, and keep the invalid statement
commented in the submitted file.

## 3. Explain the Boundary

End the file with comments identifying:

- one field intentionally not required;
- one bad state the validator prevents;
- one application-level rule it does not enforce; and
- why a fast index would not replace validation.

## Submit One Thing

Submit `week_11_pipeline_validation.mongodb.js`. Do not include a URI, password,
Atlas project ID, or unredacted account image.
