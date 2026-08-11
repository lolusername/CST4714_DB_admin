# How to Explain and Present This OER Project

> **Use this document first.** It explains the project in plain language,
> separates the actual OER from fellowship administration, and provides
> word-for-word presentation scripts. It is not student course content and is
> not counted as an OER deliverable.

## The One-Sentence Version

I redesigned CST 4714 as a complete, zero-cost, lab-first course that rebuilds
students' relational and SQL foundations, then teaches them to operate,
troubleshoot, secure, recover, and explain PostgreSQL and MongoDB systems using
authentic evidence and career-connected work.

## The Most Important Distinction

There are three related but different bodies of work.

| Body of work | What it is | Current state |
|---|---|---|
| The course OER | Textbook modules, weekly guides, labs, notebooks, datasets, assessments, projects, slides, scripts, transcripts, and instructor materials | Authored and assembled as a complete 15-week release candidate |
| Fellowship planning and evidence | Scope, pedagogy, evaluation, publication, attribution, and review records in this `fellowship` directory | Prepared for review; deliberately separate from student OER |
| Publication and release engineering | HTML, EPUB, Word, PDF handouts, metadata, validators, checksums, and QA evidence | Locally validated; not approved or publicly released |

The course is **not merely a plan**. The instructional files exist. The course
is also **not yet a completed fellowship publication** because approval,
Pressbooks review, classroom implementation, student evidence, and formal
publication remain future fellowship activities.

## What Was Actually Built

| Deliverable | Completed scope | Why it matters |
|---|---:|---|
| Open textbook | 15 modules, approximately 22,000 words | Replaces disconnected readings with one coherent course narrative |
| Weekly learning sequences | 15 guides covering two class meetings each | Connects reading, live explanation, practice, lab work, and transfer |
| Individual labs | 25 | Gives every student repeated technical practice without group-work ambiguity |
| Optional industry extensions | 15, one per week | Adds interesting professional transfer without adding required submissions |
| Educational notebooks | 6 notebooks, 68 executable code cells | Demonstrates SQL, transactions, recovery, MQL, modeling, and data integration |
| Reusable data packages | 3 | Supports repeated work with synthetic civic-service data, inventory data, and a documented CISA public-data sample |
| Major projects | 1 midterm and 1 final | Assesses operational reasoning rather than memorized commands |
| Assessment system | 6 resources | Includes diagnostic/post instruments, retrieval practice, writing, rubrics, and an assessment map |
| Student presentations | 15 decks, 214 slides | Supplies a coherent visual course rather than unrelated weekly presentations |
| Spoken presentation text | 15 exact transcripts, approximately 25,000 words | Gives every slide a complete word-for-word script and structured-text alternative |
| PDF handouts | 15 | Provides a convenient slide-study format with accurately documented limitations |
| Instructor implementation | 15 lesson plans in one guide plus 4 cross-course guides | Lets another instructor adopt the course without reverse-engineering it |
| Publication formats | Markdown, standalone HTML, EPUB, Word, and source package | Supports reuse, editing, web publication, and Pressbooks import |
| QA infrastructure | Automated structural, link, code, data, slide, privacy, and publication checks | Makes the resource maintainable rather than a one-time folder dump |

The full authoritative inventory is the
[Catalog of Created OER](../OER_CATALOG.md). Free vendor tools and tutorials are
tracked separately in the
[Free External Resource Catalog](../FREE_EXTERNAL_RESOURCES.md) and are not
misrepresented as fellowship-created OER.

## The Student Problem This Solves

The redesign responds to four connected problems.

1. Students arrive in database administration having forgotten relational
   concepts and basic SQL.
2. Existing materials often jump directly into administration commands or cloud
   dashboards without rebuilding the mental model underneath them.
3. PostgreSQL, Supabase, MongoDB, Atlas, JSON, MQL, security, recovery, and
   performance are often taught as disconnected product tutorials.
4. Students need work they can explain in an interview, not a collection of
   screenshots proving that they clicked through a vendor interface.

The course therefore starts with a substantial relational-model, relational-
algebra, and SQL re-entry sequence. It then asks students to use those concepts
to operate systems, inspect evidence, and justify decisions.

