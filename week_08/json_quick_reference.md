# JSON Quick Reference - CST4714

## What JSON Is
JSON stands for **JavaScript Object Notation**.

It became popular because it is:
- text-based,
- lightweight,
- easy for humans to read,
- easy for machines to parse,
- flexible enough to represent nested data.

The JSON standard defines:
- four primitive types: string, number, boolean, and null,
- two structured types: object and array.

That means JSON can represent:
- a single object,
- a list of objects,
- nested objects,
- arrays inside objects,
- objects inside arrays.

---

## Why JSON Became Popular
JSON spread widely because it fit the web well:
- JavaScript could work with it naturally,
- APIs needed a simple text format,
- it mapped well to dictionaries/objects in many languages,
- it was less verbose than XML for many everyday tasks,
- it made nested application data easier to represent.

JSON did **not** replace every other format.
It became common because it was simple enough to become a default.

---

## Core Syntax Rules

### Objects
Objects use curly braces and name/value pairs.

```json
{
  "course_id": 101,
  "title": "Database Administration"
}
```

### Arrays
Arrays use square brackets and ordered values.

```json
[
  "postgres",
  "mongodb",
  "duckdb"
]
```

### Valid Value Types
A JSON value can be:
- a string
- a number
- `true`
- `false`
- `null`
- an object
- an array

---

## Syntax Habits That Matter
- Keys must be in double quotes.
- String values must be in double quotes.
- Items are separated with commas.
- Do not leave a trailing comma after the last item.
- JSON has no comments.
- JSON does not have separate date or integer types in the standard.

Example:

```json
{
  "student_id": 1,
  "name": "Ava Lee",
  "active": true,
  "advisor": null,
  "tags": ["honors", "dba-track"]
}
```

---

## Why JSON Feels Flexible
The same real-world data can be represented in multiple valid ways.

For example, suppose you have:
- `students.csv`
- `courses.csv`
- `enrollments.csv`

You could represent that data as:

### Option A - Table-like JSON
Keep each CSV as its own array.

```json
{
  "students": [
    { "student_id": 1, "student_name": "Ava Lee", "major": "IT" }
  ],
  "courses": [
    { "course_id": "CST4714", "course_title": "Database Administration" }
  ],
  "enrollments": [
    { "student_id": 1, "course_id": "CST4714", "term": "Spring 2026" }
  ]
}
```

### Option B - Nested by Student
Embed each student's enrollments.

```json
[
  {
    "student_id": 1,
    "student_name": "Ava Lee",
    "major": "IT",
    "enrollments": [
      {
        "course_id": "CST4714",
        "course_title": "Database Administration",
        "term": "Spring 2026"
      }
    ]
  }
]
```

### Option C - Nested by Course
Embed each course's roster.

```json
[
  {
    "course_id": "CST4714",
    "course_title": "Database Administration",
    "students": [
      {
        "student_id": 1,
        "student_name": "Ava Lee",
        "term": "Spring 2026"
      }
    ]
  }
]
```

All three are valid JSON.
The "best" one depends on what the application needs to read and update most often.

---

## What Students Should Notice
- JSON is flexible, but not random.
- You still have to make design choices.
- A flatter structure may preserve table-like thinking.
- A nested structure may better match the application view.
- Different JSON shapes emphasize different read patterns.

---

## GitHub Web Editing Reminder
For this week, writing JSON in a plain text editor is enough.

If you use GitHub online:
- the normal GitHub file editor lets you edit files directly in the browser,
- `github.dev` gives a lightweight VS Code-like editor in the browser,
- neither one requires local installation just to write a `.json` or `.md` file.

The goal this week is not to run code.
The goal is to practice data representation clearly.
