# Lab: Backup, Restore, and Prove It

## Purpose

Perform a real logical backup and restore in a free, isolated PostgreSQL
environment, then connect that evidence to a Supabase recovery runbook.

This is individual work completed in class. Submit one notebook.

## 1. Run the Isolated Recovery Notebook

Open [`03_postgres_backup_restore.ipynb`](../notebooks/03_postgres_backup_restore.ipynb)
in Colab. The notebook uses a temporary local PostgreSQL service, so it does not
need a cloud password and cannot overwrite your Supabase project.

Run the ordered cells that:

- create a source database and Metro Support schema;
- record source structure and row counts;
- create a custom-format `pg_dump` artifact;
- inspect its table of contents and checksum;
- create a separate empty restore database;
- restore with errors treated as failures; and
- verify structure, data, relationships, one report, and one expected constraint
  failure.

Do not skip directly to the final output. The evidence sequence is the lab.

## 2. Complete the Recovery Record

In the notebook's final Markdown prompts, state:

- failure scope;
- artifact type and location;
- source and restore target names;
- at least five verification checks;
- one thing the checks do not prove; and
- how the procedure would change for a Supabase source connection without placing
  its URL in the notebook.

Use the current Supabase backup and connection documentation linked in Module 8.

## Submit One Thing

Submit the completed notebook. Before submitting, confirm that every required cell
has output, no cell contains a real connection string, and the source and restore
database names are visibly different.
