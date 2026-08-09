# Technical Setup and Troubleshooting Guide

## Purpose

This guide prepares a zero-cost, beginner-friendly environment for PostgreSQL,
MongoDB, GitHub, Python notebooks, and offline equivalents. Platform interfaces
and free plans change. Verify every linked provider instruction before a new
course release; do not turn a paid feature or trial into a student requirement.

## Instructor Readiness Check

Before the term:

1. Run all six notebooks from a clean runtime using their default offline paths.
2. Test one current Supabase Free PostgreSQL connection from the campus network.
3. Test one current Atlas Free connection from the campus network and Colab.
4. Confirm the selected MongoDB University activities remain free and distinct
   from instructor live demonstrations.
5. Test the GitHub web editor without local Git.
6. Confirm `pg_dump` and `pg_restore` client versions are compatible with the
   PostgreSQL server used in the recovery demonstration.
7. Open every cloud-dependent lab's local or static fallback.
8. Search all public files and notebook outputs for credentials and student data.

Record the check date and any temporary platform-specific correction in a release
note rather than silently changing a conceptual instruction.

## Minimum Student Environment

Students need a modern browser and an institutional or personal email address.
The normal path uses free GitHub, Supabase, MongoDB Atlas, and Colab accounts. A
student who cannot use an account must be able to complete equivalent evidence
with course files, SQLite or DuckDB, `mongomock`, a local PostgreSQL service, or
static incident evidence.

No activity should require:

- a payment card;
- a paid cloud tier;
- a commercial textbook;
- a local administrator account;
- a permanent `0.0.0.0/0` network rule;
- disabling TLS verification; or
- sharing a password or private connection string with the instructor.

## GitHub Without a Local Installation

The browser path is sufficient for early text, SQL, JSON, and README artifacts.

1. Open a repository and navigate to the target directory.
2. Use **Add file** and **Create new file**, or open a file and choose **Edit**.
3. Enter a descriptive file name with the correct extension.
4. Preview Markdown when relevant.
5. Commit with a short message describing the change.
6. Reopen the rendered or raw file and verify that the expected content exists.

Never commit `.env` files, database URLs, access tokens, downloaded credential
files, or unredacted cloud account images. A browser edit is still a publication
action when the repository is public.

## Colab and Local Jupyter

Every course notebook has an **Open in Colab** badge and remains downloadable for
local Jupyter. Students should run cells from top to bottom after a runtime reset.

If a package import fails:

1. rerun the package-install cell once;
2. restart the runtime if the install requests it;
3. run from the first cell again;
4. inspect the first error rather than repeatedly running later cells; and
5. use the documented offline path if the cloud or network remains unavailable.

Cloud credentials are entered with `getpass`. A credential should not appear in
cell source, ordinary output, a screenshot, browser history, or repository
history. Restarting a Colab runtime removes in-memory variables but does not erase
values already saved into the notebook.

## Supabase and PostgreSQL Connection Path

Treat Supabase as a managed service around PostgreSQL, not as a different SQL
language. The provider manages infrastructure; the course user still owns schema,
queries, roles/policies, secrets, logical recovery evidence, and application
behavior.

Choose the connection mode for the client instead of treating every Supabase URL
as interchangeable. As verified August 8, 2026:

- the direct database endpoint on port 5432 uses IPv6 and suits migrations,
  `pg_dump`, and long-lived backend connections when the network supports it;
- the shared Supavisor session endpoint on port 5432 supplies an IPv4-compatible
  persistent-client path; and
- the shared Supavisor transaction endpoint on port 6543 suits short-lived or
  serverless traffic but does not support prepared statements or session state.

If campus or Colab cannot reach the direct IPv6 endpoint, use the current session
pooler for notebooks and native tools. Do not route `pg_dump`, migrations, or
session-dependent lessons through transaction pooling, weaken TLS, or rewrite
unrelated SQL to hide a network mismatch.

Minimal Psycopg test:

```python
from getpass import getpass
import psycopg

database_url = getpass("PostgreSQL connection URL: ")
with psycopg.connect(database_url, connect_timeout=15) as connection:
    with connection.cursor() as cursor:
        cursor.execute("select current_database(), current_user")
        print(cursor.fetchone())
```

### PostgreSQL Connection Checklist

Inspect in this order:

1. correct provider project and current connection URL;
2. correct password and URL encoding of reserved characters;
3. project is active rather than paused or deleted;
4. direct versus pooler endpoint matches the network path;
5. required TLS mode is present in the current connection guidance;
6. client package is current;
7. schema/table exists in the database named by the URL; and
8. role has the required permission.

Do not print the URL to debug it. Print nonsecret facts such as database name,
current user, or a redacted host label.

