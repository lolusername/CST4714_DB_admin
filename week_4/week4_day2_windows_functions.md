# Week 4 Day 2 — Quick Guide to Window Functions & Custom Functions

These examples use the tables created by `week4_day2_lab.sql`. Run that script first (Supabase SQL editor or `psql`) so the `week4_day2` schema exists.

## 1. Set Your Session Search Path (Optional)
```sql
SET search_path TO week4_day2, public;
```
Now you can refer to tables without the schema prefix.

---

## 2. Start Simple: Aggregates per Student & Term
```sql
SELECT s.full_name,
       o.term,
       SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
       SUM(e.credits_earned) AS term_credits
FROM enrollments e
JOIN course_offerings o ON o.offering_id = e.offering_id
JOIN students s         ON s.student_id = e.student_id
WHERE e.status = 'completed'
GROUP BY s.full_name, o.term
ORDER BY o.term, term_gpa DESC;
```
**Why this matters:** regular aggregates collapse each term into a single row per student. We’ll reuse this query as the base for windows.

---

## 3. Window Pass #1 — Add a Rank Inside Each Term
```sql
WITH per_term AS (
    SELECT s.full_name,
           o.term,
           SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
           SUM(e.credits_earned) AS term_credits
    FROM enrollments e
    JOIN course_offerings o ON o.offering_id = e.offering_id
    JOIN students s         ON s.student_id = e.student_id
    WHERE e.status = 'completed'
    GROUP BY s.full_name, o.term
)
SELECT full_name,
       term,
       term_gpa,
       ROW_NUMBER() OVER (PARTITION BY term ORDER BY term_gpa DESC) AS term_rank
FROM per_term
ORDER BY term, term_rank;
```
**Key idea:** `PARTITION BY term` restarts `ROW_NUMBER()` for each term.

---

## 4. Window Pass #2 — Running Credits per Student
```sql
WITH per_term AS (
    SELECT s.student_id,
           s.full_name,
           o.term,
           SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
           SUM(e.credits_earned) AS term_credits
    FROM enrollments e
    JOIN course_offerings o ON o.offering_id = e.offering_id
    JOIN students s         ON s.student_id = e.student_id
    WHERE e.status = 'completed'
    GROUP BY s.student_id, s.full_name, o.term
)
SELECT full_name,
       term,
       term_gpa,
       ROW_NUMBER() OVER (PARTITION BY term ORDER BY term_gpa DESC) AS term_rank,
       SUM(term_credits) OVER (PARTITION BY student_id ORDER BY term
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS credits_so_far
FROM per_term
ORDER BY term, term_rank;
```
**Plain English:** “For each student, add the credits from earlier terms up to the current one.”

---

## 5. Save the Window Query as a View
```sql
CREATE OR REPLACE VIEW week4_day2.vw_student_term_progress AS
WITH per_term AS (
    SELECT s.student_id,
           s.full_name,
           o.term,
           SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
           SUM(e.credits_earned) AS term_credits
    FROM week4_day2.enrollments e
    JOIN week4_day2.course_offerings o ON o.offering_id = e.offering_id
    JOIN week4_day2.students s         ON s.student_id = e.student_id
    WHERE e.status = 'completed'
    GROUP BY s.student_id, s.full_name, o.term
)
SELECT per_term.student_id,
       per_term.full_name,
       per_term.term,
       per_term.term_gpa,
       ROW_NUMBER() OVER (PARTITION BY per_term.term ORDER BY per_term.term_gpa DESC) AS term_rank,
       SUM(per_term.term_credits) OVER (PARTITION BY per_term.student_id ORDER BY per_term.term
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS credits_so_far
FROM per_term;
```
Use the view:
```sql
SELECT *
FROM week4_day2.vw_student_term_progress
WHERE term = '2024-Spring'
ORDER BY term_rank;
```

---

## 6. Build a Simple SQL Function: Flag At-Risk Students
```sql
CREATE OR REPLACE FUNCTION week4_day2.fn_flag_at_risk(
    p_term text,
    p_min_gpa numeric,
    p_min_credits int)
RETURNS TABLE (
    student_id uuid,
    full_name text,
    term text,
    term_gpa numeric,
    credits_so_far int)
LANGUAGE sql AS $$
    SELECT v.student_id,
           v.full_name,
           v.term,
           v.term_gpa,
           v.credits_so_far
    FROM week4_day2.vw_student_term_progress v
    WHERE v.term = p_term
      AND (v.term_gpa < p_min_gpa OR v.credits_so_far < p_min_credits)
    ORDER BY v.term_gpa;
$$;
```
Try it:
```sql
SELECT *
FROM week4_day2.fn_flag_at_risk('2024-Spring', 2.50, 9);
```
**Why this rocks:** the heavy window logic lives in the view, so the function stays compact and re-usable.

---

## 7. Bonus: PL/pgSQL Function Template (if you want parameters + logic)
```sql
CREATE OR REPLACE FUNCTION week4_day2.fn_student_term_summary(p_student uuid)
RETURNS TABLE (
    term text,
    term_gpa numeric,
    term_rank int,
    credits_so_far int)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT term,
           term_gpa,
           term_rank,
           credits_so_far
    FROM week4_day2.vw_student_term_progress
    WHERE student_id = p_student
    ORDER BY term;
END;
$$;
```
Call it with a known student ID:
```sql
SELECT *
FROM week4_day2.fn_student_term_summary('11111111-1111-1111-1111-111111111111');
```

---

## Quick Checklist
- [ ] Run the initialization script.
- [ ] Practice the three window passes until you can explain them in plain English.
- [ ] Reference the view and function templates when building your own analytics.
- [ ] Keep screenshots or query results for lab submissions and midterm planning.

Happy querying!
