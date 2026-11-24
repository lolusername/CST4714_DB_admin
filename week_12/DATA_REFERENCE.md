## Data reference — read this before the first write

Every row below is one complete **application record**. MongoDB adds `_id`, its unique identifier, on insertion. That generated value varies by run and is retained in the saved file. `ticket_id` is our stable course identifier, protected by a unique index in the source collection. There are no joins or separate requester records in this fixture.

| ticket_id (integer) | status (text) | priority (text) | subject (text) | opened_at (UTC BSON date) |
|---|---|---|---|---|
| 1001 | open | high | Streetlight dark near bus stop | 2026-02-01 23:10 |
| 1002 | in_progress | medium | Missed recycling pickup | 2026-02-02 15:45 |
| 1003 | resolved | urgent | Low water pressure | 2026-02-03 12:05 |
| 1004 | new | low | Broken bench slat | 2026-02-04 17:20 |
| 1005 | resolved | high | Overflowing corner bin | 2026-02-05 14:00 |

`status` names the workflow state; this fixture uses new/open/in_progress/resolved, and the broader course also uses closed. `priority` is low/medium/high/urgent. All five fields are present and non-null here. A missing field and an explicit null are different states; neither occurs in these five records. Python displays a BSON date as a timezone-aware `datetime`. A date-looking string is still text. Read the saved types during the restore.
