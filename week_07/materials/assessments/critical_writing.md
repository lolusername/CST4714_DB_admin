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

## 5. Recommend Whether to Keep an Index

**Use in:** [Week 7: Does This Index Earn Its Space?](../../lab_02_index_experiment.md).
**Read:** Chapter 7, the sections on plans, index order, and controlled comparisons.

Write a short update to the application developer recommending whether to keep,
remove, or investigate the index further. Use the unchanged
ticket IDs, a difference in plan work, and one storage or update cost. A small
timing difference alone is not a dependable conclusion. Identify measured index
space separately from write overhead that this read experiment did not measure.

An **index** is an additional search structure. Its benefit depends on the query;
its cost includes space and work to keep it consistent when relevant data changes.
