# External Review and Release Gates

## Release Boundary

*Operating Cloud Databases* is a complete authored release candidate. It is not
an approved or published fellowship release.

- **Candidate version:** `1.0.0-rc.1`
- **Status reviewed:** August 9, 2026
- **Current authorization:** local QA and review preparation only

No formal tag, remote push, Pressbooks import, OpenLab publication, Academic
Works deposit, public announcement, or fellowship approval is authorized by this
record. Publication begins only after the instructor explicitly approves it.

## Gate Status

| Gate | Evidence currently available | State | What closes the gate |
|---|---|---|---|
| Authored scope | Cataloged 15-week course, open text, labs, notebooks, datasets, projects, assessments, decks, scripts, guides, and publication exports | COMPLETE | maintain inventory through release |
| Technical local QA | 259-check local pass; 261-check network pass over 135 URLs; notebook execution; PostgreSQL fixtures; all-slide/all-PDF visual review; HTML reflow/landmarks; EPUB/DOCX/checksum checks | COMPLETE | repeat from the approved release commit before tagging |
| Attribution review | Source and license register plus automated completeness checks | SELF-AUDITED | named OER reviewer signs the attribution sample |
| Accessibility review | Semantic source formats, transcripts, alternatives, visual QA, automated checks | PARTIAL | keyboard and screen-reader review in intended webbook/LMS; record defects and fixes |
| Cloud/vendor smoke test | account-free and offline checks | PARTIAL | complete the live rows in the cloud/vendor record |
| Pressbooks import/export | DOCX import package and metadata prepared | NOT RUN | import privately; inspect webbook, navigation, media, math/code, links, Digital PDF, EPUB, and Common Cartridge |
| Classroom pilot | instruments, decision rules, and de-identified packet prepared | NOT STARTED | teach the candidate, analyze actual aggregate evidence, revise, and document limits |
| Fellowship/OER-team approval | review packet prepared | PENDING | authorized reviewers record approval and required changes are closed |
| Formal release | metadata and checklist prepared | WITHHELD | explicit instructor approval, clean commit, release tag, archive checks, and approved publication destination |
| Deposit/publication | deposit metadata prepared | WITHHELD | explicit approval plus destination-specific review and final public URL/identifier |

## Attribution and License Review Sample

The reviewer should sample every source category, not merely count links.

| Sample category | Reviewer check | Result |
|---|---|---|
| Original prose/slides | default license and creator statement are visible | PENDING EXTERNAL REVIEW |
| Original code | MIT terms and source notices are present | PENDING EXTERNAL REVIEW |
| Synthetic data | CC0 designation and generation description are present | PENDING EXTERNAL REVIEW |
| Government/public data | source, retrieval date, transformation, omitted fields, and terms are recorded | PENDING EXTERNAL REVIEW |
| Adapted material | title, creator, source, license, material used, and changes are recorded | PENDING EXTERNAL REVIEW |
| Free but non-OER resources | linked rather than copied and excluded from created-OER counts | PENDING EXTERNAL REVIEW |
| Private/account-gated research | no protected expression, quiz, answer key, or screenshot was reproduced | PENDING EXTERNAL REVIEW |

Reviewer name, role, date, sampled records, defects, and disposition must be
recorded before this gate is represented as complete.

## Accessibility Review Protocol

### Source and export checks

1. Confirm one logical page title and heading hierarchy in each format.
2. Confirm descriptive links and identify repeated ambiguous link labels.
3. Inspect tables for header identification and understandable linear reading.
4. Confirm that essential diagrams have nearby visible explanation or a structured
   text equivalent.
5. Confirm that instructions do not depend on color, location, pointer input, or
   screenshots alone.
6. Confirm that code and notebook sequences explain purpose before execution and
   provide text guidance for expected failures.
7. Verify reflow/zoom behavior and that the skip link reaches the main content.
8. Use a keyboard to traverse navigation, links, code controls, and any embedded
   media without a trap or lost focus.
9. Use at least one representative screen reader to check title, landmarks,
   headings, lists, tables, links, code context, and reading order.
10. Repeat representative checks in the actual Pressbooks webbook and LMS; a
    standalone HTML result does not prove platform accessibility.

### Accessibility evidence record

| Environment and assistive technology | Pages sampled | Findings | Fix commit | Retest | Reviewer/date |
|---|---|---|---|---|---|
| Standalone HTML, semantic/reflow precheck | single-page book: cover, TOC, code, and tables | one navigation landmark, one focusable main landmark, valid skip target, embedded CSS, and no desktop/mobile page overflow; human keyboard sequence still required | | | local automated/direct inspection, August 9, 2026 |
| Standalone HTML, keyboard | NOT RUN | reliable human key sequence still required | | | |
| Standalone HTML, screen reader | NOT RUN | human/AT review required | | | |
| EPUB reader | NOT RUN | representative reading-system review required | | | |
| Pressbooks webbook | NOT RUN | import required | | | |
| Brightspace/LMS | NOT RUN | course-shell review required | | | |

PDFs are handouts with extractable text. They must not be described as tagged
accessible PDFs until tags, reading order, language, headings, lists, tables,
links, and alternative text receive an appropriate PDF audit.

## Private Pressbooks Import Review

The prepared Word file is an import candidate, not evidence that Pressbooks
rendered it correctly.

1. Create a private draft book only after approval to use the destination.
2. Import the release-candidate DOCX and retain the import report.
3. Compare chapter count, title order, heading levels, code blocks, tables,
   internal links, external links, lists, callouts, and image alternatives with
   the canonical Markdown/HTML source.
4. Inspect keyboard navigation, skip behavior, landmarks, page titles, and
   representative screen-reader output.
5. Generate Pressbooks EPUB and Digital PDF; validate structure and visually
   compare representative chapters.
6. If Common Cartridge is required, import it into a nonstudent LMS shell and
   inspect links, organization, visibility, and accessibility.
7. Record every Pressbooks-only correction in the canonical source or build
   process whenever possible; avoid an unexplained platform fork.
8. Keep the draft private until OER-team and instructor approval are recorded.

## Approval Record

| Role | Name | Scope reviewed | Decision | Required changes | Date |
|---|---|---|---|---|---|
| Instructor/author | | final release authorization | PENDING | | |
| OER/fellowship reviewer | | scope, attribution, accessibility, reuse | PENDING | | |
| Technical reviewer | | database accuracy and executable paths | PENDING | | |
| Accessibility reviewer | | intended publication and LMS formats | PENDING | | |

Blank rows mean no approval has been granted.

## Formal Release Sequence

After all required gates close and explicit instructor approval is recorded:

1. Rebuild HTML, EPUB, DOCX, cover, and checksums from the approved commit.
2. Run the structural validator, live-link validator, notebook suite, SQL fixtures,
   slide/PDF checks, credential scan, and archive checks one final time.
3. Record the exact commit and results in `RELEASE_CHECKLIST.md` and
   `RELEASE_NOTES.md`.
4. Create the approved semantic tag; do not retag a different commit.
5. Export a release archive and verify its checksum before upload.
6. Deposit or publish only to the explicitly approved destination.
7. Record the public URL, DOI/handle or other identifier, license display,
   publication date, and deposit checksum.
8. Preserve a known-limitations statement and open the pilot/revision cycle.

## Current Decision

Continue local QA and prepare review evidence. Do not tag, push, deposit, import,
publish, or claim external validation from this document alone.
