# What I Am Creating for the OER Fellowship

**Instructor's presentation guide, updated September 8, 2026.** This is a private
reporting aid, not a student assignment. The fellowship work is still a local
draft under substantive revision. It has not been approved for publication.

## The Short Answer

> I am developing *Operating Cloud Databases*, an open textbook with a coordinated
> set of individual labs, educational notebooks, in-class writing activities,
> and teaching materials for CST4714. It builds on my earlier course, but adds a
> coherent progression from relational and SQL foundations to cloud database
> operations. Students learn a concept, study a worked example, test a change,
> and explain what the result means. The new textbook and supporting resources
> are the fellowship contribution; vendor courses and earlier course materials
> are identified separately.

For a meeting, open the [current textbook PDF](../course/textbook/publishing/exports/operating_cloud_databases_second_edition_draft.pdf)
or [editable Word edition](../course/textbook/publishing/exports/operating_cloud_databases_second_edition_draft.docx).
The book has fifteen chapters; the current review PDF has 161 pages. Its
mathematical notation, numbered code listings, diagrams, and captioned platform
screenshots are part of the book itself, not just a separate collection of
Markdown files. The [quality record](evidence/FELLOWSHIP_SCOPE_EVIDENCE.md) states
which checks are complete and which remain.

## What Is New, Revised, or External?

