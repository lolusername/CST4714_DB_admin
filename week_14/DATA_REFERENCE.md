# Week 14 data reference

## Tables, events, and the resident projection

One tickets row is the authoritative state of one request. The notebook runs SQLite, while the supplied incident describes PostgreSQL and a MongoDB projection. The Python dictionaries model how a consumer handles event delivery.

| ticket_id (integer primary key) | status (required text) | source_version (positive integer) |
|---|---|---|
|1008|open|16|
|1009|resolved|5|
|1010|resolved|7|

The outbox initially has no rows. Its `event_id` text primary key names an event; `ticket_id` references tickets; `status` and `source_version` carry the complete projected state. `(ticket_id, source_version)` is unique. Statuses allowed by the source are open/resolved/closed. All shown fields are present and non-null. Versions increase separately for each ticket.

Accepted updates add these complete outbox rows:

| event_id | ticket_id | status | source_version |
|---|---|---|---|
|evt-1008-17|1008|resolved|17|
|evt-1008-18|1008|closed|18|

The supplied delivery list is 17, 17 again, 16 late, 18. Each delivery holds event_id/status/source_version; the single-ticket loop already selects ticket 1008. `last_event_id` is absent in the initial projection and is added when an event applies. That absence differs from an explicit null. Move 16 to the end for the student experiment.

The reconciliation example has source 1008 closed/18, 1009 resolved/5, 1010 resolved/7. The resident dictionary has 1008 with the experiment result, 1010 open/7, and 9999 open/1. Dictionary keys are ticket IDs; no embedded ticket_id is required in those field dictionaries. Equal counts of 3 hide missing 1009, wrong 1010, unexpected 9999.
