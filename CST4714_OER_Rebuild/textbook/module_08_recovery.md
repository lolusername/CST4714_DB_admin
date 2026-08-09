# Module 8: A Backup Matters Only When Recovery Works

## Operating Question

If the original database disappears or a harmful change commits, what artifact can
recreate the required state, where can it be restored safely, and what evidence
proves the result is usable?

## Learning Outcomes

After this module, you can:

- distinguish high availability, backup, restore, and disaster recovery;
- use recovery point and recovery time objectives to clarify a promise;
- explain logical and physical backup tradeoffs;
- create a free-tier-appropriate PostgreSQL logical backup command;
- restore into a separate target and verify structure, data, and behavior; and
- write a concise runbook with prerequisites, safety boundaries, and evidence.

## 1. Four Mechanisms Solve Different Problems

- **High availability** reduces service interruption when a component fails.
- **Backup** creates recoverable data outside the active state.
- **Restore** reconstructs data or objects from a backup artifact.
- **Disaster recovery** combines people, systems, procedures, alternate locations,
  and tested decisions for a serious failure.

A replica can quickly copy an accidental deletion. A backup can exist but be
corrupt, incomplete, inaccessible, or impossible to restore within the required
time. Redundancy and recovery complement each other.

## 2. RPO and RTO Turn "We Have Backups" Into a Promise

**Recovery Point Objective (RPO)** is the maximum acceptable data-loss window. A
daily export may imply up to roughly one day of lost changes, depending on when
failure occurs.

**Recovery Time Objective (RTO)** is the target time to restore an acceptable
service. It includes obtaining credentials, provisioning a target, transferring
data, restoring, verifying, and reconnecting consumers.

RPO and RTO are requirements, not properties automatically created by writing
them down. Backup frequency, artifact retention, restore speed, and staffing must
support them.

## 3. Choose the Failure Scope First

Ask what must be recovered:

- one table after an incorrect delete;
- one schema after a migration failure;
- an entire database after project loss;
- credentials and permissions after access corruption;
- a service in a different region; or
- an application-consistent state spanning multiple systems.

The correct artifact and procedure depend on scope. A CSV export of one table may
help recover rows but does not preserve keys, constraints, indexes, views,
functions, roles, or transactionally consistent relationships by itself.

## 4. Logical and Physical Backups

### Logical Backup

Logical tools export SQL objects and data in a form the DBMS can reconstruct.
PostgreSQL uses `pg_dump` for one database and `pg_dumpall` for cluster-wide
logical content such as roles, within supported permissions.

Benefits include object-level selection and portability across some PostgreSQL
versions. Costs can include longer export/restore time and incomplete coverage of
cluster-level configuration.

### Physical Backup

Physical backups copy database storage in a format tied more closely to the DBMS
and version, often combined with write-ahead logs for point-in-time recovery. They
can support large-system recovery and precise points but require platform support,
storage coordination, and operational expertise.

Managed services may expose snapshots or point-in-time recovery only on selected
plans. Confirm the exact plan; do not teach a paid dashboard feature as though
every student has it.

## 5. Free-Tier Reality in This Course

Supabase documentation states that projects on the Free plan do not receive the
automatic database backups available on paid plans. This course therefore treats
logical backup and restore as the required recovery path. Students never need to
pay for a backup feature.

Platform offerings change. Check the current plan documentation before class and
record the verification date in the release manifest.

## 6. Use `pg_dump` Without Publishing a Password

Obtain a current PostgreSQL connection string from the approved platform path.
Supabase offers direct and pooled connection options; network environments may
need an IPv4-compatible pooler. Use the provider's current connection guidance.

Custom-format database backup:

```bash
pg_dump \
  --format=custom \
  --no-owner \
  --no-privileges \
  --file=metro_support.dump \
  "$DATABASE_URL"
```

Plain SQL backup of one schema:

```bash
pg_dump \
  --format=plain \
  --schema=metro_support \
  --no-owner \
  --no-privileges \
  --file=metro_support.sql \
  "$DATABASE_URL"
```

Store the URL in a runtime environment variable or supported password file, not a
committed script. Avoid putting a secret directly on a shared command line or in
shell history.

`--no-owner` and `--no-privileges` improve portability when the restore target
does not have the same roles. They also omit ownership and grant evidence, so
recovery of security configuration may require a separate, reviewed script.

## 7. Inspect the Artifact Before Depending on It

For a custom-format dump:

```bash
pg_restore --list metro_support.dump
```

For a plain SQL file, inspect its beginning and end with a text viewer and search
for expected table and data statements. Record file size and a cryptographic hash
if the artifact will be transferred or retained:

