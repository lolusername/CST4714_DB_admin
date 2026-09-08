# Week 4: Views, Identity, and Safe Change - Spoken Transcript

## Slide 1

Last week we inspected the structure of our support database and added rules that reject invalid values. We saw that a table can contain valid text without containing the particular vocabulary that the application expects. This week we will keep working with that same distinction between a command succeeding and the application receiving the right result.

Our first task is to give a useful query a stable name. The support staff need a list of active tickets, and different screens should not have to reinvent the definition of active. We will create an ordinary view, read its results, and change its interface deliberately. We will also create a small table whose identifiers come from a sequence. A cancelled insertion will help us see why an identifier and a row count mean different things.

On the second day, the organization wants to record whether a request came from the web, a phone call, or a mobile application. That sounds like one new column. But old records do not contain that information, and old application code does not yet send it. We will work through the transition rather than assume those problems disappear after ALTER TABLE succeeds.

You will work individually in your course database. Each day's submission is one SQL file with the relevant queries and short explanatory comments. The purpose of those comments is to state what your change means, including what the data cannot tell us.

## Slide 2

The first row of this comparison is the base table. Our tickets table contains stored ticket records. A SELECT asks PostgreSQL to produce some result from those records. The selected columns and the filter determine what we receive.

An ordinary view retains a SELECT definition under a name. When a later query refers to that view, PostgreSQL uses the definition as part of producing the requested result. It does not require us to maintain a second independent queue table every time a ticket changes. That is useful here because the definition of active belongs in one place rather than being copied inconsistently into multiple reports.

Suppose ticket 1001 changes from open to resolved in a committed change visible to our next query. A view that selects only new, open, and in-progress tickets will stop returning 1001. We do not separately delete it from the view. The filter now evaluates differently against the visible ticket data.

A materialized view has a different purpose. It retains previously computed result rows, which can be useful when a calculation is expensive. Those rows need a refresh strategy. A result can be fast to read and still be too old for its intended use.

Today we use ordinary views. Creating one does not automatically make its query faster, nor does its name establish a security policy. We will keep those questions separate from the immediate task of defining the right result.

## Slide 3

Here is a complete view definition. The words CREATE OR REPLACE VIEW introduce the object name, metro_support.active_ticket_summary. Everything after AS is the SELECT that defines its result. If the view does not exist, PostgreSQL creates it. Replacement has compatibility rules that we will examine shortly.

Read the SELECT list before the join. We want the ticket identifier, subject, priority, and the requester's display name. The short names t and u are aliases for the tickets and users tables. They help us state where each column comes from. AS requester_name gives the output column a name that explains the person's relationship to this ticket.

The join uses requester_id. Each ticket requires an existing requester in our baseline, so this relationship should find one user. The foreign key establishes existence, and the user's primary key prevents multiple users with the same identifier from multiplying the ticket row. The WHERE clause keeps the three statuses we call active.

Running this command saves a definition. It does not itself print the seven ticket records for us. We will issue a SELECT against the view next.

Your lab uses a different relationship: the assigned agent. Some tickets have no assigned agent yet. An inner join through assignee_id would remove those tickets. That is why the lab needs a LEFT JOIN even though this requester demonstration uses an ordinary inner join. The join choice follows the meaning of the relationship.

## Slide 4

Now we read through the name we just created. FROM refers to active_ticket_summary rather than repeating the underlying tickets-to-users join. We select only two of the four columns the view makes available. A view defines an interface, and a caller can still choose a narrower result from that interface.

The result contains seven ticket identifiers on the complete baseline. Notice that Maya Chen appears for tickets 1001 and 1009, and Luis Rivera appears for 1002 and 1006. Repeated names are not automatically duplicate records. Each result row represents a ticket, and the same person can open more than one ticket. The identifier is important for distinguishing those requests.

We put ORDER BY ticket_id in this reading query because we want a predictable display order. The fact that a previous execution happened to return rows in some order is not a promise about the next execution. A caller that needs an ordering should request it explicitly.

