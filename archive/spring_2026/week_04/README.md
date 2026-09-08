# Week 4: Schema Management (PostgreSQL + Supabase)

## Week Focus
This week is about managing database structure safely in a real workflow.

Core themes:
- Views and materialized views
- Sequences and identity columns
- Constraints as integrity contracts
- Schema introspection and drift detection

## Learning Outcomes
By the end of Week 4, students should be able to:
1. Explain when to use views vs materialized views.
2. Choose and defend a key-generation strategy (`IDENTITY`/sequence-based).
3. Implement primary, foreign key, unique, and check constraints intentionally.
4. Use metadata queries to verify what the database is actually enforcing.
5. Apply migration-first discipline for structural changes.

## In-Class Flow (75+ minutes)
1. Week 3 recap and schema management model.
2. Views essentials (standard + materialized).
3. Sequence and identity essentials (core only).
4. Constraint fundamentals and common mistakes.
5. Introspection workflows (`information_schema`, `pg_catalog`).
6. Lab launch + reading response.

## Why This Week Matters
Most production data incidents are structural:
- missing/weak constraints,
- unmanaged schema drift,
- hidden coupling to table shape,
- poor key-generation assumptions.

This week builds the habits that prevent those failures.

## Week 4 Work
- Complete the lab: `lab_activity.md`
- Complete the in-class reading response: `in_class_reading_response.md`
- Use the lecture deck during instruction: `Week_04_Schema_Management_Postgres_Supabase.pptx`

### Lab scope note
- This lab uses **existing Supabase tables** and does **not** require building a brand-new schema from scratch.
- Deliverables are intentionally lightweight: brief write-up, SQL used, and screenshots.

## Required Reading (Primary Docs)
- PostgreSQL `CREATE VIEW`: [https://www.postgresql.org/docs/current/sql-createview.html](https://www.postgresql.org/docs/current/sql-createview.html)
- PostgreSQL `CREATE MATERIALIZED VIEW`: [https://www.postgresql.org/docs/current/sql-creatematerializedview.html](https://www.postgresql.org/docs/current/sql-creatematerializedview.html)
- PostgreSQL identity columns: [https://www.postgresql.org/docs/current/ddl-identity-columns.html](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
- PostgreSQL constraints: [https://www.postgresql.org/docs/current/ddl-constraints.html](https://www.postgresql.org/docs/current/ddl-constraints.html)
- PostgreSQL information schema: [https://www.postgresql.org/docs/current/information-schema.html](https://www.postgresql.org/docs/current/information-schema.html)
- Supabase migrations guide: [https://supabase.com/docs/guides/deployment/database-migrations](https://supabase.com/docs/guides/deployment/database-migrations)

## Connection to Week 5
Week 5 moves into transactions, isolation, and locking behavior.
Students who complete Week 4 well will be prepared to reason about concurrency on top of a clean, constrained schema.
