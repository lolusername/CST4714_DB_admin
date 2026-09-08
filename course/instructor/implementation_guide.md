# Course Implementation Guide

## Scope and Use

This public guide supports a two-meeting-per-week implementation of *Operating
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

Weeks 2-15 contain an optional industry extension. Week 1 has one integrated case.
An extension is ungraded, adds
no submission, and must never become an unstated prerequisite. Offer it only when
time and interest permit; a student who uses the standard lab or equivalent
fallback receives no penalty or reduced access to later work. The
[currentness, pedagogy, and QA audit](../../oer_fellowship/evidence/CURRENTNESS_PEDAGOGY_QA_AUDIT.md)
records the research basis and extension inventory.

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

## Week 9: NoSQL Evolution, Model Families, JSON, and Atlas Orientation

**Student materials:** [Week 9 guide](../weeks/week_09/README.md),
[Chapter 9](../textbook/module_09_nosql_json.md),
[CSV-to-JSON lab](../weeks/week_09/lab_01_csv_to_json.md), and the
[Metro Support CSV data](../datasets/metro_support/README.md). The worked examples
use ticket 1001. The assigned lab uses ticket 1003. Neither day assigns Mini
Inventory or a second dataset.

**Prerequisite:** relational model, keys, relationships, and access questions.

### Day 1 Arc

**Slides 1-16.** Begin with IDs, foreign keys, and one-to-many event history.
Students have already used these ideas; documents will relocate facts rather than
erase their relationships. Recover the distinction between a stable ID and a
changeable name before discussing embedding.

The history connects Codd, the earlier relational NoSQL name, Bigtable, and
Dynamo to differing operating requirements. Explain key-value and wide-column
examples through their keys before introducing additional terminology. The
wide-column example is a Bigtable-style row-key illustration, not a Cassandra
deployment recipe or a claim about analytical columnar storage.

**Graph walkthrough, slides 8-9:** four vertices and four directed edges. Every
arrow means `depends on`. Portal's outgoing neighbors are Identity and API.
Database is two hops away. Breadth-first levels are `{Portal}`, `{Identity, API}`,
then `{Database}`. The visited set prevents counting Database twice and terminates
cycles. For possible impact after Database fails, traverse incoming relationships
in reverse. Reachability alone cannot prove an outage because fallback behavior
is absent from the graph. Fewest hops also differs from minimum weighted cost.

**Vector walkthrough, slides 10-14:** define an ordered coordinate list before
using an embedding example. The text model creates coordinates; the database
searches them. Calculate dot products and lengths aloud for `q=(1,0)`,
`a=(10,0)`, and `b=(1,1)`. Cosine ranks A first with scores 1 and about 0.707.
Euclidean distance ranks B first with distances 9 and 1. These are invented
coordinates illustrating geometry, not measured language embeddings. Explain
why cosine is undefined for the zero vector. On the same unit-normalized vectors,
the exact rankings agree because squared distance equals `2 - 2*cosine`.

The recall example has exactly three overlapping IDs in two five-ID lists, so
recall at five is 0.6 for that query. Separate retrieval agreement from human
relevance and permissions. Do not create vector services, paid accounts, or
embedding API calls for this lesson.

**Individual practice, slide 16:** students choose a ticket-page representation
and explain a consequence for event reports or name changes in their own notes.
Discuss a relational answer alongside a document answer. This is practice, not
another graded deliverable or a group activity.

### Day 2 Arc

**Slides 17-32.** Teach JSON types and punctuation before asking students to
recall them. Use six value kinds; true and false are the Boolean alternatives,
not separate types. Read braces as an object, brackets as an array, a colon as
the name/value connection, and commas as separators. Show why an unquoted null
differs from a string containing `null`.

Repair `{'status': 'open',}` in two changes: double quotes and removal of the
trailing comma. Explain absent fields, explicit null, empty arrays, and zero.
Distinguish a JSON timestamp string from a stored BSON Date. No parser execution
is required. If demonstrating one, use `JSON.parse` in a trusted local JavaScript
environment for the small course-authored examples. Python's default `json.loads`
accepts NaN/Infinity extensions, and both common parsers can accept duplicate
names. Do not describe either default as a complete interoperability validator.

**Worked modeling, slides 24-28:** open the three CSVs and locate ticket 1001,
Maya 101, Priya 201, and events 5001/5002. Read the timestamps from the source.
Both complete JSON examples preserve the same selected facts. The referenced
object packages arrays for interchange; writing it does not create collections.
In the embedded object, containment supplies the event's ticket relationship.
Contrast a stale current-name copy with a deliberately historical name. End with
the five-event preview and separate authoritative history, including the refresh
and multi-document coordination responsibilities.

**GitHub demonstration, slide 29:** in a disposable instructor-owned repository,
create a Markdown file with a heading, a fenced JSON block, and a paragraph.
Show Preview, edit one line, and Commit changes. Show the raw-file download for
Brightspace. Preview formats Markdown, and commit records text; neither proves
valid JSON. Students can instead use a local editor. Do not require a public
repository or an extra repository-link submission.

**Atlas orientation, slide 30:** use the linked official Free-cluster guide and
the free MongoDB University overview/deployment/interface lessons as references.
Select Free / M0 only. Explain account/project management, database users, and IP
access as distinct layers. The browser's public source IP can differ from
Colab's. Do not add `0.0.0.0/0` merely to demonstrate the interface, disable TLS,
show a password, or purchase a paid workaround. If the UI differs or setup stalls,
use the reference and proceed to the text-only lab. No configuration screenshot
or MongoDB University completion is due in Week 9.

