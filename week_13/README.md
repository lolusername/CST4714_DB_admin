# Week 13 – Final Project Build Sprint & Consultations

Week 13 is dedicated to team work time on the **Final Group Project**. Use this session to lock in teams, pressure-test your architecture, and produce tangible artifacts toward the Week 15 delivery. The full brief lives at `final_group_project_outline.pdf` in the course root—review it closely before you start. Everything you need to work independently is captured below, so you can complete this week even if you were not in class. **Form a team of 3–4, email the instructor your roster, and pick your project topic by next Tuesday.**

## Student Materials
- Final project brief: [`final_group_project_outline.pdf`](../final_group_project_outline.pdf) — scope, deliverables, evaluation criteria, and sample scenario ideas.
- Your team workspace (Git repo/shared drive) with meeting notes, diagrams, and scripts.
- Any lab environments (Atlas clusters, Postgres instances, Supabase projects) you plan to demo.

## Before Class
1. **Finalize teams (3–4 students)** and share the roster + communication channel with the instructor.
2. Re-read the brief (PDF above) and highlight the required deliverables: design doc, implementation package, admin demonstration, written report, presentation.
3. Come with a **short case description** (problem statement + chosen stack) so you can quickly validate feasibility in consultations.
4. Collect your top 3 risks or open questions (e.g., HA strategy, security controls, migration approach) to discuss.
5. Bring laptops with access to your cloud accounts and any baseline schemas or seed data.
6. If you missed class, follow the steps below and email your team roster (3–4 names) plus your selected topic to the instructor by next Tuesday.

## In-Class Flow (Build & Consult)
1. **Kickoff (10 min):** Instructor restates final project requirements and the Week 12–15 timeline. Teams hand in finalized rosters.
2. **Team Planning Huddle (20 min):** Define owner per stream: data model, admin/ops, security, testing/demo.
3. **Working Sprint + Rotating Consultations (110–120 min):** Build toward the Week 13 milestone (detailed design & tooling):
   - Draft **data dictionary and ER/aggregation diagrams** for your core entities/collections.
   - Map admin plan: backup/restore automation, security roles & auditing, replication/HA setup, monitoring hooks.
   - Start stubbing **implementation scripts** (schema creation, seed data, migrations) and a short **demo workflow**.
   - Meet with the instructor for at least one 10–15 minute checkpoint; arrive with specific questions and blockers.
4. **Checkpoint Share-Out (15 min):** Each team states stack, admin strategy, and the riskiest assumption left.
5. **Close (5 min):** Confirm after-class tasks and schedule any extra office hours.

## Deliverables for This Week (due before Week 14)
- Finalized **team roster** + communication channel.
- **Data dictionary** and ER diagram (or MongoDB aggregation diagram) for chosen case study.
- **Admin plan draft** describing backup/restore, security (roles, auditing, RLS), replication/HA, and monitoring.
- Initial **implementation artifacts** (DDL/collection creation scripts, seed data, migration plan) committed to your repo.
- **Consultation note**: 3–5 bullet summary of decisions/feedback from the instructor meeting.
- Submit the above to your team repo or LMS before Week 14.
- **Email the instructor** with your team roster (3–4 students) and chosen topic by Tuesday.

## After Class Tasks
1. Finish any in-progress diagrams and push scripts to your repo with setup instructions.
2. Run at least one **backup/restore drill** or **failover test** and capture evidence (logs/screenshots).
3. Prep a mini-demo (2–3 minutes) you can run in Week 14 to show progress on data model + admin setup.
4. Track open risks and dependencies; book additional office hours if needed.

## Simple Reflection: Database vs Spreadsheet (≈20–25 min)
- Find 1–2 reputable sources (blog post, short video, or doc page) that compare databases to spreadsheets.
- In ~150–200 words, explain:
  - Two key differences that matter for reliability or collaboration (e.g., concurrency control, schemas, scaling).
  - One example where a spreadsheet is enough and one where a database is required.
- Submit your write-up to the LMS or team repo. Keep it concise and practical.

## Quick Reminders from the Brief
- Projects must justify technology choice (PostgreSQL, MongoDB, or hybrid) with access patterns and admin needs.
- Required evidence: backup/restore automation, security hardening, replication/HA test, and monitoring/alerting hooks.
- Submission bundle for Week 15: design doc, scripts, admin proof, slides, and written report in one package.