## The Original Design Idea

The recurring professional cycle is:

1. **Name the promise.** What should the database guarantee or make possible?
2. **Inspect evidence.** What do schema metadata, query results, plans, locks,
   logs, permissions, or restore tests show?
3. **Make one controlled change.** Change one variable rather than guessing.
4. **Verify the result.** Prove the intended behavior and check for side effects.
5. **Explain the decision.** State the evidence, tradeoff, and scope in language
   another person can evaluate.

This cycle appears in schema work, permissions, indexes, transactions, backup
and restore, MongoDB modeling, reliability, scale, incidents, and career
writing. That repeated structure is a central original contribution of the OER.

## The 15-Week Course Story

### Phase 1: Rebuild the Foundation, Weeks 1-3

- Week 1 establishes professional responsibility, evidence, relational grain,
  keys, and the difference between data and a claim about data.
- Week 2 provides the major relational algebra and SQL review: selection,
  projection, joins, grouping, set operations, safe updates, and result-grain
  verification.
- Week 3 turns that review into schema, constraint, metadata, and expected-
  failure reasoning.

This phase is deliberately more than a quick SQL recap. Students predict a
result, execute a query, inspect what happened, and explain why.

### Phase 2: Operate PostgreSQL, Weeks 4-8

- Week 4 covers views, identity, dependencies, and reversible schema change.
- Week 5 covers transactions, MVCC, locks, blocking, and two-session evidence.
- Week 6 covers identity, least privilege, grants, row-level security, and
  credential safety.
- Week 7 covers query plans, measurement, index experiments, and remeasurement.
- Week 8 covers logical backup, independent restore, verification, and the
  midterm synthesis.

This phase teaches administration as evidence-based change, not command
memorization.

### Phase 3: Understand and Operate Document Systems, Weeks 9-13

- Week 9 explains NoSQL history, key-value, wide-column, document, graph, and
  vector models; JSON; basic graph theory; and cosine similarity.
- Week 10 covers Atlas boundaries, basic MQL, CRUD evidence, arrays, nested
  fields, embedding, and referencing.
- Week 11 connects aggregation, validation, index order, sorting, and explain
  evidence.
- Week 12 covers replication, read/write concerns, reliability promises, and
  logical MongoDB recovery.
- Week 13 covers capacity, sharding, shard-key risk, Python integration, and
  public-data evidence.

This phase does not frame MongoDB as a replacement for SQL. Students choose a
model from workload, ownership, growth, atomicity, and access-pattern evidence.

### Phase 4: Integrate and Communicate, Weeks 14-15

- Week 14 uses a polyglot incident to examine source of truth, dual-write
  failure, outbox reasoning, idempotency, reconciliation, and repair direction.
- Week 15 turns technical evidence into a safe GitHub artifact, portfolio
  language, interview explanations, and final-project communication.

The final phase makes career communication part of technical competence rather
than an unrelated end-of-semester add-on.

## What Makes the Pedagogy Defensible

Do not present the project as "I made a lot of files." Present the files as the
implementation of specific learning-design decisions.

| Learning-design decision | How the course implements it |
|---|---|
| Activate and retrieve prior knowledge | Weekly retrieval prompts and a paired diagnostic/post-course inventory revisit core concepts |
| Rebuild before increasing complexity | Weeks 1-3 restore relational, algebraic, and SQL reasoning before administration assumes fluency |
| Move from model to independent practice | Worked examples are followed by partially supported and then individual tasks |
| Use active disciplinary work | Students predict, query, inspect, test, compare, repair, and explain during class |
| Keep formative work manageable | Each lab asks for one bounded submission rather than a pile of screenshots |
| Use authentic evidence | Students interpret plans, locks, constraints, permissions, restore output, document shapes, and incident records |
| Support multiple access paths | Markdown, HTML, EPUB, Word, slides, transcripts, notebooks, cloud routes, and local fallbacks preserve the learning goal |
| Connect learning to employment | Writing asks for claims, evidence, tradeoffs, incident explanations, project decisions, and interview language |
| Use real data safely | Synthetic recurring cases support repetition; a documented CISA sample adds public-data complexity without exposing private people |