Our definition did not copy user names into tickets. It retrieves the current display name through the relationship. If the requirement were to retain the exact name supplied at the moment of submission, that would be a different historical fact and a different modeling decision.

When you verify your own view, inspect identifiers as well as a total count. A count of seven alone cannot show that the seven intended tickets survived a join. In the lab, the two unassigned identifiers are especially useful checks.

## Slide 5

The lab begins with five named columns in this order: ticket identifier, subject, status, priority, and opening time. We can think of this as an interface that another query already uses. Changing it requires more care than writing a new SELECT that happens to return useful information.

PostgreSQL's CREATE OR REPLACE VIEW keeps the existing output column names, order, and data types. It permits additional columns at the end. Therefore, when you add assignee_name in the lab, append it after opened_at. Do not insert it between two existing columns or silently rename an old column. A genuinely incompatible interface may need a separately named version while callers adapt.

There is a subtle point about SELECT star. PostgreSQL expands the star when it defines a view. If we later add a column to the base table, that existing view does not automatically acquire the column. However, a later recreation or replacement from a star-based definition can produce a different interface. Explicit columns make the intended exposure easier to review.

This matters for ordinary compatibility and for sensitive information. We should not accidentally widen a report because a new base-table column happened to exist when a deployment script ran.

For this lab, preserve the original five outputs, append the assignee name, and verify the result. The textbook uses the separate name chapter4_active_queue so reading examples cannot overwrite your classroom interface with a different layout.

[Sources]
- PostgreSQL 15, CREATE VIEW: https://www.postgresql.org/docs/15/sql-createview.html

## Slide 6

Before we change objects, this small query helps establish where the command will run. current_database reports the selected PostgreSQL database. current_user reports the effective database role. current_schema reports the current schema selected from the search path. SHOW search_path displays the configured path used to resolve unqualified object names.

These values describe the connection context. They do not count application users, and they do not refer to the identity column that we will create next. In database discussions, the same everyday word can describe different mechanisms. A database role identifies an actor for privileges. A generated row identifier distinguishes one stored record from another.

Your results may differ from mine because your local server or hosted project has different names and roles. That difference is not automatically an error. The useful question is whether the connection points to the practice environment where you intended to work.

We write metro_support.tickets in our examples. The part before the dot is the schema name; the part after it is the table name. This avoids relying on an editor tab's search path to find the intended table. We used the design meaning of schema last week, and here we are using PostgreSQL's namespace meaning.

A successful query in an administrative SQL editor does not prove that an application role has the same access. We will test permissions as particular roles in Week 6. For today, record the context when diagnosing an unexpected result instead of assuming every open connection is interchangeable.

## Slide 7

This demonstration table stores notes about database changes. It is intentionally separate from tickets, so we can study identifier allocation without altering the ticket keys. It is also separate from your lab's change_notes table, which lets the demonstration and your own experiment coexist.

The first column is note_id. bigint stores a whole-number value with a large range. GENERATED BY DEFAULT AS IDENTITY asks PostgreSQL to provide a value from an associated sequence when the insert omits this column. BY DEFAULT also permits a caller to supply an explicit value, which can be useful for imports but needs care.

PRIMARY KEY is a separate part of this definition. It requires the identifier to be unique and non-null. Generated allocation and uniqueness enforcement are related in this design, but we should be able to explain which clause provides which behavior.

The change_name is required text. The created_at column records a timestamp with time zone, and its default supplies now when the insertion omits that field. Our insertion can therefore name only change_name and let the database fill the other values.

Create this demonstration table once. If it already exists from an earlier run, inspect it before expecting identifiers to restart at one. Repeated execution against an existing table and a fresh experiment are different starting states. In your personal lab, the instructions explicitly identify a disposable table that can be recreated for the experiment. That permission does not extend to arbitrary tables in a real database.

## Slide 8

This complete batch contains three transactions. Each begins with BEGIN and ends with a deliberate choice. The first inserts Initial view and commits it. RETURNING asks PostgreSQL to display the identifier produced by that insert, so we can observe allocation without guessing what happened.

