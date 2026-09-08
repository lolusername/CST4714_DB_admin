# Module 1: The Database Is a System of Responsibilities

## Operating Question

When someone says, "the database is down," what exactly might have failed, who
owns the response, and what evidence would help?

## Learning Outcomes

After this module, you can:

- distinguish data, a database, a DBMS, and a managed database platform;
- describe database work as a set of responsibilities rather than one job title;
- apply the shared-responsibility model to Supabase and MongoDB Atlas;
- identify evidence that makes an operation reproducible; and
- create a safe first technical artifact in GitHub.

## 1. Four Layers That People Call "the Database"

The word *database* is often used too loosely. Separate these layers when you
investigate a problem:

1. **Data** is the represented information: users, tickets, events, timestamps,
   and relationships.
2. **A database** is an organized collection of that data.
3. **A database management system**, or DBMS, is software that stores, queries,
   protects, coordinates, and recovers databases. PostgreSQL and MongoDB are
   DBMSs.
4. **A managed platform** runs a DBMS plus infrastructure and services. Supabase
   provides managed PostgreSQL with APIs and authentication features. Atlas
   provides managed MongoDB clusters, networking, and operational interfaces.

This distinction changes troubleshooting. A valid password can coexist with a
blocked network route. A healthy database server can contain a bad schema. A
successful query can return misleading results. "It works" is not one condition.

## 2. Database Work Is Broader Than a Job Title

A traditional database administrator may install servers, manage storage, create
accounts, monitor performance, test backups, and respond to incidents. Managed
cloud services move some of that work to a provider, but the responsibilities do
not disappear. They are redistributed.

Across database administration, backend development, data engineering, cloud
support, and security operations, the same practical verbs recur:

- **model** data so it represents the domain;
- **restrict** access to what each actor needs;
- **verify** that a change produced the intended state;
- **monitor** signals that reveal health or risk;
- **diagnose** a symptom using evidence;
- **recover** data and service after failure;
- **document** steps so another person can reproduce them; and
- **explain** a decision and its tradeoff.

This course treats those verbs as the profession. Product menus will change. The
reasoning remains useful.

## 3. Shared Responsibility in a Managed Service

In a self-managed PostgreSQL server, a team might own the operating system,
database process, storage, networking, upgrades, accounts, schemas, queries,
backups, and application behavior. A managed provider takes responsibility for
some infrastructure and software operations. The customer still owns important
choices.

For a Supabase or Atlas course project, the provider generally operates physical
infrastructure and much of the database service. You still own:

- account security and multi-factor authentication;
- project membership and privileges;
- network access rules;
- schema or document design;
- queries and indexes;
- application credentials and secret handling;
- data classification and appropriate use;
- logical backup or export work not included by the plan; and
- evidence that restoration and application behavior are correct.

The exact boundary depends on the product and plan. Read current documentation
before promising a capability. "Managed" means responsibility is shared, not
eliminated.

## 4. Evidence Is Part of the Operation

A workplace task is incomplete when only the operator knows what happened. Good
evidence answers five questions:

1. **Intent:** What state were you trying to create or investigate?
2. **Procedure:** What commands or interface actions did you use?
3. **Result:** What output or state appeared?
4. **Verification:** What independent check shows the result is correct?
5. **Tradeoff or next step:** What remains risky, costly, or unknown?

For example, a screenshot of "Success" is weak evidence. A SQL file, expected row
count, actual row count, and explanation of why the count should be eight is much
stronger. Text is searchable, diffable, and easier to reproduce.

## 5. GitHub as an Operations Notebook

Git records versions of files. GitHub hosts repositories and adds collaboration,
issues, web editing, and review. In this course, a repository is not mainly a
software product. It is an operations notebook containing SQL, JSON, Markdown,
and notebooks that another person can inspect.

### A Useful Artifact Pattern

```text
week-01/
  responsibility-map.md
week-02/
  queries.sql
  evidence.md
```

A Markdown evidence entry might look like this:

```markdown
## Check: dataset row count

Intent: confirm that setup loaded all supplied users.

Command: `SELECT count(*) FROM metro_support.users;`

Expected: 8, because the source CSV has one header and eight data rows.

Observed: 8.

Conclusion: the user import is complete, but this check does not prove that each
value is correct.
```

Notice the final limitation. Professional evidence avoids claiming more than the
test proves.

## 6. Protect Credentials From the Beginning

Never put these values in a repository, slide, screenshot, or submitted notebook:

- account passwords;
- database connection strings that contain passwords;
- API service-role keys;
- private keys or access tokens; or
- screenshots that reveal those values.

Enter secrets at runtime, store them in approved secret managers, and rotate a
secret immediately if it is exposed. A `.gitignore` file helps prevent accidental
commits, but it does not erase a secret already stored in Git history.

Use fictional or clearly synthetic data in class. The `example.test` email domain
in Metro Support is reserved for examples and cannot deliver real mail.

## Worked Example: Classify an Incident

**Report:** "The ticket dashboard spins for thirty seconds and then says it could
not load. A teammate says the cloud database is probably down."

Do not start with a conclusion. Divide the system:

| Layer | Question | Possible evidence |
|---|---|---|
| Browser/application | Did the request leave the client? | browser network status, application log |
| API/authentication | Was the request authenticated and authorized? | HTTP status, auth log, policy test |
| Network | Can the client reach the endpoint? | DNS result, connection error, allow-list settings |
| DBMS | Did the database receive or block the query? | activity view, database logs, query identifier |
| Query/data | Is the query slow or the result unexpectedly large? | SQL text, `EXPLAIN`, row counts |

The strongest first statement is not "the database is down." It is: "The user
sees a timeout; we do not yet know which layer caused it. I will collect a request
status, database activity, and a direct health check before assigning ownership."

## Common Misconceptions

### "Cloud means backups are automatic"

Backup availability depends on the service and plan. Free plans may not provide
automatic or point-in-time backups. Even when a snapshot exists, the customer
must know what it contains and how restoration will be verified.

### "The DBA owns every data problem"

Database work crosses application, infrastructure, security, and business
boundaries. Ownership should follow evidence and documented responsibility.

### "A screenshot proves reproducibility"

A screenshot may show a moment, but it rarely supplies executable steps or
expected output. Prefer text artifacts and use redacted screenshots only when the
interface state itself matters.

## Practice: Responsibility Map

For one action in Supabase or Atlas, write four lines:

1. provider responsibility;
2. student or customer responsibility;
3. evidence that the action succeeded; and
4. one secret or private value that must not appear in the evidence.

## Retrieval and Transfer

1. What is the difference between PostgreSQL and Supabase?
2. Name one responsibility a managed provider may handle and one the customer
   still handles.
3. Why is verification different from a successful command?
4. A connection fails after a password change. Name three layers you would test
   before declaring the database unavailable.

## Further Reading

- PostgreSQL: "What is PostgreSQL?" <https://www.postgresql.org/about/>
- Supabase architecture: <https://supabase.com/docs/guides/getting-started/architecture>
- MongoDB Atlas documentation: <https://www.mongodb.com/docs/atlas/>
- GitHub Skills: "Introduction to GitHub" <https://github.com/skills/introduction-to-github>
- O*NET Database Administrators: <https://www.onetonline.org/link/summary/15-1242.00>
