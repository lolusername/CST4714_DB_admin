# Metro Support Midterm

Name: [your name]
Section: [your section]
Environment and PostgreSQL version: [describe without credentials]

## Run order

[Explain how to run midterm.sql and what its reset deletes. Identify any files or tools needed.]

## Database checks

[Record actual table counts and the requester join result. Name three non-key integrity controls, identify their columns, and explain what each prevents.]

## Transactions

| Test | Before | Inside the transaction | After rollback or commit |
|---|---|---|---|
| Rollback | [observed] | [observed] | [observed] |
| Commit | [observed] | [observed] | [observed] |

[Explain the difference between the outcomes.]

## Blocking

Evidence source: [my live run / my saved Week 5 run / supplied trace analysis]

[Include the diagnostic SQL, blocked PID, blocking PID, row or resource, resolving action, and final values. Explain which values come from observation or the supplied trace.]

## One improvement

[Name the query or risk and your change. For the index route, include ordered IDs before/after, relevant plan lines, and measured index bytes. Explain whether the plan changed and one cost of keeping the index. For another route, use checks appropriate to that change.]

## Recovery plan

Status: [proposed plan / executed rehearsal]

[After Week 8: identify the source and schema, logical export command or steps, artifact name, separate restore destination, restore command or steps, and at least three verification queries or checks with expected results. Describe what the backup leaves out. Do not put real credentials here.]

## References and assistance

[Identify the supplied starter, notebook, documentation, and any assistance you used. Explain your own changes and observations.]
