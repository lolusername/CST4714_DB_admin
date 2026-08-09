# Week 15: Synthesis, Portfolio Evidence, and Final Presentations - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Synthesis, Portfolio Evidence, and Final Presentations

This final week is about synthesis rather than one more isolated feature. You have modeled facts, recovered SQL, inspected plans, controlled access, diagnosed locks, queried documents, designed indexes, reasoned about reliability, restored data, and traced an incident across systems. Now we will connect those actions into one operating story.

You will also turn one concept into a small GitHub artifact that teaches another beginner. Then you will present your final project safely and translate one real decision into resume and interview language. The goal is not to claim production mastery. The goal is to show credible evidence, reasoning, safety, and awareness of limitations.

## Slide 2: The course built verbs, not a list of product names

Employers can search a resume for PostgreSQL, MongoDB, Supabase, Atlas, GitHub, and Python. Those names become meaningful only when they are connected to actions. You modeled relationships, wrote and verified queries, enforced bad-state boundaries, tested permissions, interpreted plans, diagnosed blocking, and restored data to a separate target.

The communication verb matters equally. You learned to distinguish expected from observed behavior, preserve stable identifiers, state what evidence supports, and name what remains untested. Those habits transfer to database administration, cloud support, backend development, data engineering, security operations, and technical analysis even when a workplace uses different products.

## Slide 3: Review any data system through six connected questions

Start with purpose. Name the user, workload, and decision the system supports. Then state model grain, identity, and relationship representation. Protection asks which invalid states and unauthorized actions the database or application refuses under the intended identity.

Performance begins with important query shapes and measured plans, not a generic claim that an index is fast. Recovery separates continuity from backup and proves restoration in a separate target. Reproducibility asks whether another person can follow the run order, inspect outputs, and understand limitations without receiving credentials. These six questions can structure a project review, interview design prompt, or first incident assessment.

## Slide 4: A tool claim becomes credible when evidence defines its scope

The left side names technologies and broad actions, but an interviewer cannot tell what you actually did. ‘Added security’ might mean anything from creating an administrator password to testing row-level access under two identities. ‘Made a backup’ does not reveal whether the artifact restored.

The right side names mechanisms and observations. A named constraint refused a specific invalid state. The same query moved to a different plan under a candidate index while result correctness stayed constant. A logical artifact was restored to a separate target and verified across structure, data, and behavior. Scope makes the statement more credible, not less impressive.

## Slide 5: A useful GitHub artifact teaches one evidence chain

A portfolio artifact does not need to be a full application. One focused concept can show deeper reasoning. A repository might reproduce PostgreSQL lock diagnosis, an RLS allow-and-deny test, plan-based index design, logical restore verification, a CSV-to-JSON comparison, or MongoDB aggregation grain.

The README states purpose, prerequisites, safe run order, and expected result. The code or detailed guide demonstrates the concept with synthetic or properly licensed data. Evidence explains what one output supports. Cleanup, limitation, and sources prevent the demonstration from becoming unsafe or overstated. Another beginner should be able to learn from it without guessing.

## Slide 6: Publication safety is part of technical quality

Before publishing, search source files and notebook outputs for passwords, connection strings, API keys, tokens, and private hostnames. Notebook output can retain a secret even after the input cell changes. If a credential was exposed, rotate it; deleting the visible line does not remove it from Git history.

Use synthetic or appropriately licensed data and remove personal information. Scripts should target a clearly named disposable schema, database, or collection, with destructive commands labeled before execution. Test the run order from a clean environment or label a static guide accurately. Add source and license attribution, then open the URL outside your normal signed-in view or grant the instructor explicit access.

## Slide 7: Final lab: Teach one database concept in GitHub

Complete this lab individually. Choose one concept from the lab page and keep the scope small. Create a repository or clearly named folder with a README that explains purpose, prerequisites, safe run order, expected result, evidence meaning, cleanup, limitation, and sources. Add one SQL file, MongoDB script, notebook, or detailed Markdown guide with concrete code examples.

Use only synthetic or appropriately licensed data. Do not publish a vendor answer key, copied lesson, credential, or private account screenshot. Run the full safety checklist and verify that the submitted URL can be reviewed. In Brightspace, submit one URL and one sentence naming the concept and evidence. There is no team or partner submission.

## Slide 8: Present the project as a decision story

A final presentation is not a dashboard tour and not a race through every file. It is a concise decision story. Begin with the user and workload. Explain the platform and model choices that serve that workload. Then show a small number of high-value evidence points.

Prepared evidence is safer and more reliable than navigating secret-bearing cloud settings live. You may demonstrate a cloud query, but it should not be the only proof. A redacted output, diagram, script, or short fallback lets the audience evaluate the claim when a network path fails. The project requirements remain only on the canonical final-project page.

## Slide 9: A focused demonstration follows one technical arc

Begin with the problem and the user decision the database supports. State the workload in terms of important reads, writes, relationships, and failure concerns. Show model grain, identity, and one relationship decision rather than every field.

Then demonstrate one meaningful behavior with a prepared expected and observed result. Choose one operations decision involving access, performance, or recovery and show evidence of its mechanism. End with a tradeoff, limitation, and next step. This arc reveals engineering judgment. A long feature inventory makes each claim harder to remember and verify.

## Slide 10: STAR-R turns a lab into an honest incident story

STAR-R gives a behavioral answer a technical structure. The situation is brief context and impact. The task is your responsibility or decision. The action names what you personally inspected, changed, and verified. The result is observable. Reflection states the limit and next production step.

For the lock lab, you can say that one controlled PostgreSQL update waited behind an open transaction. Your task was to identify the blocking relationship without terminating the wrong session. You used `pg_stat_activity` and `pg_blocking_pids`, rolled back the known blocker, observed the waiting update complete, and re-read the row. In production, you would also confirm application ownership and business impact before cancellation and review timeout and transaction design.

## Slide 11: Career language should match the evidence actually produced

When asked about an index, name the unchanged query, the before-and-after plan, the work examined, and the write or storage cost. When asked to choose PostgreSQL or MongoDB, begin with access patterns, relationships, integrity, variation, scale, and recovery rather than declaring one product more modern.

For security, describe the intended identity and both an allowed and expected-denied test. For recovery, distinguish the artifact from the verified restore and state recovery-point and recovery-time limits. In every answer, separate course-lab evidence from production experience. The phrase ‘I reproduced this in an isolated cloud lab’ is accurate and still demonstrates a real method.

## Slide 12: Honest scope is stronger than inflated certainty

Course work demonstrates foundational ability, not unsupervised production ownership. Claims such as production-ready, fully secure, or fault tolerant require a much broader operational record than one semester can produce. Exactly-once language is especially risky when the evidence shows at-least-once delivery plus idempotent handling.

Credible scope names the controlled environment, exact test, observed mechanism, and limit. You can say that you reproduced lock diagnosis, tested least privilege under specified roles, compared execution plans on a known fixture, or restored a logical artifact to a separate target. Then state what production work would come next, such as load measurement, alerting, restore drills, access review, or failure testing.

## Slide 13: Your strongest course outcome is a repeatable way to reason

The course ends with a repeatable method. State the workload and data meaning. Choose the simplest mechanism that fits. Predict behavior, observe the system, and preserve reproducible evidence. Test both success and expected refusal. Connect performance to measured work and reliability to a verified recovery procedure. Name the tradeoff and limitation.

When you present or interview, explain what you personally built or investigated, which evidence supports the result, which failure or bad state you considered, and what you would inspect next in production. That is more valuable than memorizing every command because it lets you learn a new platform without losing the operating discipline you built here.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
