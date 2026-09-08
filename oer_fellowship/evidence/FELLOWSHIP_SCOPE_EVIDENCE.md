# Fellowship Scope and Quality Evidence

**Administrative record, September 8, 2026.** This explains the project; it is not
an additional student OER. Earlier publication-format and interface checks remain
dated historical records in this folder. They do not certify revised source or
newly generated files.

## Current Finding

The project has the scope of a full-course textbook and instructional-package
redesign. The defensible funding argument is the integrated educational work,
not an unsupported superlative, file total, claimed labor duration, or promised
media recognition. The current course remains a **local draft undergoing
substantive revision**, not a completed, approved release.

The [presentation guide](../HOW_TO_PRESENT_THIS_PROJECT.md) gives a short account
of what is authored, revised, and external. The [OER catalog](../../course/OER_CATALOG.md)
is the canonical file inventory. Its current draft counts are 15 chapters, 24
individual labs, seven notebooks, 15 weekly guides, and two major projects.
Multiple formats of a chapter or a script do not multiply its authorship count.

## What Changed in This Audit

| Educational problem in the earlier draft | Substantive revision | Why it matters |
|---|---|---|
| SQL review assumed remembered foundations and sometimes used a different fixture from the lab | Explain relational operations, NULL, duplicate rows, outer joins, and safe changes; supply the exact full fixture in the review notebook | Students can reason before debugging unfamiliar tools |
| Schema material named constraints without sufficiently developing data design | Add functional dependencies, normal forms, lossless reconstruction, update anomalies, and the distinction between current and historical facts | Students learn why a design is useful, not only its syntax |
| A migration invented historical source values | Teach an honest unknown value, old-client compatibility, a rollback rehearsal, and forward repair | Technical defaults do not justify fabricating information |
| Some labs required repetitive reports or hidden prerequisites | Supply bounded data, a worked start, one meaningful modification, a check, and one existing submission | Time goes toward learning and explanation rather than file production |
| The writing bank silently required eight extra assignments | Integrate its prompts into existing labs, explain unfamiliar terms, model a supported claim, and align grading | Communication develops alongside technical work without an additional assignment stream |
| MongoDB exercises depended on retained cloud data and misleading aggregate totals | Add a fresh-fixture aggregation/validation notebook and an equal-count counterexample after array expansion | The same result-grain idea transfers from SQL joins to document pipelines |
| PostgreSQL import depended on an optional SQLite branch | Build source rows independently and test PostgreSQL-only and MongoDB-only paths, including repeat imports | Alternatives must actually work independently |
| A blocking notebook could leave the learner with an expired wait | Capture the live relationship and release the lock in one controlled execution | Students can inspect a real result without racing a timeout |
| Some reporting documents claimed final readiness from older checks | Separate draft existence, executed tests, export review, external review, and classroom evidence | Reviewers can see what has actually been established |
| Early decks described activities without consistently teaching the exact prerequisite | Rebuild Week 1 around four visible requests; revise Week 2 with concrete SQL, matching-pair diagrams, and a complete zero-inclusive report before the student adaptation | Students encounter the mechanism before being asked to use it |
| The schema deck omitted the lab's subset-count example and used an incomplete constraint test | Teach `FILTER`, namespaces, dependencies, types, and actual catalog queries; show a complete named priority constraint and separate rejected/accepted updates before students adapt it to status | The chapter, demonstration, individual experiment, and short explanation address the same database problem |
| The views deck confused role identity with generated IDs and did not demonstrate the assigned migration; the reading could overwrite the lab view | Teach a complete view and result, allocation versus retention, and a full migration; use distinct reading/demo/lab object names and test their coexistence | Students can follow the reading and live examples without breaking their assignment, then explain a real result in one SQL file |
| The transaction deck depicted commit followed by rollback and did not match the assigned labs; the blocking activity emphasized copied fields | Teach alternative transaction endings, actual paired writes and failure results, then compare two outcomes of the same captured wait using one notebook setting | Students first see the mechanism, then make a meaningful change and explain its effect rather than produce a separate diagnostic report |
| The security deck used an absent view, omitted role membership, and illustrated user identity with a value the caller could set; the RLS lab offered little independent application | Supply complete role/view setup and rollback-protected tests; distinguish database roles from verified application identities; have students write a restricted report and test a newly inserted resident row | The student can observe useful authorized work and a specific ownership boundary before explaining the remaining application-security test |
| Equations and code lost their intended appearance in exported tables | Preserve native math, upright literal names, table code fonts, and adequate widths; correct clipped truth-table values | Mathematical and programming notation remains meaningful in the actual book |
| Raw reference URLs disrupted reading and pagination | Give 80 references descriptive linked titles, retaining every destination | Sources are easier to read and navigate without removing material |
| The NoSQL deck named models without enough worked reasoning and pointed to a different CSV case | Teach actual access patterns, graph traversal, cosine/distance calculations, JSON syntax, and two complete representations of the same ticket facts; use another ticket for the individual lab | Students can transfer a demonstrated design instead of guessing the syntax or comparing examples with missing facts |

