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

## 7. Explain a Reliability Limit

**Use in:** [Week 12: What Does Confirmation Promise?](../../lab_01_reliability_decisions.md).
**Read:** Chapter 12, the discussion of acknowledgments, partitions, and recovery.

Explain the confirmation and read behavior you chose for the supplied incident.
Then compare the stated backup times with the allowed data-loss and recovery
targets. Tell the manager what the design can promise and what it cannot.

A **replica** is another maintained copy of the database. A **backup** preserves
an earlier state for recovery. A deletion can spread to replicas; having several
current copies does not necessarily provide yesterday's state.
