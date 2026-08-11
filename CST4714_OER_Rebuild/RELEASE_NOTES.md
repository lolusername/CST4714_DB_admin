# Release Notes

## Version 1.0.0 Release Candidate 1

This release candidate presents the complete planned file inventory for
*Operating Cloud Databases*. It is suitable for OER-team review, Pressbooks
import, technical smoke testing, and accessibility review. It is not represented
as classroom-piloted or externally reviewed.

## Highlights

- 15 open-text modules with a major relational-model, relational-algebra, and
  SQL re-entry sequence.
- 15 weekly student guides and 25 individual in-class labs with one manageable
  submission each.
- Six executable educational notebooks with credential-safe cloud routes and
  open offline fallbacks.
- Three reusable data packages, canonical midterm and final projects, and a
  complete formative/summative assessment set.
- Fifteen student-facing PowerPoint decks containing 214 slides, complete spoken
  scripts in notes, matching transcripts, and PDF handouts.
- Public implementation, troubleshooting, accessibility, data-informed teaching,
  and release guidance without private answer keys.
- Portable HTML, EPUB, and Word book formats plus a reproducible build script and
  checksum manifest.

## Candidate Validation

- Structural validation passed 306 checks. Network-enabled validation passed 308
  checks across 143 unique URLs with no confirmed 404 or 410 result; five
  automated-client refusals remain manual-review items.
- All 68 notebook code cells re-executed through offline paths with zero errors
  after the connection-safety update; generated and checked notebook sources
  match exactly.
- PostgreSQL setup scripts executed in a disposable database with verified row
  counts and 100,000 performance rows.
- All 214 slides passed boundary checks; every final slide and all 15 exported
  PDF handouts received visual review.
- Every speaker-note script matches its transcript wording and slide order.
- The self-contained HTML passed landmark, skip-target, desktop, and mobile
  reflow checks. A representative Safari keyboard sequence successfully focused
  and activated the skip link and transferred accessibility focus into the main
  content. EPUB and DOCX archive/XML checks and SHA-256 verification passed. The
  current 90-page Word export received complete visual review, including the
  updated Module 13 connection examples.
- No credentials, student data, private grading keys, teacher-only cheat sheets,
  or temporary slide-generation files are part of the public package.

## Known Limitations

- Pressbooks import and Pressbooks-generated export review are pending. The local
  HTML, EPUB, and DOCX release-candidate exports have completed local technical
  and visual QA.
- All PDF handouts report tagged structure, are unencrypted, and contain
  extractable text, but tag-tree quality and assistive-technology reading order
  have not received human review.
- Live Atlas and Supabase notebook paths require a pre-course smoke test with
  temporary accounts.
- Account-gated vendor activities require final student-role verification.
- Comprehensive keyboard and human screen-reader checks must be completed in the
  final webbook and LMS environment.
- Five sources that reject automated link clients require manual browser review.
- Classroom implementation, aggregate learning evidence, and evidence-based
  revision have not yet occurred for this rebuilt edition.
- OER-team approval, a formal tag, remote push, deposit, and publication are
  intentionally withheld pending instructor approval.

## License

Original instructional prose and media are CC BY-NC-SA 4.0. Original code is
MIT. Original synthetic data is CC0. Source-specific notices govern adapted or
public data.
