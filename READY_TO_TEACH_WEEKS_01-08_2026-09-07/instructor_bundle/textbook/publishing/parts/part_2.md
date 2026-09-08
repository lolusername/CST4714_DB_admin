# Part II: Operating PostgreSQL Safely {.unnumbered .part-title}

Once data meaning is explicit, administration becomes controlled change under
concurrency, access rules, performance constraints, and failure. Chapters 4-8
move from views and migrations through transactions, row-level security, query
plans, indexes, backup, and restore.

Each topic uses the same discipline: frame a testable promise, observe a baseline,
make one deliberate change, verify the result and side effects, and record what
the test does not cover. Supabase appears as managed PostgreSQL, not as a new SQL
dialect, so provider responsibility remains separate from customer-owned schema,
permissions, queries, secrets, and recovery.
