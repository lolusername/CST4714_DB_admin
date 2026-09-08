# CST4714 Final Project

## Due Date
The final project is due May 26, 2026.

## Purpose
The final project is a beginner-friendly cloud database administration project.

Students should show that they can design, build, query, document, and reason about a small database system using one of the course platforms.
This is not mainly a web app project.
Students may build a simple interface if they want, but the grade is based on database work and administrative evidence.

## Platform Options

### Option A - Supabase/PostgreSQL
Best for projects with clear tables, relationships, SQL queries, indexes, and access-control or RLS thinking.

### Option B - MongoDB/Atlas
Best for projects with flexible documents, embedded arrays or subdocuments, MQL queries, indexes, and Atlas reliability planning.

### Option C - Both
Use both only if the split is simple and defensible.

A good split might use Postgres for structured core records and MongoDB for flexible logs, activity events, or changing document-shaped data.
Do not choose both just to look more advanced.

## Beginner-Friendly Project Ideas
- Campus club event tracker
- Small inventory tracker
- Course resource library
- Appointment or tutoring scheduler
- Simple support ticket tracker
- Book lending tracker
- Personal budget or expense tracker
- Student project submission tracker
- Fitness or habit tracker
- Restaurant menu and order tracker

Students may propose another small idea if it has a clear database scope.

## Scope Rules
Keep the project small.

Minimum expected scope:
- 3-5 tables for Supabase/Postgres
- or 2-4 collections for MongoDB/Atlas
- or a very small split if using both

Do not build:
- a full social network
- a full e-commerce platform
- a full learning management system
- a complex multi-tenant SaaS app
- a project that depends on paid cloud features

## Final Submission
The final submission is not a required GitHub repo.
GitHub is optional if a student already wants to use it, but it is not the submission requirement.

Students submit code/database artifacts and enough cloud access or evidence for the instructor to verify the work.

Required project artifacts:
- schema or model files
- seed data files
- query examples
- admin/reliability notes
- short written explanation
- short presentation materials

Platform-specific review access:
- Supabase/Postgres students submit SQL/project files that let the instructor inspect the schema, seed data, queries, and admin notes.
- MongoDB/Atlas students should add the instructor to the Atlas organization/project/team for review, or provide equivalent instructor access approved by the instructor.
- Both-platform students submit the Postgres/Supabase artifacts and add the instructor to the MongoDB Atlas project/team if Atlas is used.

MongoDB/Atlas review access should let the instructor verify:
- database and collection names
- sample documents
- indexes
- schema/modeling choices
- backup/reliability notes

## Required Evidence

Data model evidence:
- Supabase/Postgres projects need tables, columns/types, primary keys, foreign keys, and at least one index.
- MongoDB/Atlas projects need collections, document examples, an embed/reference explanation, and at least one index.
- Both-platform projects need a clear explanation of what each platform owns and why the split is useful.

Seed data:
- at least 20 realistic records total for a single-platform project
- or at least 10 records per platform for a two-platform project

Query evidence:
- at least four meaningful queries that answer realistic questions about the project data

Admin evidence:
- one index decision and explanation
- one access-control or permission concern
- one backup/restore plan
- one restore verification checklist
- one limitation or reliability tradeoff

Written explanation:
- 700-1000 words
- explain the project purpose, platform choice, data model, query examples, admin/reliability decisions, and what would improve with more time

Presentation:
- 5-7 minutes
- show what the database manages, the data model, one query, one admin/reliability decision, and one lesson learned

## Recommended Timeline
Week 12:
- choose project path
- choose scenario
- write `final_project_plan.md`
- create a project folder or code artifact location

Week 13:
- build schema or collections
- load seed data
- write first queries

Week 14:
- add admin evidence
- write backup/restore runbook
- peer review and revise

Week 15:
- final report
- presentation
- portfolio cleanup
- final project due May 26, 2026

## Grading Priorities
- 25 pts: clear data model
- 20 pts: meaningful queries
- 20 pts: admin and reliability evidence
- 15 pts: seed data and reproducibility
- 10 pts: written explanation quality
- 10 pts: presentation clarity
