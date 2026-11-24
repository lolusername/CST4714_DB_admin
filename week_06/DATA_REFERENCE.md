# Week 6: Data Reference

Day 1 uses the full Metro Support fixture and a restricted view. Day 2 uses the separate four-row ownership fixture below. SQL files remain the required submissions.

## Day 2 ownership fixture

The lab creates a separate `security_lab.resident_tickets` table. `ticket_id` is an integer primary key; `owner_role` and `subject` are required text. All values are supplied. No column is nullable; there are no generated IDs.

| ticket_id | owner_role | subject |
|---|---|---|
| 1 | resident_101_lab | Broken bench |
| 2 | resident_101_lab | Dark streetlight |
| 3 | resident_102_lab | Missed pickup |
| 4 | resident_102_lab | Leaking hydrant |

The two role names are PostgreSQL `NOLOGIN` roles used to test permissions on one connection. They are not rows in the full Metro Support `users` table, and they are not Supabase Auth accounts. The policy compares `owner_role` to `current_user`. It filters existing rows for a SELECT. A policy permitting a read does not itself grant SELECT and does not define an INSERT policy.

The lab later adds ticket 5 for `resident_102_lab`. Keep that addition separate from the four-row baseline. The real Supabase application example uses `auth.uid()` and an authenticated token rather than creating one PostgreSQL role for every person.

## The complete Metro Support fixture

The CSVs contain **8 users, 12 tickets, and 21 events**. They are fictional teaching data. A user can request many tickets; a ticket has one requester, an optional assignee, and several events. Each event belongs to one ticket and names its actor. IDs connect records; a display name is not a key.

The PostgreSQL schema stores timestamps as `timestamptz`; CSV/JSON show ISO 8601 strings with `Z` for UTC. In these CSVs, an empty field represents SQL `NULL`, not an empty string. SQL columns always exist even if their value is null. A missing JSON member is a different representation. These IDs are supplied, not generated.

### users: field dictionary

| Field | PostgreSQL type | Null allowed | Meaning / observed values |
|---|---|---|---|
| `user_id` | `integer` | No | Person identifier; primary key. |
| `display_name` | `text` | No | Display label; identity is still the user ID. |
| `email` | `text` | No | Fictional email; unique and required. |
| `role` | `text` | No | Application role label; not a PostgreSQL login role. Observed: `agent`, `analyst`, `resident`, `supervisor`. |
| `neighborhood` | `text` | No | Named neighborhood. |
| `created_at` | `timestamptz` | No | When the person record was created. |

<details>
<summary>All 8 users records, with every column</summary>

```csv
user_id,display_name,email,role,neighborhood,created_at
101,Requester 101,requester101@example.test,resident,Harbor,2026-01-08T14:20:00Z
102,Requester 102,requester102@example.test,resident,Northside,2026-01-10T09:15:00Z
103,Requester 103,requester103@example.test,resident,Central,2026-01-12T18:05:00Z
104,Requester 104,requester104@example.test,resident,Harbor,2026-01-18T11:40:00Z
201,Agent 201,agent201@example.test,agent,Central,2025-11-03T13:00:00Z
202,Agent 202,agent202@example.test,agent,Northside,2025-11-05T13:00:00Z
203,Agent 203,agent203@example.test,supervisor,Central,2025-09-14T13:00:00Z
204,Sam Okafor,sam.okafor@example.test,analyst,Harbor,2025-12-01T13:00:00Z
```

</details>

### tickets: field dictionary

| Field | PostgreSQL type | Null allowed | Meaning / observed values |
|---|---|---|---|
| `ticket_id` | `integer` | No | Ticket identifier; primary key in tickets and foreign key in events. |
| `requester_id` | `integer` | No | User who opened the ticket; references users.user_id. |
| `assignee_id` | `integer` | Yes | Assigned staff user; references users.user_id; null means unassigned. |
| `category` | `text` | No | Kind of service request. Observed: `parks`, `sanitation`, `streetlight`, `transportation`, `water`. |
| `priority` | `text` | No | Urgency label. Observed: `high`, `low`, `medium`, `urgent`. |
| `status` | `text` | No | Current workflow state. Observed: `closed`, `in_progress`, `new`, `open`, `resolved`. |
| `subject` | `text` | No | Short request description. |
| `opened_at` | `timestamptz` | No | When the ticket opened. |
| `closed_at` | `timestamptz` | Yes | Resolution/closure timestamp or null; cannot precede opened_at. |

<details>
<summary>All 12 tickets records, with every column</summary>