The supporting research and course implementation mapping are documented in the
[Currentness, Pedagogy, and QA Audit](CURRENTNESS_PEDAGOGY_QA_AUDIT.md).

## What Makes the Course Industry-Relevant

The industry value is not simply that students touch two cloud products.
Students practice transferable work:

- relational modeling and SQL verification;
- PostgreSQL schema, transaction, permission, performance, and recovery work;
- Supabase connection and managed-service boundaries;
- JSON and document-model reasoning;
- MongoDB Atlas, MQL, aggregation, validation, indexes, replication, and logical
  recovery;
- GitHub editing, versioned evidence, and credential-safe publication;
- Python database connections with bounded waits and cleanup;
- public-data ingestion and capacity reasoning;
- incident analysis, idempotency, reconciliation, and source-of-truth decisions;
- concise technical writing for administrators, developers, managers, and job
  interviews.

Product interfaces can change. The course therefore teaches stable concepts and
evidence patterns, then links current no-cost vendor resources for interface-
specific practice.

## What Is Genuinely OER and What Is Not

### Created or Adapted OER

- original modules, guides, labs, assignments, assessments, scripts, lesson
  plans, and explanatory notebook text;
- original code under the MIT License;
- original synthetic datasets under CC0;
- compatible adaptations with source-specific notices; and
- editable source files and publication formats.

### Free but Not Claimed as Created OER

- MongoDB University activities;
- Atlas, Supabase, GitHub, and Colab accounts or interfaces;
- official PostgreSQL, MongoDB, Supabase, GitHub, and Python documentation; and
- external videos, research, and vendor tutorials.

The project is zero-cost to students, but it does not pretend that every free
link has an open license.

## What the Most Recent Three-Hour Run Actually Did

The most recent run was **not three hours of authoring new semester content**.
The semester content had already been created in the earlier release-candidate
commits. The run was release engineering, evidence collection, and claim
correction.

| Work completed in the run | Result |
|---|---|
| Re-audited the complete package | Confirmed the authored inventory and separated locally completed work from external fellowship gates |
| Corrected all PowerPoint metadata | Replaced generic exporter titles and authors with the actual week title, `Atilio Barreda`, `en-US`, course subject, and release-candidate status |
| Regenerated all 15 PDF handouts | Preserved all visible slide content while carrying corrected metadata into the PDFs |
| Compared every PDF page with the previous version | All 214 pages were pixel-identical at 96 DPI; no layout changed |
| Inspected the PDF tag trees | Found that the exporter supplied only weak `Figure`, `Div`, and `P` semantics and no figure alternative metadata |
| Corrected the accessibility claim | Labeled PDFs as convenience handouts, not accessible PDFs; retained Markdown and transcripts as authoritative structured alternatives |
| Independently validated the EPUB | Official W3C EPUBCheck 5.3.0 returned zero errors, warnings, or informational messages under EPUB 3.3 rules |
| Replaced unreliable research links | Switched bot-blocked or intermittently unavailable routes to accessible authoritative records from PMC, ERIC, Amazon Science, and Debian Sources |
| Rebuilt publication exports | Regenerated HTML, EPUB, Word, and SHA-256 checksums from canonical Markdown |
| Rechecked the 90-page Word export | Only page 55 changed because of the intentional source-link replacement; the page was visually inspected and remained correctly formatted |
| Strengthened the validator | Expanded local checks from 306 to 383, including exact presentation/PDF title, author, language, status, and catalog metadata |
| Re-ran live link QA | 385 checks passed across 139 URLs with no 404/410; the one BLS bot refusal passed browser review |
| Avoided irrelevant or unauthorized workflows | No screen-reader session, external-account login, remote push, release tag, Pressbooks import, deposit, or publication was performed |

The run ended in local commit `22790f3`, **Improve publication format QA and
metadata**.

## How to Present the Project

### Do Not Begin With Counts

Do not open with "I made 15 modules and 25 labs." Begin with the student problem
and design response. Use counts later as evidence that the response is complete.

Recommended opening sequence:

1. The students' SQL and relational foundation was not reliable enough for an
   administration course.
2. Available free resources were useful but fragmented across products.
3. The redesign created one coherent learning progression around operational
   evidence.
