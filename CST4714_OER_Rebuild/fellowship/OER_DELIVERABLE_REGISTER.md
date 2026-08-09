# OER Deliverable and Resource Register

> **Document type:** fellowship production register, not student course content.
> For the exact files already created, their original educational contribution,
> and current completion status, use the separate
> [Catalog of Created OER](../OER_CATALOG.md). Free vendor and industry links are
> maintained separately in the
> [Free External Resource Catalog](../FREE_EXTERNAL_RESOURCES.md).

## Why This Register Exists

The course is zero-cost, but not every free resource is OER. This register makes
the boundary auditable and gives the project director a precise account of what
the fellowship creates, adapts, and curates.

- **Authored OER:** new instructional content created for this project and
  released under an open license.
- **Adapted OER:** openly licensed source material changed for this course with
  source, license, and change notices.
- **Curated free resource:** no-cost external material or platform linked for
  reading or practice. It is not copied or counted as created OER unless its
  license permits that claim.

## Primary OER Deliverable

| ID | Deliverable | Planned scope | Production role | License | Formats | Student use |
|---|---|---:|---|---|---|---|
| P1 | *Operating Cloud Databases* open textbook and lab manual | 15 modules | authored with attributed, compatible adaptations | CC BY-NC-SA 4.0, with source-specific notices | Markdown, Pressbooks web, PDF, EPUB | required conceptual reading, worked examples, practice, reference |

### Module Inventory

| Module | OER focus | Original contribution |
|---:|---|---|
| 1 | responsibility and evidence | layered incident model, shared-responsibility map, reproducible evidence pattern |
| 2 | relational model, algebra, and SQL review | prediction-to-SQL bridge, result-grain checks, safe DML review |
| 3 | schemas and integrity | Metro Support audit, managed-service boundary, expected-failure verification |
| 4 | views and safe change | five-part change record and expand-migrate-contract beginner case |
| 5 | transactions and concurrency | two-session mental model, MVCC and blocking evidence sequence |
| 6 | security | actor-action-resource access matrix and allow/deny proof pattern |
| 7 | performance | question-plan-hypothesis-change-remeasure workflow |
| 8 | recovery | free-tier-accurate logical backup, restore, and verification framework |
| 9 | NoSQL and JSON | history-to-workload narrative and multiple-valid-model comparison |
| 10 | MQL and modeling | relational-to-document translation around access patterns |
| 11 | MongoDB operations | pipeline, validation, and index reasoning in one workload |
| 12 | reliability | explicit promise, mechanism, failure, and verification framework |
| 13 | scale | shard-key and capacity reasoning for beginners |
| 14 | polyglot systems | ownership, synchronization, and incident-boundary analysis |
| 15 | careers | evidence-to-interview and evidence-to-portfolio translation |

## Supporting OER Category 1: Labs, Notebooks, and Data

| ID range | Deliverable | Planned scope | Production role | License |
|---|---|---:|---|---|
| L01-L24+ | Individual in-class labs | at least 24 | authored OER | CC BY-NC-SA 4.0; code MIT |
| N01-N06 | Educational Jupyter notebooks | 6 | authored OER | prose CC BY-NC-SA 4.0; code MIT |
| D01-D02 | Original synthetic teaching datasets | 2 relational/document cases | authored | CC0 |
| D03 | Public-data teaching sample | 1 documented subset case | adapted/curated as source terms permit | recorded per dataset |

Every lab has one manageable submission, an individual-work statement, expected
evidence, credential-safety guidance where relevant, and an equivalent path for a
platform outage or access barrier.

## Supporting OER Category 2: Assessment and Projects

| ID | Deliverable | Scope | Production role | License |
|---|---|---:|---|---|
| A1 | pre/post concept inventory | 1 paired instrument | authored OER | CC BY-NC-SA 4.0 |
| A2 | retrieval and exit bank | 15 module-aligned sets | authored OER | CC BY-NC-SA 4.0 |
| A3 | critical and career writing | 8 prompts plus common rubric | authored OER | CC BY-NC-SA 4.0 |
| A4 | midterm operations case | 1 canonical assignment and rubric | authored OER | CC BY-NC-SA 4.0 |
| A5 | final cloud database project | 1 canonical assignment and rubric | authored OER | CC BY-NC-SA 4.0 |

Private student records and private grading annotations are not OER deliverables.

## Supporting OER Category 3: Slides and Study Media

| ID range | Deliverable | Planned scope | Production role | License |
|---|---|---:|---|---|
| S01-S15 | student-facing slide decks | 15 | authored OER with attributed open visuals | CC BY-NC-SA 4.0 |
| SP01-SP15 | word-for-word spoken scripts in notes and transcript form | 15 | authored OER | CC BY-NC-SA 4.0 |
| PDF01-PDF15 | visually verified deck PDF handouts | 15 | generated format of authored OER | CC BY-NC-SA 4.0 |
| V01+ | diagrams and data visuals | as needed | authored or openly licensed adaptation | recorded per asset |

The decks teach students directly. Notes contain complete spoken prose rather
than directions such as "explain this" or "focus on that."

## Supporting OER Category 4: Implementation Package

| ID | Deliverable | Planned scope | Production role | License |
|---|---|---:|---|---|
| I1-I15 | public lesson plans | 15 | authored OER | CC BY-NC-SA 4.0 |
| I16 | technical setup and troubleshooting guide | 1 | authored OER | CC BY-NC-SA 4.0; commands MIT |
| I17 | accessibility and adaptation guide | 1 | authored OER | CC BY-NC-SA 4.0 |
| I18 | data-informed teaching protocol | 1 | authored OER | CC BY-NC-SA 4.0 |
| I19 | [production, validation, and release guide](../RELEASE_CHECKLIST.md) | 1 | authored OER | CC BY-NC-SA 4.0; scripts MIT |

Public lesson plans contain implementation guidance and likely misconceptions,
not private answers, student data, or grading commentary.

## Curated Free External Resources

These resources may be required or recommended because they provide authentic,
current practice. They cost students nothing, but they are not counted as authored
OER.

| Resource | Cost to student | Account | How it is used | OER treatment |
|---|---:|---|---|---|
| PostgreSQL official documentation | $0 | none | authoritative SQL and operations reference | linked; not copied |
| Supabase documentation and Free project | $0 | free account for project | managed PostgreSQL practice | linked platform; open fallback supplied |
| MongoDB documentation and Atlas Free cluster | $0 | free account for cluster | managed document database practice | linked platform; open fallback supplied |
| selected MongoDB University activities | $0 | free account | guided industry practice tied to a distinct course lab | linked; completion is not the only learning evidence |
| GitHub Skills and GitHub Free | $0 | free account | web editing and versioned artifacts | linked; open text fallback supplied |
| Google Colab | $0 | free account normally used | run notebooks without local installation | notebook remains downloadable and locally runnable |
| Python documentation | $0 | none | language and library reference | linked; not copied |

Platform pricing, account rules, and feature limits are rechecked before each
public release. If a formerly free required feature becomes paid, the open local
or static path becomes the default until the activity is revised.

## Adaptation Record Template

Every adapted item adds an entry with:

```text
Course item ID:
Source title and author:
Source URL:
Source license:
Material used:
Changes made:
Course license and compatibility note:
Verification date:
```

## Release Reporting Snapshot

At each tagged release, record:

- completed versus planned OER items by ID;
- total openly licensed modules, labs, notebooks, datasets, decks, transcripts,
  assessments, and implementation guides;
- adaptations and their source licenses;
- free external resources and current account/cost status;
- accessibility and technical validation status; and
- classroom revisions supported by aggregate learning evidence.
