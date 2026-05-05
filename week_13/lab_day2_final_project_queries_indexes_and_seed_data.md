# Week 13 Lab Day 2
## Final Project Queries, Indexes, and Seed Data

## Purpose
Today you will create evidence that your final project database can answer useful questions.

The goal is to move from "I have an idea" to "I have data, queries, and an index decision."

## Individual Work Only
This lab is individual.
There is no group work.

## What To Do

### 1. MongoDB University Skill Builder
Open the MongoDB University lab:

[Lab: Indexing Design Fundamentals](https://learn.mongodb.com/learn/course/indexing-design-fundamentals-on-demand-devrel-content/indexing-design-fundamentals/lab-indexing-design-fundamentals?page=1)

Use this lab to learn the new skill for today:
- identifying the query workload
- choosing an index that supports the query
- thinking about index key order
- using `explain()` to check whether MongoDB uses an index

If you are using Supabase/Postgres for your final project, still complete or review the MongoDB lab.
The same core idea applies: an index should support a real query, not just exist as a random object.

### 2. Seed Data Plan
Write a seed data plan.

Include:
- how many records you need for a useful demo
- where the data will come from
- whether the data is real, public, synthetic, or manually created
- one edge case you will include
- one data quality problem you might need to clean

### 3. Four Useful Queries
Write four questions your database should answer.

Examples:
- Which events are happening next?
- Which products are low in stock?
- Which tickets are still open?
- Which users submitted the most items?
- Which records were added this month?
- Which items belong to this category or owner?

### 4. Query Drafts
Draft the actual query for each question.

For Supabase/Postgres:
- write SQL

For MongoDB/Atlas:
- write MQL or aggregation pipeline stages

If your database is not ready yet, write the query as accurately as you can and label it as a draft.

### 5. Index Decision
Choose one query that may need an index.

Explain:
- which field or fields should be indexed
- which query the index supports
- why the index might help
- what the cost of the index might be
- what you learned from the MongoDB University indexing lab that applies to this decision

### 6. Connection Check
Write whether you can currently connect to your cloud database.

For MongoDB Atlas:
- confirm your Atlas project/cluster exists
- confirm you can see your database or collection
- confirm the instructor will be able to review the project or you know how to add them

For Supabase/Postgres:
- if using Colab or an IPv4-only network, use the Supabase pooler connection string, not the direct IPv6-only connection string
- confirm you can open the SQL Editor
- confirm you can create or inspect at least one table

## In-Class Checkpoint
Submit one Brightspace text response.

Include:
1. one sentence explaining what the MongoDB University indexing lab taught you
2. seed data plan
3. four useful project questions
4. four query drafts
5. one index decision
6. cloud connection check

## Success Standard
You are successful if your project now has enough data, query, and index evidence to become a real final submission.
