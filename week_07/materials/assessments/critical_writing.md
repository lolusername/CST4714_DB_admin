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

## Week 7: Plan the Midterm Index Test

**Use in:** [Midterm Preliminary Research](../../lab_midterm_research.md).
**Write in:** [the research notebook](../../07_midterm_preliminary_research.ipynb).

Write **180–250 words total** across the notebook's three response cells. Explain
what the query must return using two observations from your outputs. Connect
both assigned PostgreSQL sources to a possible index benefit and cost, then
propose a before-and-after PostgreSQL test. Describe what stays the same, which
results and plan evidence you will compare, and one remaining question. Label
your expected outcome as a prediction: today's Python outputs do not measure
PostgreSQL performance.

Save the outputs, observation table, and writing in your own Colab copy. Submit
**one sharing link** to that copy through today's Brightspace classwork assignment,
with viewer access for the instructor. There is no separate writing document or
file upload. You can revise and reuse this writing in your final midterm README.

The larger [index experiment](../../lab_single_session.md) is optional practice
with no separate submission. If you try it, distinguish measured index storage
from write overhead that its read experiment does not measure.

An **index** is an additional search structure. Its benefit depends on the query;
its cost includes space and work to keep it consistent when relevant data changes.
