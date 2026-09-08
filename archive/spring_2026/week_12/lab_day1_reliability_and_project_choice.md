# Week 12 Lab Day 1
## Reliability Concepts and Final Project Choice

## Purpose
Day 1 connects the syllabus topic to the final project.

Students first learn the basic reliability vocabulary behind managed cloud databases.
Then they choose a final project path that is realistic for the rest of the semester.

## Big Idea
Reliability is not just "the cloud keeps it running."

A database administrator still needs to understand:
- where writes go
- where reads can go
- what happens during failover
- what consistency tradeoffs exist
- and what recovery evidence will be required later

## Individual Work Only
This lab is individual.
There is no group work.

## First Half - Reliability Concepts

Use the class discussion and official docs to answer these in plain language:

1. What is a primary node?
2. What is a secondary or replica?
3. What is replication lag?
4. What is failover?
5. What does read preference control in MongoDB?
6. What does write concern control in MongoDB?
7. Why can reading from a replica be useful?
8. Why can reading from a replica be risky if the data is slightly behind?

Useful links:
- [MongoDB Replication](https://www.mongodb.com/docs/manual/replication/)
- [MongoDB Read Preference](https://www.mongodb.com/docs/manual/core/read-preference/)
- [MongoDB Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- [Supabase Read Replicas](https://supabase.com/docs/guides/platform/read-replicas)

## Second Half - Final Project Path Choice

Use the [final project assignment](../final_project.md) only if you need the full project requirements.

Choose:
1. a platform path
2. a beginner-friendly project scenario
3. one reliability concern your project will need to address

## In-Class Checkpoint
Submit `week12_day1_project_choice.md`.

Include:
1. chosen platform path: Supabase/Postgres, MongoDB/Atlas, or both
2. chosen project scenario
3. 3-5 sentences explaining why the platform fits the project
4. 5-7 bullet points listing the main data the project needs to store
5. one reliability concern for the project
6. one backup or restore concern for the project
7. one question you still need answered before building

## Success Standard
Day 1 is successful if every student leaves with a platform path, a manageable project scenario, and a first reliability concern.
