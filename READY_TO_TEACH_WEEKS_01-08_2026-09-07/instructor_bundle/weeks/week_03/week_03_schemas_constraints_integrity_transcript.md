# Week 3: Schemas, Constraints, and Integrity Testing - Spoken Transcript

## Slide 1

Last week we used SQL to decide which requests belong in a report and to check whether a change affected the intended row. This week we ask a different question: which incorrect states should the database refuse to store in the first place? We will stay with the same support-request case so that the new ideas concern the database, rather than a new business problem.

Consider a request assigned to a person who does not exist. A screen might prevent that choice, but an import or another program might send it. Or consider two spellings of the same status. A person may understand both, while an exact SQL comparison treats them as different values. A database rule can prevent some of these disagreements at the point where data changes.

Our first meeting is about understanding the current design. We will review a grouped query, look at where a current contact fact belongs, and query the database's descriptions of its own columns and rules. You will then inspect the actual course schema yourself. Our second meeting adds a small rule and tests what it accepts and rejects.

There is one individual SQL submission for each meeting. You do not need to learn a new application framework or create a report in another format. The important work is to connect a database definition to a particular result. We will use the full practice baseline, with eight users, twelve tickets, and twenty-one events, in a database intended for course exercises.

[Sources]
- Course textbook, Chapter 3: A Schema Protects Meaning.
- Course Metro Support setup and Week 3 lab assignments.

## Slide 2

This query reviews grouping and introduces one small piece of syntax that the first lab will use. Each result row represents a category. The first count counts every ticket in that category. The second count has a FILTER clause attached to it, so it counts only the category's tickets whose status is resolved.

Read the FILTER phrase as count this row only when this condition is true. It affects that aggregate. It does not remove the other tickets from the input to the total count. That difference is important: putting status equals resolved in the query's main WHERE clause would remove unresolved rows before both counts were calculated.

Look at parks. It has two tickets and zero resolved tickets. The category remains visible because its tickets still participate in grouping. Water has two tickets, both resolved. Across the five categories, the total column adds to twelve and the resolved column adds to four. Those numbers match the full baseline, not the smaller introductory notebook example from earlier in the course.

You can check one category with a simple filtered SELECT that lists its ticket IDs and statuses. That makes the summary less mysterious and gives you an independent way to catch a mistaken condition.

Your lab changes the subset being counted from resolved to active. Active means new, open, or in_progress in that assignment. Keep the category grouping and the total count. The idea is to adapt one expression while keeping the meaning of the result row stable. No extra table or join is necessary because category and status already belong to each ticket row.

[Sources]
- Course Metro Support ticket data and Week 3 category-report task.
- https://www.postgresql.org/docs/15/sql-expressions.html#SYNTAX-AGGREGATES

## Slide 3

Schema has two related meanings that are worth separating. In database design, we use it to mean the structure of the data: the tables, their columns, their relationships, and their rules. Saying that every ticket needs an existing requester is a statement about that design.

PostgreSQL also uses schema for a named container inside a database. Our metro_support schema contains the users, tickets, and ticket_events tables. Another schema in the same database can contain different objects. The public schema is one familiar default namespace, but it is not the only place tables can exist.

The query here uses metro_support.tickets. The part before the dot names the schema, and the part after it names the table. This form identifies the intended table without depending on a remembered search_path setting. A search path is the list of schemas PostgreSQL considers when a name is not qualified.

That detail matters in a web SQL editor. A new tab or request can use a different database session, so a setting made in an earlier session is not a dependable instruction for every later query. Using the qualified table name keeps the example clear and portable within the practice database.

The namespace is not a separate cloud project, database server, or independent backup. It helps organize names and permissions within one database. When we inspect information_schema.columns, that is another qualified name: columns is a metadata view inside the information_schema namespace. The same naming convention helps us distinguish application data from descriptions of that data.

[Sources]
- Course textbook, Chapter 3: Schema Has Two Related Meanings.
- https://www.postgresql.org/docs/15/ddl-schemas.html

## Slide 4

Maya is requester 101 and has tickets 1001, 1005, and 1009 in our baseline. The table on the left is a hypothetical alternative design. It repeats Maya's current email in every ticket. The actual course schema does not store the current email there; we are examining why it keeps that fact in users instead.

Suppose Maya changes the email associated with the account. If three independently writable copies exist, one update can leave the other two unchanged. We now have conflicting answers to a question that should have one current answer. This is an update anomaly. The difficulty is not that repeated text looks untidy; it is that several stored values claim to represent the same current fact.

