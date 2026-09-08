# Accessibility and Adaptation Guide

## Design Principle

Accessibility is part of the instructional design, not a final export setting.
Every essential idea should be available through meaningful text, a visible
example, and an executable or static evidence path. Equivalent paths should
assess the same outcome without requiring the same interface action.

## Modules and Markdown

- Use one descriptive page title and hierarchical headings without skipped
  levels.
- Write descriptive link text instead of “click here.”
- Keep paragraphs focused and code blocks short enough to discuss.
- Explain abbreviations on first use.
- Introduce a command with its purpose, expected output, and likely failure mode.
- Provide a text description immediately before or after every essential diagram.
- Do not rely on tables alone when a sequence or list is more readable on a small
  screen.
- State which details are conceptual and which are current platform behavior.

## Labs

- Begin with the operating purpose and the single submission.
- Keep the required path to a few coherent sections rather than many tiny steps.
- Separate setup from the evidence-producing task.
- State the expected kind of output without supplying a private answer.
- Give keyboard-accessible alternatives to drag, hover, or color-only actions.
- Provide a cloud and open/static path that produce equivalent reasoning evidence.
- Avoid grading screenshot aesthetics. Accept copied text, exported output, or a
  structured observation when it proves the same outcome.
- Permit additional processing time through the institution's accommodation
  process without increasing the conceptual workload.

## Slide Decks and Spoken Scripts

- Visible slide text teaches students; it does not tell an instructor what to say.
- Speaker notes contain complete spoken prose, not directions such as “discuss” or
  “focus on.”
- Use a reading-order-aware layout with a unique title on every slide.
- Maintain strong foreground/background contrast and do not encode meaning by
  color alone.
- Keep body text large and reduce words before reducing type size.
- Give diagrams text labels and include a meaningful text equivalent in the notes
  and transcript.
- Avoid automatic motion. Any animation must preserve meaning when omitted.
- Identify decorative images as decorative; give informative images concise alt
  text that states the instructional purpose.
- Export and inspect the PDF; a PowerPoint that looks correct can still produce a
  poor reading order or clipped PDF.

## Notebooks

- Use a descriptive title, learning outcomes, and an ordered run path.
- Keep one conceptual action per code cell where practical.
- Explain inputs and expected output before execution.
- Do not communicate status only through red/green color.
- Print key values as text rather than relying only on a chart.
- Include text descriptions for every chart or distribution visualization.
- Prompt for secrets at runtime and keep the default path runnable without an
  account.
- Label simulation limits. An offline library must not be described as proving a
  cloud-server feature it cannot enforce.
- Preserve meaningful outputs in the release notebook while removing noisy
  installation traces and credentials.

## Code and Data

- Use readable names and short comments that explain non-obvious purpose.
- Include a small fixture so students can inspect the entire relevant shape.
- State source, retrieval date, transformation, license/terms, and omissions for
  public data.
- Represent missing values intentionally and explain type conversion.
- Use deterministic seeds or stable identifiers when students must compare
  results.
- Supply CSV and JSON alternatives when one shape creates an access barrier.

## Equivalent Evidence Examples

| Original interaction | Equivalent path | Same outcome retained |
|---|---|---|
| click through Atlas Data Explorer | run or inspect an MQL notebook with `mongomock` | construct and interpret a filter/update |
| run a cloud lock incident | analyze a complete two-session transcript | identify waiter, blocker, mitigation, and verification |
| draw a diagram by hand | submit a labeled text outline or Mermaid source | identify entities, ownership, flow, and failure point |
| submit a screenshot | submit copied result text plus environment/action note | prove observed behavior |
| listen to a live explanation | read the complete transcript | access the same instructional script |

Equivalent does not mean easier or harder. It means that the evidence addresses
the same learning outcome without an irrelevant access barrier.

## Cognitive Accessibility and Workload

Use a stable class pattern: retrieve, model, fade, build, check. Repeated structure
reduces navigation overhead while task complexity grows. Early examples should be
complete and annotated. Middle examples should remove selected steps. Late cases
should present symptoms and constraints while retaining an evidence checklist.

Avoid adding difficulty through:

- many submission files;
- unexplained interface switching;
- long helper-function abstractions before basic code is understood;
- hidden prerequisites;
- credentials embedded in starter code;
- time pressure unrelated to the outcome; or
- simultaneous introduction of a new model, language, platform, and dataset when
  one can remain familiar.

## Adaptation Checklist

When replacing a platform, dataset, or example:

1. preserve the operating question and learning outcome;
2. identify the prerequisite that remains or changes;
3. update the worked example and expected evidence;
4. supply a new fallback;
5. record source and license changes;
6. test keyboard use and nonvisual text equivalents;
7. execute code from a clean environment;
8. render slides and PDFs; and
9. ask whether the adaptation adds construct-irrelevant difficulty.

## Manual Release Review

Automated checks cannot establish full accessibility. Before release, manually
inspect heading structure, link meaning, slide reading order, color contrast,
keyboard use, transcripts, diagram descriptions, notebook output, PDF selection
order, and the equivalence of fallback evidence.
