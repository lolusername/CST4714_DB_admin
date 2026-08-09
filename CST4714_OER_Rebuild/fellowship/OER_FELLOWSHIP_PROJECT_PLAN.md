# OER Fellowship Project Plan

## Project Title

**Operating Cloud Databases: An Open, Lab-First Course in PostgreSQL, MongoDB,
and Reliable Data Systems**

## Project Summary

This project will replace a fragmented collection of commercial-text references,
vendor tutorials, and locally created files with a coherent, accessible open
course for CST4714 Database Administration. The package will teach beginner
students to build, query, secure, diagnose, recover, and explain small database
systems using free PostgreSQL/Supabase and MongoDB/Atlas environments.

The project is intentionally larger than a textbook substitution. It combines a
15-module open text with individual labs, executable notebooks, student-facing
slide decks, reusable datasets, assessments, projects, accessibility supports,
and an implementation guide. The materials will be useful to City Tech students,
adjunct and full-time instructors, and instructors at other two- and four-year
institutions seeking a practical cloud-database course without student software
costs.

## OER Scope Versus Free External Resources

The fellowship-created OER is the reusable instructional package: the open text,
labs, notebooks, original datasets, assessments, projects, slide decks, scripts,
lesson plans, accessibility supports, and implementation guide. Those materials
are authored or license-compatibly adapted and carry an explicit open license.

The course also curates free external resources, including official PostgreSQL,
Supabase, MongoDB, GitHub, and Python documentation; selected MongoDB University
activities; GitHub Skills; and no-cost cloud interfaces. They help students
practice in current industry environments, but they are not represented as
fellowship-created OER unless a specific source provides a compatible open
license. They are linked, not copied, and each platform-dependent activity has an
open fallback. No student must buy access.

The accompanying OER deliverable and resource register records for every item
whether it is authored, adapted, or curated; its license; its format; its student
use; and whether an account is required. This distinction supports accurate
fellowship reporting and future adoption.

## Need and Rationale

Database administration courses often face three problems. First, commercial
books become expensive and stale while cloud interfaces change. Second, vendor
tutorials teach isolated product actions but rarely form a course-level learning
progression. Third, traditional lecture-heavy coverage leaves too little time for
students to practice diagnosis, recovery, and communication.

This project addresses those problems with openly licensed conceptual chapters,
links to current official documentation, realistic but small technical labs, and
one recurring service-desk case. The recurring case makes the progression visible:
students first rebuild the relational model, core relational algebra, and SQL
through prediction and verification. They then protect meaning in relational
tables, investigate access, concurrency, performance, and recovery, and later
reconsider the same workload as documents and a polyglot system.

The design is aligned with evidence that active learning improves STEM outcomes,
that structured active learning can reduce achievement gaps, and that worked
examples plus retrieval practice support durable learning. Universal Design for
Learning informs multiple representations, cloud and local pathways, predictable
lab structure, and accessible transcripts.

## Primary Course Material

### Interactive Open Textbook and Lab Manual

Fifteen web-first modules will be published in Pressbooks and exported to HTML,
PDF, and EPUB. Each module includes:

- an authentic operating question;
- a concise conceptual reading;
- annotated SQL, MQL, JSON, or Python examples;
- a worked example with self-explanation prompts;
- common misconceptions and diagnostic symptoms;
- an individual practice activity;
- an evidence checklist;
- retrieval and transfer questions;
- accessibility-aware descriptions for essential visuals; and
- official documentation and openly licensed further reading.

The text will be authored and adapted from openly licensed sources where useful,
with source-specific attribution and change notes.

## Supporting Material 1: Interactive Labs, Notebooks, and Data

- At least 24 individual in-class labs with one manageable submission each,
  including a substantial relational-model and SQL review sequence.
- Six educational Jupyter notebooks with Colab links, explanatory Markdown,
  small code cells, runtime credential entry, and offline fallback data.
- Three reusable datasets, including an original synthetic service-desk dataset
  and clearly attributed public-data cases.
- Cloud and local/static pathways so a vendor outage or account barrier does not
  end the learning activity.
- Realistic tasks in SQL, JSON, MongoDB Query Language, logical backup and restore,
  query-plan analysis, access testing, incident diagnosis, and Python integration.

## Supporting Material 2: Assessments and Projects

- An ungraded diagnostic and post-course inventory.
- Retrieval banks and exit checks aligned to each learning outcome.
- Eight short critical and career-connected writing responses using a
  claim-evidence-tradeoff structure.
- One canonical guided PostgreSQL/Supabase midterm operations case.
- One canonical flexible final cloud database project using PostgreSQL, MongoDB,
  or a justified combination.
- Transparent rubrics, student self-checks, and accessible alternate evidence
  paths.

## Supporting Material 3: Slides and Accessible Study Media

- Fifteen student-facing PowerPoint decks with complete word-for-word scripts in
  speaker notes.
