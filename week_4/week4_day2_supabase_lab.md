# Week 4 Day 2 Supabase Lab — Indexed Analytics & Window Functions

> **Goal**: Benchmark a real query, speed it up with an index, then use window functions and views to deliver advisor-ready analytics—all inside Supabase.

## 0. Reset the Lab Schema (Instructor or Student-Owned Project)
1. In the Supabase SQL editor, paste and run `week4_day2_lab.sql`. This drops and recreates the `week4_day2` schema with fresh data.
2. Confirm the tables exist:
   ```sql
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'week4_day2'
   ORDER BY table_name;
   ```
3. (Optional) `SET search_path TO week4_day2, public;` for the session so you can omit schema prefixes while experimenting.

## 1. Indexing Warm-Up
1. Capture the baseline plan:
   ```sql
   EXPLAIN (ANALYZE, BUFFERS)
   SELECT *
   FROM week4_day2.enrollments
   WHERE offering_id = 18 AND status = 'completed';
   ```
   - Screenshot the plan. Look for `Seq Scan` and high buffer counts.
2. Build the covering index and refresh stats:
   ```sql
   CREATE INDEX CONCURRENTLY IF NOT EXISTS week4_day2_enrollments_offering_status_idx
       ON week4_day2.enrollments (offering_id, status);
   ANALYZE week4_day2.enrollments;
   ```
3. Rerun the `EXPLAIN` and screenshot the faster plan. Mention `Index Scan` / `Bitmap Heap Scan` in your notes.
4. Optional: prove Supabase used the index:
   ```sql
   SELECT relname, idx_scan
   FROM pg_stat_user_indexes
   WHERE schemaname = 'week4_day2'
     AND relname = 'week4_day2_enrollments_offering_status_idx';
   ```

## 2. Window Functions in Three Passes
### Pass 1 — Term Scoreboard
```sql
SELECT s.full_name,
       o.term,
       SUM(e.grade_points * e.credits_attempted) / NULLIF(SUM(e.credits_attempted), 0) AS term_gpa,
       SUM(e.credits_earned) AS term_credits
FROM week4_day2.enrollments e
JOIN week4_day2.course_offerings o ON o.offering_id = e.offering_id
JOIN week4_day2.students s        ON s.student_id = e.student_id
WHERE e.status = 'completed'
GROUP BY s.full_name, o.term
ORDER BY o.term, term_gpa DESC;
```
- Result = per-term scoreboard per student.

### Pass 2 — Add a Rank per Term
```sql
WITH per_term AS (
    -- use the query from Pass 1
)
SELECT *,
       ROW_NUMBER() OVER (PARTITION BY term ORDER BY term_gpa DESC) AS term_rank
FROM per_term
ORDER BY term, term_rank;
```
- `PARTITION BY term` restarts row numbers each term.

### Pass 3 — Add Running Credits
```sql
WITH per_term AS (
    -- same Pass 1 query
)
SELECT full_name,
       term,
       term_gpa,
       term_rank,
       SUM(term_credits)
           OVER (PARTITION BY full_name ORDER BY term
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS credits_so_far
FROM per_term
ORDER BY term, term_rank;
```
- Translation: “For each student, add up term credits in chronological order.”
- Save the result as evidence (download CSV or screenshot).

## 3. Persist the Analytics as a View
1. Turn Pass 3 into a view:
   ```sql
   CREATE OR REPLACE VIEW week4_day2.vw_student_term_progress AS
   <pass 3 query>;
   ```
2. Test it:
   ```sql
   SELECT *
   FROM week4_day2.vw_student_term_progress
   WHERE term = '2024-Spring'
   ORDER BY term_rank;
   ```
3. Optional: grant read access to a reporting role if you use Supabase RBAC features.

## 4. (Optional Stretch) Advisor Helper Function
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
           t.credits_earned AS credits_so_far
    FROM week4_day2.vw_student_term_progress v
    JOIN week4_day2.term_credit_summary t
      ON t.student_id = v.student_id AND t.term = v.term
    WHERE v.term = p_term
      AND (v.term_gpa < p_min_gpa OR t.credits_earned < p_min_credits)
    ORDER BY v.term_gpa;
$$;
```
- Test it: `SELECT * FROM week4_day2.fn_flag_at_risk('2024-Spring', 2.5, 9);`
- Capture output and explain what each column tells an advisor.

## Deliverables (Submit via LMS or shared doc)
1. Before/after `EXPLAIN` screenshots proving the index effect.
2. Output of the Pass 3 window query or the view (`vw_student_term_progress`).
3. (Optional) Output from `fn_flag_at_risk` with a short note on how advisers might use it.
4. Short reflection: “One insight or benefit from using window functions today.”

## Troubleshooting Tips
- **Tables missing?** Run the initialization script again and ensure `week4_day2` schema exists.
- **Index not used?** Check you ran `ANALYZE`, and confirm the query predicate matches the index column order.
- **Window query errors?** Build the passes exactly as shown—each Pass uses the previous query inside a CTE.
- **Slow SQL editor?** Use the Supabase “Run Selected Query” option and keep result row limits manageable.

Happy labbing!
