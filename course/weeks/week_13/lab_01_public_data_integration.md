# Lab: Can This Dataset Support a Useful Database?

A list of vulnerabilities is easy to download. Turning it into a useful database
requires decisions about identifiers, dates, trustworthy sources, and the question
the data can actually answer. Investigate a bounded public dataset before adding
more infrastructure.

Work individually in class across the week's meetings. Submit one notebook.

## 1. Inspect the Data and Its Shape

Download [Public Data, Capacity, and Cloud Integration](../../notebooks/06_public_data_capacity_integration.ipynb)
and upload it in [Colab](https://colab.research.google.com/). Start with the embedded
CISA teaching snapshot so everyone can reproduce the same results. The live-feed
option is available after you understand the snapshot.

Run the source and quality checks. Read the source date: this is a historical
teaching subset, not current guidance for deciding whether a real system is safe.
Choose one grouped question, such as which vendors appear most often **in this
subset**. Explain why that is not a ranking of all vendors' security quality.

The notebook compares candidate distribution keys. Concentrate on **vulnerability
ID versus date added**. Use two displayed measurements to explain their different
behavior and whether a small classroom database needs sharding at all. The range
and hash demonstration is a simulation, not a benchmark of an Atlas sharded
cluster. Other candidate keys are optional exploration.

## 2. Load, Rerun, and Explain

Use SQLite first or choose your own Atlas/Supabase project. Only one target is
required. Cloud connections use hidden prompts, an Atlas runtime-IP rule or
Supabase session-pooler URI where needed, and unique practice objects.

Run the import cell twice **without rerunning the setup cell that generates
names**. Verify that the stable vulnerability ID prevents duplicate logical
records. Change the grouped question and compare one known ID with its source
record.

Replace the final submission prompts with a short explanation of your question,
key choice, repeat-run result, and one limitation. The project's transfer prompts
are a conversation starter during project work, not an additional written
deliverable. Run cleanup when finished.

**Submit:** the completed notebook with the changed query, output, and explanation.
No separate dataset report, sharding matrix, repository, or screenshot is required.
