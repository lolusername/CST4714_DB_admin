# Teaching From This Handoff

1. Open the [course README](README.md) and the relevant week. It links the
   reading, PowerPoint, lab, and notebook used in both meetings.
2. Read that week's section of the [instructor guide](instructor/implementation_guide.md).
   Open the PowerPoint Notes pane for the complete word-for-word explanation.
   The transcript contains the same script if you prefer reading it as text.
3. Rehearse the listed demonstration with the supplied fixture. For database
   connections use the [setup guide](instructor/technical_setup_troubleshooting.md).
   Follow the stated cleanup. Do not run setup against a database you need to keep.
4. Use the existing lab submission and midterm requirements. Do not turn optional
   extensions, retrieval prompts, or reading notes into additional deliverables.

## Editing

PowerPoints and Word documents are editable. For synchronized textbook formats,
edit the eight chapter sources and run `uv run tools/rebuild_textbook.py`.
The rebuild requires Pandoc, Graphviz, ImageMagick, LibreOffice, and the installed
book fonts. Set `SOFFICE` to the LibreOffice executable if it is not on PATH.
If you directly edit the Word book instead, that is a legitimate working copy;
do not rebuild over it until you have reconciled those changes with the sources.

This is a frozen handoff: edits here do not update the earlier full-course draft
or the separate GitHub directory automatically. Make the intended copy explicit.
The GitHub copy contains only student-facing material. The OER-admin brief,
instructor guidance, editable syllabus, and build tools stay in this bundle.

The [OER admin brief](OER_ADMIN_BRIEF.md) includes a presentation route and a
draft email. Nothing has been sent, uploaded, or published.
