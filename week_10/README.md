# Week 10: MQL and Document Modeling

## The Week's Question

How do we query MongoDB documents safely and decide which related facts belong
together?

## What You Will Be Able to Do

- connect to Atlas through a credential-safe notebook or use the offline fallback;
- insert, find, project, sort, update, and delete test documents;
- query nested fields and arrays;
- interpret matched, modified, and deleted counts;
- choose embedding or referencing from access patterns and growth; and
- document one model's benefit and cost.

## Before Class: Assigned Reading

Use [Chapter 10: MongoDB Models the Way an Application Reads](../Operating_Cloud_Databases.pdf).

- **Before Day 1:** read the connection, BSON, CRUD, and nested/array-query sections. Pay attention to whether a listing is shell JavaScript or notebook Python.
- **Before Day 2:** read from **Single-Document Atomicity Shapes Modeling** through **More Than One Model Can Be Valid**. Use the workload to explain embedding and referencing.

Bring one point you want clarified. Reading supports the in-class work; it does
not add a separate reading report. Optional textbook practice is not required
unless the weekly lab assigns it.

## Class Materials

- **MongoDB starting lab:** We will use [this introductory MongoDB lab](https://learn.mongodb.com/learn/course/start-here-intro-to-mongodb-2025-12-31/lesson-1-welcome-to-the-introduction-to-mongodb-course/learn?client=educators&page=3) to start working with MongoDB in class.
- **Possible additional MongoDB lab:** We may also use [Lesson 3: Managing Databases, Collections, and Documents in Atlas Data Explorer — Practice](https://learn.mongodb.com/learn/course/mongodb-and-the-document-model-smartbridge/lesson-3-managing-databases-collections-and-documents-in-atlas-data-explorer/practice?client=educators) in class. Sign in or enroll when prompted; this is optional unless announced in class.
- [Complete ticket data reference](ticket_data_reference.md): every field and nested path, value meanings, and all six supplied documents; [download the fixture as MongoDB Extended JSON](ticket_fixture.json).
- [Atlas MQL and modeling notebook](materials/notebooks/04_atlas_mql_modeling.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/04_atlas_mql_modeling.ipynb) for Lab 1; save a working copy in Drive.
- [Week 10 student deck](week_10_mql_document_modeling.pptx)
- [Week 10 PDF handout](week_10_mql_document_modeling.pdf)
- [Week 10 transcript](week_10_mql_document_modeling_transcript.md)


### MongoDB University Sandbox and Our Colab Notebook

Both let you practice in a browser and inspect the results of your actions.
MongoDB University supplies guided exercises: its introductory lab opens an
in-browser development environment connected to Atlas, with no local software
installation. Think of that lab as a **sandbox for trying the lesson's tasks**.
Follow the launched exercise's instructions for its tools, data, and connection;
it is separate from our Colab runtime and ticket dataset.

The optional Data Explorer practice focuses on Atlas's graphical view of
databases, collections, and documents. Colab instead gives us an editable Python
notebook with Markdown explanations, query cells, and saved output. Our Colab
notebook can connect to your own Atlas cluster, or use `mongomock` in memory;
`mongomock` is a teaching substitute, not an Atlas cluster. Completing a
University lab does not configure Colab's database user, URI, or IP access rule.

Use the starting lab to learn the browser environment. We may then use the
Data Explorer practice to connect what we see in the interface with the
collections and documents we query in Colab. These activities do not add a
separate submission or course-badge requirement.

## Teaching and playback

The PowerPoint has word for word speaker notes. Slides 1–20 cover Day 1 and slides 21–31 cover Day 2. Slides 7–9 introduce the complete ticket data model before the query examples. Three optional static Manim diagrams are on slides 33–35, with links from the related examples. Slide 36 compares the MongoDB University sandbox with Colab and links to both browser activities; slide 4 links to it.

Download the `.pptx` and open it in desktop PowerPoint. In Slide Show, click a thumbnail on slide 32 to play its embedded video full screen. The videos work without an internet connection. GitHub previews and the PDF handout show still images. The individual MP4 and subtitle files remain available below.

See the [static illustrations](illustrations/README.md) and [slide sources](week_10_sources.md).

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 10 videos](videos/README.md).

- [Querying inside documents: arrays and $elemMatch](videos/01_array_queries.mp4) (1:12): Dot paths reach into nested documents, and two dotted conditions on an array can be met by different elements. $elemMatch requires one element to meet both, and it filters documents without trimming the array.
- [Did the write do what you meant?](videos/02_update_results.mp4) (1:06): An updateOne with an expected-state filter changes status and appends an event in one atomic document write. Reading matchedCount and modifiedCount separates success, no match, and already-current values, and replaceOne is shown dropping omitted fields.
- [Embed or reference? Let the workload decide](videos/03_embed_or_reference.mp4) (1:21): Five access patterns for the ticket page are tested against an embedded events array that keeps growing and a referenced design read in three steps. A contact correction changes one person document, and a new event adds a history document without growing the ticket.

<!-- videos:end -->

## Free External Resources With Distinct Roles

- **Instructor live demonstration:** [Modeling Data Relationships: Lesson 3, Modeling One-to-One](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-3-modeling-one-to-one/learn). The instructor works the one-to-one example and its Practice activity, not Lesson 4.
- **Student individual activity:** [Modeling Data Relationships: Lesson 4, Modeling One-to-Many](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/learn), followed by [Lesson 4: Practice](https://learn.mongodb.com/learn/course/modeling-data-relationships/lesson-4-modeling-one-to-many/practice?page=1).
- **Optional workload support:** [Identifying Reads and Writes](https://learn.mongodb.com/learn/course/relational-to-document-model/relational-to-document-model/model-for-workloads?page=3), a video within Relational (SQL) to Document Model. It is not an interactive lab or an extra submission.

These are different lessons and practice activities within one free course.
Students do not repeat the instructor's one-to-one activity. Some MongoDB
University courses reuse videos under different course names, so this week's
boundary is the specific lesson, not a claim that different titles mean new work.

## Day 1: Basic MQL in a Safe Collection

Use **slides 1-20**. Start with the notebook's SQL-to-MongoDB comparison: the
same six tickets, the same question, and the same answer through different
query notation. The instructor then models nested fields, arrays, update
operators, and write-result counts.

Students adapt the worked filter into an active lighting-and-sanitation queue,
rather than choosing an arbitrary code change. A resolved high-priority ticket
makes the difference between category, priority, and current workload visible.

Complete [Lab 1: Query and change documents safely](lab_01_atlas_mql.md).

Submit only the completed `04_atlas_mql_modeling.ipynb` notebook.

## Day 2: Model From Access Patterns

Use **slides 21-31**. The instructor demonstrates **Lesson 3: Modeling One-to-One** and a ticket-page
read. Students complete **Lesson 4: Modeling One-to-Many**, including its
interactive **Practice**, then revise their Week 9 ticket design for a new
requirement: the page needs only the latest two events, but the system must retain
all history and update contact information in one place. No complete course badge
or validation unit is required this week.

Complete [Lab 2: Translate one workload into a document model](lab_02_document_model.md).

Submit the JSON, explanation, and Lesson 4 Practice progress image in one Brightspace
text response. The lab describes the fallback if the external platform is down.

For support with the lab's explanation, use [Writing About Database Decisions](materials/assessments/critical_writing.md). It develops the response already included in your lab, not an additional assignment.

## Optional Industry Extension: Live-Service Game Inventory Model

This activity is optional, ungraded, and does not add a submission.

Design documents for a game that must load a player's equipped items in one read,
grant one item atomically, preserve an unbounded acquisition history, and maintain
one shared catalog description per item type. Sketch an embedded, referenced, or
hybrid design and mark every bounded and potentially unbounded array. Explain one
atomicity benefit, one duplication risk, and one query that would force you to
reconsider the boundary.

## End-of-Week Self-Check

Given one-to-many related data, explain when ownership, atomic update, shared
identity, independent queries, and unbounded growth point toward embedding or
referencing.

## Reuse

See the [licenses](materials/LICENSE.md) and [source attributions](materials/ATTRIBUTIONS.md). External resources retain their own terms.
