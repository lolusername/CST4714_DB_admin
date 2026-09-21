# Week 13: Capacity, Sharding, and Python Integration

## The Week's Question

When growth changes a workload, what should we measure before scaling, and how can
Python load a small public dataset without hiding connection or data-quality
decisions?

## What You Will Be Able to Do

- state a measurable capacity and growth assumption;
- compare tune, scale up, replica, partition, and shard options;
- evaluate shard-key cardinality, frequency, monotonicity, and targeting;
- connect from Python while keeping credentials out of code and submitted output;
- inspect and load a small, licensed public-data subset; and
- turn the notebook into final-project inspiration or a skill checkpoint.

## Before Class: Assigned Reading

Use [Chapter 13: Scale Changes the Questions a System Must Answer](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read the capacity and distribution sections through **Worked Example: Evaluate Metro Support Candidates**, plus **Inspect the Public Source Before Loading It** and the storage projection in **Scaling Also Scales Operations**.
- **Before Day 2:** read the Python connection, parameterized-query, and repeat-import explanations. The notebook provides complete setup; only one database path is required.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Public data, shard-key, and cloud import notebook](materials/notebooks/06_public_data_capacity_integration.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_13/materials/notebooks/06_public_data_capacity_integration.ipynb) for Lab 1; save a working copy in Drive.
- [Week 13 student deck](week_13_scale_integration.pptx)
- [Week 13 PDF handout](week_13_scale_integration.pdf)
- [Week 13 transcript](week_13_scale_integration_transcript.md)
- [Individual lab for both meetings](lab_01_public_data_integration.md)

## Free External Data

The notebook uses the U.S. Cybersecurity and Infrastructure Security Agency's
Known Exploited Vulnerabilities catalog through its public JSON feed. The notebook
includes a small offline fixture and records the source and retrieval date.

## Day 1: Evaluate Distribution Without Pretending to Shard

Use **slides 1-16**. We distinguish latency from throughput, calculate a small
latency percentile, and compare replication, partitioning, and sharding. We then
use Notebook 06's Sections 1 and 2 to inspect the source and measure candidate
keys. The range/hash experiment makes placement visible without deploying a
sharded cluster. Atlas Free does not provide that deployment.

Begin Part 1 of the individual lab. Compare CVE identifier with date added and
explain whether either fits the question you want to answer. Save the same
notebook for Day 2; there is no separate Day 1 submission.

## Day 2: Connect, Load, Verify, and Reuse

Use **slides 17-32**. We read the connection and import code, distinguish
transaction atomicity from repeat behavior, and examine a wrong stored value
that a correct row count would miss.

Complete Part 2 of the [individual lab](lab_01_public_data_integration.md). Set
`TARGET` to `"sqlite"`, `"atlas"`, or `"postgres"`; **one path is required**.
SQLite uses Python's built-in database and the embedded data. The cloud paths
install their driver only when selected. To try another path, clean up the first
run before starting a new one.

Repeat the chosen import against its existing output, change the grouping from
vendor to product, and compare the result with the source. Write the short
maintenance handoff in the notebook, then clean up the practice objects.

Submit only the completed `06_public_data_capacity_integration.ipynb` notebook in
Brightspace. The handoff practices explaining a data pipeline to a future
colleague; it does not require a partner or another document.

## Optional Industry Extension: A Catalog Question

This activity is optional, ungraded, and does not add a submission.

Try a date-window question in the historical sample and check a matching record
directly. Discuss which index or placement rule could help that query under a
larger measured workload. Do not use the subset to declare a real system safe,
rank vendor security, or decide a current patch deadline. No additional writing
or final-project deliverable is required.

## End-of-Week Self-Check

Explain why high cardinality alone does not make a good shard key and why a
successful insert count alone does not make a trustworthy import.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
