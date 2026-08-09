# Week 3: Schemas, Constraints, and Evidence - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Schemas, Constraints, and Evidence

This week moves from querying existing relations to operating the structure that protects them. A schema is not only a list of columns. It is a collection of identities, domains, relationships, rules, and access paths that define which states the database can represent.

We will begin with a cumulative SQL clinic because administration cannot be separated from query fluency. Then we will perform a schema x-ray before changing anything. On the second day, we will create constraints and test them with expected failures. The evidence standard is two-sided: a valid state should succeed, and an invalid state should be rejected for the intended reason.

## Slide 2: Schemas protect meaning at the storage boundary

Application forms can help users enter good data, but the database is the shared storage boundary used by many clients, scripts, imports, and future applications. A rule that matters to every writer often belongs in the database as well as in the user interface.

A primary key prevents duplicate or missing identity. Types and `NOT NULL` define basic domains. `CHECK` constraints express row-level conditions such as an allowed status. `UNIQUE` protects alternate identities. A foreign key prevents a reference to a parent identity that does not exist. These mechanisms do not encode every business rule, but they make important invalid states impossible or visible at the boundary where data is committed.

## Slide 3: Perform a schema x-ray before proposing treatment

A schema x-ray is a structured inspection of the current database. Begin by listing schemas, tables, and views and stating the grain of important relations. Then inspect columns, types, defaults, and nullability. Identify primary and unique keys, followed by foreign-key relationships and their update or delete actions.

Next inspect check constraints and dependent views or functions. Finally, list indexes and connect each one to a query shape rather than assuming its name proves usefulness. This inventory becomes the migration precondition. It also prevents duplicate indexes, conflicting constraint names, and changes based on an outdated diagram. Database metadata is evidence produced by the system itself, but it still needs interpretation and a recorded environment.

## Slide 4: PostgreSQL catalogs reveal the structure the server enforces

The information schema provides portable views of many database objects. The first query lists base tables in the Metro Support schema. The second lists ticket columns in their defined order, together with PostgreSQL's reported data type and nullability.

Before accepting the output, record the current database and user so another person knows which environment was inspected. Metadata can differ between a local fixture and a cloud project. Also remember that the information schema is not the only PostgreSQL metadata surface. PostgreSQL catalogs and `psql` commands expose additional details such as index definitions, constraint expressions, ownership, and dependencies. Select the smallest query that answers the inspection question, then preserve the relevant text output.

## Slide 5: Different constraints reject different bad states

Constraint names are easier to remember when each is attached to a bad state. A primary key protects the official row identity from duplication and absence. A unique constraint protects another candidate identity, but its handling of `NULL` depends on the database and definition, so verify the exact semantics you need.

`NOT NULL` rejects missing values. A check constraint evaluates a predicate over a row, such as an allowed status or a rule that a resolution time cannot precede opening time. A foreign key protects referential existence. It does not prove that the referenced user is the correct requester or that the application is authorized to choose that user. Constraints provide specific guarantees, not general truth.

## Slide 6: Lab 1: SQL clinic and schema x-ray

This individual lab begins with a short cumulative SQL checkpoint so that forgotten joins or grouping are visible before schema work depends on them. Record the result grain and one verification check.

Then inspect the Metro Support schema using metadata queries. Include tables, ticket columns, primary and foreign keys, checks, and indexes. Connect each observed rule to a specific bad state. Finish by naming either one integrity risk the current schema permits or one rule it already protects, supported by metadata. Submit one compact x-ray rather than separate screenshots. If Supabase is unavailable, the same setup and catalog queries can run in local PostgreSQL.

## Slide 7: Make the rule observable through success and failure

On the second day, we move from inspecting rules to testing them. A DDL command that reports success proves that PostgreSQL accepted the definition in that environment. It does not yet prove that the definition rejects the intended bad state or allows the intended valid state.

We will use a transaction to keep tests controlled. Insert a valid boundary case and observe success. Then attempt one deliberately invalid row and capture the expected constraint error. Roll back so the fixture remains reusable. The purpose is not to generate errors for their own sake. The expected failure identifies which rule the database actually enforced and reveals whether the error would be understandable to an application or operator.

## Slide 8: Translate business rules into testable database behavior

The table separates a human rule from its mechanism and tests. ‘Every ticket has a stable identity’ can be implemented with a primary key, tested by inserting a new unique identifier, and challenged with a duplicate or missing identifier. The status vocabulary can be enforced with a check and challenged with a value outside the allowed set.

A foreign key can require the requester identity to exist. A unique constraint can protect an external reference from reuse. Test both expected success and expected failure because an over-restrictive constraint is also a defect. Use synthetic values in a disposable transaction. The exact error should name the violated constraint or rule, making the evidence interpretable.

## Slide 9: Create the rule, then challenge it inside a transaction

The constraint name `tickets_status_check` describes both the relation and the protected concept. A clear name improves migration review and error diagnosis. The predicate lists the supported status vocabulary. In a larger system, the choice between a check, lookup relation, domain, or application-managed workflow depends on change frequency and ownership, but the rule must still be explicit.

The test transaction attempts a synthetic row with `almost_done`. The expected result is a check-constraint violation naming the constraint. If the insert succeeds, either the constraint is missing, the wrong table is targeted, or the predicate does not express the intended rule. Roll back after the test so no invalid or temporary data remains.

## Slide 10: An index is an access path, not another integrity rule

Constraints and indexes are related but should not be confused. A constraint defines validity. A primary or unique constraint is often backed by a unique index in PostgreSQL, but the correctness promise comes from the constraint semantics.

A separately created index is an access path. It may make selected filters, joins, or ordering cheaper, but it does not automatically create a business rule. Indexes have costs: extra storage, cache use, work on inserts and updates, vacuum and maintenance overhead, and operational complexity. This week we identify indexes and the query shapes they might support. Week 7 will measure plans before deciding whether an index should remain.

## Slide 11: A constraint evidence record has four parts

A useful constraint record begins in plain language. State the invalid state to prevent and name the mechanism selected. Then show the actual definition in the intended environment. The definition alone is not enough.

Run a valid boundary case so an overly restrictive rule becomes visible. Run an expected-invalid case so the protected boundary becomes observable. Record the exact behavior and roll back the synthetic test. Finally, name a limitation. A foreign key can prove the requester identity exists, but it cannot prove that the requester submitted the ticket. A status check can protect vocabulary but not every legal status transition. Precise limits make the integrity claim credible.

## Slide 12: Lab 2: Build and test one integrity rule

Choose one rule from the lab and complete it individually. State the bad state in plain language before selecting a constraint. Predict one valid test and one invalid test. Install the rule in the disposable course schema using a descriptive constraint name.

Run both tests inside a transaction. Capture copied SQL and essential output rather than an account screenshot. The invalid test must fail because of the intended constraint, not because another required value was missing first. Roll back and confirm the fixture remains usable. Submit one record containing the rule, definition, success evidence, expected-failure evidence, and one limitation.

## Slide 13: Inspect first; constrain second; verify behavior third

This week connected metadata, integrity, and evidence. A schema x-ray establishes the current state before change. Keys protect identity, domain constraints protect values, and foreign keys protect referential existence. Indexes provide access paths and carry different costs.

The strongest habit is behavioral verification. A successful DDL command establishes that a definition was accepted. A valid boundary case shows that legitimate data still works. An expected failure shows that the intended bad state is rejected. The limitation states what the constraint cannot know. Next week we will apply the same precondition, change, verification, rollback, and limitation pattern to views and migrations that must preserve client behavior.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
