# Final Class Lab
## GitHub Database Concept Artifact

## Purpose
Today you will create one small GitHub artifact that explains a database concept from this course.

This is not a big coding assignment.
The goal is to create something you could show in a job interview, internship interview, portfolio review, or final project discussion.

## Individual Work Only
This lab is individual.
Do not combine submissions.

## What You Will Create
Create one GitHub repository or one GitHub file that teaches one course concept.

Your artifact can be:
- a Markdown guide
- a short code example with comments
- a SQL example with explanation
- a JSON/MongoDB example with explanation
- a small notebook or script
- a README that combines explanation and code

## Choose One Concept
Pick one concept from this course.

Good choices include:
- relational schema design
- primary keys and foreign keys
- SQL joins
- indexes and query performance
- transactions
- isolation and locking
- backup and restore
- database security and least privilege
- Supabase/Postgres administration
- row-level security
- JSON data
- MongoDB document modeling
- embedding vs referencing
- MongoDB aggregation
- MongoDB read/write concerns
- source of truth in distributed systems
- polyglot persistence
- graph, key-value, document, or vector databases

## Option A: Markdown Guide
Use this structure in a GitHub `README.md` file:

```markdown
# Concept Name

## What This Means
Explain the concept in beginner-friendly language.

## Why It Matters
Explain what problem this concept helps solve.

## Small Example
Include a small SQL, JSON, MongoDB, Python, or pseudocode example.

## What Can Go Wrong
Explain one mistake, limitation, or tradeoff.

## Course Connection
Name the week, lab, notebook, or final project connection.

## Interview Explanation
Write 2-4 sentences explaining how you would talk about this concept in an interview.
```

## Option B: Code Example
Create one small code file and one short `README.md`.

Your code can be:
- `example.sql`
- `example.py`
- `example.json`
- `example.mongodb.js`
- `example.md`

Your code must include comments that explain what is happening.

Your `README.md` must explain:
- what the code demonstrates
- why the concept matters
- what a real database administrator would check or verify

## Using The GitHub Web Editor
You may do this entirely in the browser.

1. Go to GitHub.
2. Create a new repository or open an existing class repository.
3. Create a file named `README.md`.
4. Paste your guide.
5. Add a code block or create a second file with a small example.
6. Commit the file directly in GitHub.
7. Copy the GitHub URL for your repository or file.

## Example Topics

### Example 1: Indexes
Your guide could explain that an index helps the database find matching rows faster, but indexes also add storage and write-maintenance cost.

Small example:

```sql
CREATE INDEX idx_tickets_status_created_at
ON tickets (status, created_at);

SELECT *
FROM tickets
WHERE status = 'open'
ORDER BY created_at DESC;
```

### Example 2: MongoDB Embedding
Your guide could explain that embedding stores related data inside the same document when the application usually reads it together.

Small example:

```json
{
  "order_id": "ord_1001",
  "student": "Avery",
  "items": [
    { "name": "burrito", "price": 8.50 },
    { "name": "drink", "price": 2.00 }
  ]
}
```

### Example 3: Source Of Truth
Your guide could explain that a source of truth is the system the application treats as official when other copies disagree.

Small example:

```text
Official order table says: paid
Event log says: missing checkout event
Decision: trust the official order table, then repair the missing event safely
```

## Submit
Submit one Brightspace text response.

Include:
1. your GitHub URL
2. the concept you chose
3. one sentence explaining why this concept matters

## Success Standard
You are successful if another student could open your GitHub artifact and understand the concept without you standing next to them.
