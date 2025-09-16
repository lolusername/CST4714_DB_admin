-- Week 4 demo schema: simple college admissions database
-- Run in Supabase SQL editor or any PostgreSQL 14+ environment.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Base tables
CREATE TABLE college (
    cname        text PRIMARY KEY,
    state        char(2) NOT NULL,
    enrollment   integer CHECK (enrollment >= 0)
);

CREATE TABLE student (
    sid          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    sname        text NOT NULL,
    gpa          numeric(3,2) CHECK (gpa BETWEEN 0 AND 4.00),
    sizehs       integer CHECK (sizehs > 0)
);

CREATE TABLE apply (
    sid          uuid NOT NULL REFERENCES student(sid) ON DELETE CASCADE,
    cname        text NOT NULL REFERENCES college(cname) ON DELETE CASCADE,
    major        text NOT NULL,
    decision     text NOT NULL CHECK (decision IN ('accepted','waitlisted','rejected','pending')),
    applied_at   date NOT NULL DEFAULT current_date,
    PRIMARY KEY (sid, cname, major)
);

-- Seed data
INSERT INTO college (cname, state, enrollment) VALUES
    ('Metro Tech University', 'NY', 24000),
    ('Coastal Liberal Arts', 'MA', 3200),
    ('Frontier State College', 'CO', 8900),
    ('Southridge Institute', 'TX', 15300);

INSERT INTO student (sid, sname, gpa, sizehs) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Andrea Flores', 3.85, 1800),
    ('22222222-2222-2222-2222-222222222222', 'Brian Kim',    3.20, 900),
    ('33333333-3333-3333-3333-333333333333', 'Chloe Patel',  3.65, 2100),
    ('44444444-4444-4444-4444-444444444444', 'Darius Johnson', 2.95, 1200);

INSERT INTO apply (sid, cname, major, decision, applied_at) VALUES
    ('11111111-1111-1111-1111-111111111111', 'Metro Tech University', 'Computer Science', 'accepted', '2024-01-15'),
    ('11111111-1111-1111-1111-111111111111', 'Coastal Liberal Arts', 'Data Science', 'waitlisted', '2024-01-22'),
    ('22222222-2222-2222-2222-222222222222', 'Frontier State College', 'Environmental Engineering', 'pending', '2024-01-19'),
    ('33333333-3333-3333-3333-333333333333', 'Metro Tech University', 'Design', 'rejected', '2024-01-25'),
    ('33333333-3333-3333-3333-333333333333', 'Southridge Institute', 'Information Systems', 'accepted', '2024-01-28'),
    ('44444444-4444-4444-4444-444444444444', 'Coastal Liberal Arts', 'Economics', 'accepted', '2024-02-02');

-- Optional view for quick reporting
CREATE OR REPLACE VIEW vw_applications_overview AS
SELECT
    a.sid, s.sname,
    a.cname, c.state,
    a.major, a.decision, a.applied_at,
    s.gpa, s.sizehs, c.enrollment
FROM apply a
JOIN student s ON s.sid = a.sid
JOIN college c ON c.cname = a.cname;

COMMIT;
