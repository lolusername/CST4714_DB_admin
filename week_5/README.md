# Week 5: Database Design and Normalization

## Learning Objectives
- Translate user stories and domain knowledge into conceptual ER models.
- Differentiate entity, relationship, and attribute types and select appropriate key strategies.
- Evaluate schemas against 1NF, 2NF, 3NF, and BCNF to diagnose redundancy and update anomalies.
- Refine logical schemas by applying normalization and justified denormalization.
- Critique sample database designs and document improvement recommendations ahead of the midterm proposal.

## Topics Covered
1. Conceptual modeling refresh (entities, relationships, cardinality, optionality)
2. Key design (primary vs surrogate keys, alternate keys, foreign key strategy)
3. Functional dependencies and anomaly detection
4. Normalization walkthrough: 1NF → 2NF → 3NF and documenting trade-offs
5. Lab practice and discussion on when denormalization is acceptable

## Materials
- `Week5_Database_Design_Normalization.pptx` — slide deck for the single-session lecture with speaker notes
- `instructor_guide.md` — facilitation plan with timings, scripts, and talking points
- `week5_design_demo.sql` — student-facing staging script (denormalized data + anomaly queries)
- `week5_normalization_lab.md` — student-facing walkthrough with dataset setup and normalization prompts

## In-Class Flow (Thursday Only)
1. **Warm-Up & Context (10 min)** — recap Week 4 takeaways, connect to midterm schema deliverables
2. **Interactive Lecture (35 min)** — ER modeling patterns, keys, and normalization theory (slides)
3. **Live Demo (20 min)** — convert a messy requirements doc into 3NF tables and highlight design decisions
4. **Design Studio Lab (45 min)** — small groups diagnose and refactor the provided sample schema using lab script
5. **Schema Review Roundtable (15 min)** — groups present findings; class votes on normalized solutions
6. **Midterm Proposal Alignment (10 min)** — outline next steps for incorporating design feedback

## Activities & Assignments
- **Normalization Lab Submission** (due Monday of Week 6): updated SQL DDL plus narrative explaining normalization choices
- **Midterm Proposal Revision** (due Thursday of Week 6): incorporate ERD + normalized schema, call out remaining assumptions
- **Discussion Board Prompt**: share one denormalization decision you endorse for performance or reporting needs

## Resources
- [Database Design (PostgreSQL Tutorial)](https://www.postgresqltutorial.com/postgresql-administration/postgresql-database-design/)
- [ER Modeling Best Practices](https://www.vertabelo.com/blog/entity-relationship-diagram-best-practices/)
- [Intro to Functional Dependencies](https://cs.uwaterloo.ca/~david/courses/se463/S14/notes/lect14.pdf)
- [Normalization Overview (1NF–BCNF)](https://www.guru99.com/database-normalization.html)
- [Documenting Database Designs](https://cwe.mitre.org/data/published/sr/index.html)

---

*Prepared for CST4714 Database Administration — Week 5 (Database Design & Normalization, single-session format).* 
