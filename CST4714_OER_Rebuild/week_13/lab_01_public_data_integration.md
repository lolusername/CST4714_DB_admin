# Lab: Public Data Capacity and Cloud Integration

## Purpose

Inspect a small cybersecurity dataset, test candidate distribution keys, and load
verified records into one course platform through a simple Python client.

This is individual work completed in class across the week's meetings. Submit one
notebook.

## 1. Inspect Before Loading

Open [`06_public_data_capacity_integration.ipynb`](../notebooks/06_public_data_capacity_integration.ipynb).

Use the live CISA feed or bundled offline fixture. Record:

- source, retrieval date, and data-use note;
- record count and selected fields;
- nulls, duplicate vulnerability IDs, and date types;
- one question the subset can answer; and
- why the selected subset is small enough for class and a free service.

## 2. Evaluate Candidate Keys

Use the notebook to compare vendor/project, date-added, vulnerability ID, and a
compound candidate. For each, interpret cardinality, high-frequency values,
monotonicity, and which queries could target it.

Run the deterministic range and hashed distribution simulation. Recommend one
candidate or recommend not sharding yet. Cite evidence and one tradeoff.

## 3. Load and Verify One Platform

Choose one required path:

- Atlas with PyMongo;
- Supabase/PostgreSQL with Psycopg;
- both for an explicitly different ownership experiment; or
- offline SQLite when cloud access is blocked.

Enter cloud URLs through `getpass`. Load records idempotently using the
vulnerability ID, verify expected and observed counts, query one known identifier,
and run one grouped question. Explain what those checks do not prove.

The notebook's final-project checkpoint asks whether this dataset/model idea fits
your project. It does not redefine the [canonical final project](../final_project.md).

## Submit One Thing

Submit the completed notebook after confirming that no URI, password, or API key
appears in cell source or output.
