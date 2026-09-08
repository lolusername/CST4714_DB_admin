# OER Deliverable and Resource Register

> **Document type:** fellowship production register, not student course content.
> For the exact files already created, their original educational contribution,
> and current completion status, use the separate
> [Catalog of Created OER](../../course/OER_CATALOG.md). Free vendor and industry links are
> maintained separately in the
> [Free External Resource Catalog](../../course/external_resources/INDEX.md).

## Why This Register Exists

The course is zero-cost, but not every free resource is OER. This register makes
the boundary auditable and gives the project director a precise account of what
the fellowship creates, adapts, and curates.

- **Authored OER draft:** instructional content created for this project with
  an identified open license, still awaiting approved release. Record whether
  it originated in the preparatory draft or the current funded work period.
- **Revised prior course material:** an existing lesson or activity substantially
  changed for this course. Identify what changed rather than counting the entire
  old asset again as new authorship. Unchanged copies are not new deliverables.
- **Adapted OER:** openly licensed source material changed for this course with
  source, license, and change notices.
- **Curated free resource:** no-cost external material or platform linked for
  reading or practice. It is not copied or counted as created OER unless its
  license permits that claim.

## Primary OER Deliverable

| ID | Deliverable | Planned scope | Production role | License | Formats | Student use |
|---|---|---:|---|---|---|---|
| P1 | *Operating Cloud Databases* open textbook and lab manual | 15 modules | authored with attributed, compatible adaptations | CC BY-NC-SA 4.0, with source-specific notices | editable Markdown and Word; generated PDF, HTML, EPUB; CUNY platform publication pending approval | assigned conceptual reading, worked examples, practice, reference |

### Module Inventory

| Module | OER focus | Original contribution |
|---:|---|---|
| 1 | responsibility and evidence | layered incident model, shared-responsibility map, reproducible evidence pattern |
| 2 | relational model, algebra, and SQL review | prediction-to-SQL bridge, result-grain checks, safe DML review |
| 3 | schemas and integrity | Metro Support audit, managed-service boundary, expected-failure verification |
| 4 | views and safe change | identity behavior, backward-compatible migration, and honest treatment of unknown historical values |
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
| L01, L03-L25 | Individual in-class labs | 24; retired L02 excluded | authored and substantially redesigned activities; prior versions retained | CC BY-NC-SA 4.0; code MIT |
| N01-N07 | Educational Jupyter notebooks | 7 | authored and revised OER; previous versions retained for comparison | prose CC BY-NC-SA 4.0; code MIT |
| D01-D02 | Original synthetic teaching datasets | 2 relational/document cases | authored | CC0 |
| D03 | Public-data teaching sample | 1 documented subset case | adapted/curated as source terms permit | recorded per dataset |

Each lab is designed around one manageable submission, individual work, a result
students can check, and credential-safety guidance where relevant. Open or local
alternatives preserve access without treating mocks or supplied traces as
equivalent tests of a live server. Environment-specific limits are stated in the
activity and technical quality record.

## Supporting OER Category 2: Assessment and Projects

| ID | Deliverable | Scope | Production role | License |
|---|---|---:|---|---|
| A1 | pre/post concept inventory | 1 paired instrument | authored OER | CC BY-NC-SA 4.0 |
| A2 | retrieval and exit bank | 15 module-aligned sets | authored OER | CC BY-NC-SA 4.0 |
| A3 | critical and career writing | 8 prompts embedded in existing labs, plus the Week 11 case-study response and common rubric | authored and revised OER, not a separate stream of extra submissions | CC BY-NC-SA 4.0 |
| A4 | midterm operations case | 1 canonical assignment and rubric | authored OER | CC BY-NC-SA 4.0 |
| A5 | final cloud database project | 1 canonical assignment and rubric | authored OER | CC BY-NC-SA 4.0 |

Private student records and private grading annotations are not OER deliverables.

## Supporting OER Category 3: Slides and Study Media

| ID range | Deliverable | Planned scope | Production role | License |
|---|---|---:|---|---|
| S01-S15 | student-facing slide decks | 15 | authored and revised course materials with source-specific notices | CC BY-NC-SA 4.0; source exceptions retained |
| SP01-SP15 | word-for-word spoken scripts in notes and transcript form | 15 | authored OER | CC BY-NC-SA 4.0 |
| PDF01-PDF15 | deck PDF handouts requiring current visual verification | 15 | generated format of the corresponding deck, not separate authorship | source deck's license and exceptions |
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
| I19 | [production, validation, and release guide](../../course/RELEASE_CHECKLIST.md) | 1 | authored OER | CC BY-NC-SA 4.0; scripts MIT |

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

For an original-course revision, also record the earlier file/version, what was
retained, what was newly explained or tested, and the actual revision date. For
new textbook authorship, cite substantive source influences and distinguish
original examples from vendor examples. A preparatory OER draft is a baseline,
not an item to relabel as newly completed during the fellowship. Uncertain origin
should be marked for review rather than guessed.

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
