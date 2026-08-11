# Currentness, Pedagogy, and Quality-Assurance Audit

> **Document type:** fellowship evidence and release-control record, not student
> course content and not a claim of external approval.

- **Audit date:** August 10, 2026
- **Candidate:** *Operating Cloud Databases*, `1.0.0-rc.1` source package
- **Review boundary:** locally controllable research, content review, build
  checks, and automated or direct inspection. Classroom piloting, OER-team
  approval, institutional deposit, and human assistive-technology review remain
  external gates.

## 1. Audit Method

The review uses four evidence types:

1. current primary technical documentation and standards for product behavior;
2. peer-reviewed or consensus research for learning-design decisions;
3. executable course fixtures, notebooks, and validators for technical claims;
4. direct inspection of student-facing files, slides, notes, transcripts, and
   publication exports.

Current product facts are separated from durable concepts. PostgreSQL, Supabase,
MongoDB, Atlas, MongoDB University, GitHub, and Colab links must be rechecked at
every release because versions, interfaces, limits, and account rules change.

Account-gated or privately visible material may inform factual understanding, but
protected wording, screenshots, quiz questions, answer keys, and proprietary
examples are not copied into the OER. Original explanations are checked against a
public primary source whenever one exists. Vendor activities remain linked free
external resources unless their page supplies a compatible open license.

## 2. Learning-Design Evidence