The notation requester_id determines current email expresses a functional dependency under our account model. Knowing which account we mean determines its current email. This is a rule about valid states, not something proved merely because today's small sample happens to be consistent.

The course design keeps one current email in users and stores requester_id in each ticket. A join can retrieve the email when a report needs it. Changing the email in one account row then changes the current contact fact without rewriting every request.

Normalization studies dependencies like this and how to separate facts without losing their relationships. The chapter develops the formal normal forms. A historical snapshot has a different purpose: the contact detail recorded at submission may intentionally remain unchanged. Before removing repetition, decide whether the values represent the same current fact or different facts at different times.

[Sources]
- Course textbook, Chapter 3: Dependencies Explain Why We Separate Tables.
- Course Metro Support users and tickets.

## Slide 5

A data type describes what kind of value a column stores and which operations make sense for it. The same visible digits can represent very different things. Ticket 1004 is an identifier, while a monetary amount might require exact decimal arithmetic. A postal code is usually a text label, even if all of its characters happen to be digits. Leading zeros can be meaningful, and adding two postal codes does not produce a useful location.

Our baseline uses integer values for identifiers and text for subjects and status labels. Text permits many spellings. We can add a CHECK to restrict a vocabulary without pretending the text type already knows the approved words.

For time, distinguish an instant from a calendar date. A timestamptz value identifies an instant that different sessions can display in different time zones. It does not preserve the original named zone as a separate fact. A date represents a calendar day without an implied time of day. Which one is appropriate depends on the question the application must answer.

The numeric type supports exact decimal values. In numeric with precision and scale, the parameters control the total precision and decimal scale. You do not need to redesign the course dataset to use every type on this slide. The purpose is to connect representation to meaning rather than choosing whatever accepts the current sample.

Types establish a starting boundary. A valid integer can still refer to a missing user, and valid text can still contain a misspelled status. Relationships, missing-value rules, and other constraints add the application-specific meaning.

[Sources]
- Course textbook, Chapter 3: Data Types Express Allowed Representation.
- https://www.postgresql.org/docs/15/datatype.html
- https://www.postgresql.org/docs/15/datatype-datetime.html

## Slide 6

There are several different questions hidden inside the phrase good data. The first is identity. The ticket_id primary key means we can refer to one particular request. It rejects a duplicate identifier and requires that the identifier be present. The users table also has a unique email rule, but that is a separate chosen identity policy for this course's account model.

The second question is whether a value may be missing. Every ticket requires a requester_id, so that column has NOT NULL. An assignee_id may be missing because a newly received request can be waiting for assignment. Making every field required would not automatically improve this design. It could prevent us from recording a legitimate unassigned request.

The third question is whether a referenced person exists. A foreign key connects a non-null requester_id or assignee_id to an existing users.user_id. The direction matters: the ticket contains the reference, and the users table supplies the identity being referenced. Many tickets may refer to the same user.

Existence is a limited promise. The current assignee foreign key would find resident user 101, even though that person is not an agent. That particular reference does not express the rule that only eligible staff should receive assignments. We might represent eligible staff separately or enforce other application and authorization rules. Later security work addresses another part of this issue.

For now, distinguish these guarantees before choosing a mechanism. Required values, unique identities, and existing references solve different problems. Your metadata inspection will show which of them the baseline actually implements.

[Sources]
- Course Metro Support users and tickets definitions.
- Course textbook, Chapter 3: Keys Identify and Connect Facts.
- https://www.postgresql.org/docs/15/ddl-constraints.html

## Slide 7

The word metadata means data about data. PostgreSQL stores descriptions of its tables and other objects, and we can query those descriptions using SQL. That lets us distinguish the schema we think was installed from the schema that actually exists in this database.

Start with the tables and what one row represents. Our users table represents accounts, tickets represents requests, and ticket_events represents recorded events. Next inspect columns. A column description tells us its type, whether it allows a missing value, and whether a default supplies a value when an insert omits it.

Keys answer identity and relationship questions. Checks describe conditions applied to a proposed row. Indexes describe additional structures that PostgreSQL may use to find or organize rows. These are related parts of a design, but one does not automatically imply every other part. A status column can be text and required while still accepting a misspelling.

In your lab, you will run a small set of queries that exposes these facts. You do not have to memorize every PostgreSQL catalog column. The skill is recognizing what question a metadata query answers and connecting its output to a possible bad state. A list of names without interpretation is less useful than one definition that explains why an invalid requester cannot be stored.

