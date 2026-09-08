# Appendix A: Notation and Technical Language {.unnumbered}

This appendix is a reading reference, not a replacement for the chapters. It
collects mathematical symbols, query-language conventions, and operational terms
that recur across the book.

## Relational Notation {.unnumbered}

Assume $T$ is a tickets relation and $U$ is a users relation.

| Operation | Conventional notation | Plain-language job | Common SQL form |
|---|---|---|---|
| selection | $\sigma_{\varphi}(T)$ | keep tuples for which predicate $\varphi$ is true | `WHERE` |
| projection | $\pi_{a_1,\ldots,a_k}(T)$ | keep selected attributes | `SELECT` list |
| rename | $\rho_S(T)$ | give a relation or attribute a usable name | `AS` |
| Cartesian product | $T \times U$ | pair every tuple in one input with every tuple in the other | `CROSS JOIN` |
| theta join | $T \bowtie_{\theta} U$ | keep paired tuples satisfying condition $\theta$ | `JOIN ... ON` |
| union | $T \cup U$ | tuples in either union-compatible relation | `UNION` |
| intersection | $T \cap U$ | tuples in both union-compatible relations | `INTERSECT` |
| difference | $T - U$ | tuples in the first compatible relation but not the second | `EXCEPT` |

The identity

$$
T \bowtie_{\theta} U = \sigma_{\theta}(T \times U)
$$

explains why an omitted join predicate can multiply rows. SQL is based on
relational ideas but is not identical to classical relational algebra: SQL tables
can contain duplicate rows, `NULL` introduces three-valued logic, ordering is
explicit, and computed expressions and aggregation extend the basic operators.

## Logic and Set Symbols {.unnumbered}

| Symbol | Read as | Example |
|---|---|---|
| $\land$ | and | $p \land q$ is true only when both predicates are true |
| $\lor$ | or | $p \lor q$ is true when either predicate is true |
| $\lnot$ | not | $\lnot p$ negates predicate $p$ |
| $\in$ | is an element of | $v \in V$ means vertex $v$ belongs to set $V$ |
| $\subseteq$ | is a subset of | $A \subseteq B$ allows $A=B$ |
| $|T|$ | cardinality of $T$ | number of tuples in relation $T$ |
| $\sum$ | sum | $\sum_{i=1}^{n}x_i$ adds indexed values |
| $\sqrt{x}$ | square root | used in Euclidean norm and distance |
| $\approx$ | approximately equal | measured or rounded comparison |

In SQL, a `WHERE` clause keeps rows only when its predicate is
`TRUE`. Both `FALSE` and `UNKNOWN` are filtered out.
That is why `column = NULL` does not find missing values; use `IS NULL`.

## Graph and Vector Notation {.unnumbered}

A graph $G=(V,E)$ contains vertices $V$ and edges $E$. A path is a sequence of
connected vertices and edges. In an undirected graph, the degree $\deg(v)$ counts
edges incident to vertex $v$, with a self-loop counted twice. A directed graph
distinguishes incoming degree from outgoing degree.

A vector $\mathbf{x}\in\mathbb{R}^{n}$ is an ordered list of $n$ real numbers.
The dot product is $\mathbf{a}\cdot\mathbf{b}$, the Euclidean norm is
$\lVert\mathbf{a}\rVert_2$, and cosine similarity is

$$
s_{\cos}(\mathbf{a},\mathbf{b}) =
\frac{\mathbf{a}\cdot\mathbf{b}}
{\lVert\mathbf{a}\rVert_2\lVert\mathbf{b}\rVert_2}.
$$

Cosine similarity is undefined for a zero vector because its denominator is zero.
It measures direction, not semantic truth. The embedding model, data, metric, and
evaluation procedure determine whether vector neighbors are useful.

## Code-Language Conventions {.unnumbered}

Every code block in the second edition declares a language. The publication build
adds a numbered listing label automatically.

