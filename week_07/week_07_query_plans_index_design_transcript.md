# Week 7 Midterm Explanation and Preliminary Research Transcript

Atilio Barreda · CST4714 Database Administration

Speaker notes for the five-slide class deck. Allow 45 minutes for the project explanation, 50 for the research notebook, and five to save and submit.

## Slide 1

Today is the midterm explanation and preliminary research lab. Spend 45 minutes walking through the actual project handout, SQL starter, README template, and rubric. Then give students 50 minutes for the research notebook and five minutes to download and submit it. The larger index demonstration is optional reference for another time.

The notebook uses supplied CSV data and Python. It does not require Supabase or execute PostgreSQL transactions or query plans. Its writing prepares students to run and explain their midterm work later.

## Slide 2

Walk through all five project parts while the assignment is open. The existing rubric gives 25 points for schema and integrity, 25 for transactions and blocking, 20 for one improvement, 15 for recovery, and 15 for documentation. The midterm is individual and worth 30 percent of the course grade.

Students may use the supplied setup and their own Week 5 observations. They add their requester join and commit example, record actual results, and explain one improvement. Recovery is taught in Week 8. An additional executed midterm restore is optional. Use the full assignment for requirements and Brightspace for the deadline.

## Slide 3

Open the actual starter. Its three tables contain eight users, twelve tickets, and twenty-one events. It resets midterm_metro and dependent objects, so it belongs in a personal practice database. Today's notebook does not run that reset; it embeds the starter CSVs for inspection.

Show the provided rollback on ticket 1004, the commit TODO, and the index comparison. Show where each result will go in the final README. Explain that the index may not change the plan on twelve rows. Students must report what their PostgreSQL test actually does.

Spend time on questions and examples of acceptable evidence. You do not need to perform the whole midterm live.

## Slide 4

Today's lab has one submission: Lastname_Week07_Research.ipynb with code outputs, the observation table, and 180 to 250 words across three response cells. Students inspect data, read two short official documentation excerpts, and propose one PostgreSQL test. They can reuse the writing in their final README after testing their predictions.

The final midterm remains midterm.sql and README.md in one ZIP. Today's notebook is classwork and does not replace those files. Students download their notebook with File > Download > Download .ipynb. There is no separate writing document or Colab sharing-link submission.

## Slide 5

Use 0 to 10 minutes for the case and files, 10 to 30 for the five project parts, 30 to 40 for the rubric and evidence examples, and 40 to 45 for questions and opening Colab. The lab then gives ten minutes to data, ten to reading, twenty-five to writing, and five to review. Save and submit in the last five minutes.

The notebook includes the data and ready-to-run code. Students change the status from open to new and record the ordered IDs. Their writing connects two data observations with the sources and a planned test. A prediction must be labeled as such. PostgreSQL testing and the recovery plan follow in the project.

Sources for the lab: https://www.postgresql.org/docs/15/indexes-intro.html and https://www.postgresql.org/docs/15/indexes-ordering.html. Original instructional content by Atilio Barreda, CC BY-NC-SA 4.0; original code MIT; synthetic data CC0.