The environment matters. Loading a setup file into one database does not install it in another. Use your personal practice environment, confirm the expected baseline, and read the actual query output before deciding what to add.

[Sources]
- Course textbook, Chapter 3: Inspect Metadata Instead of Guessing.
- https://www.postgresql.org/docs/15/information-schema.html
- https://www.postgresql.org/docs/15/catalogs.html

## Slide 8

Read this query as an ordinary SELECT applied to a different kind of information. Instead of selecting users from our application table, it selects descriptions from information_schema.columns. The filter names the metro_support schema and the users table. ORDER BY ordinal_position puts the descriptions in the table's defined column order.

The result contains six rows because the users table has six columns. It does not contain eight rows just because there are eight user accounts. This is another application of result grain: each output row describes one column. For example, the row whose column_name is email reports the type text and says the column is not nullable.

The is_nullable column uses YES and NO as metadata values. NO tells us that ordinary rows must contain a value for that attribute. A column_default describes what PostgreSQL can supply when an insert omits a value. A missing default does not itself mean that the column permits NULL. Those are separate properties.

The lab asks you to change the table filter from users to tickets. That is a small adaptation of a complete example. Compare requester_id and assignee_id in the resulting descriptions. One must have a value, while the other permits an unassigned request.

Information schema views are useful across SQL systems, although the exact objects visible can depend on the current account and privileges. Our exercise uses the owner of the disposable course schema. If you see no descriptions, first check the database, spelling, schema, and account rather than concluding that the design has no columns.

[Sources]
- Course Metro Support setup and Lab 1 metadata query.
- https://www.postgresql.org/docs/15/infoschema-columns.html

## Slide 9

This query reads pg_constraint, one of PostgreSQL's own catalogs. It returns a constraint's name, a short type code, and a readable definition produced by pg_get_constraintdef. You do not have to infer the rule from its name alone; the definition tells us what PostgreSQL actually enforces.

The conrelid condition restricts the result to the course tickets table. The expression with two colons and regclass asks PostgreSQL to resolve that qualified table name to its catalog identity. Here it avoids requiring us to look up and copy an internal object number.

The fresh baseline has a primary key, two foreign keys, and a check on the closing time. The type codes in the result include p for primary key, f for foreign key, and c for check. The two foreign keys refer to requester and assignee. The existing time check permits a missing closing time, but otherwise requires closing not to precede opening.

We are using PostgreSQL 15 for the reference test. Its NOT NULL information should also be inspected through the column metadata we just used. Absence from this particular constraint list does not mean every column permits NULL. Catalog representation can differ across PostgreSQL versions, so read the actual definition and use the appropriate metadata surface.

There is no allowed-status or allowed-priority check in the untouched baseline. That missing protection is what the next lab will address. If you already added one while practicing, your result can legitimately differ. Reset only your disposable course schema when the assignment asks for the baseline, and do not describe a changed schema as the untouched starting point.

[Sources]
- Course Metro Support setup.
- https://www.postgresql.org/docs/15/catalog-pg-constraint.html
- https://www.postgresql.org/docs/15/functions-info.html

## Slide 10

Constraints and indexes are related, but they describe different aspects of a database. Our primary key says ticket identifiers cannot be duplicated or missing. PostgreSQL creates a unique index to support that primary key. In that case, a rule and an access structure work together.

A priority CHECK evaluates the proposed priority. It does not automatically create a search index on the priority column. A foreign key requires a referenced user to exist. It also does not mean that PostgreSQL has automatically created every useful index on the referencing column. These distinctions matter when someone infers a design from a few object names.

Other indexes can support filtering, joining, or ordering without imposing our priority vocabulary. They store additional structure and need maintenance when relevant data changes. An index might improve one query and have little value for another. We will measure that tradeoff in Week 7 rather than creating indexes merely because the table has columns.

The small query at the bottom lists index names and definitions for our tickets table. Both the schema name and table name belong in the filter. On the fresh course baseline, it shows the primary-key index. That tells us what currently exists, not which additional structure we should recommend.

In today's lab you only inspect these definitions. You are not required to conduct a performance experiment or produce a tuning report. Connect the definition to the question it can answer: a constraint describes a validity rule, while an index definition describes a structure PostgreSQL can use to access or enforce particular data properties.

