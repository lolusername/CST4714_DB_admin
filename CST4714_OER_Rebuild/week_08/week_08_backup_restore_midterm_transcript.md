# Week 8: Backup, Restore, and Midterm Synthesis - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Backup, Restore, and Midterm Synthesis

This week separates the existence of backup bytes from the ability to recover a usable database. We will create a logical PostgreSQL dump, record its size and checksum, restore it into a different database, and verify structure, data, relationships, constraints, and a meaningful query.

The second class integrates the PostgreSQL half of the course through the canonical midterm operations case. The midterm is not a new list of unrelated tasks. It asks you to build a small system, diagnose one operational issue, improve one boundary or workload, and document a recovery plan using the same evidence patterns practiced in class.

## Slide 2: A backup artifact is a claim about future recovery

A file with a familiar extension is not recovery evidence. It may be empty, incomplete, corrupt, incompatible, encrypted without a key, missing required metadata, or impossible to locate when needed. A useful artifact record names the source, method, creation time, tool version, size, checksum, retention, and protection boundary.

The restore target must be separate from the source so the test does not destroy the system it is supposed to protect. Verification then checks more than row count. We need object definitions, stable identifiers, relationships, constraints, types, and a meaningful application question. The result is still bounded by the tested failure and the artifact's omissions.

## Slide 3: RPO and RTO turn recovery language into objectives

The recovery point objective describes how much recent data loss the organization can tolerate, expressed as a time window. If the RPO is one hour, a daily logical export is not sufficient by itself. The mechanism and schedule must support the objective.

The recovery time objective describes how quickly acceptable service should return. The clock includes detecting the incident, locating credentials and artifacts, provisioning a target, restoring, verifying, and reconnecting clients. A command's execution time is only one component. Classroom recovery uses a small dataset, so it demonstrates the sequence and checks, not an enterprise RTO. State the objective and the scope honestly.

## Slide 4: Logical recovery is an ordered, verifiable workflow

Begin by identifying the source database, included schemas or objects, server version, client tools, and credentials. Confirm what the selected free plan does and does not provide. Create the logical artifact with a recorded command and exit status. Then identify the exact bytes with size and a cryptographic checksum.

Restore into a separate target. A successful `pg_restore` exit is necessary but not sufficient. Verify expected schemas and tables, counts and stable identifiers, key relationships, constraint behavior, and one meaningful query. Record omissions such as roles, provider network settings, secrets, scheduled jobs, or external object storage. Recovery is a system process, not only a database command.

## Slide 5: Tool compatibility is part of reproducibility

PostgreSQL client tools have compatibility rules. An older `pg_dump` may refuse to dump a newer server. Record the server version and select a compatible current client rather than trying random binaries. The custom format supports selective restore and `pg_restore` behavior.

The example uses environment placeholders to show command shape. A real database URL contains credentials and must not be committed, printed, or pasted into a public transcript. Record a redacted command, exit status, artifact size, and checksum. Restore to a different target URL. In the course notebook, a disposable local PostgreSQL service avoids cloud credentials and selects a client compatible with the running server.

## Slide 6: Recovery verification needs independent kinds of evidence

Structure verification checks that the expected database objects exist. Data verification compares counts and stable identifiers and inspects types or values that serialization could change. Relationship checks join parent and child records or look for orphans. Constraint checks deliberately challenge an important rule in a transaction.

Behavioral verification runs a query tied to the system's purpose, such as active tickets with requester names. Finally, list omissions. A logical database dump may not capture cloud project users, network access rules, application secrets, external files, or every extension setting. Several different checks are stronger than several screenshots of the same count.

## Slide 7: Lab: Create, restore, and verify a logical artifact

Complete the recovery notebook individually. It creates a disposable local PostgreSQL source, loads Metro Support data, selects a compatible client tool, creates a custom-format dump, and restores into a different database. Run from the first cell so the evidence sequence is reproducible.

Record artifact size and an abbreviated checksum, then complete the five verification categories. The notebook removes its disposable databases at the end. Submit the completed notebook after confirming that no URL, password, or token appears in cell source or output. The cloud transfer prompt asks how the procedure would change for Supabase without redefining the lab as a paid backup exercise.

## Slide 8: The midterm integrates one PostgreSQL operating story

The midterm is defined only in the canonical midterm file. The weekly guide links to it but does not create another deliverable list. The case asks for a small reproducible PostgreSQL or Supabase environment, one transaction or lock diagnosis, one access or performance improvement, and a recovery plan with verification.

The parts belong together. Schema and seed data create the system. The incident reveals operating state. The improvement uses evidence rather than a guess. The recovery section identifies what protects the work and what the selected free tier does not promise. The final technical note explains the decision and limitation in professional language.

## Slide 9: Four evidence threads make the midterm coherent

The build thread establishes the system's meaning: schema, constraints, small seed data, and a query whose result can be checked. The operations thread uses a transaction or blocking incident to show that the student can identify state and respond safely.

The improvement thread selects either access control or performance and supplies evidence appropriate to that choice. The recovery thread names the artifact, separate target, checks, and free-tier limitation. These are not four unrelated mini-projects. Reuse the same Metro Support or approved small case so identifiers, queries, and operating claims connect across the package.

## Slide 10: Cloud features and logical recovery cover different boundaries

Managed backup features can provide important automation, retention, and point-in-time options. Their availability and guarantees depend on the current plan and configuration. Do not claim them from a marketing phrase or from an older semester's interface.

The course logical artifact is portable and testable on a free path. It supports an independent recovery exercise, but it omits managed project configuration and may not meet a strict production RPO or RTO. The correct conclusion is not that one method is universally better. Define the failure, objective, scope, and operating constraints, then combine mechanisms as needed. The midterm should state the free-tier boundary accurately.

## Slide 11: Audit the evidence before submitting

A large file count does not make a strong midterm. Audit whether each required claim has an environment, identity, exact action, and observed result. Prefer stable identifiers, copied output, expected failures, and complete plan text over decorative screenshots.

Check that the package follows the canonical assignment rather than an older weekly note. Remove database URLs, passwords, tokens, private project identifiers, IP addresses, and unredacted account images. Finally, state limitations. A bounded claim supported by reproducible evidence is more professional than a broad claim that ignores what was not tested.

## Slide 12: Recovery completes the first half's evidence cycle

The PostgreSQL half of the course now forms one operating cycle. Schemas protect meaning. Migrations control change. Transactions and locks reveal concurrent state. Roles and RLS restrict access. Plans and indexes measure work. Logical backup and separate restore provide recovery evidence.

The midterm asks you to connect those skills through one small system rather than repeat every lab. After the midterm, we will revisit the same modeling and operating questions in a different family of systems. NoSQL and JSON will not erase relational thinking. They will make us ask which representation and database model best fits a workload, update pattern, and distribution need.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
