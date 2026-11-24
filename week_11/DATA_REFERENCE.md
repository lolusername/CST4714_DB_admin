# Week 11 data reference

## One document means one request

This independent four-ticket fixture is not the twelve-ticket CSV or Week 10 fixture. All application fields and events are listed below. MongoDB adds a generated `_id`; `ticket_id` is a separate unique course ID. `assignee_id` refers conceptually to a staff member, but no staff collection is joined in this exercise. The field is an integer or explicit null: ticket 1004 is unassigned. A missing field would be different from this stored null.

`category`, `status`, `priority`, and `subject` are text. Category is streetlight or sanitation; status here is new/open/in_progress/resolved; the active filter includes new/open/in_progress. Priority is urgent/high/low here (medium also exists elsewhere in the course). `opened_at` is a UTC BSON date, represented below as an ISO string for readability. `events` is an array of embedded documents; `events.type` is text. Ticket 1004's empty array is present, not null or missing. No event time or actor field exists in this fixture.

```json
[
  {
    "ticket_id": 1001,
    "category": "streetlight",
    "status": "open",
    "priority": "urgent",
    "subject": "Dark streetlight",
    "assignee_id": 201,
    "opened_at": "2026-02-01T00:00:00+00:00",
    "events": [
      {
        "type": "created"
      },
      {
        "type": "assigned"
      }
    ]
  },
  {
    "ticket_id": 1002,
    "category": "sanitation",
    "status": "in_progress",
    "priority": "high",
    "subject": "Missed pickup",
    "assignee_id": 202,
    "opened_at": "2026-02-02T00:00:00+00:00",
    "events": [
      {
        "type": "created"
      }
    ]
  },
  {
    "ticket_id": 1003,
    "category": "streetlight",
    "status": "resolved",
    "priority": "urgent",
    "subject": "Lamp repaired",
    "assignee_id": 201,
    "opened_at": "2026-02-03T00:00:00+00:00",
    "events": [
      {
        "type": "created"
      },
      {
        "type": "resolved"
      }
    ]
  },
  {
    "ticket_id": 1004,
    "category": "streetlight",
    "status": "new",
    "priority": "low",
    "subject": "Flickering lamp",
    "assignee_id": null,
    "opened_at": "2026-02-04T00:00:00+00:00",
    "events": []
  }
]
```

## Grain check

Active ticket IDs are 1001, 1002, 1004. Default unwind emits event rows for 1001 twice and 1002 once; 1004 emits none. Both totals are 3, but they describe different populations. Group before unwind when the question counts tickets.
