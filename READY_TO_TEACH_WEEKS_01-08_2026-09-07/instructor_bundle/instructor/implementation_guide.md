# Course Implementation Guide

## Scope and Use

This instructor handoff guide supports a two-meeting-per-week implementation of *Operating
Cloud Databases*. It is not a private answer key. It identifies outcomes,
prerequisites, demonstrations, likely misconceptions, equivalent paths, and the
results an instructor can use to decide what comes next.

Most class time belongs to individual technical work. Whole-class explanation is
used to establish a model, inspect results, and resolve common errors. Students
may ask and answer questions publicly, but every lab submission is produced and
submitted individually.

## Stable Meeting Pattern

Use the same five phases often enough that students can spend attention on the
database problem rather than the class procedure.

1. **Retrieve:** three no-notes prompts from the public
   [retrieval bank](../assessments/retrieval_exit_bank.md).
2. **Model:** inspect one complete example and predict its result before running
   it.
3. **Fade:** remove selected steps or labels while retaining the same small case.
4. **Build:** students complete the individual lab and create one checkable
   submission.
5. **Check:** discuss one result and its interpretation. This can be oral or
   uncollected practice; it is not another submission beyond the lab.

Early modules provide complete commands and emphasize prediction and
interpretation. Middle modules provide partial procedures. Late modules provide a
symptom, workload, or operating promise and require students to select useful
measurements or checks.

Weeks 2-8 contain an optional industry extension. Week 1 has one integrated case.
An extension is ungraded, adds
no submission, and must never become an unstated prerequisite. Offer it only when
time and interest permit; a student who uses the standard lab or equivalent
fallback receives no penalty or reduced access to later work. The OER admin brief in this handoff records the contribution and review limits.

## Week 1: How Applications Use Databases and Relational Re-entry

**Student materials:** [Week 1 guide](../weeks/week_01/README.md),
[Chapter 1](../textbook/module_01_responsibility.md),
[Where Did the Requests Go?](../weeks/week_01/lab_01_application_database_map.md).
This one lab spans both meetings and has one Brightspace text submission.
The revised 17-slide deck uses the same four tickets and two agents as the lab.
Day 1 uses slides 1-8. Day 2 uses slides 9-17. The notes contain the complete
spoken explanation; the visible slides are for students.

**Prerequisite:** no current SQL fluency is assumed. Use the beginning diagnostic
to locate remembered vocabulary without grading it.

### Day 1 Arc

- Retrieve distinctions among data, database, DBMS, API, and managed service.
- Model one application request through client, network, API, authentication,
  database engine, schema/query, and stored data.
- Compare the Supabase and Atlas interface figures with the underlying PostgreSQL
  and MongoDB systems they manage.
- Students trace the write path for the supplied support-request case. Keep their
  working notes for the second meeting rather than collecting a separate diagram.
- Discuss how a successful write and a later missing dashboard row can coexist.
  Keep this conversation tied to the supplied request rather than adding another
  diagnostic worksheet.

### Day 2 Arc

- Retrieve tuple, attribute, key, selection, projection, and join without starting
  from SQL syntax.
- Model the lab's four-ticket table and two-agent table. State the grain before
  matching identifiers and notice that some tickets are unassigned.
- Fade the example by giving a plain-language question and asking students to mark
  rows kept, attributes kept, and matching pairs.
- Students explain which requests the current dashboard hides and how preserving
  unmatched requests changes the result. They finish the same Week 1 lab.
- Conclude by comparing the current dashboard result with the promised result.
  The lab's single Brightspace response contains the student's explanation.

**Live demonstration:** trace one familiar application action, such as opening a
support ticket, into a request, authorization decision, query, and returned data.
Then manipulate a tiny printed or projected relation before showing SQL vocabulary.

**Likely misconceptions:** “cloud provider owns every failure,” “a database is the
same as the provider dashboard,” and “a join simply adds columns without changing
row count.”

**Equivalent path:** no account is needed. Use the official-page excerpt already
recorded in the module and the synthetic relation tables.

