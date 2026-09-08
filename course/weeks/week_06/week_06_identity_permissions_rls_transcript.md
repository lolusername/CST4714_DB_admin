# Week 6: Identity, Permissions, and Row-Level Security - Spoken Transcript

## Slide 1

This week we are deciding who should be able to do what with a database. We already know how to retrieve rows, define a view, and make a change inside a transaction. Those skills become part of an access-control test. A query that works for the database administrator may fail for a report reader, and a query that returns twelve rows for an administrator may return only two for a resident. Neither difference is necessarily a bug. The intended job determines which behavior is correct.

On the first day, our report reader needs a small part of the ticket data. We will create that interface, give a role permission to read it, and test a change that the role must not make. Your individual lab applies the pattern to an analyst who needs to count tickets by status. The report must remain useful without exposing private source tables.

On the second day, both residents will have permission to read the same table. Their visible rows will differ because each row records an owner. We will inspect the rule, test a request for someone else's ticket, and add another row. We will also connect that classroom model to Supabase's login and token system. You do not need to build an authentication service to understand the database rule, but we do need to distinguish the two systems accurately. Our experiments use only synthetic course data in a personal practice project.

## Slide 2

Imagine that Resident A has signed in to the repair application. Their own ticket is number one. The browser sends a request to an endpoint, which is a URL through which the application asks for data. In the example, GET means that the client is requesting a representation of a resource, and the number three identifies the requested ticket. Ticket three belongs to Resident B.

The application cannot assume that a caller will always request the number displayed on their own dashboard. A person can edit a URL, and an ordinary software bug can also send the wrong identifier. Removing a link from the page does not prevent the server from receiving that request. The server must check whether the authenticated actor may read the requested record.

Notice that Resident A's login can be completely valid while this particular request should still be refused or return no visible row. The password check and the data-access decision are different responsibilities. A long or difficult-to-guess identifier does not replace the latter. It might make accidental discovery less likely, but it does not define who owns the record.

Our database exercise will reproduce the essential distinction with four small rows. We can name the intended owner of every row and check the exact returned identifiers. That makes a subtle application-security problem observable without introducing a large web framework or asking you to attack somebody else's service. Every request and role in the exercise belongs to our own controlled fixture.

## Slide 3

The vocabulary on this slide helps us describe a failure precisely. Identity is the account or other actor claiming to perform an action. Authentication is how a system verifies that claim. It may involve a password, a signed token, or another approved mechanism. Authorization is the decision about which action that authenticated actor may perform on a particular resource. Auditing concerns the records that help us understand what occurred.

For example, the application might authenticate Resident A successfully and then reject access to Resident B's ticket. That is not contradictory. Authentication established the caller for that request; authorization limited the caller's access. A useful audit record might identify the actor, the requested resource, and the decision. It should not store the caller's raw password just to prove that authentication occurred.

These terms also apply to programs. A reporting job can connect using a database login and receive only the privileges its job needs. A migration job may have more powerful permissions because it changes the schema. Giving both programs the administrator's credential erases a useful separation between their responsibilities.

Throughout the lab, we will identify the effective database role before interpreting the query result. That lets us say who actually performed the database operation. It does not prove that a real human completed a production login flow. We are testing one part of the system deliberately, and naming that part keeps our conclusion technically useful.

## Slide 4

The first row describes our demonstration. A report reader needs the identifiers, categories, and statuses of open tickets. It does not need residents' email addresses, and it does not need to change requests. This is a specific requirement that we can turn into a view, grants, and tests. A vague request to give the application access would not tell us which operations should be allowed.

The second row describes your lab. The analyst needs a summary interface covering all twelve tickets, so they can count by status. That differs from the demonstration's three open tickets. We will use the same permission pattern while changing the work the interface supports. The analyst still has no reason to read private source records or update a ticket.

