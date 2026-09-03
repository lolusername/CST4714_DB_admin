# Week 1: How Applications Use Databases

## The Week's Question

What happens between an application's **Submit** button and the data stored in a
database, and how does the relational model organize those facts?

## What You Will Be Able to Do

- distinguish data, a database, a DBMS, and a managed cloud platform;
- trace a request through a client, application, identity check, DBMS, and stored
  data;
- explain how PostgreSQL relates to Supabase and MongoDB relates to Atlas;
- describe several kinds of technical database work;
- identify relations, tuples, attributes, domains, keys, and relationships; and
- use selection, projection, product, join, union, and difference to describe a
  result before writing SQL.

## Before Class: Assigned Reading

- Read [Chapter 1: How database-backed applications work](../../textbook/module_01_responsibility.md) before Day 1.
- Before Day 2, read [A Relation Represents One Kind of Fact](../../textbook/module_02_sql.md#a-relation-represents-one-kind-of-fact) and [Relational Algebra Gives Us a Reasoning Vocabulary](../../textbook/module_02_sql.md#relational-algebra-gives-us-a-reasoning-vocabulary) in Chapter 2.

No reading notes are submitted this week. Bring one question or example from the
reading to class.

## Class Materials

- [Week 1 student deck](week_01_responsibility_relational_thinking.pptx)
- [Week 1 PDF handout](week_01_responsibility_relational_thinking.pdf)

## In-Class Lab

- [Week 1 simple lab](lab_01_application_database_map.md)

## Day 1: From an App Click to Stored Data

We trace a familiar action, such as creating a playlist or support ticket,
through the application and database stack. Then we tour the Supabase and Atlas
interfaces and connect their menus to PostgreSQL, MongoDB, networking, identity,
and data.

Complete the simple in-class lab before the end of Day 1.

## Day 2: Rebuild Relational Thinking

We use a tiny service-desk dataset to review relation, tuple, attribute, domain,
schema, instance, primary key, and foreign key. Then we calculate small
selection, projection, product, join, union, and difference results by hand.

If you want extra practice after class, use the same prompt used in today's
lab and expand your answer with one more entity and two additional relationships.

## Optional Industry Extension: Read a Public Architecture Diagram

This activity is optional, ungraded, and does not add a submission.

Choose the public architecture page for an application or service you use.
Identify the client, application or API, identity boundary, database or storage
service, and one failure point. Compare that published architecture with the
request path from Day 1 and note one component that the simplified class model
does not show.

## End-of-Week Check

You should be able to answer these without looking up definitions:

1. What is the difference between PostgreSQL and Supabase?
2. What does one tuple in the `tickets` relation represent?
3. How does selection differ from projection?
4. Why does a join need a matching condition?

Week 2 converts the relational operations into executable SQL and provides a
substantial review for anyone who has not used SQL recently.