| Design decision in this course | Research basis | Course implementation |
|---|---|---|
| Replace long lecture blocks with frequent disciplinary action | [Freeman et al. (2014)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4060654/) found improved STEM performance under active learning; the [National Academies (2025)](https://doi.org/10.17226/28268) identifies active engagement as a principle of equitable and effective undergraduate STEM teaching | every meeting moves from retrieval and prediction to a worked example, individual practice, evidence, and interpretation |
| Retrieve prior knowledge before adding new complexity | [Karpicke and Blunt (2011)](https://pubmed.ncbi.nlm.nih.gov/21252317/) found retrieval practice supported meaningful science learning | weekly self-checks and the 15-set retrieval/exit bank repeatedly revisit relational grain, verification, security, and recovery |
| Give novices complete examples, then fade support | [Vieira, Yan, and Magana (2015)](https://doi.org/10.22369/issn.2153-4136/6/1/1) reports benefits from programming worked examples and elaborated self-explanation for novices | the implementation guide uses Model, Fade, and Build phases; early labs provide commands while later labs provide symptoms or operating promises |
| Use short formative evidence to decide what happens next | [Morris et al. (2021)](https://eric.ed.gov/?id=EJ1319705) reviews causal evidence for formative assessment and feedback in higher education; the National Academies emphasizes multiple forms of data for improvement | one compact artifact, one interpretation, retrieval prompts, and exit evidence feed the public data-informed teaching protocol |
| Provide equivalent ways to access meaning and show learning | [CAST UDL Guidelines 3.0 (2024)](https://udlguidelines.cast.org/) addresses engagement, representation, and action/expression barriers | Markdown, slides, transcripts, PDF handouts, notebooks, static evidence, local fallbacks, and non-screenshot alternatives preserve the same outcome |
| Use authentic records without exposing private people | Research on classroom use of real-world data identifies realism and storytelling benefits while warning about privacy and release risk ([Luse and Burkman, 2018](https://aisel.aisnet.org/jmwais/vol2018/iss1/2/)) | two synthetic operational cases support safe repetition; a documented, field-reduced CISA KEV snapshot adds real public-data provenance and ambiguity |
| Make technical reasoning visible in workplace language | [NACE career-readiness competencies](https://www.naceweb.org/career-readiness/competencies/career-readiness-defined) emphasize critical thinking, communication, professionalism, and technology | claim-evidence-tradeoff writing, incident updates, reproducible artifacts, resume bullets, and bounded STAR-R stories use evidence without inflating experience |

The course does not use group work as a prerequisite for active learning. Students
may discuss publicly, but each graded artifact is individual. This preserves
accountability and avoids making class progress depend on group formation.

## 3. Current Technical Reference Baseline

The following matrix records the primary source used to check each module's most
change-sensitive claims. "Verified" means the authored explanation is consistent
with the cited source on the audit date; it does not mean the external platform
was operated under a live student account.

| Week | Claims checked | Primary evidence | Result or bounded update |
|---:|---|---|---|
| 1 | managed-service responsibility, evidence boundaries, credential safety | [Supabase architecture](https://supabase.com/docs/guides/getting-started/architecture), [Atlas network security](https://www.mongodb.com/docs/atlas/architecture/current/network-security/) | verified; provider and customer controls remain distinct |
| 2 | relational operations, `NULL`, joins, grouping, CTEs, safe DML | [PostgreSQL 18 SQL documentation](https://www.postgresql.org/docs/current/dml.html) | verified against current stable documentation; examples avoid version-fragile syntax |
| 3 | constraints, keys, metadata, indexes versus integrity | [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), [information schema](https://www.postgresql.org/docs/current/information-schema.html) | verified; primary/unique constraints and their index effects are described separately |
| 4 | identity/sequence behavior, views, dependency-aware migration | [PostgreSQL identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html), [view security](https://www.postgresql.org/docs/current/sql-createview.html) | verified; exact lock and view behavior remains version-qualified |
| 5 | MVCC, Read Committed, locking, deadlocks, retry boundaries | [PostgreSQL concurrency control](https://www.postgresql.org/docs/current/mvcc.html), [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | verified; PostgreSQL Read Uncommitted mapping and serialization-retry requirements remain explicit in the module |
| 6 | least privilege, RLS default deny, owner/bypass behavior, Supabase role context | [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [OWASP Database Security](https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html) | verified; allow and deny evidence is required from the intended role |
| 7 | `EXPLAIN ANALYZE`, buffers, row estimates, scan judgment, multicolumn indexes | [PostgreSQL `EXPLAIN`](https://www.postgresql.org/docs/current/using-explain.html), [multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html) | verified for PostgreSQL 18; optional work adds machine-readable plan inspection rather than prescribing node names |
| 8 | logical dumps, tool compatibility, separate restore, untrusted-artifact risk | [`pg_dump`](https://www.postgresql.org/docs/current/app-pgdump.html), [`pg_restore`](https://www.postgresql.org/docs/current/app-pgrestore.html) | verified; candidate now explicitly warns that restoring an untrusted dump can execute source-controlled code |
| 9 | NoSQL history, JSON grammar, model families, cosine meaning | [RFC 8259](https://www.rfc-editor.org/info/rfc8259/), [Bigtable paper](https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/), [Dynamo paper](https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store), [MongoDB cosine expression](https://www.mongodb.com/docs/manual/reference/operator/aggregation/similaritycosine/) | verified; the text distinguishes mathematical cosine similarity from product/version availability and from semantic truth |
| 10 | Atlas connection boundaries, CRUD evidence, embedding versus referencing | [Atlas connection prerequisites](https://www.mongodb.com/docs/atlas/connect-to-database-deployment/), [MongoDB modeling guidance](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/) | verified; access patterns, atomicity, duplication, and unbounded growth drive the model decision |
| 11 | aggregation order, validation, explain evidence, indexed sort | [aggregation optimization](https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/), [schema validation](https://www.mongodb.com/docs/manual/core/schema-validation/), [`$sort`](https://www.mongodb.com/docs/manual/reference/operator/aggregation/sort/) | verified; deterministic tie-breaks and Atlas Free in-memory-sort limits are now explicit |
| 12 | replica-set roles, read/write concerns, CAP scope, replication versus backup | [read concern](https://www.mongodb.com/docs/manual/reference/read-concern/), [replica-set semantics](https://www.mongodb.com/docs/manual/applications/replication/), [Atlas Free limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/) | verified; Atlas Free remains fixed at three nodes with no native backup or failover testing |
| 13 | shard-key evidence, routing, cardinality/frequency/monotonicity, secure cloud connection | [MongoDB shard-key selection](https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/), [PyMongo connection guidance](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/), [Supabase connection modes](https://supabase.com/docs/guides/database/connecting-to-postgres), [Supabase SSL modes](https://supabase.com/docs/guides/platform/ssl-enforcement) | verified; examples use Stable API, bounded waits, and explicit encrypted PostgreSQL transport while distinguishing encryption from full certificate/hostname verification |
| 14 | dual-write failure, transactional outbox, idempotency, reconciliation | [AWS transactional outbox guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [PostgreSQL logical decoding](https://www.postgresql.org/docs/current/logicaldecoding-explanation.html), [MongoDB change streams](https://www.mongodb.com/docs/manual/changeStreams/) | verified; the text avoids an exactly-once guarantee and requires stable IDs, retries, lag evidence, and repair direction |
| 15 | portfolio safety, evidence-based interview claims, career competencies | [GitHub secret-scanning guidance](https://docs.github.com/code-security/secret-scanning/introduction/about-secret-scanning), [NACE competencies](https://www.naceweb.org/career-readiness/competencies/career-readiness-defined), [O*NET DBA profile](https://www.onetonline.org/link/summary/15-1242.00) | verified; students translate bounded course evidence rather than claim production ownership |

## 4. Current Free-Platform Facts

The audit verified these change-sensitive facts on August 8, 2026:

- PostgreSQL 18 is the current stable PostgreSQL documentation line; PostgreSQL
  19 is a development/beta line and is not the course baseline.
- Supabase Free direct database endpoints use IPv6. The shared Supavisor session
  endpoint on port 5432 supports persistent clients on IPv4-only networks; the
  transaction endpoint on port 6543 suits transient/serverless traffic and does
  not support prepared statements. Native tools such as `pg_dump` should use a
  compatible direct or session connection rather than transaction pooling.
- PostgreSQL's default `sslmode=prefer` can fall back to plaintext. The notebook
  cloud paths require `require`, `verify-ca`, or `verify-full`; `verify-full` with
  the current Supabase CA is the production recommendation, while `require`
  encrypts without authenticating the server.
- Atlas Free uses MongoDB 8.0, has a fixed three-node replica set and 0.5 GB
  storage, and does not provide native backup, sharding, primary-failover tests,
  disk spill for aggregation, or the Performance Advisor. Current limits include
  500 connections, 100 operations per second, 50 pipeline stages, and a 32 MB
  in-memory sort boundary.
- Atlas requires TLS and explicit network access. A temporary single-address
  `/32` entry is safer than a permanent all-address rule. Atlas users and database
  users are separate identities. Current Python examples use Stable API version
  1, bounded server-selection/operation waits, ping, and explicit cleanup.
- Free-tier limits are instructional constraints, not production recommendations.
  The course uses small fixtures, local fallbacks, and explicit non-production
  scope.

## 5. Optional Industry Extensions

Each weekly student guide now contains exactly one clearly labeled optional,
ungraded extension that adds no submission and is never assumed as a prerequisite.

| Week | Extension | New or transferred practice |
|---:|---|---|
| 1 | status-page evidence audit | source evaluation and shared-responsibility boundaries |
| 2 | equivalent-query detective | independent verification and result-grain debugging |
| 3 | CISA KEV data contract | real-data types, nullability, and rejected-state reasoning |
| 4 | zero-downtime change note | backward compatibility and reversible migration communication |
| 5 | deadlock detective | wait-for graphs, prevention, and retry requirements |
| 6 | permission escape room | least-privilege redesign plus allow/deny tests |
| 7 | machine-readable plan detective | JSON plan evidence and automation limits |
| 8 | restore game-day go/no-go | artifact trust, checksums, isolation, and verification |
| 9 | JSON interoperability escape room | grammar versus interoperable data contracts |
| 10 | live-service game inventory | bounded embedding, references, and unbounded history |
| 11 | leaderboard pipeline | deterministic sort, compound index, and explain evidence |
| 12 | ticket-sale partition tabletop | user-facing promises, concerns, and idempotent retries |
| 13 | KEV patch-priority briefing | real public data, grouped verification, and executive writing |
| 14 | duplicate-event chaos test | idempotency, ordering, reconciliation, and lag metrics |
| 15 | sixty-second interview recording | concise technical evidence and honest scope |

## 6. Locally Controllable QA Record

The release candidate must not advance solely because the files exist. Before a
local candidate commit or tag, the current run must establish:

- publication formats rebuild from canonical Markdown;
- standalone HTML includes a skip link, one table-of-contents navigation
  landmark, and one main-content landmark;
- relative links, JSON, CSV, notebook structure, notebook outputs, credentials,
  canonical assignments, individual-work rules, and optional-extension rules pass
  the package validator;
- all notebook offline paths execute in a clean environment;
- slide count, slide boundaries, note/transcript identity, PDF page count, and PDF
  text extraction pass;
- HTML keyboard navigation and an accessibility-tree inspection are recorded;
- HTML, EPUB, and Word archives receive integrity and content spot checks; and
- external links receive automated review, with account-gated or bot-protected
  cases recorded for later manual verification.

The release checklist remains authoritative for actual results. The August 10
candidate QA run passed 383 local checks and 385 checks in network-enabled mode
across 139 unique URLs. No confirmed 404 or 410 result was found. The sole
automated-client refusal, the current BLS Database Administrators and Architects
page, passed independent browser review. All 214 final slides and all 15
final PDF handouts received visual review; all handouts report tagged structure
and are unencrypted; their title, author, language, and structure-catalog
metadata pass automated checks; a 214-page render comparison after metadata
regeneration found zero changed pixels. The six notebooks re-executed 68 offline code cells without
errors after connection-safety updates; PostgreSQL fixtures executed with
documented counts; publication checksums and EPUB/DOCX archive/XML checks passed;
official W3C EPUBCheck 5.3.0 reported zero messages under EPUB 3.3 rules; and all
90 pages of the current Word export received visual review.

Standalone HTML contains one navigation landmark, one focusable main landmark,
an effective skip target, embedded CSS, and no page-level overflow at tested
desktop and mobile widths. In Safari, an actual `Option+Tab` and `Return`
sequence focused and activated the skip link, changed the URL to
`#main-content`, moved the viewport, and transferred accessibility focus into
the main container. This representative standalone check does not replace a
comprehensive keyboard traversal or any externally assigned human assistive-
technology review in the intended Pressbooks and LMS contexts.

## 7. External Gates That Remain Honest Gaps

The following cannot be completed by local authoring alone and must not be
represented as done:

- OER-team attribution and accessibility approval;
- comprehensive keyboard review and, if required, qualified external assistive-
  technology review in the final Pressbooks and LMS environments;
- Pressbooks import plus Pressbooks-generated Digital PDF, EPUB, and Common
  Cartridge inspection;
- live Atlas, Supabase, and account-gated vendor completion under temporary
  course/student-role accounts;
- classroom implementation in a scheduled section;
- de-identified student learning/access evidence and evidence-based revision;
- final institutional approval, CUNY Academic Works deposit, dissemination, and
  public release.

These are fellowship activities, not missing authored chapters. A local release
candidate can be complete and review-ready while these gates remain open.