**Individual lab:** use ticket 1003, requester Amina Yusuf (103), assignee Priya
Shah (201), and events 5005/5006/5007. The current status is `resolved`. Required
event types are `created`, `status_changed`, `status_changed`. Students retain the
actual timestamps from the CSV, but need not retain every source column. One
Markdown file holds both complete JSON designs and the short tradeoff paragraph.
Reading guidance points to the paired example in Chapter 9. Full spoken
explanations for every slide are in the deck's Notes, not teaching directions.

**Feedback without more deliverables:** first check that both shapes retain the
same required facts. Then check one read and one change explanation. A student
who only nests arrays differently has not yet explained a modeling decision.
Help them identify whose current name a field represents or where an event goes
after the five-event preview fills. Use those concrete operations rather than
requiring an additional design report.

**Likely misconceptions:** NoSQL means no schema or no queries, JSON allows single
  quotes/comments/trailing commas, vectors store only images, and one model family
  replaces all others.

**Equivalent path:** the entire required lab uses CSV and JSON text; no Atlas query
or MongoDB University completion is required for the core evidence.

**Teaching decision:** if students copy tables directly without a workload
explanation, ask one read and one update question before MQL begins.

## Week 10: Basic MQL and Access-Pattern Modeling

**Student materials:** [Week 10 guide](../weeks/week_10/README.md),
[Chapter 10](../textbook/module_10_mql_modeling.md),
[MQL notebook](../notebooks/04_atlas_mql_modeling.ipynb),
[MQL lab](../weeks/week_10/lab_01_atlas_mql.md), and
[document-model lab](../weeks/week_10/lab_02_document_model.md).

**Prerequisite:** valid JSON, document/collection vocabulary, and relationship
cardinality.

### Day 1 Arc

Use **slides 1-17**. The lesson's worked code uses Python, while Chapter 10 labels
its runnable examples as mongosh. Make that boundary explicit before live coding.
The student submission remains one notebook, not a sequence of separate reports.

Begin with the six-row table on slide 6. For the active high/urgent queue, 1001
qualifies and 1003 does not: its priority is urgent, but its status is resolved.
The table gives students a way to predict an answer without understanding every
line of the fixture setup. Do not spend the class typing the entire supplied
fixture. Explain one document, then run the prepared setup.

Run the notebook's connection cells before the query demonstrations. Local mode
uses `mongomock`, which is not a MongoDB server or an Atlas deployment. It supports
the operations in this exercise without cloud credentials, but does not establish
network, durability, or performance behavior. Package installation needs internet
even in local mode. In Atlas mode, the first setup cell prints the runtime's
outgoing IPv4 address and a new database name. Stop there while students add the
temporary address and configure the database user. The later hidden-prompt cell
connects and pings. A website login, network entry, and database user's privileges
solve different parts of the connection problem.

The notebook leaves TLS certificate checks enabled and suppresses the original
connection exception in its user-facing error, because a URI can carry secrets.
It clears the separate URI variable even if the connection fails. A working ping
does not prove permission to insert or delete; those operations are tested next.
Students should not use unrestricted network access to work around a failed IP
check. After a Colab runtime change, check the runtime IP again.

Use slides 7-11 with the corresponding notebook cells. The array counterexample
is the essential conceptual pause: ticket 1001's event 5001 is resident-created,
while 5002 is agent-assigned. Separate dotted conditions match the document, but
no event satisfies both `created` and `agent`. The useful `$elemMatch` version for
`status_changed` by `agent` returns 1002 and 1003. A filter selects documents;
including the entire events field in a projection can return nonmatching events
inside a qualifying document. Do not imply that the filter trims the array.

For slides 12-16, insert/reset test ticket 1099 once, run the `$set` cell twice,
and then run the expected-state cell. The results are respectively `1/1`, `1/0`,
and `0/0`. **Do not rerun insertion between the repeated updates.** The first
pair means a matched document changed. The second means the values were already
present. The last means the additional `status: new` condition did not hold.
Read the stored state after each case. The guarded append of event 5999 stays
at one event when repeated. It is a separate write from the earlier status update;
the Day 2 demonstration below makes the atomicity contrast concrete.

The first deletion reports one, its repeat reports zero, and the six teaching
tickets remain. The final cleanup removes only this run's practice `tickets`
collection and closes the client. It does not delete or stop the Free cluster.
Students remove their temporary IP rule and any class-only database user when
finished. No hosted-account screenshot is part of Lab 1.

Student work changes a filter and one projected field, then explains an actual
returned ticket, the array counterexample, and the write results in the notebook's
single response cell. If students can execute syntax but cannot explain an ID,
return to the six-ticket table rather than adding another assignment.

### Day 2 Arc

Use **slides 18-28**. The instructor's external activity is specifically
[Modeling Data Relationships, Lesson 3: Modeling One-to-One](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-3-modeling-one-to-one/learn)
and its Practice activity. Show both an embedded and a referenced interpretation
of the one-to-one relationship. The student's external activity is
[Lesson 4: Modeling One-to-Many](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn)
and [Lesson 4 Practice](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1).
Do not demonstrate or complete that student Practice activity live.

