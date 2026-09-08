# Module 15: Professional Evidence Makes Technical Skill Visible

## Operating Question

How can you explain what you learned so an instructor, teammate, or interviewer can
see the evidence, reasoning, safety, and tradeoff rather than only a list of tools?

## Learning Outcomes

After this module, you can:

- connect course artifacts to database, cloud, backend, data, and security work;
- review a database system through model, query, access, performance, and recovery
  evidence;
- present a final project without exposing credentials;
- write a concise portfolio artifact that another person can run or inspect;
- answer technical and behavioral interview questions with specific evidence; and
- identify a realistic next skill rather than claiming production mastery.

## 1. Employers Evaluate Actions and Evidence

Tool names matter less when they are unsupported. Compare:

> Familiar with PostgreSQL, Supabase, MongoDB, Atlas, GitHub, and Python.

with:

> Built and verified a three-table PostgreSQL schema with named integrity
> constraints; reproduced and diagnosed a two-session blocking incident using
> `pg_stat_activity` and `pg_blocking_pids`; tested a workload-driven composite
> index with before/after plans; and restored a logical dump into a separate target
> with structure, relationship, and behavior checks.

The second statement identifies actions, evidence, and scope. It does not claim
years of production operation.

## 2. The Course Skill Matrix

| Workplace need | Course evidence |
|---|---|
| understand a data model | relational schema, JSON alternatives, embed/reference decision |
| query and verify | SQL/MQL files, result-grain notes, aggregation checks |
| protect access | role/grant matrix, RLS allow/deny tests, credential-safe notebooks |
| investigate incidents | lock relationship, query plan, polyglot timeline |
| improve performance | unchanged workload, before/after evidence, index tradeoff |
| recover data | logical artifact, separate restore, verification runbook |
| use cloud services | Supabase/Atlas shared-responsibility and free-tier decisions |
| automate carefully | small Python connection/import/recovery notebook |
| communicate | claim-evidence-tradeoff responses and final demonstration |

These skills can support database administration, cloud support, application
support, backend development, data engineering, cybersecurity operations, and
technical analysis. Job titles differ; the evidence verbs transfer.

## 3. Review a System Through Six Questions

1. **Purpose:** what workload and user decision does the system support?
2. **Model:** what does one record mean, and how are relationships represented?
3. **Integrity and access:** which bad states and unauthorized actions are refused?
4. **Queries and performance:** which questions matter, and what plans/indexes
   support them?
5. **Reliability:** what failure is tolerated, what is backed up, and how is restore
   verified?
6. **Reproducibility:** can another person rebuild, inspect, and explain the result
   without receiving a secret?

Use these questions for the final project, a portfolio review, or an interview
system-design prompt.

## 4. Present the Final Project as a Decision Story

A focused demonstration shows:

1. problem and user;
2. workload and platform choice;
3. model and one relationship decision;
4. one meaningful query and result;
5. one access, performance, or recovery decision with evidence;
6. one tradeoff or limitation; and
7. one next improvement.

Use prepared, redacted evidence. Do not open a secrets page, paste a connection
string, or depend on a live cloud request as the only proof. A short recorded or
static fallback protects the presentation from network failure.

## 5. Build a Portfolio Artifact Around One Concept

A useful repository or folder does not need a complete app. It can teach one
concept clearly:

```text
postgres-lock-diagnosis/
  README.md
  setup.sql
  session_a.sql
  session_b.sql
  diagnose.sql
  evidence/
    redacted-output.txt
```

The README should include:

- problem and learning objective;
- environment and prerequisites;
- safe run order;
- expected output;
- explanation of the evidence;
- cleanup;
- limitation; and
- source/license attribution.

Other strong concepts include RLS allow/deny tests, plan-based index design,
logical restore verification, CSV-to-JSON model comparison, aggregation grain, or
shard-key analysis.

## 6. Remove Portfolio Risk

Before publishing:

- search for passwords, URIs, API keys, tokens, and private hostnames;
- remove real personal or regulated data;
- replace dashboard screenshots with redacted, readable evidence where possible;
- ensure scripts affect only a named disposable schema or collection;
- identify destructive commands prominently;
- test the run order in a clean environment; and
- include licenses and attributions.

Rotating a credential is necessary if it was exposed. Deleting the visible line is
not enough because Git history may retain it.

## 7. Use STAR-R for Behavioral Questions

- **Situation:** concise context and impact.
- **Task:** your responsibility or decision.
- **Action:** what you personally inspected, changed, and verified.
- **Result:** observable outcome.
- **Reflection:** limitation and next production step.

Example:

> In a controlled PostgreSQL lab, one ticket update waited indefinitely behind an
> open transaction. My task was to identify the relationship without terminating
> the wrong session. I queried `pg_stat_activity` and used
> `pg_blocking_pids`, which showed the waiting PID and one blocker whose transaction
> began earlier in my Session A client. I rolled back the controlled blocker,
> observed Session B complete, and queried the row from a fresh statement to prove
> which values remained. The exercise showed the diagnostic method, but in
> production I would also confirm application ownership and business impact before
> cancellation and would review transaction timeout and workflow design.

