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

## 6. Defend a Document Boundary

In [Week 10 Lab 2](../../lab_02_document_model.md), record your insert and changed-filter observations for Part A. Use the [Chapter 10 reading response](../../reading_response.md) for Part B. Write 150–220 words to the developer building the page for ticket 1003. Bring both parts together in one Brightspace text entry.

Explain how the page retrieves the latest two events, newest first, while the system keeps its complete history. Describe where a change to the requester's current contact details happens and one cost of your design. Cite one Chapter 10 section by title and connect its idea to a result from your insert or filter practice. Identify a paper-trace result as a prediction.

An **access pattern** is a recurring question or change the application makes. **Embedding** keeps related values inside one document. **Referencing** stores an identifier that connects documents. Consider which operation gets easier under your design and which operation takes more work.
