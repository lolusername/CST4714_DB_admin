# CST4714 Database Administration

## Operating Cloud Databases: PostgreSQL, MongoDB, and Reliable Data Systems

- **Instructor:** [Instructor name]
- **Term:** [Term and year]
- **Meeting pattern:** Two class meetings in most weeks
- **Office hours and contact:** [Course-specific information]
- **Course site:** [Brightspace course link]

## Course Description

This course begins with a substantial review of the relational model, core
relational algebra, and SQL because later administration work depends on being
able to predict and verify query behavior. It then introduces the work of
operating data systems: structuring data,
controlling access, investigating performance, handling concurrent work, creating
recovery evidence, and explaining reliability tradeoffs. Students use PostgreSQL
through Supabase and MongoDB through Atlas, with GitHub for reproducible technical
artifacts and small Python notebooks for automation and integration.

The course begins with relational data and SQL, then introduces document data,
MongoDB Query Language, modeling, aggregation, and reliability. It concludes with
scaling, polyglot architecture, incident reasoning, a small cloud database
project, and career communication.

## Learning Outcomes

Successful students will be able to:

1. Design a small relational or document model for a stated workload.
2. Build and query data in PostgreSQL/Supabase and MongoDB/Atlas.
3. Apply beginner-level integrity and access controls.
4. Use database evidence to investigate concurrency and performance.
5. Plan, perform, and verify logical backup and restore work within free-tier
   platform constraints.
6. Explain reliability, replication, consistency, sharding, and multi-database
   design tradeoffs.
7. Document database work in reproducible, workplace-readable artifacts.

## Required Materials

No commercial textbook or paid cloud account is required. Some required readings
and labs are course OER; other required references and platform exercises are
free-to-access external resources. Free access is not the same as an open license,
so external resources are linked rather than copied.

- A computer with a current web browser
- A free GitHub account
- A free Supabase account
- A free MongoDB Atlas account
- Access to Google Colab or another Jupyter environment
- The open course modules, labs, and linked official documentation in this
  repository

Students who cannot create a platform account should contact the instructor. Each
cloud-dependent lab includes a local, static, or evidence-based fallback.

## Assessment

| Category | Weight |
|---|---:|
| [Midterm operations case](midterm_project.md) | 30% |
| [Final cloud database project](final_project.md) | 40% |
| Engagement and skill evidence | 30% |

### Engagement and Skill Evidence

Engagement is demonstrated through work, not mere presence. Evidence includes
individual in-class labs, brief retrieval and exit checks, six notebooks, and
eight short critical or career-connected writing responses. Most class meetings
produce one small submission. Low-stakes checks may be graded for completion and
reasonable effort; labs are graded for correctness, evidence, and explanation.

### Major Assignments

The midterm is one guided PostgreSQL/Supabase operations case. The final is a
small cloud database project using PostgreSQL, MongoDB, or a carefully justified
combination. The linked assignment pages are the only canonical requirements.

## Weekly Schedule

| Week | Topics and practice |
|---:|---|
| 1 | DBA roles; data-system vocabulary; shared responsibility; relational model and relational-algebra review; GitHub, Supabase, and Atlas orientation |
| 2 | Major SQL review: selection, filtering, sorting, joins, grouping, subqueries, CTEs, safe data changes, result grain, and verification |
| 3 | Cumulative SQL clinic; schemas, tables, keys, constraints, indexes, metadata, and managed-service boundaries |
| 4 | Views, identity and sequences, introspection, safe schema changes, and verification |
| 5 | Transactions, ACID, isolation, MVCC, locks, blocking, and two-session diagnosis |
| 6 | Roles, grants, least privilege, Supabase Auth concepts, row-level security, and secrets |
| 7 | `EXPLAIN`, query plans, selectivity, index design, and evidence-based tuning |
| 8 | Logical backup and restore, safe migrations, verification, and the midterm |
| 9 | NoSQL history and families; JSON syntax and design; Atlas orientation; tables-to-documents lab |
| 10 | MongoDB collections, CRUD, basic MQL, embedding, referencing, and access patterns |
| 11 | Aggregation pipelines, schema validation, indexes, `explain`, and workload reasoning |
| 12 | Replication, consistency, read preference, write concern, logical recovery, and final-project launch |
| 13 | Capacity, sharding, shard keys, Python integration, and a final-project skill checkpoint |
| 14 | Polyglot data systems, distributed tradeoffs, incident response, and final-project clinic |
| 15 | Integrated review, final presentations, portfolio evidence, and interview communication |

The instructor will publish course-specific dates in Brightspace. The sequence may
shift when learning evidence shows that the class needs more practice.

## Submission Standards

- Submit the artifact named by the current lab or assignment.
- Never submit passwords, database connection strings, service-role keys, or
  unredacted secrets.
- Put executable steps in a sensible order and identify expected output.
- Explain what the evidence proves; a screenshot without interpretation is not
  sufficient.
- Cite data, code, prose, and media that you did not create.

## Individual Work and Collaboration

All graded labs and projects are individual. Students may discuss concepts,
compare error messages, and point one another to documentation, but each student
must write, run, verify, and explain their own work. Follow the institution's
academic integrity and acceptable-use policies.

## Responsible Use of Tools

Documentation, autocomplete, debuggers, and instructor-approved assistance may
support learning. Students remain responsible for understanding submitted work,
protecting credentials, citing sources, and explaining every important decision.
Course-specific guidance in Brightspace controls when particular assistance is or
is not permitted.

## Accessibility and Inclusion

Course materials use headings, descriptive links, high-contrast visuals,
transcripts, speaker notes, and text alternatives. Students may use the cloud,
local, or static-data path identified by a lab when technology or access creates a
barrier. Contact the instructor or the institution's accessibility office for
formal accommodations.

## Data and Privacy

Class datasets are synthetic, public, or explicitly licensed for educational use.
Do not load private, regulated, or personally identifying information into a
course database. Do not post credentials in GitHub. Learning analytics for the
course use aggregate class patterns rather than public student-level profiles.

## Course Policies

Institutional policies for attendance, deadlines, academic integrity,
accessibility, student conduct, and emergencies apply. The instructor will add
course-specific contact and deadline details before the term begins.