Least privilege means choosing permissions sufficient for the intended task without adding unrelated powers. It does not mean denying everything. An analyst who cannot produce the required report has not received a useful design, even if the database is very restrictive. We therefore need a positive test as well as tests of prohibited actions.

This is also a design conversation. If the analyst later needs another field, we should ask what decision it supports and whether a less sensitive representation would suffice. We should not automatically grant every base table to avoid revisiting the requirement. A small, documented interface gives the application a clearer contract and gives us a manageable set of behaviors to verify.

## Slide 5

PostgreSQL uses roles for both login identities and permission groups. The first statement creates a role named report_reader_demo with NOLOGIN. That means it cannot authenticate as a database login on its own. We have not created a new password. The role is a named container for privileges that we will assign next.

The second statement grants membership in that role to our current administrative user. Membership makes the controlled role switch possible. NOLOGIN does not mean that nobody may assume the role. It means that the role is not itself a direct login account. This separation is useful when multiple logins need the same set of permissions.

The lower block begins a transaction, switches the effective role locally, and selects two built-in identity values. Session_user identifies the original database login. Current_user identifies the effective role for the operation. During our test, current_user should be report_reader_demo. Your original login name may differ from mine, and that is expected. We are not matching somebody else's account name.

ROLLBACK ends the transaction and the local role setting. Run the entire block together so the role change and observation occur on the same connection. A new web-editor execution may use a different pooled connection. Also keep role creation in your own practice environment: PostgreSQL roles exist across the database cluster rather than belonging only to one schema. We must not delete a shared role merely because its name resembles our exercise.

[Sources]
https://www.postgresql.org/docs/15/sql-set-role.html
https://www.postgresql.org/docs/15/user-manag.html

## Slide 6

Here is the complete interface for the report reader. The schema called security_demo separates our demonstration objects from the base course data and from your lab. A schema is a namespace, as we learned earlier; creating one does not automatically give every role permission to use it.

The view selects three named columns from the Metro Support tickets table and keeps rows whose status is open. It does not select email addresses or event notes. It is not a second stored copy of the ticket data. Querying the view runs its defined query against the underlying table. With the supplied fixture, there are three open tickets.

We then grant schema USAGE on the demonstration and source namespaces. USAGE permits looking up objects in those schemas; it does not itself allow reading or changing every table in them. Including source-schema USAGE lets our later negative test reach the table privilege check rather than fail earlier on the namespace. The final statement grants SELECT on this particular view. It does not grant SELECT or UPDATE on the source tickets table.

The administrative owner creates the view and already has the source access needed for its definition. A normal view can use that owner's underlying-table privileges. We will examine the consequence shortly. For now, the important point is that schema access, view access, and base-table access are distinct. We can give the reader a usable interface without giving it every power held by the person who created that interface.

[Sources]
https://www.postgresql.org/docs/15/ddl-priv.html
https://www.postgresql.org/docs/15/sql-createview.html

## Slide 7

This is our positive test. We begin a transaction and set the effective role locally to report_reader_demo. The SELECT includes current_user alongside the ticket fields so that the result identifies the role that actually ran the query. An administrator's successful SELECT would not establish that this restricted role can read the view.

In the original Metro Support fixture, the open tickets are 1001, 1007, and 1011. We order by ticket_id to make the small result easy to compare. Every returned row should name report_reader_demo and have status open. If you see additional tickets, first check whether your fixture has changed. If you see a different effective role, the test did not run in the intended context.

The final rollback ends the test transaction and restores the earlier local role state. It is safe to use the same pattern around a read because we want a consistent way to run actor tests. It becomes especially useful when a later test attempts a write that should fail.

Some web SQL editors show only the final command result rather than every intermediate SELECT. That is a display limitation, not a reason to remove the transaction boundary. The lab includes a small Colab cell that executes each query through one persistent connection and prints its result. The Python code is only a display aid. Your required submission remains the SQL file with the query and its observed outcome, not another notebook assignment.