The public lesson menus were checked September 8, 2026. The newer Relational
(SQL) to Document Model course lists videos in its Model for Workloads and
Design Relationships sections; its relationship videos overlap the older course.
Different course titles did not establish distinct hands-on work. The present
assignment names different lessons and Practice activities explicitly. The
optional workload video in the weekly guide is support, not an interactive lab.
Authentication-gated Practice internals and hosted completion behavior still
need the instructor's pre-class check. Do not promise a numerical score if the
interface only reports progress.

After the one-to-one example, demonstrate a course-authored ticket update and
page read. Use a fresh blank notebook with `mongomock` installed by Notebook 04,
or run its installation cell first. This self-contained version avoids depending
on yesterday's cleaned-up database. It models database operations locally; it
does not claim to demonstrate Atlas networking. The demo uses ticket 1001,
while the student transfer uses ticket 1003 and three events.

```python
from datetime import datetime, timezone
import mongomock

demo_client = mongomock.MongoClient()
demo_database = demo_client["week10_live_demo"]
demo_tickets = demo_database["atomic_tickets"]
page_tickets = demo_database["page_tickets"]
people = demo_database["people"]
history = demo_database["history"]

demo_tickets.insert_one({"ticket_id": 1001, "status": "open", "events": []})
page_tickets.insert_one({"ticket_id": 1001, "requester_id": 101, "status": "open"})
people.insert_one({"user_id": 101, "display_name": "Maya Chen", "email": "maya.chen@example.org"})
history.insert_many([
    {"event_id": 5001, "ticket_id": 1001, "event_type": "created",
     "event_at": datetime(2026, 2, 1, 23, 10, tzinfo=timezone.utc)},
    {"event_id": 5002, "ticket_id": 1001, "event_type": "assigned",
     "event_at": datetime(2026, 2, 2, 14, 5, tzinfo=timezone.utc)},
])
history.create_index([("ticket_id", 1), ("event_at", -1), ("event_id", -1)])
```

Slide 21 combines changes in one document. Run this block twice. The first result
is `1 1`, the second is `0 0`, and only one event 5099 exists. The property is
single-document atomicity plus an expected-state filter. A local teaching
substitute illustrates the result; MongoDB's atomicity guarantee comes from the
database specification, not from a concurrency test on this mock.

```python
result = demo_tickets.update_one(
    {"ticket_id": 1001, "status": "open"},
    {
        "$set": {"status": "in_progress"},
        "$push": {"events": {"event_id": 5099, "type": "status_changed"}},
    },
)
print(result.matched_count, result.modified_count)
print(demo_tickets.find_one({"ticket_id": 1001}, {"_id": 0}))
```

Slide 24 uses a **separate** referenced example, still in state `open`. The two
collections represent alternative designs, not a synchronized pair. Each event
stores `ticket_id`, so the parent does not carry an unbounded array of event IDs.

```python
ticket = page_tickets.find_one({"ticket_id": 1001}, {"_id": 0})
person = people.find_one({"user_id": ticket["requester_id"]}, {"_id": 0})
recent = list(history.find(
    {"ticket_id": ticket["ticket_id"]}, {"_id": 0}
).sort([("event_at", -1), ("event_id", -1)]).limit(2))
print(ticket["status"], person["display_name"])
print([event["event_id"] for event in recent])
```

Expected: `open Maya Chen` and `[5002, 5001]`. Update the authoritative person,
then rerun the page read to show why the reference supports independent changes.
This synthetic new email is a demonstration value, not a correction to the CSV.

```python
people.update_one({"user_id": 101}, {"$set": {"email": "maya.updated@example.org"}})
print(people.find_one({"user_id": 101}, {"_id": 0, "email": 1}))
print(page_tickets.find_one({"ticket_id": 1001}, {"_id": 0}))
```

The ticket stays unchanged. A real application also handles missing users and
decides what consistency is required across separate reads. The index is a
candidate access path, not a benchmark result from this tiny example. At the end:

```python
demo_client.drop_database("week10_live_demo")
demo_client.close()
```

### Student Transfer and Discussion

Lab 2 is one design, not a repeat of Week 9's two-design comparison. Students
revise ticket 1003 for a page showing the latest **two** events, while retaining
all history and allowing one authoritative contact update. Expected displayed
IDs are **5007, then 5006**; 5005 still belongs in retained history. A referenced
history is a straightforward answer. A bounded recent-event copy is also
defensible if the student explains its refresh and stale-data behavior. Do not
require a hybrid or runnable MQL. The explanation addresses a developer and
connects stored shape with actual reads, updates, and growth.

If the external Practice cannot be accessed, students use the chapter's worked
examples and note the substitution. No additional proof file or full badge is
required. The weekly guide's optional game scenario remains ungraded.

When interpreting vendor material, clarify that SQL databases do not impose
third normal form automatically, PostgreSQL supports arrays and JSON, and both
relational and document designs consider access patterns. A join is an operation
with workload-dependent costs, not proof of a defective design. Keep those
comparisons technical rather than treating a vendor slogan as a general rule.

**Equivalent path:** Notebook 4 uses `mongomock` by default. The course-authored
model comparison remains available if MongoDB University or Atlas is unavailable.

**Teaching decision:** if CRUD syntax succeeds but model reasoning is weak, use a
growing/unbounded history example before aggregation.

