# Week 10 - MongoDB Data Modeling

## Week Focus
Week 10 is where the MongoDB unit shifts from basic introduction into real design work:
- embed vs reference,
- schema validation,
- indexing basics,
- workload-based modeling,
- and a short in-class response tied to a MongoDB case-study video.

## Class Length and Level
- Duration: about 100 minutes per class day
- Level: beginner

## Two-Day Structure
Week 10 now has two class-day MongoDB labs built around MongoDB University:
1. Day 1 lab: `lab_mongodb_atlas_beginner_to_modeling.md`
2. Day 2 lab: `lab_day2_mongodb_university_modeling_studio.md`

## Why This Week Is Structured This Way
Day 1 already gives students the full MongoDB University beginner-to-modeling track.
Day 2 uses the same basic pattern:
- short live instructor modeling first,
- then individual MongoDB University work,
- then a short case-study response after the lab.

## Week 10 Course Materials
- Day 1 lab: `lab_mongodb_atlas_beginner_to_modeling.md`
- Day 2 lab: `lab_day2_mongodb_university_modeling_studio.md`
- Day 2 in-class response: `reading_response_inventory_case_study_video.md`

## Direct MongoDB University Links
Use these as the actual Week 10 assigned labs.

### Day 1 Assigned Units
- [Getting Started with MongoDB Atlas](https://learn.mongodb.com/courses/getting-started-with-mongodb-atlas-smartbridge)
- [MongoDB and the Document Model](https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge)
- [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)

### Day 2 Assigned Units
- [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)
- [Relational (SQL) to Document Model](https://learn.mongodb.com/courses/relational-to-document-model)
- [MongoDB Indexes](https://learn.mongodb.com/courses/mongodb-indexes)

## MongoDB Educator Content Used
This week is built from the strongest official MongoDB teaching material I found:

### MongoDB Educator Center
- MongoDB for Educators: https://www.mongodb.com/academia
- Introduction to Modern Databases with MongoDB: https://www.mongodb.com/academia/courses/introduction-to-modern-databases-with-mongodb
- MongoDB 101: Non-Relational Databases for Beginners: https://www.mongodb.com/academia/courses/mongodb-101-nonrelational-for-beginners

### MongoDB University
- Atlas for Educators: https://learn.mongodb.com/courses/atlas-for-educators
- Getting Started with MongoDB Atlas: https://learn.mongodb.com/courses/getting-started-with-mongodb-atlas-smartbridge
- MongoDB and the Document Model: https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge
- Modeling Data Relationships: https://learn.mongodb.com/courses/modeling-data-relationships
- Relational (SQL) to Document Model: https://learn.mongodb.com/courses/relational-to-document-model
- MongoDB Indexes: https://learn.mongodb.com/courses/mongodb-indexes

## Why These Are the Best Fit
- `Introduction to Modern Databases with MongoDB` is MongoDB's most complete educator-ready curriculum and includes modular lessons, slides, notes, and hands-on exercises.
- `MongoDB 101` is the best fallback primer if a class still needs a short reset on non-relational basics.
- `Atlas for Educators` is the best setup guidance for structuring Atlas in a classroom.
- The MongoDB University units are the best student-facing labs because they are guided, browser-based, and already aligned to beginner MongoDB learning.

## Learning Outcomes
By the end of Week 10, students should be able to:
1. Navigate MongoDB University and Atlas with confidence.
2. Explain the document model in plain language.
3. Compare embedding and referencing using workload reasoning.
4. Recognize how SQL relationships translate imperfectly into document models.
5. Explain why schema validation still matters in MongoDB.
6. Name one index choice and defend it as a read/write tradeoff.

## Recommended Flow
1. Day 1: complete the existing MongoDB University beginner-to-modeling lab path.
2. Day 2 live block: model one embed/reference example together.
3. Day 2 live block: translate one small relational design into a document design together.
4. Day 2 individual lab block: [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships).
5. Day 2 individual lab block: [Relational (SQL) to Document Model](https://learn.mongodb.com/courses/relational-to-document-model).
6. Day 2 individual checkpoint: [MongoDB Indexes](https://learn.mongodb.com/courses/mongodb-indexes).
7. Day 2 finish: `reading_response_inventory_case_study_video.md`.

## Day 2 Instructor Live Plan
Use Day 2 as a short guided demo followed by individual MongoDB University work.

### Live Block 1: Relationship Modeling Demo
Before students start the official Day 2 units, walk through a small example such as:
1. one student with current courses,
2. one reusable course record,
3. one inventory event history.

Have students decide:
- embed,
- reference,
- or hybrid.

Keep this short.
The point is to frame the lab, not replace it.

### Live Block 2: SQL-to-Document Demo
Use one small relational example and show:
- what the SQL version would normalize,
- what the MongoDB version might keep in one document,
- what should stay in one source of truth,
- and what duplication might be acceptable.

### Live Block 3: Index Triage
Before students open `MongoDB Indexes`, run a short whole-class checkpoint:
- What field would you index first?
- Why that field before a second one?
- What write cost are you accepting?

Keep this practical.
The point is not index syntax.
The point is workload reasoning.

### Live Block 4: Case-Study Close
End with the inventory-platform video response.
This works best after the MongoDB University labs because students now have enough modeling vocabulary to interpret what they see in the case study.

## Day 2 Interactive Teaching Moves
- Keep the live part short and concrete.
- Show one embedded shape and one referenced shape.
- Ask students to name the workload before naming the pattern.
- Let MongoDB University do the heavy lifting during the individual lab block.
- End by having students connect the video back to one modeling tradeoff they saw in the official units.

## Deliverable Model
Students submit:
- individual MongoDB University completion screenshots,
- and one individual video response.

This keeps the week lab-heavy without turning it into a giant formal report.
