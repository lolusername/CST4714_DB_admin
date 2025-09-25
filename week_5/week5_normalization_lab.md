# Week 5 Lab — Normalizing the Wellness Subscription Tracker

This lab walks you through reshaping the wellness center spreadsheet into a tidy relational design that lives in the default `public` schema. You will read the raw data, identify functional dependencies, and build a handful of tables that satisfy 3NF.

---

## Learning Goals Recap
- Apply 1NF, 2NF, and 3NF to eliminate redundancy and update anomalies.
- Translate functional dependencies into clear primary and foreign keys.
- Enforce business rules with declarative constraints instead of application code.
- Communicate design choices, including any intentional denormalization.

---

## Pre-Lab Review
Spend a few minutes refreshing these concepts:

- **Entities & Relationships**: Which nouns, verbs, and attributes appear in the business story?
- **Key Strategies**: Natural vs surrogate keys, composite keys, and alternate keys.
- **Functional Dependencies**: Think in terms of “determinant → dependent.”
- **Normalization Ladder**: 1NF (atomic fields), 2NF (no partial dependency), 3NF (no transitive dependency).
- **Documenting Assumptions**: Capture every business rule you enforce (or intentionally ignore).

---

## Environment Setup
Run the script below in Supabase (or any PostgreSQL 14+) to recreate the messy source table inside the `public` schema.

```sql
DROP TABLE IF EXISTS wellness_subscription_raw;

CREATE TABLE wellness_subscription_raw (
    subscription_id        integer,
    student_full_name      text,
    student_email          text,
    major                  text,
    cohort_term            text,
    advisor_name           text,
    advisor_email          text,
    plan_name              text,
    plan_category          text,
    monthly_fee            numeric(6,2),
    session_type           text,
    session_instructor     text,
    instructor_cert_level  text,
    session_room           text,
    session_day_of_week    text,
    session_time           time,
    attendance_date        date,
    attendance_status      text,
    payment_method         text,
    payment_transaction_id text,
    payment_amount         numeric(7,2)
);

INSERT INTO wellness_subscription_raw VALUES
    (4001, 'Andrea Flores', 'andrea.flores@example.edu', 'Computer Science', '2023-Fall', 'Dr. Patel', 'patel@college.edu', 'Mindfulness Plus', 'Mental Health', 45.00, 'Yoga', 'Selena Rivera', 'RYT-500', 'Studio A', 'Monday', '08:00', '2024-03-04', 'attended', 'credit_card', 'TXN-90011', 45.00),
    (4001, 'Andrea Flores', 'andrea.flores@example.edu', 'Computer Science', '2023-Fall', 'Dr. Patel', 'patel@college.edu', 'Mindfulness Plus', 'Mental Health', 45.00, 'Yoga', 'Selena Rivera', 'RYT-500', 'Studio A', 'Monday', '08:00', '2024-03-11', 'missed', 'credit_card', 'TXN-90011', 45.00),
    (4001, 'Andrea Flores', 'andrea.flores@example.edu', 'Computer Science', '2023-Fall', 'Dr. Patel', 'patel@college.edu', 'Mindfulness Plus', 'Mental Health', 45.00, 'Nutrition Workshop', 'Hank Morales', 'RD', 'Wellness Kitchen', 'Wednesday', '18:00', '2024-03-13', 'attended', 'credit_card', 'TXN-90011', 45.00),
    (4002, 'Brian Kim', 'brian.kim@example.edu', 'Information Systems', '2022-Fall', 'Prof. Chen', 'echen@college.edu', 'Recovery & Strength', 'Physical Therapy', 65.00, 'Physical Therapy', 'Alex Rao', 'DPT', 'Clinic Room 2', 'Tuesday', '09:30', '2024-03-05', 'attended', 'campus_card', 'TXN-90102', 32.50),
    (4002, 'Brian Kim', 'brian.kim@example.edu', 'Information Systems', '2022-Fall', 'Prof. Chen', 'echen@college.edu', 'Recovery & Strength', 'Physical Therapy', 65.00, 'Physical Therapy', 'Alex Rao', 'DPT', 'Clinic Room 2', 'Thursday', '09:30', '2024-03-07', 'attended', 'campus_card', 'TXN-90102', 32.50),
    (4002, 'Brian Kim', 'brian.kim@example.edu', 'Information Systems', '2022-Fall', 'Prof. Chen', 'echen@college.edu', 'Recovery & Strength', 'Physical Therapy', 65.00, 'Mobility Clinic', 'Alex Rao', 'DPT', 'Clinic Room 3', 'Friday', '11:00', '2024-03-08', 'attended', 'campus_card', 'TXN-90102', 32.50),
    (4003, 'Chloe Patel', 'chloe.patel@example.edu', 'Data Science', '2023-Spring', 'Prof. Chen', 'echen@college.edu', 'Mindfulness Plus', 'Mental Health', 45.00, 'Yoga', 'Selena Rivera', 'RYT-500', 'Studio A', 'Monday', '08:00', '2024-03-04', 'attended', 'credit_card', 'TXN-90444', 45.00),
    (4003, 'Chloe Patel', 'chloe.patel@example.edu', 'Data Science', '2023-Spring', 'Prof. Chen', 'echen@college.edu', 'Mindfulness Plus', 'Mental Health', 45.00, 'Meditation Circle', 'Selena Rivera', 'RYT-500', 'Studio B', 'Thursday', '17:30', '2024-03-07', 'attended', 'credit_card', 'TXN-90444', 45.00),
    (4004, 'Darius Johnson', 'darius.johnson@example.edu', 'Business', '2024-Spring', 'Dr. Patel', 'patel@college.edu', 'Performance Boost', 'Physical Therapy', 55.00, 'Strength Training', 'Hank Morales', 'CSCS', 'Studio C', 'Tuesday', '07:30', '2024-03-05', 'attended', 'campus_card', 'TXN-90521', 55.00);
```

