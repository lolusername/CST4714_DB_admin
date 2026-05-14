# Week 14 - Polyglot Tradeoffs and Final Project Finish Line

## Week Focus
Week 14 follows the syllabus topic:
- advanced topics
- polyglot persistence
- distributed database tradeoffs
- final project work session and review

This week is designed to be very easy to run.
The new content is short and practical, and most of class should be used for final project evidence, review, and finishing work.

## Individual Work Only
All Week 14 work is individual.
There is no group work and no combined submission.

## Week 14 Course Materials
- `Week_14_Polyglot_Tradeoffs_and_Final_Project_Finish_Line.pptx`
- `Week_14_Day2_Distributed_Database_Incident_Game.pptx`
- `teacher_guide_day1_supabase_admin_evidence.md`
- `teacher_guide_day2_distributed_database_incident_room.md`
- `week14_sqlite_supabase_postgres_admin_demo.ipynb`
- `week14_mongodb_atlas_incident_demo.ipynb`
- `lab_day1_final_project_admin_evidence_check.md`
- `lab_day2_distributed_database_incident_room.md`

## Direct Official Links
- [Supabase Connection Strings and IPv4 Pooler Guidance](https://supabase.com/docs/guides/database/connecting-to-postgres)
- [Supabase Backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase Postgres Indexes](https://supabase.com/docs/guides/database/postgres/indexes)
- [MongoDB Atlas Backup, Restore, and Archive](https://www.mongodb.com/docs/atlas/backup-restore-cluster/)
- [MongoDB Query Optimization](https://www.mongodb.com/docs/manual/core/query-optimization/)
- [MongoDB University: Replication in MongoDB](https://learn.mongodb.com/courses/replication-in-mongodb)
- [MongoDB University Practice: Read and Write Concerns with MongoDB Deployments](https://learn.mongodb.com/learn/course/replication-in-mongodb/lesson-5-read-and-write-concerns-with-mongodb-deployments/last-lesson)
- [MongoDB Atlas IP Access List](https://www.mongodb.com/docs/atlas/security/ip-access-list/)
- [Open Week 14 MongoDB Atlas Incident Demo in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_14/week14_mongodb_atlas_incident_demo.ipynb)

## Two-Class Structure

### Class 1
First half:
- polyglot persistence
- when one database is enough
- when two databases are justified
- distributed tradeoffs and data ownership
- Supabase/Postgres review: tables, SQL evidence, RLS thinking, backups, restore checks, and connection strings

Second half:
- final project admin evidence snapshot
- platform-specific access, restore, and index evidence
- instructor-review readiness

### Class 2
First half:
- distributed database incident game
- source of truth and consistency
- MongoDB University practice on read concern, write concern, and read preference
- idempotent retries
- fast reads vs correct reads

Second half:
- incident commander lab
- optional MongoDB Atlas incident repair notebook demo
- repair-pattern choice
- tradeoff writing
- short optional final-project connection

## Learning Outcomes
By the end of Week 14, students should be able to:
1. explain polyglot persistence in plain language
2. defend using one database or two databases for a project
3. explain a distributed tradeoff involving consistency, duplication, ownership, or failure
4. complete a short final project admin evidence snapshot
5. explain why source of truth matters in a distributed database incident
6. verify that the final project is ready for May 26, 2026

## Recommended Instructor Flow
1. Use `Week_14_Polyglot_Tradeoffs_and_Final_Project_Finish_Line.pptx`.
2. Keep the polyglot lecture short and connect every concept to final project decisions.
3. Use the Supabase review slides before the Day 1 lab if many students are using Supabase/Postgres.
4. Use `teacher_guide_day1_supabase_admin_evidence.md` as the instructor prep guide if students have Supabase/Postgres questions.
5. Use `week14_sqlite_supabase_postgres_admin_demo.ipynb` as an optional quick demo of schema, seed data, queries, indexes, query plans, and backup-style exports.
6. Run `lab_day1_final_project_admin_evidence_check.md` as a short platform-specific admin evidence snapshot, not a long checklist.
7. For Day 2, use `Week_14_Day2_Distributed_Database_Incident_Game.pptx`.
8. Use `teacher_guide_day2_distributed_database_incident_room.md` if you want a detailed run-of-show and sample explanations.
9. Have students open the MongoDB University practice on read and write concerns before the incident write-up.
10. Optionally demo `week14_mongodb_atlas_incident_demo.ipynb` if you want live Atlas code.
11. Run `lab_day2_distributed_database_incident_room.md`.
12. End Week 14 with students able to explain source of truth, safe retries, and distributed tradeoffs in plain language.
