# CST4714 Database Administration — 15-Week Curriculum Plan

This plan ties the existing repo materials to a complete 15-week run. Each week lists learning goals, suggested in-class flow, key artifacts already in the repo, and any added prep/assessment so the course has an end-to-end story from SQL fundamentals through MongoDB/Supabase admin and the final project.

## Week-by-Week Plan

### Week 1 – Orientation & Foundations
- Goals: define the DBA role, survey relational vs NoSQL, set up tooling (psql, Supabase account, git repo for labs).
- In class: syllabus walkthrough (`Database Administration (CST4714) – 15-Week Syllabus (Open Resources).docx`), environment checks, quick SQL warm-up.
- Assignment: install tooling checklist + 3-paragraph reflection on “What does a DBA own?”

### Week 2 – Relational Refresher & Data Modeling Basics
- Goals: review relational concepts, ER modeling vocabulary, keys, and integrity constraints.
- In class: ER mini-lab translating user stories to tables; short quiz to surface gaps.
- Assignment: draft a simple ERD and 5 queries against a sample schema.

### Week 3 – PostgreSQL Architecture & Cloud DB Management
- Goals: internal architecture, cloud DBaaS roles, schema management, advanced SQL.
- Repo materials: `week_3/Postgres_architecture.pptx`, `week_3/Cloud.pptx`, `week_3/review.sql`.
- In class: lecture + Supabase SQL Editor lab using `review.sql`; start pgexercises via Supabase.
- Assignments: architecture analysis, cloud DB comparison matrix, SQL challenge (10 queries).

### Week 4 – Advanced SQL, Constraints, Triggers, Transactions
- Goals: write functions/views/triggers, enforce constraints, reason about ACID/isolation.
- Repo materials: `week_4/Week4_Advanced_SQL_Transactions.pptx`, `week_4/week4_advanced_sql_lab_student.ipynb`, `week_4/instructor_guide.md`.
- In class: slides + demo + notebook lab; midterm project proposal kickoff.
- Assignments: lab submission; midterm proposal draft; discussion on constraint/trigger war stories.

### Week 5 – Database Design & Normalization
- Goals: functional dependencies, 1NF→BCNF, normalization trade-offs, schema critique.
- Repo materials: `week_5/Week5_Database_Design_Normalization.pptx`, `week_5/week5_design_demo.sql`, `week_5/week5_normalization_lab.md`, `week_5/instructor_guide.md`.
- In class: interactive lecture + live normalization demo + design studio lab.
- Assignments: normalization lab, midterm proposal revision, denormalization discussion post.

### Week 6 – Backup/Restore, Security Basics, and Ops Runbooks (PostgreSQL/Supabase)
- Goals: practice pg_dump/pg_restore, role/privilege design, connection pooling (PgBouncer), and routine maintenance.
- In class: checkpoint on proposals; live backup/restore drill in Supabase; create minimal runbook (backups, roles, rotation, monitoring hooks).
- Assignment: submit runbook + evidence of one restore test; update proposals with admin plan notes.

### Week 7 – Midterm Review & SQL/Design Drills
- Goals: consolidate Weeks 1–6; troubleshoot locks/isolation; rehearse midterm scenarios.
- Repo materials: `week_7/lesson_plan_midterm_review.md`, `week_7/student_review_packet.md`, `week_7/midterm_review_sql_drills.sql`, `week_7/midterm_review_slides.pptx`.
- In class: diagnostic quiz, roundtable on architecture/cloud, SQL drills, normalization studio, performance drills, project huddle.
- Assignment: midterm exam/practical + study reflection; project desk-check follow-ups.

### Week 8 – MongoDB & NoSQL Foundations
- Goals: contrast document model vs relational, CRUD with `mongosh`, intro to Atlas.
- Repo materials: `week_8/mongodb_nosql_intro.pptx`, `week_8/MongoDBShellCheatSheet.pdf`, `week_8/teacher_guide_mongodb_intro.md`.
- In class: instructor-led demo + shell practice; assign MongoDB University intro module; Joining Array Fields lab.
- Assignment: lab screenshot submission + short reflection on when to choose documents.

### Week 9 – MongoDB Philosophy, CAP, and Atlas Onboarding
- Goals: CAP trade-offs, NoSQL model survey, Atlas provisioning, automation basics.
- Repo materials: `week_9/mongodb_cap_nosql.pptx`, `week_9/mongodb_cap_lab.ipynb`, `week_9/sample_mongodb_script.js`.
- In class: CAP recap, model tour (Redis/Cassandra/Neo4j/Mongo), Atlas walkthrough, automation via `mongosh --file`, read/write concern lab.
- Assignment: export notebook with observations; adapt automation script with schema validation; prep for indexing deep dive.

