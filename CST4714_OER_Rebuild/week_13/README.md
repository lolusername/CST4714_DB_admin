# Week 13: Capacity, Sharding, and Python Integration

## The Week's Question

When growth changes a workload, what should we measure before scaling, and how can
Python load a small public dataset without hiding connection or data-quality
decisions?

## What You Will Be Able to Do

- state a measurable capacity and growth assumption;
- compare tune, scale up, replica, partition, and shard options;
- evaluate shard-key cardinality, frequency, monotonicity, and targeting;
- connect from Python without saving credentials;
- inspect and load a small, licensed public-data subset; and
- turn the notebook into final-project inspiration or a skill checkpoint.

## Course OER

- [Module 13: Scale changes the questions a system must answer](../textbook/module_13_scale.md)
- [Public data, shard-key, and cloud import notebook](../notebooks/06_public_data_capacity_integration.ipynb)
- [Open the notebook in Colab](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/CST4714_OER_Rebuild/notebooks/06_public_data_capacity_integration.ipynb)
- [Week 13 student deck](week_13_scale_integration.pptx)
- [Week 13 PDF handout](week_13_scale_integration.pdf)
- [Week 13 transcript](week_13_scale_integration_transcript.md)

## Free External Data

The notebook uses the U.S. Cybersecurity and Infrastructure Security Agency's
Known Exploited Vulnerabilities catalog through its public JSON feed. The notebook
includes a small offline fixture and records the source and retrieval date.

## Day 1: Evaluate Distribution Without Pretending to Shard

Atlas Free cannot create a sharded cluster. We use open Python code to measure
candidate key cardinality, frequency, monotonicity, and simulated range/hashed
distribution. Students make a design recommendation without claiming a paid
deployment.

## Day 2: Connect, Load, Verify, and Reuse

Students choose Atlas, Supabase/PostgreSQL, both, or the offline SQLite path. The notebook
loads a small verified subset and runs one useful query on each chosen target.

Complete [Lab: Public data capacity and cloud integration](lab_01_public_data_integration.md).

Submit only the completed `06_public_data_capacity_integration.ipynb` notebook.

## Optional Industry Extension: KEV Patch-Priority Briefing

This activity is optional, ungraded, and does not add a submission.

Use the included real CISA KEV sample to identify one vendor or product group that
appears repeatedly and one due-date or ransomware-use pattern worth investigating.
Create one grouped query, verify one group against raw records, and write a
four-sentence briefing for a vulnerability-operations lead. End with one data
limitation and one index or partitioning decision that would depend on the real
production query volume rather than this 75-record teaching sample.

## End-of-Week Self-Check

Explain why high cardinality alone does not make a good shard key and why a
successful insert count alone does not make a trustworthy import.