The second transaction inserts Cancelled change. It also receives an identifier, but then ROLLBACK removes the row change from the transaction. The third inserts Approved revision and commits that row.

On our freshly created table, those three RETURNING results are one, two, and three. Some SQL editors display only the last result by default, so a hidden earlier result tab does not mean the earlier statement failed. The next slide uses a SELECT to inspect the rows that actually remain.

The explicit commit after the first insert is important. We should not assume that an editor's batch behavior automatically establishes the transaction boundaries we intended. By including BEGIN and COMMIT, we state that the first row must survive independently of the second transaction's cancellation. We also finish the third transaction explicitly.

Run the complete batch rather than leaving it paused inside a transaction while you work elsewhere. An open transaction can retain resources and locks. If an expected failure leaves a transaction aborted, ROLLBACK ends that failed transaction before a new attempt. Here there is no expected SQL error; the cancellation is a deliberate rollback of an otherwise valid insertion.

## Slide 9

The table separates allocation from retention. All three inserts received a number. Only the first and third transactions retained a row. A SELECT from demo_change_notes therefore returns identifiers one and three, with their two change descriptions.

The missing two does not indicate that PostgreSQL lost a committed record. In this experiment we know exactly why it is absent: the associated row insertion was rolled back. The sequence allocation itself was not rolled back. Real systems can also have gaps for other reasons, so seeing a gap alone is not enough to reconstruct its history.

This is why the largest identifier is not a row count. The largest identifier here is three, while count star would report two rows. Deletions can make the difference even larger. Use aggregate counts to answer counting questions and use keys to identify records.

A sequence provides allocation without promising an uninterrupted series of committed business events. If an organization has a special legal or operational requirement for consecutive invoice numbers, that needs a separately designed process rather than an assumption about an identity column.

For the lab, explain the difference between the values returned by the inserts and the rows found by the final SELECT. You do not need a separate essay. A few precise SQL comments are enough to show that you understand why the final state is correct. If you rerun without resetting your disposable table, the exact values may differ, but this distinction still applies.

[Sources]
- PostgreSQL 15, sequence manipulation functions: https://www.postgresql.org/docs/15/functions-sequence.html

## Slide 10

You now have the two worked examples needed for the first lab. The assignment is individual, and all of the work belongs in your own course database. Start with the complete Metro Support baseline rather than one of the smaller examples from the early SQL review.

The lab supplies a five-column active queue. Your change is to add the assigned agent's display name as the final column. Use the requester demonstration to understand the join syntax, but adapt the relationship correctly. A ticket can exist before anyone is assigned to it. Keep those records with a LEFT JOIN and verify that tickets 1004 and 1009 remain in the result. Their missing assignee names are meaningful, not a reason to discard the tickets.

The second part creates the disposable change_notes table and supplies an explicit sequence of committed and rolled-back insertions. Run it, inspect the final rows, and explain why the identifiers have a gap. The metadata queries show how PostgreSQL describes the view and identity column you created.

Submit week_04_views_identity.sql in Brightspace. Include the working SQL and short comments explaining your join and the identifier result. There is no separate screenshot collection or change report. Keep this database state for Day 2, because the next lab changes the tickets table underneath the view you create today. If something fails, inspect the current definition before rerunning commands that create an object a second time.

## Slide 11

We will now change the underlying table while preserving the interface we just built. The new requirement is a source channel for each request. The allowed values will be web, phone, mobile, and unknown.

The word unknown has an important role. Old tickets were created before we had this structured field. We may find occasional clues in event notes, but those clues do not justify assigning one channel to every historical request. A database can enforce that every row contains a permitted word without proving that the word accurately describes the world. We must make that distinction ourselves when designing the migration.

There is also an application compatibility issue. An older writer may still provide an explicit list of the original ticket columns. If our new required field has no default, that otherwise valid insertion may fail. We will use a default to preserve this particular old-writer behavior while newer software begins sending the actual channel.

