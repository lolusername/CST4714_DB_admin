# Production, Validation, and Evaluation Plan

## Single-Source Publishing

Structured Markdown is the source for modules, labs, assignments, scripts, and
transcripts. Generated outputs include student web pages, PDFs, EPUB, slide
handouts, and Brightspace-ready packages. Canonical assignment files are linked,
not copied, into weekly guides.

## Quality Gates

Every public release must pass:

1. **Content alignment:** every activity names an outcome and produces evidence
   used by that outcome.
2. **Technical execution:** SQL and JSON fixtures parse; notebooks execute on
   offline data; cloud cells are isolated and safely prompt for credentials.
3. **Slide quality:** every slide renders without clipping or unintended overlap;
   visible text is student-facing; speaker notes contain a complete spoken script.
4. **Accessibility:** headings, links, contrast, text alternatives, transcripts,
   and PDF reading order receive automated and manual checks.
5. **Source integrity:** every external fact, dataset, adaptation, and image has a
   traceable source and compatible use.
6. **Link health:** public links resolve and time-sensitive platform instructions
   record a verification date.
7. **Privacy and safety:** no credentials, student data, private grading keys, or
   personally identifying analytics are present.

## Classroom Evaluation Cycle

### Before the Course

- administer the ungraded diagnostic;
- record access barriers and provide equivalent paths;
- compare concept categories, not named-student rankings; and
- identify two ideas requiring an early worked example.

### During the Course

- use three-question retrieval checks in most meetings;
- score one common checkpoint in each lab;
- record common error categories;
- use one exit question to identify the next instructional decision; and
- log platform problems separately from conceptual errors.

### Decision Rules

- Below 70 percent correct on a core idea: reteach with a different representation
  before adding complexity.
- 70-84 percent: use one targeted retrieval item and a faded example.
- 85 percent or above: move forward and schedule spaced retrieval.
- More than 15 percent blocked by access or tooling: use the equivalent local or
  static path and revise setup instructions before judging learning.

### After the Course

- compare pre/post concept categories;
- sample rubric evidence from the midterm and final;
- collect student feedback about clarity, access, relevance, and workload;
- audit broken links and changed free-tier features;
- revise the highest-impact misconception and access points first; and
- publish a de-identified revision note with the next version.

## Data Stewardship

Individual grades and submissions stay in institution-approved systems. Public
evaluation reports use aggregate or de-identified results. No predictive risk
score, biometric data, browser surveillance, or public student profile is part of
the project.
