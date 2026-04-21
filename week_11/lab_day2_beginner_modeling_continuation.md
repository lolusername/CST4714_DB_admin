# Week 11 Lab Day 2
## Beginner Modeling Continuation: Embed, Reference, and Workload

## Purpose
Day 2 continues the MongoDB basics by slowing down and focusing on beginner modeling choices.

Students should leave able to explain:
- what one-to-one and one-to-many relationships are
- what embedding means
- what referencing means
- and why workload matters when choosing between them

## Big Idea
MongoDB modeling is not just "put everything in one document" and it is not "rebuild SQL tables with different syntax."

The main Day 2 skill is learning to ask:
- what data is read together
- what changes together
- what should stay in one source of truth

## Individual Work Only
This lab is individual.
There is no group work.

## In Class Live Coding

### 1. Embedded Example Demo
Show one document where related data naturally lives together.

Example:

```javascript
{
  _id: 101,
  studentName: "Ava Lopez",
  email: "ava@example.edu",
  currentCourses: [
    { courseId: "CST4714", title: "Database Administration" },
    { courseId: "CST3232", title: "Internet Programming" }
  ]
}
```

### 2. Referenced Example Demo
Show one version where shared data should stay separate.

Example:

```javascript
// students
{
  _id: 101,
  studentName: "Ava Lopez",
  email: "ava@example.edu",
  courseIds: ["CST4714", "CST3232"]
}
```

```javascript
// courses
{
  _id: "CST4714",
  title: "Database Administration",
  credits: 3
}
```

### 3. Workload Question Demo
Ask:
- what is read together most often?
- what changes often?
- what would be annoying to update in many places?

## Complete These Official Resources
1. [MongoDB Data Modeling Intro (SmartBridge)](https://learn.mongodb.com/courses/mongodb-data-modeling-intro-smartbridge)
2. [Modeling Data Relationships](https://learn.mongodb.com/courses/modeling-data-relationships)
3. [Embedding vs References](https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/)

## Individual Lab

### Part A - Relationship Identification
Choose one simple application domain:
- students and courses
- products and inventory events
- or customers and orders

Name:
1. one one-to-one relationship
2. one one-to-many relationship

### Part B - Write One Embedded Model
Write one JSON document that embeds related data.

Your embedded version should be realistic enough that one common read can happen from one main document.

### Part C - Write One Referenced Model
Write a second version that uses references instead.

This version can be:
- two collections
- or a main collection plus IDs that point elsewhere

### Part D - Compare the Two
Write short answers:
1. what gets easier in the embedded model?
2. what gets riskier in the embedded model?
3. what stays cleaner in the referenced model?
4. what common read pattern might favor embedding?
5. what update pattern might favor referencing?

### Part E - Very Light Preview
You do not need to build an aggregation pipeline yet.

Just answer this question:
- if your application later needed a summary report, what is one question you might ask the database often?

Examples:
- How many students are in each course?
- Which products had the most stock changes this week?
- Which customers placed the most orders?

## What Students Should Submit
Submit:
1. one screenshot showing completion or progress in `MongoDB Data Modeling Intro` or `Modeling Data Relationships`
2. `week11_day2_modeling_practice.md`
3. the Week 11 video response submitted in the Brightspace text box

## What Goes in `week11_day2_modeling_practice.md`
Include:
1. the application domain you chose
2. one one-to-one relationship
3. one one-to-many relationship
4. your embedded JSON example
5. your referenced JSON example
6. your short comparison answers
7. one future summary/reporting question you might ask later

## Success Standard
Day 2 is successful if students stop treating embed vs reference as a slogan and start treating it as a workload decision.

## What Strong Day 2 Work Shows
- the student can explain what data is read together
- the student can explain what should stay in one source of truth
- the student can write valid beginner JSON examples
- the student can connect modeling choices to a later question or report
