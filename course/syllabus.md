# CST4714 Database Administration

## Fall 2026 Course Syllabus

| Course information | Details |
|---|---|
| **Instructor** | Professor Atilio Barreda |
| **Credits** | 3 credits; 2 class hours and 2 lab hours |
| **Class meetings** | Two 100-minute meetings in most weeks |
| **Section, time, and room** | Check the current listing in CUNYfirst and Brightspace |
| **Course site** | [CUNY Brightspace](https://brightspace.cuny.edu/) |
| **Contact and office hours** | Posted in Brightspace |

## Course Description

CST4714 is a hands-on course about running databases, not just designing them.
We will review the relational model and SQL at the beginning of the semester
because it is difficult to administer a database if you cannot tell what a
schema or query is supposed to do.

The first part of the course uses PostgreSQL and Supabase. We will work with
tables, constraints, transactions, roles, indexes, query plans, backups, and
restores. The second part uses MongoDB and Atlas to study document databases,
JSON, data modeling, aggregation, indexing, replication, and scaling. We will
also compare the two approaches instead of treating either one as the answer to
every problem.

By the end of the semester, you should be able to build a small database, make
reasonable administration decisions, test whether those decisions worked, and
explain your work to another person.

## Prerequisites and SQL Review

The City Tech catalog lists CST2405, CST2415, or CST3604 with a grade of C or
higher as prerequisite routes. CUNYfirst is the final record of whether a
student has met the prerequisite.

You are expected to have seen databases and SQL before, but you are not expected
to remember everything. The first three weeks include a substantial review of
the relational model, relational algebra, SQL, keys, constraints, joins,
grouping, subqueries, and common mistakes. The opening diagnostic is ungraded
and helps me decide what we need to review in class.

## Learning Outcomes

By the end of this course, you should be able to:

1. explain the responsibilities of a database administrator and the difference
   between the database engine, a cloud platform, and an application;
2. create and query a small relational database using PostgreSQL and Supabase;
3. create and query a small document database using MongoDB and Atlas;
4. choose a sensible relational or document model for a stated problem;
5. use constraints, validation, roles, privileges, and basic access controls to
   protect a database;
6. investigate transactions, blocking, query plans, and indexes when something
   is slow or behaving unexpectedly;
7. plan and check a logical backup and restore; and
8. explain database choices and tradeoffs in writing, in a demonstration, and
   in a job interview.

## Required Materials and Accounts

There is no textbook to purchase. The course-created textbook is assigned one
chapter at a time through each weekly page; slides, labs, datasets, and links
will also be posted in Brightspace. Other
materials, including vendor documentation and MongoDB learning activities, are
free to use but are not necessarily openly licensed.

You will need:

- regular access to a computer with a current web browser;
- your City Tech/CUNY account and Brightspace;
- a free GitHub account;
- a free Supabase account;
- a free MongoDB Atlas account; and
- Google Colab or another Jupyter notebook environment.

Do not purchase a paid database plan or enter a payment card for this course.
If an account, device, or network problem prevents you from doing an assignment,
let me know. I will provide a local or non-cloud alternative when the platform
itself is the problem.

## How Class Will Work

This course meets twice in most weeks. A typical class includes a short
explanation or demonstration followed by guided practice and an individual lab.
Most labs are designed to begin, and often finish, during class. Some classes
will also include a short writing response, notebook exercise, or check for
understanding.

Questions are expected. Database work produces errors, and learning how to read
an error carefully is part of the course. We may discuss a problem as a class,
but graded labs and projects are completed individually.

## Assignments and Grading

| Category | Weight | What is included |
|---|---:|---|
| In-class work and skill practice | 30% | individual labs, notebook exercises, short writing responses, and brief checks for understanding |
| Midterm PostgreSQL/Supabase project | 30% | an individual database administration case completed during the first half of the course |
| Final cloud database project | 40% | an individual project using PostgreSQL/Supabase, MongoDB/Atlas, or a well-explained combination |

Attendance by itself is not graded. The in-class work category is based on the
work you complete and submit. Small checks may be graded for completion and
reasonable effort. Labs and projects are graded for correctness, explanation,
and whether the work can be checked.

### Letter Grades

| Grade | Range | Grade | Range |
|---|---:|---|---:|
| A | 93-100 | C+ | 77-79.9 |
| A- | 90-92.9 | C | 70-76.9 |
| B+ | 87-89.9 | D | 60-69.9 |
| B | 83-86.9 | F | below 60 |
| B- | 80-82.9 |  |  |

## Major Projects

### Midterm PostgreSQL/Supabase Project - 30%

The midterm is an individual PostgreSQL/Supabase administration case. You will
build and query a small relational database, work with transactions, investigate
a controlled locking or blocking problem, make one useful access or performance
improvement, and describe how the database could be backed up and restored.
Detailed instructions and the rubric will be posted as one assignment in
Brightspace.

### Final Cloud Database Project - 40%

For the final, you will build a small database project using
PostgreSQL/Supabase, MongoDB/Atlas, or a combination that you can justify. You
will design the data model, load sample data, write useful queries, add and
explain one index, address one access-control concern, and discuss backup,
recovery, and reliability. You will also give a short individual demonstration
of the finished project.

A public GitHub repository can be useful for a portfolio, but it is not
required. You may submit code or other requested files through Brightspace, or
give me access to the cloud project when the assignment calls for it. The final
project instructions and rubric will be kept in one Brightspace assignment so
that there is only one list of requirements.

## Submitting Work

Submit the item and format named in Brightspace. When an assignment requires a
particular interface view, its instructions will say so explicitly; otherwise,
submit the requested code, notebook, URL, or written response.

When you submit technical work:

- put commands, queries, or steps in an order that another person can follow;
- identify which database or tool you used;
- include the relevant result or observation;
- explain mistakes or limitations when they matter; and
- remove passwords, connection strings, keys, and private account information.

## Individual Work, Documentation, and AI Tools

All graded labs, notebooks, writing responses, the midterm, and the final
project are individual. You may discuss concepts, compare error messages that
do not contain private information, and point classmates to documentation. You
may not copy another student's finished work or submit an answer you cannot
explain.

Unless an assignment says otherwise, you may use official documentation,
autocomplete, syntax references, debugging tools, and AI tools. If you use a
tool to suggest code or an explanation, you are still responsible for testing
it and understanding it. Generated work that you cannot run, check, and explain
will not receive credit.

The opening diagnostic and any activity marked as a closed check must be
completed without outside assistance. Cite sources for prose, code, data, or
images that you did not create.

## Attendance and Missed Class

Regular attendance is important because a large part of the course is guided
technical practice. Attendance is recorded for college reporting, but it is not
a separate grade.

If you miss class, check Brightspace first. Complete the posted lab or catch-up
version and contact me promptly if illness, an accommodation, or a serious
technical problem affects a deadline. Do not email private medical information
or account credentials.

## Late Work and Technical Problems

The due date and any late or catch-up period will be listed on each Brightspace
assignment. Contact me before a major deadline when possible if you know you
will have a problem submitting.

If Brightspace, Supabase, Atlas, GitHub, or Colab is unavailable, save your work
and a small record of the error. Use the local alternative listed in the
assignment or follow the submission update I post in Brightspace.

## Communication

Check Brightspace announcements and your City Tech email regularly. Use the
contact information posted in Brightspace and include `CST4714`, your section,
and a useful subject line in your message. I normally respond within two
business days.

Grades and personal student matters should be discussed through a private
college-approved channel, not in a public GitHub issue or shared class document.
Never send a password, private key, complete connection string, service-role
key, or recovery code.

## Fall 2026 Course Schedule

This is the planned order of topics. I may adjust the pace based on what the
class needs and on changes to the cloud platforms. Brightspace will show the
actual due dates.

| Week | Topics | Main work |
|---:|---|---|
| 1 | Course introduction; what a DBA does; relational model and relational algebra review; GitHub orientation | responsibility exercise and relational review |
| 2 | SQL review: SELECT, filtering, sorting, joins, grouping, subqueries, CTEs, and safe data changes | SQL practice lab |
| 3 | SQL and schema review: tables, keys, constraints, indexes, and database metadata | schema and integrity lab |
| 4 | Views, identity columns, sequences, introspection, and safe schema changes | view and migration exercise |
| 5 | Transactions, ACID, isolation, MVCC, locks, and blocking | transaction and blocking lab |
| 6 | Roles, privileges, least privilege, Supabase Auth, row-level security, and secrets | access-control lab |
| 7 | `EXPLAIN`, query plans, selectivity, and index design | query-plan and indexing lab |
| 8 | Logical backups and restores, migrations, review, and the midterm project | restore exercise and midterm |
| 9 | History of NoSQL; JSON; types of NoSQL databases; MongoDB Atlas orientation | JSON and document-design exercise |
| 10 | MongoDB collections, CRUD, basic MQL, embedding, referencing, and access patterns | MongoDB query and modeling lab |
| 11 | Aggregation pipelines, validation, indexes, and `explain` | aggregation and performance lab |
| 12 | Replication, consistency, read preference, write concern, and recovery | reliability and recovery exercise |
| 13 | Capacity, sharding, shard keys, Python database connections, and final-project planning | notebook and project checkpoint |
| 14 | Using more than one database, distributed-system tradeoffs, incident response, and project work | incident exercise and project work |
| 15 | Course review, final demonstrations, and explaining database work in portfolios and job interviews | final project and individual demonstration |

### Important Fall 2026 Dates

The [City Tech Fall 2026 academic calendar](https://www.citytech.cuny.edu/registrar/docs/fall_2026.pdf)
is the official source for college dates.

| Date | College calendar item | Date | College calendar item |
|---|---|---|---|
| **Aug. 28** | Fall term and classes begin | **Oct. 13** | Classes follow a Monday schedule |
| **Sept. 1** | First scheduled meeting for this section | **Oct. 23** | Midterm progress reports due |
| **Sept. 3** | Last day to add; last day to drop without a WD | **Nov. 6** | Last day to withdraw with a W |
| **Sept. 4** | Verification of Enrollment rosters available | **Nov. 25** | No classes scheduled |
| **Sept. 7** | Labor Day; college closed | **Nov. 26-27** | Thanksgiving holiday; college closed |
| **Sept. 11-13** | No classes scheduled | **Dec. 15-21** | Final examination period |
| **Sept. 17** | Verification of Enrollment rosters due | **Dec. 21** | End of Fall 2026 term |

## Account and Data Safety

Use synthetic, public, course-supplied, or properly licensed data for this
course. Do not upload private employer data, protected student information,
medical data, or other sensitive personal information.

Your website login, cloud project, database user, application role, and API key
are different things. I will never need your password. If you need help, send
the smallest relevant error message after removing passwords, keys, connection
strings, account identifiers, and other private information.

## Accessibility

City Tech is committed to supporting the educational goals of enrolled students
with disabilities in the areas of enrollment, academic advisement, tutoring,
assistive technologies, and testing accommodations. If you have or think you
may have a disability, you may be eligible for reasonable accommodations or
academic adjustments as provided under applicable federal, state, and city
laws. You may also request services for temporary conditions or medical issues
under certain circumstances. If you have questions about eligibility or would
like to seek accommodation services or academic adjustments, call
718-260-5143, email `Accessibility@citytech.cuny.edu`, or visit the
[Center for Student Accessibility](https://www.citytech.cuny.edu/accessibility/).

## Academic Integrity

Students and all others who work with information, ideas, texts, images, music,
inventions, and other intellectual property owe their audience and sources
accuracy and honesty in using, crediting, and citing sources. As a community of
intellectual and professional workers, the College recognizes its
responsibility for providing instruction in information literacy and academic
integrity, offering models of good practice, and responding vigilantly and
appropriately to infractions of academic integrity. Accordingly, academic
dishonesty is prohibited in CUNY and at City Tech and is punishable by penalties
including failing grades, suspension, and expulsion. See the current
[City Tech Academic Integrity policy](https://www.citytech.cuny.edu/academic-integrity/index.aspx).

## Student Support

[City Tech Student Hub](https://www.citytech.cuny.edu/current-student/) |
[CUNY Brightspace](https://brightspace.cuny.edu/) |
[Academic Technologies and Online Learning](https://www.citytech.cuny.edu/atol/) |
[Center for Student Accessibility](https://www.citytech.cuny.edu/accessibility/) |
[Academic Integrity](https://www.citytech.cuny.edu/academic-integrity/index.aspx) |
[Fall 2026 Academic Calendar](https://www.citytech.cuny.edu/registrar/docs/fall_2026.pdf) |
[Official CST4714 Course Outline](https://www.citytech.cuny.edu/computer-systems/docs/courses/CST4714.pdf)

## Changes to the Syllabus

I may adjust the pace, examples, or dates when the class needs more practice, a
platform changes, or the college schedule requires it. Changes will be posted
in Brightspace. Grading weights and major project requirements will not change
without a clear announcement.

**Version:** Fall 2026, September 1, 2026.
