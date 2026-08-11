# Publication Package

This directory turns the canonical Markdown textbook into portable publication
formats without replacing the editable source.

## Build

From `CST4714_OER_Rebuild`:

```bash
python3 tools/build_publication.py
```

The build requires Pandoc and ImageMagick. It creates:

- a standalone, self-contained semantic HTML book with embedded styling;
- an EPUB with the course cover;
- a Word document prepared for Pressbooks import; and
- a SHA-256 checksum manifest.

Generated files are written to [`exports/`](exports/). The HTML and EPUB are
student reading formats. The Word file is the most predictable CUNY Pressbooks
import format because every module title uses Heading 1. After import, move
"About This Book" to front matter and "License, Attribution, and Reuse" to back
matter in the Pressbooks organize screen.

Presentation handouts are rebuilt separately from the canonical decks:

```bash
python3 tools/update_deck_metadata.py
python3 tools/export_handout_pdfs.py
```

The first command sets accurate title, author, language, and candidate-status
metadata. The second uses LibreOffice to export tagged, unencrypted PDF
handouts. A tagged flag alone is not an accessibility claim; see the
[publication-format QA record](../fellowship/PUBLICATION_FORMAT_QA.md).
When comparing a regenerated set with a previous release tree, use:

```bash
python3 tools/compare_pdf_renders.py /path/to/reference/CST4714_OER_Rebuild
```

Candidate exports retain the `1.0.0-rc.1` version string until Pressbooks,
accessibility, and OER-team review are complete. Final release exports use
`1.0.0`.

Pressbooks remains the preferred public reading platform because it can publish
an accessible webbook and generate Digital PDF, EPUB, and Common Cartridge
exports. The repository remains the editable, version-controlled source.
