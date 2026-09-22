# Week 6: Identity, Permissions, and Row-Level Security

## The Week's Question

How can we grant the access an application needs while denying access it should
not have?

## What You Will Be Able to Do

- separate identity, authentication, authorization, and auditing;
- create group roles and apply schema, view, and table privileges;
- test one allowed action and one denied action;
- explain Supabase Auth, PostgreSQL roles, token claims, and RLS as distinct layers;
  and
- build and test a beginner row-ownership policy.

## Before Class: Assigned Reading

Use [Chapter 6: Access Should Be Useful and Limited](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read through **Test Both an Allowed and a Denied Action**, plus the limited reporting-view worked example.
- **Before Day 2:** read the Supabase identity, row-security, secret-handling, and network-control sections. Distinguish database roles from individual application users.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Week 6 student deck](week_06_identity_permissions_rls.pptx)
- [Week 6 PDF handout](week_06_identity_permissions_rls.pdf)
- [Week 6 transcript](week_06_identity_permissions_rls_transcript.md)

## Database Setup

Use your own PostgreSQL/Supabase practice project. If its account or connection
is not working, use the existing notebook's disposable PostgreSQL setup instead.
Both routes run the same lab SQL; the notebook does not test Supabase Auth or
cloud networking.

### PostgreSQL Without a Cloud Database Account

[![Open setup in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_03/03_views_identity_migration.ipynb)
[View the setup notebook on GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_03/03_views_identity_migration.ipynb)

1. Open a fresh copy in a Python 3 / CPU runtime. Run from the top through the
   query under **Read a Few Rows**, then stop before **Day 1: A View Is a Named
   Query**. The Week 3 title is intentional: you are reusing its setup, not doing
   its assignment. The fixture should report 8 users, 12 tickets, and 21 events.
2. Add code cells using **+ Code**. Put each lab SQL block between the triple
   quotes shown below. Keep each `BEGIN`, role change, query, and `ROLLBACK`
   together in one call. Do not use **Run all** or the Week 3 export cells.
3. Save the SQL inside your quotes, including your explanation comments, in a
   text editor under the filename specified by the current lab. Submit that SQL
   file, not the Python wrapper or the notebook. Run the lab's cleanup first;
   then run the notebook's final **Finish: Remove Only This Notebook's Practice
   Database** cleanup cell when you are done with the runtime.

This small check confirms which database and role receive your SQL:

```python
run_sql("""
SELECT current_database(), current_user;
""")
```

Replace the SELECT with a lab's setup or test block. The helper prints SELECT
results even when a batch ends in `ROLLBACK`. An expected permission denial
appears as a Python `RuntimeError` containing PostgreSQL code `42501`; the
connection closes and rolls back that transaction. Continue with the next
separate test cell. A different error is not a successful permission test.
**Skip the Supabase connection-URI display cell** when using this local route.

Colab still needs a Google account, internet access, and a working runtime.
An already-running disposable local PostgreSQL server is another option; the
notebook's setup explains its local-Jupyter settings. Ask for the classroom
alternative if neither is available. On another day, start fresh if the runtime
expired. Lab 2 supplies its own setup and does not depend on Lab 1's role.

## Day 1: Least-Privilege Role

Slides 1-11 explain the permission model and demonstrate a reader of three open
tickets. The instructor uses `report_reader_demo`; your lab uses a separate
analyst role and a view covering all 12 tickets. You will write a grouped report
under that restricted role as well as test prohibited actions.

Complete [Lab 1: Test allowed and denied actions](lab_01_least_privilege.md).

Submit only `week_06_least_privilege.sql`.

## Day 2: Row-Level Security Test Harness

Slides 12-24 show the four-row ownership case, a direct lookup, and the effect
of adding a row. The instructor's new row belongs to Resident A. In your separate
lab, add a row for Resident 102 and test both residents again. The Supabase token
and UUID examples explain the real-application connection; they do not require
you to build a login system or migrate the course fixture.

Complete [Lab 2: Restrict rows by current actor](lab_02_rls_test_harness.md).

Submit only `week_06_rls_test.sql`.

For support with the lab's explanation, use [Writing About Database Decisions](materials/assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

## Optional Industry Extension: Permission Escape Room

This activity is optional, ungraded, and does not add a submission.

Review this deliberately unsafe proposal without executing it:

```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
```

Assume the application only reads a reporting view and inserts support tickets.
Replace the proposal with the smallest object/action grants you can defend, then
name one allowed test and two denied tests. Add one sentence explaining why RLS,
schema privileges, and secret storage remain separate controls even after the
table grants are corrected.

## End-of-Week Self-Check

Explain why a successful query in the Supabase SQL editor does not determine what an
ordinary authenticated application user can see.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
