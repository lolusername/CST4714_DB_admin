# CST4714 Fall 2026 Course Home

This is the full local teaching draft for **CST4714 Database Administration**.
Each weekly page contains the assigned textbook reading, slides, class plan,
individual lab, and any notebook or free external activity used that week.

## Essential Course Links

- **Syllabus:** [PDF](CST4714_Fall_2026_Syllabus.pdf) | [Word](CST4714_Fall_2026_Syllabus.docx) | [editable source](syllabus.md)
- **Textbook:** [web edition](textbook/publishing/exports/operating_cloud_databases_second_edition_draft.html) | [PDF](textbook/publishing/exports/operating_cloud_databases_second_edition_draft.pdf) | [Word](textbook/publishing/exports/operating_cloud_databases_second_edition_draft.docx) | [EPUB](textbook/publishing/exports/operating_cloud_databases_second_edition_draft.epub)
- **Projects:** [midterm](assignments/midterm_project.md) | [final project](assignments/final_project.md)
- **Course datasets:** [Metro Support](datasets/metro_support/README.md) | [Mini Inventory](datasets/mini_inventory/README.md) | [CISA KEV sample](datasets/cisa_kev_sample/README.md)
- **Jupyter/Colab lessons:** [notebook index](notebooks/README.md)

There is no textbook to purchase. The assigned book is included above. Free
vendor lessons and documentation are linked only when they add useful practice.

## Weekly Course Map

Open the week page before class. The chapter listed in the third column is the
assigned reading for that week; no separate reading notes are required unless a
Brightspace assignment explicitly asks for them.

| Week | Main topics | Assigned textbook reading | Open the class |
|---:|---|---|---|
| 1 | How database-backed applications work; DBMS and cloud platforms; relational model and algebra | [Chapter 1](textbook/module_01_responsibility.md) and the opening relational-model sections of [Chapter 2](textbook/module_02_sql.md) | [Week 1](weeks/week_01/README.md) |
| 2 | Major SQL review: filters, joins, grouping, subqueries, set operations, and safe changes | [Chapter 2](textbook/module_02_sql.md) | [Week 2](weeks/week_02/README.md) |
| 3 | PostgreSQL schemas, keys, constraints, metadata, and indexes | [Chapter 3](textbook/module_03_schema.md) | [Week 3](weeks/week_03/README.md) |
| 4 | Views, identity columns, metadata, and safe schema changes | [Chapter 4](textbook/module_04_change.md) | [Week 4](weeks/week_04/README.md) |
| 5 | Transactions, ACID, MVCC, locks, blocking, and deadlocks | [Chapter 5](textbook/module_05_transactions.md) | [Week 5](weeks/week_05/README.md) |
| 6 | Roles, privileges, Supabase Auth, row-level security, and secrets | [Chapter 6](textbook/module_06_security.md) | [Week 6](weeks/week_06/README.md) |
| 7 | `EXPLAIN`, query plans, selectivity, and index design | [Chapter 7](textbook/module_07_performance.md) | [Week 7](weeks/week_07/README.md) |
| 8 | Logical backup, restore, RPO/RTO, and midterm work | [Chapter 8](textbook/module_08_recovery.md) | [Week 8](weeks/week_08/README.md) |
| 9 | NoSQL history and models; JSON; Atlas and GitHub orientation | [Chapter 9](textbook/module_09_nosql_json.md) | [Week 9](weeks/week_09/README.md) |
| 10 | Basic MQL and access-pattern-driven document modeling | [Chapter 10](textbook/module_10_mql_modeling.md) | [Week 10](weeks/week_10/README.md) |
| 11 | Aggregation pipelines, validation, MongoDB indexes, and `explain` | [Chapter 11](textbook/module_11_mongodb_operations.md) | [Week 11](weeks/week_11/README.md) |
| 12 | Replica sets, consistency choices, partitions, and logical recovery | [Chapter 12](textbook/module_12_reliability.md) | [Week 12](weeks/week_12/README.md) |
| 13 | Capacity, sharding, shard keys, Python, and public-data imports | [Chapter 13](textbook/module_13_scale.md) | [Week 13](weeks/week_13/README.md) |
| 14 | PostgreSQL and MongoDB together; outbox pattern and incident repair | [Chapter 14](textbook/module_14_polyglot.md) | [Week 14](weeks/week_14/README.md) |
| 15 | Integrated review, final demonstrations, portfolios, and interviews | [Chapter 15](textbook/module_15_careers.md) | [Week 15](weeks/week_15/README.md) |

## How the Materials Fit Together

- The **textbook chapter** introduces and explains the week's concepts.
- The **PowerPoint** supports the two class meetings with examples, diagrams,
  screenshots, code, and discussion prompts. Its notes contain a complete spoken
  script; the matching transcript provides the same content as structured text.
- The **lab** is individual, begins in class, and asks for one clearly named
  submission.
- A **notebook** appears when executable exploration is more useful than a static
  worksheet.
- **Brightspace** remains the source for due dates and submission links.

## Included Course Materials

The package contains 15 textbook chapters, 15 weekly class pages, 24 individual
labs, 7 notebooks, 3 reusable datasets, 15 slide decks with transcripts and PDF
handouts, a midterm, a final project, assessments, and instructor implementation
guides.

The PDF handouts are convenience copies. Earlier inspection found limited tag
semantics, so every deck also includes a structured transcript. The textbook
offers Word, HTML, and EPUB alternatives. Revised exports still need full
reading-order and accessibility review; extractable text or a tagged-PDF flag
alone does not establish accessibility.

## Instructor Resources

- [Course implementation guide](instructor/implementation_guide.md)
- [Technical setup and troubleshooting](instructor/technical_setup_troubleshooting.md)
- [Accessibility and adaptation](instructor/accessibility_adaptation.md)
- [Assessment resources](assessments/README.md)
- [Course alignment map](course_map.md)

## OER and Fellowship Boundary

The student course and the fellowship documentation are intentionally distinct:

- [OER catalog](OER_CATALOG.md) lists the course-created open materials.
- [Free, non-OER resources](external_resources/INDEX.md) lists vendor-owned materials
  such as MongoDB educator decks and MongoDB University activities.
- [Fellowship documentation](../oer_fellowship/README.md) contains planning, research,
  review, release, and presentation materials. It is not assigned to students.

Nothing in this folder has been formally published or deposited as OER. The
package remains an unpublished draft under technical and educational review.
The public GitHub repository contains only the separately prepared Week 1 package.
Changing this local draft does not authorize publishing the fellowship materials.

## Editing and Rebuilding

Edit the human-readable source closest to the material. Textbook chapters are in
`textbook/`; weekly guides and labs are grouped under `weeks/`.
Generated Word, PDF, HTML, EPUB, and slide-handout files should be rebuilt rather
than edited separately.

Run the course validator after a change:

```bash
python3 tools/validate_oer.py
```

Original instructional prose and media are licensed CC BY-NC-SA 4.0, original
code is MIT licensed, and original synthetic datasets are CC0 unless a file
states otherwise. See [LICENSE](LICENSE.md) and [ATTRIBUTIONS](ATTRIBUTIONS.md).
