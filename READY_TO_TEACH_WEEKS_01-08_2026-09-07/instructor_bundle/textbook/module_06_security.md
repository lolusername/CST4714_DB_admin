# Access Should Be Useful and Limited

## Operating Question

How can we prove that the right actor can perform a required action while the
wrong actor is denied, without exposing credentials during the test?

## Learning Outcomes

After this module, you can:

- distinguish identity, authentication, authorization, and auditing;
- represent access as actor-action-resource conditions;
- create PostgreSQL roles and apply grants using least privilege;
- explain the relationship among Supabase Auth, PostgreSQL roles, and row-level
  security;
- write and test a beginner RLS policy; and
- handle connection strings and service credentials safely.

## Security Questions Need Separate Terms

Imagine two residents using the same repair application. Both have valid accounts;
both need to read their requests. If one resident changes a ticket number in a
browser URL, the server must still decide whether that person may read the
requested row. Hiding a button or using a long identifier does not make the row
private. The access decision must hold when the caller sends a different request.

- **Identity:** who or what claims to be acting?
- **Authentication:** how is that claim verified?
- **Authorization:** what may the authenticated actor do?
- **Auditing:** which logs record relevant actions and decisions?

A valid password proves authentication only within its mechanism. It does not mean
the account should read every row. A failed query may reflect authentication,
authorization, network access, an object name, or SQL syntax. Classify the failure
before changing permissions.

These stages explain several different symptoms. "Network unreachable" occurs
before the server can decide table permissions. A bad password prevents the
intended login. "Permission denied for table" means a reachable database rejected
an operation. A query returning no rows may be valid because no row satisfies an
access policy. Granting every privilege is not an appropriate response to all
four situations.

## Model Access as Actor, Action, Resource, and Condition

Replace "give the app access" with a testable statement:

| Actor | Action | Resource | Condition |
|---|---|---|---|
| support agent | `SELECT`, `UPDATE` | assigned tickets | only rows assigned to that agent |
| resident | `SELECT` | tickets | only tickets requested by that resident |
| analyst | `SELECT` | reporting view | no private internal notes |
| migration process | schema changes | application schema | only during controlled deployment |

This matrix reveals different layers. A table grant may permit `SELECT` on the
table, while RLS limits which rows the statement can return.

A **privilege** authorizes an operation on an object, such as reading a table.
A **policy** can add conditions on which rows that operation may affect. For an
ordinary SELECT in the simple resident design, think of the result as the rows
satisfying both the application's question and the resident's ownership rule.

$$
R_{\text{visible}} = \sigma_{\text{requested condition}\,\land\,\text{owner is current resident}}(R).
$$

This is a model of the result, not an instruction to trust an ownership condition
supplied by the browser. The database policy is applied even when the caller's
query omits that condition. Object privileges must also permit SELECT; a row
policy does not grant table access on its own.

## PostgreSQL Roles Represent Users and Groups

PostgreSQL uses roles for both login identities and privilege groups.

```sql
CREATE ROLE metro_analyst NOLOGIN;
GRANT metro_analyst TO CURRENT_USER;
```

This creates a permission group and lets your current administrative login assume
it during the controlled test. It does not create a new password or an application
account. Run it only in your personal practice environment with the permitted
role-management privileges. If the role already exists from your earlier run,
inspect or clean up that exercise rather than treating an existing shared role
as disposable.

A group role with `NOLOGIN` collects privileges. Login roles become members. This
separates identity lifecycle from permission definition.

`session_user` identifies the original database login; `current_user` is the
effective database role used for checks such as the test below. They can differ
after `SET ROLE`. A person in the Supabase dashboard is another identity again.
Keeping these names distinct makes an access test interpretable.

## Grant the Minimum Required Privileges

PostgreSQL privileges are object-specific. Accessing a table in a schema can
require both schema `USAGE` and table privileges.

```sql
GRANT USAGE ON SCHEMA metro_support TO metro_analyst;
GRANT SELECT ON metro_support.chapter4_active_queue TO metro_analyst;
```

If the analyst should read only the view, do not also grant broad access to every
base table. The view above is introduced in Chapter 4; create it there first, or
use the complete limited-view example later in this chapter.

A normal PostgreSQL view generally checks underlying relation access using the
view owner's permissions. This can deliberately expose selected columns without
granting the caller direct access to the base table. It also means that a view
owned by an elevated role is not automatically an RLS-safe resident interface.
On PostgreSQL 15 and later, a `security_invoker` view uses the caller's underlying
permissions instead. The reporting-view exercise and the resident-policy
exercise test different designs, not interchangeable shortcuts.

Revoke privileges that were granted too broadly:

```sql
REVOKE UPDATE, DELETE
ON metro_support.tickets
FROM metro_analyst;
```

