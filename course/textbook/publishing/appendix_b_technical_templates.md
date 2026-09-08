# Appendix B: Reusable Technical Templates {.unnumbered}

These templates turn a lab, project, or workplace exercise into a compact,
reviewable record. Replace brackets with observed facts. Do not submit secrets,
private URLs, addresses, tokens, or unredacted account images.

Use a template when it helps organize the work at hand. These are reference
tools, not a set of required forms. The weekly lab defines what to submit; use
the relevant ideas in that existing response rather than adding another report.

## Companion Materials {#companion-materials .unnumbered}

The textbook explains the examples; the accompanying course package supplies the
files used to run them. An EPUB reader cannot execute a Jupyter notebook or SQL
script. In the EPUB, links to these files lead to this index. Locate the named
file in the course materials supplied by your instructor, then open it in the
stated tool. The weekly guide identifies the assigned lab and its submission.

The Word and HTML versions link to those files within the complete course folder.
Keep that folder structure when moving the book. A Word or HTML file separated
from its companion package cannot supply the notebooks by itself.

| File or folder, relative to the course root | Use |
|---|---|
| `datasets/metro_support/postgres_setup.sql` | Full relational baseline: 8 users, 12 tickets, 21 events |
| `notebooks/01_relational_sql_review.ipynb` | SQL review and full-fixture practice |
| `notebooks/02_postgres_transactions_locks.ipynb` | Transaction and blocking experiment |
| `notebooks/03_postgres_backup_restore.ipynb` | PostgreSQL logical backup and separate restore |
| `notebooks/04_atlas_mql_modeling.ipynb` | MongoDB CRUD, arrays, and document-model practice |
| `notebooks/05_mongodb_logical_recovery.ipynb` | BSON-aware export and metadata recovery |
| `notebooks/06_public_data_capacity_integration.ipynb` | Inspect and import public data through a selected database path |
| `notebooks/07_aggregation_validation.ipynb` | Fresh four-ticket aggregation and validation case |
| `datasets/cisa_kev_sample/kev_sample.json` | Bounded, documented public-data snapshot |
| `weeks/week_06/lab_01_least_privilege.md` | Allowed and denied access tests |
| `weeks/week_07/performance_lab_setup.sql` | Disposable 100,000-row index experiment |
| `weeks/week_15/lab_01_github_concept_artifact.md` | Individual concept-guide assignment |

For a notebook, download the `.ipynb` file, open
[Google Colab](https://colab.research.google.com/), and choose **File > Upload
notebook**. Notebook Markdown cells explain installation, data, and cleanup.
SQL scripts run in the database environment named in the corresponding lab.
The `.md` files are readable assignment guides, not database commands.

## Query and Index Decision {.unnumbered}

**Question.** [State the user-visible or operational query in one sentence.]

**Expected grain.** [One row/document per what?]

**Baseline.** [Query text, representative parameters, result count, plan, timing
method, and environment.]

**Hypothesis.** [Name the predicate, join, sort, or access path that may explain
the observed work.]

**Controlled change.** [One query rewrite, statistic refresh, or index.]

**Verification.** [Same result meaning, comparable plan/run measurements, and write or
storage cost.]

**Decision.** [Keep, revise, or remove the change, with one limitation.]

## Access-Control Test Matrix {.unnumbered}

| Actor | Resource | Action | Expected | Observed result | Decision |
|---|---|---|---|---|---|
| `[role/user]` | `[schema.table or collection]` | `[read/write/admin]` | allow/deny | `[result or error class]` | `[correct/change needed]` |

Test at least one required success and one required denial. A role name or policy
definition alone does not establish effective access.

## Recovery Runbook Entry {.unnumbered}

1. **Failure and scope:** [deleted rows, damaged database, lost collection,
   account problem, region/service issue, or application corruption].
2. **Target promise:** [RPO and RTO, including assumptions].
3. **Artifact:** [type, creation command/process, timestamp, size, checksum,
   encryption, retention, and location category].
4. **Separate restore target:** [name and isolation boundary; never overwrite the
   source during a first test].
5. **Structure checks:** [schemas/collections, constraints/validators, indexes,
   roles/settings within scope].
6. **Data checks:** [counts, stable identifiers, relationships, aggregates].
7. **Behavior checks:** [one meaningful query and one expected rejection].
8. **Measured recovery:** [realized data-loss window and elapsed recovery time].
9. **Limitations:** [what the artifact and test do not cover].
10. **Cleanup:** [temporary target, credentials, access rules, and retained test
    record].

## Cloud Connection Diagnosis {.unnumbered}

Record only nonsecret facts.

| Layer | Safe question | Useful observation |
|---|---|---|
| service | Is the intended project/deployment active? | status label and capture date |
| network | Can this runtime reach the current endpoint? | error class, DNS result category, IPv4/IPv6 route category |
| TLS | Is a current client validating the expected service? | driver/client version and certificate mode; never a secret URI |
| identity | Is this a database credential rather than a website login? | redacted role/user label and authentication result |
| authorization | Does the identity have the required narrow action? | allowed and denied test results |
| object | Do the expected database, schema/collection, and table names exist? | metadata query or redacted tree |
| query | Does the filter use the intended types and values? | query plus known identifier/result |

Stop widening access when the observations point to another layer. Never normalize a
TLS error with `tlsInsecure=True`, publish a connection string, or leave a broad
temporary access rule in place after the exercise.

## Decision-Result-Tradeoff Paragraph {.unnumbered}

> **Decision:** [State one technical decision.] **Result:** [Name the observed
> result, comparison, or failure that supports it.] **Tradeoff:** [State the cost,
> limitation, or condition under which the decision should be revisited.]

This format is appropriate for a lab conclusion, final-project explanation,
portfolio README, or interview answer. It is stronger than a tool list because it
shows reasoning and scope.