**Teaching decision:** if students cannot state row grain or distinguish selection
from projection, Week 2 begins with relation marking rather than a longer SQL
lecture.

## Week 2: Relational Algebra and Major SQL Review

**Student materials:** [Week 2 guide](../weeks/week_02/README.md),
[Chapter 2](../textbook/module_02_sql.md),
[SQL review notebook](../notebooks/01_relational_sql_review.ipynb),
[query ladder](../weeks/week_02/lab_01_sql_query_ladder.md), and
[joins, aggregates, and DML lab](../weeks/week_02/lab_02_joins_aggregates_dml.md).

**Prerequisite:** Week 1 row/attribute/key vocabulary. Assume students have seen
SQL previously but cannot retrieve it reliably.

### Day 1 Arc

- Retrieve selection, projection, join, and result grain.
- Model one question through four representations: plain language, relational
  algebra, predicted tuples, and SQL.
- Use slides 1-10. Demonstrate the high-priority query, NULL predicates, newest
  active requests, and requester join before students adapt them.
- Load the complete fixture before the demonstrations and labs: 8 users,
  12 tickets, and 21 events. Use the SQL setup file or the notebook section titled
  **Use the Complete Week 2 Lab Dataset**. The earlier 4/6/9 notebook demonstration
  is a separate instance; running the entire notebook is not another assignment.
- Students complete the query ladder individually. The Harbor query changes the
  supplied requester join; have them inspect a matching and an excluded ticket
  in the CSVs. Their brief explanation stays in the same SQL file.

### Day 2 Arc

- Use slides 11-21. Retrieve matching pairs, then contrast the 10-row inner
  assignee join with the 12-row left join. Identify tickets 1004 and 1009.
- Follow ticket 1003's three events before grouping by status. Distinguish a
  ticket count from a count of ticket-event pairs.
- Explain the nested query and CTE, then work through slide 16's complete
  resolved-ticket report: Priya 2, Noah 2, Elena 0. Replace `count(r.ticket_id)`
  with `count(*)` to expose the incorrect 1 for Elena. Students later change
  the resolved filter to the lab's active definition.
- Demonstrate the complete transaction block for ticket 1002: medium, high
  inside the transaction, medium after rollback. Students use ticket 1006.
- Students complete the second lab and check one staff count by listing its
  ticket IDs. Use their existing SQL comments for the closing explanation;
  there is no additional exit submission.

**Live demonstration:** deliberately run a plausible but wrong join, compare row
counts, and repair it from the intended relationship. Roll back a test update.

**Likely misconceptions:** `DISTINCT` repairs a wrong join, `NULL` behaves like an
empty string, every selected column can accompany an aggregate, and successful
execution proves correctness.

**Equivalent path:** Notebook 1 runs in Colab or local Jupyter with DuckDB and no
cloud account. The labs can use any approved PostgreSQL environment.

**Teaching decision:** do not advance to schema administration if most students
cannot explain a one-to-many join result. Use the same relations and a different
visual representation before adding syntax.

## Week 3: Schema X-Ray, Keys, Constraints, and Index Vocabulary

**Student materials:** [Week 3 guide](../weeks/week_03/README.md),
[Chapter 3](../textbook/module_03_schema.md),
[SQL clinic](../weeks/week_03/lab_01_sql_clinic_schema_xray.md), and
[integrity lab](../weeks/week_03/lab_02_integrity_constraints.md).

**Prerequisite:** basic `SELECT`, joins, grouping, and safe DML from Week 2.

### Day 1 Arc

Use **slides 1-11**. The PowerPoint notes contain the full spoken script.

- Run slide 2's complete `count(*) FILTER` query before assigning its adaptation.
  All five categories remain. Their totals sum to 12 tickets and 4 resolved
  tickets. A top-level `WHERE status = 'resolved'` would remove parks and
  transportation. The lab's active version should sum to 7 active tickets.
