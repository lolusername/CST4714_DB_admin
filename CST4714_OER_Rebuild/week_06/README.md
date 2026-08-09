# Week 6: Identity, Permissions, and Row-Level Security

## The Week's Question

How can we prove useful access and intentional denial at the same time?

## What You Will Be Able to Do

- separate identity, authentication, authorization, and audit evidence;
- create group roles and apply schema, view, and table privileges;
- test one allowed action and one denied action;
- explain Supabase Auth, PostgreSQL roles, token claims, and RLS as distinct layers;
  and
- build and test a beginner row-ownership policy.

## Read and Use

- [Module 6: Access should be useful and limited](../textbook/module_06_security.md)
- [Week 6 student deck](week_06_identity_permissions_rls.pptx)
- [Week 6 PDF handout](week_06_identity_permissions_rls.pdf)
- [Week 6 transcript](week_06_identity_permissions_rls_transcript.md)

## Day 1: Least-Privilege Role

Complete [Lab 1: Prove allow and deny](lab_01_least_privilege.md).

Submit only `week_06_least_privilege.sql`.

## Day 2: Row-Level Security Test Harness

Complete [Lab 2: Restrict rows by current actor](lab_02_rls_test_harness.md).

Submit only `week_06_rls_test.sql`.

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

Explain why a successful query in the Supabase SQL editor does not prove what an
ordinary authenticated application user can see.
