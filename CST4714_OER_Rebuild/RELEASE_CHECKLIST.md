# OER Production, Validation, and Release Guide

## Purpose and Boundary

Use this guide before publishing or adapting *Operating Cloud Databases*. It
checks the public course package, not private grading records or fellowship
administration.

- The [Catalog of Created OER](OER_CATALOG.md) is the authoritative inventory of
  authored and adapted course resources.
- The [`fellowship/` directory](fellowship/README.md) contains planning,
  evaluation, and reporting documents. Those documents are not counted as
  student course content.
- The [Free External Resource Catalog](FREE_EXTERNAL_RESOURCES.md) records
  no-cost platforms and vendor materials. Free access does not make those items
  OER, and they are not counted as fellowship-created resources.

## 1. Inventory and Scope

- [x] The OER catalog links every completed resource and describes its original
  educational contribution.
- [x] Counts match the actual files: 15 modules, 15 weekly guides, 25 individual
  labs, 6 notebooks, 3 data packages, 15 decks, 15 transcripts, and 15 PDF
  handouts.
- [x] `midterm_project.md` and `final_project.md` remain the only canonical major
  assignment descriptions.
- [x] Weekly guides link to checkpoints rather than copying or changing project
  requirements.
- [x] No private answer key, named-student record, grading annotation, credential,
  teacher cheat sheet, or slide-generation source is in the public package.

## 2. Learning Design

- [x] Weeks 1-3 provide a substantial relational-model, relational-algebra, and
  SQL re-entry sequence before administration work assumes SQL fluency.
- [x] Every lab states that graded work is individual and asks for one manageable
  submission.
- [x] Activities move from prediction or worked example to practice, evidence,
  interpretation, and transfer.
- [x] Cloud-dependent work has a local, static, or simulated path that targets
  the same learning outcome.
- [x] Career writing asks students to make a claim with technical evidence and a
  bounded tradeoff rather than summarize a product or video.
- [x] MongoDB University live demonstrations are distinct from assigned student
  activities.

## 3. Slides, Scripts, and Study Formats

- [x] Every visible slide is student-facing and contains no instructions to the
  presenter.
- [x] Every slide has complete word-for-word spoken prose in PowerPoint speaker
  notes.
- [x] Every transcript matches the notes exactly in wording and slide order.
- [x] Every deck passes the slide-boundary test and a full-size visual review.
- [x] Every PDF page count matches its deck, contains extractable text, and passes
  a separate visual review after export.
- [x] PDFs are labeled as handouts, not as tagged accessible PDFs unless a tag and
  reading-order audit has actually been completed.

## 4. Technical Validation

Run the package validator from the repository root:

```bash
python CST4714_OER_Rebuild/tools/validate_oer.py
```

Before a public release, also run the live-link mode from a network that permits
vendor sites:

```bash
python CST4714_OER_Rebuild/tools/validate_oer.py --check-urls
```

- [x] Markdown relative links resolve.
- [x] JSON parses, CSV headers and row shapes are valid, and documented data counts
  match.
- [x] All notebooks parse and contain no saved error output.
- [x] Offline notebook paths execute in a clean environment.
- [x] Cloud examples request credentials at runtime and do not weaken TLS or
  certificate validation.
- [x] SQL setup files execute in a disposable PostgreSQL database when PostgreSQL
  is available.
- [ ] External URLs receive automated and manual review; account-gated or
  bot-protected pages are opened in a browser.
- [x] Platform cost, account, and free-tier claims are checked against current
  official pages.

## 5. Accessibility Review

- [x] Markdown uses one logical heading hierarchy, descriptive links, tables with
  headers, and language that does not depend on color alone.
- [x] Essential diagrams are explained in nearby visible text, the transcript, or
  the module.
- [x] Slides use readable type, high contrast, consistent navigation, and no
  overflowing text.
- [x] Transcripts provide the complete spoken content in structured text.
- [x] Notebooks use Markdown explanations before code, concise code cells,
  explicit expected output, and text error guidance.
- [x] Equivalent evidence is available when a screenshot, account, cloud service,
  or live demonstration creates an access barrier.
