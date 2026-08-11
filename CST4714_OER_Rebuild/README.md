# CST4714 Database Administration

## Operating Cloud Databases: PostgreSQL, MongoDB, and Reliable Data Systems

This is a beginner-friendly, lab-first course about building, operating, securing,
measuring, and recovering small database systems. We use PostgreSQL through
Supabase and MongoDB through Atlas because both platforms provide realistic cloud
workflows without requiring a paid account.

The course is not a tour of buttons. Each week asks you to make and defend an
operational decision: how data should be structured, who should be allowed to do
what, how to investigate slow or blocked work, and how to prove that a system can
recover.

## Start Here

1. Read the [course syllabus](syllabus.md).
2. Review the [course map](course_map.md) to see how the skills build.
3. Open the current week below.
4. Keep your weekly artifacts in one private or public GitHub repository unless
   your instructor gives a different submission location.

## Read and Reuse the Book

The canonical modules remain editable Markdown. The release-candidate
[publication package](publication/README.md) also provides a
[standalone HTML book](publication/exports/operating_cloud_databases_v1.0.0-rc.1.html),
[EPUB](publication/exports/operating_cloud_databases_v1.0.0-rc.1.epub), and
[Word import file](publication/exports/operating_cloud_databases_v1.0.0-rc.1.docx).
The Word file is prepared for CUNY Pressbooks import. See the
[release notes](RELEASE_NOTES.md) for completed checks and known limitations.

## Weekly Course Map

| Week | Operating question | Student guide |
|---|---|---|
| 1 | What does a database professional operate, and how does the relational model organize facts? | [Enter the profession and rebuild relational thinking](week_01/README.md) |
| 2 | How do relational operations become trustworthy SQL results? | [Complete the SQL review studio](week_02/README.md) |
| 3 | How do schemas, keys, constraints, and indexes divide responsibility? | [Build a dependable schema](week_03/README.md) |
| 4 | How can a database change without breaking its users? | [Expose and change data safely](week_04/README.md) |
| 5 | What happens when two sessions act at the same time? | [Transactions and concurrency](week_05/README.md) |
| 6 | How do we grant useful access without granting everything? | [Identity, permissions, and RLS](week_06/README.md) |
| 7 | How do we explain and improve a slow query? | [Plans, evidence, and indexes](week_07/README.md) |
| 8 | Can we restore the system we claim to have backed up? | [Backup, recovery, and the midterm](week_08/README.md) |
| 9 | Why do document databases exist, and what does JSON make possible? | [From tables to documents](week_09/README.md) |
| 10 | How do we query documents and choose what belongs together? | [MQL and document modeling](week_10/README.md) |
| 11 | How do pipelines, validation, and indexes support a workload? | [MongoDB operations](week_11/README.md) |
| 12 | What do replication and recovery promises really mean? | [Reliability and restore evidence](week_12/README.md) |
| 13 | When does scale change the design of a database system? | [Capacity, sharding, and integration](week_13/README.md) |
| 14 | How should a team reason across more than one data system? | [Polyglot incident response](week_14/README.md) |
| 15 | How do you explain these skills in a project review or interview? | [Synthesis and career evidence](week_15/README.md) |

## Major Assignments

- [Midterm operations case](midterm_project.md): one guided PostgreSQL/Supabase
  investigation and repair package.
- [Final cloud database project](final_project.md): a small PostgreSQL, MongoDB,
  or carefully justified two-platform system.

These are the only canonical descriptions of the major assignments. Weekly pages
contain checkpoints and links, not alternate requirements.

## Cost and Resource Types

Students are never required to purchase a textbook, subscription, database plan,
or certification. The course uses two clearly separated resource types:

- **Course OER:** original or license-compatible adapted modules, labs,
  assignments, datasets, notebooks, slides, transcripts, and implementation
  materials that may be retained and adapted under the licenses in this package.
- **Free external resources:** official documentation, cloud platforms, GitHub
  Skills, selected MongoDB University activities, and similar resources that cost
  students nothing but may not carry an open license. These are linked rather than
  copied and are not claimed as fellowship-created OER.

See the [catalog of created OER](OER_CATALOG.md) for exact artifacts and current
status. The [free external resource catalog](FREE_EXTERNAL_RESOURCES.md) records
the no-cost platforms and vendor materials that are linked but not claimed as
created OER. Fellowship planning and reporting documents remain separate in the
[`fellowship/` directory](fellowship/README.md).

## Course Platforms

- [GitHub](https://github.com/) stores reproducible SQL, JSON, notebooks, and
  short technical explanations.
- [Supabase](https://supabase.com/) provides managed PostgreSQL and a browser SQL
  editor.
- [MongoDB Atlas](https://www.mongodb.com/atlas/database) provides a managed
  MongoDB cluster and browser Data Explorer.
- [Google Colab](https://colab.research.google.com/) runs the six course notebooks
  without a local Python installation.

Free plans change over time. The labs use only features documented as available
without payment and provide a local or evidence-based fallback when a cloud
feature is unavailable. A free account may be required for a platform activity,
but a paid upgrade is never a course requirement.

## What You Produce

The first four class meetings include a substantial relational-model and SQL
review. Students rebuild forgotten skills through relational-algebra reasoning,
query prediction, SQL execution, and verification before the course assumes those
skills in administration labs.

Every class produces one small, checkable artifact such as a query file, a JSON
model, a query-plan explanation, a restore log, an incident note, or a notebook.
The goal is not to collect screenshots. The goal is to leave with evidence that
another person can inspect, reproduce, and discuss.

## Accessibility and Formats

Every module is available as structured Markdown. Slide decks include complete
spoken scripts in speaker notes, and each deck is also published as a PDF handout
and a structured-text transcript. The transcript is the complete text alternative
to the spoken presentation. Every PDF reports tagged structure, but automated
tag-tree inspection found insufficient semantics and no figure alternative-text
metadata. The PDFs are convenience handouts, not claimed accessible PDFs. Labs
avoid color-only instructions, identify expected output, and include text
alternatives for essential visuals.

The open textbook is also built as semantic HTML, EPUB, and Word. These portable
formats expand device and assistive-technology options; final accessibility is
verified again in the public Pressbooks and LMS environments.

## Open License

Unless a file says otherwise, original instructional text and slides are licensed
under [CC BY-NC-SA 4.0](LICENSE.md). Original code is licensed under the MIT
License, and original datasets are released under CC0. See
[ATTRIBUTIONS.md](ATTRIBUTIONS.md) for adapted and linked resources.