4. The deliverable is a complete course system, not a textbook alone.
5. The remaining fellowship work is review, pilot evidence, revision, and
   approved publication.

## Recommended Ten-Slide Presentation

### Slide 1: Operating Cloud Databases

**On the slide:** Project title, CST 4714, your name, and the sentence "A
lab-first bridge from relational reasoning to cloud database operations."

**Say this:**

"My project is a full redesign of CST 4714 Database Administration called
Operating Cloud Databases. It is a zero-cost, lab-first course that begins by
rebuilding relational and SQL reasoning, then asks students to operate,
troubleshoot, secure, recover, and explain PostgreSQL and MongoDB systems. The
central idea is that database administration should be taught as evidence-based
decision making, not as memorizing commands or clicking through a cloud
dashboard."

### Slide 2: The Student Problem

**On the slide:** Four short phrases: forgotten SQL, weak mental models,
fragmented tutorials, and screenshot-based evidence.

**Say this:**

"The redesign began with a practical teaching problem. Students were entering
database administration without a dependable command of relational concepts or
basic SQL. At the same time, the available no-cost materials treated SQL,
PostgreSQL administration, cloud platforms, MongoDB, and JSON as separate
tutorials. Students could sometimes reproduce steps, but they had difficulty
explaining what the system promised, what evidence showed, or why a change was
appropriate. I designed the course to rebuild that reasoning before increasing
the technical complexity."

### Slide 3: The Course Design

**On the slide:** Promise -> Evidence -> Controlled change -> Verification ->
Explanation.

**Say this:**

"Every major topic uses the same professional cycle. Students first name the
promise, such as a permission boundary, a performance expectation, or a recovery
claim. They inspect evidence, make one controlled change, verify the outcome,
and explain the tradeoff. Repeating this cycle across SQL, constraints,
transactions, indexes, backup, document modeling, replication, and incidents
helps students transfer a stable method instead of memorizing unrelated product
features."

### Slide 4: The Learning Progression

**On the slide:** Four bands: Foundation, PostgreSQL Operations, MongoDB and
Documents, Integration and Careers.

**Say this:**

"The first three weeks rebuild relational grain, keys, algebra, SQL, schema, and
constraints. Weeks four through eight apply that foundation to PostgreSQL views,
transactions, security, performance, and recovery. Weeks nine through thirteen
explain why NoSQL models exist, introduce JSON and document modeling, and build
toward MongoDB aggregation, validation, reliability, recovery, capacity, and
Python integration. The last two weeks connect polyglot incident reasoning to
portfolio and interview communication."

### Slide 5: What Students Actually Do

**On the slide:** Predict, execute, inspect, decide, explain.

**Say this:**

"Students do not spend the semester watching demonstrations. They predict query
results, execute and verify SQL, inspect schema metadata, reproduce a blocking
incident, compare query plans, restore a database independently, design more
than one valid JSON representation, choose embedding or referencing from an
access pattern, analyze an aggregation and index, and explain an incident or
design decision in career-relevant language. Each lab is individual and asks for
one manageable, checkable artifact."

### Slide 6: Scope of the OER

**On the slide:** Use only the largest categories: 15 modules, 25 labs, 6
notebooks, 3 datasets, 15 decks/214 slides, and complete implementation package.

**Say this:**

"The primary OER is a fifteen-module open textbook and lab manual. Around it I
built fifteen two-class weekly guides, twenty-five individual labs, six
executable notebooks, three reusable data packages, a midterm and final project,
a complete assessment system, fifteen student-facing slide decks containing 214
slides, exact word-for-word scripts and transcripts, and an implementation guide
with a lesson plan for every week. The package is available as editable Markdown
and as HTML, EPUB, and Word for publication and reuse."

### Slide 7: Pedagogy and Access

**On the slide:** Retrieval, worked examples, active practice, formative
evidence, multiple formats, and local fallbacks.

**Say this:**

"The instructional design is grounded in active STEM learning, retrieval
practice, worked examples with faded support, formative evidence, and multiple
ways to access or demonstrate learning. Students receive structured text,
slides, full transcripts, notebooks, and equivalent local or static paths when
a cloud account creates a barrier. The goal is not to lower the technical
standard. It is to remove access friction while preserving the same reasoning
and evidence requirement."

