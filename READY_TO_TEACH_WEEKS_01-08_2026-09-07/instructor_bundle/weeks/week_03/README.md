# Week 3: Build a Dependable PostgreSQL Schema

## The Week's Question

How can a schema protect meaning while remaining inspectable and reproducible?

## What You Will Be Able to Do

- retrieve and apply cumulative SQL skills before new administration work;
- inspect schemas, columns, constraints, and indexes through metadata;
- choose data types, nullability, primary keys, and foreign keys;
- reject bad states with named constraints; and
- distinguish an integrity rule from an access structure.

## Before Class: Assigned Reading

Use [Chapter 3: A Schema Protects Meaning](../../textbook/module_03_schema.md).

- **Before Day 1:** read from **"Schema" Has Two Related Meanings** through **Keys Identify and Connect Facts**, then **Inspect Metadata Instead of Guessing**. Connect the design rules to the columns and relationships we inspect in class.
- **Before Day 2:** read **Constraints Reject Invalid States**, **An Index Is an Access Structure, Not the Rule Itself**, and **Worked Example: Audit the Metro Support Baseline**. Study how an allowed-value rule accepts one change and rejects another.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Metro Support setup](../../datasets/metro_support/postgres_setup.sql)
- [Week 3 student deck](week_03_schemas_constraints_integrity.pptx)
- [Week 3 PDF handout](week_03_schemas_constraints_integrity.pdf)
- [Week 3 transcript](week_03_schemas_constraints_integrity_transcript.md)

## Day 1: Cumulative SQL Clinic and Schema X-Ray

Use **slides 1-11**. We work through a category report that counts both all tickets
and resolved tickets, including categories with no resolutions. Then we review
schema names, data types, keys, and why one current contact fact belongs in one
place. We query `information_schema` and PostgreSQL catalogs to compare the
intended design with the definitions the server actually stores.

Complete [Lab 1: SQL clinic and schema X-ray](lab_01_sql_clinic_schema_xray.md).

Submit only `week_03_schema_xray.sql`.

## Day 2: Prevent Misspelled Statuses

Use **slides 12-20**. The live example inspects priority values, adds a named
`CHECK`, and demonstrates a rejected change followed by an accepted change and
rollback. The lab adapts that example to status. We also distinguish what a
`CHECK` permits from what `NOT NULL` requires. Index experiments come in Week 7.

Complete [Lab 2: Reject bad states](lab_02_integrity_constraints.md).

Submit only `week_03_integrity_build.sql`.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

## Optional Industry Extension: Real-Data Contract Review

This activity is optional, ungraded, and does not add a submission.

Open the included [CISA KEV teaching sample](../../datasets/cisa_kev_sample/README.md)
and select four fields from the real public-data record. Propose a PostgreSQL type,
nullability rule, and one justified constraint for each. Then invent one bad row
that each rule should reject. Do not claim that your proposed constraints are
CISA's production schema; they are a consumer-side contract for one clearly
stated application, such as a vulnerability-remediation queue.

## End-of-Week Self-Check

Explain why each pair is different:

- schema definition versus current data;
- primary key versus foreign key;
- `NULL` versus an empty string;
- constraint versus index; and
- application validation versus database integrity.