- Review schema as design versus namespace, the copied-current-email anomaly,
  and the types used for identifiers, text, and timestamps. The dependency
  arrow means one current value per requester, not one ticket per requester.
- Run the metadata queries on slides 8-10. Six rows describe the six columns in
  `users`; they do not count its eight people. On the fresh PostgreSQL 15
  baseline, `tickets` has one primary key, two foreign keys, one timestamp
  check, and only its primary-key index. Inspect `is_nullable` separately.
- Students complete Lab 1 individually. Their single SQL file contains the
  report, inspection queries, and short comments tied to actual definitions.

### Day 2 Arc

Use **slides 12-20**. Begin with the mismatch between `IN PROGRESS` and
`in_progress`. No extra demonstration table is required.

- Use slide 14 to distinguish an existing rule from the priority `CHECK` being
  added. A requester foreign key proves that a person exists; it does not prove
  that an assignee has an agent role.
- Run slide 15's inspection query and add `tickets_priority_allowed` once. The
  fresh data contains high: 4, low: 3, medium: 4, and urgent: 1. If ADD reports an
  existing name, inspect the definition rather than deleting it reflexively.
- Run slide 17's invalid update alone. It should report SQLSTATE `23514` and
  `tickets_priority_allowed`, leaving ticket 1004 at `low`. Then run the valid
  transaction batch: `RETURNING` shows `high`; after `ROLLBACK`, the final query
  shows `low`. If a failed statement leaves an explicit transaction aborted,
  run `ROLLBACK` before attempting another test.
- Explain slide 18's three-valued logic: an allowed-list `CHECK` alone accepts
  `NULL`, but the baseline's separate `NOT NULL` rule rejects a missing priority.
- Students adapt the example to `tickets_status_allowed` and run Lab 2's tests
  individually. Leave expected-failure statements commented out in the final
  SQL file so a reviewer can run the successful path without stopping.
- Discuss the short explanation already required in that file: a database rule
  protects writes from an import or script as well as a form, but an allowed
  vocabulary does not decide who may close a ticket. Do not add a reflection
  form or separate writing submission.

**Likely misconceptions:** foreign keys automatically create all useful indexes,
application validation replaces database integrity, and a declared constraint is
proven without a rejection test.

**Equivalent path:** use the provided PostgreSQL setup SQL locally when Supabase
is unavailable. Both paths submit the same SQL file. Relevant values in comments
are sufficient; neither lab requires screenshots.

**Teaching decision:** if constraint names are remembered but bad-state reasoning
is weak, reteach from invalid rows and expected failures rather than definitions.

## Week 4: Views, Identity, Introspection, and Safe Migration

**Student materials:** [Week 4 guide](../weeks/week_04/README.md),
[Chapter 4](../textbook/module_04_change.md),
[views lab](../weeks/week_04/lab_01_views_identity.md), and
[safe migration lab](../weeks/week_04/lab_02_safe_migration.md).

**Prerequisite:** schema metadata, constraints, and transaction-guarded tests.

### Day 1 Arc

- Use slides 1-10. Create `active_ticket_summary`, then read its seven active
  identifiers and requester names. Explain the required requester relationship
  before students adapt it to the optional assignee relationship.
- State the append-only column rule for `CREATE OR REPLACE VIEW`. Distinguish a
  connection role from an identity column without beginning the Week 6 lesson.
- Create `demo_change_notes` once, run the three explicit transactions, and read
  retained IDs 1 and 3. The sequence allocated 2 even though its row rolled back.
- Students complete the two compact lab parts individually: the queue adaptation
  and their separate `change_notes` identity experiment. Both belong in one SQL
  file. Preserve their queue for Day 2.

### Day 2 Arc

- Use slides 11-21. Read the actual precheck, then run the complete rehearsal on
  slide 14 and repeat the catalog lookup after rollback.
- Model adding `source_channel` while preserving old records and old writers.
  Historical rows become `unknown`, not an invented channel such as `web`.
- Explain the CHECK, NOT NULL, and DEFAULT as three different rules. Students
  fill these clauses in the lab using the worked example as a reference.