### Common PostgreSQL Symptoms

| Symptom | Inspect first | Avoid |
|---|---|---|
| network unreachable with an IPv6 address | current IPv4-compatible pooler option and campus IPv6 support | disabling TLS |
| password authentication failed | current database password, username format, and URL encoding | sharing the URL publicly |
| relation does not exist | database, schema, `search_path`, capitalization, and setup cell | recreating random tables |
| permission denied | current role, grant, ownership, and RLS context | switching every user to administrator |
| transaction aborted | first error in the transaction, then `ROLLBACK` | rerunning later commands in the failed transaction |
| dump version mismatch | server major version and selected client binary | using an older client blindly |

## MongoDB Atlas Connection Path

Atlas requires three separate ideas:

- an Atlas account/project and active free deployment;
- a database user with a username and password; and
- network access that permits the current client path.

Those controls are not interchangeable. A website login is not a database user,
and a database password does not add an IP address to network access.

As verified August 8, 2026, Atlas Free uses MongoDB 8.0 on a fixed three-node
replica set with 0.5 GB storage. It does not provide native backup, sharding,
primary-failover testing, aggregation disk spill, or Performance Advisor. Current
instructional boundaries include 500 connections, 100 operations per second, 50
aggregation stages, and a 32 MB in-memory sort limit. Treat those as changing
Free-tier limits, not production design recommendations.

Minimal PyMongo test:

```python
from getpass import getpass
from pymongo import MongoClient

mongodb_uri = getpass("Atlas connection URI: ")
client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=15000)
client.admin.command("ping")
print("Connected to Atlas")
client.close()
```

### Atlas Connection Checklist

Inspect in this order:

1. copy the current `mongodb+srv://` URI from the intended deployment;
2. replace placeholders and URL-encode reserved password characters;
3. confirm the deployment is available;
4. confirm the database user exists and has only the needed role;
5. add only the temporary network access needed for the current runtime, using a
   single-address `/32` rule instead of an all-address rule when feasible;
6. use a current supported PyMongo version;
7. verify DNS/SRV resolution, system date/time, and TLS support; and
8. run `ping` before creating course data.

Do not use `tlsInsecure=True` as a routine fix. It disables certificate
verification and can conceal a wrong host, interception, old client, DNS issue,
clock problem, or unsupported network path. Diagnose the cause or use the offline
path.

### Common Atlas Symptoms

| Symptom | Inspect first | Avoid |
|---|---|---|
| server selection timeout | URI, network access, deployment state, DNS, and current driver | repeatedly widening network access |
| TLS handshake failure | current URI/driver, system clock, DNS, network inspection, supported runtime | `tlsInsecure=True` |
| authentication failed | database user, password encoding, and authentication source in current URI | using the Atlas website password |
| no documents returned | database/collection names, filter types, and seed cell | inserting duplicates until something appears |
| operation not permitted | database-user role and free-tier feature support | granting broad administrative roles |

Remove temporary broad network access after class. A lab may record that the rule
was narrowed or removed, but it must not publish account identifiers or IP data.

## Logical Backup and Tool Compatibility

The course uses logical backup and restore because free-tier native backup
features may be limited. A successful command is only artifact creation; recovery
requires a separate target and verification.

For PostgreSQL:

- identify the server major version;
- choose a compatible `pg_dump`/`pg_restore` client;
- record command, exit status, artifact size, and checksum;
- restore into a different database; and
- verify structure, counts/identity, relationships, constraints, and a meaningful
  query.

For MongoDB:

- distinguish document export from BSON-aware Database Tools;
- record how BSON types are preserved;
- identify which indexes, validators, users, and managed settings travel or do
  not travel in the selected method; and
- restore to a separate database and test behavior.

## Platform-Outage Fallback Rule

When more than a small minority of the class is blocked by a platform or network,
stop treating repeated setup attempts as learning. Switch to the equivalent open
path and record the failure separately from conceptual performance.

Equivalent evidence must preserve the operating question. For example:

- a static lock transcript can still support blocker/waiter diagnosis;
- `mongomock` can support MQL shape and update reasoning while explicitly not
  claiming server validation or explain behavior;
- SQLite can support idempotent import and verification while the class compares
  its local boundary with managed PostgreSQL; and
- a versioned JSON fixture can support data-quality and model decisions during a
  feed outage.

## End-of-Class Safety Check

- Cloud URIs and passwords are absent from source and output.
- Temporary broad network access is removed or narrowed.
- Disposable course databases have unique names.
- No student used a shared instructor credential.
- Expected evidence was saved before a temporary runtime closed.
- Platform errors are recorded separately from conceptual errors.
