# Week 4: Advanced SQL, Constraints, and Transaction Management

## Learning Objectives
- Implement advanced SQL constructs including user-defined functions, complex views, and trigger-based automation
- Configure and manage table-level constraints to enforce business rules and data integrity
- Explain PostgreSQL transaction processing and the ACID properties that govern reliability
- Diagnose concurrency issues by examining isolation levels, locks, and transactional anomalies
- Launch the midterm project proposal process by translating technical requirements into a scoped plan

## Topics Covered
1. SQL functions (built-in, user-defined, PL/pgSQL essentials)
2. Views and materialized views for abstraction and optimization
3. Constraints: primary/foreign keys, uniqueness, checks, exclusion, deferrable logic
4. Triggers and trigger functions for auditing, validation, and denormalized writes
5. Transactions, ACID properties, and PostgreSQL isolation levels
6. Lock monitoring, error recovery, and best practices for transactional SQL

## Materials
- `Week4_Advanced_SQL_Transactions.pptx` — lecture slides covering functions, views, triggers, constraints, and transactions
- `week4_advanced_sql_lab_student.ipynb` — student lab notebook for in-class and homework work
- `week4_advanced_sql_lab_teacher.ipynb` — instructor annotated notebook with solution notes and talking points
- `instructor_guide.md` — facilitation notes, demos, and assessment guidance

## In-Class Flow
1. **Lecture (50 min)** — walk through slides on functions, views, constraints, triggers, and ACID
2. **Demo (20 min)** — instructor shows creation of a view, trigger function, and constraint violation detection
3. **Lab (60 min)** — students complete notebook exercises against Supabase/PostgreSQL staging database
4. **Midterm Project Workshop (20 min)** — groups outline proposal scope, deliverables, and success criteria

## Activities & Assignments
- **Lab Submission** (due 48h post-class): notebook exports showing successful creation of view, trigger, constraint tests, and transaction rollback scenario
- **Midterm Project Proposal Draft** (due start of Week 5): 1-page summary including problem statement, dataset, planned schema, and risk assessment
- **Discussion Board Prompt**: share one real-world scenario where a constraint or trigger prevented bad data

## Resources
- [PostgreSQL Functions and Operators](https://www.postgresql.org/docs/current/functions.html)
- [CREATE FUNCTION Reference](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [Views and Materialized Views](https://www.postgresql.org/docs/current/tutorial-views.html)
- [Constraint Documentation](https://www.postgresql.org/docs/current/ddl-constraints.html)
- [Trigger Documentation](https://www.postgresql.org/docs/current/plpgsql-trigger.html)
- [Transactions & Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html)

---

*Prepared for CST4714 Database Administration — Week 4 (Advanced SQL & Transactions).* 