## Slide 8

The negative test uses the same role and transaction pattern, but now attempts to change one ticket. The WHERE clause limits the target to ticket 1004. We do not use an unrestricted UPDATE just because we expect permissions to reject it. A mistaken grant is exactly the kind of problem this test is supposed to reveal.

The intended result is SQLSTATE 42501, an insufficient-privilege error. Our report reader has permission to use the source schema, but it has no UPDATE privilege on the tickets table. PostgreSQL should reject the operation. A missing table error or a network failure would not demonstrate that authorization boundary.

After an error, some clients stop executing the rest of the submitted batch. If that happens, run ROLLBACK separately on the same connection so the failed transaction and its local role setting end. The Colab display helper handles this with a transaction that rolls back even when a write unexpectedly succeeds. It also catches the database error after leaving that transaction context.

Suppose the update does succeed. We have found a permissions problem rather than passed the lab. Rollback prevents that test from permanently changing the row, and we then investigate how the role received the privilege. Direct grants, inherited roles, and PUBLIC can all matter. After correcting the relevant grant, repeat both the allowed and denied tests. A fix that also breaks the required report is incomplete.

## Slide 9

This diagram explains why our positive test can work without direct SELECT permission on the tickets table. The reader receives SELECT on the view. For a normal PostgreSQL view, the underlying relation access is generally checked using the view owner's permissions. The owner can read tickets, and the view definition exposes only the selected columns and open rows.

This is a deliberate interface design, but it has limits. A view is not automatically safe for every purpose merely because it hides some fields. If a resident-facing view is owned by a privileged role, its underlying access can differ from what the resident would receive by reading the table directly. In particular, elevated ownership can change how row-security policies are applied. We must test the actual interface the caller uses.

PostgreSQL 15 and later support security_invoker views. With that option, the underlying permissions and row policies use the invoking user's context. That design also requires the caller to have the relevant base-relation permissions. It is not a magic switch that keeps our current view-only grants unchanged and makes every design secure.

For Day 1, we are deliberately teaching a limited reporting view. For Day 2, we will read a policy-protected table as ordinary resident roles. Those are different access designs. Keeping them separate prevents us from accidentally treating the report reader's elevated-owner view as a resident-private API. The lesson is to verify each exposed path, not only the object behind it.

[Sources]
https://www.postgresql.org/docs/15/sql-createview.html

## Slide 10

These four results can look similar when an application simply displays that something went wrong. Their causes are different. Network unreachable means the client could not reach the selected endpoint. PostgreSQL did not get a chance to apply our table grant. Changing privileges cannot create a network route.

Password authentication failed means the intended database login did not authenticate. Check the database credential and endpoint rather than substituting an API key. An API key and a PostgreSQL password serve different connection paths. With Supabase, a session-pooler address is often the appropriate IPv4-compatible route for these persistent classroom connections when the direct database hostname is not reachable from the client.

SQLSTATE 42501 identifies an insufficient-privilege failure, but we still need to identify the effective role, object, and operation. For example, missing schema USAGE and missing table SELECT are different grants even though both can prevent a read. The error must match the boundary we intended to test.

Zero rows without an error is different again. The query may match nothing, or row-level security may exclude the requested records. In Day 2 we will deliberately produce that result while the table read itself is permitted. It is not appropriate to respond by granting everything. Start with a small known fixture, identify the actor, and compare the expected row identifiers. Those observations tell us which part of the request deserves investigation.

[Sources]
https://supabase.com/docs/guides/database/connecting-to-postgres

## Slide 11

Your first lab applies this permission pattern to an analyst. The supplied view includes all twelve tickets, with selected reporting fields but no resident email or internal event notes. Its role is metro_analyst_lab, which is separate from the report_reader_demo role in the live example. Run the setup only in your own practice project.