```bash
shasum -a 256 metro_support.dump
```

A list or checksum proves properties of the artifact, not that PostgreSQL can
successfully restore it.

Treat an untrusted dump as executable input. Current PostgreSQL documentation
warns that restoring a dump can execute SQL selected by source superusers. Inspect
the source and archive list, restore first into an isolated disposable target with
a least-privileged restore role, and never test an untrusted artifact directly
against production.

## 8. Restore Into a Separate Target

Never test by overwriting the only copy. Create an empty, disposable database or
instructor-approved restore target.

Custom format:

```bash
pg_restore \
  --dbname="$RESTORE_DATABASE_URL" \
  --no-owner \
  --no-privileges \
  --exit-on-error \
  metro_support.dump
```

Plain SQL:

```bash
psql \
  --set=ON_ERROR_STOP=on \
  --dbname="$RESTORE_DATABASE_URL" \
  --file=metro_support.sql
```

`--exit-on-error` and `ON_ERROR_STOP` make failures visible rather than allowing a
long process to appear successful after skipped errors.

## 9. Verify Structure, Data, and Behavior

### Structure

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'metro_support'
ORDER BY table_name;
```

Inspect expected constraints and indexes as well as tables.

### Data

```sql
SELECT 'users' AS object, count(*) FROM metro_support.users
UNION ALL
SELECT 'tickets', count(*) FROM metro_support.tickets
UNION ALL
SELECT 'ticket_events', count(*) FROM metro_support.ticket_events;
```

Counts are necessary but not sufficient. Check a known relationship and a
boundary row.

### Behavior

Run one meaningful report and one expected-failure constraint test inside a
transaction. If access configuration is part of the recovery scope, test an
allowed and denied operation.

### Application Boundary

If the recovery objective includes application service, use a temporary safe
configuration to test a real read and write path. Do not redirect production
traffic before verification and approval.

## Worked Example: A Recovery Runbook Entry

```text
Purpose: recover the Metro Support schema after an accidental destructive change.

Artifact: custom-format logical dump, created daily by an approved operator.

Prerequisites: pg_dump/pg_restore major version compatible with the server;
temporary source and restore credentials; empty restore target; enough storage.

Safety boundary: never restore over the source database. Never commit URLs.

Procedure: create dump; record exit code, size, and SHA-256; list contents;
restore with --exit-on-error into the separate target.

Verification: confirm 3 tables; expected row counts; foreign-key relationships;
status constraint; one active-ticket report; one denied analyst action.

Success decision: all required checks pass and the reviewer signs the log.

Cleanup: revoke temporary credentials and remove the restore target according to
the retention policy.
```

## 10. Safe Migrations and Recovery Are Connected

A backup before a migration is useful only if:

- it includes the necessary scope;
- it can be restored within the decision window;
- the old application remains compatible with the restored state; and
- the team knows whether rollback, forward fix, or restore is safest.

For small changes, transactional DDL and a tested rollback may be faster. For a
destructive data transformation, restore may be part of the response. Plan before
execution.

## Common Misconceptions

### "The dump command returned, so recovery is ready"

Exit status, artifact inspection, separate restore, and verification are still
required.

### "A CSV is a full database backup"

CSV can preserve selected row values but usually omits schema, constraints,
indexes, permissions, and transactionally consistent multi-table state.

### "A replica protects against deletion"

Replication can reproduce the deletion. Recovery needs an artifact or history
outside the active state and a tested procedure.

### "RPO and RTO are the same"

RPO concerns acceptable data loss; RTO concerns acceptable recovery duration.

## Practice

Write a restore verification checklist for Metro Support with:

1. two structure checks;
2. two data checks;
3. one behavior check;
4. one access check; and
5. one statement of what the checklist does not prove.

## Retrieval and Transfer

1. How does high availability differ from backup?
2. What does an RPO of four hours mean?
3. Why restore into a separate target?
4. What do `--no-owner` and `--no-privileges` trade away?
5. Why is a row count not complete restore verification?
6. Which free-tier constraint changes the required Supabase recovery lab?

## Further Reading

- PostgreSQL backup and restore: <https://www.postgresql.org/docs/current/backup.html>
- PostgreSQL `pg_dump`: <https://www.postgresql.org/docs/current/app-pgdump.html>
- PostgreSQL `pg_restore`: <https://www.postgresql.org/docs/current/app-pgrestore.html>
- Supabase database backups: <https://supabase.com/docs/guides/platform/backups>
- Supabase connection guidance: <https://supabase.com/docs/guides/database/connecting-to-postgres>
