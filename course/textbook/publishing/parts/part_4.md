# Part IV: Scale and Integration {.unnumbered .part-title}

Scale is not merely a larger number of rows. It changes coordination, routing,
capacity, cost, recovery, observability, and the number of failure combinations an
operator must understand. Chapters 13-14 examine workload-based capacity,
sharding decisions, safe imports, client connection contracts, polyglot
persistence, event-driven propagation, and reconciliation.

The central question remains ownership of truth. A multi-database design is
defensible only when each fact has an authoritative source, partial failures are
expected, and a repair path is designed before an incident.
