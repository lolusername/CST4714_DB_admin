# Writing About Database Decisions

Administrators explain database behavior to developers, colleagues, and people
using an application. These short responses practice that work: identify who is
affected, explain what happened, and recommend what should change. Use particular
rows, rules, or operations to support your explanation. The relevant technical
terms are introduced below and in the assigned chapter.

The response below is **part of the linked lab, not an additional assignment**. Use the submission format specified in the lab: a Brightspace text
entry, a SQL comment, a notebook Markdown cell, or the final concept guide. Write
in class after the relevant demonstration and experiment. There is no separate
reading report or minimum word count unless the lab explicitly states one.

## From a Result to an Explanation

Explain what you recommend, point to something that supports it, and state an
important limitation. Those are thinking moves, not required section headings.

For example, suppose a practice table contained five orders before an update and
still contains five afterward. "The update worked because there are five rows"
does not tell us whether the right order changed. A stronger explanation is:

> The order count stayed at five, but that alone cannot establish that the update
> was correct. Order 42 now has the requested shipping address, and order 43 still
> has its original address. I would also check that the application shows the new
> address before telling the customer the problem is resolved.

The explanation distinguishes a useful check from what it cannot establish. It
does not claim to have tested the application when only SQL was tested.

## 4. Explain an Access Boundary

**Use in:** [Week 6: Row-Level Security](../../lab_02_rls_test_harness.md).
**Read:** Chapter 6, the sections on database roles and row-level security.

Explain what each test user could see and why. Identify the permitted rows and
the rows belonging to the other user. Use the new ticket and direct-lookup result
from your experiment. Write to the developer: explain what these checks establish
and why a real application still needs a request using each user's verified login
token. If your test did not run as the intended user, say that rather than drawing
an access conclusion from an owner account.

**Authorization** means deciding what an identified user may do. A successful
connection establishes neither permission to see every row nor isolation between
users. Your two-user test addresses that distinction.
