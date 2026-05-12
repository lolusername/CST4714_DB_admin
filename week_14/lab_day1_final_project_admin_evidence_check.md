# Week 14 Lab Day 1
## Admin Evidence Snapshot

## Purpose
Today is not a busy-work checklist.

Today you will write one short admin evidence snapshot for your final project.
This should help you finish the final submission, not create extra work.

## Individual Work Only
This lab is individual.
There is no group work.

## What To Do

### 1. One-Database Or Two-Database Decision
Write 3-5 sentences.

Answer:
- Are you using Supabase/Postgres, MongoDB/Atlas, or both?
- Why is that still the right choice?
- If you are using both, what does each database own?
- If you are using both, what is one risk of splitting the data?

If you are only using one database, say why one database is enough.

### 2. Complete Your Platform Track
Only complete the track that matches your project.

#### Supabase/Postgres Track
Write one short paragraph that explains:
- one table or relationship you can show as evidence
- one permission or RLS concern
- one backup/restore check you would run
- one index tied to a real SQL query

Example:
`My project uses Supabase/Postgres because the data is structured. I can show the tickets and users tables, including the relationship between tickets.user_id and users.user_id. A permission concern is that students should create tickets, but only staff should close them. If I restored the project, I would check table counts and rerun the open-ticket query. I would index status and created_at because users often search open tickets by date.`

#### MongoDB/Atlas Track
Write one short paragraph that explains:
- one collection or document shape you can show as evidence
- one permission or review-access concern
- one backup/restore check you would run
- one index tied to a real MQL or aggregation query

Example:
`My project uses MongoDB/Atlas because the records have flexible nested details. I can show the tickets collection with embedded status history. A permission concern is that the instructor needs approved Atlas review access without exposing passwords. If I restored the project, I would check collection names, sample documents, and indexes. I would index status and created_at because users often search open tickets by date.`

#### Both-Platform Track
Write one short paragraph that explains:
- what Supabase/Postgres owns
- what MongoDB/Atlas owns
- which system is the source of truth for the most important data
- one risk if the two systems disagree
- one restore check for each platform

### 3. Review Readiness
Write one sentence explaining how the instructor will verify your project.

Examples:
- `I will submit SQL files, seed data, query examples, and screenshots from Supabase.`
- `I will add the instructor to my Atlas project and include collection names, sample documents, queries, and index notes.`
- `I will submit Supabase files and provide Atlas review access because my project uses both.`

## Optional Demo
If you need a concrete example, open:

`week14_sqlite_supabase_postgres_admin_demo.ipynb`

The notebook uses SQLite, but the ideas transfer to Supabase/Postgres:
- tables
- seed data
- useful queries
- indexes
- query plans
- backup-style exports

## Submit
Submit one Brightspace text response.

Include:
1. one-database or two-database decision
2. your platform-track paragraph
3. review-readiness sentence

## Success Standard
You are successful if your response can be reused in your final project report or presentation.
