# Week 3: Build a Dependable PostgreSQL Schema

## The Week's Question

How can a schema protect meaning while remaining inspectable and reproducible?

## What You Will Be Able to Do

- retrieve and apply cumulative SQL skills before new administration work;
- inspect schemas, columns, constraints, and indexes through metadata;
- choose data types, nullability, primary keys, and foreign keys;
- reject bad states with named constraints; and
- distinguish an integrity rule from an access structure.

## Read and Use

- [Module 3: A schema protects meaning](../textbook/module_03_schema.md)
- [Metro Support setup](../datasets/metro_support/postgres_setup.sql)
- [Week 3 student deck](week_03_schemas_constraints_evidence.pptx)
- [Week 3 PDF handout](week_03_schemas_constraints_evidence.pdf)
- [Week 3 transcript](week_03_schemas_constraints_evidence_transcript.md)

## Day 1: Cumulative SQL Clinic and Schema X-Ray

We begin with cumulative SQL retrieval rather than assuming the review is
finished. Then we query `information_schema` and PostgreSQL catalogs to compare
the schema we think exists with the schema the server actually stores.

Complete [Lab 1: SQL clinic and schema X-ray](lab_01_sql_clinic_schema_xray.md).

Submit only `week_03_schema_xray.sql`.

## Day 2: Make Invalid States Impossible

We audit `status`, `priority`, timestamps, and relationships, then add named
constraints and one workload-driven index candidate. Expected errors become
evidence when they show a bad state was rejected for the intended reason.

Complete [Lab 2: Reject bad states](lab_02_integrity_constraints.md).

Submit only `week_03_integrity_build.sql`.

## Optional Industry Extension: Real-Data Contract Review

This activity is optional, ungraded, and does not add a submission.

Open the included [CISA KEV teaching sample](../datasets/cisa_kev_sample/README.md)
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