| Material | How to describe the contribution | Where to show it |
|---|---|---|
| Open textbook | A newly authored textbook developed from the course's subject matter, with substantial current revisions to explanations, worked examples, notation, research context, and code. Its chapters and formats are one work, not several books. | [Textbook and editable/exported formats](../course/textbook/README.md) |
| Integrated labs and writing | New or substantially redesigned teaching activities built from prior classroom experience and course cases. The revision removes missing prerequisites, unnecessary submissions, and unexplained technical jumps. | [Weekly course map](../course/README.md#weekly-course-map), [writing guide](../course/assessments/critical_writing.md) |
| Educational notebooks | Authored explanatory prose, executable examples, student modifications, synthetic fixtures, safe connection paths, and explicit local alternatives. Several revise earlier notebook ideas; the new aggregation/validation notebook is an additional resource. | [Seven-notebook collection](../course/notebooks/README.md) |
| Slides and instructor guidance | A coherent revision of teaching materials, not a claim that all topics or all earlier slides originated in the fellowship. Notes, figures, examples, sequencing, and adoption guidance are identifiable authored contributions. | [OER catalog](../course/OER_CATALOG.md) |
| Earlier semester materials | The prior teaching baseline, retained for comparison and reuse. Do not count unchanged copies as newly authored fellowship output. | [Preserved Spring 2026 course](../archive/spring_2026/) |
| Earlier OER draft | A previous version of the same developing textbook. A revised edition is not fifteen additional original modules. | [First-edition source](../archive/oer_first_edition/textbook/README.md) |
| MongoDB educator decks, University labs, documentation, platforms | External educational resources, retained because they help students. Course-authored introductions and response prompts are separate contributions; the underlying vendor material is not ours. | [Free external resources](../course/external_resources/INDEX.md) |
| CISA data sample | A documented selection and transformation of public source data, not an original collection of vulnerability records. | [Dataset provenance](../course/datasets/cisa_kev_sample/README.md) |

The [deliverable register](planning/OER_DELIVERABLE_REGISTER.md) defines this
boundary. The [OER catalog](../course/OER_CATALOG.md) is the single inventory for
counts. There are currently 15 chapter drafts, 24 individual labs, and seven
notebooks. Those counts describe files that exist, not resources certified as
ready to publish. Drafts, tested examples, reviewed exports, and classroom-tested
materials are different completion states.

## Show One Coherent Learning Sequence

A reviewer should be able to follow the learning, not just browse many files.

**Foundations:** Open [Chapter 2](../course/textbook/module_02_sql.md), then the
[Week 2 join lab](../course/weeks/week_02/lab_02_joins_aggregates_dml.md).
Explain the connection between relational operations, the query's unit of
counting, and a report that must preserve staff with no assigned work.
The [Week 2 deck](../course/weeks/week_02/week_02_relational_algebra_sql_review.pptx)
teaches this with actual SQL and a complete resolved-ticket example. Students
adapt it to active work in the lab. The chapter supplies the explanation, the
slides support the demonstration, and the lab asks for a different result.

**The next step, from a correct query to dependable stored data:** Open
[Chapter 3](../course/textbook/module_03_schema.md), then the
[Week 3 deck](../course/weeks/week_03/week_03_schemas_constraints_integrity.pptx).
The chapter explains why current facts belong in one place and what constraints
can guarantee. Slides 15-18 work through an allowed-priority rule, a rejected
update, an accepted update, rollback, and the separate role of `NOT NULL`.
Students then [adapt the rule to status](../course/weeks/week_03/lab_02_integrity_constraints.md).
Their short SQL-file explanation connects a misspelling to a missing report
result and identifies a limit: the vocabulary does not decide who may close a
ticket. This is one lab with an integrated explanation, not several deliverables.

**Changing a working database:** [Week 4](../course/weeks/week_04/README.md)
connects Chapter 4 to a complete view-and-identity demonstration and a required-field
migration. Students first see the SQL and its result, then adapt a requester join
to an optional assignee. The second lab adds `source_channel`, rehearses rollback,
and tests accepted and rejected values. Its short writing asks why historical
rows must remain `unknown` and why a later repair should preserve newly collected
facts. This is an accessible technical and ethical decision grounded in their
own experiment, not a generic workplace reflection. Each day requires one SQL
file, and the deck contains the instructor's word-for-word teaching script.

For a concise demonstration to the fellowship committee, show the reading,
slide 14's complete rehearsal, and the lab's final explanation prompt together.
The authored contribution is the explanation, worked case, teaching sequence,
adaptation, and assessment. PostgreSQL's features themselves are not original
research, and the retained Supabase screenshot is a dated interface illustration.

**A later application of the same idea:** Open
[Notebook 07](../course/notebooks/07_aggregation_validation.ipynb), then
[the Week 11 lab](../course/weeks/week_11/lab_01_pipeline_validation.md).
Unwinding events produces the same total as the number of active tickets, but
duplicates one ticket and removes another. Students have to understand what each
record represents, not merely accept a plausible total.

**A controlled experiment with a professional explanation:**
[Week 5](../course/weeks/week_05/README.md) teaches transactions using a ticket
assignment and its history record. The first individual lab tests commit,
rollback, and a duplicate-key failure in one SQL file. On the second day,
[Notebook 02](../course/notebooks/02_postgres_transactions_locks.ipynb) opens
clearly labeled connections and captures a real lock wait. Students predict the
effect of changing one setting, compare the final rows from rollback and commit,
and write a short update to the developer inside that same notebook. The reading
explains the mechanism; the 23-slide deck includes complete SQL, diagrams,
visible results, and a word-for-word script. This is an authored teaching
experiment and integrated writing task, not a claim to have invented database
transactions. Both experiment branches have been executed locally; current
hosted Supabase behavior remains a separate check.

**Professional interpretation:** Open
[the writing guide](../course/assessments/critical_writing.md). Show how a short
explanation is embedded in the technical submission. Students explain specific
results in plain language; they do not write an additional generic reflection.

**Security without assuming application-development experience:**
[Week 6](../course/weeks/week_06/README.md) starts with a reader who needs a
report but must not edit tickets or read resident email. The deck teaches the
role and grants before students write their own grouped report. Day 2 uses
four rows to explain ownership. Students test both residents, request another
resident's ticket directly, then add a new row and rerun the same policy.
Their one SQL submission includes a short developer update explaining the
visible IDs and the real-login test still needed. The newly authored teaching
sequence, demonstrations, diagrams, script, and assessment are identifiable
contributions. PostgreSQL RLS and Supabase documentation remain external sources.
The 24-slide deck and PDF have been individually reviewed; 39 local checks cover
the actual demonstration, lab SQL, and display code. Hosted user-token behavior
is not counted as tested.

**Performance as an explanation, not a speed contest:**
[Week 7](../course/weeks/week_07/README.md) connects Chapter 7's plan-reading
explanation and diagrams to two individual experiments. First, students reduce
the requested output from twenty rows to five and inspect whether scanning also
decreases. Next, they test a composite index, preserve the exact result IDs,
measure storage, and write a brief recommendation in the same SQL submission.
The instructor demonstrates a different partial index, including a query it
cannot serve. The 24-slide deck contains captured results and a complete spoken
script; its code and the student variants passed 35 local checks. The fellowship
contribution is this authored explanation, counterexample, tested teaching
fixture, and aligned assessment, not PostgreSQL's indexing technology. It does
not claim measured student gains or production performance.

**Recovery as a testable claim:** [Week 8](../course/weeks/week_08/README.md)
connects Chapter 8 to a three-table PostgreSQL restore. The 24-slide deck teaches
the commands, expected results, and a counterexample: changing a ticket's subject
preserves every row count. Students adapt one known-ticket query and write a
short recovery account in the same notebook. The authored contribution includes
the beginner explanation, executable fixture, failure tests, safe cleanup, spoken
script, and aligned writing prompt. The notebook has been tested locally and in
a Linux root/sudo environment, which is distinct from testing hosted Colab.
Day 2 connects recovery to earlier transaction, permission, and indexing work
without adding another assignment. The midpoint project requirements are unchanged.

**The same facts, different document designs:**
[Week 9](../course/weeks/week_09/README.md) connects the relational case to
NoSQL models without requiring students to learn a new query language first.
The revised 32-slide deck teaches key-value and wide-column access, directed
graphs and traversal, vector similarity with actual calculations, and JSON
syntax. The chapter and slides then show complete referenced and embedded
representations of ticket 1001, preserving the same people and both events.
Students adapt the reasoning to ticket 1003 and its three events. They submit
two JSON examples and one short explanation in a single Markdown file.

For a fellowship demonstration, show the [worked book example](../course/textbook/module_09_nosql_json.md),
slides 24-28, and the [individual lab](../course/weeks/week_09/lab_01_csv_to_json.md).
The original contribution is the matched-case explanation, illustrations,
spoken script, instructional progression, and assessment. The test suite checks
that the alternative representations really retain the same facts, rather than
merely looking plausible. GitHub and MongoDB University remain external tools;
their content is not counted as our authorship. These are tested examples and
reviewed exports, not yet measured student learning outcomes.

**A document design that changes with the workload:**
[Week 10](../course/weeks/week_10/README.md) teaches exact Python queries and
their results before students adapt them. A small array counterexample exposes
conditions that match different events. Repeating an update distinguishes a
matched document from a changed one. Day 2 then changes Week 9's requirement:
show the latest two events while retaining all history and keeping current
contact details editable in one place. Students explain one JSON design in one
Brightspace response after a specific MongoDB University activity. The instructor
demonstrates another lesson rather than completing their assigned activity.
The revised 28-slide deck has 6,332 spoken words, matching handouts, and tested
examples. The open notebook and authored modeling prompt are course contributions;
MongoDB University's lessons and Practice content remain external resources.
Local execution and visual checks are recorded separately from the untested
hosted Atlas/Colab route and account-gated activity completion.

Chapter 10 now follows that design through complete shell examples: read the
ticket, find its current contact, fetch its newest two events, correct the email
once, and append another event without losing older history. Its explanation
connects the model to update ownership, deterministic ordering, index cost, and
document growth. The example is in the editable Word, PDF, HTML, and EPUB editions.

**A report can have the correct total and still be wrong:**
[Week 11's notebook and lab](../course/weeks/week_11/lab_01_pipeline_validation.md)
ask students to inspect the source identities behind a category count. Expanding
events duplicates one request and loses another while preserving both the grand
total and category totals in this deliberately constructed case. Students then
add urgency and newest opening, and test a date requirement with positive and
negative examples. The notebook is the one submission. Local aggregation and a
supplied validation trace are distinguished from actual MongoDB enforcement.

The instructor guide provides a separate sort-index experiment whose returned
IDs and examined-document counts were tested on local MongoDB. Students do the
linked University sort lab instead of repeating that exact live demonstration,
then write a brief inventory-case recommendation in Brightspace. The authored
counterexample, explanation, tests, fallback, and writing prompt are fellowship
contributions; the University lab and video are not. The revised 28-slide Week 11
deck teaches the same sequence with a word-for-word script, editable result
tables, and a pipeline diagram. Its exported examples were executed against a
local database, and every slide and PDF page was individually inspected. The
whole-course and textbook audits are still in progress; this is evidence of a
specific completed revision rather than a claim that the full release is ready.

**A restore can preserve the count while returning the wrong information:**
[Week 12's recovery notebook](../course/notebooks/05_mongodb_logical_recovery.ipynb)
exports five tickets, restores them into a separate target, and introduces one
incorrect subject. Students see why counts, IDs, and date types can all look
correct. They recover one document from the verified file parse and explain the
additional rules and environment information a colleague would need. The source
of the recovery value is visible, the code is short enough to follow, and the
assignment stays inside one notebook.

The authored contribution is the recovery counterexample, its typed-value
comparison, transparent repair, separately tested collection rules, and concise
professional recommendation. It extends the PostgreSQL recovery lesson rather
than replacing its terminology with MongoDB commands. The current notebook and
its two documented repair choices have been tested locally; the accompanying
Week 12 deck is still being revised. Do not present a pending slide revision as
a completed resource or count these repeated tests as student learning results.

These examples demonstrate continuity across relational and document models.
They also show why a beginner course can be intellectually demanding without
requiring advanced mathematics, complex software projects, or many deliverables.

## Why This Is a Substantial OER Project

The main contribution is a connected treatment of database administration that
another instructor can teach and modify. A continuing synthetic service-desk
case connects SQL foundations to document modeling, permissions, performance,
recovery, and synchronization. Students encounter increasingly consequential
problems using facts they already understand.

The intellectual work includes choosing counterexamples that expose plausible
errors, explaining the underlying mechanism, deciding what beginners need first,
and connecting each experiment to a professional decision. For example, a left
join can keep an unassigned request visible, while an event expansion can quietly
turn a ticket count into an event count. Both lessons develop the same habit:
identify what each result record represents before trusting the answer.

The reusable output includes the textbook, individual lab activities,
open-source notebook code, original synthetic teaching data, integrated writing
prompts, and instructor implementation guidance. Code is MIT-licensed; original
instructional prose is CC BY-NC-SA 4.0. Specific source notices identify exceptions.
Editable sources and supplied fixtures let adopters change the scenario without
rebuilding the course from scratch.

## What the Current Revision Actually Adds

- Chapters explain prerequisite concepts before asking students to apply them.
  For example, the SQL review develops NULL, row multiplicity, and outer joins;
  the schema chapter explains functional dependencies and normalization.
- Labs supply a starting fixture, worked example, one meaningful student change,
  and a way to check the result. Required tasks remain individual and in class.
- Writing asks students to reason about their own result or a supplied case.
  It does not require invented workplace experience or unexplained terminology.
- Technical QA includes actual isolated PostgreSQL and MongoDB executions,
  failure cases, and repeat imports, not only syntax inspection.
- Integration tests also follow the student reading-to-lab path. For example,
  separate textbook and lab view names now prevent one lesson from overwriting
  the other's column layout. Chapter 6 deliberately reuses the reading's view.
- The ongoing visual review covers the actual exported book and slides.
  Source revisions do not automatically make earlier PDF or Word copies current.

The dated [quality record](evidence/FELLOWSHIP_SCOPE_EVIDENCE.md) distinguishes
these executed checks from remaining work. Do not present an old screenshot,
page count, or validation receipt as a check of a newly changed artifact.

## How to Discuss the Funding Scope

Present the project as **a primary open textbook plus an integrated teaching and
assessment package**, and ask the OER team to assess that documented scope at the
appropriate funding level. The official 2026-27 call lists project stipends of
$1,300-$6,000 depending on scope, plus compensation for required professional
development. It does not promise a maximum award for a particular file count.
[City Tech fellowship call](https://openlab.citytech.cuny.edu/library/call-for-applicants-to-the-oer-fellowship-ay-26-27/)

A useful scope discussion identifies work still to perform during the award:
substantive authorship and revision, subject review, accessibility remediation,
technical testing, classroom implementation, documented revision, and approved
publication. You can ask directly:

> I would like this evaluated at the upper end of the fellowship's project
> funding range. The proposed deliverable is a primary textbook with coordinated
> open labs, notebooks, assessments, and adoption materials. I can show the
> earlier course baseline, the substantive additions, and the remaining review
> and implementation work. What scope and review milestones would you need to
> approve that level of support?

The award-period work record should distinguish preparatory drafts from later
funded revisions. Confirm the treatment of any previously supported material
with the fellowship team. The official call identifies substantive revision as
something to discuss with the OER librarian; compensation depends on the agreed
scope and applicable hourly calculation, not an inferred number of hours.
[City Tech fellowship call, checked September 7, 2026](https://openlab.citytech.cuny.edu/library/call-for-applicants-to-the-oer-fellowship-ay-26-27/)

## Status to State Aloud

> The full set of draft materials exists. I am strengthening the textbook,
> aligning instruction and assignments, testing the examples, and reviewing the
> exported formats. Some technical paths have been executed successfully; that
> is not the same as external review or classroom validation. The remaining
> fellowship work includes review, revision, implementation, and publication
> after approval.

Peer review, complete accessibility review, hosted-platform compatibility,
classroom outcomes, and publication remain separate milestones. The current
record reports executed checks rather than claiming those milestones are done.
The author retains editorial responsibility for reviewed AI-assisted drafts and
should follow the fellowship's disclosure requirements.

Nothing here authorizes a GitHub release, deposit, public textbook upload, or
account login. The minimal public class package and the unpublished fellowship
materials remain separate.