First verify the supplied read as the analyst. Then write a grouped query that counts tickets by status through the view. GROUP BY and COUNT are the same operations we practiced in the SQL review. The new requirement is that the useful report must run under the restricted role. Its group counts should add up to twelve without any broad read grant on the base tables.

The denied tests attempt to read resident email and update a ticket. A permission error is the intended result; a typo or failed connection is not. Keep those tests inside the guarded transaction pattern. If the web editor hides the SELECT output, the optional display cell can run the same SQL and show it. It does not replace the SQL or add another required deliverable.

In your SQL comments, explain what the analyst can do and which observations support the restriction. Then run the lab's cleanup as the administrator. The submission is one SQL file containing your setup, tests, grouped report, brief explanation, and cleanup. The goal is to implement and explain a working access boundary, not to produce a separate security essay.

## Slide 12

We now have a different requirement. Both residents may read a table, but each resident should see only the tickets that belong to them. Granting SELECT on the table is necessary for the read, but it does not express that ownership condition by itself. Row-level security adds the row rule.

Our fixture contains four tickets and two resident identities. We will run the same SELECT for each identity so the only intentional change is the actor. If the results differ in the expected way, we can connect that difference to the ownership rule rather than to a different WHERE clause written by each caller.

We will also request another resident's ticket directly. That brings us back to the changed URL from the opening example. A caller's choice of identifier must not override the policy. Finally, we will insert one additional ticket as the administrator and repeat the resident reads. A correct ownership rule should apply to that new record without an updated list of allowed ticket numbers.

The classroom roles are deliberately small and observable. They let us study authorization without first building a login service. Later in the sequence we will explain how Supabase normally represents many signed-in people through one shared database role and verified user claims. We are not going to pretend that switching a local database role is the same as testing a complete production login flow.

## Slide 13

Read this entire fixture before thinking about the policy syntax. Tickets one and two belong to resident_a_demo. Tickets three and four belong to resident_b_demo. The subject column gives the records recognizable meaning, but ownership is represented explicitly by owner_role. We should not infer ownership from a ticket's number or wording.

The instructor's setup creates this table in security_demo, the namespace used for the live demonstrations. It creates two NOLOGIN roles and grants our administrative user membership so that we can run controlled tests as either actor. Each resident role receives schema USAGE and SELECT on this table. Neither receives INSERT, UPDATE, or DELETE privileges.

With those grants and row-level security still disabled, an ordinary reader can select all four rows. That gives us a useful baseline. A table grant permits the operation on the relation; it does not automatically know that the text in owner_role is meant to restrict visibility. We must define that rule.

Your lab uses a separate schema called security_lab and roles named resident_101_lab and resident_102_lab. The same four subjects make the comparison familiar, but the demonstration and student objects do not share names. That separation matters when you rerun a setup or clean up an exercise. We are operating on synthetic records, not real residents, and we should remove only the objects that this particular exercise created.

## Slide 14

The first statement enables row-level security on our demonstration table. Enablement changes the access rules, but it does not supply the ownership condition by itself. Once RLS is enabled, an ordinary role with SELECT but no applicable allowing policy sees no rows in this simple case. That is the default-deny behavior we can observe before creating the policy.

The CREATE POLICY statement names the rule read_own_demo. ON identifies its table. FOR SELECT limits this policy to reading, and TO names the two ordinary resident roles. USING contains the condition applied to existing rows for this operation. We compare the owner_role value stored in each row with current_user, the effective database role for the test.

For Resident A, the comparison is true for rows one and two. It is false for three and four. PostgreSQL keeps the allowed rows even though our SELECT does not include an ownership WHERE clause. The database rule is therefore not dependent on the application remembering to add the filter every time.

Do not replace the comparison with true just to make an empty result disappear. That would permit every row for this covered read. Also remember that a policy does not grant SELECT on the table. We deliberately set up the object privileges first and then added the row restriction so we could reason about each layer. A complete test identifies both the actor's grants and the rows its policy allows.

