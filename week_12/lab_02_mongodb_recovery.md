# Week 12 Lab: Recover One Ticket in Atlas

[Open in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_12/materials/notebooks/05_mongodb_atlas_recovery.ipynb)

**One class, one lab, one submission.** Work individually. Allow about **20 minutes after the guided Atlas setup**. The instructor demonstrates Cells 01–06; you change one line in Cell 07, run Cell 08, and write 3–4 sentences in Section 09.

## Before the repair

Save a copy of the required Atlas notebook in Drive. Use a database user to authenticate Python and the runtime's IP address to allow the network connection. Keep credentials in the hidden input or Colab Secrets. Do not purchase anything or use an unrestricted IP rule.

The [data reference](DATA_REFERENCE.md) lists all five records. In Cell 04, confirm that Atlas has the five source tickets, including 1004 with subject **Broken bench slat**. Cell 05 saves a BSON-aware Extended JSON artifact; Cell 05b retains it outside the temporary runtime. Cell 06 restores elsewhere and intentionally changes only target ticket 1004. Count, IDs, and date types still pass, while the complete-values check fails.

## Your one-line change

In **Cell 07**, replace `None` with the lookup for ticket 1004 in `saved_by_id`. Recover the saved document; do not type a guessed subject. Run the cell, then **Cell 08**. The repeat should show matched **1**, modified **0**, and **5** tickets, with all value checks passing. Refresh the target in Atlas Data Explorer and check the repaired subject.

## Explain what the evidence establishes

In Section 09, write 3–4 sentences covering the real connection/write-read evidence, the error missed by counts, recovery from the saved artifact, and why replicated copies alone do not supply an earlier value. Name one thing the document file does not reconstruct, such as an index, validator, or application configuration.

**Validation is not required for this lab.** No server election, index reconstruction, or paid backup exercise is required. The older Lab 1 policy response provides optional practice.

## Submit your saved Colab link

Save outputs and your explanation. Give the instructor viewer access through **Share**, then paste your own saved Colab notebook URL into Brightspace. Check that the instructor can open it. **Submit your saved Colab link.** If you observed the instructor's demonstration, label the results as observations.