- Students rehearse, roll back, then apply the migration in one SQL file with
  short comments and verification queries. No separate change report is required.
- Exit with a remaining risk outside the database command itself.

**Live demonstration:** slide 17 preserves the first six queue columns and
appends the new field. Slide 18 shows a valid update with rollback and a separate
invalid update. Verify 1004 and 1009, not just the seven-row count. The saved
Supabase screenshot on slide 16 shows a temporary-table rollback, not this
complete migration; its script explicitly explains the distinction.

**Likely misconceptions:** a view stores an independent copy by default, DDL
success proves every client still works, and rollback means only writing the
opposite command.

**Equivalent execution path:** use local PostgreSQL with the supplied complete
fixture. Without a working server, students can trace the worked results, but
that is preparation rather than completed execution. Restore access or provide
an instructor-managed practice database before assessing the operational lab.

**Teaching decision:** if students omit preconditions or verification, compare a
successful DDL message with an actual old-client query result. Repair that gap
through a small example rather than adding another paperwork requirement.

## Week 5: Transactions, MVCC, Locks, and Incident Communication

**Student materials:** [Week 5 guide](../weeks/week_05/README.md),
[Chapter 5](../textbook/module_05_transactions.md),
[transaction lab](../weeks/week_05/lab_01_transaction_outcomes.md),
[blocking lab](../weeks/week_05/lab_02_blocking_incident.md), and
[transactions/locks notebook](../notebooks/02_postgres_transactions_locks.ipynb).

**Prerequisite:** Week 4's commit/rollback boundary, basic UPDATE and INSERT,
primary keys, and a WHERE condition. Thread programming and advanced diagnostic
joins are not prerequisites. The notebook supplies the concurrency mechanics.

### Day 1 Arc

Use **slides 1-9**. Start with the relationship between current assignment and
history, before introducing the ACID vocabulary.

- Slide 4 runs the complete Noah/202/event-5998 rehearsal in `metro_support` and
  ends with rollback. Slide 5's fresh queries show that neither change remained.
- Slide 6 deliberately copies existing event 5001 to produce a duplicate-key
  error. Run the lower rollback/check block separately. Priority remains `low`.
- Slide 7's UPDATE matches zero rows without raising an error. Explain why the
  application must check the affected-row result before claiming an assignment.
- Students work individually in `transaction_lab`, assigning Priya/201 and event
  5999. They rehearse, commit, and test a failed new pair. One SQL file includes
  their observations and explanation. Day 1 does not require two connections.

The main fixture must begin with ticket 1004 unassigned and `new`. Do not commit
the instructor rehearsal into a student's source dataset. The lab's copy has
explicit primary keys but does not reproduce every original constraint; this
is a controlled transaction exercise, not a production schema-copy technique.

### Day 2 Arc

Use **slides 10-23** and Notebook 02. Its simplified row begins `medium / open`,
which differs deliberately from the full Metro Support fixture.

- Teach the three connection roles and visible row versions before the activity
  query. An ordinary reader sees `medium / open` while A sees `high / open`.
- Demonstrate `KEEP_A_CHANGE = False`. B is `active` but waits on a lock; A is
  `idle in transaction`. The captured `pg_blocking_pids` result identifies A as
  B's blocker. The notebook ends A and waits for B before the cell returns.
- Read the actual final row: `medium / in_progress`. Explain why a finished
  command and a verified data outcome are different observations.
- Students preserve that result, predict the commit case, change only
  `KEEP_A_CHANGE = True`, and rerun through cleanup. Expected final state:
  `high / in_progress`. B's SQL and the starting fixture remain unchanged.
- The comparison and developer-facing update share the notebook's final Markdown
  cell. There is no separate incident form, screenshot collection, or report.

The reading's write-skew example is enrichment. Introduce the snapshot distinction
without asking beginners to implement serializable retry logic. The optional
deadlock diagram extends a one-direction wait into a cycle; it is not a second
required live experiment.

