# Week 10 Complete Ticket Data Reference

**One document represents one support ticket.** The Day 1 database has one
collection, `tickets`. Each ticket embeds one `requester` object, an array of
text `tags`, and an array of `events` objects. A requester can appear on several
tickets. A ticket can have several events. There is no separate users, agents,
or events collection in this Day 1 fixture; the IDs identify those people or
records in the case. Day 2 explores storing related records separately.

MongoDB calls each named value a **field**. The field names below are the exact
names to use in this notebook. These tables describe our supplied data; they do
not create a MongoDB schema validator or claim that every possible document has
the same fields.

### All Ticket Fields

| Field | Type | Meaning |
| --- | --- | --- |
| `_id` | ObjectId | Generated MongoDB document ID. |
| `ticket_id` | Integer | Ticket number in the support case. |
| `category` | String | Kind of request. |
| `priority` | String | Urgency label. |
| `status` | String | Current workflow state. |
| `subject` | String | Short description of the request. |
| `requester` | Document | The person who opened the ticket. |
| `assignee_id` | Integer or null | Assigned staff ID; null if unassigned. |
| `opened_at` | BSON date | When the ticket opened, in UTC. |
| `tags` | Array of strings | Descriptive labels. |
| `events` | Array of documents | The supplied history entries. |
| `course_fixture` | String | Marker identifying teaching records. |

### Values and Rules in This Fixture

- **`priority`:** every supplied ticket has this field. Values are `low`,
  `medium`, `high`, or `urgent`.
- **`status`:** values are `new`, `open`, `in_progress`, or `resolved`.
  In this exercise, **active** means `new`, `open`, or `in_progress`.
  There is no field named `active`.
- **`category`:** values are `streetlight`, `sanitation`, `water`, or `parks`.
- **`ticket_id`:** the original tickets are 1001–1006. The write exercise adds
  disposable ticket 1099. The loader creates a unique index on `ticket_id`.
- **`_id`:** a separate identifier generated at insertion. Its value changes
  between fresh runs; it is different from `ticket_id`.
- **`assignee_id`:** assigned staff are 201 or 202. Ticket 1004 is unassigned,
  so its value is null (`None` in Python).
- **`opened_at`:** constructed from a Python `datetime` and stored as a BSON
  date. Sort this field to order tickets by opening time.
- **`tags`:** a ticket can have several labels, such as `lighting` and `safety`.
- **`events`:** a ticket can have several event objects or an empty array.
- **`course_fixture`:** always `"cst4714"` on the supplied records. Keep it in
  the notebook filters so operations stay within the teaching records.

### Fields Inside Requester and Events

| Path used in a query | Type | Meaning |
| --- | --- | --- |
| `requester.user_id` | Integer | Requester identifier. |
| `requester.display_name` | String | Requester display label. |
| `events.event_id` | Integer | Event identifier. |
| `events.type` | String | Kind of event. |
| `events.actor_role` | String | Role of the person who performed it. |
| `events.at` | BSON date | When the event occurred, in UTC. |

Requester IDs are 101–104 here; the display labels look like `"Requester 101"`.
Tickets 1001 and 1005 both belong to requester 101. The supplied event IDs are
5001–5008; the later write exercise adds event 5999 to the disposable test ticket.
Event `type` values are `created`, `assigned`, or `status_changed`. The
`actor_role` values are `resident` or `agent`. An event's `at` date is different
from its parent ticket's `opened_at` date.

`requester.user_id` is a dotted path into one embedded object. `events.type`
reaches into objects inside an array. With `$elemMatch` on `events`, the conditions
inside it use the element's own keys, such as `type` and `actor_role`.
The `[]` notation in the shape below explains an array; do not include `[]` in a
MongoDB field path.

### Complete Document Shape

```text
tickets collection
└── one ticket document
    ├── _id: ObjectId (generated on insertion)
    ├── ticket_id: integer
    ├── category: string
    ├── priority: string
    ├── status: string
    ├── subject: string
    ├── requester: object
    │   ├── user_id: integer
    │   └── display_name: string
    ├── assignee_id: integer or null
    ├── opened_at: date
    ├── tags: [string, ...]
    ├── events: [
    │     {event_id: integer, type: string, actor_role: string, at: date}, ...
    │   ]
    └── course_fixture: string
```

### The Additional Test Field

The write exercise creates ticket **1099** with `test_record: True` (a Boolean).
The six original tickets do **not** have that field; an absent field is not an
explicit `False` value. The reset creates 1099 with `status: "new"` and
`events: []`. It initially omits `assignee_id` and `tags`; `$set` later adds
`assignee_id: 202`. Its event 5999 has the same four event fields listed above.
This is a disposable practice record, not a seventh original case ticket.

### Field Names Used in Different Course Examples

This notebook adapts selected columns from the Week 9 case. In its event objects,
`event_type` becomes **`type`** and `event_at` becomes **`at`**. Use those shorter
names in Day 1 queries. Day 2's separate-history examples use `event_type` and
`event_at` again. The fixture is not a lossless copy of every CSV field.
Empty `events` arrays on 1005 and 1006 mean their history is omitted here; they do
not establish that the original tickets never had events.

### Read the Six Tickets Before Predicting Results

`priority` is present in the stored data even if a query's projection leaves it
out. To display it, include `"priority": 1` in the **projection** (the second
dictionary passed to `find`). That does not add a priority condition to the
**filter** (the first dictionary). The crew exercise asks you to select active
work by category and status, then display priority as part of the result.

