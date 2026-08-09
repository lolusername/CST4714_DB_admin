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

Candidate exports retain the `1.0.0-rc.1` version string until Pressbooks,
accessibility, and OER-team review are complete. Final release exports use
`1.0.0`.

Pressbooks remains the preferred public reading platform because it can publish
an accessible webbook and generate Digital PDF, EPUB, and Common Cartridge
exports. The repository remains the editable, version-controlled source.