**Connection preparation:** use a personal Supabase Session pooler URL and the
notebook's encrypted-connection setting. Do not substitute transaction pooling
or assume browser tabs are persistent sessions. The notebook obtains each PID
with `SELECT pg_backend_pid()` on the actual worker connection, and its diagnostic
query targets only those PIDs. Current local tests do not verify Supabase's UI,
TLS, network routing, or hosted permission policy; test the teaching connection
before class. Credentials are entered at the hidden prompt, never in saved cells.

**Likely misconceptions:** MVCC removes all locks, every delay is blocking, commit
and close-window are equivalent, and terminating a blocker explains the root
cause.

**Connection fallback:** the supplied rollback trace supports interpretation,
followed by a labeled prediction of the commit case. It does not demonstrate
that the student connected to or administered PostgreSQL. Arrange a live
connection demonstration when access becomes available, rather than calling
the static path equivalent execution.

**Teaching decision:** if students can name the blocker but cannot distinguish the
two final priorities, return to the single-row comparison. Ask which transaction
wrote each column and whether that transaction committed. A PID list alone is
not enough to decide what should happen to someone else's uncommitted work.

## Week 6: Roles, Grants, RLS, and Secret Boundaries

**Student materials:** [Week 6 guide](../weeks/week_06/README.md),
[Chapter 6](../textbook/module_06_security.md),
[least-privilege lab](../weeks/week_06/lab_01_least_privilege.md), and
[RLS lab](../weeks/week_06/lab_02_rls_test_harness.md).

**Prerequisite:** schema-qualified SELECT, GROUP BY from Week 2, views from
Week 4, and the transaction/rollback pattern from Week 5. Introduce authentication
and authorization explicitly; do not assume students know web tokens or RLS.

### Day 1 Arc

Use slides **1-11**. The first case asks why a valid login should not expose
another person's ticket. Slides 3-4 explain the vocabulary and actual reporting
requirement. Slides 5-8 contain the complete role/view setup, effective-role
observation, allowed query, and rollback-guarded denied update. The source fixture
must be fresh: the demonstrated open IDs are 1001, 1007, and 1011.

Run the slide 5 setup as the administrator in your personal practice project,
then slide 6. All demonstration roles and objects use `_demo` or `security_demo`;
they are separate from the book's `metro_analyst` and students' `_lab` roles.
Observe `session_user` and `current_user` from slide 5's lower batch. Execute the
allowed and denied actor tests as complete transactions, not as disconnected
web-editor commands. After an expected error, execute rollback separately if the
client stopped before reaching it.

Slide 9 explains the normal view owner's underlying-table privileges, including
why this reporting design is not automatically a resident-safe RLS interface.
Do not convert the view to `security_invoker` and then imply the existing
view-only grants will still suffice. Slide 10 distinguishes network, credential,
grant, and zero-row results.

Students adapt the pattern to the supplied analyst view. Their own grouped
query must work through that view under `metro_analyst_lab`; its counts sum to
12. This is useful work under the limited role, not another required report.
The supplied Colab cell only displays the SQL tests if the editor hides
intermediate results. Explain `tests` as a list of role/query pairs, one
rolled-back transaction per pair, and the connection's automatic close.

After Day 1, clean up only your demonstration:

```sql
DROP VIEW security_demo.open_ticket_report;
REVOKE USAGE ON SCHEMA security_demo, metro_support FROM report_reader_demo;
REVOKE report_reader_demo FROM CURRENT_USER;
DROP ROLE report_reader_demo;
DROP SCHEMA security_demo;
```

### Day 2 Arc

Use slides **12-24**. Begin with the actual four rows in slide 13. The required
lab is a database authorization experiment, not a Supabase Auth implementation.
Create the following fresh demonstration as the administrator after the Day 1
cleanup. It requires no retained changes to Metro Support:

