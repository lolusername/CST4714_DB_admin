# Week 10 Lab
## MongoDB University Lab Track: Day 2 Modeling and Indexing

## Purpose
Day 2 should keep the same structure as Day 1:
- a short live instructor walkthrough first,
- then individual MongoDB University lab work.

The goal is to move students from general MongoDB familiarity into:
- embedding vs referencing,
- SQL-to-document translation,
- and one first-pass indexing decision.

## Big Idea
Day 2 is not about covering every MongoDB feature.
It is about spending real time in the official MongoDB labs so students move from:
- document thinking,
- to relationship decisions,
- to practical workload-based modeling.

## In Class Live Coding

### 1. Embed vs Reference Demo

Use this for:
- showing one embedded student record,
- showing one referenced student record,
- and explaining why workload matters more than blindly copying SQL tables.

Suggested live example:
- one student with current courses,
- one reusable course record,
- one update scenario where duplication helps reads but creates maintenance cost.

### 2. SQL-to-Document Demo

Use this for:
- translating one small relational design into document shapes,
- showing that more than one JSON/document answer can be valid,
- and explaining what should stay in one source of truth.

Suggested live tables:
- `students`
- `courses`
- `enrollments`

### 3. First Index Demo

Use this for:
- showing one common read pattern,
- choosing one first index,
- and explaining the read/write tradeoff in plain language.

# Lab: #

## Submit screenshot of completion w/ score ##
### 1. Modeling Data Relationships
- [Open the lab here](https://learn.mongodb.com/courses/modeling-data-relationships)

This is the main Day 2 unit.
It is where students work directly with:
- embedding,
- referencing,
- one-to-one and one-to-many relationships,
- and workload-based modeling.

### 2. Relational (SQL) to Document Model
- [Open the lab here](https://learn.mongodb.com/courses/relational-to-document-model)

This is the Day 2 bridge unit.
It helps students connect:
- normalized SQL structure,
- document boundaries,
- duplication tradeoffs,
- and source-of-truth decisions.

### 3. MongoDB Indexes
- [Open the lab here](https://learn.mongodb.com/courses/mongodb-indexes)

Use this as the shorter Day 2 checkpoint.
Students should leave able to explain:
- why indexes help common reads,
- why indexes are not free,
- and one field they would index first in a simple application.

## MongoDB University Labs to Complete in Order
1. [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)
2. [Relational (SQL) to Document Model](https://learn.mongodb.com/courses/relational-to-document-model)
3. [MongoDB Indexes](https://learn.mongodb.com/courses/mongodb-indexes)

### 4. In-Class Response: Event-Driven Inventory Platform Case Study
- File: `reading_response_inventory_case_study_video.md`

Complete this after the MongoDB University work.
This is an individual Day 2 response that asks students to connect the case-study video back to:
- modeling decisions,
- workload,
- and database tradeoffs.
