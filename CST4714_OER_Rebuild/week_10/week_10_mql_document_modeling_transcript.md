# Week 10: Basic MQL and Document Modeling - Spoken Transcript

This transcript matches the complete word-for-word scripts stored in the PowerPoint speaker notes.

## Slide 1: Basic MQL and Document Modeling

This week begins practical MongoDB work at a beginner level. The first class uses a disposable collection or the offline notebook to run filters, projections, sorting, updates, and a controlled delete. We will compare MQL with familiar SQL ideas without pretending the languages have identical semantics.

The second class focuses on data modeling. Embedding and referencing are not stylistic choices. They affect read locality, update ownership, document growth, duplication, and consistency. The instructor live activity and the individual MongoDB University activity are intentionally different, and the course-authored model decision remains the central evidence.

## Slide 2: SQL concepts provide a bridge, not a one-to-one translation

Familiar SQL concepts can reduce initial cognitive load. A MongoDB collection is the query source, a filter document selects matching documents, a projection document controls returned fields, and cursor methods can sort and limit results.

The bridge has limits. MongoDB fields can be missing, nested, arrays, or BSON types not present in ordinary JSON. Projection has inclusion and exclusion rules, with `_id` handled specially. A filter document is not a SQL string, and dot notation refers to nested paths. Use the comparison to recover the question structure, then learn MQL's actual document and array semantics.

## Slide 3: Connect to Atlas without weakening the credential boundary

An Atlas connection needs an active deployment, a database user, network access, DNS, TLS, and a current driver. The course notebook uses `getpass` so the connection URI is not stored in a code cell or ordinary output. The first operation is an administrative ping, which separates connection evidence from later collection mistakes.

A TLS handshake error is not a reason to disable certificate verification. Check the current URI, PyMongo version, system time, DNS and SRV resolution, network inspection, and Atlas access list. If the environment remains blocked, use the notebook's `mongomock` path. That path demonstrates document operations while clearly not claiming Atlas server behavior.

## Slide 4: A filter selects documents; a projection selects returned fields

The filter requires an active status and high priority. `$in` compares the status field with the listed values. The projection includes ticket identifier, status, and subject while explicitly excluding MongoDB's `_id` field. The cursor sorts by ticket identifier before iteration.

State result grain as one output item per matching ticket document. Before running, inspect the six-document fixture and predict identifiers. If no documents match, check database and collection names, field spelling, type, and actual values before inserting more data. A numeric identifier does not match a string containing the same digits. Verification uses stable identifiers and a count, not only the printed document shape.

## Slide 5: Nested paths and arrays require document-aware predicates

Dot notation addresses a nested path: the neighborhood field inside the requester object. The `events` field is an array of event objects. `$elemMatch` requires one array element to satisfy both the event type and destination status conditions.

Without `$elemMatch`, separate predicates on `events.type` and `events.to` can be satisfied by different array elements, producing a document that has a status-changed event somewhere and a resolved destination somewhere else. The intended question is about one event with both properties. Array semantics are a central reason to inspect the document shape rather than translating SQL clauses mechanically.

## Slide 6: Write results separate finding a target from changing its value

MongoDB update results distinguish matching from modification. If the filter identifies ticket 1002, `matched_count` can be one. If the priority is already the requested value, `modified_count` can be zero even though the target was found. That is not automatically a failure.

A matched count of zero can indicate the wrong database, collection, identifier type, field path, or current state. A modified count larger than expected indicates a scope problem. Always verify with a follow-up read of the stable identifier and changed field. For a course fixture, record the before value, update result, after value, and cleanup or reset behavior.

## Slide 7: A safe delete uses a narrow filter and verified result

A delete is not made safe by being short. Begin with the exact filter and preview matching stable identifiers. In a teaching collection, select one disposable identifier and use `delete_one`. Inspect `deleted_count`, then query the identifier again to verify absence.

MongoDB does not provide a general multi-document transaction around every casual Data Explorer action, and a successful delete can replicate. Use a disposable course database and a known reset path. Never demonstrate an empty filter such as `{}` on a shared collection. The same scope-and-verification habits from SQL DML carry into MQL even though the command syntax differs.

## Slide 8: Lab 1: Basic MQL with observable write evidence

