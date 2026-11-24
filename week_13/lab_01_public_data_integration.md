# Lab: Import Once, Repeat, and Change the Question

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_13/lab_01_public_data_integration.md)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_13/materials/notebooks/06_public_data_capacity_integration.ipynb)

**Week 13 has one 100-minute Thanksgiving-week meeting.** Work individually. The lab below is **20 minutes after the instructor-guided setup and examples**. Use the same saved notebook throughout and submit one viewable Colab link. Use Atlas for this lesson.

## 1. Follow the guided setup and example

Save your own copy of the [notebook](materials/notebooks/06_public_data_capacity_integration.ipynb) in Drive. Use the [data reference](DATA_REFERENCE.md) to inspect the fields in one catalog entry. Keep `USE_LIVE_FEED = False` so the supplied 75 records and measurements are reproducible.

Follow **Cells 01, 02a–02b, 03–06, 07a and 07** with the instructor. Inspect the source and data checks; compare CVE-ID and date-added measurements. Cell 07 simulates range and hash placement in Python.

In **Cell 08**, keep `TARGET = "atlas"`. **Cell 10** prints the runtime IPv4 address, pauses for its temporary `/32` access-list rule, and then reads the hidden URI or allowed Colab secret. Use your own Free cluster and database user scoped to `cst4714_week13`. Keep credentials out of code/output. Do not enable a paid feature or access from everywhere.

After successful setup, run **Cell 11 twice into the same collection**. Expect **0 → 75 → 75** records. Do not rerun Cell 08 between imports. Run **Cell 14** to compare all records, fields and types with the source. The instructor first demonstrates **Cell 15** with vendor grouping. These steps happen before the individual lab timer starts.

## 2. Your 20-minute task

1. Change Cell 15's `GROUP_FIELD` from `"vendorProject"` to `"product"`.
2. Rerun that cell. Check that its database output matches the independent source calculation. Read what one product row counts.
3. Write **5–7 sentences** in the notebook's **Submission Record**. Identify the historical source; use one measured comparison of CVE ID and date added; explain both imports into the same collection; interpret one changed product row; name a value/group verification and one remaining limit.

Keep your own wording and actual outputs. Ping checks connectivity. Comparing all 75 records with the source checks the import. Each product group counts the selected catalog entries for that product. If you watched the instructor's demonstration, identify which results you observed.

## 3. Submit one saved Colab link

Save the changed query, both import outputs, verification and handoff in your own Drive copy. Use Share to grant the instructor viewer access. **Submit that copy's viewable Colab URL in Brightspace**, using the existing due date. Check that no credential appears in the saved notebook.

Keep cleanup disabled until your evidence is saved. Cell 16 can then remove only this run's practice collection and close the connection; remove the temporary runtime IP rule when no longer needed. SQLite (09), PostgreSQL (12–13), live-feed exploration and extra project prompts are optional and ungraded here. If setup takes longer, continue in the same notebook under the course's technical-problem policy.