### Slide 8: Industry and Career Relevance

**On the slide:** PostgreSQL, Supabase, MongoDB Atlas, MQL, JSON, GitHub, Python,
recovery, security, performance, and incident writing.

**Say this:**

"The course uses current no-cost platforms, but the durable skills are broader
than the products. Students practice relational and document modeling,
credential-safe connections, least privilege, transaction and lock evidence,
query-plan analysis, backup and recovery, aggregation, validation, index design,
reliability, capacity, and incident communication. They finish by translating
bounded technical evidence into a GitHub artifact and an interview explanation
without exposing credentials or exaggerating production experience."

### Slide 9: Quality and Reusability

**On the slide:** Editable source, licenses, automated checks, executed code,
validated formats, and documented limitations.

**Say this:**

"I treated this as a maintainable publication rather than a folder of files.
Original instructional material has a visible open license, original code is
MIT licensed, synthetic data is CC0, and free external resources are tracked
separately rather than claimed as OER. The current candidate passes 383 local
checks. Notebook offline paths and PostgreSQL fixtures execute, links are
audited, slide notes match transcripts, all 214 slide handouts were visually
compared, and the EPUB passes official EPUBCheck. Known limitations, including
the weak PDF tag semantics, are documented rather than hidden."

### Slide 10: Current Status and Fellowship Work

**On the slide:** Authored release candidate -> external review -> classroom
pilot -> evidence-based revision -> approved publication.

**Say this:**

"The authored course is complete as a release candidate, but I am not claiming
that the fellowship process is finished. The next work is OER and accessibility
review, private Pressbooks import and export inspection after approval, live
platform smoke testing, classroom implementation, analysis of aggregate student
evidence, revision in response to that evidence, and approved public deposit.
That distinction lets me show substantial completed authorship while keeping the
remaining fellowship work honest and meaningful."

## Thirty-Second Script

"I redesigned CST 4714 as Operating Cloud Databases, a complete zero-cost,
lab-first course. It begins with a major relational algebra and SQL rebuild,
then teaches PostgreSQL and MongoDB administration through a repeated cycle of
naming a system promise, inspecting evidence, making one controlled change, and
verifying the result. The release candidate includes fifteen textbook modules,
twenty-five individual labs, six notebooks, three datasets, a complete
assessment and project system, fifteen slide decks with exact scripts, and
instructor implementation guidance. The remaining fellowship work is external
review, classroom piloting, evidence-based revision, and approved publication."

## Two-Minute Script

"My fellowship project addresses a problem I saw in CST 4714 Database
Administration. Students were expected to reason about permissions,
transactions, performance, recovery, and cloud databases, but many had forgotten
the relational model and basic SQL. The no-cost resources available to them were
useful, but they were fragmented across PostgreSQL, Supabase, MongoDB, Atlas,
JSON, and vendor tutorials.

I redesigned the course as Operating Cloud Databases. The first three weeks
rebuild relational grain, keys, relational algebra, SQL, schemas, and
constraints. Students then apply that foundation to PostgreSQL transactions,
security, indexes, performance evidence, backup, and restore. The second half
explains why NoSQL models exist and develops JSON, MQL, document modeling,
aggregation, validation, reliability, recovery, scale, and Python integration.
The final weeks connect polyglot incident reasoning to portfolio and interview
communication.

The course uses one repeated professional cycle: name the promise, inspect
evidence, make one controlled change, verify the result, and explain the
tradeoff. That cycle is implemented in fifteen open-text modules, twenty-five
individual labs, six executable notebooks, three data packages, two major
projects, a complete assessment system, fifteen slide decks with 214 slides and
exact scripts, and public instructor guidance.

The course is zero-cost, but I distinguish created OER from free external
resources. It also includes editable source, multiple reading formats, local
fallbacks, licensing and attribution records, and automated quality checks. It
is now a complete authored release candidate. The remaining fellowship work is
external review, Pressbooks inspection after approval, classroom piloting,
evidence-based revision, and formal publication."

## Five-Minute Script

