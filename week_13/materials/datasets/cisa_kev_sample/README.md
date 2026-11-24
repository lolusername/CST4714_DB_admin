# CISA Known Exploited Vulnerabilities Teaching Sample

This package is a small, versioned subset of the U.S. Cybersecurity and
Infrastructure Security Agency's Known Exploited Vulnerabilities catalog. It is
used to practice data-source evaluation, JSON/CSV inspection, idempotent import,
aggregation, capacity reasoning, and candidate shard-key analysis.

## Files

- `kev_sample.json`: source metadata plus 75 selected vulnerability records.
- `kev_sample.csv`: the same selected fields in a flat format; CWE arrays use `|`
  as the within-cell separator.

## Transformation

`tools/build_datasets.py` retrieves the official JSON feed, selects the first 75
records in source order, and keeps only:

- CVE ID;
- vendor/project;
- product;
- vulnerability name;
- date added;
- due date;
- known ransomware campaign use; and
- CWE list.

The snapshot metadata records the source catalog version, source release time,
retrieval time, URL, and selection. Descriptions, remediation text, and notes are
omitted to keep the classroom fixture compact. For current vulnerability-management decisions, consult the live CISA catalog.

## Source and Use

Official feed:
<https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>

CISA provides the catalog as public U.S. government information. Review the
current [KEV catalog and its license notice](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
before redistribution. Course-authored transformation code is MIT licensed; this
README is CC BY-NC-SA 4.0. Source data retains applicable U.S. government terms.

## Safety

The catalog identifies publicly known vulnerabilities. Use the snapshot for the classroom exercises above.
