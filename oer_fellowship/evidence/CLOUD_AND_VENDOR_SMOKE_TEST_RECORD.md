# Cloud and Vendor Smoke-Test Record

## Purpose

This record separates checks that can be completed without an account from checks
that require a temporary Atlas, Supabase, Colab, GitHub, or MongoDB University
student context. It records exactly which bounded account-gated checks were
completed and which credentialed or student-role workflows remain untested.

- **Candidate:** *Operating Cloud Databases*, version `1.0.0-rc.1`, with
  second-edition textbook revision `2.0.0-draft`
- **Record updated:** August 26, 2026
- **Publication state:** local release candidate; not approved, tagged,
  deposited, or published

## Status Summary

| Surface | Account-free evidence completed | Account-gated evidence | Current state |
|---|---|---|---|
| Six notebooks | JSON parse, cell inventory, clean offline execution, no saved errors | Colab runtime and full live notebook routes | Offline path passed; full cloud notebook path remains pending |
| MongoDB Atlas | URI/TLS/network guidance and credential handling reviewed | Active Free project, access boundary, Data Explorer state, and backup-plan boundary inspected | Interface evidence passed; no reversible manual pause exposed; database-user connection/write path not run |
| Supabase/PostgreSQL | Connection-mode guidance and local PostgreSQL execution reviewed | Healthy Free project inspected; reversible temporary-table transaction run in SQL Editor | Focused live check passed; project paused afterward; remote Python notebook route remains pending |
| MongoDB University | Current titles and public URLs checked | Student enrollment, launch, completion, and score evidence | Not run |
| GitHub/Colab | Public links and no-secret instructions reviewed | Browser-editor workflow and Colab launch under a student account | Not run |

No instructor, student, reviewer, or vendor representative was contacted while
preparing this record. No account credentials were requested, created, copied,
or stored.

## Focused Live Cloud Check: August 25, 2026

This check used existing instructor-owned free-tier projects. It was intentionally
narrow: verify current interface claims, execute one reversible PostgreSQL
operation, capture publication-safe evidence, and leave no persistent teaching
data or credentials.

### MongoDB Atlas observations

- The Free deployment was resumed and displayed as active.
- The project overview separately warned that the current client address had not
  been added. This verifies the teaching distinction between service state and
  connection readiness.
- The overview displayed `0 B / 512 MB`; this is a data-size observation, not
  evidence of backup coverage.
- Data Explorer opened, but the interface still required a usable connection
  path. No database user or persistent credential was created for this audit.
- The Backup page offered paid continuous or daily backup upgrades rather than
  an active native backup for the Free deployment. The textbook therefore teaches
  a separate logical `mongodump`/`mongorestore` recovery path and does not imply
  that opening the Backup page proves an artifact exists.
- No collection, document, network rule, database user, or backup artifact was
  created.
- At cleanup, the deployment action menu exposed edit, tools, sample data, and
  `Terminate`, but not a reversible manual pause. The cluster was not terminated.
  It had zero active connections and the current client address remained
  disallowed. This record does not mislabel deletion as pausing.

### Supabase observations and reversible query

- The existing Free project reported `Healthy`, `Nano`, and `No backups`.
- The public schema contained no tables at the time of inspection.
- In SQL Editor, the following temporary, transactional check was run:

```sql
BEGIN;
CREATE TEMP TABLE oer_validation (
    ticket_id integer PRIMARY KEY
);
INSERT INTO oer_validation VALUES (1001);
ROLLBACK;

SELECT to_regclass('pg_temp.oer_validation') IS NULL
    AS rollback_verified;
```

- The result was `rollback_verified = true`.
- The editor displayed a heuristic row-level-security warning because it saw
  `CREATE TABLE`; the table was temporary, existed only inside the session, and
  was removed by rollback. The warning was interpreted rather than ignored as a
  universal rule.
- No persistent schema, table, row, policy, credential, or application key was
  created or copied.
- After evidence capture, the project was paused through Project Settings. The
  dashboard subsequently displayed `Resume project`, verifying the reversible
  shutdown completed.

### Screenshot handling

- Six interface captures were retained as teaching evidence: Atlas overview,
  Data Explorer, Free backup boundary, Supabase overview, empty Table Editor, and
  rollback verification.
- Organization, project, deployment, URL, and account identifiers were covered
  before the images entered the textbook or fellowship showcase.
- Each textbook figure includes nearby interpretation, a dated interface-change
  caveat, and a text alternative. Screenshots supplement the concept; they are
  not the sole path to the learning outcome.

## Completed Local Evidence

### Notebook execution

- All six notebooks parsed as valid notebook JSON.
- All 68 code cells re-executed through the documented offline paths in clean
  temporary copies on August 10, 2026 after the cloud connection-safety update.
- The executed copies produced zero error outputs.
- Course notebooks were not overwritten with temporary execution output.
- The canonical builder and checked notebooks match exactly at the cell-source
  level.
- Connection cells obtain secrets at runtime rather than embedding them.
- MongoDB examples do not normalize certificate errors with `tlsInsecure=True`.
- Supabase guidance distinguishes direct, session-pooler, and transaction-pooler
  connections and identifies the IPv4-compatible session-pooler route.
- Cloud notebook contracts default to disabled, request secrets through
  `getpass`, bound connection/operation waits, and require explicit encrypted
  PostgreSQL transport. The text distinguishes `sslmode=require` encryption from
  `verify-full` certificate and hostname verification.
- Atlas notebook contracts use Stable API version 1, bounded server-selection and
  operation timeouts, an explicit ping, and client cleanup.

### PostgreSQL fixtures

- `datasets/metro_support/postgres_setup.sql` executed in a disposable local
  PostgreSQL database.