[Sources]
https://www.postgresql.org/docs/15/ddl-rowsecurity.html

## Slide 15

This query is intentionally ordinary. It selects the effective role, ticket identifier, and subject, then orders by ticket number. There is no condition saying that the owner must be Resident A. The policy supplies the ownership restriction as part of access to the table.

We begin the transaction, use SET LOCAL ROLE for resident_a_demo, and run the SELECT before rolling back. The expected identifiers are one and two. The current_user value in the result should identify resident_a_demo. That lets us verify that we observed the intended actor rather than the administrator.

Next we repeat the complete batch with only the role name changed to resident_b_demo. The SQL query stays the same. Now the expected identifiers are three and four. The underlying table still contains four records; the different result does not mean that the first query deleted or moved anything. It means that the visible row set depends on the actor and the policy.

This comparison is stronger than checking that each query returns two rows. Two identical counts could hide the wrong identities. We inspect the actual ticket IDs and their ownership. We also keep the entire actor test on one connection so a pool cannot silently change the context between separate submissions. If an editor hides the intermediate result, we use the lab's display helper to show the same query through a persistent connection, rather than drawing conclusions from an unobserved result.

## Slide 16

Now Resident A requests ticket three explicitly. We have added a WHERE condition to the SELECT, but we have not changed the policy. The query condition identifies one desired ticket. The policy separately requires that the row's owner match the effective role. For ticket three, those two requirements cannot both hold for Resident A.

The result should be zero rows without a permission error. The role is allowed to perform SELECT on the table. The requested record simply does not belong to the set that this role may see. This is why we must not define every successful negative test as an error message. A restricted read often works by excluding rows.

Our controlled fixture gives us knowledge that a general caller would not have. We know that ticket three exists and belongs to Resident B. An empty response in an arbitrary application could also mean that the requested record does not exist. We should not claim that an empty result proves hidden ownership unless our test setup gives us the necessary facts.

The example corresponds to changing the ticket number in a browser request. The request can choose which ticket it wants, but that choice does not rewrite the authorization rule. We are testing the database layer directly today. Before deploying a real application, the same behavior needs verification through its actual authenticated request path, including any views or server components that might use a more powerful credential.

## Slide 17

The administrator now adds ticket five for Resident A. The INSERT names the columns explicitly, which makes the meaning of each value clear. The new subject is Blocked drain. This is a data change, not a change to the policy. Resident roles still have SELECT only, so we execute the insertion as the administrator rather than quietly granting them write access.

Predict the two SELECT results before running them. Resident A should now see one, two, and five. Resident B should still see three and four. The same ownership expression applies to the new record because its owner_role value is resident_a_demo. We do not edit the policy to add the number five.

This checks a limitation that a fixed four-row test could miss. A rule listing ticket numbers might accidentally produce the correct initial result, then fail as soon as a new ticket arrives or ownership changes. Describing the relationship between the row and actor makes the rule reusable across new data.

In your lab, you will add ticket five for the other resident, resident_102_lab, in your separate security_lab schema. You will write the short INSERT yourself and rerun both resident tests. That is an adaptation of this demonstration rather than a new large project. If you rerun an INSERT with the same primary key, PostgreSQL should report a duplicate key. Inspect the existing row or use the documented reset path instead of repeatedly inserting the same identifier.

## Slide 18

The administrator's result is different from either resident's result. After the demonstration insertion, Resident A sees one, two, and five. Resident B sees three and four. The administrative context can see all five. That does not, by itself, mean that the policy failed for the residents.

PostgreSQL table owners normally bypass row-level security. Superusers and roles with the BYPASSRLS attribute also bypass it. A table owner can use FORCE ROW LEVEL SECURITY to make ordinary owner access subject to row policies, but that does not remove a superuser's or BYPASSRLS role's separate bypass ability. We must identify the actual role and its powers rather than assume every administrator account behaves identically.

