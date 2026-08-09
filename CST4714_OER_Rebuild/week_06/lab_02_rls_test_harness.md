# Lab 2: Restrict Rows by Current Actor

## Purpose

Observe row-level security with a simple PostgreSQL test harness before mapping the
same idea to Supabase Auth and `auth.uid()`.

This is individual work completed in class. Submit one SQL file.

## 1. Create Actors and Owned Rows

Create `week_06_rls_test.sql`. In a disposable `security_lab` schema:

- create two uniquely suffixed no-login roles representing resident 101 and
  resident 102;
- create a `resident_tickets` table with ticket ID, owner role, subject, and
  status; and
- insert two rows for each actor.

Grant schema usage and table select to both roles. Do not grant update.

## 2. Enable and Test RLS

Enable row-level security. Create a select policy whose `USING` expression allows
a row only when its stored owner role equals `current_user`.

Use `SET ROLE` to run the same ordered query as each resident role. Record:

- expected visible ticket IDs;
- observed visible ticket IDs; and
- whether a row owned by the other role appears.

Try one update separately and record the short expected permission error. Reset
the role after every actor test.

Then query as the table owner and explain why owner behavior is not valid evidence
for an ordinary user's RLS result.

## 3. Transfer the Pattern to Supabase

End the file with a comment that maps:

- `current_user` in this harness to a request identity;
- the stored owner role to a user ownership UUID;
- the no-login resident roles to Supabase's `authenticated` request role plus
  token claims; and
- the policy comparison to `requester_auth_id = auth.uid()`.

Name the application or API path that would need to be tested in addition to the
SQL editor.

## Submit One Thing

Submit `week_06_rls_test.sql`. It must show two actors receiving different row
sets, one expected denial, and the Supabase mapping explanation.
