# Week 6: Identity, Permissions, RLS, and Secrets - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Identity, Permissions, RLS, and Secrets

This week asks a precise security question: which actor should be allowed to perform which action on which resource? We will translate that question into PostgreSQL roles and grants, then add row-level security for cases where the same table action should expose different rows to different identities.

Security evidence must include both sides of a boundary. One expected success shows that useful work remains possible. One expected denial shows that the restricted action is actually blocked. We will also separate Supabase Auth identities, token claims, PostgreSQL roles, row-level policies, and privileged service credentials so that the word user does not hide several different layers.

## Slide 2: Least privilege is a testable actor-action-resource rule

‘Make the application secure’ is too broad to implement or test. Least privilege becomes concrete when written as an actor-action-resource rule. For example: the reporting role may select from the active-ticket summary view but may not select directly from the users table or update tickets.

The rule must preserve useful work. A role that cannot complete its intended task is not a successful least-privilege design. It is a broken design with few privileges. Conversely, a role that succeeds only because it inherited an administrator membership does not prove the minimum grant. Build a matrix first, grant deliberately, and test from the intended role rather than from the object owner.

## Slide 3: A cloud request crosses several identity layers

A person or service first authenticates through some mechanism. In Supabase, an authenticated request may carry signed claims. The database-facing layer maps that request into PostgreSQL roles and session context. Grants determine which table-level operations are available, while row-level policies further restrict which rows qualify.

A successful website login therefore does not mean the request can query every table. A PostgreSQL database user is not automatically the same as the person in Supabase Auth. A service-role credential can bypass intended client restrictions and must not be exposed in browser code. When troubleshooting, identify the layer that establishes identity, the role used for permission checks, and the policy context used for row filtering.

## Slide 4: Design permissions in a matrix before writing GRANT

The matrix separates business need from SQL implementation. The reporting role needs `SELECT` on a stable view and should be denied direct update access. A ticket agent may need to read assigned tickets and update a limited set of columns, while changing requester identity remains outside the task. A resident request may read only rows owned by that identity. A migration job may receive temporary, narrowly scoped power.

The expected-deny column is part of the design, not an afterthought. It identifies the boundary that should be tested. If the denial is unclear, the requested privilege is probably too vague. This matrix also reveals when a view, function, column-level grant, or row-level policy is needed instead of a broad table grant.

## Slide 5: Grant through the intended interface and test as the role

The no-login role groups permissions without creating a separate password for this classroom test. Schema `USAGE` allows the role to resolve object names in the schema. The `SELECT` grant targets the active-ticket view rather than all Metro Support tables.

`SET ROLE` changes the active permission context for the session when the current user is allowed to assume the role. The view query is the expected success. The ticket update is the expected denial. If the update succeeds, inspect inherited memberships, ownership, existing grants, and whether the test actually changed role. Reset the role after the test. In a production system, role assumption and test setup require stricter administrative controls, but the allow/deny reasoning is the same.

## Slide 6: Lab 1: Build and test one least-privilege role

Complete this lab individually in the disposable schema. Begin with the access rule in plain language and the expected denial. Create or use the assigned no-login role, grant schema usage and the minimum object action, then change into that role for testing.

Capture one useful success and one denial that targets the intended boundary. A syntax error or missing table is not permission-denial evidence. Record current user and current role during the test. Clean up the disposable role if the lab directs it. Submit one record with the matrix row, SQL, observed allow and deny, and one limitation.

## Slide 7: Table permission answers what; RLS also answers which rows

Table-level privileges answer whether a role may attempt an operation such as `SELECT` or `UPDATE`. Row-level security adds predicates that determine which rows are visible or modifiable for the current policy context.

RLS is not a replacement for authentication, grants, secure application code, or testing. It is an additional database boundary. A privileged owner or role with bypass capability can observe behavior different from an ordinary request. We will build a small test harness with two resident identities, verify each resident's visible rows, and run a deliberate cross-resident denial.

## Slide 8: A grant opens an operation; a policy filters its row scope

A table grant determines whether the role may perform an operation on the relation. With RLS enabled, a policy then contributes row predicates. For `SELECT`, a `USING` expression determines visible existing rows. For updates, `USING` controls which rows can be targeted, while `WITH CHECK` controls whether the proposed new row is allowed.

A role can have `SELECT` privilege and still receive zero rows because no policy permits visibility. That result is not automatically an error. Conversely, testing as an owner that bypasses RLS can return all rows and falsely suggest the policy is broken. The test identity and active policy context must accompany the result.

## Slide 9: An RLS policy turns ownership into a server-side predicate

This local teaching harness stores a simulated user identifier in a session setting and compares it with `requester_id`. It makes the predicate easy to inspect without claiming that an arbitrary client-supplied setting is secure production identity.

When the setting is 101, the ordinary test role should see only tickets whose requester identifier is 101. Change the setting to 102 and the visible set should change. In Supabase, a policy commonly uses trusted token-derived helpers such as `auth.uid()` and an appropriately modeled ownership column. The production rule must establish identity through a trusted authenticated request, not through a value that an untrusted client can freely choose.

## Slide 10: RLS evidence needs identities, expected sets, and a denial

A complete RLS test begins with configuration evidence: table privileges, whether RLS is enabled, the policy definition, and the role used for the test. Then make the expected row set explicit for identity A and compare stable identifiers. Repeat under identity B with a different expected set.

Finally, attempt one operation across the ownership boundary. Depending on operation and policy, the system may return no row, affect zero rows, or raise an error. Record the actual behavior rather than demanding one universal message. These tests support the policy claim for the fixture and identities tested. They do not prove every API route supplies trustworthy claims or every privileged role is safely controlled.

## Slide 11: A secret grants power to whoever possesses it

A password, database URL, API token, or service-role key is a bearer of authority. Whoever obtains it may gain the associated access. A public repository, notebook output, browser bundle, or shared screenshot can copy that power far beyond the intended user.

Course notebooks prompt with `getpass`, keep secrets in memory, and avoid printing them. Production systems should use a supported secret manager, scoped credentials, rotation, and audit controls. A `.gitignore` entry reduces accidental addition of a file, but it does not erase a secret already committed. If exposure occurs, revoke or rotate the credential first, then remove it from visible history and investigate use.

## Slide 12: Lab 2: Build an RLS test harness

Complete the RLS test individually. Use the no-login role and session-identity harness supplied in the lab. Record the policy definition and confirm that the role does not own the table or bypass RLS.

For each resident, predict and observe the exact ticket identifiers. Then attempt the assigned cross-resident action and record whether it returns no row, affects zero rows, or is denied. Finish by mapping the local identity setting to Supabase's authenticated request and token-derived identity without treating them as the same mechanism. Submit one evidence record and confirm that no real token, URI, or account detail appears.

## Slide 13: Security claims become credible through bounded identities and tests

This week separated authentication, PostgreSQL roles, grants, row-level policies, and secrets. Least privilege begins with an actor-action-resource rule. Grants establish object-level operations. RLS narrows row scope. Secrets carry the power of the identity and must remain outside public source and output.

The evidence pattern is deliberately two-sided: useful work succeeds and out-of-scope work is restricted. Testing as an administrator cannot stand in for testing as the application role. Next week we will use the same baseline-change-remeasure discipline for query performance. An index recommendation, like a security recommendation, must be tied to a specific workload and observable evidence.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
