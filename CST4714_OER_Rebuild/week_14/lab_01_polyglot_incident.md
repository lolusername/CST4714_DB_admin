# Lab: Repair a Stale MongoDB Projection

## Purpose

Triage a cross-database incident from an evidence packet, choose a safe repair,
and write a workplace-readable update.

This is individual work completed in class. No live cloud system is required.
Submit one Markdown file.

## Incident

The resident portal reads a MongoDB ticket projection and shows ticket 1008 as
`open`. The staff dashboard reads authoritative PostgreSQL and shows `resolved`.

Architecture:

```text
PostgreSQL ticket + outbox transaction -> relay -> MongoDB projection
```

Evidence packet:

```text
PostgreSQL tickets:
ticket_id=1008 status=resolved source_version=17 updated_at=14:03:12Z

PostgreSQL outbox:
event_id=evt-1008-17 aggregate_id=1008 type=ticket_resolved
source_version=17 created_at=14:03:12Z published_at=14:03:13Z

Consumer log:
14:03:13Z received evt-1008-17 attempt=1
14:03:13Z error timeout writing projection
14:03:14Z queued retry evt-1008-17
14:04:00Z retry worker paused: expired database credential

MongoDB projection:
ticket_id=1008 status=open source_version=16 last_event_id=evt-1008-16

Operations note:
The event handler uses an upsert keyed by ticket_id and applies an event only when
incoming source_version is greater than the stored source_version.
```

## 1. Build the Timeline and Ownership Decision

Create `week_14_incident_report.md`. List the events in order and answer:

- Which system owns ticket status?
- Did the authoritative transaction commit?
- Was the event created and published?
- Where did propagation stop?
- Which evidence rules out a missing outbox event?

## 2. Recommend and Verify the Repair

Choose a repair that preserves the authoritative state and the idempotent version
rule. Explain why manually changing both databases or replaying every event from
the beginning is not the first action.

Write five verification checks covering the repaired record, retry queue,
duplicate effect, consumer lag, and a broader affected partition. Include one
rollback or containment action if the repair produces unexpected results.

## 3. Write the Incident Update

Write a concise update with:

- user impact;
- evidence-based cause;
- mitigation;
- verification;
- remaining limitation; and
- prevention next step.

Separate observed facts from inference and avoid blaming a person.

## Submit One Thing

Submit `week_14_incident_report.md` containing the timeline, repair decision,
verification checks, and incident update.
