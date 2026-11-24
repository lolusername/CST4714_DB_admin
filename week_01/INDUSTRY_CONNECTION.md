# Industry / Career Connection

## GitLab: a database outage became a recovery problem

GitLab’s January 2017 outage involved accidental deletion from its primary database. Recovery depended on finding a usable copy and understanding which data lived in which system. [GitLab engineering postmortem · February 10, 2017](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/).

## Why this belongs in the lesson

An application can depend on several stores. A database administrator checks the affected records and the recovery path before announcing that data is safe. In the classroom, apply the same diagnostic steps to the ticket example.

Read the worked course example first, then use this case for a three-minute connection to professional work. No additional submission is required.

## Teaching explanation

GitLab published an unusually detailed account of its January 2017 outage. Data was accidentally removed from the primary database, and several expected backup paths did not provide the recovery they needed. The company’s Git repositories and its application database were different stores. Knowing which service failed helps us identify the affected data. Our dashboard example traces how a query handles a saved ticket. The connection is the habit of checking the actual system boundary and evidence. A DBA or reliability engineer needs to explain that difference clearly.

The original prose here is CC BY-NC-SA 4.0. The linked company article retains its own license.
