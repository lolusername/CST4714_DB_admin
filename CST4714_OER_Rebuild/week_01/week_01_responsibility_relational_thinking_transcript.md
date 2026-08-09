# Week 1: Responsibility, Evidence, and Relational Thinking - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Responsibility, Evidence, and Relational Thinking

Welcome to Operating Cloud Databases. This course is not mainly about memorizing buttons in Supabase or MongoDB Atlas. It is about making a promise about a data system, observing what actually happened, and producing evidence another person can inspect.

This week has two connected jobs. First, we will separate the responsibilities of an application, a database engine, and a managed cloud provider. Second, we will rebuild the relational ideas that later SQL and administration work depend on. Those jobs belong together because an operator cannot diagnose a system without knowing both where a failure may live and what the data is supposed to mean.

## Slide 2: The course is organized around operating promises

A statement such as ‘the database is secure’ is too broad to test. A useful operating promise is smaller and more concrete. For example: a resident can read their own tickets but cannot read another resident’s tickets. That promise identifies an actor, an action, a resource, and a boundary.

Evidence might include one allowed query and one expected denial executed under the intended identity. Even that evidence has limits. It may prove the tested policy for the tested rows, but it does not prove that every application route uses the same identity correctly. Throughout the course, we will use this promise, evidence, and limitation pattern instead of relying on confident language or isolated screenshots.

## Slide 3: A database request crosses several responsibility layers

Imagine that a browser displays ‘could not load tickets.’ The message is a symptom at the client, not a diagnosis. The request may fail because the client built the wrong query, the network cannot reach the host, the managed project is paused, the database rejected authentication, the role lacks permission, the schema name is wrong, or the data does not match the filter.

The layers on this slide give us a disciplined search order. We first identify where the symptom was observed. Then we collect evidence at each boundary instead of changing several things at once. A managed service can remove some infrastructure work, but it does not remove the need to understand the database, schema, identity, query, and data layers that the customer still controls.

## Slide 4: Managed service divides work; it does not erase it

Shared responsibility is not a universal checklist because exact boundaries depend on the service and plan. The durable idea is that a provider operates the service infrastructure while the customer still makes choices inside and around the database.

If a team assumes the provider owns every security decision, it may place an administrator credential in application code. If it assumes automatic recovery without checking the plan, it may discover too late that the needed backup feature was not included. We will consult current official documentation for exact provider promises. We will not infer a promise from the word cloud. For every important control, name who configures it, who monitors it, and what evidence shows that it works.

## Slide 5: Evidence turns a symptom into a reproducible observation

A reproducible evidence record begins with the environment. ‘It failed in the cloud’ is not enough. We need the service, database, identity or role, tool, and any version that affects behavior. Next comes the exact action. A paraphrase can hide the real predicate, target, or command option.

Then record what was observed, not what was expected: the exact error, count, returned identifiers, plan node, or changed state. Interpretation comes after observation. Finally, state a limit. A successful query may prove connectivity and permission for one role, but it does not prove recovery readiness. These five parts make technical writing shorter because each sentence has a clear job.

## Slide 6: A screenshot can support evidence but cannot carry it alone

Screenshots are sometimes useful, especially when an interface state cannot be copied as text. The problem is not the image itself. The problem is treating the image as a complete explanation. A cropped green check may omit the query, role, database, time, and target. A dashboard can show a project exists without proving that an application can connect. A dump file icon can show that bytes exist without proving that the bytes restore.

A stronger packet surrounds the visual with reproducible context and an interpretation. Whenever text output can be copied safely, text is often easier to search, compare, and make accessible. The evidence should answer what happened, under which conditions, and what conclusion is justified.

## Slide 7: Lab 1: Map responsibility with evidence

Your first lab is individual. Choose Supabase or MongoDB Atlas and use the official documentation linked in the lab. Select one concrete control, such as database users, network access, project availability, or backup behavior. State one responsibility the provider claims and one responsibility the customer retains.

Then describe a realistic failure caused by confusing those responsibilities. Do not invent product features. Cite the official page and identify the first evidence you would inspect. Submit one compact record, not a collection of screenshots. If account access is blocked, the static documentation path produces the same reasoning evidence. No password, project identifier, IP address, or private account image belongs in the submission.

## Slide 8: Rebuild relational thinking before rebuilding SQL

We now shift from the system boundary to the meaning of stored facts. Many people remember pieces of SQL but have lost the relational model that makes SQL predictable. We will restore that foundation before asking the language to do more complicated work.