- [ ] A keyboard and screen-reader check is completed in the intended publication
  platform before the course opens.

## 6. Licensing, Attribution, and Privacy

- [x] Original prose and slides carry the package CC BY-NC-SA 4.0 notice; original
  code carries MIT; original synthetic data carries CC0.
- [x] Adapted resources record title, creator, source URL, source license, material
  used, and changes.
- [x] Public or government data packages record source, retrieval date,
  transformation, omitted fields, and applicable source terms.
- [x] Free external resources are linked rather than copied unless a compatible
  license explicitly permits adaptation.
- [x] Outputs are scanned for connection strings, tokens, private hosts, personal
  data, and account identifiers.

## 7. Release Record

Complete this table for each tagged release. Keep the detailed artifact evidence
in the OER catalog and the fellowship process narrative in the fellowship folder.

| Field | Release value |
|---|---|
| Version or tag | |
| Publication date | |
| Commit | |
| Validator result | |
| Live-link review date | |
| Deck/PDF visual reviewer | |
| Accessibility reviewer | |
| Platform/free-tier reviewer | |
| Known limitations | |
| Changes supported by learning evidence | |

## Current Candidate Snapshot

As of August 9, 2026, the package contains the complete planned file inventory,
including 214 authored slides with matching notes and transcripts. This snapshot
becomes a release record only after all checks above are completed and a version
or tag is assigned.

### Completed Candidate Checks

- The structural validator passed 306 checks. Network-enabled validation passed
  308 checks across 143 unique external URLs, with no confirmed 404 or 410
  result. Five sources rejected or refused the automated client and remain
  explicitly queued for manual review.
- All 214 slides passed the PowerPoint boundary test. Every final slide and every
  final PDF contact sheet received visual review after export; all 15 PDFs match
  their deck page counts, report tagged structure, are unencrypted, contain
  extractable text, and show no clipping, overlap, or broken-render artifacts.
- Every speaker-note script matches its transcript wording and slide order.
- The canonical 15-module Markdown text builds reproducibly as self-contained
  HTML, EPUB, and a Word file prepared for Pressbooks import. The HTML contains
  one navigation landmark, one focusable main landmark, an effective skip link,
  embedded styling, and no page-level horizontal overflow at tested desktop and
  mobile widths.
- SHA-256 verification passed for all three publication artifacts. EPUB and DOCX
  archive and XML checks passed; EPUB metadata and navigation are present. The
  current 90-page Word export received a complete page-by-page visual review,
  including the updated Module 13 connection examples.
- All 68 code cells across the six notebooks executed through the offline paths
  in a clean temporary run with zero error outputs.
- The Metro Support and Week 7 performance SQL setup files executed in a
  disposable PostgreSQL database. Verified counts were 8 users, 12 tickets, 21
  ticket events, and 100,000 performance rows.
- A targeted credential scan found no embedded database URI with credentials,
  token, API key, account identifier, private host, or named-student record.

### Known Candidate Limitations

- PDFs report tagged structure and contain extractable text, but tag-tree quality
  and assistive-technology reading order have not received human review.
  Structured Markdown and transcripts remain the text alternatives.
- Standalone HTML structure, focus targets, desktop layout, and mobile reflow were
  inspected programmatically and visually. A representative Safari keyboard
  sequence successfully focused and activated the skip link and transferred
  accessibility focus into the main content. Comprehensive keyboard traversal
  and a representative screen-reader review remain pending; both must be
  completed in the final publication and LMS environments.
- Offline notebook paths were executed. Live Atlas and Supabase paths still
  require a pre-course smoke test with temporary course accounts and no saved
  credentials.
- Account-gated vendor activities were checked for current title, URL, role, and
  free enrollment, but not completed under a student account during this audit.
- Keyboard and screen-reader checks must be repeated in the final LMS or web
  publication environment.
- The Pressbooks import, public webbook URL, and Pressbooks-generated Digital PDF
  and Common Cartridge have not yet received final review.
- OER-team attribution/accessibility review, classroom pilot evidence,
  evidence-based revision, formal approval, tagging, deposit, and publication
  remain open. No push, tag, import, deposit, or publication is authorized by
  this snapshot.