Our classroom sequence is to inspect, rehearse, verify, roll back, and only then apply the small change. The transaction makes the rehearsal reversible in this database. It does not make every migration free of locking or deployment risks. We will keep the classroom example small enough to understand and describe the limits honestly.

Continue in the same personal database from Day 1. The view is part of the state we are deliberately preserving, so do not reset it between the two labs.

## Slide 12

This comparison gives the change three audiences. First, the historical rows. Before the migration they have no source_channel column. Afterward, the structured value is unknown unless we have a trustworthy record-specific basis for something more precise. Setting every old value to web would make later reporting look complete while adding a claim we cannot support.

Second, the new writers. Updated application code can send the actual channel. The allowed-value rule rejects a spelling that we have not agreed to use. That makes the structured field more consistent, though it still cannot prove that the application reported the real event truthfully.

Third, the older writers. Here we mean clients that insert an explicit list of the old columns and omit the new one. DEFAULT unknown supports that omission. It does not magically make every old program compatible with every schema change. Programs that depend on column positions, changed types, or a different result shape require their own checks.

Our baseline contains twelve tickets. That small size lets us follow the entire backfill and verify it directly. A production table with millions of rows and continuous traffic raises additional questions about lock duration, batches, validation, and deployment order. The textbook explains a broader expand-and-migrate pattern for that setting.

The immediate goal is to preserve the meaning of old data while introducing a better field for future data. The migration should improve what we can record without pretending that we already knew it.

## Slide 13

The precheck is a set of ordinary queries about the starting state. The first query reads information_schema.columns, which describes the columns PostgreSQL currently exposes to this role. We restrict it to the tickets table in the metro_support schema and to the specific column name source_channel.

Before this migration, that query returns zero rows. That means no matching column description appears in this context. It is different from a query returning one row whose value is zero. The next two queries are aggregates and do return a row containing a count: twelve stored tickets and seven rows in the active queue.

Those values are expectations for the complete, unchanged classroom baseline plus your Day 1 view. They are not universal truths about every support database. If the column already exists, do not blindly add it again. Inspect your earlier attempt and determine whether you previously committed the migration. If the queue count differs, investigate the definition and data before proceeding.

The precheck does not prove every possible property of the database. It establishes the particular conditions this small change relies on. The lab also depends on the view keeping the unassigned tickets, which we checked yesterday and will check again after the change.

Keep these queries in your SQL file. They make the intended starting point understandable to another person and help you diagnose a repeat run. We are using executable inspection rather than asking for a separate administrative form.

## Slide 14

This is the complete rehearsal. BEGIN establishes the transaction. The first ALTER TABLE adds a text column that is initially allowed to be missing. The UPDATE fills missing historical values with unknown. Its WHERE clause states which rows need the backfill rather than overwriting every value unconditionally.

The next ALTER TABLE creates a named CHECK constraint. It permits web, phone, mobile, or unknown. This is the same allowed-vocabulary technique we practiced with priority and status last week. Naming the rule helps us interpret the later error when we deliberately try fax.

We then require a value with NOT NULL and define unknown as the default for an omitted value. These are distinct rules. The CHECK limits permitted non-null text. NOT NULL rejects an explicitly missing value. The default supplies a value when a writer leaves the column out.

The grouped SELECT runs before the transaction ends, so it can inspect our uncommitted changes within this session. It should show unknown with a count of twelve. ROLLBACK then removes the added column and associated rules, as well as the backfill. We will query the catalog again to verify that outcome.

Run this whole batch together in the practice database. If any statement fails and the session remains in an aborted transaction, run ROLLBACK before retrying. The textbook includes optional timeout guardrails and explains what they limit. Our small classroom batch makes the transaction boundaries visible without assuming that every production migration can use exactly this approach.

## Slide 15

A successful ALTER TABLE message is useful, but it answers only part of our question. This table organizes the specific outcomes we need to check. During the rehearsal, the new column exists with its intended rules. The historical rows contain unknown, and the existing queue still returns seven tickets.