## Week 11: Aggregation, Validation, Sort Performance, and Case Writing

**Student materials:** [Week 11 guide](../weeks/week_11/README.md),
[Chapter 11](../textbook/module_11_mongodb_operations.md),
[aggregation notebook](../notebooks/07_aggregation_validation.ipynb),
[pipeline/validation lab](../weeks/week_11/lab_01_pipeline_validation.md), and
[sort/case response lab](../weeks/week_11/lab_02_sort_and_case_response.md).

**Prerequisite:** basic MQL, embedding/referencing tradeoffs, and index evidence
from PostgreSQL.

**Deck navigation:** slides 1-16 support Day 1 and slides 17-28 support Day 2.
Each slide has a word-for-word script in its PowerPoint notes. The matching
transcript contains the same script; this guide supplies preparation and live
code rather than another required student deliverable.

| Slides | Teaching work | Companion material |
|---|---|---|
| 1-7 | SQL grouping review, four-ticket fixture, stage outputs, field paths | Notebook 07 setup and worked pipeline |
| 8-11 | Conditional count, newest date, equal-total identity error | Lab 1's summary change and explanation |
| 12-16 | Required fields, BSON dates, installed rule, counterexamples | Lab 1's validation change and cleanup |
| 17-23 | Queue query, compound order, measured work, remaining fetch | The separate mongosh sort demonstration below |
| 24-28 | Incorrect stage rewrite, external sort lab, inventory recommendation | Lab 2's single Brightspace submission |

### Day 1 Arc

Use the four-ticket fixture in Notebook 07, not retained Week 10 data. Read its
IDs and statuses before discussing operators. Active means `new`, `open`, or
`in_progress` in this application. Resolved requests still exist; they simply do
not belong in this report. The correct active IDs are 1001, 1002, and 1004.

**Explain what one document represents.** This is the meaning of "grain," not a
new command. Before grouping, one document is one ticket. After grouping, one
document is one category summary. MongoDB has not replaced the stored tickets
with summaries; this read-only pipeline produces a result. Walk the supplied
loop one stage at a time: `$match` produces three tickets, `$group` produces two
category summaries, `$project` gives those summaries their display fields, and
`$sort` puts sanitation before streetlight. `$sum: 1` counts each input reaching
the group. It does not somehow remember unique tickets from an earlier stage.

The dollar sign has two related but different roles. `$group` names an operator.
Inside its expression, `"$category"` reads a field value. Plain `"category"` is a
literal string and would put every input into the same named group. The group
output's `_id` is the group key, not a request's original MongoDB `_id`. Projection
renames that key to `category`. These small language distinctions are more useful
to beginners than a long list of unfamiliar stages.

**Give students one report change.** They add urgent count and newest opening
using the provided expressions, then include both fields in `$project`. The
expected sanitation row has active count 1, urgent count 0, and February 2 as its
newest opening. Streetlight has active count 2, urgent count 1, and February 4.
Streetlight's source tickets are 1001 and 1004. Ticket 1003 is urgent but resolved,
so it must not contribute. `$cond` produces 1 or 0 for each qualifying ticket;
`$sum` combines those values. `$max` compares the stored BSON dates. A date display
may include midnight and an offset; do not mistake that formatting for a
different calendar day in this UTC fixture.

**Investigate the convincing wrong result.** The unwind example produces IDs
1001, 1001, and 1002. Its total is three, exactly the correct active-ticket total,
but it duplicates 1001 and loses 1004, whose event array is empty. Even category
totals happen to agree here: two streetlight rows and one sanitation row. Ask
students to identify the source IDs rather than trust either total. An urgent
count after unwind would expose another consequence: the urgent 1001 contributes
twice. `preserveNullAndEmptyArrays` can retain 1004, but cannot prevent 1001's two
rows. Do not add deduplication machinery to a ticket count that never needed
unwind. For an event report, unwind is appropriate and the result should be
labeled as events. This connects to one-to-many SQL joins without assigning a
second SQL lab.

**Teach a rule with a positive test and counterexamples.** The starting validator
requires `ticket_id`, `status`, and `subject`, while allowing other fields.
Students add `opened_at` to `required` and a `bsonType: "date"` property, then
rerun the validator cell. `required` tests presence; the property checks the
value's type. Neither alone expresses the complete date requirement. The test
cell accepts a valid Python `datetime` encoded as BSON Date, rejects
`almost_done`, rejects a timestamp stored as text, and rejects a missing date.
Expected validation failures have code 121. A duplicate ID is a different failure
(11000), while insufficient permission is not proof of validation at all.

The two date cases are enabled only after the student adds the date rule. If they
have not edited it, the cell explicitly says those cases are not enabled. It
removes its own temporary IDs after testing, so another run does not pollute the
four-ticket summary. Installing a validator does not repair old documents. A rule
that an assignee exists elsewhere also is not enforced by this schema. The book
has a broader example with more required fields; the notebook intentionally adds
one rule at a time rather than copying that entire schema.

**Choose the execution path honestly.** Local mode runs the aggregation, but
`mongomock` does not implement server-side validation. Its supplied trace can be
interpreted, not described as an executed database rejection. Students can finish
the same notebook assignment using this path. Atlas users need their runtime's
temporary `/32` rule, a database user rather than a website login, and permission
to modify the practice collection's validator. Test the instructor's `collMod`
permission before class; successful ping or CRUD does not prove it. If permissions
are missing, keep the local path rather than spending the period broadening
account privileges. Cleanup drops only this run's `tickets` collection and closes
the connection; students also remove their temporary IP entry.

