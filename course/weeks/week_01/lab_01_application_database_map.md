# Week 1 Lab: Where Did the Requests Go?

The campus repair desk says its dashboard shows **every active request**. A
student has a confirmation number for a broken bench, but staff cannot find that
request on the dashboard. Your job is to explain the discrepancy using the data.

Work individually in class. You do not need SQL, a cloud account, or GitHub to
complete this lab. Submit one short text response in Brightspace.

## The Data

For this exercise, **active** means `new` or `open`. A blank assignee, shown as
`NULL`, means that no staff member has been assigned yet.

**Tickets: one row per request**

| ticket_id | subject | status | assignee_id |
|---:|---|---|---:|
| 1001 | Streetlight dark near bus stop | open | 201 |
| 1003 | Low water pressure | resolved | 201 |
| 1004 | Broken bench slat | new | NULL |
| 1009 | Bus shelter panel cracked | new | NULL |

**Agents: one row per staff member**

| agent_id | name |
|---:|---|
| 201 | Priya Shah |
| 202 | Noah Williams |

The dashboard first keeps active tickets, then keeps **only tickets with a
matching agent**. It currently displays:

| ticket_id | subject | agent |
|---:|---|---|
| 1001 | Streetlight dark near bus stop | Priya Shah |

## 1. Trace a Request

Here is a worked example for reading request 1001:

```text
The browser asks the application for request 1001.
The application checks permission and asks the DBMS for that ticket.
The DBMS returns the matching row.
The application formats the response and the browser displays it.
```

Now describe what must happen when a student **submits a new request**. Use the
same components and include where the new record is stored. Three or four plain
sentences are enough. The supplied tables tell you which application facts must
survive after the browser closes.

## 2. Explain the Missing Requests

Use the tables to answer these together in a short paragraph:

- Which ticket IDs should appear if the dashboard really shows every active
  request? Which of those IDs are missing?
- What part of the dashboard's rule removes them? Does the data support the
  claim that their records were deleted?
- How should the rule change so staff can see unassigned work? Describe the
  behavior in words; no SQL is required.

Check your reasoning with this change: suppose ticket 1004 is assigned to agent
202, and nothing else changes. Predict what the **current** dashboard would show
and whether its original promise would now be satisfied.

## Submit

Paste your request trace and your explanation into **one Brightspace text
submission**. Include the relevant ticket IDs and your prediction. A diagram is
welcome but not required. You are graded on connecting your explanation to the
given rows, distinguishing stored data from displayed results, and proposing a
rule that preserves unassigned active tickets.
