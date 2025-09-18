-- Week 4 Day 2 lab dataset
-- Drops and recreates the week4_day2 schema with sample data for indexing, analytics, and automation exercises.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE students (
    student_id      uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name       text NOT NULL,
    major           text NOT NULL,
    entry_term      text NOT NULL,
    credits_goal    integer NOT NULL CHECK (credits_goal BETWEEN 60 AND 180)
);

CREATE TABLE faculty (
    faculty_id      serial PRIMARY KEY,
    full_name       text NOT NULL,
    department      text NOT NULL
);

CREATE TABLE courses (
    course_id               serial PRIMARY KEY,
    course_code             text UNIQUE NOT NULL,
    course_name             text NOT NULL,
    department              text NOT NULL,
    credits                 integer NOT NULL CHECK (credits BETWEEN 1 AND 6),
    default_grading_scale   text NOT NULL
);

CREATE TABLE course_offerings (
    offering_id     serial PRIMARY KEY,
    course_id       integer NOT NULL REFERENCES courses(course_id),
    term            text NOT NULL,
    instructor_id   integer NOT NULL REFERENCES faculty(faculty_id),
    starts_on       date NOT NULL,
    ends_on         date NOT NULL,
    capacity        integer NOT NULL CHECK (capacity BETWEEN 10 AND 120)
);

CREATE TABLE enrollments (
    enrollment_id       bigserial PRIMARY KEY,
    student_id          uuid NOT NULL REFERENCES students(student_id),
    offering_id         integer NOT NULL REFERENCES course_offerings(offering_id),
    enrolled_on         date NOT NULL,
    status              text NOT NULL CHECK (status IN ('enrolled','completed','dropped')),
    final_grade         text,
    grade_points        numeric(4,2),
    credits_attempted   integer NOT NULL CHECK (credits_attempted BETWEEN 1 AND 6),
    credits_earned      integer NOT NULL DEFAULT 0,
    CONSTRAINT enforce_completed_grade
      CHECK (
        (status <> 'completed' AND final_grade IS NULL AND grade_points IS NULL)
        OR (status = 'completed' AND final_grade IS NOT NULL AND grade_points BETWEEN 0 AND 4.33)
      )
);

CREATE TABLE term_credit_summary (
    student_id      uuid NOT NULL,
    term            text NOT NULL,
    credits_attempted integer NOT NULL DEFAULT 0,
    credits_earned    integer NOT NULL DEFAULT 0,
    quality_points    numeric(10,2) NOT NULL DEFAULT 0,
    gpa               numeric(4,2),
    last_recalc       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (student_id, term)
);

CREATE TABLE enrollment_audit (
    audit_id        bigserial PRIMARY KEY,
    enrollment_id   bigint NOT NULL,
    student_id      uuid NOT NULL,
    term            text NOT NULL,
    before_status   text,
    after_status    text,
    before_grade    text,
    after_grade     text,
    changed_at      timestamptz NOT NULL DEFAULT now()
);

-- Faculty roster
INSERT INTO faculty (full_name, department) VALUES
    ('Ariana Brooks', 'Computer Science'),
    ('Elliot Chen', 'Computer Science'),
    ('Maya Fernandez', 'Information Systems'),
    ('Leo Grant', 'Business'),
    ('Priya Iyer', 'Data Science'),
    ('Samir Khan', 'Mathematics'),
    ('Emily Novak', 'Information Systems'),
    ('Thomas O''Neal', 'Business');

-- Course catalog
INSERT INTO courses (course_code, course_name, department, credits, default_grading_scale) VALUES
    ('CS101',  'Intro to Programming',          'Computer Science',     3, 'letter'),
    ('CS205',  'Data Structures',               'Computer Science',     4, 'letter'),
    ('CS375',  'Web Application Development',   'Computer Science',     3, 'letter'),
    ('DS210',  'Applied Statistics',            'Data Science',         3, 'letter'),
    ('DS340',  'Data Warehousing',              'Data Science',         3, 'letter'),
    ('DS360',  'Machine Learning Fundamentals', 'Data Science',         3, 'letter'),
    ('IS220',  'Systems Analysis',              'Information Systems',  3, 'letter'),
    ('IS330',  'Database Administration',       'Information Systems',  3, 'letter'),
    ('BUS101', 'Foundations of Business',       'Business',             3, 'letter'),
    ('BUS305', 'Project Management',            'Business',             3, 'letter'),
    ('MTH150', 'Discrete Mathematics',          'Mathematics',          3, 'letter'),
    ('MTH255', 'Applied Linear Algebra',        'Mathematics',          4, 'letter');

