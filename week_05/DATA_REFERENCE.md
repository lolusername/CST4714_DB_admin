# Metro Support data reference

Metro Support is a fictional help desk. All people and records are synthetic.
The complete lab fixture contains **8 users, 12 tickets, and 21 events**. A user
may request many tickets; a ticket may have one assignee or no assignee; a ticket
may have many history events. Requester, assignee, and actor refer to different
roles and all point to `users.user_id`.

The fixture contains the values shown here. The
baseline SQL declares keys, required fields, unique email, and the date-order
check. In the integrity lab, you add CHECK constraints for some of the allowed values in status, priority, category, and role.

Every row has the declared columns. SQL NULL is a value marker for missing or
inapplicable information. Empty
CSV fields in this fixture load as SQL NULL. The SQL uses explicit integer IDs;
the identity experiment later creates a separate generated `note_id`.

## users

One row represents one person.

| Field | Type and rule | Meaning |
|---|---|---|
| `user_id` | integer; primary key | Unique person identifier; supplied explicitly in this fixture |
| `display_name` | text; required | Synthetic display label; join on the user ID |
| `email` | text; required and unique | Synthetic contact address ending in example.test |
| `role` | text; required | Observed: resident, agent, supervisor, analyst |
| `neighborhood` | text; required | Observed: Harbor, Northside, Central |
| `created_at` | timestamp with time zone; required | When the user record was created |

One complete example record (JSON notation for readability; SQL uses typed columns):

```json
{
  "user_id": 101,
  "display_name": "Requester 101",
  "email": "requester101@example.test",
  "role": "resident",
  "neighborhood": "Harbor",
  "created_at": "2026-01-08T14:20:00Z"
}
```

## tickets

One row represents one request.

| Field | Type and rule | Meaning |
|---|---|---|
| `ticket_id` | integer; primary key | One stable identifier for one request |
| `requester_id` | integer; required foreign key | Person who reported the request; references users.user_id |
| `assignee_id` | integer; nullable foreign key | Staff member assigned to the request; NULL means unassigned |
| `category` | text; required | Observed: parks, sanitation, streetlight, transportation, water |
| `priority` | text; required | Observed: low, medium, high, urgent |
| `status` | text; required | Observed: new, open, in_progress, resolved, closed |
| `subject` | text; required | Short description of the request |
| `opened_at` | timestamp with time zone; required | When the request was recorded |
| `closed_at` | timestamp with time zone; nullable | Closure time when recorded |

One complete example record (JSON notation for readability; SQL uses typed columns):

```json
{
  "ticket_id": 1001,
  "requester_id": 101,
  "assignee_id": 201,
  "category": "streetlight",
  "priority": "high",
  "status": "open",
  "subject": "Streetlight dark near bus stop",
  "opened_at": "2026-02-01T23:10:00Z",
  "closed_at": null
}
```

## ticket_events

One row represents one event on one request.

| Field | Type and rule | Meaning |
|---|---|---|
| `event_id` | integer; primary key | One stable identifier for one history event |
| `ticket_id` | integer; required foreign key | Request this event describes; references tickets.ticket_id |
| `actor_id` | integer; required foreign key | Person who acted; references users.user_id |
| `event_type` | text; required | Observed: created, assigned, status_changed |
| `old_status` | text; nullable | Prior status when relevant; absent for a creation event |
| `new_status` | text; nullable | Recorded resulting status when relevant |
| `note` | text; nullable | Explanation attached to the event |
| `event_at` | timestamp with time zone; required | When the event was recorded |

One complete example record (JSON notation for readability; SQL uses typed columns):

```json
{
  "event_id": 5001,
  "ticket_id": 1001,
  "actor_id": 101,
  "event_type": "created",
  "old_status": null,
  "new_status": "open",
  "note": "Reported through mobile form",
  "event_at": "2026-02-01T23:10:00Z"
}
```

## Names that change between exercises

- Week 1 uses a four-ticket extract and a two-row `agents` table. Its `agent_id`
  corresponds to the later `users.user_id`; its `name` corresponds to `display_name`.
- The first Week 2 examples use a smaller **4 / 6 / 9** fixture in `main`, with
  fewer columns. The separate **8 / 12 / 21** lab fixture uses `metro_support`.
  They are different instances; do not transfer requester IDs or counts between them.
- Week 5's `lock_lab.tickets` intentionally has only `ticket_id`, `priority`,
  and `status`. Its complete starting row is **1004 / medium / open**. The main
  Metro Support row 1004 is **low / new**. Always name the schema when explaining it.
- In the full fixture, active means `new`, `open`, or `in_progress`. Week 1's
  smaller question defines active as only `new` or `open`.

The original CSV files retain every record. The notebook also provides a named
fixture-loading cell and a visible count check before the lab queries.

## Week 5 example identifiers

The Day 1 lecture's worked assignment uses Agent 202 and event 5998. The student transaction lab deliberately uses Agent 201 and event 5999. These are separate rehearsal examples; use the IDs printed in the block you are running. The Day 2 lock_lab row begins medium/open, whereas the full Metro Support ticket 1004 begins low/new.
