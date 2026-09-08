# Course Content Creation README

Use this guide when creating weekly course materials for this course or adapting the workflow to another course.

The goal is to create materials that are useful in class, easy for students to follow, and aligned with the syllabus instead of generating extra files that duplicate each other.

## Core Principles

- Start from the syllabus and textbook before creating anything.
- Make student-facing materials, not instructor planning notes disguised as student content.
- Keep weekly content small enough to actually use in class.
- Prefer in-class work, short checkpoints, and practical skill-building over long take-home deliverables.
- Use official documentation and high-quality educator resources when platform details matter.
- Do not create duplicate assignment descriptions across multiple files.
- Do not publish teacher-only notes, answer keys, cheat sheets, or scripts unless explicitly requested.

## Standard Workflow

1. Read the syllabus topic for the week.
2. Check the assigned textbook chapter or relevant textbook sections.
3. Review the previous and next week so the new content fits the course sequence.
4. Research current official resources if the topic involves modern tools, cloud platforms, software docs, certifications, pricing, or platform workflows.
5. Decide the weekly structure before writing files.
6. Create or update the week README as a short guide.
7. Create student-facing labs or assignments.
8. Create the PowerPoint only after the week structure is clear.
9. Export a PDF version of the PowerPoint when requested or when students need an easy viewing format.
10. Update the root README links.
11. Verify that files are linked, non-duplicative, and student-facing.

## Preferred File Pattern

For a normal week, use this structure:

```text
week_##/
  README.md
  Week_##_Descriptive_Title.pptx
  Week_##_Descriptive_Title.pdf
  lab_day1_short_topic.md
  lab_day2_short_topic.md
```

Use fewer files when possible.
Do not create several handouts that explain the same assignment.

If a major assignment applies across multiple weeks, put it in one canonical file at the course root:

```text
final_project.md
midterm_project_options.md
```

Then link to that file from weekly materials instead of copying the same requirements into weekly READMEs.

## Weekly README Expectations

The weekly README should be a short guide, not a full textbook chapter and not a second copy of every assignment.

Include:

- week focus
- syllabus alignment
- list of course materials
- official links or textbook connections
- two-day structure if the course meets twice
- learning outcomes
- recommended instructor flow

Avoid:

- full assignment rubrics
- repeated final project requirements
- long student deliverable lists
- teacher-only notes
- content that belongs in the PowerPoint or lab file

## PowerPoint Expectations

PowerPoints should teach students directly.

Slide body content should:

- explain the topic, not tell the instructor what to focus on
- use plain language
- avoid text overflow
- include diagrams, visuals, comparisons, examples, or workflows when useful
- avoid huge walls of text
- avoid generic decorative visuals that do not teach anything

Speaker notes should:

- include a clear teaching script when requested
- explain what the instructor should say or emphasize
- include extra context that would clutter the slide
- define terms in beginner-friendly language
- connect concepts to labs and assignments

For technical/database topics, good slides usually include:

- one mental model diagram
- one concrete example
- one "why this matters" explanation
- one tradeoff or limitation
- one connection to the lab or project

Always check for:

- no overflowing text
- no unreadably small text
- no teacher-only planning language on student-facing slides
- no duplicated assignment requirements from another file

## Lab Expectations

Labs should be practical, in-class, and easy to submit.

Default lab style:

- individual work only unless explicitly changed
- no teams or group submissions unless explicitly requested
- fewer steps rather than many tiny instructions
- short in-class checkpoints
- concrete actions students can finish during class
- plain-language reflection questions
- one submission location, usually Brightspace

Good lab submissions include:

- a completion screenshot when using an external training platform
- a short text response in Brightspace
- a small code file, SQL file, JSON file, or query file when appropriate
- a short plan file only when planning is the point of the lab

Avoid:

- too many deliverables
- long reports for in-class labs
- requiring students to create markdown files when a Brightspace text response is enough
- making students use GitHub unless the assignment truly needs it
- mixing live-coding activities and student labs into the same unclear task

## External Platform Labs

When using MongoDB University, Supabase, GitHub Education, certification resources, or similar platforms:

- link the exact lab or resource
- state whether it is live-coded by the instructor or completed by students
- make the submission simple
- include a security warning if credentials, connection strings, keys, tokens, or `.env` files are involved
- do not ask students to expose secrets in screenshots

