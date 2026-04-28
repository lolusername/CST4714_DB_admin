# Week 12 - Reliability and Final Project Launch

## Week Focus
Week 12 follows the syllabus topic:
- replication and reliability concepts
- MongoDB Atlas reliability
- read preference and write concern
- backup and restore thinking

Week 12 also launches the final project.
Each class meeting should spend about half the time on reliability concepts and about half the time helping students start a realistic, beginner-friendly final project.

## Individual Work Only
All Week 12 work is individual unless the instructor explicitly changes the project policy.

## Week 12 Course Materials
- `Week_12_Reliability_and_Final_Project_Launch.pptx`
- `Week_12_Reliability_and_Final_Project_Launch.pdf`
- `lab_day1_reliability_and_project_choice.md`
- `lab_day2_restore_first_project_studio.md`
- `lab_atlas_jumpstart_using_python.md`

## Why This Week Is Structured This Way
Students need to learn reliability vocabulary before the final project, but they also need class time to make the project manageable.

The full final project assignment is in [`../final_project.md`](../final_project.md).
Week 12 only introduces the project and gives students in-class checkpoints to start it.

## Direct Official Links

### MongoDB / Atlas
- [Replication](https://www.mongodb.com/docs/manual/replication/)
- [Read Preference](https://www.mongodb.com/docs/manual/core/read-preference/)
- [Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- [MongoDB Atlas Back Up, Restore, and Archive Data](https://www.mongodb.com/docs/atlas/backup-restore-cluster/)
- [Atlas Backup Scheduling](https://www.mongodb.com/docs/atlas/backup/cloud-backup/schedule-backup/)

### Supabase / Postgres
- [Supabase Backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase Backup and Restore using the CLI](https://supabase.com/docs/guides/platform/migrating-within-supabase/backup-restore)
- [Supabase Read Replicas](https://supabase.com/docs/guides/platform/read-replicas)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)
- [PostgreSQL High Availability, Load Balancing, and Replication](https://www.postgresql.org/docs/current/high-availability.html)

## Textbook Connection
Use the local textbooks as background support:
- Molina/Ullman, *Database Systems: The Complete Book*: failure modes, logging, recovery, media failure, distributed databases, and data replication.
- Obe and Hsu, *PostgreSQL: Up and Running*: backup/restore utilities, restore workflow, and replication background.
- *PostgreSQL 16 Cookbook*: WAL, backup strategies, recovery, and replication troubleshooting.

## Two-Day Structure

### Day 1
First half:
- replication vocabulary
- primary/secondary model
- failover
- read preference
- write concern

Second half:
- final project explanation
- choose platform path
- choose beginner-friendly project scenario
- start the project proposal

### Day 2
First half:
- backup/restore thinking
- restore-first mindset
- reliability runbooks
- Supabase and Atlas reliability comparisons

Second half:
- project studio
- create a project folder or code artifact location
- write initial schema/model plan
- write first reliability/runbook notes

## Learning Outcomes
By the end of Week 12, students should be able to:
1. explain primary, secondary, replica set, failover, replication lag, read preference, and write concern in plain language
2. explain why backups are not enough unless restore steps are tested
3. compare a basic reliability concern in Atlas and Supabase
4. choose a final project platform path: Supabase/Postgres, MongoDB/Atlas, or both
5. define a beginner-friendly application domain and scope
6. start final project artifacts with a schema/model plan, seed data plan, and reliability checklist

## Recommended Flow
1. Start with `Week_12_Reliability_and_Final_Project_Launch.pptx`.
2. Run Day 1 reliability discussion, then have students complete `lab_day1_reliability_and_project_choice.md`.
3. Use `../final_project.md` only when students need the full final project assignment.
4. Run Day 2 backup/restore discussion, then have students complete `lab_day2_restore_first_project_studio.md`.
5. Use `lab_atlas_jumpstart_using_python.md` when students need hands-on practice connecting Python to Atlas.
6. End Week 12 with every student having a chosen platform, chosen project scenario, and first project proposal draft.
