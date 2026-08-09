# Week 9: Why NoSQL Models Exist and What JSON Enables - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Why NoSQL Models Exist and What JSON Enables

This week does not announce that relational databases are obsolete. It asks why several nonrelational models became useful alongside them. Different workloads place different pressure on representation, distribution, consistency, query shape, and schema evolution.

We will study the history and central ideas of key-value, wide-column, document, graph, and vector systems. Then we will examine JSON as a data-interchange syntax and a flexible document representation. The in-class assignment will not use SQL or MQL. You will take two small CSV tables and write multiple possible JSON designs in a text editor, then explain which read, update, and growth assumptions make each design reasonable.

## Slide 2: Multiple database models exist because workloads disagree

A data model is a set of concepts for representing facts and operations. Relational systems represent facts in relations and derive results through relational operations. A key-value system makes direct lookup by key central. A document system makes nested records and arrays first-class. A graph system makes vertices, edges, and traversals explicit. A vector system indexes points in a high-dimensional space for similarity search.

No model removes tradeoffs. Embedding related data can make one document read easy but duplicate shared facts. Normalizing facts into relations can protect a source of truth but require joins. Graph traversal can express paths naturally but adds another operating model. Choose by the workload and lifecycle, not by which product is newest.

## Slide 3: NoSQL evolved through several overlapping pressures

Relational theory in the 1970s offered a powerful logical model and declarative querying. The word NoSQL appeared in 1998 in Carlo Strozzi's name for a relational system that did not use SQL, which differs from today's broad meaning. In the mid-2000s, systems such as Google Bigtable and Amazon Dynamo published designs for large distributed workloads with particular availability, partitioning, and access-pattern goals.

Around 2009, NoSQL became a community label for several nonrelational database families. The label has never meant one architecture. Modern relational databases support JSON, search, and extensions; document databases add transactions and analytics; cloud services combine models. History is better understood as expanding design choices than as one generation replacing another.

## Slide 4: Relational strengths remain valuable in a multi-model world

Relational databases remain strong when identities, relationships, and constraints must be explicit and many query shapes combine data. Declarative SQL and mature transaction, indexing, recovery, and administration systems make them a durable general-purpose choice.

A specialized model may reduce impedance for a dominant workload. A document can retrieve a bounded aggregate in one read. A graph can traverse variable-length relationships. A vector index can retrieve approximate semantic neighbors. These advantages do not automatically justify another database. The team must also operate security, observability, backup, consistency, and synchronization. The best tool is the one whose benefits exceed its total design and operating costs for the actual workload.

## Slide 5: Key-value stores optimize access through a known key

A key-value model treats a unique key as the primary access path to a value. Session state, cache entries, feature flags, counters, and idempotency records are common examples. The design can scale direct lookup and partition keys effectively because the access pattern is explicit.

The tradeoff appears when a new question does not know the key. ‘Find every session belonging to users in one neighborhood’ may require another index, a maintained secondary structure, or a different system. Atomic operations may be limited to one key or a documented scope depending on the product. Key design, value size, expiration, hot keys, replication, and recovery remain operational concerns.

## Slide 6: Wide-column systems organize sparse rows by access pattern

Wide-column systems descend from ideas popularized by Bigtable and related designs. The exact terminology varies, but a row is addressed by a key and may contain sparse, grouped columns. In Cassandra-style modeling, a partition key determines distribution, while clustering columns order rows within a partition.

The flexibility does not mean no schema. Partition size, query patterns, data duplication, timestamp/version behavior, consistency, and compaction must be designed. A time-series workload might partition by device and time bucket, then cluster by event time. That serves device-time queries efficiently but may require a second denormalized table for a query by alert type. Write-oriented distribution can trade flexible ad hoc querying for predictable designed access.

## Slide 7: Document databases make nested aggregates first-class

A document database stores records with nested objects and arrays, commonly represented with BSON or JSON-like syntax. A ticket document can embed a requester snapshot and a bounded list of recent events, allowing one read to return the aggregate in the shape the application uses.

Embedding has costs. If the requester name is authoritative in many ticket documents, changing it requires several updates and can leave contradictory copies. An unbounded event history can make a document grow without a safe limit. Referencing preserves separate identity and independent lifecycle but requires additional reads, aggregation lookup, or application composition. Document modeling therefore begins with read, update, ownership, cardinality, boundedness, and growth patterns.

## Slide 8: Graph databases make paths and neighborhoods explicit

In graph theory, vertices represent entities and edges represent relationships. Edges may be directed or undirected, labeled, and weighted. A vertex's degree counts incident edges, while a path follows a sequence of adjacent edges. Path length may count hops or sum weights.

Graph databases are useful when variable-length relationship traversal is the central question: fraud rings, identity links, network topology, recommendations, dependency impact, or knowledge graphs. A question such as ‘which alerts connect to this user within three relationship hops?’ maps naturally to graph traversal. The tradeoff includes operating another system, modeling edge meaning, controlling traversal explosion, indexing entry points, and deciding which facts remain authoritative elsewhere.

## Slide 9: Vector databases retrieve nearby representations

A vector is an ordered list of numbers. An embedding model can represent text, images, audio, products, users, or other objects in a space where some semantic relationships correspond to geometric proximity. The database stores the vector together with an identifier and metadata.

Cosine similarity divides the dot product by the product of vector magnitudes. The result measures orientation: vectors pointing in similar directions have similarity near one, orthogonal vectors near zero, and opposite directions near negative one. Many vector systems use cosine distance, inner product, or Euclidean distance with exact or approximate nearest-neighbor indexes. The embedding model, normalization, metric, filter behavior, recall, latency, and update lifecycle must be evaluated together.

