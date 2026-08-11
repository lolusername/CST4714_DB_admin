# Publication Format QA

> **Evidence boundary:** This record covers objective local checks of the
> release-candidate EPUB and PDF handouts. It is not an accessibility
> certification, a PDF/UA claim, a human assistive-technology review, or an
> authorization to publish.

## Candidate and Tools

- **Candidate:** *Operating Cloud Databases*, version `1.0.0-rc.1`
- **Review date:** August 10, 2026
- **EPUB validator:** W3C EPUBCheck 5.3.0, the official EPUB conformance checker
- **Java runtime:** Eclipse Temurin 21.0.12+8
- **PDF export:** LibreOffice 25.8.1.1
- **PDF inspection:** Poppler `pdfinfo` 26.02.0 and MuPDF `mutool` 1.26.2
- **Screen-reader test: NOT RUN**

No screen-reader task is assigned to the instructor. If a fellowship or
institution requires human assistive-technology review, a qualified external
accessibility reviewer must perform and record that review in the final
Pressbooks and LMS environments.

## EPUB Conformance

The official [W3C EPUBCheck 5.3.0 release](https://github.com/w3c/epubcheck/releases/tag/v5.3.0)
was downloaded from the W3C project release and run against:

`publication/exports/operating_cloud_databases_v1.0.0-rc.1.epub`

The validator selected EPUB 3.3 rules and completed successfully.

**EPUBCheck 5.3.0 result: PASS**

```text
Validating using EPUB version 3.3 rules.
No errors or warnings detected.
Messages: 0 fatals / 0 errors / 0 warnings / 0 infos
EPUBCheck completed
```

This result establishes machine-readable EPUB conformance for the checked file.
It does not establish usability in every reading system or accessibility after a
future Pressbooks import and re-export.

The rebuilt Word import file remains 90 pages. A render comparison with the
previous candidate found one changed page, page 55, containing the intentionally
updated Module 9 source link. Direct inspection of that page found normal line
wrapping with no clipping, overlap, or page overflow.

## PDF Metadata and Structure

All 15 handouts were regenerated from their canonical PowerPoint decks after
replacing generic exporter metadata with the actual week title, author, course,
language, and release-candidate status. Automated inspection confirms for every
PDF:

- the exact week title and `Atilio Barreda` author metadata;
- one page per slide, totaling 214 pages;
- extractable text and no replacement glyphs;
- no encryption;
- document language `en-US`;
- display-document-title preference; and
- a marked structure tree.

The PowerPoint source files carry the same title, author, language, and status
metadata. The reproducible maintenance commands are:

```bash
python3 tools/update_deck_metadata.py
python3 tools/export_handout_pdfs.py
```

A 96-DPI pixel comparison against the prior committed handouts passed for all
214 pages. The metadata regeneration changed no visible slide content:

```text
PDF render comparison: PASS (214 pages are pixel-identical at 96 DPI)
```

## PDF Tag-Tree Findings

MuPDF object inspection found that LibreOffice emitted only `Figure`, `Div`, and
`P` structure types. It did not emit semantic heading, list, table, or link tags,
and no `Figure` object included `/Alt` or `/ActualText`. Many figure objects are
decorative slide shapes, so the raw figure count is not a count of meaningful
images. It does show that the exporter did not distinguish decorative artifacts
from meaningful visuals with usable alternative-text metadata.

| Week | Total tags | Figure | Div | P | Figure tags with alt/actual text |
|---:|---:|---:|---:|---:|---:|
| 1 | 396 | 87 | 151 | 158 | 0 |
| 2 | 590 | 154 | 203 | 233 | 0 |
| 3 | 375 | 91 | 133 | 151 | 0 |
| 4 | 342 | 79 | 117 | 146 | 0 |
| 5 | 351 | 75 | 126 | 150 | 0 |
| 6 | 359 | 93 | 122 | 144 | 0 |
| 7 | 432 | 116 | 155 | 161 | 0 |
| 8 | 320 | 76 | 116 | 128 | 0 |
| 9 | 550 | 129 | 201 | 220 | 0 |
| 10 | 459 | 118 | 161 | 180 | 0 |
| 11 | 437 | 109 | 153 | 175 | 0 |
| 12 | 445 | 104 | 169 | 172 | 0 |
| 13 | 427 | 106 | 160 | 161 | 0 |
| 14 | 340 | 84 | 127 | 129 | 0 |
| 15 | 400 | 96 | 152 | 152 | 0 |

The [PDF Association's tagged-PDF guidance](https://pdfa.org/resource/tagged-pdf-q-a/)
explains why a marked/tagged flag alone is not enough: useful accessibility
depends on appropriate semantic tags, logical order, and alternatives for
non-text content.

**PDF handout accessibility claim: NOT MADE**

The PDFs are convenience handouts. The canonical Markdown modules and exact
structured-text transcripts are the authoritative alternatives. A later PDF/UA
remediation project would need to establish semantic headings, lists, tables,
links, decorative-artifact treatment, meaningful visual alternatives, logical
reading order, and human validation in a representative reader.

## Publication Boundary

The EPUB conformance pass and corrected PDF metadata strengthen the release
candidate. They do not close Pressbooks, LMS, external accessibility review,
classroom pilot, fellowship approval, or publication gates. No tag, push,
deposit, import, or publication is authorized by this report.
