# Lab 1: Prove Allow and Deny

## Purpose

Create one privilege group that can read a limited reporting view but cannot read
sensitive base data or update tickets.

This is individual work completed in class. Submit one SQL file. Use only a
personal course project because the lab creates roles.

## 1. Build the Access Boundary

Create `week_06_least_privilege.sql` and a no-login role named with your assigned
course suffix, such as `metro_analyst_ab12`. Avoid a shared generic name.

Create `metro_support.analyst_ticket_summary` with only:

- ticket ID;
- category;
- priority;
- status;
- opening timestamp; and
- closing timestamp.

Grant the role only the schema access and view read privilege it needs. Do not
grant base-table update, user email, or event-note access.

## 2. Test the Matrix

Use `SET ROLE` to test these actions:

| Action | Expected result |
|---|---|
| select from the analyst view | allowed |
| select email from `users` | denied |
| select note from `ticket_events` | denied |
| update a ticket | denied |

Run expected-deny statements separately. Copy the short permission error into a
comment and leave the denied statements commented in the submitted script so it
runs from top to bottom. Always `RESET ROLE` after the test.

## 3. Explain the Evidence

End the file with a comment naming:

- the actor, action, resource, and condition;
- what the allow test proves;
- what the deny tests prove; and
- one privileged path this test does not cover.

## Submit One Thing

Submit `week_06_least_privilege.sql`. No password, login role, API key, or
connection string belongs in the file.