After rollback, the added column should no longer exist. The original tickets and the old view should still be usable. The catalog query at the bottom repeats the column lookup from the precheck. Zero result rows after rollback are the expected outcome for that lookup.

Notice that structure and meaning are separate. We could create a perfectly valid NOT NULL text column and fill it with an invented channel. The schema would satisfy a structural check while the historical interpretation would be wrong. Conversely, a reasonable backfill could coexist with an incorrectly replaced view that drops unassigned work. We need checks that correspond to both risks.

You can run the metadata and queue queries before and after the batch. If your editor only displays one result set at a time, inspect the relevant result tab or run the read-only verification query on its own after the transaction ends.

This rehearsal demonstrates that this particular PostgreSQL change is transactional. It does not demonstrate that holding a lock is harmless or that reversing any future data transformation will recover lost detail. Those are additional operating questions. In your SQL file, keep the checks close to the change so another reader can connect the expected result to its purpose.

## Slide 16

This is a saved screenshot of the Supabase SQL editor from August 25, 2026. Supabase gives us a browser interface to PostgreSQL, so the transaction language is still SQL. The screenshot shows a small temporary-table rollback check, not the full tickets migration from the preceding slides.

In that demonstration, an explicit transaction created a disposable temporary table named oer_validation and then rolled back. The visible SELECT asks whether PostgreSQL can still resolve that temporary table. to_regclass returns a relation identifier when it can find the named object and null when it cannot. Comparing the result with IS NULL produces the true value shown as rollback_verified.

The full small demonstration is BEGIN, CREATE TEMP TABLE oer_validation with one integer column, ROLLBACK, and then the visible catalog check. Because creation occurred inside the rolled-back transaction, the object is absent afterward. A temporary table created and committed before the transaction would be a different starting state and would not support that same interpretation.

For our lab, checking whether this temporary table disappeared would not verify the ticket change. We instead check source_channel, the rules attached to it, the twelve historical rows, and the seven-row queue. A verification query has to describe the object and behavior that matter for the actual change.

The interface may look different in your current project. The SQL transaction boundaries and the meaning of the result matter more than reproducing the precise appearance of this saved editor screen.

[Sources]
- Course screenshot: textbook/figures/cloud_interfaces/supabase_sql_rollback.png, captured August 25, 2026.

## Slide 17

Once the rehearsal succeeds and rollback restores the expected starting state, repeat the same migration with COMMIT in place of ROLLBACK. That deliberate change retains the new column and its data. Do not run the ADD COLUMN block again after it has already committed; begin with inspection if you are unsure of the current state.

The existing view does not automatically gain source_channel. We now replace its definition with an explicit seven-column interface. Compare the first five expressions with the original lab view. They retain ticket_id, subject, status, priority, and opened_at in the same order. The sixth is the assignee name added in Day 1. The seventh, and only new output here, is source_channel.

The LEFT JOIN remains because assignment is still optional. Adding a channel did not change that business fact. Tickets 1004 and 1009 must remain in the queue even though they have no assigned user. A new requirement should not silently undo a correct decision from the previous lesson.

After this definition runs, read the queue and inspect the new output. You should still find seven active identifiers, and their channel values should initially be unknown on the unmodified classroom baseline.

This is a small example of evolving an interface while preserving existing callers. A caller that selects the original named columns can continue to do so. A caller that needs the new field can request it explicitly. We still need to test real application assumptions rather than infer compatibility from the view name alone.

## Slide 18

We will test both sides of the allowed-value rule. The first batch starts a transaction, updates ticket 1004 to mobile, and returns the changed identifier and channel. Because mobile belongs to the allowed list and is not null, the statement succeeds. The returned row shows what the update would retain if we committed it.

We then roll back, because this is a test against a historical ticket whose channel is not established by our data. We should not leave behind a made-up mobile value merely because it was useful for demonstrating a valid update. A later SELECT should show unknown again.

The second UPDATE uses fax. Run it separately from the successful batch. We expect PostgreSQL to reject it with SQLSTATE 23514 and the constraint name tickets_source_channel_allowed. The constraint name identifies the particular protection we installed. The original value should remain unchanged after the rejected statement.

