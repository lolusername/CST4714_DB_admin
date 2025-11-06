# Instructor Guide — Week 11 Indexing & Design Fundamentals

## Purpose
Help students progress through MongoDB University's Indexing & Design Fundamentals module while translating theory into measurable performance gains on their Atlas workloads. By the end of the session, every student should know how to interpret `explain` plans, design compound/multikey indexes, and verify improvements against real query logs.

## Session Snapshot
- **Format:** 170-minute studio session (can be split into two shorter meetings)
- **Theme:** Diagnosing query performance, building indexes that match workload shapes, validating ROI with profiler data
- **Anchor Resource:** [MongoDB University — Indexing & Design Fundamentals (Introduction to Indexes)](https://learn.mongodb.com/learn/course/indexing-design-fundamentals/indexing-design-fundamentals/introduction-to-indexes)

---

## Pre-Class Checklist
- [ ] Rewatch the MongoDB University videos (especially “When to Create an Index” and “Compound vs Multikey”).
- [ ] Prepare a clean Atlas sample dataset (e.g., `sample_supplies.sales` or last week’s embedded `customers` collection).
- [ ] Capture at least three Atlas Profiler entries (slow queries) to demonstrate before/after stats.
- [ ] Pre-create example indexes you can toggle on/off with `db.collection.dropIndex()` to show plan changes.
- [ ] Refresh on `collMod` and `validate` commands in case students ask about index corruption or storage limits.
- [ ] Set up a shared worksheet (Google Doc or LMS discussion post) where teams list their workload queries and candidate indexes.

---

## Agenda & Facilitation Notes

### 0:00–0:15 — Diagnostic Warm-Up
- Prompt: “What makes a query ‘slow’ in MongoDB? List at least three observable symptoms.”
- Display an `explain` output with a COLLSCAN plan; ask students to identify risk indicators (`totalDocsExamined` >> `nReturned`, missing sort stage).
- Transition by comparing B-tree traversal to the relational B+ tree they studied earlier in the course.

### 0:15–0:45 — Anatomy of Indexes
- Use a whiteboard to break down single-field vs compound vs multikey indexes. Emphasize prefix rules.
- Live demo:
  ```bash
  mongosh "mongodb+srv://<cluster>/<db>" --apiVersion 1 --username <user>
  > db.sales.createIndex({ storeLocation: 1, purchaseMethod: 1, saleDate: -1 })
  ```
- Highlight how the query optimizer chooses candidate plans; show `winningPlan` vs `rejectedPlans`.
- Discuss storage overhead and write amplification using Atlas Metrics → “Opcounters”.

### 0:45–1:20 — Guided Lab: Explain-Measure-Design Loop
- Students pair up, choose one workload query, and run:
  ```javascript
  db.orders.find({ status: 'SHIPPED', orderDate: { $gte: ISODate('2024-01-01') } })
           .sort({ orderDate: -1 })
           .projection({ customerId: 1, total: 1 })
           .explain('executionStats')
  ```
- Capture metrics in a shared table (query shape, keys examined, docs examined, execution time).
- Coach them through deriving index candidates respecting equality → sort → range order.
- Require them to rerun `explain` after each index change; screenshot results for homework verification.

### 1:20–1:30 — Break & Reflection
- Reflection prompt: “Which field order would you prioritize in a compound index for your workload and why?”
- Encourage posting answers in the LMS discussion thread for asynchronous participants.

### 1:30–2:00 — Advanced Patterns & Edge Cases
- Demonstrate:
  - Multikey behavior with array fields (`isMultiKey: true`).
  - Partial indexes for soft-deleted or tenant-specific data.
  - TTL indexes and how they interplay with performance.
- Show how to read Atlas Performance Advisor suggestions, emphasizing when to decline (e.g., low selectivity or write-heavy collections).

### 2:00–2:30 — Performance Clinics
- Rotate between teams while they implement indexes on their projects.
- Use a “clinic ticket” system: students submit their query shape + dataset size; you advise on index scope.
- Encourage use of Node.js or Python snippets to replay representative workloads if raw data is unavailable.

### 2:30–2:50 — SLO Alignment & Assessment Preview
- Connect indexing outcomes to the course SLOs (administration & performance tuning).
- Outline expectations for the upcoming checkpoint:
  - Provide `createIndex` statements.
  - Provide `explain` before/after metrics.
  - Interpret resource trade-offs (RAM, storage).
- Discuss rubric criteria: accuracy, documentation quality, and ability to justify design choices.

### 2:50–3:00 — Exit Ticket
- Prompt: “Name one query that still performs a COLLSCAN and describe what additional data or index pattern you need to fix it.”
- Collect responses via sticky notes or LMS poll to inform Week 12 planning (aggregation tuning).

---

## Differentiation Strategies
- **Fast movers:** Challenge them to compare alternative indexes with `db.collection.aggregate([{ $indexStats: {} }])` and reason about usage frequency.
- **Need support:** Provide a worksheet that walks through index prefix rules with partially completed examples.
- **Remote learners:** Screen-record the explain-plan walkthrough and share profiler exports so they can analyze asynchronously.
- **Ops-focused students:** Offer an optional exercise on rolling index builds with `background: true` (or Atlas rolling builds) and monitoring impact.

---

## Assessment & Follow-Up
- **Homework:** Submit a mini-report including query description, index definition, explain output screenshots, and a maintenance consideration (e.g., when to drop or rebuild).
- **Checkpoint quiz:** 8–10 questions covering index types, compound ordering rules, partial/TTL use cases, and interpreting `executionStats`.
- **Project integration:** Require teams to log their “index registry” in the repo (JSON or markdown) for future auditing.
- **Preview Week 12:** Aggregation pipeline performance, `$match`/`$sort` placement, and index intersection scenarios.

---

## Resources & References
- Student handout: `week_11/README.md`
- MongoDB Docs: [Indexes](https://www.mongodb.com/docs/manual/indexes/), [Analyze Query Performance](https://www.mongodb.com/docs/manual/tutorial/analyze-query-plan/), [Atlas Profiler](https://www.mongodb.com/docs/atlas/atlas-profiler/)
- MongoDB Blog: [Six Indexing Best Practices](https://www.mongodb.com/blog/post/building-with-patterns-the-schema-versioning-pattern)
- Tools: Atlas Performance Advisor, `mongosh` `explain`, Compass Schema Analyzer
- External inspiration: PostgreSQL `EXPLAIN ANALYZE` output for cross-database comparisons (useful analogy for SQL-minded students)

---

*Prepared for CST4714 Database Administration — revision date 2025-03-17.*
