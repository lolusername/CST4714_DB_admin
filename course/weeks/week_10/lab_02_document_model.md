# Lab 2: Design the Ticket Page

A resident opens one ticket page to see its status and latest events. Staff also
need to update the resident's contact details once, without finding every ticket
that ever mentioned that resident. Design documents for those two requirements.

Work individually in class. Submit one Brightspace text response.

## 1. Use the MongoDB University Modeling Activity

Open [Modeling Data Relationships: Lesson 4, Modeling One-to-Many](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn).
Use the lesson and complete its [Practice activity](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1).
Sign in with your free MongoDB University account if requested. The full course
and badge are not required. Validation is next week's subject.

The instructor demonstrates **Lesson 3: Modeling One-to-One**, not this lesson.
Follow Lesson 4's own examples before applying the ideas below. Keep one image
of its Practice result or progress; no invented score or full-course badge.

If the platform or account access is unavailable, use Chapter 10's worked embedding and
referencing examples and note that substitution in the same response. You still
complete the design task; do not invent a completion score.

## 2. Apply It to One Ticket

Use ticket **1003** and its three events from the
[Week 9 CSV-to-JSON case](../week_09/lab_01_csv_to_json.md). Start with one of your
Week 9 designs or the worked shapes in [Chapter 10](../../textbook/module_10_mql_modeling.md).

**New requirement:** the ticket page shows the **latest two events**, newest
first, while the system retains all three current events and future history.
The current contact details must be editable in one authoritative user record.
This is a revision for a workload, not another request to write two JSON versions.

Write one representative JSON ticket document. Show where its requester ID and
latest events belong. If you keep related data in another collection, show one
small example of that related document too. There is more than one defensible
answer.

In a short explanation to the developer implementing the page, name the two
event IDs it should show and describe how it retrieves them, where a contact
change happens, and what you would do if one ticket accumulated 50,000 events.
Plain language is sufficient; no runnable MQL is required for this response.
Embedding all history forever is not the only way to make a page convenient.
References identify related documents; MongoDB does not automatically enforce a
foreign key between them.

**Submit:** your JSON, a concise explanation, and the Lesson 4 Practice progress image
in one Brightspace text response. Redact account details from the image. No extra
file, repository, or full-course completion is required.
