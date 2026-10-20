# In-Class Writing Response: When the Backups Did Not Work

**Week 8, Day 1. Individual. About 20 minutes in class: 7 minutes of video, 3 minutes of background, and 10 minutes of writing. Write your response in the Brightspace assignment.**

No SQL, no screenshots, no database work. Watch one short video about a real
outage, read the facts below, then write a short response that uses this week's
recovery terms.

## Watch (7 minutes)

**rm -rf: The Typo That Deleted GitLab's Production Database (ep. 489)**,
DatabaseHistory, 7:21.
https://www.youtube.com/watch?v=04tfN5WrDS4

The video retells the story. For facts, use GitLab's own postmortem:
https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
Where the two differ, the postmortem wins. For example, the title says "typo,"
but the postmortem says a correct command was run on the wrong server.

## What happened, in brief

On January 31, 2017, GitLab.com's replica database fell behind and could not
catch up. The primary had already removed write-ahead log (WAL) segments the
replica still needed, and GitLab was not archiving WAL. While an engineer was
rebuilding the replica, they meant to wipe the replica's data directory. They ran
the command on the **primary** instead. They stopped it after a second or two,
but about 300 GB of production data was already gone.

Then the team looked for a backup:

- **Scheduled `pg_dump` backups:** the job ran `pg_dump` 9.2 against a
  PostgreSQL 9.6 server. The version mismatch made every run fail, so the S3
  bucket meant to hold the dumps was empty.
- **Failure alerts:** the failure emails were rejected by the receiving mail
  system, so nobody learned the backups were failing.
- **Cloud disk snapshots:** turned on for other servers, but not for the
  database servers.
- **Replication:** the replica was the thing being rebuilt, and its data had
  already been wiped.
- **What saved them:** a disk snapshot an engineer had taken by hand about
  **6 hours** earlier, to copy data to a test (staging) server. It was never
  meant to be a backup.

Restoring from that snapshot lost about 6 hours of changes: roughly 5,000
projects, 5,000 comments, and 700 new user accounts. Git repositories and wikis
were stored separately and were not lost. Copying the data back was slow, and
GitLab.com was down for about **18 hours**.

## Terms to use

- **High availability (HA):** a standby keeps the service running when a machine fails. It copies harmful writes too.
- **Backup:** a saved earlier state, kept somewhere you can actually reach.
- **Restore:** rebuilding a database from a backup, then checking the result.
- **Disaster recovery (DR):** the whole tested plan: people, access, systems, and steps.
- **RPO:** the most recent data you can afford to lose, measured in time.
- **RTO:** how long the service can afford to be down.

## Write (10 minutes)

Write **150 to 250 words**. Answer all three questions.

1. **Two safety measures.** Pick two of GitLab's safety measures from the list
   above. For each one, explain why it did not bring the data back, and say
   which term it belongs to: HA, backup, restore, or DR.
2. **RPO and RTO.** GitLab lost about 6 hours of data and was down about 18
   hours. If its targets had been an RPO of 1 hour and an RTO of 2 hours, did it
   meet them? Name one thing GitLab would have needed in place to meet them.
3. **One check.** Name one check you would add to a backup routine so that a
   silent failure like GitLab's gets caught **before** the day you need the
   backup. Connect it to today's lab: what does restoring into a separate
   database and checking the result prove that "the backup job ran" does not?

Requirements:

- Use at least **three** of the terms above correctly.
- Write full sentences. Make an argument, not a summary of the video.
- Base claims about GitLab on the facts above or the postmortem. Label your own
  ideas as recommendations, and do not invent details.

## Submit

Write your response in the Brightspace assignment for this week.

## Why this sits in Week 8

Today's lab restores a backup into a separate database and tests it. GitLab
had several ways to make backups, but nobody had tested restoring from them.
The lesson of the week in one sentence: a backup only counts once a restore from
it has been tested.