[Sources]
- Course textbook, Chapters 3 and 7.
- https://www.postgresql.org/docs/15/view-pg-indexes.html
- https://www.postgresql.org/docs/15/indexes.html

## Slide 11

You now have the examples needed for the first lab. Work individually in your personal PostgreSQL or Supabase practice database. The linked setup file resets only the named course schema, but that still means you should not use a project containing work you need to preserve under that schema. Confirm the eight-user, twelve-ticket, twenty-one-event baseline before interpreting results.

Begin with the category report. Our demonstration counted resolved tickets within each category. Your change counts active tickets instead, using the lab's definition: new, open, or in_progress. Keep the total count alongside it. The totals across categories should add to twelve, and the active counts should add to seven. There is no reason to add a join to that query because the needed values are already in tickets.

Then inspect the ticket columns, constraints, and indexes using the supplied metadata queries. Use the results to answer the three questions in the lab. Identify what requires a requester to exist, what permits an absent assignee, and whether the current schema limits the status vocabulary.

Finish with a short SQL comment recommending one missing protection. Support it with the definition you inspected or the absence of the relevant rule in the complete result. In the next meeting, we will implement a small improvement rather than ending with a recommendation.

Your submission is week_03_schema_xray.sql in Brightspace. Keep the queries and brief explanations together. You do not need a separate diagram, a screenshot collection, or a document describing every catalog row.

[Sources]
- Week 3 Lab 1: Inspect a Database Before Changing It.
- Course Metro Support setup.

## Slide 12

In the first meeting we inspected the current schema. Today we will change one part of it. The starting question is specific: can we keep the priority and status vocabulary consistent even when a write comes from a script rather than our usual form?

We will work through a complete priority example. We first inspect the values already stored, then add a named CHECK constraint. After that, we try an unsupported value and read the resulting error. We also try a valid value, inspect it inside a transaction, and roll it back so the practice row returns to its earlier state.

Both tests matter. A rule that rejects every value would stop the misspelling but also prevent legitimate work. A rule that accepts every value would let the demonstration run without protecting anything. The intended rule should accept the approved choices and reject a choice outside that vocabulary.

The lab asks you to adapt the worked priority rule to status. You will use the same table and the same style of SQL. There is no new software setup beyond the personal practice database you used earlier. Start with the baseline requested by the lab so earlier experiments do not create confusing duplicate constraints or changed values.

We will also revisit NULL because a CHECK expression and a WHERE filter use three-valued logic differently. Understanding that difference prevents a common mistake: assuming that an allowed-value check also makes a value mandatory. The closing explanation will describe a real protection and a real limit in plain language.

[Sources]
- Week 3 Lab 2: Make Misspelled Statuses Impossible.
- Course textbook, Chapter 3.

## Slide 13

Here is the problem that motivates the second meeting. Imagine an update stores the status as the capitalized words IN PROGRESS with a space. Our report looks for the lower-case value in_progress with an underscore. Those are different strings under the settings used by our practice database. The request can still exist while the report no longer includes it.

A text data type permits a wide range of character sequences. It cannot infer that these two spellings were intended to mean the same thing. A form might offer a dropdown, but a script or CSV import can use another write path. If the allowed vocabulary matters to every writer, we can make it a database rule as well.

We will use a CHECK constraint to list the accepted status values. That will make an unsupported spelling fail rather than quietly enter the table. The application still needs to handle the failure with a useful message. Rejecting a value is a storage decision, not a complete user experience.

This is related to the missing-request problem from Week 1, but the cause differs. In that case, a join removed requests without an assignee. Here, inconsistent spelling could cause a filter to miss a stored row. We should not assume every missing result has the same cause. The link is that we can name the source fact, the query condition, and the behavior we expect. A constraint protects the vocabulary; a correctly written report still has to use it.

[Sources]
- Course textbook, Chapters 1-3 and the Metro Support status values.
- https://www.postgresql.org/docs/15/ddl-constraints.html

## Slide 14

This table connects a few database rules to particular changes in our practice data. These are distinct examples, not a request to add five more lab tasks. The first four mechanisms already exist in the baseline. The priority CHECK is the new rule we are about to install.

Ticket 1001 already exists. Giving ticket 1004 that identifier would duplicate the primary key. Setting requester_id to NULL would violate the requirement that every ticket have a requester. Setting it to 999999 would keep an integer value present, but it would refer to a user who does not exist. That is the foreign-key case rather than the missing-value case.