If the editor reports that the current transaction is aborted, finish it with ROLLBACK before continuing. Do not mistake a later aborted-transaction message for the original reason the fax value was rejected.

Keep the invalid statement commented in the submitted SQL file and record the expected error in a comment. That lets a reader intentionally run the negative test without having a routine execution stop unexpectedly. A useful test suite needs examples that should succeed and examples that should fail. We will carry that habit into later permissions, recovery, and data-loading work.

## Slide 19

Before commit, our rehearsal has a clear boundary. ROLLBACK removes the transaction's changes and returns us to the earlier committed state. That is the mechanism we just observed with the column, rules, and backfill.

After the migration commits and new requests arrive, the situation changes. Suppose a new mobile request correctly records its channel. Dropping the entire column would discard a real fact that the old database never held. Writing an opposite-looking command is therefore not necessarily an adequate recovery plan. We may need a forward repair that fixes a view definition or writer behavior while preserving the newly collected data.

The default also deserves a precise explanation. An older writer that omits the field receives unknown. A writer that explicitly sends NULL receives a NOT NULL error. Missing a column from an INSERT list and supplying a missing value for that column are different operations. A newer writer should provide the actual channel when it knows it, rather than treating the default as a substitute for collecting the information.

Finally, a transaction can retain locks while it remains open. Transactional does not mean that other users cannot wait. Keep the classroom batch together and end it deliberately. Production planning needs to account for table size, traffic, lock behavior, and deployment order.

Your explanation should identify which state can be recovered and which facts must survive. That is more informative than promising that every change can always be undone immediately.

## Slide 20

The second lab uses the same database and queue from Day 1. Work individually and begin with the supplied precheck. If you have not completed the queue portion of the first lab, finish that before adding the field. The identity experiment is useful background but is not a prerequisite for changing the tickets table.

The starter gives you the transaction boundary, column addition, historical backfill, and grouped result query. Complete the three rules using the worked slide and the textbook: the named allowed-value CHECK, NOT NULL, and the default for omitted values. The exercise is to connect each rule to its purpose and verify its behavior, not to recall every keyword without a reference.

Run the rehearsal and confirm that rollback removes the column. Then apply the verified version with COMMIT, and append source_channel to the existing view while preserving its earlier columns and LEFT JOIN. Test mobile inside a transaction that rolls back, and test the invalid fax value separately.

Submit one file, week_04_safe_migration.sql, in Brightspace. Include the precheck, completed migration, view update, and verification queries. In short comments, explain why historical rows use unknown, how the default supports an older writer, and why dropping the column later could erase real data. There is no additional change-plan document.

If your result differs from the expected state, investigate the definition and affected identifiers. A thoughtful diagnosis of the actual state is more useful than rerunning the entire dataset reset and losing the change you were trying to understand.

## Slide 21

We began with a reusable query and ended with a change to the data it reads. The connecting idea is that an interface has meaning for the people and software using it. A queue can look plausible while losing unassigned requests, so we verified particular identifiers rather than relying only on a count.

The identity experiment gave us another distinction between appearance and meaning. An identifier gap can be a normal consequence of a rolled-back insertion. The key distinguishes a record; it does not summarize how many records have committed. We can explain the actual result because we followed the transaction boundaries.

The channel migration extended that reasoning to historical data and application compatibility. We added a useful field without manufacturing old facts. We supported the specific older-client behavior of omitting the field, and we kept the view's existing columns while appending the new one. Valid and invalid updates showed what the rules actually accept.

These are skills you can describe concretely in a technical interview. You could explain that you changed a PostgreSQL interface, rehearsed the migration in a transaction, checked old and new behavior, and identified the point at which a later repair must preserve newly collected data. You should also state that this was a controlled classroom database rather than claim that you operated a production service.

Next week we will look more closely at transactions that overlap. The same BEGIN, COMMIT, and ROLLBACK statements will help us explain what another session can see and why one operation sometimes waits for another.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
