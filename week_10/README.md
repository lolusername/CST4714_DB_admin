# Week 10 – Relational → Document Modeling & Credential Launch

## Student Materials
- `relational_to_document_modeling.pptx` — slide deck covering MongoDB's modeling methodology, relationship patterns, and credential expectations.
- `relational_to_document_lab.js` — `mongosh` lab that reshapes relational-style data into embedded and referenced document models.
- Credential brief — MongoDB University [Relational to Document Model Skill Badge](https://learn.mongodb.com/courses/relational-to-document-model).

## Before Class
1. Register for a free MongoDB Atlas account if you have not already.
2. Enroll in the MongoDB University Relational to Document Model course (link above); skim the overview module.
3. Install or update `mongosh`; confirm you can connect to your Atlas cluster with `mongosh "<connection-string>"`.
4. Optional: Load the provided relational CSVs (posted on the LMS) into SQLite or Postgres so you can follow the live migration demo.

## In-Class Flow
1. **Relational Recap:** Review the highest-read queries from your midterm design and consider their access patterns.
2. **Modeling Methodology:** Capture the 5-step MongoDB schema workflow and note where it differs from your SQL process.
3. **SQL → Mongo Lab:** Run `mongosh --file week_10/relational_to_document_lab.js ...` together for the core workflow; note which sections you will finish at home.
4. **Validation Deep Dive:** Observe how the script applies `jsonSchema` validation and think about how you will enforce governance in your project.
5. **Credential Kickoff:** Record the requirements for the MongoDB skill badge and commit to a timeline for completion.

## After Class Tasks
1. Finish the remaining steps in `relational_to_document_lab.js`, customize it with one of your project entities, and submit the updated script plus a short reflection on embedding vs referencing.
2. Complete at least the first two chapters of the MongoDB University course before Week 11; post questions in the discussion board.
3. Draft a credential plan that includes target completion date, study schedule, any support you need from the instructor, and upload a screenshot of your completed skill badge certificate once earned.

## Helpful Commands
```bash
# Run the lab against your Atlas cluster
mongosh "mongodb+srv://<cluster>/<database>" --username <user> --file week_10/relational_to_document_lab.js

# Inspect validation rules after running the script
mongosh> db.getCollectionInfos({ name: 'customers' })[0].options.validator
```

## External Resources
- MongoDB Docs: [Data Modeling Concepts](https://www.mongodb.com/docs/manual/data-modeling/), [Embedding vs Referencing](https://www.mongodb.com/docs/manual/core/data-model-design/#embedding-and-referencing)
- Blog: [6 Rules of Thumb for MongoDB Schema Design](https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design)
- Credential: [Relational to Document Model Skill Badge FAQ](https://learn.mongodb.com/certificates)
