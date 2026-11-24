# Week 13: A Repeatable Public-Data Import into Atlas

## The week's question

If we import the same dataset again, do we recognize the same records or create duplicates? Use a small historical CISA catalog sample to connect from Python, load records by a stable identifier, and verify both values and grouped results.

**Week 13 is the Thanksgiving week: one 100-minute class.** Use the required Atlas route below. The individual lab takes **20 minutes after guided setup and examples**. Students work quietly in their own saved Colab copy and submit **one viewable Colab link** in Brightspace. No additional report or worksheet.

## Before the single class

**Before the single meeting:** read [Chapter 13: Scale Changes the Questions a System Must Answer](../Operating_Cloud_Databases.pdf), focusing on capacity and distribution, **Inspect the Public Source Before Loading It**, the Python connection, and repeat-import explanations. Read the [textbook corrections](../COURSE_CORRECTIONS.md) with it. Use the reading to prepare for the guided example.

Prepare access to your own MongoDB Atlas **Free** cluster and a database user with `readWrite` on **cst4714_week13**. This user is separate from your Atlas website login. Keep the Drivers URI private. The notebook discovers the current Colab runtime's IPv4 address and pauses so you can add its temporary `/32` rule. Choose the Free tier and allow only that runtime address. Setup time is outside the 20-minute lab.

## Class materials

- [Required Atlas notebook](materials/notebooks/06_public_data_capacity_integration.ipynb)
- [Open the required notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_13/materials/notebooks/06_public_data_capacity_integration.ipynb); save your own copy in Drive.
- [PowerPoint](week_13_scale_integration.pptx), [PDF](week_13_scale_integration.pdf), and [spoken transcript](week_13_scale_integration_transcript.md).
- [Short individual lab](lab_01_public_data_integration.md).
- [Complete data reference](DATA_REFERENCE.md) and [retained JSON/CSV source files](materials/datasets/cisa_kev_sample/README.md).

## One 100-minute meeting

| Minutes | What happens | Exact notebook route |
|---|---|---|
| 0–10 | Understand one catalog entry and the Colab/Python/PyMongo/Atlas roles | 01, 02a, 02b; open the data reference |
| 10–25 | Inspect the source and compare two ways of assigning entries to buckets | 03–06, then **07a** (one ID) and **07** (15 arrivals) |
| 25–50 | Choose one target, allow the runtime IP, connect and ping | 08 with TARGET=atlas; 10 |
| 50–65 | Import twice into the same collection, read back all fields and inspect vendor groups | 11 twice; 14; 15 with vendorProject; Atlas Data Explorer |
| 65–85 | Individual product grouping and 5–7 sentence handoff | Change Cell 15; Submission Record |
| 85–100 | Career connection, limits, saving and sharing | Submit one viewable saved Colab link |

Keep `USE_LIVE_FEED = False`. Use Cells **01, 02a–02b, 03–08, 10, 11 twice, 14 and 15**. Skip **09, 12 and 13**, which are optional SQL paths. Cell 16 is optional cleanup after retaining evidence. Supplied setup code can stay collapsed; it still needs to run. Run each numbered cell in sequence so you can respond to the connection prompt.

The expected record counts are **0 → 75 → 75**, with the same collection on both imports. Do not rerun the name-generating Cell 08 between them. Cell 14 independently reads all 75 records and compares all eight selected fields and their types with the source; it also displays one known record. Cell 15 compares the database grouping with a separate calculation from the source. Use the read-back comparison to verify the stored values.

## What to submit

In the 20-minute individual lab, change `GROUP_FIELD` from `"vendorProject"` to `"product"`, rerun its source comparison, and interpret one result. Write 5–7 sentences in **Submission Record** using the source limitation, one measured key comparison, the repeated import, the changed product result and its checks.

Save the changed code, outputs and handoff in your own Drive copy. Give the instructor viewer access and submit **that copy's Colab sharing URL in Brightspace**, using the existing due date. If access fails, label observed instructor evidence honestly and finish the same notebook under the course's existing technical-problem policy.

## Scope and optional practice

The retained data are the first 75 selected records from catalog version **2026.07.10**, retrieved **July 13, 2026**, with eight documented fields. Each record describes a vulnerability listed in the catalog. The source is historical and nonrandom. Read each count as a description of the selected entries. Labels and calendar-day strings are preserved; `cwes` remains an array in Atlas.

Cell 07's four buckets illustrate range/hash placement in Python. SQLite, PostgreSQL, the live feed and extra date-window questions remain optional later practice.

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 13 videos](videos/README.md).

- [Capacity: measure before you scale](videos/01_capacity_before_scaling.mp4) (1:17): Twenty invented requests average 93 ms while the 95th percentile is 500 ms. Then compare the scaling options by what each one leaves behind, and see why three replicas are copies while three shards are portions.
- [Shard keys: distribution and targeting](videos/02_shard_keys.mp4) (1:37): Using the 75-record CISA fixture, a ranged dateAdded key sends all 15 later records to the last range, while a hashed cveID spreads them 3, 3, 6, 3. Hashing cannot split a repeated value, and a query without the shard key goes to every shard.
- [A repeatable Python import](videos/03_repeatable_import.mp4) (1:28): A Python client connects with a hidden URI, TLS checks on, and timeouts, then imports by a stable key so a second run leaves 75 records instead of 150. A failed write shows the difference between a transaction's rollback and a rerunnable, per-document loop.

<!-- videos:end -->

## Industry/Career Connection — Discord: access patterns and hot partitions

Discord's 2023 engineering account describes message-storage growth, hot partitions, a data-service layer, and migration from Cassandra to ScyllaDB. Measure distribution and access patterns before selecting infrastructure, then verify the migrated values against the source. A data engineer should report the import key, repeat behavior, field checks, and remaining limits.

Read the [company's own account](https://discord.com/blog/how-discord-stores-trillions-of-messages).

## Notebook route and data

Read the [complete data reference](DATA_REFERENCE.md) before the first query. Notebook code cells now have stable numbered titles. Expand setup code when you want its mechanics; keep student changes and query results visible. The [static illustration and editable Manim source](illustrations/README.md) show the lesson's actual record relationships. Embedded PowerPoint videos and separate subtitle files remain available; the PDF and GitHub previews show still images.

## End-of-Week Self-Check

Name two properties you would check before choosing a shard key. Explain how you verified the imported values.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