Supabase's SQL Editor commonly runs with elevated database privileges. That makes it useful for defining tables and policies, but an unrestricted result in that context is not a test of what an ordinary application user receives. The role-switch tests deliberately change the effective role before selecting.

This distinction also matters for a backend service. If it connects using a privileged credential, it may not receive the same row restrictions as a resident request. The service then needs appropriate authorization in its own trusted path. Our positive and negative resident tests establish the behavior of those ordinary roles. They do not establish that every administrative tool or API endpoint exposes data safely. A useful security claim identifies its tested actor and interface instead of saying that the whole database is secure.

[Sources]
https://www.postgresql.org/docs/15/ddl-rowsecurity.html

## Slide 19

Our classroom model gives each resident a distinct PostgreSQL role. Supabase applications usually distinguish people differently. A user signs in through Supabase Auth and receives an access token. The application presents the token with requests, and the receiving service verifies it before using its claims. A claim is a statement carried by the token, such as the user's identifier.

Many signed-in users can reach the database through the same authenticated role. That role therefore does not identify one particular person. The user-specific request context supplies the distinction, and auth.uid is a Supabase helper that returns the user identifier for the current authenticated request.

The arrow in the diagram represents a trust boundary. The browser is not allowed to establish ownership merely by putting somebody else's ID in a request body. A verified token binds the request to an authenticated identity under the service's rules. Creating a JSON object that says user_id equals another person's ID is not equivalent to authenticating as that person.

A signed JSON Web Token is not necessarily encrypted. Its payload may be readable, while the signature helps the receiving service verify that its claims have not been altered. A usable access token is still a credential and should not be printed in a shared notebook. Today we are learning the relationship among these layers. We have not built a login system or executed a real user-token request merely by using SET ROLE in PostgreSQL.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security
https://supabase.com/docs/guides/getting-started/api-keys

## Slide 20

This policy illustrates how the ownership comparison changes for a Supabase application. The role named authenticated permits the policy to apply to signed-in requests. The row's requester_auth_id is compared with the verified user identifier returned by auth.uid. The nested SELECT is the form used in Supabase's guidance; the important idea here is comparing the stored owner with the authenticated request identity.

Do not paste this into today's unchanged Metro Support table. The teaching fixture uses integer requester IDs, while Supabase Auth uses UUID identifiers. A UUID is a 128-bit identifier, often written as groups of hexadecimal characters. It is not a password, and replacing one type with another does not automatically establish which real person owns each old record.

A real migration must populate the ownership column correctly. The intended role also needs the necessary object privileges, row security must be enabled, and the application must use the intended API route. A nullable column full of missing values would not complete that design.

If auth.uid returns NULL because the request lacks an authenticated user context, equality with that value is unknown rather than true. Recall our SQL three-valued logic review: a row condition must be true to admit the row. This connects a familiar SQL mechanism to an access-control outcome. The illustrative policy is not a completed deployment or proof of hosted authentication. It explains what must replace the classroom role-name comparison when identity comes from verified application-user claims.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security
https://www.postgresql.org/docs/15/functions-comparison.html

## Slide 21

Reading existing data and accepting new data are related but separate decisions. USING describes the existing rows available to a covered operation. In our read-only lab, it decides which tickets a resident's SELECT may return. WITH CHECK describes which proposed new row values are permitted for an INSERT or relevant UPDATE policy.

Suppose an application allows Resident A to submit a ticket. It must not allow that request to assign ownership to Resident B merely by changing an input field. An insert policy can compare the proposed owner identifier with the authenticated user's identifier. If they do not match, the new row should be rejected. The policy fragment on the slide illustrates that comparison.

An INSERT privilege is still required. A policy is not a substitute for the object grant. Likewise, giving INSERT on the table does not by itself establish who may be named as the owner. We need the operation-level permission and the appropriate condition for the resulting data.

