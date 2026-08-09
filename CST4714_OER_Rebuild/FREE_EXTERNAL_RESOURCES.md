# Free External Resource Catalog

## Boundary

Every resource in this file costs students nothing at the time of verification,
but free access is not the same as an open license. These resources are linked for
authentic practice and current reference. They are not counted as fellowship-
created OER unless a specific item has a documented compatible license.

**Verification date:** August 8, 2026. Platform pricing, account requirements,
URLs, and free-tier limits must be checked before each course release.

## Platforms and Documentation

| Resource | Course use | Account | Student cost | Open fallback or equivalent | Classification |
|---|---|---|---:|---|---|
| [PostgreSQL documentation](https://www.postgresql.org/docs/current/) | authoritative SQL and operations reference | none | $0 | course modules and local PostgreSQL | Free external reference |
| [Supabase documentation](https://supabase.com/docs) | managed PostgreSQL, browser editor, Auth/RLS context, connection guidance | none to read; free account for project | $0 | local PostgreSQL and static evidence paths | Free external reference/platform |
| [MongoDB documentation](https://www.mongodb.com/docs/) | MQL, modeling, aggregation, indexes, replication, sharding, and tools reference | none to read | $0 | course modules and `mongomock` notebook paths | Free external reference |
| [MongoDB Atlas](https://www.mongodb.com/atlas/database) | managed MongoDB and Data Explorer | free account | $0 free option | `mongomock`, JSON fixtures, and static evidence | Free external platform |
| [MongoDB University](https://learn.mongodb.com/) | selected guided industry practice | free account | $0 | course-authored equivalent prompts | Free external practice |
| [GitHub Free](https://github.com/) | versioned SQL, JSON, notebook, and portfolio artifacts | free account | $0 | local files or LMS text submission | Free external platform |
| [GitHub Skills](https://skills.github.com/) | optional guided GitHub practice | free account | $0 | course GitHub web-editor instructions | Free external practice |
| [Google Colab](https://colab.research.google.com/) | browser execution of course notebooks | free account normally used | $0 | local Jupyter execution | Free external platform |
| [Python documentation](https://docs.python.org/3/) | language and standard-library reference | none | $0 | course notebook explanations | Free external reference |
| [DuckDB documentation](https://duckdb.org/docs/) | embedded SQL reference for offline notebooks | none | $0 | bundled notebook examples | Free external/open-source reference |

## Free-Access Verification Evidence

The following official pages support the current cost and feature statements.
They are evidence about linked services, not course-created OER.

| Claim used by the course | Current official evidence | Course response |
|---|---|---|
| PostgreSQL 18 is the current stable documentation baseline | [PostgreSQL documentation](https://www.postgresql.org/docs/current/) identifies the current stable manual; development or beta documentation is not the course baseline | examples use durable SQL and PostgreSQL 18 behavior unless a module explicitly marks a version dependency |
| Supabase has a $0 Free plan with a managed PostgreSQL database | [Supabase pricing](https://supabase.com/pricing) lists the Free plan at $0 and identifies its included database quota and project limits | labs remain within the Free plan and never require disabling the spend cap or entering payment information |
| Supabase Free does not include automatic backups | [Supabase backup documentation](https://supabase.com/docs/guides/platform/backups) recommends that Free projects create and retain logical exports | the recovery lab uses a separate logical dump, restore, and verification path rather than promising dashboard backups |
| Supabase exposes different connection modes for different network and client needs | [Supabase connection guidance](https://supabase.com/docs/guides/database/connecting-to-postgres) distinguishes the IPv6 direct endpoint, IPv4-compatible Supavisor session endpoint, and transaction endpoint for transient/serverless traffic | notebooks use direct or session connections for persistent clients and native tools; transaction pooling is not used for prepared-statement or session-dependent work |
| Atlas Free currently uses MongoDB 8.0 with a fixed three-node replica set and 0.5 GB storage | [Atlas Free cluster limits](https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/) also document no native backup, sharding, failover testing, aggregation disk spill, or Performance Advisor, plus current connection, throughput, pipeline-stage, and in-memory-sort limits | fixtures remain small; recovery uses logical tools; sharding and failover are taught through evidence and simulation rather than fictional Free-tier operations |
| Atlas requires TLS and explicit network access | [Atlas network-security guidance](https://www.mongodb.com/docs/atlas/architecture/current/network-security/) documents encrypted connections and access-list controls | students use temporary, narrow access such as one-address `/32` rules when feasible, never disable certificate checking, and remove temporary access after use |
| MongoDB University contains free activities | the [MongoDB University catalog filtered to Free resources](https://learn.mongodb.com/catalog?labels=%5B%22Format%22%2C%22Learning+Format%22%5D&values=%5B%22Free%22%2C%22Course%22%5D) and the selected activity pages identify free enrollment | vendor activities are linked for current practice, while a course-authored fallback preserves the outcome if enrollment or the platform fails |
| GitHub has a $0 individual plan | [GitHub pricing](https://github.com/pricing) lists GitHub Free at $0 and includes public and private repositories | students may use a free repository or submit equivalent local/LMS files when account access is a barrier |
| Colab has a free-of-charge path with variable limits | the [official Colab FAQ](https://research.google.com/colaboratory/faq.html) describes free access and explains that resources and limits are not guaranteed | notebooks remain downloadable and include local or static fallbacks; no GPU or paid runtime is required |

Verification confirms only the claims recorded here. It does not convert a
vendor page, account, course, or cloud service into OER.

## Selected MongoDB University Activities

| Week | Activity | Instructional role | Why it is not counted as created OER | Course-authored fallback |
|---:|---|---|---|---|
| 9 | [Getting Started with MongoDB Atlas](https://learn.mongodb.com/courses/getting-started-with-mongodb-atlas-smartbridge) | optional setup orientation | vendor-hosted content | Week 9 setup sequence and static JSON lab |
| 9 | [MongoDB and the Document Model](https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge) | optional model orientation | vendor-hosted content | Module 9 and CSV-to-JSON lab |
| 10 | [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships) | instructor live demonstration | vendor-hosted content | Module 10 worked example and notebook |
| 10 | [Relational SQL to Document Model](https://learn.mongodb.com/courses/relational-to-document-model) | individual student practice | vendor-hosted content | course-authored model comparison prompt |
| 11 | [Improving Performance of Sort Stages](https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only) | individual performance practice | vendor-hosted content | course-authored pipeline/index lab and offline example |
| 12 | [MongoDB Atlas Backup and Recovery](https://learn.mongodb.com/learn/course/mongodb-atlas-backup-recovery/lesson-1-back-up-and-recover-an-atlas-free-tier/learn) | optional current product context | vendor-hosted content | logical recovery notebook and runbook lab |

The instructor live activity in Week 10 is intentionally different from the
individual student activity. Vendor completion screenshots are supporting
evidence only; the course-authored interpretation demonstrates the learning.

## Public Data Source

The [CISA Known Exploited Vulnerabilities feed](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
is an official U.S. government source. The transformed teaching snapshot is
cataloged as D03 in [the OER catalog](OER_CATALOG.md); it is not represented as an
original course dataset. Its package README records source and transformation
details.

## Replacement Rule

If a required external feature becomes paid, inaccessible, or materially changed,
the linked resource is removed from the required path. The course-authored local,
static, or simulated path becomes the default until the activity is revised and
revalidated. Students are never required to start a paid trial or provide a
payment card.