Privileges on future tables are separate from current objects. Default privileges
can automate future grants, but they are defined by the object-creating role and
must be tested.

Privileges can also come from memberships and `PUBLIC`, the implicit group of
all roles. Revoking a direct grant from one role does not erase a privilege it
still receives through another path. Therefore, read the effective result of a
test instead of treating the presence of a REVOKE statement as a security proof.

## Test Both an Allowed and a Denied Action

An allow-only test is incomplete. In a dedicated practice environment:

```sql
BEGIN;
SET LOCAL ROLE metro_analyst;

SELECT current_user, ticket_id, status
FROM metro_support.chapter4_active_queue;
ROLLBACK;
```

Then test the denied operation in its own transaction on the same connection:

```sql
BEGIN;
SET LOCAL ROLE metro_analyst;

-- This should fail if no base-table update privilege was granted.
UPDATE metro_support.tickets
SET priority = 'urgent'
WHERE ticket_id = 1001;

-- Execute this even if the client stops after the expected error.
ROLLBACK;
```

The expected error is an insufficient-privilege error, SQLSTATE `42501`, not a
misspelled table or a broken connection. Rollback ends the transaction and its
local role setting. Keep actor, query, and transaction on one connection: separate
editor executions may use different pooled sessions. The
[Week 6 lab](../weeks/week_06/lab_01_least_privilege.md) includes a small Colab
display cell when a web editor hides intermediate results.

## Supabase Adds an Identity Layer to PostgreSQL

Supabase Auth can issue JSON Web Tokens for application users. Requests through
Supabase's data APIs are mapped to PostgreSQL roles such as `anon` or
`authenticated`, and claims can be read by policy helpers such as `auth.uid()`.

A **token** is a value the client presents with a request. A JSON Web Token, or
JWT, carries claims such as a user identifier; the receiving service verifies
the token before using those claims. A signed token is not necessarily encrypted.
Treat a usable login token as a credential, even when its payload can be decoded.
The browser must not be allowed to establish identity merely by writing an
arbitrary user ID in the request body.

This creates distinct concepts:

- a Supabase dashboard account administers a project;
- a PostgreSQL role controls database privileges;
- an application user exists in the authentication system;
- a token carries claims about a request; and
- an RLS policy evaluates row access inside PostgreSQL.

Do not treat these identities as interchangeable.

In the Day 2 lab, two PostgreSQL roles make the difference observable without
building a login system. The four supplied rows name their owner role; comparing
`owner_role = current_user` makes resident 101 see tickets 1 and 2 while resident
102 sees 3 and 4. A normal Supabase application instead serves many people through
the shared `authenticated` role and uses verified user claims to distinguish
them. It does not need one database role for every resident.

The Supabase SQL editor commonly runs with elevated ownership privileges. Table
owners and roles with `BYPASSRLS` can bypass row-level security. A successful query
in the editor therefore does not prove what an anonymous or authenticated client
can see.

## Row-Level Security Adds a Row Predicate

The following is an **illustrative Supabase adaptation**, not a command to paste
into the unchanged Metro Support fixture. That fixture has integer requester
IDs, not Supabase Auth UUIDs. A UUID is a 128-bit identifier, commonly displayed
as groups of hexadecimal characters; it is not a password.

For this adaptation, assume that a reviewed migration has created and populated
`requester_auth_id uuid` with actual application-user identities, the appropriate
schema is exposed to the intended API, and SELECT has been explicitly granted to
`authenticated`. Adding a nullable column without mapping existing residents
would not establish correct ownership.

```sql
ALTER TABLE metro_support.tickets ENABLE ROW LEVEL SECURITY;

CREATE POLICY residents_read_own_tickets
ON metro_support.tickets
FOR SELECT
TO authenticated
USING (requester_auth_id = (SELECT auth.uid()));
```

`USING` controls which existing rows are visible for the operation. `WITH CHECK`
controls which new or changed row states may be created for relevant operations.

With no authenticated user, `auth.uid()` can be NULL. Equality with NULL is not
true, so this ownership condition does not select a row. That is the same
three-valued logic introduced in Chapter 2, now serving an access boundary.

```sql
CREATE POLICY residents_insert_own_tickets
ON metro_support.tickets
FOR INSERT
TO authenticated
WITH CHECK (requester_auth_id = (SELECT auth.uid()));
```

Policy design is default-deny after RLS is enabled: if no applicable policy allows
the operation, ordinary roles cannot perform it. Verify current Supabase guidance
and test through the same role and request path the application uses.

