# Week 4 In-Class Reading Response (Open Data Edition)
## Practical Schema Stewardship

## Activity Type
In-class individual response (participation credit)

## Time
20 minutes

## Goal
Show you can translate technical documentation into practical decisions about data quality, trust, and responsible release.

---

## Assigned Reading
1. PostgreSQL `CREATE VIEW`
- [https://www.postgresql.org/docs/current/sql-createview.html](https://www.postgresql.org/docs/current/sql-createview.html)

2. PostgreSQL Identity Columns
- [https://www.postgresql.org/docs/current/ddl-identity-columns.html](https://www.postgresql.org/docs/current/ddl-identity-columns.html)

3. PostgreSQL Constraints
- [https://www.postgresql.org/docs/current/ddl-constraints.html](https://www.postgresql.org/docs/current/ddl-constraints.html)

4. Optional context: Supabase migrations
- [https://supabase.com/docs/guides/deployment/database-migrations](https://supabase.com/docs/guides/deployment/database-migrations)

---

## Submission Format
Create `week4_reading_response.md` and answer all prompts.

For each prompt:
- 100 to 150 words,
- include one citation line with section or heading,
- use your own language (no copy-paste blocks).

Total target: 400 to 600 words.

---

## Prompts

### Prompt 1: Views and Public Understanding
Explain one practical reason to use a view instead of repeating joins in many queries.

Then connect your answer to open data quality:
- how a view can improve consistency,
- how it can reduce misinterpretation by downstream users.

### Prompt 2: Identity Values and Accountability
Explain the difference between identity-generated values and gap-free numbering.

Then answer:
- why gaps are normal,
- why using IDs as "event order truth" can be misleading in analysis.

### Prompt 3: Constraints and Harm Prevention
Choose one constraint type (`CHECK`, `UNIQUE`, or `FOREIGN KEY`) and explain one bad write it prevents.

Then describe one downstream impact:
- what confusion, bias, or reporting error this protection helps avoid.

### Prompt 4: Inclusive Communication in Data Work
Write one short guideline for column naming, definitions, or metadata notes that helps a broad audience interpret data correctly.

Keep it specific and technical (not generic values language).

---

## Scoring (Participation / 10)
- 3 pts: all prompts answered
- 3 pts: citations included and relevant
- 2 pts: explanations are clear and technically correct
- 2 pts: answers connect schema choices to trust and data usability

No credit if most text is copied without interpretation.

---

## Quality Bar
Strong submissions:
- explain tradeoffs, not just definitions,
- name assumptions explicitly,
- separate fact from inference,
- use professional, neutral language that works for mixed audiences.

