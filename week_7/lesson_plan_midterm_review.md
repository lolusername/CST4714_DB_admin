# Week 7 Lesson Plan — Midterm Review Intensive

**Duration:** 170 minutes (2 hrs 50 min)  
**Format:** Single in-person session with optional breakout pods  
**Resources Needed:** Projector, whiteboard, timer, student laptops with PostgreSQL/Supabase access

---

## 0. Pre-Class Setup (Instructor)
- Load the `midterm_review_slides.pptx` deck and confirm embedded timings.
- Open `week_3/review.sql` in pgAdmin/Supabase for live query demos.
- Print or distribute `student_review_packet.md` and diagnostic slips (Questions 1–6).

---

## 1. Arrival & Diagnostic (15 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 0:00–0:05 | Welcome & Agenda | Highlight midterm date, scope, and deliverables. |
| 0:05–0:15 | Diagnostic Micro-Quiz | Students individually answer 6 mixed questions (architecture, SQL, normalization). Collect results for grouping. |

**Facilitation Tips**
- Keep atmosphere low-stakes; emphasize growth focus.
- Use diagnostic results to assign students to pods (mix strengths/needs).

---

## 2. PostgreSQL Architecture & Cloud Operations Roundtable (25 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 0:15–0:25 | Rapid Fire Recap | Use slides to prompt definitions: shared buffers, WAL, background writer, DBaaS SLAs. |
| 0:25–0:40 | Scenario Sprint | Small groups discuss 3 scenarios (capacity planning, failover, cost optimization). Share takeaways. |

**Facilitation Tips**
- Connect back to `Postgres_architecture.pptx` and Week 3 cloud notes.
- Capture key vocabulary on board for reference later.

---

## 3. SQL Mastery Lab (45 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 0:40–0:50 | Demo | Instructor walks through one window function and one trigger debugging example. |
| 0:50–1:15 | Pod Work | Students tackle prompts 1–4 in `midterm_review_sql_drills.sql` (joins + aggregates + transactions). |
| 1:15–1:25 | Debrief | Volunteers present solutions; surface multiple approaches. |

**Facilitation Tips**
- Encourage use of `EXPLAIN` and transaction controls during practice.
- Pair students who struggled with Week 4 lab with peers confident in PL/pgSQL.

---

## 4. Normalization Studio (35 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 1:25–1:35 | Briefing | Present flawed schema excerpt (appendix of `student_review_packet.md`). |
| 1:35–1:55 | Group Refactor | Teams identify anomalies, propose 3NF/Boyce-Codd redesign, justify key choices. |
| 1:55–2:00 | Lightning Share | Each group posts one design decision and rationale. |

**Facilitation Tips**
- Remind students of Week 5 rubric for schema critique.
- Have `Week5_Database_Design_Normalization.pptx` on standby for quick refresh if needed.

---

## 5. Performance & Troubleshooting Drills (30 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 2:00–2:05 | Transition | Quick stretch/water break. |
| 2:05–2:25 | Drill Stations | Rotating prompts on deadlocks, isolation levels, maintenance plans (use slides + whiteboard). |
| 2:25–2:30 | Synthesis | Chart recurring themes; connect to midterm expectations. |

**Facilitation Tips**
- Use anonymized stories from previous cohorts to ground discussion.
- Emphasize log interpretation and proactive monitoring behaviors.

---

## 6. Midterm Project Huddle (15 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 2:30–2:40 | Deliverable Checklist | Review proposal components (Week 4) and revision notes (Week 5). |
| 2:40–2:45 | Desk Checks | Instructor circulates to unblock individual teams. |
| 2:45–2:50 | Resource Push | Share office hours, LMS discussion threads, and template links. |

**Facilitation Tips**
- Keep groups focused on actionable next steps (schema sketch, environment setup).
- Document common blockers to address asynchronously after class.

---

## 7. Exit Ticket & Wrap-Up (10 min)
| Time | Activity | Notes |
| --- | --- | --- |
| 2:50–2:55 | Exit Ticket | Students submit top-two review priorities + midterm prep commitment. |
| 2:55–3:00 | Closing Remarks | Encourage peer study pods and remind of midterm logistics. |

**Facilitation Tips**
- Collect exit tickets digitally (QR code) or on paper for faster synthesis.
- Follow up via LMS announcement summarizing class-wide focus areas.

---

## Homework / Follow-Up
- Complete remaining prompts in `student_review_packet.md`.
- Finalize midterm project proposals by end of Week 8 day 2.
- Optional: schedule 1:1 coaching slot for schema or performance tuning support.

---

*Last updated: 2025-02-14 — adjust timing if running a shorter 150-minute block (reduce lab and drill segments proportionally).* 
