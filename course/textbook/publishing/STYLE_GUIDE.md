# Second-Edition Publication Style

The Word/PDF design resolves the `compact_reference_guide` preset with one named
override, `textbook_typography`, so a long technical book reads more like a real
textbook than an office memo.

## Exact Token Map

| Token | Value |
|---|---|
| page | US Letter portrait |
| margins | 0.82 in top/bottom; 0.85 in left/right |
| header/footer distance | 0.42 in |
| body | Linux Libertine G, 11 pt, left aligned, 6 pt after, 1.18 line spacing |
| title | Linux Biolinum G, 30 pt, dark teal `#0B4F4A` |
| heading 1 | Linux Biolinum G, 19 pt, dark teal, 18 pt before, 10 pt after, page break before |
| heading 2 | Linux Biolinum G, 14 pt, teal, 14 pt before, 7 pt after |
| heading 3 | Linux Biolinum G, 11.5 pt, slate blue, 10 pt before, 5 pt after |
| block code | Liberation Mono, 9 pt; 1.05 line spacing |
| inline code | Liberation Mono, 8.5 pt |
| code block | pale teal-gray fill, teal left rule, 2 pt before and 7 pt after |
| captions and listing labels | Linux Biolinum G, 8.5 pt, muted slate |
| bullet/number text indent | 0.375 in; 0.188 in hanging indent |
| table width | up to 6.8 in / 9792 DXA; compact content uses its natural width |
| table text | 10 pt body, 9.5 pt repeated header; flexible row heights |
| code in table cells | Liberation Mono, 9 pt; retains code styling |
| table indent | 120 DXA |
| cell margins | 80 DXA top/bottom, 120 DXA start/end |
| table header fill | pale teal `#DCEFEB` |
| running header | book title and draft status, 8 pt muted slate |
| footer | centered draft label and automatic page number |

The cover follows the `editorial_cover` header pattern: generous title scale,
one coherent visual metaphor, clear subtitle, author, edition status, and license.

Explicit font assignments remove inherited theme-font attributes so Word and
LibreOffice cannot silently substitute a theme face. The build requests DejaVu
Math TeX Gyre for equations; exported mathematical symbols still require visual
inspection. Syntax colors come from `syntax.theme`. Its darkest necessary
categories retain at least 4.5:1 contrast on the code background; labels also
identify the language without relying on color.

## Source Rules

- Use semantic headings rather than manually formatted bold paragraphs.
- Put executable material in a fenced block with a language.
- Use `$...$` and `$$...$$` for mathematics; do not spell out Greek operators in
  code font when a conventional symbol exists.
- Write SQL literals such as `TRUE`, `FALSE`, and `UNKNOWN` as inline code,
  including in truth tables. Keep logical operators and variables as math.
- Use `\text{ticket\_id}` for a literal column name inside an equation. This
  preserves a single upright label in Word/PDF rather than spaced variables.
- Include equation text when estimating table widths. A cell containing only
  an equation is not an empty cell. Keep a short list introduction with its
  first item rather than leaving it at the foot of a page.
- Keep alt text descriptive and captions interpretive: state what the reader
  should notice, not only what objects appear.
- Use descriptive linked titles in further reading rather than displaying raw
  URLs. Retain the exact source destinations; shorter display text improves
  reading, navigation, and page flow without removing references.
- Retain Graphviz `.dot` or SVG source beside rendered PNG diagrams.
- Redact account identifiers, connection strings, addresses, email, and secrets
  before a cloud screenshot enters the book.
- Treat Word, PDF, HTML, and EPUB as synchronized outputs, not independent
  manuscripts.