**One submission.** The notebook contains the modified pipeline, modified rule,
outputs, and one editable explanation cell. Grade whether students support their
summary with source IDs, diagnose the duplicated/lost request, and correctly
interpret both date failures. Do not require a screenshot, extra source file, or
second report. A correct local trace interpretation and an actual Atlas test are
different kinds of work, but the assigned conceptual standard is the same.

### Day 2 Arc

- Retrieve stage order and compound-index reasoning.
- Students complete the free external **Improving Performance of $sort stages
  (Lab Only)** activity individually.
- Connect completion to a course-authored explanation of filter, sort, index
  evidence, and cost.
- Students submit the redacted completion evidence and the 200-300 word case-study
  response as one Brightspace text response. No separate Markdown file is needed.

**Live demonstration:** use the exact setup and query below while presenting
slides 18-23. Slide 24 returns to the four-ticket case: matching open tickets
before sorting and limiting returns 1001, while limiting to the newest ticket
before matching open returns nothing because 1004 has status `new`. This
counterexample prevents a blanket instruction to reorder stages for speed.
Slides 25-28 connect correctness, validation, and performance to the individual
lab and writing response. The following week's handoff remains replication,
consistency, and recovery, as specified in the syllabus.

### Day 2 Live Sort Demonstration

Use the following **mongosh** example for the instructor demonstration, not as an
additional student assignment or a Python cell. It creates a separate synthetic
10,000-ticket workload. It is not the original Metro Support CSV data. Its larger
size makes examined-document counts meaningful without needing a large or paid
deployment. Run the setup before the live explanation; students need to read the
query and index, not memorize fixture-generation syntax.

Use an instructor practice database on a local MongoDB server or an already
available personal Atlas deployment. Do not change a shared course collection.
Run this setup once, and retain its printed name for cleanup:

```javascript
const sortPracticeName = "cst4714_sort_" + new ObjectId().toHexString().slice(-8);
db = db.getSiblingDB(sortPracticeName);
print(sortPracticeName);
db.sort_tickets.createIndex({ ticket_id: 1 }, { unique: true });
db.sort_tickets.insertMany(Array.from({ length: 10000 }, (_, i) => ({
  ticket_id: 30000 + i,
  status: i % 5 === 0 ? "open" : "resolved",
  opened_at: new Date(Date.UTC(2026, 1, 1) + i * 60000),
  subject: "Synthetic request " + i
})));
```

The workload is "show the newest twenty open requests." Equality on `status`
selects the relevant group. The two descending sort keys give newest first and
a unique ticket-ID tie-breaker. A limit means at most twenty qualifying requests,
not twenty arbitrary inputs filtered afterward. We include the subject in the
result, so the proposed index is not a covering index for this projection.

```javascript
const filter = { status: "open" };
const projection = { _id: 0, ticket_id: 1, opened_at: 1, subject: 1 };
const order = { opened_at: -1, ticket_id: -1 };
const beforeRows = db.sort_tickets.find(filter, projection).sort(order).limit(20).toArray();
const before = db.sort_tickets.find(filter, projection).sort(order)
  .limit(20).explain("executionStats");
printjson({
  returned: before.executionStats.nReturned,
  documents: before.executionStats.totalDocsExamined,
  keys: before.executionStats.totalKeysExamined,
  plan: before.queryPlanner.winningPlan
});
```

Locate the collection scan and blocking sort in the winning plan. Plan nesting
can vary by MongoDB version; do not teach one screenshot path as a universal
schema. Returned records and examined work answer different questions. The
single-field unique ID index protects identity, but does not provide this
status-and-time access path.

Now add one candidate index, then run the same read and inspect its plan:

```javascript
db.sort_tickets.createIndex(
  { status: 1, opened_at: -1, ticket_id: -1 },
  { name: "open_by_recent" }
);
const afterRows = db.sort_tickets.find(filter, projection).sort(order).limit(20).toArray();
const after = db.sort_tickets.find(filter, projection).sort(order)
  .limit(20).explain("executionStats");
printjson({
  returned: after.executionStats.nReturned,
  documents: after.executionStats.totalDocsExamined,
  keys: after.executionStats.totalKeysExamined,
  plan: after.queryPlanner.winningPlan,
  sameOrderedIDs: JSON.stringify(beforeRows.map(row => row.ticket_id)) ===
                  JSON.stringify(afterRows.map(row => row.ticket_id))
});
```

For this exact fixture on the audit's local MongoDB 8.0.29 server, the initial
plan returns 20 and examines 10,000 documents with zero index keys. After the
index, the plan returns the same twenty IDs and examines 20 documents and 20
keys, with no blocking sort. The first ID is 39995, then 39990, down to 39900.
These are reproducible observations for this fixture, not a timing guarantee.
Read the current run rather than asserting another server must choose the same
plan. `FETCH` is expected because the query returns the subject, which is absent
from the index. Twenty examined documents is not a failed optimization.

The index orders all statuses, not only open requests; its name is a reminder
of the demonstrated workload, not a partial-index predicate. Its equality prefix
narrows the scan to open entries, and the remaining keys already provide the
requested order. Inserts and relevant updates must also maintain this index,
and its entries consume storage. Do not describe a 500-to-1 reduction in examined
documents as a 500-times runtime speedup. There is also no need to teach sharding
to solve this bounded query problem.

