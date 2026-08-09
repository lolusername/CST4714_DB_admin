# Lab 1: Query and Change Documents Safely

## Purpose

Use beginner MQL against a disposable course collection and verify every write.

This is individual work completed in class. Submit one notebook.

## 1. Open the Course Notebook

Open [`04_atlas_mql_modeling.ipynb`](../notebooks/04_atlas_mql_modeling.ipynb) in
Colab. Choose one path:

- **Atlas path:** configure your temporary network access, enter the Atlas URI only
  in the hidden runtime prompt, and use your uniquely named course database.
- **Offline path:** keep cloud mode off and use the in-memory MongoDB-compatible
  fixture. The same document shapes and operations run without an account.

Never place the URI in a cell. Do not set `tlsInsecure=True`; diagnose credentials,
network access, DNS, system time, and current driver/TLS support instead.

## 2. Complete the Query and Write Sequence

Run and explain notebook cells that:

- insert the synthetic ticket documents;
- find active high-or-urgent tickets with an explicit projection and sort;
- query a nested requester field;
- query one array value and one `$elemMatch` condition;
- update one test document with `$set` and `$push`;
- compare matched and modified evidence;
- read back the final document;
- delete only a record marked `test_record: true`; and
- prove cleanup with `deletedCount` and a final query.

Modify one filter and one projection so your output differs from the worked
example.

## 3. Complete the Evidence Prompts

In the notebook's final Markdown cell, explain:

- one result grain;
- why `$elemMatch` was or was not required;
- what `matchedCount` and `modifiedCount` proved;
- why the delete predicate was safe; and
- one Atlas connection control you configured and later narrowed or removed.

## Submit One Thing

Submit the completed notebook. Confirm that no URI or password appears in source
or output and that your explanation names actual query evidence.