This answer is credible because it narrows the context and names evidence.

## 8. Explain Technical Choices With Claim-Evidence-Tradeoff

Interview question: "Why did you add that index?"

- **Claim:** I kept a composite index on status and descending opening time for the
  newest-open-ticket queue.
- **Evidence:** On the 100,000-row fixture, the unchanged query moved from a scan
  plus sort to an index-supported path, removed the explicit sort, and examined
  far fewer rows for a 20-row result.
- **Tradeoff:** the index consumes storage and adds work to writes and backup, so I
  would monitor its actual usage and remove it if the workload changes.

Avoid "indexes make queries faster" without a query, plan, or cost.

## 9. Answer Design Questions by Stating Assumptions

Interview question: "Would you use PostgreSQL or MongoDB?"

A strong beginner response:

1. ask about access patterns, relationships, integrity, variation, scale, and
   recovery;
2. state an assumption;
3. choose the simpler suitable model;
4. show one alternative and tradeoff; and
5. name evidence that could change the decision.

Example:

> If authoritative appointments have stable relationships and scheduling
> conflicts, I would begin with PostgreSQL constraints and transactions. If the
> system also stores highly variable, append-heavy form snapshots read as whole
> documents, MongoDB could own that bounded responsibility. I would not add a
> second store until query volume or model friction justified its synchronization
> and recovery cost.

## 10. Be Honest About Scope

Course evidence demonstrates foundational skill, not unsupervised production
ownership. Useful phrases include:

- "I reproduced this in an isolated cloud lab..."
- "The evidence showed..."
- "This check did not prove..."
- "In production I would also inspect..."
- "I have not operated that feature at scale, but I can explain the decision and
  next measurement..."

Honest scope plus concrete reasoning is stronger than inflated certainty.

## 11. Plan the Next Skill From a Job Posting

Choose a role family and examine several current postings. Count recurring skills,
then connect one gap to a small project.

Examples:

- Linux and shell: automate a safe dump verification script.
- Python: write a small, idempotent data import with logging.
- monitoring: create a local dashboard from query and backup-age metrics.
- cloud networking: document TLS, DNS, IPv4/IPv6, and allow-list diagnostics.
- CI: validate SQL/JSON/notebooks on every repository change.

Do not chase every product. Build depth around one evidence-producing workflow.

## Worked Example: Turn a Lab Into a Resume Bullet

Weak:

> Used MongoDB Atlas in class.

Evidence inventory:

- designed embedded and referenced ticket models;
- wrote MQL filters and an aggregation;
- added validation and a compound index;
- compared `COLLSCAN`/`IXSCAN`, documents examined, and returned;
- restored a logical collection export to a separate target; and
- documented Atlas Free limitations.

Possible bullet:

> Modeled and queried a MongoDB Atlas service-desk dataset, implemented focused
> BSON schema validation, and evaluated a compound index with execution-statistics
> evidence; documented a free-tier logical recovery and verification procedure.

Adjust wording to exactly match completed work.

## Common Misconceptions

### "A portfolio needs a full web application"

A small, reproducible operations artifact can demonstrate deeper database skill
than a large app whose data decisions are hidden.

### "The interview wants one correct database"

Many design prompts evaluate assumptions, tradeoffs, failure thinking, and evidence.

### "A certificate proves operational ability"

Training can structure learning. Projects and explanations show how you apply and
verify it.

### "Mentioning every tool sounds more qualified"

A few specific actions with evidence are easier to trust than a long technology
inventory.

## Practice

Choose one course artifact. Write:

1. a 30-second explanation;
2. one resume bullet;
3. one STAR-R interview story;
4. one limitation; and
5. one next production-level measurement or control.

## Retrieval and Transfer

1. Which six questions review a database system end to end?
2. What makes a portfolio run order safe and reproducible?
3. How does STAR-R improve a technical incident story?
4. What belongs in a claim-evidence-tradeoff answer?
5. Why should a presentation have a non-live fallback?
6. How can you describe course work without overstating production experience?

## Further Reading

- O*NET Database Administrators: <https://www.onetonline.org/link/summary/15-1242.00>
- O*NET in-demand DBA technologies: <https://www.onetonline.org/link/demand/15-1242.00>
- U.S. Bureau of Labor Statistics, Database Administrators and Architects:
  <https://www.bls.gov/ooh/computer-and-information-technology/database-administrators.htm>
- NACE Career Readiness Competencies:
  <https://www.naceweb.org/career-readiness/competencies/career-readiness-defined>
- GitHub Skills: <https://skills.github.com/>
- GitHub secret scanning guidance:
  <https://docs.github.com/code-security/secret-scanning/introduction/about-secret-scanning>
