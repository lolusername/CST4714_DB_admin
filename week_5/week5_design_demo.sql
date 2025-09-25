-- Week 5 live demo staging script: denormalized ticketing sheet
-- Audience: students (run-only). Instructor decomposition steps live in instructor_guide.md.
-- Goal: load the messy source data so you can surface anomalies before normalizing.

-- ---------------------------------------------------------------------------
-- 1. Business narrative (read aloud before running)
-- ---------------------------------------------------------------------------
-- A city theatre sells tickets for seasonal performances. The operations team
-- keeps everything in a single spreadsheet with these columns:
--   customer_full_name, customer_email, phone,
--   performance_title, genre, venue_name, venue_capacity,
--   show_date, show_time, ticket_section, ticket_price,
--   seats_purchased, order_total, payment_status
-- Problems encountered:
--   * Duplicated venue data with conflicting capacities.
--   * Tickets for different show dates share the same order id.
--   * Updating a customer’s email requires editing every past order row.
--   * Queries for revenue by performance are slow and error prone.
-- This script recreates that spreadsheet so you can diagnose issues. The
-- step-by-step normalization walkthrough lives in the instructor guide.

-- ---------------------------------------------------------------------------
-- 2. Recreate the spreadsheet as a staging table to surface anomalies
-- ---------------------------------------------------------------------------
CREATE TABLE event_ticketing_raw (
    order_id            integer,
    customer_full_name  text,
    customer_email      text,
    phone               text,
    performance_title   text,
    genre               text,
    venue_name          text,
    venue_capacity      integer,
    show_date           date,
    show_time           time,
    ticket_section      text,
    ticket_price        numeric(7,2),
    seats_purchased     integer,
    order_total         numeric(9,2),
    payment_status      text
);

INSERT INTO event_ticketing_raw VALUES
    (101, 'Maya Patel',   'maya@example.com',   '212-555-0199', 'Hamilton Revival', 'Musical', 'Grand Lyric Hall', 1800, '2024-04-12', '19:30', 'Orchestra', 185.00, 2, 370.00, 'paid'),
    (102, 'Malik Jones',  'malik@example.com',  '718-555-2211', 'Hamilton Revival', 'Musical', 'Grand Lyric Hall', 1850, '2024-04-13', '19:30', 'Mezzanine', 145.00, 3, 435.00, 'paid'),
    (103, 'Ava Chen',     'ava.chen@example.com','917-555-6644', 'City Lights Ballet', 'Dance', 'Spectrum Arts Center', 950, '2024-05-01', '20:00', 'Balcony', 95.00, 4, 380.00, 'pending'),
    (103, 'Ava Chen',     'ava.chen@example.com','917-555-6644', 'City Lights Ballet', 'Dance', 'Spectrum Arts Center', 940, '2024-05-04', '14:00', 'Balcony', 95.00, 2, 190.00, 'pending'),
    (104, 'Maya Patel',   'maya@example.com',   '212-555-0199', 'City Lights Ballet', 'Dance', 'Spectrum Arts Center', 950, '2024-05-04', '14:00', 'Orchestra', 135.00, 2, 270.00, 'paid');

-- ---------------------------------------------------------------------------
-- 3. Explore anomalies (students use these queries to drive normalization)
-- ---------------------------------------------------------------------------
-- Conflicting venue capacities
-- SELECT venue_name, array_agg(DISTINCT venue_capacity) AS capacities
-- FROM event_ticketing_raw
-- GROUP BY venue_name;

-- Order spanning multiple show dates
-- SELECT order_id, show_date, show_time, seats_purchased
-- FROM event_ticketing_raw
-- ORDER BY order_id;

-- Recomputed totals vs stored totals
-- SELECT order_id,
--        SUM(seats_purchased * ticket_price) AS computed_total,
--        MAX(order_total) AS stored_total
-- FROM event_ticketing_raw
-- GROUP BY order_id;

-- Normalization steps live in week_5/instructor_guide.md for instructor use only.