---

## Lab Workflow

### Step 1 — Inspect the raw sheet (15 min)
- List obvious issues: duplicate venue capacities, repeated plan details, subscriptions spanning multiple show dates.
- Sketch the functional dependencies you observe (e.g., `plan_name → plan_category, monthly_fee`).

### Step 2 — Draft your target tables (15 min)
- Recommend starting entities: `students`, `advisors`, `wellness_plans`, `sessions`, `subscriptions`, `attendance_events`.
- Decide on primary keys (hint: emails make good natural keys; subscription IDs already exist).
- Outline the foreign keys that will connect the tables.

### Step 3 — Build and load the normalized schema (25 min)
- Create your tables in the `public` schema with explicit constraints.
- Use `INSERT ... SELECT DISTINCT ... FROM wellness_subscription_raw` to populate dimensions.
- Insert attendance rows by joining back to your dimension tables to pick up surrogate IDs if needed.

### Step 4 — Validate & Reflect (15 min)
- Run one or two “proof” queries (e.g., attendance by plan, revenue per subscription) and confirm the results look sane.
- Note any denormalization decisions or TODOs for your midterm project.

Deliverables: a SQL script containing your DDL + inserts + proof queries, plus a short reflection (1–2 paragraphs) describing key dependencies solved and remaining assumptions.

---

## Submission Checklist
- ✅ Normalized schema DDL (`CREATE TABLE ...`).
- ✅ Insert statements derived from `wellness_subscription_raw`.
- ✅ At least one validation query with output notes.
- ✅ Written reflection covering design decisions and any intentional denormalization.

Combine everything into a single SQL file plus a brief Markdown/PDF note for the reflection.

---

## Extension Ideas (Optional)
- Add a `payments` table if you need to reconcile transaction IDs separately.
- Build a view that reconstructs the original spreadsheet columns from your normalized tables.
- Experiment with materialized views for summary reporting once you are confident in the design.

---

*Need a reset? Rerun the setup script to recreate `wellness_subscription_raw` and iterate again.*
