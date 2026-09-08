# Week 1: How Applications Use Databases

A support request exists in the database, but the staff dashboard does not show
it. This week we learn enough about applications and relational data to explain
how that can happen.

## Open in Class

- [PowerPoint](week_01_responsibility_relational_thinking.pptx)
- [PDF handout](week_01_responsibility_relational_thinking.pdf)
- [Individual lab: Where did the requests go?](lab_01_application_database_map.md)

No database installation or cloud account is required this week. Use a browser
and a text editor, or work on paper during the class discussion.

## Before Class: Assigned Reading

Read [Chapter 1](../../textbook/module_01_responsibility.md) before Day 1
and the opening relational-model discussion in [Chapter 2](../../textbook/module_02_sql.md)
before Day 2. The formatted book is included in the course README.
The following official pages are optional supplementary explanations:

- **Before Day 1:** read PostgreSQL's
  [Architectural Fundamentals](https://www.postgresql.org/docs/current/tutorial-arch.html).
  Focus on the client, the database server, and why they may run on different computers.
- **Before Day 2:** read PostgreSQL's
  [Relational Concepts](https://www.postgresql.org/docs/current/tutorial-concepts.html)
  and the refresher below. Focus on what one row represents and how tables connect.

No reading response is submitted this week. In class, you will use the ideas to
explain the lab's missing requests.

## Day 1: An Application Request

An application is the software people interact with. A database holds organized
data; a **database management system (DBMS)** processes queries and manages access,
changes, and storage. PostgreSQL and MongoDB are DBMSs. Supabase and Atlas are
platforms that host and manage database services and provide additional tools.

For a typical support website, the path is:

```text
Browser form -> application/API -> database server -> stored ticket
Browser list <- application/API <- query result    <- stored tickets
```

Saving a request and displaying a list are different operations. A successful
save does not prove that a later query will include the request. We will trace
both operations, distinguish a permission problem from a query problem, and tour
the database interfaces in the slides.

Start the individual lab with the class. Its small dataset is provided in the
lab itself.

## Day 2: Relational Thinking Before SQL

A **relation** is a set of tuples with named attributes. For now, picture a table:
one tuple is one row, and an attribute is a column. First state what a row means,
such as "one support request." This is also called the table's **grain**.

A **primary key** uniquely identifies a row. A **foreign key** connects a value
to a key in another table. A missing assignee does not mean that the ticket is
missing. In SQL, `NULL` represents a missing or unknown value. It is neither the
number zero nor the text `"NULL"`.

| Operation | Meaning | Support-desk example |
|---|---|---|
| Selection, `sigma` | Keep rows satisfying a condition | Tickets whose status is `open` |
| Projection, `pi` | Keep selected attributes | Only ticket ID and subject |
| Product | Pair every row on one side with every row on the other | Four tickets and two agents produce eight pairs |
| Join | Keep pairs satisfying a matching condition | Match each assigned ticket to its agent ID |
| Union | Combine compatible sets | IDs of tickets reported through either of two channels |
| Difference | Keep members of one set absent from another | Active ticket IDs missing from the dashboard |

The slides show the mathematical symbols and small worked results. Mathematical
relations are sets, so they have no duplicate tuples. SQL query results may
contain duplicates unless the query removes them. Neither gives a guaranteed
display order without an explicit ordering rule.

We will work through small results together, then finish the **same lab**.
Submit one individual response in Brightspace, following the lab instructions.

## GitHub's Online Editor

We will also practice editing a file in a repository you own. Open **Add file >
Create new file**, name the file `week_01/notes.md`, and enter a heading beginning
with `#`. Use **Preview** to inspect the formatting, then **Commit changes** to
save a version. You can return to the file and use its edit button to revise it.

This is a tool demonstration, not an extra assignment. Work in your own repository
rather than proposing changes to the class repository. GitHub's
[creating-files guide](https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files)
provides the complete interface instructions.

## Check Your Understanding

Explain why a ticket can be stored successfully yet absent from a dashboard.
Then distinguish selection from projection, and explain what a join's matching
condition does. These ideas become executable SQL in Week 2.

For support with the lab's explanation, use [Writing About Database Decisions](../../assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.