For MongoDB University labs, a strong pattern is:

- complete the linked lab
- submit a completion screenshot
- answer 3-4 short reflection questions
- explain how the lab connects to the current week or final project

## Assignment Design Preferences

Assignments should be beginner-friendly and career-connected.

Good assignments:

- connect to realistic database administration tasks
- ask students to explain choices, not just follow clicks
- emphasize evidence: schema, seed data, queries, indexes, access control, backup/restore, reliability
- are small enough to finish
- allow multiple correct answers when modeling or design is the goal

Avoid assignments that:

- become full app-building projects by accident
- require paid cloud features
- require too much setup before learning begins
- assume students already know advanced tooling
- grade UI polish more than database thinking

## Final Or Major Projects

Keep major project instructions in one canonical file.

For this course style, a final project should usually be:

- a small cloud database administration project
- beginner-friendly
- focused on database artifacts and administrative evidence
- not primarily a web app

Preferred platform options:

- Supabase/PostgreSQL
- MongoDB/Atlas
- both only if the split is simple and defensible

Submission should usually be based on:

- code or database artifacts
- SQL files, model files, seed data, query examples, and admin notes
- instructor access to cloud database projects when needed
- Brightspace text or file submission when that is simpler than GitHub

GitHub should be optional unless the course objective specifically requires Git/GitHub.

## Teacher-Only Materials

Do not publish teacher-only materials by default.

Teacher-only materials include:

- answer keys
- cheat sheets
- hidden instructor scripts
- grading keys
- generated solution scripts
- private setup notes

If teacher-only files are needed, keep them out of normal student-facing folders when possible.
Use a clearly named private/internal location such as:

```text
.internal_teacher_guides/
```

Do not link internal teacher materials from the student-facing README.
Do not stage, commit, or push internal materials unless explicitly told to.

## Research Expectations

Research is required when information may have changed.

Use official sources for:

- MongoDB Atlas
- MongoDB University
- Supabase
- PostgreSQL
- GitHub Education
- certifications
- cloud database features
- pricing or free-tier rules
- software workflows

For pedagogy, prefer:

- education research
- STEM/CS teaching resources
- project-based learning guidance
- active learning and worked-example strategies

Translate research into usable classroom design.
Do not dump research summaries into student-facing files unless students actually need them.

## Style Preferences

Use clear, direct language.

Student-facing content should be:

- readable by beginners
- practical
- concrete
- respectful
- not overly formal
- not overloaded with terminology before examples

Prefer:

- "What you will do"
- "Why this matters"
- "What to submit"
- "Success standard"
- "Useful links"

Avoid:

- unnecessary academic jargon
- long abstract introductions
- giant rubrics in weekly READMEs
- repeated assignment text across files
- vague "explore the topic" instructions

## Quality Checklist

Before considering the content done, check:

- The week matches the syllabus.
- The textbook connection is correct.
- The root README links the new materials.
- The week README is short and not duplicative.
- Labs are individual unless group work was explicitly requested.
- In-class assignments can realistically be done in class.
- Brightspace text responses are used when files are unnecessary.
- PowerPoint slides are student-facing.
- Speaker notes are useful for teaching.
- PDF exists if requested.
- No secret credentials appear in examples or screenshots.
- No teacher-only materials are published.
- No obsolete links or stale file references remain.

## Reusable Prompt For Another Course

When starting a new course repo, use a prompt like this:

```text
Read the syllabus and textbook materials first. Then create the next week of course content using my preferred structure.

Keep the weekly README short. Create student-facing slides, practical in-class labs, and only the minimum number of files needed.

Do not duplicate assignment instructions across files. If a major project applies across multiple weeks, create one canonical root-level assignment file and link to it.

Make labs individual unless I explicitly ask for groups. Prefer Brightspace text responses and simple in-class checkpoints over many deliverables.

For PowerPoints, make the slides teach students directly, avoid text overflow, include visuals/diagrams, and put a useful teaching script or focus notes in the speaker notes.

Do not publish teacher-only cheat sheets, answer keys, hidden scripts, or generated solution scripts unless I explicitly ask.
```
