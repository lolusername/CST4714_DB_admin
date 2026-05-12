# Week 14 Day 1 Teacher Guide
## Supabase/Postgres Review, Polyglot Tradeoffs, and Admin Evidence

## What Today Is Really About
Today is not a new-build day.
It is an evidence day.

Students should leave with language and artifacts they can reuse in the final project:
- one-database or two-database decision
- one platform-specific admin evidence paragraph
- one instructor review-readiness sentence

The final project is due May 26, 2026.
The last class meeting is May 19, 2026.

## Fast Class Plan
Use `Week_14_Polyglot_Tradeoffs_and_Final_Project_Finish_Line.pptx`.

Suggested flow:
- Slides 1-6: polyglot persistence and distributed tradeoffs
- Slides 7-9: admin evidence, restore thinking, review readiness
- Slides 10-14: Supabase/Postgres review
- Slide 19: launch Day 1 lab
- Lab: `lab_day1_final_project_admin_evidence_check.md`

The lecture should be short.
The lab should be the main class activity.

## Core Concepts You May Need To Explain

### Polyglot Persistence
Polyglot persistence means using more than one database type in the same system.

Beginner framing:
- One database is usually enough.
- Two databases are only justified when each has a clear job.
- A two-database project is not automatically better.

Good example:
- Postgres owns users, permissions, orders, and structured records.
- MongoDB owns flexible logs, events, nested records, or documents that change shape often.

Bad example:
- The student stores the same important data in both systems and cannot say which one is the source of truth.

### Source of Truth
The source of truth is the official place where a fact lives.

If a student uses both Supabase/Postgres and MongoDB/Atlas, ask:
- Which platform owns the official copy of each important fact?
- What happens if the two platforms disagree?
- Which system should be restored first after an incident?

If they cannot answer those questions, tell them to use one platform.

### Distributed Tradeoffs
When data is split across systems, the project gets harder.

Tradeoffs students can mention:
- duplication: the same fact may exist in two places
- consistency: one system may update before the other
- failure: one database may be up while the other is down
- restore: backups may restore to different points in time
- security: permissions must be managed in both places
- cost: two platforms create more operational work

Students only need to explain one tradeoff clearly.

## Supabase/Postgres Review

### What Supabase Is
For this class, Supabase is managed Postgres with a useful dashboard around it.

Students should understand:
- Tables are Postgres tables.
- SQL Editor runs SQL against Postgres.
- Table Editor is a visual way to inspect rows.
- Authentication and Row Level Security can protect data.
- Connection strings allow external tools or notebooks to connect.

Do not let students treat Supabase as magic.
It is still a relational database project.

### What A Supabase Project Should Show
Minimum strong evidence:
- 3-5 tables
- primary keys
- at least two relationships if the project needs multiple tables
- realistic seed data
- at least four meaningful SQL queries in the final submission
- one index decision tied to a query
- one access-control or RLS concern
- one backup/restore plan

### Row Level Security
Row Level Security, or RLS, controls which rows a user can access.

Beginner explanation:
- Table permissions decide access broadly.
- RLS policies can make access depend on the current user, row owner, role, or condition.

Students do not need perfect production RLS.
They do need to identify what should be protected.

Good student answer:
`Only staff should update ticket status. Students can create tickets, but they should not edit tickets submitted by other users.`

Weak student answer:
`I will make it secure.`

### Connection Strings And Pooler
Supabase provides connection strings for Postgres access.

Important teaching point:
- Some environments have IPv6 problems.
- If direct connection fails from a notebook or cloud environment, the Supabase pooler connection string may work better.

Students should never submit:
- database passwords
- service role keys
- full connection strings
- screenshots showing secrets

### Backups And Restore
A backup is not useful unless the student can explain restore.

Ask students:
- What mistake are you preparing for?
- What file, backup, export, or SQL script would you use?
- Where would you restore?
- What would you check after restore?

Good restore verification checklist:
- tables exist
- row counts look correct
- important query still works
- index still exists
- permission/RLS concern is still understood

## Index And Performance Evidence

Students do not need advanced tuning.
They need one clear index decision.

A good index explanation includes:
- the query question
- the filtered, joined, or sorted column
- why the index helps reads
- one cost of the index

Example:
`Users often search open tickets by status and created date. I would index status and created_at because that supports filtering by status and sorting recent records. The cost is extra storage and slightly slower writes because the index must be maintained.`

If students say "indexes make it faster," push them to name the exact query.

## Common Student Questions

### Can I Use Only Supabase?
Yes.
One well-explained Supabase/Postgres project can earn full credit.

### Can I Use Only MongoDB?
Yes.
One well-explained MongoDB/Atlas project can earn full credit.

### Should I Use Both?
Only if the split is simple and defensible.
Most students should not add a second platform this late.

### Do I Need A Web App?
No.
The grade is based on database design, queries, seed data, admin evidence, explanation, and presentation.

### Do I Need To Submit A GitHub Repo?
No.
GitHub is optional.
Students must submit code/database artifacts and enough evidence or access for grading.

### What If My Live Cloud Project Fails During Demo?
Screenshots, SQL files, exported data, notebook output, and written admin notes can still prove the work.
Students should prepare evidence before the deadline.

## How To Use The Notebook
Use `week14_sqlite_supabase_postgres_admin_demo.ipynb` if students need a concrete demo.

The notebook uses SQLite because it runs anywhere without credentials.
It demonstrates the same ideas students need for Supabase/Postgres:
- create tables
- insert seed data
- write useful queries
- create an index
- inspect a query plan
- export a backup-style SQL script

When explaining it, say:
`SQLite is not Supabase, but the relational thinking transfers. Supabase is Postgres, so the final SQL may differ slightly, but the database administration ideas are the same.`

## Day 1 Brightspace Submission
Students submit one text response.

Required items:
1. one-database or two-database decision
2. platform-track paragraph for Supabase/Postgres, MongoDB/Atlas, or both
3. review-readiness sentence

Keep them from overbuilding.
The target is clear evidence, not a perfect production system.
