# Lab 2: Recover One Ticket in 15 Minutes

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_12/materials/notebooks/05_mongodb_logical_recovery_short.ipynb)

A restored collection has five tickets, the right IDs, and real dates. One subject
is still wrong. Recover that one ticket from its saved document, then explain
why the first checks missed the problem.

**Time:** 15 minutes during the one-hour class. Work individually. The setup and
verification code are supplied. You change **one line** and write **2–3 sentences**.

## Open the Short Notebook

Open the Colab link above and save a copy in Drive. The
[short notebook](materials/notebooks/05_mongodb_logical_recovery_short.ipynb)
also runs in local Jupyter. Use its numbered code cells **01–07**.

This lab uses `mongomock`, an in-memory Python practice database with part of
MongoDB's API. Colab requires a Google sign-in. **No Atlas account, connection URI,
server setup, failover, or validator exercise is required today.**

## Follow the Seven Cells

| Time | Cells | What to do |
|---|---|---|
| 0–3 minutes | 01–02 | Run the supplied packages and fresh five-ticket fixture. |
| 3–7 minutes | 03–05 | Save Extended JSON, restore to a separate target, and inspect the wrong subject on ticket **1004**. |
| 7–11 minutes | 06–07 | Replace the `None` placeholder with the saved-document lookup, then repeat the repair and verify the result. |
| 11–15 minutes | Explanation and submission | Write 2–3 sentences, save, and submit your shared Colab link. |

In Cell 05, count, IDs, and date-type checks still pass, but the complete-values
check fails. The saved subject is **Broken bench slat**. The target has a different
subject. Repair it from the saved document instead of typing a replacement
subject by hand.

After Cell 06, all four checks should pass. In Cell 07 the repeated repair should
report **matched: 1**, **modified: 0**, and **5** tickets. Repeating the repair must
not append a sixth ticket. If the notebook reports **INCOMPLETE**, finish Cell 06
and rerun Cells 06–07.

## Explain the Recovery in 2–3 Sentences

In the notebook's **Your explanation** text cell, explain:

- why count, IDs, and date types could pass while a subject was wrong;
- how you recovered the correct document from the saved artifact; and
- one thing this document file does not restore before an application reopens,
  such as a unique index, validator, or application configuration.

The JSON file contains documents. It does **not** contain collection index or
validator definitions. You only need to recognize that limitation today; rebuilding
or testing a validator is **not required**. The artifact is saved in this temporary
practice runtime; a real recovery copy must be retained outside the system you
might lose.

## Submit

**Submit one shared, viewable Colab notebook link in Brightspace.**

Save the outputs and explanation in your Drive copy. In Colab, use **Share** to
allow your instructor to view it. Choose **Anyone with the link → Viewer** if your
account permits it, or explicitly share with your instructor as a viewer. Paste
the **shared Colab notebook URL** into the Brightspace lab submission and verify
that the instructor can open it.

**Do not submit an `.ipynb` attachment.** No separate report, exported JSON file,
Atlas screenshot, or additional writing assignment is required.

## Optional Longer Reference

The [original full notebook](materials/notebooks/05_mongodb_logical_recovery.ipynb)
and [extended lab instructions](reference_mongodb_recovery_extended.md) preserve the
longer index, validator, Atlas, and tool-comparison activities. They are optional
reference and are **not required for today's short lab**.
