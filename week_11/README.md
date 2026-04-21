# Week 11 - MongoDB Basics Continued: MQL and Beginner Modeling

## Week Focus
Week 11 continues Week 10 instead of jumping ahead.

Because Week 10 did not give enough time for students to finish the MongoDB basics, Week 11 stays focused on:
- reading MongoDB documents,
- writing very basic MongoDB Query Language (MQL),
- using Atlas Data Explorer,
- and understanding beginner-level modeling choices.

This week should feel slower, clearer, and more hands-on than the original plan.

## Individual Work Only
All Week 11 work is individual.
There is no partner or group submission.

## Two-Day Structure
1. Day 1: student-facing lecture deck plus a basic MQL and Atlas lab
2. Day 2: a short MongoDB University in-class lab on improving `$sort` performance plus the inventory-platform video response

## Week 11 Course Materials
- `Week_11_MongoDB_Basics_Continued_MQL_and_Modeling.pptx`
- `lab_day1_basic_mql_and_data_explorer.md`
- `lab_day2_beginner_modeling_continuation.md`
- `reading_response_inventory_case_study_video_week11.md`

## Why This Week Is Structured This Way
Students still need more practice with:
- collections and documents,
- filters and simple queries,
- nested fields and arrays,
- insert and update basics,
- and embed vs reference at the beginner level.

The goal is not to rush into advanced MongoDB topics before the foundation is stable.

## Direct Official MongoDB Links

### Day 1 Assigned Resources
- [MongoDB and the Document Model (SmartBridge)](https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge)
- [MongoDB CRUD Operations: Insert and Find Documents (SmartBridge)](https://learn.mongodb.com/courses/mongodb-crud-operations-insert-and-find-documents-smartbridge)
- [Create, View, Update, and Delete Documents in Atlas](https://www.mongodb.com/docs/atlas/atlas-ui/documents/)
- [db.collection.find()](https://www.mongodb.com/docs/current/reference/method/db.collection.find/)
- [$elemMatch](https://www.mongodb.com/docs/manual/reference/operator/query/elemmatch/)

### Day 2 Assigned Resource
- [Improving Performance of `$sort` stages (Lab Only)](https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only)

### Day 2 Support Resources
- [MongoDB Data Modeling Intro (SmartBridge)](https://learn.mongodb.com/courses/mongodb-data-modeling-intro-smartbridge)
- [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)
- [Data Modeling](https://www.mongodb.com/docs/manual/data-modeling/)
- [Embedding vs References](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)

## Learning Outcomes
By the end of Week 11, students should be able to:
1. explain what a MongoDB document and collection are
2. read simple MQL filters and understand what they return
3. write beginner queries using equality, comparison operators, and one logical operator
4. query a nested field and a basic array field
5. explain what `insertOne()`, `find()`, `updateOne()`, and `deleteOne()` do at a high level
6. compare one embedded model and one referenced model for the same scenario
7. explain one MongoDB modeling choice from the inventory-platform video in plain language
8. explain at a high level why reducing data before a `$sort` stage can improve performance

## Recommended Flow
1. Start with `Week_11_MongoDB_Basics_Continued_MQL_and_Modeling.pptx`.
2. Run the Day 1 live demo inside Atlas Data Explorer.
3. Have students complete `lab_day1_basic_mql_and_data_explorer.md`.
4. Start Day 2 with a short recap of why query shape matters.
5. Have students complete `lab_day2_beginner_modeling_continuation.md`, which now points to the official MongoDB University `$sort` performance lab.
6. Finish Day 2 with `reading_response_inventory_case_study_video_week11.md`.

## What Is Still Only a Preview
Week 11 is still not a full aggregation-and-performance week.

The Day 2 `$sort` lab is just a guided preview of a later MongoDB topic.
Students do not need to master broader performance tuning here.

## Why These Are the Best Fit
- `MongoDB and the Document Model` is the right reset for students who still need a stronger document-level mental model.
- `MongoDB CRUD Operations: Insert and Find Documents` is the best official beginner MQL unit because it covers insertion, filters, comparison operators, logical operators, and arrays.
- `Improving Performance of \`$sort\` stages (Lab Only)` is short enough to work as an in-class official lab without turning the whole week into an advanced performance week.
- The same inventory-platform video still works well because it lets students see beginner modeling ideas in a realistic application context.