```sql
CREATE ROLE resident_a_demo NOLOGIN;
CREATE ROLE resident_b_demo NOLOGIN;
GRANT resident_a_demo, resident_b_demo TO CURRENT_USER;
CREATE SCHEMA security_demo;
CREATE TABLE security_demo.resident_tickets (
    ticket_id integer PRIMARY KEY,
    owner_role text NOT NULL,
    subject text NOT NULL
);
INSERT INTO security_demo.resident_tickets VALUES
    (1, 'resident_a_demo', 'Broken bench'),
    (2, 'resident_a_demo', 'Dark streetlight'),
    (3, 'resident_b_demo', 'Missed pickup'),
    (4, 'resident_b_demo', 'Leaking hydrant');
GRANT USAGE ON SCHEMA security_demo TO resident_a_demo, resident_b_demo;
GRANT SELECT ON security_demo.resident_tickets TO resident_a_demo, resident_b_demo;
```

Before enabling RLS, slide 15's actor query returns all four rows. After the
first statement on slide 14 enables RLS, it returns none until the policy is
created. Then the same query returns 1/2 for A and 3/4 for B. Keep the effective
role visible. Slide 16's direct lookup returns no row for A, not SQLSTATE 42501.
This makes the difference between object permission and row filtering explicit.

Run slide 17's INSERT as the administrator. Without changing the policy,
Resident A now sees 1/2/5 and B still sees 3/4. Students later add their own
ticket 5 for **Resident 102**, not your demonstration's Resident A, and explain
why only that resident's result changes. They also run the direct lookup.

Slides 18-22 explain owner/bypass behavior, the verified-token request path,
UUID ownership mapping, USING versus WITH CHECK, and credential types. The
Supabase policy is explicitly an illustration: today's fixture has no mapped
Auth UUIDs and the lab grants residents SELECT only. Do not paste the illustration
into Metro Support or call a local role test a hosted authentication test.

For the final comments, ask for a short developer update about the observed
IDs and the remaining real-token test. Do not add a separate writing document.
Close the demonstration with this cleanup:

```sql
DROP SCHEMA security_demo CASCADE;
REVOKE resident_a_demo, resident_b_demo FROM CURRENT_USER;
DROP ROLE resident_a_demo;
DROP ROLE resident_b_demo;
```

**Likely misconceptions:** login equals authorization, RLS replaces all grants,
service-role credentials belong in frontend code, and one successful query establishes
least privilege.

**Connection preparation:** use a personal database account permitted to create
roles and assume the test roles. For Colab, the Supabase session pooler provides
an IPv4-compatible persistent route. Verify the current connection before class;
local PostgreSQL tests do not verify the hosted account, network, or editor UI.
Never use a student's real data to demonstrate a permission failure.

**Outage boundary:** a supplied result can support interpretation, but it does
not establish that a student's own role or policy ran. Arrange a functioning
practice connection for the operational portion instead of describing an
unexecuted trace as equivalent implementation.

**Teaching decision:** if an expected-deny result is missing, require the
allow/deny test pair under the intended role. An administrator view is not an
equivalent permission test.

## Week 7: Explain Plans, Measurements, and Index Design

**Student materials:** [Week 7 guide](../weeks/week_07/README.md),
[Chapter 7](../textbook/module_07_performance.md),
[plan-reading lab](../weeks/week_07/lab_01_plan_reading.md),
[index experiment](../weeks/week_07/lab_02_index_experiment.md), and
[performance fixture](../weeks/week_07/performance_lab_setup.sql).

**Prerequisite:** SELECT, WHERE, ORDER BY, LIMIT, GROUP BY, and the distinction
between a stored row and a query result. Index structure, selectivity, and plan
vocabulary are taught this week rather than assumed.

### Day 1 Arc

Use **slides 1-12**. Run the supplied performance fixture in your personal
practice database, then create this separate demonstration copy:

```sql
DROP SCHEMA IF EXISTS performance_demo CASCADE;
CREATE SCHEMA performance_demo;
CREATE TABLE performance_demo.tickets AS
SELECT * FROM performance_lab.tickets;
ALTER TABLE performance_demo.tickets ADD PRIMARY KEY (ticket_id);
ANALYZE performance_demo.tickets;
```