| Ticket | Category | Priority | Status | Opened at (UTC) |
| --- | --- | --- | --- | --- |
| 1001 | streetlight | high | open | 2026-02-01 23:10:00 |
| 1002 | sanitation | medium | in_progress | 2026-02-02 15:45:00 |
| 1003 | water | urgent | resolved | 2026-02-03 12:05:00 |
| 1004 | parks | low | new | 2026-02-04 17:20:00 |
| 1005 | sanitation | high | resolved | 2026-02-05 14:00:00 |
| 1006 | streetlight | medium | in_progress | 2026-02-06 01:30:00 |

### All Six Complete Supplied Documents

Every field supplied by the loader is shown below. Only the generated `_id` is
omitted because it is assigned at runtime. Dates use **MongoDB Extended JSON**:
`{"$date": "...Z"}` represents a BSON date, rather than an ordinary date-looking
string. These blocks are a readable data reference, not Python cells to run.
The actual loader constructs Python `datetime` values.

#### Ticket 1001

```json
{
  "ticket_id": 1001,
  "category": "streetlight",
  "priority": "high",
  "status": "open",
  "subject": "Streetlight dark near bus stop",
  "requester": {
    "user_id": 101,
    "display_name": "Requester 101"
  },
  "assignee_id": 201,
  "opened_at": {
    "$date": "2026-02-01T23:10:00Z"
  },
  "tags": [
    "lighting",
    "safety"
  ],
  "events": [
    {
      "event_id": 5001,
      "type": "created",
      "actor_role": "resident",
      "at": {
        "$date": "2026-02-01T23:10:00Z"
      }
    },
    {
      "event_id": 5002,
      "type": "assigned",
      "actor_role": "agent",
      "at": {
        "$date": "2026-02-02T14:05:00Z"
      }
    }
  ],
  "course_fixture": "cst4714"
}
```

#### Ticket 1002

```json
{
  "ticket_id": 1002,
  "category": "sanitation",
  "priority": "medium",
  "status": "in_progress",
  "subject": "Missed recycling pickup",
  "requester": {
    "user_id": 102,
    "display_name": "Requester 102"
  },
  "assignee_id": 202,
  "opened_at": {
    "$date": "2026-02-02T15:45:00Z"
  },
  "tags": [
    "recycling"
  ],
  "events": [
    {
      "event_id": 5003,
      "type": "created",
      "actor_role": "resident",
      "at": {
        "$date": "2026-02-02T15:45:00Z"
      }
    },
    {
      "event_id": 5004,
      "type": "status_changed",
      "actor_role": "agent",
      "at": {
        "$date": "2026-02-03T13:30:00Z"
      }
    }
  ],
  "course_fixture": "cst4714"
}
```

#### Ticket 1003

```json
{
  "ticket_id": 1003,
  "category": "water",
  "priority": "urgent",
  "status": "resolved",
  "subject": "Low water pressure",
  "requester": {
    "user_id": 103,
    "display_name": "Requester 103"
  },
  "assignee_id": 201,
  "opened_at": {
    "$date": "2026-02-03T12:05:00Z"
  },
  "tags": [
    "water",
    "building"
  ],
  "events": [
    {
      "event_id": 5005,
      "type": "created",
      "actor_role": "resident",
      "at": {
        "$date": "2026-02-03T12:05:00Z"
      }
    },
    {
      "event_id": 5006,
      "type": "status_changed",
      "actor_role": "agent",
      "at": {
        "$date": "2026-02-03T14:25:00Z"
      }
    },
    {
      "event_id": 5007,
      "type": "status_changed",
      "actor_role": "agent",
      "at": {
        "$date": "2026-02-03T19:40:00Z"
      }
    }
  ],
  "course_fixture": "cst4714"
}
```

#### Ticket 1004

```json
{
  "ticket_id": 1004,
  "category": "parks",
  "priority": "low",
  "status": "new",
  "subject": "Broken bench slat",
  "requester": {
    "user_id": 104,
    "display_name": "Requester 104"
  },
  "assignee_id": null,
  "opened_at": {
    "$date": "2026-02-04T17:20:00Z"
  },
  "tags": [
    "parks"
  ],
  "events": [
    {
      "event_id": 5008,
      "type": "created",
      "actor_role": "resident",
      "at": {
        "$date": "2026-02-04T17:20:00Z"
      }
    }
  ],
  "course_fixture": "cst4714"
}
```

#### Ticket 1005

```json
{
  "ticket_id": 1005,
  "category": "sanitation",
  "priority": "high",
  "status": "resolved",
  "subject": "Overflowing corner bin",
  "requester": {
    "user_id": 101,
    "display_name": "Requester 101"
  },
  "assignee_id": 202,
  "opened_at": {
    "$date": "2026-02-05T14:00:00Z"
  },
  "tags": [
    "sanitation",
    "safety"
  ],
  "events": [],
  "course_fixture": "cst4714"
}
```

#### Ticket 1006

```json
{
  "ticket_id": 1006,
  "category": "streetlight",
  "priority": "medium",
  "status": "in_progress",
  "subject": "Flickering lamp outside library",
  "requester": {
    "user_id": 102,
    "display_name": "Requester 102"
  },
  "assignee_id": 201,
  "opened_at": {
    "$date": "2026-02-06T01:30:00Z"
  },
  "tags": [
    "lighting",
    "library"
  ],
  "events": [],
  "course_fixture": "cst4714"
}
```

### Load the Practice Data

Run **Load the six practice tickets** below. Check for **6 inserted** and
**6 verified** documents before continuing. Its supporting Python is collapsed;
the data reference above stays visible. The cell also defines the small SQLite
helper used in Section 2.

Rerunning this cell replaces records marked `course_fixture: "cst4714"`,
including the later disposable test record, in this run's randomly named practice
database. Do not rerun it between the repeated-write steps. The final cleanup
removes the entire practice `tickets` collection. Keep personal and project data
out of this collection.

**License:** prose CC BY-NC-SA 4.0; synthetic data CC0.
