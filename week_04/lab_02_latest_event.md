# Lab 2: Show the Latest Event Without Hiding a Request

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_04/04_reliable_reporting.ipynb)

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_04/lab_02_latest_event.md)

Add a latest-history summary to the active-ticket queue. Each active request must
appear once, even if it has no assignee. Work individually in class; use the same
12-ticket fixture and the notebook's Day 2 worked examples.

## 1. Understand the Ranking Before Filtering

Run this complete query and inspect ticket 1003:

```sql
SELECT ticket_id, event_id, event_type, event_at,
       ROW_NUMBER() OVER (
           PARTITION BY ticket_id
           ORDER BY event_at DESC, event_id DESC
       ) AS rn
FROM metro_support.ticket_events
ORDER BY ticket_id, rn;
```

The result still contains 21 events. Each ticket's numbering restarts at 1.
For ticket 1003, event 5007 receives 1, 5006 receives 2, and 5005 receives 3.
Use a CTE to name that result before filtering its `rn` column.

The secondary `event_id` order breaks equal-timestamp ties deterministically.
It is a reporting rule, not proof of which real-world event happened last.

## 2. Build and Check the View

Adapt the notebook's worked all-ticket query into
`metro_support.active_ticket_latest_event`. Its columns must be `ticket_id`,
`status`, `event_id`, `event_type`, and `event_at`. Use the **current ticket
status** to keep `new`, `open`, and `in_progress` requests.

Start from `tickets` and `LEFT JOIN` the ranked events. Keep `e.rn = 1` in the
`ON` condition so a ticket with no recorded event would retain NULL event fields.
Do not require an assigned staff member. Test your SELECT before wrapping it in
`CREATE OR REPLACE VIEW`.

Check **7 distinct ticket IDs** with no duplicate identifiers. Confirm that
ticket 1004 keeps event 5008 and ticket 1009 keeps event 5016. Inspect a multi-event
active ticket's source history and check its selected event independently.

**Submit:** `week_04_latest_event.sql` in Brightspace, containing the view and
verification queries. Add brief SQL comments explaining the tie-break and what
would happen to a ticket with no events if `e.rn = 1` moved from `ON` into `WHERE`.
No separate report, screenshot collection, or notebook submission is required.