This copy isolates your demonstration from the student experiment and any
reading indexes. It is not a general database migration or backup method.
`performance_demo` is disposable and must contain only this demonstration.
The source has 100,000 tickets: 5,000 `in_progress`, 2,000 `open`, 3,000 `new`,
and 90,000 `closed`. Opening times are distinct, so the twenty IDs have a
deterministic order. Real applications with timestamp ties need a tie-breaker.

Slide 2 supplies the complete query for twenty newest `in_progress` tickets.
Show its result before adding EXPLAIN. The first five IDs are 99906, 99905,
99904, 99903, and 99902. Slides 4-8 explain execution safety and the captured
plan. In the locally tested baseline, the scan outputs 5,000 rows and removes
95,000; the sort examines all 5,000 candidates even though it emits only twenty.
The displayed plan is abbreviated and dated. Estimates and timings may differ
in your environment. Read the actual plan, never change settings merely to make
it resemble a slide.

Use slide 10's primary-key lookup to contrast a narrow index-supported question
with the queue's filtering and ordering. Slide 11 introduces join and aggregate
nodes as vocabulary for prior SQL, not another assigned join-tuning exercise.

Students complete Lab 1 for `open` tickets in `performance_lab`. Their change
from LIMIT 20 to LIMIT 5 tests the small-result misconception. On the supplied
unindexed status fixture, both scans still qualify 2,000 rows and remove 98,000.
They restore LIMIT 20 before Day 2. One SQL file contains the observation and
index hypothesis; no separate plan report or screenshot set is needed.

### Day 2 Arc

Use **slides 13-24**. Recreate the demonstration copy with the setup above if it
was changed. Run the exact slide 2 query and analyzed plan twice before adding
anything. Keep its twenty IDs and relevant plan lines. The setup has already
refreshed statistics; do not also refresh them between measurements.

Explain B-tree navigation and the two-column ordering example before the partial
index. Slide 16 creates one partial index on `opened_at DESC` for `in_progress`
rows. Rerun the unchanged query twice. In the local test the ordered index scan
returns twenty rows with no Sort, and all twenty IDs are unchanged. Slide 18
changes the predicate to `open` as a **separate counterexample**, not as part of
the before/after comparison. The partial index contains none of those rows and
cannot provide that queue's complete result. This supplies a concrete index
limitation without creating a second speculative index.

Slide 19 measures index bytes. Distinguish measured space from write overhead
that this SELECT experiment does not quantify. The example recommendation
names the observed result and a deployment limit without asking students to
claim production experience.

Students create the supplied composite `(status, opened_at DESC)` index for
their open queue. This is different from your partial-index demonstration.
They compare the same twenty IDs, scan/sort work, repeated measurements, and
storage, then write a developer update inside that one SQL file. A supported
`test further` recommendation is acceptable when their observed plan differs.

After your demonstration, remove only its schema:

```sql
DROP SCHEMA performance_demo CASCADE;
```

**Live demonstration boundary:** all analyzed commands are SELECTs on synthetic
data. Standard CREATE INDEX is appropriate here, not a universal production
deployment command. Never disable planner strategies to manufacture a win or
benchmark a destructive write in a live service.

**Likely misconceptions:** sequential scan is always bad, index scan is always
good, lower one-time runtime proves a lasting improvement, and indexes have no
write or storage cost.

**Connection fallback:** the deck's dated plan excerpts support analysis and
prediction during an outage. They do not establish that the student created
or measured an index. Provide a working local PostgreSQL or rescheduled live
path for the execution outcome; do not call a copied plan an equivalent run.

**Teaching decision:** if students recommend from node name alone, compare two
plans with different table sizes/selectivities before recovery work.

## Week 8: Logical Backup, Verified Restore, and Midterm Integration

