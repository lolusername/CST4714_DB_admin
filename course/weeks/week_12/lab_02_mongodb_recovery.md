# Lab 2: Recover the Documents and Their Rules

A recovery check reports the correct ticket count, IDs, and date types. One
subject is still wrong. Find what those checks missed, recover that document
from the saved artifact, and distinguish its values from the collection's rules.

Work individually in class. Submit one completed notebook.

## 1. Restore and Repair One Ticket

Download [MongoDB Logical Recovery](../../notebooks/05_mongodb_logical_recovery.ipynb)
and upload it in [Colab](https://colab.research.google.com/) through **File > Upload
notebook**. Run in order.

The default local path needs no account. For Atlas, follow the notebook's pause
to add the Colab runtime's temporary `/32` IP rule before entering a hidden URI.
Both paths use fresh source and restore names. The notebook never asks you to
change an existing project collection or trigger a failover.

Inspect the canonical Extended JSON file, then restore it to the new target.
Compare the date representation, expected IDs, and complete document values.
Choose ticket 1001 or 1004 for the supplied incorrect-migration case. In **Your
Repair**, select its saved document, run the replacement, and confirm that all
five documents match the artifact again. Rerun the repair to check that it does
not create an extra ticket. The code around your change is provided and explained.

Continue through the rule-reconstruction cells. Both paths test the unique ticket
key. Atlas also tests the server validator; local mode supplies a clearly labeled
trace for that unsupported feature. Observe what the notebook must rebuild
**separately** from the document file.

## 2. Make a Recovery Recommendation

In the notebook's final explanation, answer this practical question:

> If a colleague handed you only this JSON file, what could you recover, and what
> else would you ask for before reopening the application?

Use the incorrect-subject result to explain why count and type checks alone were
insufficient. Identify an index or validator that would be missing without the
separate reconstruction step. Explain one difference from
the PostgreSQL archive you used in Week 8. Read the supplied tool-comparison
table, but do not write a second table or five-check report.

A JSON file is useful logical data recovery, not a complete Atlas project backup.
The notebook links the official `mongodump`/`mongorestore` guidance for database-level
recovery.

Run cleanup and remove any temporary Atlas network rule. Remove the printed
runtime-IP output before submission. Keep the synthetic data and query outputs.

**Submit:** the notebook with outputs and your recovery recommendation. No separate
report or exported-data attachment is required.
