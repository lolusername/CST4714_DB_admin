-- Metro Support PostgreSQL setup
-- Run only in a course or personal practice database. This resets the
-- metro_support schema so the dataset is reproducible.

DROP SCHEMA IF EXISTS metro_support CASCADE;
CREATE SCHEMA metro_support;
SET search_path TO metro_support, public;

CREATE TABLE users (
    user_id integer PRIMARY KEY,
    display_name text NOT NULL,
    email text NOT NULL UNIQUE,
    role text NOT NULL,
    neighborhood text NOT NULL,
    created_at timestamptz NOT NULL
);

CREATE TABLE tickets (
    ticket_id integer PRIMARY KEY,
    requester_id integer NOT NULL REFERENCES users(user_id),
    assignee_id integer REFERENCES users(user_id),
    category text NOT NULL,
    priority text NOT NULL,
    status text NOT NULL,
    subject text NOT NULL,
    opened_at timestamptz NOT NULL,
    closed_at timestamptz,
    CHECK (closed_at IS NULL OR closed_at >= opened_at)
);

CREATE TABLE ticket_events (
    event_id integer PRIMARY KEY,
    ticket_id integer NOT NULL REFERENCES tickets(ticket_id),
    actor_id integer NOT NULL REFERENCES users(user_id),
    event_type text NOT NULL,
    old_status text,
    new_status text,
    note text,
    event_at timestamptz NOT NULL
);

INSERT INTO users
    (user_id, display_name, email, role, neighborhood, created_at)
VALUES
    (101, 'Maya Chen', 'maya.chen@example.test', 'resident', 'Harbor', '2026-01-08T14:20:00Z'),
    (102, 'Luis Rivera', 'luis.rivera@example.test', 'resident', 'Northside', '2026-01-10T09:15:00Z'),
    (103, 'Amina Yusuf', 'amina.yusuf@example.test', 'resident', 'Central', '2026-01-12T18:05:00Z'),
    (104, 'Jordan Bell', 'jordan.bell@example.test', 'resident', 'Harbor', '2026-01-18T11:40:00Z'),
    (201, 'Priya Shah', 'priya.shah@example.test', 'agent', 'Central', '2025-11-03T13:00:00Z'),
    (202, 'Noah Williams', 'noah.williams@example.test', 'agent', 'Northside', '2025-11-05T13:00:00Z'),
    (203, 'Elena Garcia', 'elena.garcia@example.test', 'supervisor', 'Central', '2025-09-14T13:00:00Z'),
    (204, 'Sam Okafor', 'sam.okafor@example.test', 'analyst', 'Harbor', '2025-12-01T13:00:00Z');

INSERT INTO tickets
    (ticket_id, requester_id, assignee_id, category, priority, status, subject, opened_at, closed_at)
VALUES
    (1001, 101, 201, 'streetlight', 'high', 'open', 'Streetlight dark near bus stop', '2026-02-01T23:10:00Z', NULL),
    (1002, 102, 202, 'sanitation', 'medium', 'in_progress', 'Missed recycling pickup', '2026-02-02T15:45:00Z', NULL),
    (1003, 103, 201, 'water', 'urgent', 'resolved', 'Low water pressure', '2026-02-03T12:05:00Z', '2026-02-03T19:40:00Z'),
    (1004, 104, NULL, 'parks', 'low', 'new', 'Broken bench slat', '2026-02-04T17:20:00Z', NULL),
    (1005, 101, 202, 'sanitation', 'high', 'resolved', 'Overflowing corner bin', '2026-02-05T14:00:00Z', '2026-02-05T20:15:00Z'),
    (1006, 102, 201, 'streetlight', 'medium', 'in_progress', 'Flickering lamp outside library', '2026-02-06T01:30:00Z', NULL),
    (1007, 103, 202, 'parks', 'medium', 'open', 'Playground gate will not latch', '2026-02-07T16:10:00Z', NULL),
    (1008, 104, 201, 'water', 'high', 'resolved', 'Hydrant leaking slowly', '2026-02-08T10:25:00Z', '2026-02-09T09:05:00Z'),
    (1009, 101, NULL, 'transportation', 'medium', 'new', 'Bus shelter panel cracked', '2026-02-09T22:15:00Z', NULL),
    (1010, 102, 202, 'sanitation', 'low', 'closed', 'Replacement bin request', '2026-02-10T13:50:00Z', '2026-02-12T16:30:00Z'),
    (1011, 103, 201, 'transportation', 'high', 'open', 'Crosswalk signal delayed', '2026-02-11T08:35:00Z', NULL),
    (1012, 104, 202, 'streetlight', 'low', 'resolved', 'Lamp stays on during daytime', '2026-02-12T14:45:00Z', '2026-02-14T18:10:00Z');

