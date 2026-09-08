# Data-Informed Teaching Protocol

## Purpose

This protocol uses small, low-stakes learning signals to decide what to retrieve,
reteach, or extend. It does not predict individual success, automate grades, or
turn student access problems into academic deficits.

## Evidence Sources

| Evidence | Frequency | Decision supported | Not used for |
|---|---|---|---|
| beginning diagnostic | once before instruction | select early SQL and relational examples | grading or placement labels |
| three retrieval prompts | most meetings | identify concepts needing immediate feedback or spacing | polished-writing grades |
| one lab checkpoint | each lab | distinguish execution, verification, and explanation problems | surveillance of every click |
| one exit prompt | most meetings | choose the next worked example | permanent student classification |
| critical writing rubric | eight responses | monitor evidence and tradeoff communication | grammar-only ranking |
| midterm/final common criteria | twice | evaluate integrated course outcomes | public student comparison |
| post-course inventory | once after instruction | compare concept categories and material access | retroactive grade changes |

## Meeting Cycle

### Retrieve

Students answer three short prompts without notes. The instructor scans for
correct concept categories and common reasoning errors. Immediate feedback should
explain the distinction, not merely announce an answer.

### Model and Fade

Choose one complete worked example based on the retrieval pattern. Ask students to
predict a result or evidence type before revealing it. Follow with a partially
worked example that removes one or two supports, not every support at once.

### Build

Students complete the individual lab. Record one common checkpoint: for example,
whether the student states result grain, captures both allow and deny evidence, or
verifies a separate restore. Track error categories, not a public list of names.

### Check

Use one exit prompt that asks for evidence and a limitation or tradeoff. The exit
response selects the next instructional action.

## Aggregate Decision Prompts

- **Below 70 percent conceptually correct:** reteach before adding complexity.
  Change the representation, such as moving from prose to a table, diagram,
  transcript, or executable example.
- **70 to 84 percent:** continue with one targeted retrieval prompt and one faded
  example in the next meeting.
- **85 percent or above:** advance, but schedule spaced retrieval in a later week.
- **More than 15 percent blocked by access or tooling:** switch to the equivalent
  open/static path and repair setup guidance before interpreting performance.

These are decision prompts, not algorithms. Small class sizes, missing responses,
question ambiguity, accommodations, and the difference between a typo and a
conceptual error require professional judgment.

## Error Categories

Use a small vocabulary to make revision possible:

- prerequisite recall;
- concept distinction;
- syntax or command shape;
- result interpretation;
- verification gap;
- unsafe credential or access practice;
- platform/network access;
- instruction ambiguity; and
- workload/cognitive-overload signal.

An error can have more than one category. Platform/network access must be recorded
separately from conceptual understanding.

## SQL Review Decision Example

If students can write `SELECT` and `WHERE` but cannot state result grain after a
one-to-many join, do not solve the problem with more syntax drills. Return to two
small relations, predict matching pairs, draw the joined tuples, and then run the
SQL. Recheck the same grain concept later with ticket events and again with an
aggregation pipeline.

## Recovery Decision Example

If students equate a nonzero dump file with recovery, show two artifacts: one file
that exists but cannot restore and one separate restore with verification checks.
Ask students to rank the evidence and state what each item proves. The next lab
checkpoint should require a behavioral query, not another screenshot.

## Equity and Privacy Rules

- Keep individual grades and access disclosures in institution-approved systems.
- Publish only aggregate or de-identified course-improvement findings.
- Do not publish small-cell results that could reveal a student.
- Do not create predictive risk scores or public dashboards of named students.
- Do not treat account, disability, language, device, or network barriers as lack
  of ability.
- Offer the equivalent path before grading the technical evidence.
- Explain to students what evidence is collected and how it changes instruction.

## Revision Log Template

```text
Module and version:
Evidence source:
Aggregate pattern:
Access/tooling pattern (separate):
Interpretation and uncertainty:
Instructional change:
OER file(s) changed:
Accessibility/license check:
Recheck date and prompt:
Observed result after change:
```

## Fellowship Reporting

Report the number and type of OER revisions supported by aggregate evidence, not
claims that the materials caused an outcome without an appropriate research
design. Useful descriptive reporting includes concept-category change, lab
completion/revision patterns, common rubric dimensions, material cost, access
barriers, and the specific resource revision made in response.

Separate three statements:

1. **Observed:** what the aggregate evidence shows.
2. **Inferred:** the plausible instructional interpretation and uncertainty.
3. **Changed:** the OER revision or teaching action taken.
