# Week 12 Lab Day 2
## Restore-First Thinking and Final Project Studio

## Purpose
Day 2 connects reliability to project execution.

Students first learn why backup/restore planning matters.
Then they start the final project with a small, concrete build plan.

## Big Idea
A backup is only a claim until restore has been tested or at least planned carefully.

For this course, students do not need enterprise disaster recovery.
They do need a beginner-level runbook that explains:
- what should be backed up
- how restore would happen
- what evidence would prove the restore worked
- and what data loss or downtime risk remains

## Individual Work Only
This lab is individual.
There is no group work.

## First Half - Backup and Restore Concepts

Answer these in plain language:

1. What is a backup?
2. What is a restore?
3. What is point-in-time recovery?
4. Why should restore steps be planned before an incident?
5. Why might restoring a database cause downtime?
6. What would you check after a restore to prove the application is usable?

Useful links:
- [Supabase Backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase Backup and Restore using the CLI](https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore)
- [MongoDB Atlas Back Up, Restore, and Archive Data](https://www.mongodb.com/docs/atlas/backup-restore-cluster/)
- [Atlas Backup Scheduling](https://www.mongodb.com/docs/atlas/backup/cloud-backup/schedule-backup/)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

## Second Half - Final Project Studio

Start your final project folder or code artifact location.

Use the [final project assignment](../final_project.md) only if you need the full project requirements.

Create a short project plan file named:
- `final_project_plan.md`

## What Goes in `final_project_plan.md`

### 1. Project Title
Use a clear title.

Example:
- `Campus Club Event Tracker`

### 2. Platform Path
Choose one:
- Supabase/Postgres
- MongoDB/Atlas
- both

### 3. Problem Statement
Write 3-5 sentences explaining what the database will help manage.

### 4. Data Model Plan
Follow the minimum scope rules in the final project assignment.
List the first tables, collections, or both-platform split you plan to build.

### 5. Seed Data Plan
Describe:
- what sample records you will create
- how many records are enough for testing
- what edge case or unusual record you will include

### 6. Query Plan
List at least four questions your database should answer.

Examples:
- Which events are coming up this week?
- Which products are low in stock?
- Which tickets are still open?
- Which users submitted the most items?

### 7. Admin and Reliability Plan
Write 5-7 bullets covering:
- one index you might need
- one access-control concern
- one backup concern
- one restore verification step
- one reliability tradeoff or limitation

## In-Class Checkpoint
Submit:
1. `week12_day2_reliability_notes.md`
2. `final_project_plan.md`

## What Goes in `week12_day2_reliability_notes.md`
Include:
1. 3-5 sentences explaining why restore-first thinking matters
2. one restore verification checklist with at least four checks
3. one Supabase/Postgres reliability idea
4. one MongoDB/Atlas reliability idea

## Success Standard
Day 2 is successful if students leave with a project plan that is small enough to finish and concrete enough to start building immediately.