The Week 10 revision also repairs a missing runtime-IP step, mismatched notebook
fields, an ambiguous repeat-update exercise, and incorrect vendor activity roles.
The redesigned second-day task adds a latest-two-event read and retained-history
requirement to Week 9's JSON case, rather than repeating the same assignment.
Its writing supports one existing Brightspace response. Public vendor menus show
that the previously assigned relational-to-document sections are videos, not
interactive labs. The replacement uses separate one-to-one and one-to-many
lessons and Practice activities within one course, with exact links.

These are revisions of the existing course and OER drafts. They are not evidence
that every listed resource was first authored during this audit or during the
funded period.

## Executed Technical Checks

Tests in this audit use synthetic course data in isolated local PostgreSQL 15
and MongoDB 8.0.29 environments. They do not use production student data or alter
the instructor's hosted databases.

| Check | Current result | Boundary |
|---|---|---|
| PostgreSQL lab reference cases | 33 checks passed: fixture counts, joins and NULL, safe DML, constraints, views, identity, migration, roles/RLS, and index comparison | Not a check of every textbook SQL listing |
| Textbook PostgreSQL and Python source | 143 recorded source executions, assertions, and explicit exclusions; actual custom/plain dump and restore, live blocking, SQL review, reading/lab coexistence, index-result preservation, source-data inspection, and stale-event handling verified | This count includes exclusions and is not 143 independent passing tests; the Supabase identity adaptation needs a hosted request context |
| Textbook MongoDB source | 80 recorded exact-source executions and assertions; chapter fixtures, CRUD, array semantics, complete referenced-page reads, repeated contact correction, retained history, grouping, BSON-date rejection, and explain results checked | Records are operations plus assertions, not 80 independent features; a local standalone server does not test replica failover, Atlas networking, or Database Tools recovery |
| Textbook MongoDB Database Tools recovery | 11 records covering actual dump/restore commands, archive observations, and checks of separately restored records, BSON dates, validation rules, and indexes | Quiescent synthetic source on a local server; not an Atlas network, failover, or concurrent-backup test |
| Week 6 student-visible authorization test | Actual lab SQL and Python display code executed; allowed results and SQLSTATE 42501 denials verified | Does not verify Supabase browser-session behavior |
| Existing notebook local paths | Executed the local/default paths; executed real PostgreSQL blocking and dump/restore paths | Static incident and mock paths are explicitly identified as such |
| MongoDB live-equivalent notebook paths | CRUD, array matching, BSON-aware logical recovery, index recreation, aggregation, and validation executed against an actual local server | Not proof of Atlas network, account, or free-tier permissions |
| Public-data import | SQLite, PostgreSQL-only, and MongoDB-only paths executed, including repeated imports | Uses the supplied bounded snapshot, not a production ingestion service |
| New aggregation student modification | Category counts, urgent counts, latest dates, array-expanded identities, and accepted/rejected date validation checked | A four-ticket teaching fixture does not measure production performance |
| Week 14 incident model | New, repeated, and stale full-state messages tested; missing version guard reproduces the incorrect final state | A Python model, not a concurrent distributed implementation |
| Week 1 deck | Seven checks of actual slide SQL, 17 matching spoken scripts, and individual slide/PDF visual review | Tiny four-ticket case; SQL is a teaching illustration, not required student coding |
| Week 2 deck | 24 local PostgreSQL checks of actual slide SQL and stated results; 21 matching scripts; individual slide/PDF visual review | Complete 8-user/12-ticket/21-event fixture; not a hosted SQL Editor test |
| Week 3 deck | 38 local PostgreSQL checks of slide SQL, named constraint cases, and student adaptations; 20 matching scripts with 5,090 spoken words; individual slide/PDF visual review | Covers metadata, subset counts, accepted and rejected changes, rollback, and CHECK/NULL behavior; not a current Supabase UI test |
| Week 4 deck | 32 local PostgreSQL checks of actual slide SQL and student adaptations; 21 matching scripts with 5,064 spoken words; all slide/PDF pages visually reviewed | Tests views, column replacement, sequence gaps, migration, valid/invalid updates, old-writer omission, and the local equivalent of the dated screenshot; not a current Supabase UI test |
| Week 5 deck, labs, and transaction notebook | 38 local PostgreSQL checks, including both revised notebook branches; 23 matching scripts with 5,740 spoken words; every slide and PDF page visually reviewed | Tests actual slide/lab SQL, aborted paired changes, zero affected rows, three isolation cases, captured blocker relationships, final rows, and normal cleanup. Hosted Supabase, Colab installation, TLS, and every network-failure path are not established by these local tests |
| Week 5 connection-error handling | Five injected failures verify safe messages, clearing the temporary URL, and closing connections opened before a later connection fails | Mocked client failures using the actual notebook cell, not live network or server failure tests |
| Week 6 deck, labs, and demonstration guide | 39 local PostgreSQL checks; 24 matching scripts with 5,721 spoken words; every slide and PDF page individually reviewed | Covers actual setup/cleanup, restricted reporting, denied writes, rollback under an accidental grant, direct lookup, new-row visibility, default-deny, view-owner versus invoker behavior, ordinary-owner FORCE behavior, and actual display code. Does not establish hosted Supabase user-token, browser, TLS, or Colab installation behavior |
| Book layout regressions | Seven checks cover math-aware table widths, preserved table code fonts, truth-table values, upright equation labels, list lead-ins, and long-number heading separation | These checks cover particular previously observed defects, not every layout |
| Week 7 deck, labs, and demonstration guide | 35 local PostgreSQL checks; 24 matching scripts with 5,884 spoken words; all slide/PDF pages individually reviewed; displayed measurements match the preserved execution capture | Covers fixture/reset, actual slide SQL, partial-index eligibility, exact ordered results, repeated runs, storage, a smaller-limit comparison, the student composite-index experiment, and cleanup. Local timing does not establish hosted performance, concurrent write cost, or a service guarantee |
| Week 8 deck, lab, and demonstration guide | 17 actual-code/content checks; 24 matching scripts with 5,817 spoken words; all slide/PDF pages individually reviewed | Covers displayed dump/restore commands, expected values, named constraint failure, rolled-back migration, a changed-subject counterexample, and the committed-delete incident in disposable local databases. Does not establish hosted recovery, physical backup, or production cutover |
| Week 8 recovery notebook | 19 checks on isolated macOS PostgreSQL 15; 20 checks on Ubuntu 24.04/PostgreSQL 16 using the actual root/sudo setup branch; two complete runs per environment | The Linux test reproduces the old private-directory permission failure and verifies the fix. Checks cover exact baseline, both student ticket choices, damaged values, missing constraints, unrelated SQL errors, and cleanup. These overlapping suites are not additive counts of independent features. Neither environment is hosted Google Colab |
| Week 9 deck, JSON lab, and Chapter 9 examples | 34 local checks; 32 scripts with 6,585 spoken words; all slide/PDF pages individually reviewed | Covers extracted JSON, invalid syntax, Python parser caveats, actual CSV facts, equivalent document representations, graph traversal, cosine/distance calculations, and recall. No cloud deployment, desktop PowerPoint execution, or classroom learning outcome is implied |