An INSERT also needs an INSERT grant. If it supplies a different user's ID, the
`WITH CHECK` condition rejects the new row. A SELECT of another user's existing
row ordinarily returns no matching row rather than revealing it and then raising
an error. This is why access testing must compare visible identities as well as
error messages. [Supabase RLS guide](https://supabase.com/docs/guides/database/postgres/row-level-security)

Do not solve a failed ownership test by adding `USING (true)`. That rule allows
every row for its covered operation. Multiple permissive policies combine with
OR, so one broad policy can undo the restriction expected from another. Owners
normally bypass RLS; superusers and roles with `BYPASSRLS` bypass it. RLS is not a
defense against an unrestricted database administrator.
[PostgreSQL row-security rules](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

## Worked Example: Build an Access Test Matrix

**Requirement:** an analyst may read ticket identifiers, category, priority,
status, and opening time, but not resident email addresses or internal event notes.

### Design

Create a limited view:

```sql
CREATE OR REPLACE VIEW metro_support.analyst_ticket_summary AS
SELECT ticket_id, category, priority, status, opened_at, closed_at
FROM metro_support.tickets;

GRANT USAGE ON SCHEMA metro_support TO metro_analyst;
GRANT SELECT ON metro_support.analyst_ticket_summary TO metro_analyst;
REVOKE ALL ON metro_support.users FROM metro_analyst;
REVOKE ALL ON metro_support.ticket_events FROM metro_analyst;
```

### Test

| Test | Expected |
|---|---|
| select from `analyst_ticket_summary` | allowed |
| select email from `users` | denied |
| select note from `ticket_events` | denied |
| update a ticket | denied |

### Interpret

If the expected allow succeeds and every expected deny fails for permission
reasons, the results support the stated boundary. They do not demonstrate protection
against a privileged administrator, a leaked credential, a vulnerable function,
or an untested API path.

## Secret Handling Is a Database Skill

A connection URI may include host, database, user, and password. Treat the whole
string as a secret when it contains credentials.

Safe notebook pattern:

```python
from getpass import getpass

database_url = getpass("Paste the temporary database URL: ")
```

Do not hardcode a secret, print it, save it in notebook output, or place it in a
GitHub issue. Use environment variables or platform secret storage in applications.

Supabase distinguishes publishable client keys from secret server keys; older
projects may also show legacy `anon` and `service_role` keys. A publishable key
identifies an application component, not a particular resident. A user's signed
login token supplies the user context. Secret keys and legacy service-role keys
provide elevated access and must not be shipped in browser code. Check the key
type, not just whether a string is called an "API key."
[Supabase API-key guide](https://supabase.com/docs/guides/getting-started/api-keys)

If a secret reaches Git history, revoke or rotate it first. Removing the visible
line does not make the old credential safe.

## Network Controls Complement Authorization

A remote connection crosses several gates. The hostname must resolve; the
network must reach the service; TLS must establish the intended protected
connection; authentication must succeed; and authorization must permit the
operation. Passing one gate does not establish that the remaining gates pass.

Atlas IP access lists, database users, TLS, PostgreSQL connection controls, and
platform network restrictions reduce who can reach a service. They do not replace
least-privilege database authorization.

For temporary classroom allow-list rules, use the narrowest practical scope and
remove them after the activity. An allow-from-anywhere rule may be convenient, but
it increases exposure and still requires strong credentials and database
permissions.

## Common Misconceptions

### "RLS is enabled, so the policy works"

Enablement and a policy definition are only configuration. Test the intended
client role, token claims, allowed rows, and denied rows.

### "The `authenticated` role identifies one person"

It represents a class of requests. Policies commonly use token claims such as the
user ID to distinguish rows.

### "A public client key is the same as a service-role key"

They have different powers and intended locations. Treat service credentials as
secrets and never expose them in client code.

### "More privileges will fix the error"

Broad grants may hide the actual problem and create a security defect. Identify
the actor, object, action, and expected policy first.

## Study and Practice

For Day 1, read through "Test Both an Allowed and a Denied Action" and the
limited-view worked example. For Day 2, read the Supabase identity, row-security,
and credential sections. The weekly labs contain complete practice setup and
cleanup. The matrix below is optional self-study, not another required file.

Choose one Metro Support actor. Write an access matrix with two allowed actions
and two denied actions. For each action, identify:

- the PostgreSQL object or API resource;
- the grant or policy layer involved;
- the exact test; and
- what the result would and would not prove.

## Retrieval and Transfer

1. How do authentication and authorization differ?
2. Why can a PostgreSQL group role use `NOLOGIN`?
3. Why should an access test include a denied action?
4. What is the difference between `USING` and `WITH CHECK` in RLS?
5. Why can the Supabase SQL editor be a misleading RLS test path?
6. What should happen first after a secret is committed to Git?

## Further Reading

- [PostgreSQL roles](https://www.postgresql.org/docs/current/user-manag.html)
- [PostgreSQL privileges](https://www.postgresql.org/docs/current/ddl-priv.html)
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [Supabase row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Supabase API security](https://supabase.com/docs/guides/api/securing-your-api)
