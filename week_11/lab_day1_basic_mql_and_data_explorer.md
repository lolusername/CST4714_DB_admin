# Week 11 Lab Day 1
## MongoDB Basics Continued: MQL and Atlas Data Explorer

## Purpose
Day 1 is a reset and continuation week.

The goal is to give students more time with the basics:
- documents,
- collections,
- basic MQL filters,
- nested fields,
- arrays,
- and simple CRUD actions in Atlas.

## Big Idea
Students should not move into harder MongoDB topics until they can comfortably read and write beginner-level queries.

Day 1 is about getting students to the point where they can look at a document and answer:
- what collection this belongs to,
- what fields matter,
- how to filter it,
- and what a query is asking for.

## Individual Work Only
This lab is individual.
There is no group work.

## In Class Live Coding

### 1. Read a Document Demo
Use Atlas Data Explorer and open one collection such as:
- `sample_mflix.movies`
- or `sample_supplies.sales`

Show students how to identify:
- top-level fields
- nested fields
- arrays
- `_id`

### 2. Basic `find()` Demo
Show one simple filter:

```javascript
db.movies.find({ title: "The Matrix" })
```

Then show one nested-field example:

```javascript
db.movies.find({ "imdb.rating": { $gte: 8 } })
```

### 3. Arrays and Result Shaping Demo
Show one array example:

```javascript
db.movies.find({ genres: "Drama" })
```

Then show how results can be shaped:
- projection
- sort
- limit

## Complete These Official Resources
1. [MongoDB and the Document Model (SmartBridge)](https://learn.mongodb.com/courses/mongodb-and-the-document-model-smartbridge)
2. [MongoDB CRUD Operations: Insert and Find Documents (SmartBridge)](https://learn.mongodb.com/courses/mongodb-crud-operations-insert-and-find-documents-smartbridge)
3. [Create, View, Update, and Delete Documents in Atlas](https://www.mongodb.com/docs/atlas/atlas-ui/documents/)

## Individual Lab

### Part A - Document Reading
Open one Atlas sample collection:
- `sample_mflix.movies`
- or `sample_supplies.sales`

Pick one document and identify:
1. one top-level field
2. one nested field
3. one array field
4. the `_id` field

### Part B - Basic Filters
Write and run these beginner queries in Atlas or in the query bar.

#### Query 1 - Equality
Write one equality filter.

Example pattern:

```javascript
{ title: "The Matrix" }
```

#### Query 2 - Comparison Operator
Write one comparison filter using one of:
- `$gt`
- `$gte`
- `$lt`
- `$lte`

Example pattern:

```javascript
{ "imdb.rating": { $gte: 8 } }
```

#### Query 3 - One Logical or Array Query
Write either:
- one logical query using `$and` or `$or`
- or one array query using a field like `genres`

Example patterns:

```javascript
{ $or: [ { year: { $gte: 2000 } }, { runtime: { $lte: 100 } } ] }
```

```javascript
{ genres: "Drama" }
```

### Part C - Result Shaping
Take one of your queries and add:
- projection
- sort
- or limit

Example pattern:

```javascript
db.movies.find(
  { genres: "Drama" },
  { title: 1, year: 1, genres: 1 }
).sort({ year: -1, _id: 1 }).limit(5)
```

### Part D - One Safe Write Practice
Create your own practice collection in Atlas called:
- `week11_practice.people`

Insert 2-3 simple documents using the Atlas UI or an insert command.

Suggested shape:

```javascript
{
  name: "Ava Lopez",
  major: "IT",
  completedLabs: ["atlas", "find"],
  standing: "freshman"
}
```

Then do one update on one document.

Suggested pattern:

```javascript
db.people.updateOne(
  { name: "Ava Lopez" },
  { $set: { standing: "sophomore" } }
)
```

## What Students Should Submit
Submit:
1. one screenshot showing completion of `MongoDB and the Document Model` or `CRUD Operations: Insert and Find`
2. one screenshot showing one successful query result in Atlas
3. `week11_day1_mql_log.md`

## What Goes in `week11_day1_mql_log.md`
Include:
1. the sample collection you used
2. one pasted document example or short field summary
3. your equality filter
4. your comparison filter
5. your logical or array filter
6. one shaped result example using projection, sort, or limit
7. 4-6 sentences explaining what felt easier or clearer about MQL after this lab

## Success Standard
Day 1 is successful if students can read beginner MQL and explain what a filter is doing in plain language.

## What Strong Day 1 Work Shows
- the student can tell the difference between top-level, nested, and array fields
- the student can write at least one valid beginner filter
- the student understands that result shaping changes output, not the stored document
- the student can explain what `updateOne()` changed
