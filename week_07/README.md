# Week 7 Midterm Explanation and Preliminary Research

**One 100-minute meeting: 45 minutes explaining the midterm, 50 minutes of research and writing in Colab, and 5 minutes to save and submit.**

Today we walk through the Metro Support project and its rubric, then investigate the data and plan the index experiment.

**The midterm is a separate project, not today's notebook.** Everything about it is on one page: [midterm instructions](../week_08/materials/assignments/midterm_project.md). Today's Colab notebook is classwork with its own Brightspace link.

## Materials

- **[Midterm instructions: the whole midterm on one page](../week_08/materials/assignments/midterm_project.md)**
- [Midterm SQL starter](../week_08/materials/assignments/midterm_starter.sql)
- [Final README template](../week_08/materials/assignments/midterm_README_template.md)
- [Class slides](week_07_query_plans_index_design.pptx)
- [Slide handout](week_07_query_plans_index_design.pdf)
- [Transcript](week_07_query_plans_index_design_transcript.md)
- [Animation: When Does an Index Help? (1:45)](animations/index_usefulness/README.md)
- [Today's research lab](lab_midterm_research.md)
- [Colab notebook](07_midterm_preliminary_research.ipynb)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_07/07_midterm_preliminary_research.ipynb)

Open the notebook with the button above and choose **File > Save a copy in Drive**. The data and code are included. No Supabase connection or package installation is needed today. You can also download the notebook and use File > Upload notebook at [Colab](https://colab.research.google.com/).

<!-- videos:start -->
## Videos

Short silent animations with captions (6 for this week). Each has a subtitle file; see [all Week 7 videos](videos/README.md).

- [When does an index help?](videos/01_index_usefulness.mp4) (1:44): A last-name index finds two matching rows by looking up, then fetching. It cannot help a query with no WHERE clause or one on a different column, and every INSERT has to maintain it.
- [Reading a query plan](videos/02_reading_a_query_plan.mp4) (0:55): SQL describes the answer and the plan describes the work. Read the plan tree inside out and follow 100,000 rows down to 20, then compare EXPLAIN with EXPLAIN ANALYZE.
- [Selectivity: why a Seq Scan can beat an index](videos/03_selectivity.mp4) (1:07): Tables are read in pages. When 2% of the rows match, an index skips most pages. When 80% match, reading every page once is cheaper.
- [How a B-tree index finds rows](videos/04_btree_index.mp4) (0:58): Root, internal, and leaf pages narrow an equality search to a few page reads. Linked leaves serve ranges and ORDER BY, and the depth grows very slowly.
- [Composite indexes: column order matters](videos/05_composite_index.mp4) (1:08): An index on (status, opened_at DESC) answers "newest 20 open tickets" without a scan or a sort. Filtering on only its second column scatters the matches.
- [Testing an index hypothesis](videos/06_index_experiment.mp4) (1:03): Baseline, hypothesis, add index, remeasure, decide: the textbook's worked example, comparing plan shape, rows, sort, and buffers, and checking for the same answer.

<!-- videos:end -->

## Class schedule

| Minutes | Work |
|---|---|
| 0 to 10 | Explain the case, the two final files, and what the supplied starter already includes |
| 10 to 30 | Walk through the five project parts and the evidence each needs |
| 30 to 40 | Explain the rubric, show how the README records results, and distinguish observed results from predictions |
| 40 to 45 | Questions and opening the notebook |
| 45 to 55 | Inspect the supplied data in Colab |
| 55 to 65 | Read the two short documentation sections |
| 65 to 90 | Write 180–250 words and plan one PostgreSQL test |
| 90 to 95 | Review your observations and remaining question |
| 95 to 100 | Save your Colab copy and submit its sharing link |

## Today's submission and the completed midterm

Submit the **sharing link** to your saved Colab copy, **Lastname_Week07_Research**, for today's classwork. Use **Share** to give the instructor viewer access, and make sure the outputs and writing are saved in the copy. There is no separate writing document or index-lab SQL submission today. Reuse the research in your final README after testing your predictions.

The final midterm is individual, worth 30% of the course grade, and submitted as **midterm.sql** plus **README.md** in one ZIP. The notebook does not replace either final file. Recovery is taught in Week 8; use the final deadline posted in Brightspace.

The larger [index experiment](lab_single_session.md), advanced plan operators, and partial indexes are optional reference. They are outside today's required work. Today's Python results describe the CSV dataset; they do not prove how PostgreSQL will execute the query.
