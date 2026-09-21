# Lab 1: Count the Work That Needs Attention

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_04/04_reliable_reporting.ipynb)

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_04/lab_01_category_report.md)

An operations manager needs one row per request category, not one row per history
event. Build a report that counts all requests, active requests, and active
requests that have high or urgent priority. Work individually in class.

## 1. Read the Data and the Worked Example

Run the notebook introduction and setup, or use the
[PostgreSQL setup](materials/datasets/metro_support/README.md). Confirm **8 users,
12 tickets, 21 events**. One ticket is one request. Ticket 1003 has three event
rows, so a direct ticket-event join can multiply the rows being counted.

Run this worked example before changing it:

```sql
SELECT category,
       count(*) AS total_tickets,
       count(*) FILTER (WHERE status = 'resolved') AS resolved_tickets
FROM metro_support.tickets
GROUP BY category
ORDER BY category;
```

It keeps all five categories. The total column sums to 12; the resolved column
sums to 4. `FILTER` changes only its aggregate, unlike a top-level `WHERE` that
would remove rows before every aggregate.

## 2. Adapt, Check, and Explain

Adapt the example to return `category`, `total_tickets`, `active_tickets`, and
`high_or_urgent_active_tickets`. Active means `new`, `open`, or `in_progress`.
The final measure must satisfy **both** the active condition and
`priority IN ('high', 'urgent')`.

Keep all five categories, including zeros. Check that the columns sum to
**12, 7, and 2**. Then write a separate simple `SELECT` that lists the two
high-or-urgent active ticket IDs. Compare those records with the CSV or notebook
data rather than only comparing totals.

**Submit:** `week_04_category_report.sql` in Brightspace, containing your report,
the independent check, and two or three SQL-comment sentences explaining what
one report row represents and why joining all events could overstate workload.
No screenshots, separate report, or notebook attachment are needed.