### Week 10 – Relational → Document Modeling & Credential Kickoff
- Goals: apply MongoDB relationship patterns, embed vs reference decisions, validation with `jsonSchema`.
- Repo materials: `week_10/relational_to_document_modeling.pptx`, `week_10/relational_to_document_lab.js`.
- In class: review project access patterns; run lab script together; validation deep dive; launch MongoDB University Relational to Document Model Skill Badge.
- Assignment: finish/customize lab script, submit reflection; progress on skill badge.

### Week 11 – Indexing & Query Performance Lab (MongoDB)
- Goals: design single/compound/multikey indexes; analyze plans with `explain`; use Atlas Performance Advisor.
- Repo materials: `week_11/README.md` (flow + commands).
- In class: query shape inventory, explain-plan lab, compound index practice, Performance Advisor discussion.
- Assignment: document chosen indexes with before/after metrics; complete indexing course module; short reflection.

### Week 12 – Atlas Administration & Schema Design Patterns
- Goals: consolidate MongoDB design patterns; practice cluster admin (networking, access, backups); connect to Atlas free tier.
- Repo materials: `week_12/MongoDB.pdf`, `week_12/MongoDB_Design.pptx`, `week_12/mongodb_atlas_free_access.pdf`.
- In class: lecture on design patterns + hands-on Atlas setup (IP allowlists, users, backups, alerts).
- Assignment: run one backup/restore on Atlas sandbox; document network/auth config; map 3 patterns to project collections.

### Week 13 – Final Project Build Sprint & Consultations
- Goals: lock team rosters, draft data dictionary/diagrams, admin plan draft, start automation scripts.
- Repo materials: `week_13/README.md`, `final_group_project_outline.pdf`.
- In class: working sprint with rotating consults; checkpoint share-out.
- Deliverables: roster, data dictionary + ER/aggregation diagrams, admin plan draft, seed/migration scripts, consultation notes.

### Week 14 – Peer Review, Troubleshooting, and Demo Polish
- Goals: peer feedback on build/demo, fix blockers (auth, backups, HA tests, monitoring), rehearse demo flow.
- Repo materials: `week_14/README.md`.
- In class: peer review rounds, troubleshooting clinic, working sprint, class share-out.
- Deliverables: backup/restore evidence, security roles/auditing, replication/HA test, monitoring/alerts, near-final slides.

### Week 15 – Final Project Support, Supabase/Mongo Review, Real-World Case Studies
- Goals: remove final blockers for the project, refresh Supabase + MongoDB admin fundamentals, and analyze real implementations.
- New materials: `week_15/week15_final_support.pptx` (created in this update).
- In class (suggested 150 min):
  - Quick readiness survey and targeted Q&A.
  - Supabase admin refresher (roles, RLS, backups, PgBouncer) + checklist for project handoff.
  - MongoDB Atlas refresher (indexes, profiling, backup/restore, replica set health).
  - Case study discussions:
    - **Supabase:** HappyTeams migration from Heroku to Supabase (performance + PgBouncer, 2023) — https://supabase.com/blog/case-study-happyteams.
    - **MongoDB Atlas:** Toyota Connected telematics platform achieving 99.99% availability with Atlas (2024) — https://www.mongodb.com/solutions/customer-case-studies/toyota-connected.
  - Lab time: teams verify backup/restore, HA/failover test, and security checks; instructor desk checks.
  - Optional lightning run-through of final demo (10–12 min per team).
- Deliverables: final project package (design doc, scripts, admin evidence, monitoring screenshots, slides, written report) submitted before presentations.

## Major Milestones
- **Midterm Proposal Draft:** end of Week 4; revision Week 5; checkpoint Week 7.
- **Midterm Exam/Practical:** Week 7.
- **Final Project Timeline (per `final_group_project_outline.pdf`):**
  - Week 12: case study selection & scope.
  - Week 13: detailed design & tooling.
  - Week 14: build, test, admin validation.
  - Week 15: polish, presentation, written report.

## Tooling & Environments
- PostgreSQL/Supabase: Supabase SQL Editor for labs; pg_dump/pg_restore and PgBouncer for admin drills.
- MongoDB: `mongosh`, Atlas free-tier clusters, Atlas Profiler/Performance Advisor, Jupyter notebooks with `pymongo`.
- Collaboration: team repos + shared docs for designs, runbooks, and evidence.
