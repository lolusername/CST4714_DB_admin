# Industry / Career Connection: GitHub: checking a login did not guarantee the right repository

**Primary source:** [GitHub incident report, October 2016](https://github.blog/news-insights/the-library/incident-report-inadvertent-private-repository-disclosure/). External content retains its own terms.

## What the organization reported

GitHub reported that authorization checks succeeded, but a later routing query could return another repository’s path during concurrent database responses. Some requests therefore received content from the wrong repository. The case illustrates the access problem we will investigate in PostgreSQL.

## Connection to this lesson

A permission test must check both the acting identity and the resource actually returned. A successful login or an allowed query alone cannot establish isolation.

Use the case to examine how the permission would work in Metro Support.

## A short application

For our ownership fixture, test resident_101_lab against both its own IDs and ticket 3. Explain why seeing zero rows for ticket 3 is the correct result, and why an administrator’s successful read does not test that resident’s access.

Use this as a two-minute worked lecture example or optional review. It adds no submission, new account, or required reading beyond the weekly assignment.

**Career connection — Security engineer / database administrator:** Verify actor, target, action, and returned records in a repeatable access test.
