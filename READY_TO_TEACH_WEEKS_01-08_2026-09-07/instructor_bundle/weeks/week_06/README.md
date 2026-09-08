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

Use [Chapter 6: Access Should Be Useful and Limited](../../textbook/module_06_security.md).

- **Before Day 1:** read through **Test Both an Allowed and a Denied Action**, plus the limited reporting-view worked example.
- **Before Day 2:** read the Supabase identity, row-security, secret-handling, and network-control sections. Distinguish database roles from individual application users.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- [Week 6 student deck](week_06_identity_permissions_rls.pptx)
- [Week 6 PDF handout](week_06_identity_permissions_rls.pdf)
- [Week 6 transcript](week_06_identity_permissions_rls_transcript.md)

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

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

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