Week 10 adds 69 checks of the actual exported slide code and complete instructor
demonstrations, plus a 96-check notebook suite covering repeated setup/writes,
array counterexamples, typed dates, cleanup, and injected connection failures.
The notebook runs twice in its mock path and twice against isolated MongoDB
8.0.29. These overlapping checks are not independent measures of learning or
feature counts. Its 28 slides, 28 PDF pages, and 6,332 spoken words now align with
the individual labs. All rendered slides and PDF pages were individually
reviewed, with byte-identical prior-page review carried forward after the last
two code-layout repairs. No hosted Atlas/Colab run or account-gated University
Practice completion is implied.

Week 11's revised notebook has 91 checks across two runs each in local mock mode
and real local MongoDB 8.0.29, plus injected connection failures. The actual
student changes produce the expected urgency/date summary and reject invalid
status, text dates, and missing dates on the server. Repeated tests preserve the
four-ticket fixture; cleanup preserves another collection in the same database.
Mock-mode output remains explicitly a supplied trace, not server validation.
Four exact instructor-guide sort-demo blocks and ten assertions verify a
10,000-document workload, the same ordered twenty results, before/after work
counts, index/scan/sort stages, and cleanup. These checks do not establish hosted
Atlas permissions, Colab installation, runtime speedup, or University completion.