The users table's email rule addresses duplication across account rows. Giving user 102 the email already used by user 101 would conflict with that rule. The database is enforcing the chosen account policy; it is not proving that an email address belongs to the person who typed it.

Finally, extreme is a text value, so its spelling fits the priority column's basic type. It becomes invalid under our intended allowed-value rule only after we add the CHECK. The contrast shows why a type alone is sometimes too broad.

When diagnosing a rejected operation, read which rule failed. An error caused by a missing required value does not test whether a different foreign key works. Good test inputs hold unrelated requirements steady so the intended boundary is the reason for rejection. We will use an existing ticket for the priority test to keep that comparison small and clear.

[Sources]
- Course Metro Support baseline definitions and synthetic records.
- https://www.postgresql.org/docs/15/ddl-constraints.html

## Slide 15

The first query tells us what priority values are currently stored and how often each appears. On a fresh baseline, high appears four times, low three times, medium four times, and urgent once. The total is twelve. These observations tell us whether the current rows fit the particular rule we intend to add. They do not establish that no other value could ever be appropriate for a different application.

Now read the ALTER TABLE statement. It names the existing metro_support.tickets table. ADD CONSTRAINT creates a named rule, tickets_priority_allowed. CHECK supplies the condition for a proposed row. The IN expression compares priority with the four approved text values inside the parentheses.

With this ordinary form of ADD, PostgreSQL checks the existing rows as well as enforcing the rule on later writes. If a stored value already violated the new condition, we would need to investigate that value and plan a correction rather than pretending the definition had succeeded. We are using a small practice table. A large production migration also raises locking and deployment questions that we will study later.

The constraint name is an identifier for the rule. The quoted words are data values. Keeping that distinction clear helps when reading an error message: it may name tickets_priority_allowed while showing extreme as the proposed value.

Run the addition once on the fresh baseline. If you revisit the exercise, inspect the saved definition before trying to add it again. A duplicate-object error on a repeat run is different from the expected rejection of an invalid priority.

[Sources]
- Course Metro Support priority values and Week 3 worked constraint.
- https://www.postgresql.org/docs/15/sql-altertable.html
- https://www.postgresql.org/docs/15/ddl-constraints.html

## Slide 16

This diagram represents the proposed new version of one ticket row moving through the priority rule. The upper path proposes high. That value belongs to our allowed list, so this check passes. Assuming the other applicable rules also pass, PostgreSQL accepts the update. It can become permanent when the transaction commits.

The lower path proposes extreme. That value is outside the list. PostgreSQL rejects the update and reports the named constraint. It does not partially store the invalid priority and wait for us to fix it afterward. The earlier row remains the starting state for a later attempt.

The central box is the condition, not the entire database engine. PostgreSQL may enforce other constraints, and the current account still needs permission to perform the operation. A successful priority check alone is not proof that every possible write is authorized or meaningful. In our demonstration, we control those other details so that priority is the property being tested.

The same row condition applies when data comes from an ordinary insert or update through a different client. A script does not become exempt just because it bypasses the usual form. An administrator who can alter or remove the rule is a different access boundary, which is one reason integrity design and permissions both matter.

Notice that our successful example is later rolled back. Passing this rule allows the change to proceed; it does not require the transaction to commit. That connects the schema lesson with the careful data-change rehearsal from last week.

[Sources]
- Course-authored editable priority-check diagram and synthetic test case.
- Course textbook, Chapters 3 and 5.

## Slide 17

Here is the actual test sequence. The priority CHECK must already exist. Ticket 1004 begins with priority low. Run the first UPDATE separately. It attempts to change that priority to extreme. The expected result is a check violation with SQLSTATE 23514 and the constraint name tickets_priority_allowed. The original row stays unchanged because PostgreSQL rejects the statement.

Do not place that deliberate failure in the middle of a larger batch and assume the following statements will run. An error can leave an explicit transaction aborted, and some editors group selected statements into a transaction. If the editor reports that state, run ROLLBACK before continuing. This is why the lab separates expected failures from the successful batch.

Now run the complete second block together. BEGIN opens the transaction. The UPDATE targets the same ticket and uses the valid value high. RETURNING shows ticket 1004 with high while we are inside the transaction. ROLLBACK then discards that test change. The final SELECT should show low again.

That sequence tests two different properties. Acceptance of high shows that the rule permits this intended value. Rejection of extreme shows that it excludes the unsupported value. Returning to low shows that the successful demonstration did not leave a permanent data change.