```javascript
db.getSiblingDB(sortPracticeName).sort_tickets.drop()
```

This removes only the demonstration collection. It does not stop a hosted
deployment. The student activity remains the separately linked MongoDB University
sort lab, followed by one inventory-video response.

The phrase "when semantics permit" matters. Moving a filter on a field computed
by `$group` before that group is not an optimization of the same query. Likewise,
limiting all requests before filtering to open requests does not mean "newest
open requests." Demonstrate the query whose output is needed, then assess the
work it does. Do not infer a speedup from a four-ticket timing measurement.

For the video response, distinguish observation from recommendation. A student
can propose an index or validation rule using today's concepts without claiming
the presenter used that exact mechanism. Grade the connection between a
locatable design decision, its workload, and a real cost; do not require a
generic claim that MongoDB is faster. The student University sort activity stays
separate from the instructor's course-data demonstration.

**Likely misconceptions:** pipelines are unordered lists, `$group` preserves one
row per source document, validation fixes old data, and an index that supports a
sort is free.

**Equivalent path:** Notebook 7 runs aggregation locally. Its labeled validation
trace supports interpretation but is not a server test. If MongoDB University is
unavailable, use the Chapter 11 plan example and the lab's stated fallback.

**Teaching decision:** if students list stages without tracking shape/grain,
rebuild the pipeline on the notebook's four documents before reliability.

## Week 12: Replication, Reliability Promises, and Logical Recovery

**Student materials:** [Week 12 guide](../weeks/week_12/README.md),
[Chapter 12](../textbook/module_12_reliability.md),
[reliability lab](../weeks/week_12/lab_01_reliability_decisions.md),
[MongoDB recovery notebook](../notebooks/05_mongodb_logical_recovery.ipynb),
[recovery lab](../weeks/week_12/lab_02_mongodb_recovery.md), and the canonical
[final project](../assignments/final_project.md).

**Prerequisite:** transactions, PostgreSQL recovery, MQL, validators, and indexes.

### Day 1 Arc

- Retrieve replication versus backup and failure versus recovery.
- Model a reliability claim as promise, mechanism, failure case, and verification.
- Trace primary, secondaries, acknowledgment, election, and client interruption
  without promising zero data loss or zero downtime.
- Students complete the reliability-decisions lab individually.
- Introduce the final only through the canonical file and one planning checkpoint.

### Teaching the Read and Write Controls

Use one new request throughout the explanation. A, B, and C are voting,
data-bearing members. A is already primary. A and B can exchange messages,
while C cannot reach them. This is a supplied reasoning trace, not a live Atlas
failover exercise.

| Moment | A | B | C | What the application can conclude |
|---|---|---|---|---|
| Before submission | request absent | request absent | request absent | Nothing has been recorded yet |
| A applies the insert | request present | not yet applied | request absent | One copy has changed; the requested majority acknowledgment is not yet established |
| B receives and satisfies the required acknowledgment | request present | request present | request absent | A majority is available in this three-data-bearing-member example; the isolated C need not acknowledge |
| A later read uses C's older eligible state | request present | request present | request absent | A missing result can reflect lag, not loss of the acknowledged request |

Explain the three controls separately before combining them. **Write concern**
sets the acknowledgment the client waits for. **Read preference** selects
eligible members. **Read concern** constrains the state a read may return.
Majority read concern by itself does not make every secondary immediately
current. A causal session orders related operations and carries the dependency
from a write to a later read. With the documented majority read and write
concerns, a read in that session can wait for the required state instead of
returning a pre-write answer. A timeout remains possible. Do not promise that
these settings prevent another authorized request from changing the ticket.

For an immediate confirmation page, teach the primary route with majority read
and write concerns in the same causal session as a concrete candidate. A
secondary can also participate in causally consistent reads under documented
conditions, but the dependency may require waiting for it to catch up. C's
actual eligibility and client reachability matter; the trace does not promise
that every isolated member will continue serving every type of read.

An acknowledgment timeout means the client lacks the requested confirmation.
It does not prove the insert was rolled back. Connect this to the stable `_id`
from Chapter 12: check whether that request exists and whether its content
matches, rather than submit the same work under a new identifier. A duplicate-key
error alone is not proof of success for the intended operation.

Distinguish the current partition from losing A. While A and B remain connected
and healthy, A need not step down merely because C is absent. If A also becomes
unavailable while B and C cannot communicate, B alone cannot elect a new primary.
Election and driver reconnection are mechanisms with preconditions, not
instantaneous recovery promises. Use CAP to explain this communication conflict,
not as a permanent two-letter label for a product.

### A Worked Recovery Timeline Before the Lab

Use different numbers from the assessed case. A complete artifact represents
16:10. A deletion occurs at 16:22. Detection takes two minutes, retrieving and
authorizing the artifact takes one minute, and restoration plus application
checks take four minutes. Assume there is no later export or replayable log.

The unrecoverable window is `16:22 - 16:10 = 12 minutes`. Against a five-minute
data-loss target, that artifact is too old. The observed recovery duration is
`2 + 1 + 4 = 7 minutes`, so this particular drill fits a ten-minute service target.
This distinguishes **RPO**, the tolerated recovery-point gap, from **RTO**, the
tolerated time to restore the service. Meeting one does not imply meeting the
other. Finishing an export at 16:10 would not by itself prove its data represents
16:10; the case explicitly supplies the represented point in time.

