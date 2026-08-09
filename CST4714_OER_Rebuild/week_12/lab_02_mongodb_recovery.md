# Lab 2: MongoDB Logical Recovery Evidence

## Purpose

Create a transparent collection-level logical export, restore it to a different
database, and verify the result while accurately stating what the artifact omits.

This is individual work completed in class. Submit one notebook.

## 1. Run the Recovery Notebook

Open [`05_mongodb_logical_recovery.ipynb`](../notebooks/05_mongodb_logical_recovery.ipynb)
in Colab.

- Atlas path: enter the URI through `getpass`, create a uniquely named source and
  restore database, and remove temporary network access after class.
- Offline path: use the in-memory fixture to execute the same export, restore, and
  verification sequence.

The notebook writes canonical Extended JSON to a runtime file, records size and
SHA-256, restores to a different collection, and verifies counts, identifiers,
types, one query, and one expected validation failure.

## 2. Compare With `mongodump`

Complete the notebook table comparing the educational JSON artifact with
`mongodump`/`mongorestore` for:

- BSON type fidelity;
- collection options and validators;
- index definitions;
- multi-collection consistency;
- Atlas users/network configuration; and
- compatibility requirements.

The JSON exercise is real logical recovery practice, but it must not be mislabeled
as a complete database backup.

## 3. Complete the Evidence Record

Name the source, separate restore target, artifact, five checks, limitation, Atlas
Free constraint, and production next step. Confirm that no URI appears in source
or output.

## Submit One Thing

Submit the completed notebook.
