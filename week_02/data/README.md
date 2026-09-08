# Metro Support Dataset

Metro Support is a fictional public-service help desk used throughout the course.
The dataset is intentionally small enough to inspect by eye but rich enough to
practice relationships, integrity, concurrency, security, indexing, JSON,
document modeling, aggregation, and recovery.

## Files

- [users.csv](users.csv): 8 people who submit or handle tickets.
- [tickets.csv](tickets.csv): 12 support requests, one row per request.
- [ticket_events.csv](ticket_events.csv): 21 status changes and notes over time.
- [PostgreSQL setup](postgres_setup.sql): creates the tables and loads all rows.

The [Week 2 notebook](../01_relational_sql_review.ipynb) also includes all the
rows. Its **Use the Complete Week 2 Lab Dataset** section loads them in DuckDB.

## Relationships

- `tickets.requester_id` refers to `users.user_id`.
- `tickets.assignee_id` may refer to a staff user or be empty.
- `ticket_events.ticket_id` refers to `tickets.ticket_id`.
- `ticket_events.actor_id` refers to `users.user_id`.

## Intentional Design Questions

- Should `status` and `priority` accept arbitrary text?
- Should a deleted user remove historical tickets?
- Which queries need an index?
- Who may read internal event details?
- In MongoDB, should events be embedded in a ticket or referenced separately?

## License

This is original synthetic data. It contains no real personal information and is
released under CC0 1.0.