The key habit is to state what one row represents. Once the grain is clear, selection means keeping certain rows, projection means keeping certain attributes, and a join means creating matching pairs based on a relationship. SQL will return in full next week. Today the goal is to reason about the expected relation first, so that later a query result can be checked against a model rather than accepted because it ran.

## Slide 9: A relation represents one kind of fact at a stated grain

A relation schema describes a kind of fact. For example, `tickets(ticket_id, requester_id, status, subject)` says that each tuple records one ticket. The schema names attributes and their intended domains. The relation instance is the current set of ticket tuples at a particular moment.

Grain is the plain-language answer to ‘what does one row mean?’ It is not just a data-warehouse term. If one row means one ticket, adding ticket events through a join can produce multiple rows per ticket. If one row means one event, counting rows gives events, not tickets. Stating grain before a query protects us from results that look reasonable but answer a different question.

## Slide 10: Keys make identity and relationships testable

A candidate key is a minimal set of attributes that uniquely identifies a tuple. When a design selects one candidate as the primary key, it establishes the official row identity. In `users`, `user_id` identifies one user. In `tickets`, `ticket_id` identifies one ticket.

The `requester_id` value in a ticket can refer to `users.user_id`. That relationship lets us ask who requested each ticket. It also gives the database a rule it can enforce later with a foreign key. The key value does not copy the user's name into the ticket. It preserves an identity link, which reduces contradictory copies but means a read may need a join.

## Slide 11: Selection keeps tuples; projection keeps attributes

Selection and projection are easy to confuse because SQL places `SELECT` before `WHERE`. Relational algebra names the operations by what they do. Selection, written with sigma, keeps tuples that satisfy a predicate. If we select tickets whose status is open, every ticket attribute remains unless another operation removes attributes.

Projection, written with pi, keeps named attributes. If we project `ticket_id` and `subject`, those are the only attributes in the result. Mathematical relations are sets, so duplicate tuples are not retained. SQL uses bag or multiset behavior by default, so a SQL projection may keep duplicate rows unless `DISTINCT` is requested. That difference will matter next week.

## Slide 12: A join creates the matching pairs required by a relationship

A join does not simply place two tables side by side. Conceptually, it creates tuple pairs that satisfy a condition. Here, a user tuple matches a ticket tuple when `users.user_id` equals `tickets.requester_id`.

Maya has two matching ticket tuples, so a join result containing user and ticket attributes will contain two rows associated with Maya. Luis has one matching ticket, so he appears once. This row multiplication is correct for a one-to-many relationship. It becomes a bug only when we expected a different grain or used the wrong matching condition. Before executing a join, predict which pairs should exist and what one output row will represent.

## Slide 13: Relational algebra gives SQL a prediction to test

The path on this slide will guide the SQL review. Start with a question that can be checked. Then state result grain. For ‘which open tickets include requester names,’ one output tuple should represent one open ticket together with its requester.

Next identify relational operations. Select open tickets, join each selected ticket to the matching requester, and project the identifiers, subject, and display name needed by the question. Predict the output before writing SQL: which ticket identifiers should appear, how many rows should exist, and which attributes should be present. Finally, write and run SQL. When the result differs, inspect the model, data, and query instead of adding `DISTINCT` automatically.

## Slide 14: Lab 2: Represent a question as relational operations

This lab is individual and does not require a database connection. Read the Metro Support relation instances in the lab. For the assigned question, state what one tuple means in each source and in the expected result.

Then identify which tuples the selection should retain, which attributes the projection should retain, and which attribute equality creates valid join pairs. List stable identifiers rather than relying only on names. Finish with one check that could reveal a wrong answer, such as an expected count, a user with no matching ticket, or a ticket that should be excluded. Submit one artifact containing the model and prediction. The next class will translate this reasoning into executable SQL.

## Slide 15: The first operating habit is to make meaning and evidence explicit

This week established four habits that will return throughout the course. First, locate the responsibility boundary instead of treating a client symptom as a diagnosis. Second, state the grain of every relation and result. Third, predict relational operations before relying on SQL syntax. Fourth, record the environment, action, observation, interpretation, and limitation.

These habits are connected. A database operator needs to know what the data means, where a rule is enforced, and what evidence can confirm or challenge a claim. Before next week, you should be able to distinguish selection from projection, identify a valid join relationship, and describe why managed service does not mean the customer has no operational responsibility.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
