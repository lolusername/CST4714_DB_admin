# Week 1: Enter the Profession and Rebuild Relational Thinking

## The Week's Question

What does a database professional operate, and how does the relational model turn
real-world facts into structures we can query and protect?

## What You Will Be Able to Do

- distinguish data, a database, a DBMS, and a managed platform;
- map provider and customer responsibilities in Supabase and Atlas;
- create a safe, reproducible GitHub evidence artifact;
- identify relations, tuples, attributes, domains, keys, and relationships; and
- reason with selection, projection, product, join, union, and difference before
  writing SQL.

## Read and Use

- [Module 1: The database is a system of responsibilities](../textbook/module_01_responsibility.md)
- [Module 2, Sections 1-2: Relations and relational algebra](../textbook/module_02_sql.md)
- [Week 1 student deck](week_01_responsibility_relational_thinking.pptx)
- [Week 1 PDF handout](week_01_responsibility_relational_thinking.pdf)
- [Week 1 transcript](week_01_responsibility_relational_thinking_transcript.md)

## Day 1: Responsibility, Evidence, and Safe Setup

We begin with an outage claim and separate the application, network, managed
platform, DBMS, query, and data layers. Then we compare what the provider operates
with what the customer must still decide and verify.

Complete [Lab 1: Build a responsibility and evidence map](lab_01_responsibility_evidence.md).

The only submission is the URL to your completed `responsibility_map.md` file.

## Day 2: Relational Model and Algebra Recovery

We rebuild the language underneath SQL: relation, tuple, attribute, domain,
schema, instance, key, selection, projection, product, join, union, and difference.
The focus is not memorizing Greek symbols. The focus is predicting what one output
row means and which operations turn the inputs into that output.

Complete [Lab 2: Relational reasoning before SQL](lab_02_relational_reasoning.md).

The only submission is the URL to your completed `relational_reasoning.md` file.

## Optional Industry Extension: Status-Page Evidence Audit

This activity is optional, ungraded, and does not add a submission.

Choose one resolved incident from the public status history for Supabase or
MongoDB Cloud. In six lines, record the user-visible symptom, affected layer,
provider action, customer action if any, recovery evidence, and one fact the
notice does not establish. Treat the notice as an operations source: distinguish
what it directly reports from what you infer. Keep the note in your course folder
only if it helps you; no account or cloud change is required.

## End-of-Week Self-Check

Without notes, explain:

1. why Supabase is not the same thing as PostgreSQL;
2. how selection differs from projection;
3. why a join can create more rows than either input; and
4. what evidence is stronger than a screenshot that merely says "Success."

If any answer is unclear, revisit the worked examples before Week 2. Week 2 turns
the relational operations into executable SQL.