-- Student roster
WITH lists AS (
    SELECT
        ARRAY['Andrea','Brian','Chloe','Darius','Elena','Farah','Gabe','Hector','Isha','Jon','Kira','Luis','Marta','Nikhil','Ophelia'] AS first_names,
        ARRAY['Flores','Kim','Patel','Johnson','Lopez','Nguyen','Olsen','Perez','Quinn','Singh','Turner','Valdez','Wong','Xu','Young'] AS last_names,
        ARRAY['Computer Science','Information Systems','Business','Data Science','Mathematics'] AS majors,
        ARRAY['2022-Fall','2023-Spring','2023-Fall','2024-Spring'] AS entry_terms
)
INSERT INTO students (student_id, full_name, major, entry_term, credits_goal)
SELECT
    gen_random_uuid(),
    CONCAT(
        lists.first_names[( (gs.i - 1) % array_length(lists.first_names, 1) ) + 1],
        ' ',
        lists.last_names[( (gs.i - 1) % array_length(lists.last_names, 1) ) + 1],
        ' ',
        gs.i
    ) AS full_name,
    lists.majors[( (gs.i - 1) % array_length(lists.majors, 1) ) + 1] AS major,
    lists.entry_terms[( (gs.i - 1) % array_length(lists.entry_terms, 1) ) + 1] AS entry_term,
    120 AS credits_goal
FROM generate_series(1, 60) AS gs(i)
CROSS JOIN lists;

-- Course offerings across multiple terms
WITH term_calendar(term, starts_on, ends_on, idx) AS (
    VALUES
        ('2023-Fall',  DATE '2023-08-28', DATE '2023-12-15', 0),
        ('2024-Spring',DATE '2024-01-16', DATE '2024-05-10', 1),
        ('2024-Summer',DATE '2024-05-20', DATE '2024-08-02', 2),
        ('2024-Fall',  DATE '2024-08-26', DATE '2024-12-13', 3)
), faculty_count AS (
    SELECT COUNT(*)::integer AS total_faculty FROM faculty
)
INSERT INTO course_offerings (course_id, term, instructor_id, starts_on, ends_on, capacity)
SELECT
    c.course_id,
    t.term,
    ((c.course_id + t.idx) % faculty_count.total_faculty) + 1 AS instructor_id,
    t.starts_on,
    t.ends_on,
    24 + ((c.course_id + t.idx) % 8) * 4 AS capacity
FROM courses c
CROSS JOIN term_calendar t
CROSS JOIN faculty_count
ORDER BY c.course_id, t.idx;

-- Enrollment data
WITH schedule AS (
    SELECT
        s.student_id,
        o.offering_id,
        o.term,
        o.starts_on,
        ROW_NUMBER() OVER (PARTITION BY s.student_id, o.term ORDER BY o.offering_id) AS per_term_seq,
        ROW_NUMBER() OVER (PARTITION BY s.student_id ORDER BY o.term, o.offering_id) AS seq
    FROM students s
    JOIN course_offerings o ON TRUE
), grade_scale AS (
    SELECT * FROM (VALUES
        (0, 'A', 4.00),
        (1, 'A-', 3.70),
        (2, 'B+', 3.30),
        (3, 'B', 3.00),
        (4, 'B-', 2.70),
        (5, 'C+', 2.30),
        (6, 'C', 2.00),
        (7, 'C-', 1.70),
        (8, 'D+', 1.30)
    ) AS g(idx, letter, points)
), enrollment_rows AS (
    SELECT
        schedule.student_id,
        schedule.offering_id,
        (schedule.starts_on - ((schedule.seq % 10) + 5) * INTERVAL '1 day')::date AS enrolled_on,
        status_codes.status_code,
        grade_scale.letter,
        grade_scale.points,
        c.credits
    FROM schedule
    JOIN course_offerings o ON o.offering_id = schedule.offering_id
    JOIN courses c ON c.course_id = o.course_id
    JOIN grade_scale ON grade_scale.idx = (schedule.seq + c.course_id) % 9
    CROSS JOIN LATERAL (
        SELECT CASE
            WHEN (schedule.seq % 11) = 0 THEN 'dropped'
            WHEN (schedule.seq % 7) = 0 THEN 'enrolled'
            ELSE 'completed'
        END AS status_code
    ) AS status_codes
    WHERE schedule.per_term_seq <= 4
)
INSERT INTO enrollments (student_id, offering_id, enrolled_on, status, final_grade, grade_points, credits_attempted, credits_earned)
SELECT
    student_id,
    offering_id,
    enrolled_on,
    status_code,
    CASE WHEN status_code = 'completed' THEN letter ELSE NULL END AS final_grade,
    CASE WHEN status_code = 'completed' THEN points ELSE NULL END AS grade_points,
    credits AS credits_attempted,
    CASE WHEN status_code = 'completed' THEN credits ELSE 0 END AS credits_earned
FROM enrollment_rows;

ANALYZE students;
ANALYZE courses;
ANALYZE course_offerings;
ANALYZE enrollments;

COMMIT;
