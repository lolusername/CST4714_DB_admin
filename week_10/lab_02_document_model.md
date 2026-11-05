# Week 10 Lab 2 | Run queries in MongoDB

**[Launch the first interactive lab — Insert and Find](https://play.instruqt.com/embed/mongodb/tracks/crud-operations-in-mongodb--perform-crud-operations?token=em_8KmVAuFzDNFfao8W)**

Work individually for **55 minutes** in the MongoDB labs. Keep notes on what you run and what comes back. The required submission is **Part A, your lab record**, in one Brightspace text entry before you leave. Use the next 20 minutes to finish your work or, if your record is ready, try the [optional Chapter 10 response](reading_response.md).

## Start here | 5 minutes

On the lab page, select **Launch**, then **Start** when the workspace is ready. The first challenge is **Insert a Document**. Follow the instructions beside the MongoDB shell.

If you cannot get a working terminal within five minutes, [open the course notebook](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/10_day_2_insert_and_find.ipynb) and start there.

## Work in the lab | 55 minutes

| Time | What to do | Evidence to keep |
|---|---|---|
| First 15 minutes | Follow **Insert a Document** in the training environment. Use the database, collection, and fields named by the challenge. Run the insert once. Find the new document by its ID or another identifying field. | Record the collection, the filter you used for the read, and one field and value the read actually returned. An insert acknowledgment alone does not show what was stored. |
| Next 15 minutes | Work through the **Find** challenge. Pick a filter that returns a document. Predict what will happen if you change one value or add a condition. Run both versions in the lab where permitted, or use the notebook for the comparison. | Record both filters and one difference you observed: an ID that entered or left the result, or a change in count. If a prediction missed, explain which value surprised you. |
| Last 25 minutes | Open [the second interactive lab — Modify Query Results](https://play.instruqt.com/embed/mongodb/tracks/crud-operations-in-mongodb--modify-query-results?token=em_xAduftZJZ3IDAMmt) and select **Launch**. Try **Sort and Limit**. Predict which result will appear first. Change the sort direction or limit and run it again. Work on projection or counting if time permits. | Record what changed on screen. Compare the number displayed with the number of stored matches. What did the limit leave out? |

The first lab is timed. If you finish the insert and find challenges with time left on its clock, try the update challenge. When that session ends, move to the second lab even if you have unfinished challenges. If either terminal stalls, the notebook below lets you continue.

If the lab gives you a result you didn't expect, pause before running the next command. Write down what matched and change just one condition so you can explain the difference.

## If you need the course notebook

[Run the Week 10 Day 2 notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/10_day_2_insert_and_find.ipynb) or [download it for local Jupyter](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/10_day_2_insert_and_find.ipynb). Run the setup cell and note which engine it reports. The notebook uses a disposable MongoDB Community Server when available and labels the in-memory simulator if it has to use one. No Atlas credentials are needed. Use the notebook for the remainder of the same 55-minute block; it is an alternative way to do the work, not another assignment.

Use the small ticket collection to insert ticket 1090, read it back, and compare two filters. Try changing “at least 30 minutes” to “more than 30 minutes,” then choose a new boundary and check your prediction. Use the later exercises to investigate what a limited display leaves in storage. Record your own outputs for Part A. If both environments fail, tell the instructor where you got stuck; keep any actual output and label any hand-traced results as predictions.

## Submit

For **Part A (required)**, enter these three lines in the Week 10 Day 2 Brightspace text box:

- **Environment:** Which player challenge or notebook step did you reach? If you used the notebook, include the engine shown.
- **Write and read:** What did you insert, how did you look it up, and which field and value came back?
- **Changed filter:** Give the two conditions, your prediction, and the observed difference. Explain what caused it. If a command failed, identify the last result you actually saw.

Submit your lab record before leaving. **Part A alone meets the submission requirement.** If you choose to write [Part B, the optional Chapter 10 response](reading_response.md), add it below Part A in the same text entry.

Both labs are part of [MongoDB University’s CRUD Operations in MongoDB course](https://learn.mongodb.com/courses/crud-operations-in-mongodb).
