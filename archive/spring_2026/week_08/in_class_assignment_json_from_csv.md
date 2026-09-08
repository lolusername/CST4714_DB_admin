# Week 8 In-Class Assignment
## From CSV "Tables" to JSON

## Purpose
This activity introduces JSON by asking you to transform a small set of CSV "tables" into one or more JSON representations.

You will not run SQL.
You will not run MongoDB queries.
You will not need a notebook.

You will only:
- read the CSV files,
- think about structure,
- write JSON examples in a text editor or GitHub's web editor,
- explain why your structure makes sense.

---

## Files for This Activity
Use the CSV files in:
- `week_08/csv_case/students.csv`
- `week_08/csv_case/courses.csv`
- `week_08/csv_case/enrollments.csv`

Treat them as if they were simple relational tables.

---

## Tool Rule
For this assignment, use a plain text editor only.

Examples:
- VS Code
- TextEdit in plain text mode
- Notepad
- the GitHub file editor in the browser
- `github.dev`

Do not run:
- SQL
- MongoDB shell
- Atlas queries
- Python scripts

This is a modeling and representation exercise, not a query exercise.

---

## Part 1 - Read the CSVs
Open the three CSVs and make sure you understand:
- what each file represents,
- which columns act like identifiers,
- how the files relate to each other,
- which information repeats across rows.

Write 2-3 sentences:
- What is the domain?
- What seems to be the "main thing" in the data?

---

## Part 2 - Write One Table-Like JSON Version
Create a file named something like:
- `json_option_a.json`
- or `json_option_a.md`

Write a JSON example that keeps the CSVs mostly table-like.

That usually means:
- one array for students,
- one array for courses,
- one array for enrollments.

This version should feel close to the original CSV structure.

You do **not** need to include every row if time is short.
You can use 2-3 representative rows per section.

---

## Part 3 - Write One More JSON Version
Create a second file named something like:
- `json_option_b.json`
- or `json_option_b.md`

Write a different valid JSON representation of the same data.

Examples:
- group by student and embed enrollments,
- group by course and embed roster information,
- create a single object with nested sections,
- use references in one place and nested details in another.

There are many right answers.

The goal is to show that JSON is flexible and that the same source data can be reshaped in multiple ways.

---

## Part 4 - Explain the Tradeoffs
Under your JSON, write a short explanation:

1. What structure did you choose?
2. Why might that structure help a user or application?
3. What information became repeated or more nested?
4. Which version feels more table-like?
5. Which version feels more app-friendly?

Keep this explanation short but specific.

---

## GitHub Web Editor Option
If you want to do the work fully online:

1. Open your repository on GitHub.
2. Navigate to the folder where you want to create your file.
3. Use the GitHub file editor or open the repository in `github.dev`.
4. Create a new `.json` or `.md` file.
5. Paste your JSON examples.
6. Commit the file in the browser.

Shortcut:
- when viewing a repository on GitHub, press `.` to open `github.dev`.

Use `github.dev` if you want a browser editor that feels closer to VS Code.

---

## Deliverables
Submit only:
1. one file with your first JSON representation
2. one file with your second JSON representation
3. a short explanation paragraph, either in one of those files or in a separate markdown file

Everything should be completed in class.

---

## Evaluation (100 points)
- 35 pts: first JSON version is valid and clearly connected to the CSV structure
- 35 pts: second JSON version shows a meaningfully different representation
- 20 pts: explanation names real tradeoffs and design choices
- 10 pts: work is organized, readable, and uses correct JSON syntax

---

## Strong Answer Reminder
A strong answer does **not** say:
- "This is the one correct JSON format."

A strong answer does say things like:
- "This version stays close to table thinking."
- "This version is more nested because the app would probably read data by student."
- "This version repeats some course information, but it may be easier to use in one screen."
