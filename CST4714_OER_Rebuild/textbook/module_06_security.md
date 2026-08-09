# Module 6: Access Should Be Useful and Limited

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

## 1. Security Questions Need Separate Terms

- **Identity:** who or what claims to be acting?
- **Authentication:** how is that claim verified?
- **Authorization:** what may the authenticated actor do?
- **Auditing:** what evidence records relevant actions and decisions?

A valid password proves authentication only within its mechanism. It does not mean
the account should read every row. A failed query may reflect authentication,
authorization, network access, an object name, or SQL syntax. Classify the failure
before changing permissions.

## 2. Model Access as Actor, Action, Resource, and Condition

Replace "give the app access" with a testable statement:

| Actor | Action | Resource | Condition |
|---|---|---|---|
| support agent | `SELECT`, `UPDATE` | assigned tickets | only rows assigned to that agent |
| resident | `SELECT` | tickets | only tickets requested by that resident |
| analyst | `SELECT` | reporting view | no private internal notes |
| migration process | schema changes | application schema | only during controlled deployment |

This matrix reveals different layers. A table grant may permit `SELECT` on the
table, while RLS limits which rows the statement can return.

## 3. PostgreSQL Roles Represent Users and Groups

PostgreSQL uses roles for both login identities and privilege groups.

```sql
CREATE ROLE metro_analyst NOLOGIN;
CREATE ROLE analyst_login LOGIN PASSWORD 'replace-at-runtime';

GRANT metro_analyst TO analyst_login;
```

Do not put a literal password in a committed file. Create the login interactively
or use a secret mechanism approved for the environment. In shared cloud platforms,
you may not have permission to create unrestricted login roles; follow the
provider's supported model.

A group role with `NOLOGIN` collects privileges. Login roles become members. This
separates identity lifecycle from permission definition.

## 4. Grant the Minimum Required Privileges

PostgreSQL privileges are object-specific. Accessing a table in a schema can
require both schema `USAGE` and table privileges.

```sql
GRANT USAGE ON SCHEMA metro_support TO metro_analyst;
GRANT SELECT ON metro_support.active_ticket_queue TO metro_analyst;
```

If the analyst should read only the view, do not also grant broad access to every
base table. Review view security behavior and ownership for the PostgreSQL version
and use case.

Revoke privileges that were granted too broadly:

```sql
REVOKE UPDATE, DELETE
ON metro_support.tickets
FROM metro_analyst;
```

Privileges on future tables are separate from current objects. Default privileges
can automate future grants, but they are defined by the object-creating role and
must be tested.

## 5. Test Both an Allowed and a Denied Action

An allow-only test is incomplete. In a dedicated practice environment:

```sql
SET ROLE metro_analyst;

SELECT *
FROM metro_support.active_ticket_queue;

-- This should fail if no base-table update privilege was granted.
UPDATE metro_support.tickets
SET priority = 'urgent'
WHERE ticket_id = 1001;

RESET ROLE;
```

An expected permission error is positive evidence. Record the actor, action,
object, expected outcome, and observed outcome. Do not "fix" the denied action by
granting more access if denial is the intended policy.

## 6. Supabase Adds an Identity Layer to PostgreSQL

Supabase Auth can issue JSON Web Tokens for application users. Requests through
Supabase's data APIs are mapped to PostgreSQL roles such as `anon` or
`authenticated`, and claims can be read by policy helpers such as `auth.uid()`.

This creates distinct concepts:

- a Supabase dashboard account administers a project;
- a PostgreSQL role controls database privileges;
- an application user exists in the authentication system;
- a token carries claims about a request; and
- an RLS policy evaluates row access inside PostgreSQL.

Do not treat these identities as interchangeable.

The Supabase SQL editor commonly runs with elevated ownership privileges. Table
owners and roles with `BYPASSRLS` can bypass row-level security. A successful query
in the editor therefore does not prove what an anonymous or authenticated client
can see.

## 7. Row-Level Security Adds a Row Predicate

Suppose each ticket stores the requesting application user's UUID in a column
named `requester_auth_id`.

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
reasons, the evidence supports the stated boundary. It does not prove protection
against a privileged administrator, a leaked credential, a vulnerable function,
or an untested API path.

## 8. Secret Handling Is a Database Skill

A connection URI may include host, database, user, and password. Treat the whole
string as a secret when it contains credentials.

Safe notebook pattern:

```python
from getpass import getpass

database_url = getpass("Paste the temporary database URL: ")
```

Do not hardcode a secret, print it, save it in notebook output, or place it in a
GitHub issue. Use environment variables or platform secret storage in applications.

Supabase's `service_role` key is powerful and bypasses RLS in normal server-side
use. Never expose it in browser code. Use public client keys only for their
documented purpose and rely on correctly tested policies.

If a secret reaches Git history, revoke or rotate it first. Removing the visible
line does not make the old credential safe.

## 9. Network Controls Complement Authorization

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

## Practice

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

- PostgreSQL roles: <https://www.postgresql.org/docs/current/user-manag.html>
- PostgreSQL privileges: <https://www.postgresql.org/docs/current/ddl-priv.html>
- PostgreSQL row security: <https://www.postgresql.org/docs/current/ddl-rowsecurity.html>
- Supabase row-level security: <https://supabase.com/docs/guides/database/postgres/row-level-security>
- Supabase API security: <https://supabase.com/docs/guides/api/securing-your-api>