```csv
ticket_id,requester_id,assignee_id,category,priority,status,subject,opened_at,closed_at
1001,101,201,streetlight,high,open,Streetlight dark near bus stop,2026-02-01T23:10:00Z,
1002,102,202,sanitation,medium,in_progress,Missed recycling pickup,2026-02-02T15:45:00Z,
1003,103,201,water,urgent,resolved,Low water pressure,2026-02-03T12:05:00Z,2026-02-03T19:40:00Z
1004,104,,parks,low,new,Broken bench slat,2026-02-04T17:20:00Z,
1005,101,202,sanitation,high,resolved,Overflowing corner bin,2026-02-05T14:00:00Z,2026-02-05T20:15:00Z
1006,102,201,streetlight,medium,in_progress,Flickering lamp outside library,2026-02-06T01:30:00Z,
1007,103,202,parks,medium,open,Playground gate will not latch,2026-02-07T16:10:00Z,
1008,104,201,water,high,resolved,Hydrant leaking slowly,2026-02-08T10:25:00Z,2026-02-09T09:05:00Z
1009,101,,transportation,medium,new,Bus shelter panel cracked,2026-02-09T22:15:00Z,
1010,102,202,sanitation,low,closed,Replacement bin request,2026-02-10T13:50:00Z,2026-02-12T16:30:00Z
1011,103,201,transportation,high,open,Crosswalk signal delayed,2026-02-11T08:35:00Z,
1012,104,202,streetlight,low,resolved,Lamp stays on during daytime,2026-02-12T14:45:00Z,2026-02-14T18:10:00Z
```

</details>

### ticket_events: field dictionary

| Field | PostgreSQL type | Null allowed | Meaning / observed values |
|---|---|---|---|
| `event_id` | `integer` | No | History-entry identifier; primary key. |
| `ticket_id` | `integer` | No | Ticket identifier; primary key in tickets and foreign key in events. |
| `actor_id` | `integer` | No | User who performed the event; references users.user_id. |
| `event_type` | `text` | No | Kind of history entry. Observed: `assigned`, `created`, `status_changed`. |
| `old_status` | `text` | Yes | State before the event, or null if unavailable. Observed: `in_progress`, `open`. |
| `new_status` | `text` | Yes | State recorded after the event, or null. Observed: `closed`, `in_progress`, `new`, `open`, `resolved`. |
| `note` | `text` | Yes | Optional event explanation. |
| `event_at` | `timestamptz` | No | When the event happened. |

<details>
<summary>All 21 ticket_events records, with every column</summary>

```csv
event_id,ticket_id,actor_id,event_type,old_status,new_status,note,event_at
5001,1001,101,created,,open,Reported through mobile form,2026-02-01T23:10:00Z
5002,1001,201,assigned,open,open,Electrical crew notified,2026-02-02T14:05:00Z
5003,1002,102,created,,open,Pickup was scheduled for Monday,2026-02-02T15:45:00Z
5004,1002,202,status_changed,open,in_progress,Route supervisor checking vehicle log,2026-02-03T13:30:00Z
5005,1003,103,created,,open,Pressure lower on two floors,2026-02-03T12:05:00Z
5006,1003,201,status_changed,open,in_progress,Crew dispatched,2026-02-03T14:25:00Z
5007,1003,201,status_changed,in_progress,resolved,Valve adjustment restored pressure,2026-02-03T19:40:00Z
5008,1004,104,created,,new,Photo attached in original report,2026-02-04T17:20:00Z
5009,1005,101,created,,open,Bin blocks part of sidewalk,2026-02-05T14:00:00Z
5010,1005,202,status_changed,open,resolved,Extra collection completed,2026-02-05T20:15:00Z
5011,1006,102,created,,open,Flicker repeats every few seconds,2026-02-06T01:30:00Z
5012,1006,201,status_changed,open,in_progress,Ballast inspection scheduled,2026-02-06T15:10:00Z
5013,1007,103,created,,open,Gate opens toward play area,2026-02-07T16:10:00Z
5014,1008,104,created,,open,Small stream along curb,2026-02-08T10:25:00Z
5015,1008,201,status_changed,open,resolved,Gasket replaced and area checked,2026-02-09T09:05:00Z
5016,1009,101,created,,new,No sharp edge visible,2026-02-09T22:15:00Z
5017,1010,102,created,,open,Current bin lid is missing,2026-02-10T13:50:00Z
5018,1010,202,status_changed,open,closed,Replacement delivered,2026-02-12T16:30:00Z
5019,1011,103,created,,open,Wait exceeds one full light cycle,2026-02-11T08:35:00Z
5020,1012,104,created,,open,Possible photocell issue,2026-02-12T14:45:00Z
5021,1012,202,status_changed,open,resolved,Photocell cleaned and tested,2026-02-14T18:10:00Z
```

</details>

### Rules versus examples

The SQL enforces primary keys, foreign keys, required fields, unique emails, and `closed_at IS NULL OR closed_at >= opened_at`. The labels listed above are **observed values**, not enum constraints in this fixture. A data dictionary does not silently add a CHECK rule. The Week 8 small recovery fixture has a separate status CHECK; do not confuse the two schemas.
