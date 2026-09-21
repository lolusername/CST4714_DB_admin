# Lab: Can This Dataset Support a Useful Database?

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_13/lab_01_public_data_integration.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_13/materials/notebooks/06_public_data_capacity_integration.ipynb)

A list of vulnerabilities is easy to download. Turning it into a useful database
requires decisions about identifiers, dates, trustworthy sources, and the question
the data can actually answer. Investigate a bounded public dataset before adding
more infrastructure.

Work individually in class across the week's meetings. Submit one notebook.

## 1. Inspect the Data and Its Shape

Click **Open in Colab** above and save a working copy in Drive. The
[downloadable notebook](materials/notebooks/06_public_data_capacity_integration.ipynb) also supports local Jupyter.
Start with the embedded CISA teaching snapshot so everyone can reproduce the
same results. The live-feed
option is available after you understand the snapshot.

Run **Sections 1 and 2** of the notebook. Read the source date: this is a historical
teaching subset, not current guidance for deciding whether a real system is safe.
Choose one grouped question, such as which vendors appear most often **in this
subset**. Explain why that is not a ranking of all vendors' security quality.

The notebook compares candidate distribution keys. Concentrate on **vulnerability
ID versus date added**. Use two displayed measurements to explain their different
behavior and whether a small classroom database needs sharding at all. The range
and hash demonstration is a simulation, not a benchmark of an Atlas sharded
cluster. Other candidate keys are optional exploration.

Keep this notebook for Day 2. There is no separate Day 1 submission.

## 2. Load, Rerun, and Explain

In **Section 3**, set `TARGET` to `"sqlite"`, `"atlas"`, or `"postgres"`.
Only one target is required. SQLite needs no database account or package download.
Cloud connections use hidden prompts, an Atlas runtime-IP rule or Supabase
session-pooler URI where needed, and unique practice objects. If you want to try a
second target, clean up the first run before starting another.

Run the import cell twice **without rerunning the setup cell that generates
names**. Verify that the stable vulnerability ID prevents duplicate logical
records. Run the known-record comparison and the vendor grouping. Then change
`GROUP_FIELD` from `"vendorProject"` to `"product"` and rerun that cell. Explain
what one result row means now. The notebook compares the database grouping with
the checked source and checks all eight selected fields for one known ID.

Write a short maintenance handoff in the notebook's **Submission Record**. Explain
your question, key choice using two displayed measurements, repeat-run result,
one verification result, and one limitation. Use the changed product row as your
concrete example. The audience is an imagined future maintainer; you still work
individually. The final-project transfer prompts are for discussion, not an
additional written deliverable. Run cleanup when finished, including removing a
temporary Atlas runtime-IP rule if you added one.

**Submit in Brightspace:** the completed notebook with the changed query, output,
and handoff. Check that no credential appears in saved code or output.
No separate dataset report, sharding matrix, repository, or screenshot is required.