- Verified fixture counts were 8 users, 12 tickets, and 21 ticket events.
- `course/weeks/week_07/performance_lab_setup.sql` created 100,000 rows, including 2,000 open
  rows used by the performance experiment.
- The Metro Support fixture contained zero orphan tickets.
- The disposable QA database was dropped after verification.

### Static safety checks

- The public package contains no saved connection URI, password, access token,
  private host, Atlas project identifier, Supabase project identifier, or student
  account detail.
- Destructive examples use disposable course data, narrow filters, preview or
  prediction steps, and reset/rollback guidance.
- Cloud-dependent outcomes have an offline, static, or simulated route targeting
  the same concept.
- Screenshots are not required as the sole evidence of technical behavior.

## Live Test Protocol: MongoDB Atlas

Run this only with a disposable free deployment and temporary course user. Do not
paste the URI into a notebook cell that will be saved.

1. Create or reset a temporary Atlas database user with the narrowest useful
   role for the exercise.
2. Add only the current runtime address as a temporary `/32` network entry.
3. Launch notebook 04 or 05 from the repository's Colab link.
4. Enter the `mongodb+srv://` URI through the runtime prompt.
5. Run `client.admin.command("ping")` without disabling TLS verification.
6. Create the named disposable database and collection.
7. Insert the small course fixture, then verify count, one stable identifier,
   and one meaningful query.
8. Exercise the notebook's update, validation, export, or restore path as
   applicable.
9. Rerun the safe load or write step and confirm its documented repeat behavior.
10. Drop the disposable database, remove the temporary user if no longer needed,
    and remove the temporary network entry.

### Atlas evidence to record

| Field | Result |
|---|---|
| Date, notebook, and commit | August 25, 2026; interface-only focused check; no notebook/commit claim |
| Runtime and Python/PyMongo versions | NOT RUN |
| Atlas deployment type and MongoDB major version | Free deployment observed; server major version not queried |
| Ping result | NOT RUN |
| Count, stable identifier, and meaningful query | NOT RUN |
| Rerun/idempotency result | NOT RUN |
| Cleanup confirmed | No database objects, credentials, users, or network rules created |
| Limitation or required revision | Full credentialed ping/read/write/notebook path remains pending |

## Live Test Protocol: Supabase/PostgreSQL

Run this only with a disposable project or disposable schema. Use the dashboard's
current connection panel rather than copying an old hostname from course notes.

1. Create a disposable schema or project and record the PostgreSQL server major
   version.
2. Choose the connection route that matches the runtime: direct connection when
   IPv6 works, session pooler for a persistent IPv4-compatible client, or
   transaction pooler only for a transient/serverless pattern that does not
   require prepared statements.
3. Enter the connection string through the runtime prompt; do not print it.
4. Prefer `sslmode=verify-full` with the current Supabase CA certificate. If the
   classroom route uses `sslmode=require`, record that it encrypts traffic but
   does not validate the CA or hostname; never use `disable`, `allow`, or the
   fallback-capable default `prefer`.
5. Create or load the small course fixture into the disposable schema.
6. Verify table names, row counts, one stable identifier, one relationship, and
   one meaningful query.
7. Rerun the import or upsert and verify the documented repeat behavior.
8. If the exercise concerns authorization, test one intended success and one
   intended denial through the intended client identity rather than only as an
   owner or administrative role.
9. Drop the disposable schema or project artifacts and remove temporary secrets.

### Supabase evidence to record

| Field | Result |
|---|---|
| Date, notebook, and commit | August 25, 2026; dashboard SQL Editor focused check; no notebook/commit claim |
| Runtime and Psycopg/SQLAlchemy versions | NOT RUN |
| PostgreSQL version | NOT RUN |
| Connection mode and reason | Supabase dashboard SQL Editor; avoided copying a credential for this focused check |
| Connection result | SQL executed successfully in the existing project |
| Count, stable identifier, relationship, and query | Temporary row `1001`; rollback check returned `true`; relationship check not in scope |
| Rerun/idempotency result | NOT RUN |
| Intended allow/deny result, if applicable | NOT RUN |
| Cleanup confirmed | Transaction rollback removed the temporary table; no persistent object created; project paused and `Resume project` displayed |
| Limitation or required revision | Remote Python/Colab connection and full fixture path remain pending |

## Student-Role Vendor Activity Check

Each check uses a fresh or representative student account and records only
course-level observations. Do not retain a learner's name, email address, score,
or account identifier in this public file.

| Week | Activity | Role in course | Student-role result |
|---|---|---|---|
| 9 | Getting Started with MongoDB Atlas | optional setup support | NOT RUN |
| 9 | MongoDB and the Document Model | optional setup/concept support | NOT RUN |
| 10 | Modeling Data Relationships | instructor live demonstration | NOT RUN |
| 10 | Relational (SQL) to Document Model | individual assigned activity | NOT RUN |
| 11 | Improving Performance of Sort Stages - Lab Only | individual assigned activity | NOT RUN |
| 12 | MongoDB Atlas Backup and Recovery | optional reliability support | NOT RUN |

For each activity, verify that the link opens, free enrollment remains available,
the title and learning role still match the weekly guide, keyboard operation is
reasonable, completion evidence can be redacted, and the open course fallback
still teaches the same outcome if the vendor activity changes.

## Release Decision

The completed local and focused live evidence is sufficient for a locally
reviewable release candidate and for the specific interface and rollback claims
recorded above. It is not sufficient to claim a complete live Atlas notebook
route, a complete remote Supabase Python route, or a verified student-role vendor
experience. Those broader claims remain withheld until the corresponding tests
contain dated evidence.