The revised Week 11 deck adds 28 slides with 6,142 spoken words in matching
PowerPoint notes and transcript. Its SQL bridge, exact document results,
event-expansion counterexample, date-rule tests, and measured index comparison
align with the notebook and two individual labs. A 79-check suite combines
exported-code execution, displayed-result checks, note coverage, and exact
activity links. It is not 79 independent experiments. The actual Python and
mongosh examples run on isolated MongoDB 8.0.29; the SQL bridge runs on SQLite.
All 28 slide images and PDF pages were individually reviewed, with identical
images carried forward after the final syllabus-handoff correction. Thirteen
native editable tables preserve the result displays. The final file hashes bind
the examples, notes, renders, notebook, and instructor guide to these checks.
This is a completed revision of these materials, not approval of the whole
course or a claim of hosted execution, University completion, accessibility
certification, or measured student learning.

Week 12's recovery notebook now has a 176-check suite covering actual cells,
both student ticket choices, repeated setup/export/restore/repair, and missing-
rule and damaged-file cases. Each path runs twice using `mongomock` and isolated
MongoDB 8.0.29. The checks establish that a wrong subject can survive count,
ID, and date-type checks, while comparison against the saved typed values detects
it. A same-valued integer/double substitution also fails the Canonical Extended
JSON comparison. Students repair from the verified file parse and test separately
reconstructed indexes and, on the server, schema rules. Invalid artifact bytes
or JSON stop before resetting the target. Missing rules and unrelated permission
errors cannot masquerade as successful validation. Cleanup preserves unrelated
collections. Connection-error and IP-failure cases are injected rather than
tested against a hosted account.

These are overlapping correctness checks, not 176 independent learning outcomes.
The weekly lab and implementation guide now match the notebook's one repair and
one in-notebook recommendation. The seventeen original Week 12 slides were
individually inspected and their obsolete assignment instructions identified;
the revised deck and its scripts are still pending. Chapter 12 and the textbook
exports are unchanged by this notebook pass. No hosted Atlas/Colab execution,
replica failover, or institutional accessibility approval is implied.

Detailed machine results are retained privately in the instructor's audit
workspace. No credentials, private answer keys, or production identifiers belong
in a public evidence packet. Before a release, attach a sanitized dated summary
with the tested source version and the exact artifact manifest.

## Work Still Under Review

All fifteen chapter sources have received substantive revisions, and all fifteen
weekly guides now identify reading for both meetings. The Word, PDF, HTML, and
EPUB have been rebuilt. The current PDF has 161 pages, and the HTML/EPUB preserve
152 MathML elements and 141 numbered listings. Rendering exposed and prompted
fixes for cover overflow, font substitutions, small tables, and duplicated
heading numbering, truth-table clipping, and reference pagination. EPUBCheck 5.3.0
reports zero fatals, errors, warnings, or informational messages for the current
EPUB. Mechanical checks of all PDF pages report no out-of-page characters or
replacement glyphs. The Word renderer's PDF and supplied PDF are pixel-identical
across all 161 pages at 120 DPI in the current rebuild. Earlier 96-DPI receipts
apply to their recorded versions.

The current standalone HTML was tested in headless Chromium at desktop and phone
widths (1440 and 375 pixels). Images load, internal anchors resolve, the keyboard
skip link works, and the tested mobile code listing can be focused and scrolled
with the keyboard. Eight screenshots of its opening, notation, truth-table, and
new referenced-page sections were individually inspected. Descriptive link text
replaced the three remaining raw-URL labels. The current automated Word
accessibility audit reports zero high, medium, or low-priority findings. None of these
checks is a screen-reader or institutional accessibility certification.

The current exact-image record covers 59 of 161 pages, including all of Chapter
10 (pages 96-108), the revised source references, and unchanged earlier pages.
The count is not a withdrawal of earlier content review: fixing the global
long-number heading separator changed 50 previously reviewed earlier page images,
which need renewed visual inspection. Together with later unreviewed pages, 102
current pages remain outside the exact-image review record. The previous 95-page
record applies only to its older export. Two interface figures with excess empty
space, a one-row table continuation, literal timeline labels that should
match mathematical subscripts, and a sparse chapter-end reference page are recorded for further
pagination refinement. Week 1's 17 slides, Week 2's
21 slides, Week 3's 20 slides, Week 4's 21 slides, Week 5's 23 slides, Week 6's
24 slides, Week 7's 24 slides, Week 8's 24 slides, Week 9's 32 slides, Week 10's
28 slides, and Week 11's 28 slides have been revised, tested, and individually
inspected with their PDF exports. This covers 262 of the current 321 slides.
The remaining 59 slides in Weeks 12-15 still
require the current audit.
The Week 4 screenshot's image-level alt text did not survive PPTX export, despite
using the authoring tool's documented setter. Week 8's two exported images also
lack image-level descriptions; the new screenshot used that setter. Visible
captions and notes explain these figures, but the accessibility defects still
require remediation. Week 9's two image descriptions also did not survive the
authoring export; the diagrams have visible explanations and spoken notes, but
the PPTX image-level description defect remains recorded. Week 10's retained
Atlas image also lacks image-level description metadata after export. Its
caption and notes do not replace that remaining accessibility repair.

