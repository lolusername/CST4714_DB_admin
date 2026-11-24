# Industry / Career Connection: GitLab: backup automation still needed a restore test

**Primary source:** [GitLab incident postmortem, February 2017](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/). External content retains its own terms.

## What the organization reported

GitLab’s postmortem describes failed logical backups caused by a pg_dump/server version mismatch, failed notification delivery, and recovery procedures that had not been regularly tested. A backup schedule did not establish a usable recovery path.

## Connection to this lesson

Test the artifact, restore into a separate destination, compare known values and rules, and record who can perform the procedure. The lab demonstrates database restoration; full service recovery includes more dependencies.

We apply the company's example to the Metro Support design below.

## A short application

A source and restore each have three tickets, but ticket 1002 has the wrong requester in the restore. Decide whether recovery passed, name the comparison that detects the error, and state what a count check missed.

Use this as a two-minute worked lecture example or optional review. It adds no submission, new account, or required reading beyond the weekly assignment.

**Career connection — Site reliability engineer / database administrator:** Record each recovery check and its owner in the runbook.
