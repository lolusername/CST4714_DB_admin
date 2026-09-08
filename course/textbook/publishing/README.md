# Second-Edition Publication Workspace

This folder turns the complete second-edition source into four synchronized
formats without making any generated file the only editable copy.

## One Command

From `course` run:

```bash
uv run tools/build_textbook.py
```

The command rebuilds editable Word, PDF, standalone HTML, EPUB, the cover, and a
SHA-256 manifest in `exports/`. It also creates the Word reference template used
to keep typography and page layout consistent.

## Where to Change Things

| Change | Canonical source |
|---|---|
| chapter explanation, equation, or code | `../module_*.md` |
| diagram content | `../figures/*.dot` or `*.svg` |
| cloud screenshot | `../figures/cloud_interfaces/` |
| title, edition, description | `book_metadata.yaml` |
| opening explanation | `front_matter.md` |
| part transitions | `parts/` |
| notation, glossary, technical templates | `appendix_*.md` |
| license and source statement | `back_matter.md` |
| web/EPUB appearance | `operating_cloud_databases_2e.css` |
| Word/PDF appearance | token map in `STYLE_GUIDE.md` and build code |

The generated Word document is the primary human review copy. Use Word comments
for review, then transfer accepted changes to the canonical source before the
next build. This avoids silent divergence between Word, PDF, web, and EPUB.

## Current Draft and Checks

The September 8, 2026 revision contains all 15 chapters, five part introductions,
two appendices, and back matter. Its current PDF has 158 US Letter pages. The
HTML and EPUB contain 152 MathML elements, 132 numbered code listings, and 15
instructional images. These are formats of one textbook, not separate authored
books.

The current EPUB passes EPUBCheck 5.3.0 with zero fatals, errors, warnings, or
informational messages. The repository validator checks the source manifest,
export checksums, current source-derived math/listing/image counts, and companion
links. Word, PDF, and HTML links resolve relative to the complete course folder;
the EPUB explains how to locate the companion files in that folder. The minimal
public Week 1 repository is not advertised as the full textbook download.

Rendered-page inspection exposed and corrected a cover caption overflow, font
theme overrides, undersized tables, duplicated heading numbering, and clipped
truth-table values. SQL values retain code styling in tables; literal names
remain upright labels inside equations. Eighty raw reference links now use
descriptive titles, preserving every source destination and eliminating a page
that previously contained only one reference. Mechanical
PDF checks report no characters outside the page and no replacement glyphs.
The current standalone HTML was checked at 1440- and 375-pixel widths in Chromium.
The checks found and corrected a long plan-node label that widened the phone
layout. Images loaded, internal anchors resolved, and the keyboard skip link
worked. The long mobile code listing also accepted keyboard focus and scrolled
with the arrow key. Six desktop/mobile screenshots were inspected. The automated
Word audit reports no high- or medium-priority findings and three low-priority
link-label findings; this is not accessibility certification.

Current visual observations cover pages 1-95, either inspected directly
or matched byte-for-byte to previously inspected page images. The other 63 pages
still require individual review. The Word renderer's PDF and the supplied PDF are
pixel-identical across all 158 pages at 120 DPI in the current rebuild. Earlier
96-DPI receipts apply to their recorded versions. That establishes matching exports, not visual
approval of pages not yet inspected. Complete accessibility review remains in
progress. Earlier receipts apply only to their recorded artifact hashes, even
when an earlier draft happened to have the same page count.

Chapter 9 now includes complete referenced and embedded JSON representations of
the same selected CSV facts. The vector diagram shows the angle between the
actual vectors, figure captions follow reading order, and exact search is no
longer incorrectly equated with a mandatory full scan. Local checks verify the
JSON examples, selected source rows, and displayed graph/vector calculations.

Use the same installed fonts, font configuration, and LibreOffice runtime for
building and reviewing the Word/PDF pair. The September 8 check found that a
different font configuration changed list wrapping even with the same page
count. After matching the configuration, all pages matched; 48 earlier pages
were individually rechecked, rather than inheriting obsolete review approvals.

The [current quality record](../../../oer_fellowship/evidence/FELLOWSHIP_SCOPE_EVIDENCE.md)
also distinguishes actual local database execution from cloud-platform checks.
After a source or style change, rebuild and repeat the relevant structural and
visual checks. From `course`, run `uv run tools/validate_oer.py`. A release also
needs fresh link, EPUBCheck, and institutionally required accessibility review.

## Publication Boundary

This directory contains authored publication files and generated formats. It
does not absorb MongoDB University, MongoDB educator decks, Supabase, Atlas, or
other free vendor material into the OER claim. Those resources remain cataloged
separately in `../../external_resources/`.
