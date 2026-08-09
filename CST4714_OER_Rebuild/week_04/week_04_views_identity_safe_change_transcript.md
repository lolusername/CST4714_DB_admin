# Week 4: Views, Identity, and Safe Change - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Views, Identity, and Safe Change

This week asks how a database can change without surprising every client at once. We begin with views and execution identity, then move into a beginner-safe migration pattern. The technical commands are only one part of the work. A change also has a starting-state check, dependency boundary, verification query, rollback or forward-repair plan, and remaining risk.

The same evidence habits from constraints apply here. We will not assume that a successful `ALTER TABLE` means applications still work. We will inspect the current context, expose a stable interface where useful, make one controlled change, and verify behavior through the interface a client actually uses.

## Slide 2: A view can separate a stable interface from changing storage

A standard PostgreSQL view is a named query. It normally stores the definition rather than an independent copy of every result row. When a client selects from the view, PostgreSQL evaluates the view within the database's rules and current data.

Views can create a stable column shape, hide implementation detail, centralize a repeated relational expression, and provide a narrower permission boundary. They are not automatic security barriers or performance caches. The view owner, caller identity, security options, underlying permissions, and query plan all matter. Use a view when the database interface is a deliberate contract, not simply to avoid writing a join twice.

## Slide 3: Identity changes what the same SQL is allowed to do

SQL does not execute without an identity. The current user, active role, database, schema search path, and provider context influence object resolution and authorization. An administrator can often query a table that an application role cannot see. That success is not evidence that the application works.

When investigating access or a view, record the identity under which the query ran. In Supabase, the SQL editor may use a privileged database role, while browser requests use roles and claims derived from an authenticated request. Those layers will receive fuller treatment in Week 6. For now, the durable rule is simple: test behavior under the identity whose promise you are making.

## Slide 4: Interrogate the execution context before blaming the query

The first query records four context facts. `current_database()` identifies the database named by the connection. `current_user` identifies the role used for permission checks. `current_schema()` reports the first valid schema in the effective search path. The setting itself shows the schema-resolution order.

These facts can explain why identical unqualified SQL resolves to different objects or receives different permissions. The second query lists views in the Metro Support schema. If a client reports that a view is missing, verify database, schema, search path, object spelling, and privilege before recreating anything. Context evidence prevents a common troubleshooting mistake: changing the schema when the connection or identity is the actual difference.

## Slide 5: A view states its result grain and column contract

This view defines one row per active ticket. The join attaches the matching requester's display name, and the alias `requester_name` becomes part of the visible column contract. The status list defines active for this interface.

After creation, query the view using the intended role and verify stable ticket identifiers, column names, and row count. Inspect the view definition in metadata so a later change does not rely on memory. A view can reduce direct base-table exposure, but it does not automatically prevent every inference or update. Permissions, row-level policies, and security behavior must be tested separately.

## Slide 6: Lab 1: Create and verify one stable view

This individual lab begins by recording the execution context. Then create the assigned view in the disposable Metro Support schema. State the view's result grain and choose client-facing column names deliberately.

Query the view and verify its shape with identifiers and a count. If the environment permits role testing, use the intended limited role; otherwise state the context limitation explicitly. Include copied SQL and relevant text output, not a private project screenshot. Submit one record containing context, view definition, verification, and one limitation.

## Slide 7: Change compatibility before removing the old path

On the second day, we treat a migration as a sequence. The goal is to preserve service while storage or interfaces evolve. The beginner-safe pattern is expand, migrate, verify, and contract.

Expansion adds a compatible new path without removing the old one. Migration copies or transforms existing data and moves writers or readers. Verification checks data, dependencies, and client behavior. Contraction removes the old path only after evidence shows it is no longer needed. Not every classroom change needs a long deployment, but reasoning in stages exposes assumptions that a one-command migration hides.

## Slide 8: Expand, migrate, verify, then contract

The sequence starts with a precondition because a migration written for one schema can damage another. Confirm columns, types, constraints, row counts, and dependencies. Expansion then adds the new structure while preserving the old path. A nullable column, compatibility view, or additional write path may support that transition.

Migration backfills data or moves clients in a controlled scope. Verification compares old and new representations, checks nulls and counts, and exercises dependent queries. Contraction is last. Removing the old path too early turns a reversible transition into an outage. In a simple classroom database, the stages may occur in one session; the reasoning still matters.

## Slide 9: A safe change record makes the transition reviewable

This simplified sequence first checks a data precondition. It then adds a compatible column, backfills a derived label, and verifies that no current ticket remains without the new value. Those steps do not yet establish a production-ready migration.

We still need to inspect dependencies, concurrent writes, repeated execution, transaction boundaries, and which representation is authoritative. A rollback might remove the new column if no client depends on it, while a forward repair may be safer after clients begin using it. The example is useful because it exposes the questions. A migration record should never imply that one successful backfill proves every reader, writer, permission, index, and recovery path remains correct.

## Slide 10: Rollback and forward repair solve different situations

Rollback is not always the opposite DDL command. Dropping a new column can destroy data written after the migration began. Reversing a type conversion may be lossy. Once clients depend on a new interface, rollback can create another outage.

A forward repair keeps the current direction and corrects the defect, such as backfilling missed rows, repairing a view, or adding a compatibility alias. The right response depends on the observed state, data written since the change, client adoption, and recovery options. Record the decision point before executing either path. Every rollback or forward repair needs its own verification; its label does not guarantee safety.

## Slide 11: A five-part change record keeps the claim bounded

The five-part record begins with a precondition. The change section states exactly what was executed and under which identity. Verification covers more than the table definition: inspect transformed data and a representative client-facing query or view.

Recovery names either rollback or forward repair and the state in which it remains safe. The fifth part is the remaining risk. Examples include concurrent writes not tested, a client outside the repository, a large-table lock, or a provider feature not available on the free tier. This record is compact enough for classroom use but follows the same reasoning expected in a professional change request.

## Slide 12: Lab 2: Perform one reversible migration

Complete the migration individually in the disposable course schema. Do not begin with `ALTER TABLE`. First query the expected columns, data condition, and any view named in the lab. If the precondition fails, stop and diagnose rather than forcing the script.

Apply the compatible change and migration step. Verify both metadata and data, then run the representative client query. Record whether rollback or forward repair is safer at that point and why. Submit one five-part record. If live PostgreSQL is unavailable, use the supplied before-and-after transcript and write the same evidence-based decision.

## Slide 13: Safe change preserves a contract while the implementation moves

This week treated views, identity, and migrations as one topic: preserving understandable interfaces while the database evolves. A view can provide a stable shape, but its permissions and behavior must be tested under the intended identity. Context queries reveal which database, user, schema, and search path actually execute the SQL.

A safe migration begins with a precondition and expands compatibility before removing the old path. Data and client behavior are verified before contraction. Rollback and forward repair are choices based on state, not magic words. Next week, independent sessions will make state more complicated. Transactions, MVCC, and locks will show why concurrent operators need the same disciplined evidence.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
