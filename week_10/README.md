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

Bring one point you want clarified on Day 1. On Day 2, use printed pages **116–120** for the [Chapter 10 reading response](reading_response.md), completed during class.

## Class Materials

- **Day 2 starts here:** [Lab 2 handout and interactive MongoDB lab](lab_02_document_model.md). After the lab, open the [Chapter 10 writing prompt](reading_response.md).
- **Day 1 browser orientation:** We use [this introductory MongoDB lab](https://learn.mongodb.com/learn/course/start-here-intro-to-mongodb-2025-12-31/lesson-1-welcome-to-the-introduction-to-mongodb-course/learn?client=educators&page=3) to start working with MongoDB in class.
- **Optional Day 1 Data Explorer practice:** You may use [Lesson 3: Managing Databases, Collections, and Documents in Atlas Data Explorer — Practice](https://learn.mongodb.com/learn/course/mongodb-and-the-document-model-smartbridge/lesson-3-managing-databases-collections-and-documents-in-atlas-data-explorer/practice?client=educators) in class. Sign in or enroll when prompted; this is optional unless announced in class.
- [Complete ticket data reference](ticket_data_reference.md): every field and nested path, value meanings, and all six supplied documents; [download the fixture as MongoDB Extended JSON](ticket_fixture.json).
- [Atlas MQL and modeling notebook](materials/notebooks/04_atlas_mql_modeling.ipynb)
- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lolusername/CST4714_DB_admin/blob/main/week_10/materials/notebooks/04_atlas_mql_modeling.ipynb) for Lab 1; save a working copy in Drive.
- [Week 10 student deck](week_10_mql_document_modeling.pptx)
- [Week 10 PDF handout](week_10_mql_document_modeling.pdf)
- [Week 10 transcript](week_10_mql_document_modeling_transcript.md)


### MongoDB University Sandbox and Our Colab Notebook

Day 1 uses the Colab notebook with the six-ticket fixture. For Day 2, open [CRUD Operations in MongoDB](https://learn.mongodb.com/courses/crud-operations-in-mongodb) and follow your instructor to the lab. The [Lab 2 handout](lab_02_document_model.md) gives the tasks and links to the notebook if the player won’t start.

## Playing the course videos

You can play the embedded videos in desktop PowerPoint or open the MP4 and subtitle files below. The PDF handout and GitHub preview show still images.

The Colab notebook also includes all four still diagrams and three inline video players beside the relevant lesson sections. Click a player's play button; if the player is missing, run its titled video cell first. The supporting display code is hidden. Media loads from the public course repository, so no file upload is needed; viewing it requires internet access. The video cells work independently of the Atlas connection. If inline playback is unavailable, use the player's **Open MP4** link.

See the [static illustrations](illustrations/README.md) and [slide sources](week_10_sources.md).

<!-- videos:start -->
## Videos

Short silent animations with captions (3 for this week). Each has a subtitle file; see [all Week 10 videos](videos/README.md).

- [Querying inside documents: arrays and $elemMatch](videos/01_array_queries.mp4) (1:12): Dot paths reach into nested documents, and two dotted conditions on an array can be met by different elements. $elemMatch requires one element to meet both, and it filters documents without trimming the array.
- [Did the write do what you meant?](videos/02_update_results.mp4) (1:06): An updateOne with an expected-state filter changes status and appends an event in one atomic document write. Reading matchedCount and modifiedCount separates success, no match, and already-current values, and replaceOne is shown dropping omitted fields.
- [Embed or reference? Let the workload decide](videos/03_embed_or_reference.mp4) (1:21): Five access patterns for the ticket page are tested against an embedded events array that keeps growing and a referenced design read in three steps. A contact correction changes one person document, and a new event adds a history document without growing the ticket.

<!-- videos:end -->

## Day 1: Basic MQL in a Safe Collection

Start with the notebook's SQL-to-MongoDB comparison. The
same six tickets, the same question, and the same answer through different
query notation. The instructor then models nested fields, arrays, update
operators, and write-result counts.

Students adapt the worked filter into an active lighting-and-sanitation queue,
rather than choosing an arbitrary code change. A resolved high-priority ticket
makes the difference between category, priority, and current workload visible.

Complete [Lab 1: Query and change documents safely](lab_01_atlas_mql.md).

Submit only the completed `04_atlas_mql_modeling.ipynb` notebook.

## Day 2: MongoDB University lab and Chapter 10 response

1. **Minutes 0–15:** Follow a worked example in the lecture. See how MongoDB adds one account, how to read it back by its ID, and how to add two accounts in one call.
2. **Minutes 15–20:** follow your instructor from the course overview to **Design Effective Queries**, open its lab, and start **Insert a Document**. If you can’t reach a terminal in five minutes, open the course notebook linked in the handout.
3. **Minutes 20–75:** run the commands yourself. Read back a document you inserted, change a filter, and save what you observed.
4. **Minutes 75–95:** write the [Chapter 10 reading response](reading_response.md) on ticket 1003. Use one observation from your lab and one named section from the reading.
5. **Minutes 95–100:** submit the lab record and reading response together in one Brightspace text entry.

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