- Accessible PDF versions and transcript files.
- Original diagrams and data visuals with meaningful alternative text.
- Consistent typography, contrast, source notes, and layout validation.
- Decks designed to support learning and live demonstration, not to provide
  private directions to the instructor.

## Supporting Material 4: Instructor Implementation Package

- Fifteen public lesson plans that identify outcomes, prerequisite knowledge,
  materials, live-demo paths, likely misconceptions, and fallback options without
  publishing private answer keys.
- A technical setup and troubleshooting guide for free cloud accounts, network
  access, TLS, IPv4/IPv6 connection differences, and credential safety.
- An accessibility and adaptation guide.
- A data-informed teaching protocol that uses aggregate retrieval, lab, and exit
  patterns to trigger reteaching without predictive profiling.
- A production and validation guide for future adopters.

## Student-Centered Teaching Design

Approximately 65-75 percent of class time is reserved for active work. Most class
meetings use a stable sequence: retrieve, inspect a worked example, complete a
partially worked example, build independently, and answer an exit question. Labs
are individual and designed to finish in class. One small artifact replaces long
lists of screenshots and disconnected deliverables.

Worked-example support fades over the term. Early labs provide commands and ask
students to predict and interpret results. Middle labs leave gaps in the procedure.
Late labs present symptoms and constraints, requiring students to choose evidence
and defend a response.

## Data-Informed Improvement Plan

The course will collect an ungraded pre/post concept inventory, aggregate results
from short retrieval checks, lab checkpoint completion, and student feedback on
access and cognitive load. The instructor will use predefined decision rules to
select reteaching examples while retaining professional judgment.

Project evaluation will examine:

- change in concept-inventory performance;
- completion and revision patterns for key labs;
- quality of evidence in a common midterm and final rubric;
- student ability to explain one technical choice in a career genre;
- student-reported material cost and access barriers; and
- instructor notes about pacing, platform failures, and needed revisions.

Only aggregate, de-identified results will appear in public dissemination.

## Accessibility Plan

- Semantic headings, descriptive links, plain-language directions, and readable
  line lengths in web and document formats.
- High-contrast slide design that does not depend on color alone.
- Speaker-note scripts, transcripts, and tagged or accessibility-checked PDFs.
- Alternative text for meaningful images and text equivalents for diagrams.
- Captions or transcripts for original media.
- Keyboard-operable tools and non-drag alternatives where possible.
- Cloud, local, and static-data routes for account, network, and device barriers.
- Explicit expected output and error-recovery guidance in labs.

## Licensing and Permissions

- Original instructional content: CC BY-NC-SA 4.0.
- Original code: MIT License.
- Original synthetic data: CC0 where feasible.
- Adaptations: source-compatible licenses with attribution and change notices.
- Vendor and industry documentation: linked rather than reproduced unless reuse
  permission is explicit.

Materials produced with fellowship support will be shared through the selected
public platform and deposited in CUNY Academic Works in accordance with fellowship
requirements.

## Publication Platform Ranking

1. **Pressbooks:** strongest fit for a modular open textbook, accessible web
   reading, and PDF/EPUB export.
2. **OpenLab:** strongest fit for course community, weekly navigation, and public
   adoption notes.
3. **Manifold:** useful for media-rich annotation if Pressbooks is unavailable.

The source repository remains the version-controlled production home, while the
selected public platform is the student reading interface.

## Work Plan and Milestones

| Period | Work |
|---|---|
| Months 1-2 | finalize outcomes, common case, source and license audit, accessibility template, and pre/post inventory |
| Months 3-5 | author and pilot PostgreSQL modules, labs, notebook set 1, midterm, and decks |
| Months 6-8 | author and pilot MongoDB, reliability, scaling, and polyglot modules, labs, notebook set 2, and decks |
| Months 9-10 | complete final project supports, career materials, implementation guide, and platform migration |
| Months 11-12 | accessibility review, link and code validation, student feedback revision, public release, and repository deposit |

Final fellowship materials will be completed by June 15, 2027.

## Dissemination and Adoption

The project will publish a versioned release with an adoption checklist, editable
source files, environment requirements, estimated class patterns, and change log.
It will be shared through City Tech OER channels and CUNY Academic Works. A short
faculty workshop will demonstrate how to adopt one module, replace a dataset, and
run the automated quality checks without rebuilding the entire course.

## Sustainability

Conceptual explanations and labs are separated from vendor-interface details so
screenshots can be replaced without rewriting the learning objective. A link
checker, notebook execution checks, SQL/JSON validation, slide overflow tests, and
source manifest support an annual maintenance cycle. Each release records tested
platform dates and known free-tier limitations.

## Scope and Stipend Rationale

This is a full-course transformation with a new primary open text and four large
categories of supporting material, not a small resource substitution. It includes
authoring, adaptation, technical development, accessibility work, classroom
piloting, evaluation, multi-format publication, and dissemination. The proposed
scope is therefore aligned with the fellowship's highest funding tier.