For updates, designs may need to constrain both the existing row and its proposed replacement so a user cannot take over or reassign another user's record. That is beyond the required implementation today, but the distinction explains why a SELECT policy alone is not a complete read-write application design. Our lab intentionally keeps resident roles read-only. The administrator adds the fifth row, and the resident tests evaluate visibility. State that scope when explaining what you implemented rather than claiming to have tested every kind of write.

[Sources]
https://supabase.com/docs/guides/database/postgres/row-level-security

## Slide 22

The word key is not enough to tell us whether a value belongs in browser code. A Supabase publishable client key identifies an application component. It is designed for client use, but it does not identify which resident has signed in. A user's access token supplies authenticated user context for the request and should be treated as a usable credential.

A secret key or legacy service-role key has a different purpose. It belongs in a trusted server-side component and can provide elevated access that bypasses row policies. It must not be embedded in a public notebook or shipped as part of browser source. Legacy anon keys and newer publishable keys also differ in format; check the documented key type rather than guessing from the variable's name.

A PostgreSQL password or credential-bearing connection URI is another credential again. It connects as a database login and is not a substitute for a resident's application token. Our optional Colab helper prompts for the database URI at runtime so it does not have to appear in the source cell. Protect the notebook outputs too, and close the connection when the operation finishes.

If a secret appears in Git or another shared location, revoke or rotate it first. Deleting the visible line does not invalidate a value that somebody already copied or that remains in history. Then update legitimate consumers and investigate its use through the appropriate logs. The practical lesson is to connect credential handling to the power that credential grants, rather than treating all strings called API keys as interchangeable.

[Sources]
https://supabase.com/docs/guides/getting-started/api-keys

## Slide 23

Your second lab keeps the same compact structure: setup, a controlled experiment, and an explanation with cleanup. Use your own PostgreSQL or Supabase practice project. The supplied fixture creates resident_101_lab and resident_102_lab, with two tickets initially assigned to each role. These are database roles for the exercise, not real residents or Supabase Auth accounts.

Run the two resident queries and the direct lookup for ticket three as resident_101_lab. The first resident should see one and two, the second should see three and four, and the direct lookup should return no row. Check the effective role as well as the returned identifiers. A result under an administrative owner does not substitute for those tests.

Next, write an INSERT as the administrator for ticket five, owned by resident_102_lab. Choose an ordinary synthetic subject. Rerun the resident queries without changing the policy. The first resident's set should stay the same; the second should gain the new ticket. Your file should contain the query you wrote and the observations that explain its effect.

Write the final comments to the application's developer. Explain what was visible, what the direct lookup returned, and why the owner comparison is a different test context. Name the remaining real-application check: using each person's verified login token through the intended request path. Then run the supplied cleanup. Submit the SQL file in Brightspace. There is no separate essay, screenshot collection, or authentication application to build for this lab.

## Slide 24

We can now describe three concrete outcomes. The analyst can produce the required report through a limited interface. A prohibited source-table action is rejected for the tested role. Each ordinary resident sees the expected ticket identifiers, including the correct change when a new owned ticket is added.

Those observations are more informative than saying that RLS is enabled or that a GRANT statement ran successfully. Configuration describes what we intended to establish. Testing as the actor reveals what that context actually permits. The positive case matters because the application still needs to function, and the negative case matters because unrelated access must remain unavailable.

Our conclusions also have limits. These exercises do not prove that every API endpoint uses the same context, that every token is handled correctly, or that a leaked administrative credential is harmless. A production review must examine the actual request paths and privileged components. We have learned the mechanism and practiced a small, repeatable way to investigate it, not certified a complete application.

Before leaving the exercise, use the documented cleanup for your own roles and schema. Keep the SQL and observations, but not credentials. The next topic is performance: once a query is both correct and permitted, we need to understand the work PostgreSQL performs to produce its result. The same discipline carries over. Identify the case, observe the mechanism, make a controlled change, and explain the specific result rather than relying on a reassuring label.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
