# Week 7 Lab
## NoSQL Design Studio: If You Designed a Database System Today

## Purpose
This lab is a bridge from the SQL/PostgreSQL unit into next week's MongoDB work.

You will use what you already know about relational systems to answer a larger design question:

**If you were designing a database system today, what would stay similar to SQL, what would change, and why?**

By the end, you should be able to:
- name features worth keeping from SQL-era systems,
- identify pressures that pushed people toward NoSQL systems,
- match different workloads to different database families,
- justify a design choice in plain language.

## Completion
- everything should be completed during class

---

## Big Idea
This is a thinking lab, not a syntax lab.

You are not trying to memorize MongoDB commands yet.
You are trying to reason like a database designer:
- what must a database still do well,
- what new pressures changed the design space,
- what tradeoffs would you accept for a specific workload,
- what administrative responsibilities never disappear.

---

## Scenario
Imagine a college hires your team in 2026 to design the data layer for a new campus platform.

The platform includes:
- student and faculty profiles,
- mobile sessions,
- event RSVPs,
- course resource catalogs,
- notifications,
- recommendation features,
- analytics and log data.

The college asks:

> "We know SQL databases are powerful. But if you designed a database system today, how would it be similar to SQL, how would it be different, and why?"

Your job is to produce a short design answer that is technically defensible.

---

## Step 1: Silent Warm-Up + Group Check
Without notes, answer these individually:

1. What are **three things SQL/relational systems do well**?
2. What are **two pressures modern applications create** that a database designer may need to handle differently?
3. Which matters more for a database designer: product hype or workload fit? Explain in one sentence.

Write first, then compare with your group.

---

## Step 2: Group Design Card
Work with one group only. Do not combine with another group.

Choose **one** workload below:

### Workload A - Mobile Sessions
The app mostly needs to fetch session or token data by a known key, with very fast reads and writes.

### Workload B - Resource Catalog
Different resource categories share some fields, but many have different attributes, media, and metadata.

### Workload C - Relationship Intelligence
The college wants to detect suspicious account sharing, shared devices, and connected behavior patterns.

### Workload D - Telemetry and Activity Logs
The platform records large volumes of time-stamped events and mostly queries recent windows or aggregates.

Create one group design card on paper, in a shared doc, or in a single markdown file.

Your card must answer these four prompts:

### 1. What We Keep From SQL
List 3 things worth keeping.

Examples:
- declarative querying,
- transactions,
- indexes,
- integrity rules,
- backup and recovery discipline.

### 2. What We Change for This Workload
List 3 things you would change.

Examples:
- more flexible record structures,
- horizontal scale-out,
- nested records,
- specialized storage model,
- different consistency tradeoffs.

### 3. Best Database Family
Choose one:
- key-value,
- document,
- column-family,
- graph,
- still primarily relational.

Then justify the choice in 3-4 sentences.

### 4. DBA Reality Check
Name at least 3 responsibilities that still exist.

Examples:
- validation and governance,
- indexing,
- monitoring,
- backup/restore testing,
- security and least privilege,
- retention policy,
- incident response.

Use this quick reasoning table if it helps:

| Design area | Keep from SQL-era systems? | Change for modern systems? | Why? |
| --- | --- | --- | --- |
| Declarative querying |  |  |  |
| Transactions / correctness boundaries |  |  |  |
| Indexes / performance tuning |  |  |  |
| Schema rigidity vs flexibility |  |  |  |
| Scaling strategy |  |  |  |
| Relationship handling |  |  |  |
| Backup / recovery / security |  |  |  |

Rules:
- every answer needs a reason, not just a label,
- your final card should fit on one page,
- keep the focus on workload fit, not brand names.

---

## Step 3: Rapid Share-Out + Exit Ticket
Each group should be ready to give a short summary of its choice:
- workload chosen,
- database family chosen,
- one SQL idea kept,
- one thing changed,
- one DBA responsibility that remains.

After the share-out, write an individual exit ticket of 100-150 words:

**If you were designing a database system today, what would still look like SQL, what would look different, and why?**

Your response must include:
- one thing you would definitely keep,
- one thing you would probably change,
- one reason workload matters more than hype,
- one admin responsibility that does not disappear.

---

## Deliverables
Everything is completed in class.

Submit only:
1. one group design card
2. one individual exit ticket

Submission note:
- choose one person from the group to submit the group design card,
- at the top of the submission, that person must write the names of everyone in the group,
- use a line like: `Submitted by: Maya Chen | Group members: Luis Gomez, Ari Patel`

No screenshots, no code file, and no after-class polish.

---

## Evaluation (100 points)
- 35 pts: group design card shows clear keep/change reasoning
- 25 pts: workload is matched to a plausible database family
- 20 pts: DBA/admin concerns are realistic
- 20 pts: exit ticket is clear, specific, and evidence-based

---

## Inclusion and Professional Language Standard
Write for a mixed audience.

- define technical terms the first time you use them,
- avoid assuming everyone shares the same app or cultural examples,
- focus on evidence and tradeoffs,
- challenge ideas, not people,
- prefer claims you can justify over confident but vague answers.

---

## Strong Answer Reminder
A strong answer does **not** say:
- "NoSQL is better because it is newer."

A strong answer does say things like:
- "I would keep declarative querying and indexing because those solve durable problems."
- "I would change data shape or scaling strategy because this workload is nested, bursty, or relationship-heavy."
- "Even in a flexible system, the DBA still has to handle recovery, monitoring, and security."