Complete this lab individually in Notebook 4. Choose the Atlas path or the default `mongomock` path. Run from the first cell so the fixture and database names are known. Modify the assigned filter rather than only pressing Run.

Record stable identifiers for scalar, nested, and array queries. Update one known ticket and interpret matched and modified counts before verifying the field. Complete the safe disposable delete and reset. If using Atlas, record that temporary network access was narrowed or removed without publishing the address or project details. Submit one completed notebook evidence record with no connection URI in source or output.

## Slide 9: Model around access, update ownership, and growth

On the second day, the question shifts from how to query a document to why the document has that shape. A document boundary can support atomic updates and read locality for a bounded aggregate. It can also create duplication, large documents, and update fan-out when shared facts are embedded widely.

We will begin with access patterns: which facts are normally read together, which facts change together, who owns each fact, how many related items can exist, and how quickly the collection grows. Embedding and referencing are consequences of those answers, not universal rules.

## Slide 10: Embedding and referencing move work to different operations

Embedding is strong when child data belongs to one parent, is normally read with that parent, and remains bounded. A shipping address snapshot inside an order can preserve what was used at purchase time. A small set of ticket tags can be naturally embedded.

Referencing is strong when the related entity has independent identity, is shared by many parents, grows without a safe bound, or changes on its own schedule. An agent profile referenced by many tickets avoids updating every ticket when the current profile changes. Hybrid designs are common: embed a deliberate snapshot for read context and reference the authoritative identity. The model must document which copy owns which meaning.

## Slide 11: Unbounded arrays turn convenience into growth risk

An array of events can make a ticket easy to display, but event history may grow for years. MongoDB documents have a size limit, and large frequently changing arrays increase rewrite, indexing, and concurrency costs. The problem may appear long before the hard limit if the application reads the whole document unnecessarily.

Estimate cardinality and arrival rate. Define retention and archival behavior. Ask whether old events are queried independently, whether one event must be updated separately, and whether many writers append concurrently. A bounded recent-events array plus a referenced event collection can be a justified hybrid. The word flexible does not remove capacity planning.

## Slide 12: A model decision follows five workload questions

Begin with the dominant read: fields, relationships, sort, and acceptable freshness. Then document writes: which facts change together, which change independently, and whether several writers contend on the same aggregate. Name ownership so duplicated snapshots are not confused with authoritative current data.

Estimate bounds and growth over the retention horizon. Finally, name a query and update that can verify the proposed shape serves the workload. A model diagram without access and update evidence is only a picture. The same five questions can justify embedding, referencing, or a hybrid, and they reveal when a relational model remains the simpler choice.

## Slide 13: Live demonstration and individual practice stay distinct

The instructor live-codes the Modeling Data Relationships activity to make the reasoning visible. Students are not assigned that same activity as their individual lab. The individual MongoDB University activity is Relational SQL to Document Model, which provides distinct practice translating a small relational design.

The course-authored model decision remains essential because vendor completion alone does not show why a shape fits the Metro Support workload. If MongoDB University is unavailable, the module and notebook fixture provide an open fallback with the same access, update, ownership, and growth questions. No student must pay for either path.

## Slide 14: Lab 2: Defend one document boundary

Complete the student modeling activity individually. The activity is different from the instructor's live example. Then apply the course model-decision questions to the assigned Metro Support relationship.

Provide one document shape in JSON or a labeled outline. State the read it makes easier, the update it makes harder, where the authoritative fact lives, and whether the related data remains bounded. Include activity completion evidence if the external path worked, but do not submit a private account screenshot. The open fallback can earn the same credit. Submit one model decision, not a team artifact.

## Slide 15: MQL operates the document; access patterns justify its shape

This week established basic MQL and document modeling. Filters, projections, nested paths, arrays, updates, and deletes must be predicted and verified with stable identifiers. Write results separate matching from actual modification. Connection safety keeps credentials and TLS verification intact.

Modeling then asks which facts are read together, changed together, owned together, and bounded together. Embedding improves locality and one-document operations for suitable aggregates. Referencing protects independent identity and growth. Next week we will process documents through aggregation pipelines, enforce document rules with validation, and evaluate indexes for a filter-and-sort workload.

## License

Original transcript text is licensed CC BY-NC-SA 4.0. See the course attribution file for sources and adaptations.
