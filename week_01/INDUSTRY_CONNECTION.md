# Industry / Career Connection

## GitLab: a database outage became a recovery problem

GitLab’s January 2017 outage involved accidental deletion from its primary database. Recovery depended on finding a usable copy and understanding which data lived in which system. [GitLab engineering postmortem · February 10, 2017](https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/).

## Why this belongs in the lesson

An application can depend on several stores. A database administrator checks the affected records and the recovery path before announcing that data is safe. This is a teaching interpretation of the case, not a claim that the company used our synthetic data or classroom SQL.

Read the worked course example first, then use this case for a three-minute connection to professional work. No additional submission is required.

## Teaching explanation

GitLab published an unusually detailed account of its January 2017 outage. Data was accidentally removed from the primary database, and several expected backup paths did not provide the recovery they needed. The company’s Git repositories and its application database were different stores. That distinction matters: saying the website is broken does not yet tell us which data is affected. Our little ticket example is a query problem, not the GitLab incident. The connection is the habit of checking the actual system boundary and evidence. A DBA or reliability engineer needs to explain that difference clearly.

The original prose here is CC BY-NC-SA 4.0. The linked company article retains its own license.