| Label | What the listing represents |
|---|---|
| SQL | PostgreSQL-compatible SQL unless a note identifies another dialect |
| MongoDB shell / JavaScript | MQL or JavaScript-style values as entered in `mongosh` or Data Explorer |
| JSON | strict JSON: quoted keys/strings, no comments, and no trailing commas |
| Python | Python 3 code, normally a notebook or small client example |
| Shell | a command entered in a POSIX-like terminal; placeholders and environment variables must be replaced safely |
| Text | directory structure, pseudodata, or output that is not executable code |

`mongosh` object notation is not strict JSON. Values such as `ObjectId(...)`,
`ISODate(...)`, regular expressions, and unquoted field names belong to shell or
BSON representations. Extended JSON provides JSON-compatible encodings for BSON
types when data crosses text-only boundaries.

## Operational Glossary {.unnumbered}

**Access pattern.** A recurring read or write shape, including predicates,
returned fields, sort order, frequency, latency expectation, and consistency need.

**Atomicity.** The guarantee that a transaction's changes commit together or do
not remain. MongoDB also guarantees atomicity for a single-document write.

**Backup.** A retained artifact or managed history intended for recovery. A
backup is useful only with a compatible restore path and verification.

**BSON.** MongoDB's binary document representation, which supports more types
than strict JSON.

**Cardinality.** Depending on context, the number of rows in a relation, distinct
values in a column, or possible values of a key.

**Constraint.** A database-enforced rule such as `NOT NULL`, `UNIQUE`, `CHECK`,
primary key, or foreign key.

**Durability.** A DBMS promise about committed data surviving failures within a
documented model. It is not indefinite retention.

**Evidence.** An observable artifact that supports or contradicts a technical
claim: query text, result, plan, count, checksum, denied action, log, restore test,
or recorded limitation.

**Idempotent operation.** An operation designed so that repeating it produces the
same intended state rather than accidental duplicates or compounded changes.

**Index.** An access structure that trades storage and write maintenance for
faster support of selected predicates, joins, or ordering.

**Isolation.** Rules governing what concurrent transactions can observe and when
they must wait, retry, or abort.

**Least privilege.** Giving an actor only the actions and resources required for
its current job.

**Managed service.** A service in which the provider operates selected
infrastructure and software layers while the customer retains data, access,
configuration, workload, recovery, and application responsibilities defined by
the plan and contract.

**MVCC.** Multi-version concurrency control, which lets transactions read
appropriate row versions while concurrent changes proceed under an isolation
model.

**Projection.** In relational algebra, choosing attributes; in MongoDB queries,
choosing document fields. The similar word does not make the complete semantics
identical.

**Read concern.** MongoDB setting that controls visibility guarantees for a read.

**Read preference.** MongoDB setting that chooses which replica-set members are
eligible to serve a read.

**Recovery point objective (RPO).** Maximum tolerable data-loss interval. If the
last recoverable state is at $t_r$ and failure occurs at $t_f$, realized loss is
$t_f-t_r$.

**Recovery time objective (RTO).** Maximum tolerable service-recovery duration. If
failure occurs at $t_f$ and acceptable service returns at $t_a$, realized recovery
time is $t_a-t_f$.

**Replication.** Copying an active change history to other members for
availability and read/write behavior. Replication is not a historical backup.

**Row-level security (RLS).** A PostgreSQL mechanism that applies row predicates
according to role and policy context.

**Schema.** The structural and semantic rules for stored data. A flexible document
system still has a schema, whether the server, application, convention, or data
quality process enforces it.

**Selectivity.** The fraction of input rows expected to match a predicate,
$s=\text{matching rows}/\text{input rows}$.

**Shard key.** Fields used to distribute and route a sharded collection. Quality
depends on distribution, targeting, growth, and workload rather than cardinality
alone.

**Source of truth.** The authoritative owner of a fact when multiple stores hold
copies or projections.

**Write concern.** MongoDB setting that defines the acknowledgment required from
replica-set members for a write.
