# Week 15 data reference

## Complete review fixture

One staff row is one staff member. One tickets row is one request. `tickets.assignee_id` is a nullable foreign key to `staff.agent_id`. A NULL means unassigned; it does not create a fourth staff member. SQLite foreign-key enforcement is enabled in setup.

|agent_id (integer primary key)|name (required text)|
|---|---|
|201|Agent 201|
|202|Agent 202|
|203|Agent 203|

|ticket_id (integer primary key)|assignee_id (integer or SQL NULL)|status (required text)|
|---|---|---|
|1|201|open|
|2|201|resolved|
|3|NULL|new|
|4|202|open|

Allowed status values are new/open/in_progress/resolved. No field is omitted from these SQL rows. Python prints SQL NULL as None; JSON encodes it as null. The JSON document uses the ticket identifier as its _id. It includes assignee_id and status.

Active IDs are 1, 3, 4. The zero-inclusive staff report counts matched ticket IDs and returns 201: 1, 202: 1, 203: 0. Ticket 3 is active but unassigned, so it is outside the matched staff workload. Three tickets are active. Two have an assignee.