Then students reason through Lab 1's own times in one Brightspace response.
No decision matrix, screenshot, account check, separate project report, or live
partition is required. The project discussion transfers the same reasoning to
one important operation, without duplicating the final-project requirements.

### Day 2 Arc

- Retrieve BSON types and the separate restore target from Week 8's PostgreSQL
  exercise. Read the five-ticket fixture before running the recovery cells.
- Demonstrate the document export and manifest. Show the date marker returned by
  `json.loads`, then the datetime reconstructed by `json_util.loads`. A valid JSON
  parse alone does not reconstruct BSON values.
- Compare the complete restored result with the saved values. Demonstrate the
  supplied wrong-subject case and let students explain why count, identifiers,
  and datetime checks still pass.
- Students choose ticket 1001 or 1004, select its saved document in the provided
  repair cell, and rerun the replacement. The result must match all five original
  documents without creating a sixth ticket.
- Run the separate rule reconstruction and its allowed/rejected tests. End with
  one recovery recommendation inside the same notebook, then cleanup.

### Notebook Walkthrough and Discussion

The default path runs in memory. Atlas is optional and additionally enforces the
server validator. Start with local mode if connection setup would displace the
lesson. For Atlas, students print the runtime's IPv4 address, pause to add only
that temporary `/32` entry, and enter the URI in the hidden prompt. The connection
uses verified TLS, bounded waits, and a cleared URI variable. It does not grant
permissions; the database user must already be able to work in the two scoped
practice databases, including `collMod`.

The source contains IDs 1001-1005. Active requests are exactly 1001, 1002, and
1004. The manifest names the expected collection, count, identifiers, indexes,
and validator. It is separate from the JSON data file. The source fixture remains
unchanged during export, so the notebook does not establish a changing-source or
multi-collection snapshot guarantee.

The file hash identifies the bytes expected by this restore. It is not an
authenticity signature or a completeness test. The restore checks that digest
and parses the content before resetting its disposable target collection. It
does not restore over the source. The Canonical Extended JSON comparison uses
sorted field names to compare stored values and type representations. This
avoids treating an integer and a same-valued double as identical simply because
Python numeric equality permits it.

When the target's subject changes, all three weak checks stay true. The complete
value comparison becomes false. The student repair is one saved-document
selection, not an unrelated Python programming exercise. `replace_one` locates
the existing ticket, uses its saved `_id`, and replaces its document. Running the
repair again is harmless in this unchanged fixture: it matches the same ticket
and does not create another. The source data and export remain unchanged.

The document-only restore starts with the automatic `_id_` index. Recreating
`unique_ticket_id` establishes a separate constraint on the business identifier.
Recreating `status_by_date` restores the two-field index definition, but the lab
does not claim a measured performance gain on five tickets. In Atlas, `collMod`
also installs strict/error schema validation. The test cell accepts a valid
document and rejects a duplicate ticket number. The Atlas path then rejects an
invalid status, a date stored as text, and an absent date. It distinguishes
error 11000 from 121 and propagates unrelated errors instead of calling any
failure a successful test. It removes every temporary test document afterward.

The local path really tests its unique index, but prints a clearly labeled
supplied trace for the unsupported schema checks. Students should say they
interpreted that trace rather than claim MongoDB enforced a rule in their local
runtime. Neither path changes replication settings or tests a primary failover.

For the recommendation, the central issue is whether the colleague has only the
document file or also the rules and deployment information. Students should
connect one result to an omission and to a reopening decision. The Week 8 archive
can include PostgreSQL schema and constraints within its dump scope. This
document-only JSON file omits the collection rules and requires separate
reconstruction. MongoDB Database Tools offer a broader logical archive, but
neither artifact automatically recreates every hosted project setting.

The notebook has one editable repair and one short response. Do not add a
five-check report, another table, exported-file attachment, or final-project
submission. Cleanup removes only the two practice collections and their temporary
file. Other collections remain untouched. Students must separately remove the
temporary Atlas network rule and its printed IP output before submitting.

**Live demonstration:** show why a replicated accidental delete is still a valid
replicated operation and why an independent recovery artifact addresses a
different failure.

**Likely misconceptions:** replicas are backups, majority acknowledgment solves
every loss scenario, free-tier topology permits every failure test, and JSON
automatically preserves every BSON type and collection setting.

**Equivalent path:** Notebook 5 uses `mongomock` for data, repair, and unique-index
practice. The schema trace supports interpretation but does not replace a real
server enforcement test.

**Teaching decision:** if students cannot separate data from metadata, compare the
restored documents with the missing index/validator list before scaling.

## Week 13: Capacity, Sharding, Public Data, and Python Integration

**Student materials:** [Week 13 guide](../weeks/week_13/README.md),
[Chapter 13](../textbook/module_13_scale.md),
[public-data notebook](../notebooks/06_public_data_capacity_integration.ipynb), and
[integration lab](../weeks/week_13/lab_01_public_data_integration.md).

**Prerequisite:** query/index reasoning, MongoDB document operations, and reliable
import evidence.

### Day 1 Arc

