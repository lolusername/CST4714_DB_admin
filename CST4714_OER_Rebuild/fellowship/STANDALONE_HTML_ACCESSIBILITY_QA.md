# Standalone HTML Accessibility QA

> **Evidence boundary:** This is a local release-candidate check, not an
> accessibility certification, external approval, or substitute for testing the
> final Pressbooks webbook and LMS course.

## Artifact and Environment

- **Artifact:** `operating_cloud_databases_v1.0.0-rc.1.html`
- **Test date:** August 9, 2026
- **Environment:** Safari 26.5.2 on macOS 26.5.2
- **Source:** the self-contained HTML export built from the canonical 15-module
  Markdown text
- **Representative Safari keyboard result: PASS**
- **Screen-reader test: NOT RUN**

## Checks Completed

### Semantic structure

Direct inspection of the document and Safari accessibility tree found:

- one document title;
- one table-of-contents navigation landmark before the main content;
- one focusable main landmark with `id="main-content"` and `tabindex="-1"`;
- a visible-on-focus skip link whose target is the main landmark;
- logical heading levels for the book and modules;
- nested list structure;
- tables exposing column headers;
- links with accessible text; and
- code content retained in the reading order.

This check establishes that the authored standalone export exposes the expected
structure. It does not establish how an imported copy will be transformed by
Pressbooks or Brightspace.

### Reflow and overflow

The complete single-page book was inspected at representative desktop and mobile
widths, including 1280-pixel and 390-pixel viewports. No page-level horizontal
overflow was observed. Long code remains inside a locally scrollable code block
rather than forcing the entire page wider.

### Representative keyboard sequence

An actual Safari keyboard sequence was run against the local export:

1. `Option+Tab` moved focus to **Skip to main content**.
2. `Return` activated the link.
3. The URL changed to `#main-content`.
4. The viewport moved from the page beginning into the main reading region.
5. Safari's accessibility focus moved to the main-content container.

The sequence demonstrates that the skip mechanism is operable with the keyboard
in this tested browser. It is deliberately described as representative because
every one of the book's links was not traversed manually.

## Checks Not Completed

- A complete keyboard traversal of every navigation and content link was not
  completed.
- VoiceOver or another screen reader was not used to review spoken output,
  reading order, table navigation, link context, or code pronunciation.
- The EPUB was not reviewed in a representative reading system.
- The candidate has not been imported into Pressbooks or Brightspace, so those
  platforms' navigation, focus behavior, transformations, and assistive-
  technology output remain untested.
- All PDF handouts report tagged structure, are unencrypted, contain extractable
  text, and were visually reviewed. They are not represented as accessible PDFs
  until tag-tree quality and assistive-technology reading order receive human
  review.

## Required Retest Before Publication

1. Import the approved candidate into a private Pressbooks book.
2. Repeat the skip-link sequence and traverse representative navigation, links,
   tables, and code using keyboard input alone.
3. Use VoiceOver or another representative screen reader to check title,
   landmarks, headings, lists, tables, links, code context, and reading order.
4. Inspect one imported chapter with dense code, one with a table, the table of
   contents, and front/back matter.
5. Repeat representative checks in the intended Brightspace shell.
6. Record the reviewer, environment, defects, corrective commit, and retest in
   `EXTERNAL_REVIEW_AND_RELEASE_GATES.md`.

## Interpretation

The local HTML has a sound semantic and keyboard-accessible starting point. The
remaining work is human assistive-technology review and platform verification,
not authorship of missing chapters, labs, or other semester content.
