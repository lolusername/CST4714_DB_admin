# Mini Inventory Dataset

Mini Inventory is a fictional, original dataset for project inspiration and the
event-driven inventory case. It is intentionally small and contains no real
people, organizations, products, or transactions.

- `items.csv` stores authoritative item identity and reorder policy.
- `inventory_events.csv` stores append-style receipts, reservations, sales, and
  adjustments.

Students can model current stock as a relational view or aggregation, embed a
bounded event summary, keep events separate, test idempotent event IDs, or discuss
which system should own quantity.

This dataset is released under CC0 1.0.