**Student materials:** [Week 8 guide](../weeks/week_08/README.md),
[Chapter 8](../textbook/module_08_recovery.md),
[backup/restore notebook](../notebooks/03_postgres_backup_restore.ipynb),
[recovery lab](../weeks/week_08/lab_01_backup_restore.md), and the canonical
[midterm operations case](../assignments/midterm_project.md).

**Prerequisite:** read a three-table schema, follow a simple join, distinguish
commit from rollback, and interpret the earlier permissions and plan examples.
Teach RPO/RTO here rather than assuming students already know recovery vocabulary.

### Day 1 Arc

- Slides 1-7 introduce the committed-deletion problem, recovery mechanisms,
  the worked clock-time calculation, and the dated Supabase Free screenshot.
- Slides 8-15 teach the notebook's smaller fixture, Python/tool/SQL layers,
  archive, separate restore, and actual expected results. Explain the options
  before asking students to use them.
- Demonstrate the notebook through ticket 1001, then the changed-subject example
  below. Students adapt the supplied query to 1002 or 1003 and explain the added
  check in their notebook. They do not create an additional checklist or report.
- Use the notebook's final cleanup after the recovery account. Colab's practice
  service stops; an existing local PostgreSQL service remains running.

### Day 2 Arc

- Slides 17-20 rehearse a nullable-column migration and distinguish rollback,
  a corrective change, restore, and resolving a waiting writer.
- Slides 21-23 connect a specific problem to one improvement and show a concise
  recovery handoff. Both transaction control and blocking are in the midterm;
  one does not substitute for the other. The recovery plan is required, while
  executing a further midterm restore is optional.
- Students work individually on the canonical midterm, repair one incomplete
  part, rerun it, and update the explanation. No separate clinic submission.

### Instructor Demonstration: Counts Can Miss a Changed Subject

Run Notebook 3 through the supplied known-ticket check, but not cleanup. Add a
temporary demonstration code cell to your own copy. The transaction changes
only the restored subject, displays the count and ticket, and rolls back. The
student task is different: check another ticket against its intended source.

```python
demo_sql = """
BEGIN;
UPDATE metro_support.tickets
SET subject = 'Incorrect subject' WHERE ticket_id = 1001;
SELECT count(*) FROM metro_support.tickets;
SELECT ticket_id, subject FROM metro_support.tickets WHERE ticket_id = 1001;
ROLLBACK;
"""
demo = subprocess.run(
    PG_PREFIX + [PSQL, '-X', '--set=ON_ERROR_STOP=on', '--dbname', RESTORE_DB,
                 '--command', demo_sql],
    check=True, text=True, capture_output=True,
)
print(demo.stdout)
```

Expected inside the transaction: count `3`, but ticket 1001 has `Incorrect
subject`. Rerun the notebook's known-ticket check afterward: rollback restored
`Streetlight dark near bus stop`. Ask what the count failed to establish, then
explain why a record-value comparison addresses that gap.

For Day 2, replace `demo_sql` in the same temporary cell with slide 18's
`BEGIN; ALTER TABLE ...; SELECT ...; ROLLBACK;` example. Inside the transaction,
the catalog query returns `follow_up`. Afterward, rerun only the catalog query:
there should be no result. Use the disposable notebook target, not the midterm
project or a cloud source. Keep this instructor rehearsal out of the student's
required lab submission. Run notebook cleanup when demonstrations are finished.

**Likely misconceptions:** sync/replication equals backup, restore into the source
is the safest test, command success proves behavioral correctness, and free cloud
tiers guarantee native backups.

**Access path:** Notebook 3 creates disposable PostgreSQL databases without a
cloud secret. If Colab startup fails, help the student use a local/instructor-
provided PostgreSQL environment and the same notebook. The deck's worked results
can support discussion during troubleshooting, but reading them is not equivalent
to performing the required restore. Do not claim an unavailable transcript or
cloud path has been supplied or tested.

**Teaching decision:** if the explanation is weak, have the student revisit the
query they already adapted and explain which changed value it would detect.
Grade the connection between the result and the claim, not the length of a report.