INSERT INTO ticket_events
    (event_id, ticket_id, actor_id, event_type, old_status, new_status, note, event_at)
VALUES
    (5001, 1001, 101, 'created', NULL, 'open', 'Reported through mobile form', '2026-02-01T23:10:00Z'),
    (5002, 1001, 201, 'assigned', 'open', 'open', 'Electrical crew notified', '2026-02-02T14:05:00Z'),
    (5003, 1002, 102, 'created', NULL, 'open', 'Pickup was scheduled for Monday', '2026-02-02T15:45:00Z'),
    (5004, 1002, 202, 'status_changed', 'open', 'in_progress', 'Route supervisor checking vehicle log', '2026-02-03T13:30:00Z'),
    (5005, 1003, 103, 'created', NULL, 'open', 'Pressure lower on two floors', '2026-02-03T12:05:00Z'),
    (5006, 1003, 201, 'status_changed', 'open', 'in_progress', 'Crew dispatched', '2026-02-03T14:25:00Z'),
    (5007, 1003, 201, 'status_changed', 'in_progress', 'resolved', 'Valve adjustment restored pressure', '2026-02-03T19:40:00Z'),
    (5008, 1004, 104, 'created', NULL, 'new', 'Photo attached in original report', '2026-02-04T17:20:00Z'),
    (5009, 1005, 101, 'created', NULL, 'open', 'Bin blocks part of sidewalk', '2026-02-05T14:00:00Z'),
    (5010, 1005, 202, 'status_changed', 'open', 'resolved', 'Extra collection completed', '2026-02-05T20:15:00Z'),
    (5011, 1006, 102, 'created', NULL, 'open', 'Flicker repeats every few seconds', '2026-02-06T01:30:00Z'),
    (5012, 1006, 201, 'status_changed', 'open', 'in_progress', 'Ballast inspection scheduled', '2026-02-06T15:10:00Z'),
    (5013, 1007, 103, 'created', NULL, 'open', 'Gate opens toward play area', '2026-02-07T16:10:00Z'),
    (5014, 1008, 104, 'created', NULL, 'open', 'Small stream along curb', '2026-02-08T10:25:00Z'),
    (5015, 1008, 201, 'status_changed', 'open', 'resolved', 'Gasket replaced and area checked', '2026-02-09T09:05:00Z'),
    (5016, 1009, 101, 'created', NULL, 'new', 'No sharp edge visible', '2026-02-09T22:15:00Z'),
    (5017, 1010, 102, 'created', NULL, 'open', 'Current bin lid is missing', '2026-02-10T13:50:00Z'),
    (5018, 1010, 202, 'status_changed', 'open', 'closed', 'Replacement delivered', '2026-02-12T16:30:00Z'),
    (5019, 1011, 103, 'created', NULL, 'open', 'Wait exceeds one full light cycle', '2026-02-11T08:35:00Z'),
    (5020, 1012, 104, 'created', NULL, 'open', 'Possible photocell issue', '2026-02-12T14:45:00Z'),
    (5021, 1012, 202, 'status_changed', 'open', 'resolved', 'Photocell cleaned and tested', '2026-02-14T18:10:00Z');

-- Verification: these counts should be 8, 12, and 21.
SELECT 'users' AS table_name, count(*) AS row_count FROM users
UNION ALL
SELECT 'tickets', count(*) FROM tickets
UNION ALL
SELECT 'ticket_events', count(*) FROM ticket_events;
