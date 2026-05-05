# Week 13 - Scaling Concepts and Final Project Build

## Week Focus
Week 13 follows the syllabus topic:
- scaling concepts
- sharding and capacity planning
- shard keys, hotspots, and cost signals
- final project build work

This week is designed to be low-prep for the instructor.
The main goal is to give students enough scaling vocabulary to make smarter final project decisions, then use most of class to build project evidence.

## Individual Work Only
All Week 13 work is individual.
There is no group work and no combined submission.

## Week 13 Course Materials
- `Week_13_Scaling_and_Final_Project_Build.pptx`
- `lab_day1_final_project_scope_and_data_model.md`
- `lab_day2_final_project_queries_indexes_and_seed_data.md`
- `sample_final_project_cisa_kev_tracker.ipynb`

## Direct Official Links
- [MongoDB Sharding](https://www.mongodb.com/docs/manual/sharding/)
- [MongoDB Query Optimization](https://www.mongodb.com/docs/manual/core/query-optimization/)
- [MongoDB Explain Results](https://www.mongodb.com/docs/current/reference/explain-results/)
- [MongoDB University: Lab - Indexing Design Fundamentals](https://learn.mongodb.com/learn/course/indexing-design-fundamentals-on-demand-devrel-content/indexing-design-fundamentals/lab-indexing-design-fundamentals?page=1)
- [MongoDB University: Sharding Strategies Skill Badge](https://learn.mongodb.com/courses/sharding-strategies)
- [Supabase Postgres Indexes](https://supabase.com/docs/guides/database/postgres/indexes)
- [Supabase Connection Strings and IPv4 Pooler Guidance](https://supabase.com/docs/guides/database/connecting-to-postgres)

## Recommended MongoDB University Pairing
Use [Lab: Indexing Design Fundamentals](https://learn.mongodb.com/learn/course/indexing-design-fundamentals-on-demand-devrel-content/indexing-design-fundamentals/lab-indexing-design-fundamentals?page=1) with Class 2.

This is the best pairing because students can immediately apply the lab to the final project:
- identify a query workload
- choose an index
- think about index key order
- test whether a query uses an index with `explain()`

The [Sharding Strategies Skill Badge](https://learn.mongodb.com/courses/sharding-strategies) matches the syllabus topic more directly, but it is better as an optional extension because it is broader and more advanced than students need for the final project checkpoint.

## Two-Class Structure

### Class 1
First half:
- scaling vocabulary
- capacity signals
- sharding mental model
- shard key and hotspot examples

Second half:
- final project scope check
- data model build time
- platform-specific data model evidence

### Class 2
First half:
- query evidence
- indexes and why they matter
- beginner query performance signals
- MongoDB University indexing lab
- Supabase/Postgres and MongoDB Atlas connection gotchas

Second half:
- seed data work time
- query writing work time
- index evidence work time

## Learning Outcomes
By the end of Week 13, students should be able to:
1. explain why scaling is usually a workload problem, not just a bigger-server problem
2. explain what a shard key is and why a bad key can create hotspots
3. name at least three capacity signals that suggest a database is under pressure
4. build or revise the final project data model
5. create or plan seed data for the final project
6. write at least four useful final project queries
7. identify one index that supports a final project query

## Recommended Instructor Flow
1. Use `Week_13_Scaling_and_Final_Project_Build.pptx`.
2. Run `lab_day1_final_project_scope_and_data_model.md` after the scaling introduction.
3. Use `sample_final_project_cisa_kev_tracker.ipynb` as a quick inspiration example if students are stuck.
4. Pair the second class with MongoDB University's `Lab: Indexing Design Fundamentals`.
5. Run `lab_day2_final_project_queries_indexes_and_seed_data.md` during the second class.
6. End the week with each student having a data model, seed data plan, query list, and at least one index decision.
