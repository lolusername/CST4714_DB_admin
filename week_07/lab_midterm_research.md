# Week 7 Lab: Midterm Preliminary Research

Spend about 50 minutes preparing Part 4 of the Metro Support midterm, the index test. Inspect the supplied data in Colab, read two short documentation sections, and write a plan for the test you will run later in PostgreSQL. Work individually.

## Open the notebook

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_07/07_midterm_preliminary_research.ipynb)

Open the notebook with the button above, then choose **File > Save a copy in Drive**. Rename your copy Lastname_Week07_Research and connect to a Python 3 runtime. You can also [download the notebook](07_midterm_preliminary_research.ipynb) and use **File > Upload notebook** at [Colab](https://colab.research.google.com/).

The notebook includes all data and code. No installation, Supabase login, or database credentials are needed. It uses Python to inspect CSV data; PostgreSQL transaction and index tests happen later in the midterm.

## The query you are researching

Section 4A of the [midterm starter](../week_08/materials/assignments/midterm_starter.sql) lists the newest open tickets:

```sql
SELECT ticket_id, subject, opened_at
FROM midterm_metro.tickets
WHERE status = 'open'
ORDER BY opened_at DESC, ticket_id DESC
LIMIT 20;
```

Section 4B proposes this index for it. The last key breaks ties between equal timestamps.

```sql
CREATE INDEX midterm_tickets_status_opened_idx
ON midterm_metro.tickets (status, opened_at DESC, ticket_id DESC);
```

Today you study the data this query reads and what the documentation says such an index can do. You do not write or run SQL today.

## Work in the notebook

1. **Inspect the data, about 10 minutes.** Run the cells from the top and fill in the observation table: the three table counts, the ordered open-ticket IDs, the ordered new-ticket IDs, and one ticket's ID, status, and requester. Record the open list before you change STATUS to new.
2. **Read, about 10 minutes.** Open the two linked PostgreSQL excerpts on indexes and ordering, and read only the paragraphs the notebook names. Look for what an index might avoid, why PostgreSQL might choose another plan, and what work an index adds.
3. **Write, about 25 minutes.** Write 180–250 words in total across the three response cells:
   - **A, about 50–70 words:** what the query must return, two observations from your notebook, and why LIMIT 20 can return fewer than twenty rows in this dataset.
   - **B, about 80–110 words:** how an index could help the filter or the ordering, one cost, an idea from each source with its link, and why an index definition online does not prove that this small database will run faster.
   - **C, about 50–70 words:** one before-and-after PostgreSQL test, what stays the same, which results and plan evidence you will compare, and what would make you keep or reconsider the index. Label your expected outcome as a prediction and end with one question you still need answered.
4. **Check, about 5 minutes.** Make sure every observation matches an output, both source links are present, and your expected result is labeled as a prediction.

## Submit

Submit **one Colab link** in today's classwork assignment in Brightspace. Run every cell, then choose **File > Save** so your outputs and writing are stored in your Drive copy, Lastname_Week07_Research. Choose **Share**, give the instructor viewer access, and copy the link. Submit your saved copy's link, not the starter notebook's GitHub or Colab link. No file upload, separate report, or screenshots.

I will look for accurate observations, a connection between the two sources and this dataset, a test that compares the same query and results, and a clear distinction between what you observed and what you predict. You can revise and reuse the writing in your final midterm README. The final midterm still uses midterm.sql and README.md.
