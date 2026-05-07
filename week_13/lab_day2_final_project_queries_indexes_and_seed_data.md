# Week 13 Lab Day 2
## Final Project Queries, Aggregations, Indexes, and Seed Data

## Purpose
Today you will create evidence that your final project database can answer useful questions.

The goal is to move from "I have an idea" to "I have data, queries, one reporting/aggregation idea, and an index decision."

## Individual Work Only
This lab is individual.
There is no group work.

## What To Do

### 1. MongoDB University Skill Builder
Open the MongoDB University lab:

[Lab: Fundamentals of Data Transformation](https://learn.mongodb.com/learn/course/fundamentals-of-data-transformation/fundamentals-of-data-transformation/lab-fundamentals-of-data-transformation?page=1)

Use this lab to learn the new skill for today:
- building a basic aggregation pipeline
- filtering early with `$match`
- grouping and summarizing with `$group`
- shaping output with `$project`
- sorting and limiting output for readable results
- using `explain()` to reason about pipeline performance

If you are using Supabase/Postgres for your final project, still complete or review the MongoDB lab.
The same core idea applies: useful final projects need reporting queries, not just raw tables or collections.

### 2. Instructor Mini-Lesson: Indexing After Aggregation
After the MongoDB University lab, return to the Week 13 PowerPoint:

`Week_13_Scaling_and_Final_Project_Build.pptx`

Use slides 16-22.

The goal is to connect today's aggregation/reporting work to one final project index decision.

If the instructor assigns extra official MongoDB University practice, use:

[Lab: Indexing Design Fundamentals](https://learn.mongodb.com/learn/course/indexing-design-fundamentals-on-demand-devrel-content/indexing-design-fundamentals/lab-indexing-design-fundamentals?page=1)

This is optional unless the instructor explicitly says to complete it.
The required work is still the final project checkpoint below.

### 3. Seed Data Plan
Write a seed data plan.

Include:
- how many records you need for a useful demo
- where the data will come from
- whether the data is real, public, synthetic, or manually created
- one edge case you will include
- one data quality problem you might need to clean

### 4. Four Useful Queries
Write four questions your database should answer.

Examples:
- Which events are happening next?
- Which products are low in stock?
- Which tickets are still open?
- Which users submitted the most items?
- Which records were added this month?
- Which items belong to this category or owner?

### 5. Query Drafts
Draft the actual query for each question.

For Supabase/Postgres:
- write SQL

For MongoDB/Atlas:
- write MQL or aggregation pipeline stages

If your database is not ready yet, write the query as accurately as you can and label it as a draft.

### 6. One Reporting or Aggregation Idea
Choose one query that would make your project demo more useful.

Write:
- what the output should show
- whether it needs filtering, grouping, sorting, limiting, or joining/lookup
- why the output would help someone understand your project
- what you learned from the MongoDB University data transformation lab that applies to this query

Examples:
- count records by category
- show the five most recent records
- show records grouped by owner, status, risk, or type
- join or look up related information from another collection/table
- summarize totals, averages, or counts for a dashboard

### 7. Index Decision
Choose one query that may need an index.

Explain:
- which field or fields should be indexed
- which query the index supports
- why the index might help
- what the cost of the index might be
- whether filtering early in a query or pipeline affects this decision

### 8. Connection Check
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
1. one sentence explaining what the MongoDB University data transformation lab taught you
2. seed data plan
3. four useful project questions
4. four query drafts
5. one reporting or aggregation idea
6. one index decision
7. cloud connection check

## Success Standard
You are successful if your project now has enough data, query, reporting, and index evidence to become a real final submission.
