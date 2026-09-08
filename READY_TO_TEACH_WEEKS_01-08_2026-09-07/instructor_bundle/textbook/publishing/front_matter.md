# About This Book {.unnumbered}

*Operating Cloud Databases* is a beginner-friendly, lab-first textbook for
students who need both a substantial relational/SQL review and an introduction to
modern managed data systems. It develops one operating method across every
topic: define the question, model the mechanism, run a controlled check, interpret
the result, and state the tradeoff.

The book begins with relations, relational algebra, SQL, schema, and constraints.
It then teaches safe change, transactions, access control, performance, and
recovery in PostgreSQL and Supabase. This classroom volume contains Chapters 1-8. Later chapters of the developing
textbook are intentionally outside this handoff.

This second edition adds mathematical notation, explicitly
labeled code listings, editable conceptual diagrams, dated and redacted cloud
interface figures, expanded relational review, and worked operational examples. The original edition remains
preserved separately.

## Who This Is For {.unnumbered}

The primary reader has written some SQL before but may not remember how relational
operations explain a query. No prior cloud administration or MongoDB experience is
assumed. Examples stay small enough to reason about, while the questions mirror
real operational work: What does this query mean? What can fail? Who owns the
control? Which result would change the decision? What remains uncertain?

## How to Read a Chapter {.unnumbered}

Every chapter follows a stable learning pattern:

1. **Operating question:** the problem the chapter teaches you to reason about.
2. **Learning outcomes:** actions you should be able to perform and explain.
3. **Concepts and models:** durable ideas before product menus.
4. **Numbered code listings:** executable or inspectable examples with a named
   language and an explanation of the expected result.
5. **Worked example:** one decision carried from question through verification.
6. **Misconceptions:** plausible shortcuts that fail under closer inspection.
7. **Practice, retrieval, and transfer:** individual work that asks you to reuse
   the idea in a new situation.

## The Recurring Case {.unnumbered}

Metro Support is a small synthetic service-request system with users, tickets,
and ticket events. Its scale is intentionally modest. A beginner can inspect every
row, while the same facts support joins, constraints, locks, access policies,
indexes, backups, document models, aggregation, replication, integration, and
incident communication.

The dataset is not presented as a production city system. It is a controlled
environment for learning how an operator moves from a concrete question to a
tested decision.

## Cloud Interfaces and Change {.unnumbered}

Interface figures were captured from live free-tier teaching projects on August
25, 2026 and redacted before inclusion. They show what was observed, not a
promise that a menu or plan will remain identical. Each screenshot is paired with
the durable concept it demonstrates and a reminder to verify current official
documentation before relying on a platform feature.

No student must purchase a textbook, subscription, certification, or database
plan. Required cloud work has a local, static, or simulated route when an account,
network, plan, or interface prevents access.

## Accessibility and Formats {.unnumbered}

The canonical source uses semantic headings, descriptive links, text alternatives,
language-labeled code blocks, and source equations that convert to Word equations
and MathML. The same book is built as editable Word, PDF, standalone HTML, and
EPUB so readers can select the format that works best with their device and
assistive technology. Slide decks in the complete course package have structured
text transcripts.

Weekly guides name the sections to read before each meeting. The chapters also
offer optional practice for revision and transfer; those exercises are not extra
graded submissions unless the instructor assigns them. A chapter's shell listing
and its associated Python notebook teach related ideas in different languages.
Use the stated environment and fixture rather than pasting shell code into a
Python cell or assuming that two teaching datasets have identical rows.

## Edition Status {.unnumbered}

This is the **unpublished Chapters 1-8 classroom volume**, prepared September 7, 2026. It is complete enough for
substantive review and classroom piloting, but it is not a formally deposited or
approved release. Version and review status appear in the source, exports, and
fellowship release records so draft work cannot be mistaken for publication.