- Retrieve tune, scale up, read replica, partition, and shard distinctions.
- Model a sharded cluster with shards, replica sets, config servers, and `mongos`.
- Use the CISA teaching snapshot to measure cardinality, largest-value frequency,
  monotonic input order, and query targeting.
- Run the notebook's deterministic range and hash simulations.
- Students record an individual “do not shard yet” or conditional candidate
  recommendation with evidence.

### Day 2 Arc

- Retrieve source, transformation, stable key, upsert, and verification.
- Model the notebook's simple SQLite path before showing optional Atlas and
  PostgreSQL branches.
- Students choose one target, enter cloud credentials only through `getpass`, load
  idempotently, and verify count, known identifier, and grouped question.
- Students discuss the final-project transfer prompts while working in their
  existing project. No additional written checkpoint is collected.

**Live demonstration:** rerun the same import and show that the stable key
preserves logical count. Compare local SQLite's process boundary with managed
PostgreSQL and Atlas network/authentication boundaries.

**Likely misconceptions:** high cardinality guarantees a good shard key, hashed
distribution makes every query faster, Atlas Free can deploy a sharded cluster,
and insert count proves trustworthy import.

**Equivalent path:** the versioned CISA fixture is embedded in Notebook 6, and
SQLite is built into Python. No live feed or cloud account is required.

**Teaching decision:** if recommendations ignore query targeting, ask students to
route one exact-ID query and one vendor/date question before Week 14.

## Week 14: Polyglot Incident Response and Final Operations Clinic

**Student materials:** [Week 14 guide](../weeks/week_14/README.md),
[Chapter 14](../textbook/module_14_polyglot.md), and
[polyglot incident lab](../weeks/week_14/lab_01_polyglot_incident.md).

**Prerequisite:** relational/document modeling, evidence, recovery, and integration.

### Day 1 Arc

- Retrieve source of truth, idempotency, and synchronization failure.
- Model one ticket stored authoritatively in PostgreSQL with a document-shaped read
  copy in MongoDB. Trace identifier, version/time, and failure points.
- Fade by presenting mismatched values and partial logs without naming the cause.
- Students complete the incident lab individually: impact, boundary evidence,
  diagnosis, and a duplicate/delayed-delivery experiment. The inline Python model
  makes the guarded and unguarded final states visible without cloud setup.

### Day 2 Arc

- Retrieve one operational evidence pattern from each final-project category.
- Students work individually on their final using the canonical requirements.
- Hold short public demonstrations of model, query, access/performance, and
  recovery evidence; students apply the same checklist to their own work.
- Exit with one verified claim, one unresolved risk, and one next action.

**Live demonstration:** compare a failed dual write with an outbox/idempotent
consumer concept at a beginner level. Emphasize ownership and evidence rather than
adding a framework.

**Likely misconceptions:** two stores are automatically more scalable, both copies
can be authoritative, timestamp comparison alone proves correctness, and retrying
without an idempotent key is safe.

**Equivalent path:** the incident has supplied logs and a plain-Python model. Final
work can use the open local path when a cloud service is unavailable.

**Teaching decision:** if students repair values without naming ownership and
verification, require those two statements before final presentations.

## Week 15: Integrated Review, Public Artifact, and Career Translation

**Student materials:** [Week 15 guide](../weeks/week_15/README.md),
[Chapter 15](../textbook/module_15_careers.md),
[GitHub concept-artifact lab](../weeks/week_15/lab_01_github_concept_artifact.md), and the
canonical [final project](../assignments/final_project.md).

**Prerequisite:** one completed or nearly completed final project and safe public-
artifact practices.

### Day 1 Arc

- Retrieve the course verbs: model, query, restrict, diagnose, measure, recover,
  integrate, and explain.
- Model a short public README that teaches one concept with original explanation,
  safe code or a Markdown guide, expected evidence, and limitations.
- Students create the GitHub concept artifact individually and verify that no
  credential, private account detail, or private dataset appears.
- Translate one artifact into a Situation-Task-Action-Result-Reflection outline.

### Day 2 Arc

- Use the post-course inventory for reflection and course improvement, not a
  final-exam grade.
- Students give short individual final demonstrations centered on one operating
  claim and its evidence.
- Ask follow-up questions about tradeoffs, limitations, and the next production
  check rather than obscure trivia.
- Students complete the interview response and name one next skill/artifact.

**Live demonstration:** turn a weak claim such as “I know MongoDB” into a supported
claim naming the workload, action, observed evidence, tradeoff, and limitation.

**Likely misconceptions:** a tool list is a portfolio, classroom scale invalidates
all skill evidence, confidence requires hiding limitations, and public work should
include real credentials or account screenshots.

**Equivalent path:** a local Markdown/code artifact may be submitted privately if
public GitHub creates a barrier. The interview explanation remains the same.

**Teaching decision:** report aggregate changes in concept categories and material
access. Do not publish named student results or claim causal impact beyond the
available design.

## After the Course

1. Run the technical, link, accessibility, notebook, and slide validation suite.
2. Review aggregate diagnostic/post categories, lab revision patterns, rubric
   dimensions, and access feedback.
3. Separate platform failures from conceptual errors.
4. Record one observed pattern, one cautious interpretation, and one OER change.
5. Update the [created OER catalog](../OER_CATALOG.md), attribution record, and
   release status.
6. Preserve the boundary among public OER, free external resources, and private
   student/grading records.