## Slide 10: Cosine and Euclidean measures answer different questions

Cosine similarity ignores overall magnitude after normalization and asks whether two vectors point in a similar direction. Euclidean distance measures the ordinary straight-line distance between their endpoints and is sensitive to magnitude as well as direction.

Neither metric is universally better. The embedding model is trained or intended with particular similarity behavior. If vectors are normalized to unit length, squared Euclidean distance is `2 minus 2 times cosine similarity`, so ranking by one is directly related to ranking by the other. Without normalization, the rankings can differ substantially. Evaluate the model's guidance and a labeled retrieval set rather than choosing a metric because its name sounds familiar.

## Slide 11: Choose a model from the dominant workload question

This table begins with the natural question rather than the product. Relational systems support constrained facts and changing declarative queries. Key-value systems excel at known-key access. Wide-column systems serve partition-oriented access at distributed scale. Documents make bounded nested aggregates direct. Graphs and vectors specialize in paths and similarity.

The common cost column is not a condemnation. Every useful strength shifts work somewhere else. A document may duplicate a shared label. A wide-column design may duplicate data across query-specific tables. A graph or vector store adds specialized monitoring and recovery. A polyglot design is justified only when the workload benefit exceeds the synchronization and operating burden.

## Slide 12: JSON is strict syntax with flexible composition

The second day focuses on JSON. JSON grew from JavaScript object-literal syntax into a language-independent interchange format because it is compact, text-based, easy for people to inspect, and easy for many programming languages to parse. Its modern syntax is standardized by ECMA-404 and RFC 8259.

JSON is strict. Property names and strings use double quotes. Values are objects, arrays, strings, numbers, true, false, or null. Standard JSON has no comments and no trailing commas. Its flexibility comes from composing objects and arrays, not from ignoring syntax or abandoning design.

## Slide 13: JSON became popular at the boundary between systems

JSON uses notation familiar from JavaScript, but the data format is language independent. It became attractive for browser and API exchange because the grammar is small, text is inspectable, and many languages can map objects and arrays into native structures. It was often lighter for web developers than XML toolchains, though XML retains strengths such as mixed content, schemas, namespaces, and document standards.

Standardization matters because a permissive parser can accept text that another system rejects. ECMA-404 describes the syntax, while RFC 8259 defines the Internet media type and interoperability guidance. Modern use includes APIs, configuration, event messages, logs, and document databases. Popularity does not make JSON the best format for every task.

## Slide 14: Valid JSON has seven value forms and exact punctuation

The outer braces contain an object: an unordered collection of name-value members. Names are strings in double quotes. Values here include a number, string, Boolean, null, nested object, and array. The array contains two strings and preserves their order.

Standard JSON does not include a native date type, decimal type, binary value, comment, or undefined value. Systems represent those ideas through strings, numbers, conventions, or an extended format. MongoDB BSON adds types such as dates, ObjectIds, decimals, and binary data, while Extended JSON represents BSON values in JSON-compatible text. Do not assume that ordinary JSON round-trips every database type without a conversion decision.

## Slide 15: One CSV relationship can have multiple valid JSON designs

Two CSV files can describe items and inventory events through an item identifier. One JSON design embeds each item's events inside the item object. That makes a whole-item read direct and preserves event order in one array. It is reasonable when the event subset is bounded and normally read with the item.

Another design keeps item objects and event objects separate, with each event storing `item_id`. That preserves independent event growth and one event representation but requires a lookup or application join to assemble history. Both can be valid JSON and valid models. The decision depends on access, update ownership, cardinality, boundedness, and growth, not on formatting preference.

## Slide 16: Atlas and GitHub setup are support, not extra deliverables

The GitHub browser editor can create and commit a `.json` or `.md` file without a local installation. Preview Markdown, but validate JSON with a parser because a code block can look correct while containing invalid syntax.

Atlas setup requires an account project, a database deployment, a separate database user, and network access. Those controls are distinct. Use only a free option and temporary necessary access. Do not commit the connection URI or publish private account information. Setup is not a separate graded deliverable. The required learning evidence is the JSON model and explanation, which remains possible in a text editor during an account or platform problem.

## Slide 17: Lab: Turn two CSV tables into multiple JSON designs

Complete this lab individually and entirely in a text editor. Read the two small CSV files and identify the item key, event reference, relationship cardinality, and any missing values. Decide what one item and one event mean before writing JSON.

Create two different valid representations. One may embed events inside items; another may keep separate item and event arrays or use an identifier-keyed object. Validate each JSON block. Then defend one design for a named access pattern and explain an update or growth tradeoff. There are many correct answers, but every answer must preserve identity and relationship meaning. Submit one text response. No SQL or MQL is required.

## Slide 18: Model choice begins with the question and ends with operating tradeoffs

This week placed NoSQL in history and separated several database families. Key-value systems center known-key access. Wide-column systems center partition-oriented distributed access. Documents center nested aggregates. Graphs center paths. Vector systems center similarity. Relational systems remain powerful for constrained facts and flexible declarative queries.

JSON provides strict, portable syntax for composing objects and arrays. It permits many representations, but flexibility shifts responsibility to design, validation, and documentation. Next week we will move from writing JSON examples to querying MongoDB documents with MQL and choosing embedding or referencing from explicit access and update patterns.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