"I want to begin with the teaching problem rather than the file count. CST 4714
asks students to make decisions about database administration, but students do
not always enter the course with a reliable command of relational concepts or
basic SQL. They may remember isolated commands without being able to predict the
grain of a result, explain what a join changes, or verify that an update was
safe. At the same time, the available free materials tend to separate SQL,
PostgreSQL administration, cloud platforms, MongoDB, and JSON into unrelated
product tutorials.

My response was to redesign the whole course as Operating Cloud Databases. The
course begins with a substantial relational and SQL re-entry sequence. Students
rebuild relations, tuples, attributes, keys, selection, projection, joins,
grouping, set operations, and safe data modification. That foundation is then
used to understand schemas, constraints, views, transactions, locks, identity,
permissions, query plans, indexes, backup, and recovery in PostgreSQL and
Supabase.

The second half does not present MongoDB as a fashionable replacement for SQL.
It begins with the history and motivations of NoSQL and compares key-value,
wide-column, document, graph, and vector models. Students learn strict JSON and
see that the same relational source can have more than one valid document
representation. They then use access patterns, ownership, atomicity,
duplication, and growth to choose embedding or referencing. Later work connects
MQL, aggregation, validation, index design, replication, recovery, capacity,
sharding, and Python integration.

The unifying design is a repeated professional evidence cycle. Students name a
promise, inspect evidence, make one controlled change, verify the result, and
explain the decision. For example, they do not merely create an index. They state
the query question, inspect the original plan, form a hypothesis, add one index,
remeasure, and explain the cost. They do not merely create a backup. They restore
it into a separate destination and verify behavior. They do not merely draw a
MongoDB document. They defend the boundary using the reads, writes, ownership,
and growth of the workload.

The completed release candidate includes fifteen open-text modules, fifteen
weekly guides for two class meetings each, twenty-five individual labs, fifteen
optional industry extensions, six executable notebooks, three reusable data
packages, a midterm and final, a complete assessment system, fifteen
student-facing decks with 214 slides, exact word-for-word scripts and
transcripts, and an instructor implementation guide with a lesson plan for every
week. The book can be edited in Markdown and built as HTML, EPUB, or Word.

The pedagogy uses active practice, retrieval, worked examples with fading
support, small formative artifacts, and career-connected technical writing. The
course also provides local or static alternatives when a cloud platform is
unavailable. That keeps the outcome consistent without making a paid plan or a
successful vendor login the real assessment.

I also treated licensing and maintainability as part of the project. Original
instructional prose and slides carry an open license, code is MIT licensed,
synthetic datasets are CC0, and linked vendor materials are cataloged separately
instead of being counted as created OER. Automated checks cover inventory,
links, notebooks, data, SQL, credentials, slides, notes, transcripts, and
publication exports. The EPUB passes official EPUBCheck, and known limitations
are recorded honestly.

This is a complete authored release candidate, not a claim that the entire
fellowship process is finished. The remaining work is external OER and
accessibility review, private Pressbooks testing after approval, live platform
smoke testing, classroom use, analysis of aggregate student evidence, revision,
and approved publication. That next phase will let me evaluate not only whether
the materials exist, but how well they support actual students."

## Best Live Demonstration Route

Do not scroll through the entire repository. Show one example of each layer.

1. Open the [course homepage](../README.md) to establish the coherent 15-week
   sequence.
2. Open [Module 2](../textbook/module_02_sql.md) to show the substantial SQL and
   relational-algebra rebuild.
3. Open the [Week 2 SQL Query Ladder](../week_02/lab_01_sql_query_ladder.md) to
   show the individual, evidence-based lab format.
4. Open the [Relational and SQL Review notebook](../notebooks/01_relational_sql_review.ipynb)
   to show executable instruction rather than static prose alone.
5. Open the [Week 9 NoSQL and JSON module](../textbook/module_09_nosql_json.md)
   and [CSV-to-JSON lab](../week_09/lab_01_csv_to_json.md) to show the bridge from
   relational thinking to multiple valid document models.
6. Open one [PowerPoint deck](../week_09/week_09_nosql_models_json.pptx) and its
   [exact transcript](../week_09/week_09_nosql_models_json_transcript.md) to show
   the student-facing media and complete script.
