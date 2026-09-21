-- Deterministic, disposable Week 7 fixture.
-- Run only in a personal or instructor-approved practice database.

DROP SCHEMA IF EXISTS performance_lab CASCADE;
CREATE SCHEMA performance_lab;

CREATE TABLE performance_lab.tickets (
    ticket_id bigint PRIMARY KEY,
    assignee_id integer,
    category text NOT NULL,
    priority text NOT NULL,
    status text NOT NULL,
    subject text NOT NULL,
    opened_at timestamptz NOT NULL
);

INSERT INTO performance_lab.tickets
SELECT
    n AS ticket_id,
    CASE WHEN n % 13 = 0 THEN NULL ELSE 200 + (n % 25) END AS assignee_id,
    (ARRAY['streetlight', 'sanitation', 'water', 'parks', 'transportation'])[(n % 5) + 1] AS category,
    (ARRAY['low', 'medium', 'high', 'urgent'])[(n % 4) + 1] AS priority,
    CASE
        WHEN n % 100 < 2 THEN 'open'
        WHEN n % 100 < 7 THEN 'in_progress'
        WHEN n % 100 < 10 THEN 'new'
        ELSE 'closed'
    END AS status,
    'Synthetic ticket ' || n AS subject,
    timestamptz '2025-01-01 00:00:00+00' + n * interval '2 minutes' AS opened_at
FROM generate_series(1, 100000) AS g(n);

ANALYZE performance_lab.tickets;

SELECT count(*) AS row_count,
       count(*) FILTER (WHERE status = 'open') AS open_count
FROM performance_lab.tickets;
