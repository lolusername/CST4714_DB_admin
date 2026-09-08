# Operating Cloud Databases

This directory is the editable source for the assigned textbook,
*Operating Cloud Databases*, second edition. The earlier manuscript remains in
`../../archive/oer_first_edition/` for provenance and is not assigned in the
current course.

Student reading formats are available in [Word](publishing/exports/operating_cloud_databases_second_edition_draft.docx),
[PDF](publishing/exports/operating_cloud_databases_second_edition_draft.pdf),
[web](publishing/exports/operating_cloud_databases_second_edition_draft.html), and
[EPUB](publishing/exports/operating_cloud_databases_second_edition_draft.epub).

## Edit Here

- Edit chapter prose in `module_01_*.md` through `module_15_*.md`.
- Edit diagram structure in `figures/*.dot` or `figures/*.svg`.
- Replace only publication-safe cloud images in `figures/cloud_interfaces/`.
- Edit front matter, part introductions, appendices, publication styling, and
  build settings in `publishing/`.

Code fences must carry a language such as `sql`, `json`, `javascript`, `python`,
or `bash`. Mathematical notation uses Pandoc/LaTeX delimiters: `$...$` inline and
`$$...$$` for display equations. The build converts the same notation to Word
equations, MathML for web/EPUB, and the PDF rendering.

## Do Not Edit as Source

The `.docx`, `.pdf`, `.html`, and `.epub` files in
`publishing/exports/` are generated review and reading formats. Rebuild
them after changing the source instead of maintaining four conflicting books.

Run the build from `course`:

```bash
uv run tools/build_textbook.py
```

The second edition remains an unpublished draft until formal review and approval.
