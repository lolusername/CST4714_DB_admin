# Writing About Database Decisions

Administrators explain database behavior to developers, colleagues, and people
using an application. These short responses practice that work: identify who is
affected, explain what happened, and recommend what should change. Use particular
rows, rules, or operations to support your explanation. The relevant technical
terms are introduced below and in the assigned chapter.

The eight prompts below are **part of the linked labs, not eight additional
assignments**. Use the submission format specified in the lab: a Brightspace text
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

## 1. Explain a Missing Result

**Use in:** [Week 1: Where Did the Requests Go?](../weeks/week_01/lab_01_application_database_map.md).
**Read:** Chapter 1's request-path and missing-dashboard-result discussion.

Write to the repair-desk staff member who cannot find request 1004. Explain how a
stored request can be missing from the dashboard. Use the supplied ticket IDs to
identify the rule responsible and describe the corrected behavior in ordinary
language. Include the lab's prediction after an assignment changes.

No SQL is needed. "Missing from this result" and "deleted from the database" are
different claims. The lab provides enough information to distinguish them.

## 2. Explain Why a Constraint Matters

**Use in:** [Week 3: Make Misspelled Statuses Impossible](../weeks/week_03/lab_02_integrity_constraints.md).
**Read:** Chapter 3, the sections on constraints and rejected changes.

Explain one accepted change and one rejected change from your experiment. Name
the rule and the bad state it prevents. Connect that state to a person using the
application, such as a staff member choosing which requests to handle first.

A **constraint** is a rule the database checks when data changes. Rejection can
be the correct result. An application message is still needed so a person can
understand and correct the input.

## 3. Write an Incident Update

**Use in:** [Week 5: The Query Finished, but Which Change Survived?](../weeks/week_05/lab_02_blocking_incident.md).
**Read:** Chapter 5, "Waiting Is a Relationship Between Sessions" through "Safe
Incident Communication."

Explain to the developer which update waited and which session held the resource
it needed. Compare the final data when that session rolls back with the data when
it commits. Explain why both choices let the waiter finish but are not the same
business decision. Use the notebook's actual results, or label its supplied
rollback trace and your unexecuted commit prediction if you used that path.

The **blocked** session is waiting; the **blocking** session holds something it
needs. State what was observed before proposing a cause. Describe the scope of
the classroom experiment; its results do not measure a production outage.

## 4. Explain an Access Boundary

**Use in:** [Week 6: Row-Level Security](../weeks/week_06/lab_02_rls_test_harness.md).
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

## 5. Recommend Whether to Keep an Index

**Use in:** [Week 7: Does This Index Earn Its Space?](../weeks/week_07/lab_02_index_experiment.md).
**Read:** Chapter 7, the sections on plans, index order, and controlled comparisons.

Write a short update to the application developer recommending whether to keep,
remove, or investigate the index further. Use the unchanged
ticket IDs, a difference in plan work, and one storage or update cost. A small
timing difference alone is not a dependable conclusion. Identify measured index
space separately from write overhead that this read experiment did not measure.

An **index** is an additional search structure. Its benefit depends on the query;
its cost includes space and work to keep it consistent when relevant data changes.

## 6. Defend a Document Boundary

**Use in:** [Week 10: Document Model Decision](../weeks/week_10/lab_02_document_model.md).
**Read:** Chapter 10, the embedding and referencing discussion.

Explain the document shape already submitted in the lab. Describe how the page
retrieves the latest two events while retaining all history, and where a current
contact correction happens. Explain a cost of that choice and what would need
attention if the history grew to 50,000 events. This supports the lab's existing
response; it does not require another JSON model or another submission.

An **access pattern** is a recurring question or change the application makes.
Embedding means placing related values inside a document; referencing means
storing an identifier that leads to data elsewhere. Neither choice wins for
every workload.

## 7. Explain a Reliability Limit

**Use in:** [Week 12: What Does Confirmation Promise?](../weeks/week_12/lab_01_reliability_decisions.md).
**Read:** Chapter 12, the discussion of acknowledgments, partitions, and recovery.

Explain the confirmation and read behavior you chose for the supplied incident.
Then compare the stated backup times with the allowed data-loss and recovery
targets. Tell the manager what the design can promise and what it cannot.

A **replica** is another maintained copy of the database. A **backup** preserves
an earlier state for recovery. A deletion can spread to replicas; having several
current copies does not necessarily provide yesterday's state.

## 8. Describe a Technical Decision in an Interview

**Use in:** [Week 15: GitHub Concept Project](../weeks/week_15/lab_01_github_concept_artifact.md).
**Read:** Chapter 15, the worked project and interview explanations.

Use the closing explanation in your concept guide to describe the problem, the
change you made, the result you checked, and what you would investigate next.
Connect it to the code or example already in that guide. Do not create a second
portfolio item or a separate interview report.

"In a course exercise, I ..." is an accurate and useful opening. Distinguish a
local experiment from work on a production service. A limitation you understand
is a stronger interview answer than experience you did not have.

## The Week 11 Video Response

The [inventory case-study response](../weeks/week_11/lab_02_sort_and_case_response.md)
has its own prompt and uses an external MongoDB video. That lab is the canonical
assignment. The course-authored interpretation prompt is reusable OER; the video
and MongoDB University activity are not claimed as course-authored work.

## Feedback and Revision

Feedback should identify one technically important strength or correction. You
may improve the explanation in the same submitted artifact; no extra report is
needed. The [common rubrics](rubrics.md) explain how reasoning is assessed. Clear
meaning matters, not an imitation of corporate language or an advanced vocabulary.