The Week 9 book rebuild used the same explicit font configuration for export
and independent Word rendering. A previous mismatch changed list wrapping;
48 earlier pages were individually rechecked, and only 34 unchanged prior page
reviews carried forward. Thirteen more pages complete Chapter 9's review.
Its corrected vector geometry, sequential figure captions, exact-search
qualification, and complete JSON examples are present in all four book formats.
The full-course validator reports 481 passing checks. Its purpose is consistency
and structural checking, not certification of instructional quality.

Both temporary local database servers were shut down after execution testing.
No hosted Atlas or Supabase project changed during this audit.

The substantive audit is not complete. Remaining work includes:

- completing the export-level review and verifying remaining environment-specific
  examples without extending local results to hosted platforms;
- inspecting the remaining Weeks 11-15 slides and their word-for-word spoken
  scripts against the revised teaching sequence;
- checking the rebuilt Word, PDF, HTML, and EPUB for actual
  layout, mathematical notation, code, tables, image captions, and navigation;
- repeating inventory, link, and public-package checks after further revisions;
- external subject, OER attribution, and accessibility review;
- testing the current hosted-platform and account-gated student routes where
  access permits, with explicit fallback limits; and
- classroom implementation, feedback-informed revision, and approved publication.

Old export page counts, slide totals, and EPUBCheck receipts are not current
revision results until the new files are rebuilt and checked.

## Educational Quality Criteria

The course's standards are observable rather than promotional.

**Depth with accessible entry:** introduce a new term in context, explain the
mechanism, show a small worked example, and only then ask for an independent
change. Keep advanced extensions distinct from required beginner work.

**Coherence:** the textbook explains the lab's concept; the deck teaches it;
the lab uses a documented fixture; the writing interprets that same result.
The syllabus's established sequence and grading weights remain intact.

**Authentic reasoning:** an activity changes a query, data shape, access rule,
transaction, or operating decision. Students encounter a meaningful consequence
rather than collecting screenshots or repeating a vendor badge requirement.

**Reusable authorship:** another instructor can obtain editable sources, locate
setup and cleanup, identify expected behavior, and adapt an activity without
reverse-engineering a collection of slides.

**Honest access and evaluation:** no required paid feature, no hidden group work,
no production credentials in notebooks, no claimed learning gain without actual
classroom evidence, and no claim that a mock enforces a real server's guarantees.

These standards address the published City Tech criteria for content, coverage,
organization, attribution, accessibility, navigation, modularity, and relevance.
Their presence in a plan does not establish that the final artifacts pass them.
[City Tech OER evaluation criteria](https://openlab.citytech.cuny.edu/oerfellowship/files/2017/05/OER-Evaluation-Criteria-5.26.17.pdf)

## Funding and Reporting Boundary

The current official fellowship call provides a scope-dependent project stipend
range of $1,300-$6,000 and separate professional-development compensation.
It also requires licensing, accessibility, completion, and public sharing.
The program determines the award and how preparatory or previously funded work
is treated. [City Tech 2026-27 call](https://openlab.citytech.cuny.edu/library/call-for-applicants-to-the-oer-fellowship-ay-26-27/)

Request evaluation of the actual primary textbook and supporting package. Keep
dated work records, reviewed versions, technical results, revision decisions,
and adoption feedback. Do not infer hours from word counts or describe unchanged
prior teaching material, vendor resources, duplicate formats, or administrative
reporting as newly authored student resources.

Publication remains approval-only. No part of this audit is a deposit, public
release, external endorsement, guarantee of maximum funding, or claim that the
course has already improved student outcomes.

Local commit `3046f03` records the revised minimal Week 1 public-package files;
it has not been pushed. It contains no full-course textbook or fellowship files.
The six-file share copy matches that local package. The remaining OER revisions
are local, outside the public package, and not part of that commit.
