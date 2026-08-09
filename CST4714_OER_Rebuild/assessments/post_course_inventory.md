# End-of-Course Concept and Confidence Inventory

## Purpose

This ungraded inventory is paired with the beginning diagnostic. Complete it
without searching first. It measures changes in course-level concepts and
confidence; it is not a final exam and is not used to rank students.

## Part A: Applied Concepts

1. A managed PostgreSQL query fails. Separate one possible provider
   responsibility, one customer responsibility, and one piece of evidence you
   would inspect first.
2. State what one row represents in a query that joins `tickets` to
   `ticket_events`, and explain why the ticket may repeat.
3. Translate this question into relational operations and SQL: “Which residents
   have no ticket?”
4. Choose one database constraint and describe an expected-failure test proving
   it is enforced.
5. Two sessions appear slow, but one is waiting for the other. Name evidence that
   distinguishes blocked work from expensive work.
6. Write an actor-action-resource least-privilege rule and name one expected allow
   and one expected deny.
7. A query becomes faster after an index is added. Name the before/after evidence
   and one cost you would evaluate before keeping the index.
8. A backup command succeeds. Name at least four different restore checks needed
   before claiming the system can recover.
9. Represent a ticket and its status history as either related tables or a
   document. Defend the choice with one read pattern, one update pattern, and one
   growth assumption.
10. Distinguish replication, backup, partitioning, and sharding in one sentence
    each.
11. A public-data import reports 75 successful writes. Name checks for identity,
    type or quality, rerun behavior, and a question-driven result.
12. Two databases contain different versions of the same customer fact. State the
    first ownership question and two pieces of evidence you would collect before
    repairing it.

## Part B: Evidence Judgment

For each claim, label the evidence **weak**, **partial**, or **strong for the
stated scope**, then explain why.

1. “The screenshot shows that the query ran.”
2. “The test role can select its own two rows and receives an expected denial for
   another resident's row.”
3. “The dump file exists and has a nonzero size.”
4. “A separate database was restored; tables, counts, keys, relationships,
   constraints, and one meaningful query were verified.”
5. “The index should stay because the plan changed from a scan to an index scan.”
6. “The import is rerunnable because the stable source identifier is a primary
   key and a second run preserves the count.”

## Part C: Confidence

Rate each statement from 1 (not yet) to 5 (I can explain and demonstrate it).

- I can recover forgotten SQL by reasoning from result grain and relational
  operations.
- I can create related tables and test their integrity rules.
- I can interpret a database error or symptom using evidence.
- I can use GitHub to publish a safe, reproducible technical artifact.
- I can connect to a cloud database without saving a credential.
- I can explain a PostgreSQL query plan and index tradeoff.
- I can write basic MQL and defend embedding or referencing.
- I can distinguish replication from backup and verify a restore.
- I can explain one capacity, sharding, or polyglot tradeoff.
- I can describe a course skill in a project review or job interview.

## Part D: Access and Material Feedback

1. Did you spend money on any course-required book, database plan, subscription,
   certification, or software? If yes, identify what and why.
2. Which access path worked best: cloud platform, Colab, local tool, or static
   fallback?
3. Which platform or network barrier most affected your learning?
4. Which module, lab, notebook, diagram, or transcript most helped you understand
   a difficult idea?
5. Name one instruction that should be clarified and one activity that should be
   retained.

## Aggregate Comparison Categories

For course improvement, compare beginning and ending evidence by category rather
than by publicly identifying students:

- data-system responsibility;
- relational model and SQL;
- integrity and safe change;
- concurrency and evidence;
- security and least privilege;
- performance and indexes;
- backup, restore, and reliability;
- JSON, MQL, and document modeling;
- scale and multi-system reasoning; and
- reproducibility and career communication.

Report counts or percentages only when the group is large enough to protect
privacy. Do not publish named responses, grades, access disclosures, or predictive
student labels.
