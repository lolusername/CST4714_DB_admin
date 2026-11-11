# Lab 1: Count Requests Without Counting Them Twice

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_11/lab_01_pipeline_validation.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_11/materials/notebooks/07_aggregation_validation.ipynb)

A summary says there are three active requests. That sounds correct, but the
pipeline counted one request twice and lost another. Find out how a plausible
total can hide an incorrect result.

Work individually in class. Submit the **sharing link to your completed Colab copy** in Brightspace.

**Validation is not needed for this lab. We will cover it next week.** All
validator material is grouped into one collapsed section in the notebook.
Leave it collapsed and keep `RUN_VALIDATION = False` for this lab.

## 1. Build and Check the Summary

Click **Open in Colab** above and save a working copy in Drive. The
[downloadable notebook](materials/notebooks/07_aggregation_validation.ipynb) also supports local Jupyter.
Run the setup and aggregation sections in order, then write your explanation.
Skip the collapsed validation section. The notebook supplies its own four-ticket case;
nothing from Week 10 needs to be retained.

Keep local mode on, or use your personal Atlas practice project with the notebook's
hidden credential prompt and temporary runtime-IP instructions.

The worked pipeline counts active tickets by category. Add **urgent count** and
**newest opening date**, using the supplied expressions. Inspect the actual ticket
IDs to check the streetlight result. Then run the `$unwind` example and explain
why its rows answer a different question. A matching grand total is insufficient.

## 2. Explain the Aggregation Result

Complete the notebook's one explanation cell: your streetlight result and its
source IDs, plus why unwound rows count events rather than tickets. Explain why
the matching totals do not prove the reports counted the same things. Run cleanup
when finished. No validator change, date tests, or validation explanation is
needed for this lab.

## 3. Submit Your Colab Link

Save your completed copy with the modified aggregation pipeline, outputs, and
short explanation. In Colab, choose **File > Save**, then **Share** and give the
instructor **viewer access**. Copy the sharing link and paste it into the
Brightspace Lab 1 submission.

Submit the link to **your saved copy**, not the starter notebook’s GitHub or
Colab link. If you worked in local Jupyter, upload your completed notebook to
Colab first, save it, and submit its sharing link through the same process.
**Do not upload an `.ipynb` file to Brightspace.** No JavaScript file, repository,
screenshot, or extra report is required. Assignee sets and event analytics are
optional extensions.

<details>
<summary>Validation — not needed for this lab; we will cover it next week</summary>

The notebook keeps the validator and its examples together for next week's
lesson. The supplied rule allows optional fields but requires a valid ticket ID,
status, and subject. The later example adds a required BSON `opened_at` date and
compares an allowed date, an invalid status, a date stored as text, and a missing
date. Atlas can enforce the rule; local mode provides an explicitly labeled
trace to interpret. That trace is not a live server test.

Leave this material for next week. It is not part of this lab's submission.

</details>
