# Midterm Project Metro Support

CST4714 Database Administration · Atilio Barreda · Individual project · 30% of the course grade

## What you are making

You will use the small Metro Support database from class to show that you can check data, control a transaction, explain a blocked session, and test one database improvement. Then you will describe how to recover the database from a backup. Submit two files: **midterm.sql** and **README.md**.

We introduce the project in Week 7 and cover the recovery portion in Week 8. Use the deadline posted in Brightspace. The project does not require a web application, a new dataset, or a presentation.

## Start with the supplied files

- Save [midterm_starter.sql](midterm_starter.sql) as **midterm.sql**.
- Save [midterm_README_template.md](midterm_README_template.md) as **README.md**.
- Use the [Week 5 blocking notebook](../notebooks/02_postgres_transactions_locks.ipynb) for Part 3. You may reuse your own Week 5 observations.

The starter includes all three tables and the seed data. You may use this supplied code. Your work is to complete the marked sections, record what actually happened, and explain the results in your own words. Work in your personal Supabase practice project or a local/instructor-provided PostgreSQL database.

The starter resets **midterm_metro**, a separate practice schema. Running it from the top deletes previous work in that schema and any objects that depend on it. Use a dedicated practice database. Save your SQL and observations before restarting. Once setup is complete, select and run the section you need. Do not rerun setup between the two halves of an experiment.

## Part 1 Build and check the database

Run the supplied setup. Confirm **8 users, 12 tickets, and 21 ticket events**. Add a relationship query joining tickets to their requesters. It should return one row for each of the 12 tickets, with its requester name.

In the README, identify three existing non-key integrity controls and explain what each prevents. The starter already contains examples of NOT NULL, UNIQUE, and CHECK. You do not need to redesign the tables or invent new constraints.

Keep the setup and both verification queries in midterm.sql. Record your actual counts and relationship result in the README.

## Part 2 Roll back and commit a change

Use ticket **1004**, which starts with priority **low** in this dataset. The starter gives you a rollback example: change its priority to high inside a transaction, inspect it, roll back, and inspect it again.

Then write a similar transaction that changes its priority to **medium** and commits. Query the row after COMMIT. Record the before, inside, and after values for both transactions, and explain why the final values differ. Keep the same session throughout each transaction. Run each BEGIN through its final verification together if your editor changes sessions between runs.

Leave the committed medium value in the database. Use simple updates; adding ticket events is not required.

## Part 3 Explain one blocking incident

Use your Week 5 notebook results, or run its controlled example again. Record the diagnostic SQL, the blocked and blocking session IDs, the row involved, the action that released the block, and the final row values.

If you cannot connect, use the notebook's supplied trace and label your answer **supplied trace analysis**. Explain that trace rather than claiming a live run. The reasoning criteria are the same for either path. The notebook uses **lock_lab**, whose starting values differ from the midterm dataset; read the trace's values carefully.

Put this short explanation in the README. Include the notebook only if you changed its code. Screenshots are optional and earn no extra credit.

## Part 4 Test one improvement

**Recommended route: use the index experiment already outlined in the starter.** The query asks for the newest open tickets. Run the SELECT and its analyzed plan before adding the index. Add the supplied index on (status, opened_at DESC, ticket_id DESC), then repeat the identical SELECT and plan. The last key breaks timestamp ties. Save the ordered ticket IDs, relevant plan lines, and index size.

Explain the problem the index is intended to address, whether your plan changed, whether the result stayed the same, and one cost of keeping the index. This database has only 12 tickets. PostgreSQL may keep using a sequential scan, and timings may barely change. An honest explanation of that result can earn full credit. A faster time or an Index Scan is not required. Do not add fake rows or change planner settings to force a result.

If you prefer, choose one alternative already covered in class: a least-privilege grant, an RLS policy test, or a safe schema change. Show the relevant before/after checks and explain a tradeoff. Complete **one** improvement only. The 100,000-row classroom demonstration is optional practice, not a second midterm database.

## Part 5 Write a recovery plan after Week 8

Add a short recovery section to the README, about one page at most. Name the source database and schema, describe the logical backup command or interface steps, and identify a separate empty restore destination. Include the restore command or steps and at least three specific verification checks, with expected results.

For this starter, useful checks include table counts, requester relationships, ticket 1004's committed value, and the added index. State any limits of the backup, such as omitted roles or grants. Use the Week 8 examples and adapt their schema and destination to your project. A logical export is sufficient; do not depend on a paid backup feature. **Executing a restore is optional.** Clearly distinguish a proposed check from a result you actually observed.

## Submission checklist

Submit one ZIP containing midterm.sql and README.md. Keep expected-error tests commented out so the ordinary SQL run can finish. Include a modified blocking notebook only if needed. Do not include passwords, connection strings, API keys, or service-role keys.

Your SQL should include setup, the two verification queries, rollback and commit work, and your chosen improvement. Your README should explain run order and environment, actual results, blocking, the improvement, and the recovery plan. Replace every prompt in the template before submitting.

## Rubric 100 points

| Area | Points | What I will check |
|---|---:|---|
| Reproducible schema and data integrity | 25 | Setup runs, counts and relationships are checked, and you explain three controls |
| Transactions and blocking diagnosis | 25 | Rollback and commit outcomes are verified; the blocking explanation matches the evidence |
| Workload based improvement | 20 | One change has a reason, relevant before/after checks, and a stated tradeoff |
| Recovery readiness | 15 | The plan uses a separate destination and at least three meaningful checks |
| Documentation and communication | 15 | Another person can follow the two files; results are clear and secrets are absent |

Use the code and notebooks we have already worked with. A small working project with clear explanations is enough.
