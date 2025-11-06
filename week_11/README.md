# Week 11 – Indexing & Query Performance Lab

Week 11 focuses on MongoDB's Indexing & Design Fundamentals with an emphasis on the **Introduction to Indexes** module from MongoDB University. Students will diagnose slow queries, design compound indexes that match real workloads, and validate improvements using `explain` metrics.

## Student Materials
- MongoDB University course: [Indexing & Design Fundamentals — Introduction to Indexes](https://learn.mongodb.com/learn/course/indexing-design-fundamentals/indexing-design-fundamentals/introduction-to-indexes).
- Sample workload notebook (reuse your Week 10 document schemas or import `sample_supplies` into Atlas for lab work).
- Atlas Performance Advisor screenshots for discussion (optional but recommended).

## Before Class
1. Finish at least the first module of the MongoDB University course above; capture one takeaway about single-field vs compound indexes.
2. Identify two read-heavy queries from your project or the sample dataset; paste their `find()` shapes into your notes so you can reference them live.
3. Ensure `mongosh` is installed and that you can connect to your Atlas cluster with read/write access to a sandbox database.
4. Turn on the Atlas Profiler for your sandbox cluster (Free tier is fine) so you can fetch slow-query samples during class.

## In-Class Flow
1. **Indexing Primer (15 min):** Summarize how MongoDB stores B-trees and why multikey indexes behave differently; tie back to the University video.
2. **Query Shape Inventory (20 min):** Students surface their top three operations (filter + sort + projection). Document them on the board and map which parts need indexing support.
3. **Explain Plan Lab (40 min):**
   - Run each query with and without indexes.
   - Use `db.collection.find(query).sort(sortClause).explain('executionStats')` to capture winning plan stages.
   - Highlight `stage`, `nReturned`, `totalKeysExamined`, `totalDocsExamined`, and `executionTimeMillis`.
4. **Compound & Multikey Practice (35 min):** Design compound indexes that align with filter → sort → projection order. Explore multikey caveats by indexing arrays and reviewing `isMultiKey` in the explain output.
5. **Performance Advisor Review (20 min):** If Atlas suggests indexes, compare them to your custom designs. Debate when to accept automated recommendations vs curating manually.
6. **Wrap-Up (10 min):** Students document one “final” index per workload and note trade-offs (write amplification, storage, TTL considerations).

## After Class Tasks
1. Implement and document the indexes chosen in class inside your project repo. Include:
   - Index definition (`db.collection.createIndex()` call).
   - Before/after explain metrics.
   - Risks or maintenance plans (e.g., TTL, partial filters).
2. Complete the remaining sections of the MongoDB University Indexing course and take the built-in knowledge checks.
3. Submit a short reflection (1–2 paragraphs) answering: “Which query benefited most from indexing and how did you validate the improvement?”

## Helpful Commands
```bash
# Connect to Atlas and evaluate a query plan
mongosh "mongodb+srv://<cluster>/<db>" --username <user>
> db.orders.find({ status: 'SHIPPED', orderDate: { $gte: ISODate('2024-01-01') } })
        .sort({ orderDate: -1 })
        .projection({ customerId: 1, total: 1 })
        .explain('executionStats')

# Build and inspect a compound index
> db.orders.createIndex({ status: 1, orderDate: -1, total: -1 })
> db.orders.getIndexes()

# Drop or rename indexes during experiments
> db.orders.dropIndex('status_1_orderDate_-1_total_-1')
```

## External Resources
- MongoDB Docs: [Indexes](https://www.mongodb.com/docs/manual/indexes/), [Compound Indexes](https://www.mongodb.com/docs/manual/core/index-compound/), [Multikey Indexes](https://www.mongodb.com/docs/manual/core/index-multikey/)
- Blog: [Understanding Explain Plan Output](https://www.mongodb.com/blog/post/performance-best-practices-mongodb-explain)
- Tooling: [Atlas Performance Advisor](https://www.mongodb.com/docs/atlas/performance-advisor/), [Atlas Profiler](https://www.mongodb.com/docs/atlas/atlas-profiler/)