For your submitted SQL file, keep expected-failure statements commented out and record their short error details. The lab explains that format so another person can run the normal path without stopping at a deliberate error. Your status adaptation follows the same separation between an expected rejection and a valid rollback rehearsal.

[Sources]
- Week 3 Lab 2 and the course priority fixture.
- https://www.postgresql.org/docs/15/tutorial-transactions.html
- https://www.postgresql.org/docs/15/errcodes-appendix.html

## Slide 18

Recall that SQL can produce true, false, or unknown when a condition involves a missing value. The first two rows in this table behave as we would expect. High belongs to the allowed priority list, so the predicate is true. Extreme is outside the list, so the predicate is false and the CHECK rejects that row.

The third row deserves attention. Comparing NULL with the listed words produces unknown. A CHECK rejects a false condition; unknown does not fail that check by itself. So an allowed-value CHECK alone does not require a priority to be present.

Our baseline also declares priority NOT NULL. Those two rules work together: the value must be present, and the present value must belong to the list. We should not remove one simply because the other sounds like a general validation rule.

Compare this with a WHERE filter from Week 2. A WHERE clause keeps rows only when its condition is true. It filters out both false and unknown. We are using the same truth values for different operations, so the resulting behavior differs. Understanding the mechanism is more useful than memorizing that NULL is somehow special.

This slide is a conceptual comparison, not an instruction to remove NOT NULL from the course table. In the lab, inspect the existing nullability and keep the intended requirement. When explaining your result, say which rule does which job. An error for a missing priority may concern NOT NULL, while the extreme-value test should identify tickets_priority_allowed. That distinction tells us what the experiment actually tested.

[Sources]
- Course textbook, Chapter 2 on NULL and Chapter 3 on CHECK.
- https://www.postgresql.org/docs/15/ddl-constraints.html#DDL-CONSTRAINTS-CHECK-CONSTRAINTS

## Slide 19

The second lab uses the priority example we just worked through. Keep that rule, and write the matching status rule named tickets_status_allowed. The approved status values are new, open, in_progress, resolved, and closed. Before adding the rules, inspect the existing priority and status values as the assignment describes.

Work individually. Your task is an adaptation of the complete example, not a search for a new schema pattern. The lab gives two invalid UPDATE statements: one uses priority extreme, and the other uses status IN PROGRESS with a space and capital letters. Run them separately so each result is visible. Record the relevant constraint names rather than copying an entire application screen.

Then run the supplied valid update and rollback together. Inside the transaction, ticket 1004 can have high priority and status in_progress. After rollback, its original values should still be low and new. If those are not the final values, examine your starting fixture and which statements actually executed before drawing a conclusion about the rule.

The last metadata query inspects the two saved definitions. Add a short explanation of how these rules protect imports and scripts as well as a web form. Also identify something they do not decide. For example, an allowed status vocabulary does not establish which person is authorized to close a request.

Submit week_03_integrity_build.sql in Brightspace. The constraints, normal test path, commented expected failures, error notes, and short explanation belong in that one file. No index experiment or separate written report is part of this lab.

[Sources]
- Week 3 Lab 2: Make Misspelled Statuses Impossible.
- Course writing guide, Explain Why a Constraint Matters.

## Slide 20

We have now connected a design choice to an observable database behavior. The baseline already identified tickets and users, required some values, and protected references. Our additions keep priority and status within agreed vocabularies. That makes the data more consistent across ordinary write paths, including a web form, an import, and a SQL script.

The metadata query shows the installed definition and its name. The rejected test shows that an unsupported value encounters the intended rule. The accepted test shows that a legitimate value can still pass. The rollback check keeps the experiment repeatable by returning the data to its starting state.

There are still decisions outside these rules. An allowed status list does not decide who may close a ticket or whether a particular sequence of status changes makes sense. A foreign key can establish that an account exists without establishing that it belongs to an eligible agent. Naming those limits helps a developer understand what additional work the application or security design must perform.

This is a useful way to discuss the exercise in a technical conversation: I inspected the existing schema, found that the status vocabulary was unrestricted, added a named constraint, and tested both acceptance and rejection. The concrete result is more informative than saying only that I used PostgreSQL.

Next week we will look at changes that must preserve existing application behavior. Today's habits carry forward: identify the current state, understand the intended rule, make a controlled change, and check its consequences. Keep the explanation connected to the exact SQL and records you used.

[Sources]
- Course textbook, Chapters 3, 4, and 15.
- Week 3 lab outcomes.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
