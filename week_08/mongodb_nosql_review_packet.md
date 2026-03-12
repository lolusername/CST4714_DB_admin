# MongoDB and NoSQL Review Packet - CST4714

This packet now spans two moments in the course:
- the Week 7 NoSQL bridge
- the Week 8 MongoDB lecture

## How To Use This Packet
1. After Week 7, complete the history and workload-classification parts without notes.
2. After Week 8, return to the MongoDB modeling and query prompts.
3. Review the concept refreshers only after you try the questions.
4. Finish with the exit ticket so you can connect the ideas to your own project.

---

## 1. Diagnostic Check (Closed Notes)
1. Why did NoSQL become prominent again in the 2000s even though non-relational databases existed long before that?
2. Match each workload to a NoSQL family: session store, product catalog with variable attributes, fraud relationship analysis, and high-volume telemetry.
3. In MongoDB, what is the difference between embedding related data and referencing related data?
4. What does it mean to say that MongoDB writes are atomic at the document level by default?
5. Why is "schema-less" a misleading phrase in professional MongoDB work?
6. Give one reason a workload may still fit PostgreSQL better than MongoDB.

Write your answers before reading Section 2.

---

## 2. Concept Refreshers

### 2.1 NoSQL History in One Story
- Early databases included hierarchical and network models.
- The relational model became dominant because it made data more declarative and portable through SQL.
- Web-scale applications later pushed teams toward systems optimized for horizontal growth, flexible records, and simpler application-shaped data.
- The NoSQL movement did not erase relational databases. It made multi-model thinking mainstream.

**Quick recall:** Finish this sentence: "NoSQL rose again because..."

### 2.2 The Four Major Families
- **Key-value:** best when the application already knows the key and needs very fast retrieval.
- **Document:** best when data is naturally shaped like nested application objects.
- **Column-family:** best for huge sparse or time-windowed workloads with heavy write volume.
- **Graph:** best when traversing relationships is the main query pattern.

**Quick recall:** Which family would you choose for a recommendation engine, and why?

### 2.3 MongoDB Modeling
- A MongoDB document is a BSON record stored inside a collection.
- Good document design starts with access patterns: what gets read and written together?
- **Embed** when the child data belongs to the parent, stays bounded, and is usually fetched together.
- **Reference** when the child data is shared, many-to-many, or grows without a safe bound.
- Flexible schema still needs validation rules and naming discipline.

**Quick recall:** Why can giant arrays become a design problem?

### 2.4 CRUD and Aggregation
- `insertOne`, `find`, `updateOne`, and `deleteOne` are the basic MongoDB CRUD patterns.
- Read the filter first. Then read the projection or update operator.
- Aggregation is a pipeline: filter, reshape, group, sort, project.
- `$unwind` expands arrays into multiple pipeline rows, which can multiply work.

**Quick recall:** What question does `$group` usually answer?

### 2.5 DBA Lens
- MongoDB still requires indexes, validation, backup/restore planning, security, and monitoring.
- A flexible schema shifts governance work; it does not remove it.
- Denormalization can improve reads, but it can also make updates harder to keep consistent.
- If a workload constantly needs cross-document transactions and many joins, the model may be a poor fit.

**Quick recall:** What is one MongoDB administrative task that has the same spirit as what we already do in PostgreSQL?

---

## 3. Workload Classification Practice

For each case below, choose a database family and justify your answer in 2-3 sentences.

### Case A - Campus Mobile App Sessions
Students log in frequently, and the app mostly needs to look up session or token data by a known key.

### Case B - Course Resource Catalog
Each resource has a shared core structure, but different categories have different attributes and media metadata.

### Case C - Academic Integrity Investigation
You need to analyze shared devices, accounts, IPs, and submissions to find suspicious relationship patterns.

### Case D - Lab Sensor Streams
Hundreds of devices write timestamped values continuously, and instructors mostly query recent time windows.

When you answer, name one DBA concern too: indexing, retention, failover, schema drift, access control, or backup/restore.

---

## 4. Modeling Practice

You are storing bookstore orders.

### Relational Sketch
- `customers(customer_id, name, email)`
- `orders(order_id, customer_id, status, ordered_at)`
- `order_items(order_id, sku, qty, price)`

### Task
1. Describe one reason this normalized structure is good.
2. Describe one reason a MongoDB `orders` document with embedded `lineItems` could be better for an order-detail screen.
3. Name one field you would consider storing as a snapshot inside the order document and explain why.
4. Name one thing you would probably keep as a reference instead of embedding.

---

## 5. Query Practice

Assume a collection named `orders` with documents shaped like this:

```javascript
{
  customerId: 42,
  status: "shipped",
  shippingCity: "Tampa",
  lineItems: [
    { sku: "SSD-1TB", qty: 1, price: 89.99 },
    { sku: "USB-C-HUB", qty: 2, price: 24.50 }
  ]
}
```

### Prompt 1 - Filter + Projection
Write a `find` query that returns shipped orders from Tampa and shows only `customerId`, `status`, and `shippingCity`.

### Prompt 2 - Targeted Update
Write an `updateOne` query that changes one pending order to `paid`.

### Prompt 3 - Aggregation Thinking
Without writing the full syntax yet, describe the pipeline stages you would use to answer this question:

"Which customers generated the most revenue from shipped orders?"

### Prompt 4 - Index Reasoning
If Prompt 1 becomes frequent, what field or field combination would you consider indexing first, and why?

---

## 6. Answer Key Highlights

| Item | Expected Idea |
| --- | --- |
| 1 | NoSQL became prominent again because web-scale and cloud workloads stressed relational assumptions around scale, flexibility, and application-shaped data. |
| 2 | Session store -> key-value; variable product catalog -> document; fraud relationships -> graph; telemetry -> column-family. |
| 3 | Embedding stores child data inside the parent document; referencing links to separate documents by identifier. |
| 4 | A single document update either succeeds or fails as one unit by default. |
| 5 | MongoDB still needs structure, validation, naming discipline, and governance even if every field is not predeclared in one rigid table schema. |
| 6 | PostgreSQL may be better when the workload depends on many joins, strong relational integrity, and broad ad hoc reporting. |

Use these highlights to self-check. If your wording differs but your reasoning matches, that is fine.

---

## 7. Exit Ticket
Answer these in complete sentences:

1. Why is "best tool for the job" a better mindset than "MongoDB is modern, so use MongoDB"?
2. Is your current project idea more relational or more document-shaped? Defend your answer.
3. What is one MongoDB anti-pattern you want to avoid?

---

## 8. Study Checklist
- [ ] I can explain the historical reason NoSQL re-emerged.
- [ ] I can name the four major NoSQL families and a workload for each.
- [ ] I can explain embed versus reference in MongoDB.
- [ ] I can read a basic `find` and `updateOne` query.
- [ ] I can explain what an aggregation pipeline does.
- [ ] I can name at least three MongoDB DBA responsibilities.
