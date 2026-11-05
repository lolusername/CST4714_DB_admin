# Week 10 Lab 2 | Insert and find documents in MongoDB

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_10/lab_02_document_model.md)

Today you will **work individually for 55 minutes** in MongoDB University, then have **20 minutes to write**. By the end, you should be able to retrieve a document you inserted, explain how a filter changes a result, and use Chapter 10 to recommend a design for a ticket page.

**Submit:** one Brightspace text entry with two parts. Part A is your short lab record below. Part B is your [Chapter 10 reading response](reading_response.md). Keep your notes in a text editor as you work.

## Launch the lab | 5 minutes

1. Open [MongoDB CRUD Operations: Insert and Find Documents](https://learn.mongodb.com/courses/mongodb-crud-operations-insert-and-find-documents). Sign in or enroll in the free unit if prompted.
2. Start **Lesson 1** and select **Practice**. Follow the activity into its provided workspace. Use the database, collection, and example documents named there. Earlier lessons may need to be visited in order.
3. Use the University workspace for today's exercises. Keep the course ticket data for the reading response. If the workspace will not launch after one sign-in or relaunch attempt, [use the course practice below](#if-the-university-workspace-is-unavailable).

## Work through three lessons | 55 minutes

| Time | Open in MongoDB University | Do and observe |
|---|---|---|
| First 20 min | [Lesson 1 Practice — Inserting documents](https://learn.mongodb.com/learn/course/mongodb-crud-operations-insert-and-find-documents/lesson-1-inserting-documents-in-a-mongodb-collection/practice) | Follow the insert task. Identify the collection and one field you can use to recognize the inserted document. Read it back with a find operation where the workspace allows it. Record one returned field and value. |
| Next 20 min | [Lesson 2 Practice — Finding documents](https://learn.mongodb.com/learn/course/mongodb-crud-operations-insert-and-find-documents/lesson-2-finding-documents-in-a-mongodb-collection/practice) | Run a find exercise. Predict which documents match. Change one condition or compare two filters provided by the exercise. Record the filters and a concrete difference in the returned documents or counts. A zero-match result is evidence too. |
| Last 15 min | [Lesson 3 Practice — Comparison operators](https://learn.mongodb.com/learn/course/mongodb-crud-operations-insert-and-find-documents/lesson-3-finding-documents-by-using-comparison-operators/practice) | Try a comparison using the exercise's field and data type. Predict whether a value at the boundary is included. Where the workspace permits it, compare a strict condition with an inclusive one, for example `$gt` with `$gte` at the same value. Explain the result. |

Use each lesson's **Learn** section when you need an example. Follow the platform's directions inside graded tasks. If one task prevents extra queries, use the next permitted exercise or the course practice to try your variation, and label where you ran it. If you finish early, try Lesson 4 on array elements. At the writing cue, stop at your current checkpoint and record what you actually tried.

## Part A | Lab record

Use these three lines in Brightspace. Include only the collection name, conditions, and enough of each result to explain your observation. Leave account details out.

- **Route and progress:** Which environment did you use? Which lesson or step did you reach?
- **Insert and read back:** What did you insert, how did you look for it, and what field/value came back? If an operation failed, record the error or last usable observation.
- **Changed filter:** Give the first condition and result, then the changed condition and result. Explain why the change mattered. Mark a prediction explicitly if you could not execute it.

**Next:** complete [Part B, the Chapter 10 reading response](reading_response.md). Paste both parts into the same Week 10 Day 2 Brightspace submission. The text entry is the entire hand-in.

## If the University workspace is unavailable

Use a fresh [Colab notebook](https://colab.research.google.com/) or local Jupyter. These Python cells create a small in-memory practice collection with `mongomock`. This route uses the same insert, read-back, and filter decisions. It runs without an Atlas login or database URI. Label Part A **in-memory practice**.

Run this setup cell once. Rerunning it starts the exercise over.

```python
%pip -q install "mongomock>=4.3,<5"
import mongomock

practice_client = mongomock.MongoClient()
tickets = practice_client.week10_day2.practice
tickets.insert_many([
    {"ticket_id": 1001, "status": "open", "age_minutes": 12},
    {"ticket_id": 1002, "status": "in_progress", "age_minutes": 30},
    {"ticket_id": 1003, "status": "resolved", "age_minutes": 45},
])
```

1. Insert the new practice ticket and read it back. Which returned value lets you identify it?

```python
ticket = {"ticket_id": 1090, "status": "open", "age_minutes": 30}
result = tickets.insert_one(ticket)
print(tickets.find_one({"_id": result.inserted_id}, {"_id": 0}))
```

2. Run the same display function with two filters. Predict the ticket IDs for each filter before running it. Then try one different status of your choice.

```python
def matching_ids(condition):
    return [row["ticket_id"] for row in tickets.find(
        condition, {"_id": 0, "ticket_id": 1}
    ).sort("ticket_id", 1)]

print(matching_ids({"status": "open"}))
print(matching_ids({"status": "open", "age_minutes": {"$gte": 30}}))
```

3. Replace `$gte` with `$gt`, leaving the threshold at 30. Explain which ticket moved out of the result. Then try another threshold that changes the result again. Record the results you observed before closing the session with `practice_client.close()`.

**If both workspaces are unavailable:** use the four documents printed above as a paper trace. Trace the insert, predict what the read-back would show, and list the matching ticket IDs for the open, inclusive, and strict conditions. Label your results **paper prediction** and give the point where access stopped. Then complete the same reading response.