7. Open the [Implementation Guide](../instructor/implementation_guide.md) to show
   that another instructor can teach the course.
8. End with the [OER Catalog](../OER_CATALOG.md) and
   [External Review and Release Gates](EXTERNAL_REVIEW_AND_RELEASE_GATES.md) to
   distinguish completed authorship from pending fellowship work.

## Questions You Are Likely to Receive

### "Is this a textbook or a course shell?"

"It is a modular open textbook and lab manual surrounded by a complete course
implementation package. The OER remains portable and editable outside any one
LMS. Weekly guides organize two class meetings, but Brightspace is not the
canonical source."

### "What is original about it?"

"The original contribution is the coherent beginner progression and repeated
evidence cycle, not the existence of SQL or MongoDB documentation. I authored
the explanations, recurring cases, worked examples, labs, assessments, scripts,
lesson plans, fallback paths, and career communication tasks that turn public
technical knowledge into a teachable course."

### "Why cover both PostgreSQL and MongoDB?"

"The comparison teaches model selection rather than product loyalty. Students
first rebuild relational reasoning, then learn why a document model may serve a
specific workload. They must justify either choice using access patterns,
ownership, integrity, growth, atomicity, recovery, and operational evidence."

### "How does the project help students get jobs?"

"Students leave with practice in SQL, PostgreSQL, MongoDB, JSON, MQL, GitHub,
Python connections, security, performance, backup, recovery, and incident
reasoning. More importantly, they practice translating one bounded piece of
technical evidence into a clear claim for a project review, incident note,
portfolio, or interview."

### "What happens if a student cannot access Atlas or Supabase?"

"The cloud platform is a practice environment, not the learning outcome. Labs
include local, static, or simulated evidence paths that preserve the same
decision and explanation. No paid plan is required."

### "How do you know the materials work?"

"I can currently demonstrate technical and design quality, not yet student
learning gains. The files, code paths, links, slides, scripts, data, and
publication exports have substantial local QA. The fellowship pilot uses a
diagnostic/post instrument, completion evidence, access feedback, and a revision
record. I will make learning-effectiveness claims only after actual classroom
evidence exists."

### "Is everything in the package OER?"

"No. The created and adapted instructional materials are cataloged and licensed
as OER. Free vendor resources such as MongoDB University and cloud interfaces
are linked and tracked separately. Zero cost and open licensing are related but
not identical."

### "Is it published?"

"No. It is a complete authored release candidate. Publication is intentionally
withheld until approval, platform review, fellowship review, and the authorized
release process."

### "Why is more fellowship work needed if the files already exist?"

"Authorship is only one phase of responsible OER work. The remaining work is
external review, Pressbooks transformation review, classroom implementation,
student evidence, evidence-based revision, accessibility checks in the actual
publication environment, and approved dissemination."

## Claims to Make

- "This is a complete authored 15-week release candidate."
- "This is a full-course transformation, not a replacement reading list."
- "The course includes a major relational algebra and SQL rebuild."
- "Every required lab is individual and produces one manageable artifact."
- "Every deck has complete spoken prose in its notes and a matching transcript."
- "Created OER and free external resources are tracked separately."
- "Local technical QA is complete for the candidate."
- "External review, classroom evidence, revision, and publication remain."

## Claims Not to Make

- Do not say that the project has already been approved, peer reviewed,
  classroom validated, deposited, or published.
- Do not say that student learning improved before collecting actual evidence.
- Do not claim that MongoDB University, vendor documentation, or cloud platforms
  are fellowship-created OER.
- Do not call the PDF handouts accessible PDFs; use the structured Markdown and
  transcripts as the authoritative alternatives.
- Do not promise a particular stipend amount.
- Do not claim a specific number of full-time development months unless real
  contemporaneous records support it.

## Before Any Presentation

1. Choose the required length: 30 seconds, 2 minutes, 5 minutes, or the ten-slide
   structure.
2. Lead with the student problem and evidence cycle, not the inventory count.
3. Demonstrate only two or three representative artifacts.
4. Keep the created-OER/free-resource distinction visible.
5. End with the honest release-candidate boundary and next fellowship phase.
6. Never improvise a publication, approval, accessibility, or learning-gain
   claim beyond the evidence recorded here.
