# Slide Outline — Week 7 Midterm Project Review

## Slide 1 — Title
- CST4714 Midterm Project Review
- Tracks, Rubric, FAQs, and Success Tips

## Slide 2 — Why the Midterm Matters
- 35% of final grade; demonstrates DBA mindset
- Choose a track that matches your goals and strengths
- Same rubric for every option

## Slide 3 — Agenda
- Project options overview
- Deliverables & timeline
- Rubric breakdown
- FAQs & common pitfalls
- Sample SQL & admin workflows
- Study plan and next steps

## Slide 4 — Option 1: Structured Database Build
- Guided path with provided datasets
- Requirements: 3+ related tables, PK/FK, 1 constraint
- Load ≥20 rows/table; 5 SQL queries (joins, aggregates, subqueries)
- Admin task: roles/permissions or backup
- Submit SQL scripts, ERD, 2–3 page report

## Slide 5 — Option 1: Starter Checklist
- Validate schema sketch against normalization checklist
- Script DDL + sample data for reproducibility
- Annotate queries with comments for reviewers

## Slide 6 — Option 2: White Paper / DBA Report
- Best for research/storytelling focus
- 3–5 page technical paper framing a real-world problem
- Include ERD, technology comparison, DBA concerns (security, RLS, backups, scaling)
- Cite references when appropriate

## Slide 7 — Option 2: Writing Roadmap
- Outline problem, stakeholders, success metrics
- Provide schema diagram + narrative justification
- Contrast at least two deployment options (e.g., Supabase vs. self-hosted)

## Slide 8 — Option 3: Coding-Heavy DBA/DevOps
- Deep dive into advanced SQL + admin tooling
- 4+ tables, meaningful constraints
- 10+ queries (window, CTE, recursive)
- 2 triggers + 1 view/materialized view
- Roles, RLS policies, backup/restore demo, GitHub repo

## Slide 9 — Option 3: Implementation Tips
- Leverage migrations/scripts for repeatable setup
- Capture `EXPLAIN ANALYZE` results to show tuning
- Document RLS policy tests and restore steps

## Slide 10 — One Rubric, Four Pillars
- Schema & Design — 20 pts
- SQL & Analysis — 25 pts
- Admin & DevOps — 25 pts
- Documentation — 20 pts
- Professionalism — 10 pts

## Slide 11 — Timeline & Logistics
- Track declaration due Week 5 (default Option 1 if silent)
- Midterm review labs during Week 7
- Final submission due Week 8 (see syllabus)
- Upload to Blackboard; Option 3 include GitHub link

## Slide 12 — FAQ Highlights
- Can I propose my own dataset? → Yes, get approval early.
- What if my ERD changes mid-project? → Document revisions and rationale.
- Do I need Supabase? → Any PostgreSQL environment is fine; show admin competency.
- How do I handle partner work? → Projects are individual; peer feedback allowed.

## Slide 13 — Common Pitfalls
- Missing constraint or undocumented assumption
- Queries without sample output or comments
- Backup/restore not demonstrated or validated
- White paper lacking actionable DBA recommendations

## Slide 14 — Sample SQL: Option 1 Baseline
```sql
CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES member(member_id),
    facility_id INT REFERENCES facility(facility_id),
    start_time TIMESTAMPTZ NOT NULL,
    slots SMALLINT CHECK (slots > 0)
);

COMMENT ON TABLE booking IS 'Tracks facility usage for utilization analysis.';
```

## Slide 15 — Sample SQL: Option 3 Advanced Query
```sql
WITH ranked_sessions AS (
    SELECT
        member_id,
        start_time::date AS usage_day,
        COUNT(*) OVER (PARTITION BY member_id) AS total_sessions,
        ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY start_time DESC) AS recent_rank
    FROM booking
)
SELECT *
FROM ranked_sessions
WHERE recent_rank <= 5;
```

## Slide 16 — Admin Workflow Snapshot
- Backup: `pg_dump -Fc --dbname $DB_URL --file midterm_backup.dump`
- Restore: `pg_restore --clean --dbname $DB_URL midterm_backup.dump`
- Roles: create read-only/reporting roles; document grants
- RLS testing: log policies and expected outcomes

## Slide 17 — Advice from Past Cohorts
- Start with ERD + constraints; iterate before loading data
- Keep a changelog with commands run and issues found
- Use version control even for Option 1 or 2; submit sanitized repo snapshots
- Schedule a check-in during Week 7 office hours

## Slide 18 — Personal Action Plan
- Confirm track and dataset/topic
- Identify the rubric pillar that needs the most practice
- Block two work sessions before midterm deadline
- List open questions for instructor or TA

## Slide 19 — Resources & Support
- Week 3–5 slide decks and labs
- Supabase docs & PostgreSQL official guides
- Peer study pod sign-up, office hours, LMS discussion board

## Slide 20 — Q&A / Exit Ticket
- What’s still unclear?
- Share one concrete next step in the chat or on paper

---

*Prepared for CST4714 Database Administration — last revised 2025-02-14.* 
