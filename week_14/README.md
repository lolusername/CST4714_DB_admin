# Week 14 – Final Project Peer Review, Presentations, and Troubleshooting

Week 14 extends the Week 13 build sprint. Teams either **work on implementation** or **shift to presentation polish** if their build is done. The session centers on peer review (one group presents to another), live Q&A, and targeted troubleshooting with the instructor.



## In-Class Flow (150 minutes)
1. **Kickoff (10 min):** Timeline review for Week 15 presentations + Q&A on deliverables.
2. **Consultation Queue (10 min):** Teams post blockers; instructor schedules 10–15 minute desk checks.
3. **Peer Review Round 1 (30 min):** Pair teams. Team A presents to Team B (5–7 min), then B gives feedback (8–10 min) on clarity, risks, and demo readiness. Swap roles.
4. **Troubleshooting Clinic (30 min):** Instructor floats; teams work through blockers surfaced earlier (auth, backups, HA tests, monitoring alerts, migration bugs).
5. **Working Sprint (30–40 min):** Build, fix, or rehearse. Prioritize admin evidence (backup/restore proof, security roles/auditing, replication/HA test, monitoring alerts).
6. **Peer Review Round 2 (30 min):** Rotate pairings if possible. Focus on **presentation polish** if the build is stable; otherwise, validate fixes from Round 1.
7. **Whole-Class Share-Out (10 min):** Each team states: (a) riskiest open item, (b) what will be demoed, (c) what is left for Week 15.
8. **Close (10 min):** Confirm after-class tasks, report/presentation deadlines, and any extra office hours for technical issues.

### Peer Review Structure (per round)
- **Presenter covers:** scenario, target users, stack choice, schema/collections highlights, admin controls (backup/restore, security, HA/replication, monitoring/alerts), demo script.
- **Reviewers deliver:** 3 strengths, 3 risks/gaps, 1 question to pressure-test reliability/security, and 1 suggestion for the live demo flow.
- **Artifacts captured:** reviewer notes + action items posted to the team repo or shared doc before swapping.

## Deliverables for Week 15 (work toward these today)
- **Final project repo/package** with:
  - Schema/collection definitions, migrations, and seed data
  - Automation scripts for backup/restore; evidence of one successful drill
  - Security roles/policies + auditing/logging configuration
  - Replication/HA setup + a captured failover or resilience test
  - Monitoring/alerting hooks (dashboard or logs) with screenshots
- **Presentation deck** ready for the live demo (10–12 minutes)
- **Written report (draft today, finalize after class)** summarizing design decisions, admin controls, and testing evidence

## After Class Tasks
1. Incorporate peer review feedback into code, scripts, and slides; push updates to your repo.
2. Run one full **demo rehearsal** (10–12 minutes) and time it. Record outstanding risks and mitigation.
3. Finish the **draft report** and circulate for team review; lock final versions before Week 15.
4. If you hit blockers, email the instructor with a concise status + artifacts (error logs, screenshots, connection details) for targeted help.

## Quick Checklist
- [ ] Peer review feedback recorded and assigned
- [ ] Backup/restore evidence captured
- [ ] Security roles/auditing configured and tested
- [ ] Replication/HA or failover test documented
- [ ] Monitoring/alerts demonstrated
- [ ] Slides and demo script rehearsed (≤12 minutes)
