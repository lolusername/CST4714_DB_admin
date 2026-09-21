# Week 13: Capacity, Sharding, and Python Integration - Spoken Transcript

## Slide 1

This week we will follow a public dataset through two related decisions. First, we will decide what the data can tell us about distribution and capacity. Then we will load it into a database and test what happens when the same import runs again.

Imagine that a colleague asks you to build a small catalog application. The first import succeeds. Tomorrow the source publishes an update, and your colleague runs the same program again. A program that simply appends every row can create duplicates. A program that replaces the whole database can erase information that somebody else added. Before choosing either behavior, we need to identify the records, understand the source, and define the intended effect of a repeat.

Our example uses a historical subset of CISA's Known Exploited Vulnerabilities catalog. We will analyze records about vulnerabilities, not download vulnerable software or test anybody's system. The same import decisions apply to transit records, museum collections, product catalogs, and many other datasets.

On Day 1, we will use Python to measure key choices and make a bounded distribution experiment. On Day 2, we will complete a repeatable import. SQLite gives everyone a working local path. Atlas and PostgreSQL are optional alternatives. The two meetings contribute to one individual notebook submission, with no separate report.

## Slide 2

Capacity planning begins with a workload that we can describe and measure. The size of a database is one part of that description. It does not tell us how quickly users need answers, how many operations arrive together, or which records receive most of the attention.

Latency measures how long one request takes. If a lookup starts now and finishes eighty milliseconds later, its latency is eighty milliseconds. Throughput measures completed work over an interval, such as requests per second. A system can have substantial throughput while some individual requests remain slow. The two measurements answer different questions.

The working set consists of the data and index pages that the workload uses repeatedly. A large archive can have a relatively small active working set. A smaller database can still cause heavy disk activity if its common operations touch many different pages. We need observations of the actual access pattern to understand that pressure.

The growth horizon tells us how far ahead a projection looks. Planning for tomorrow and planning for a year require different assumptions about retention and incoming data.

Our catalog could support a daily summary and an interactive lookup. The summary might scan many records once a day. The lookup might retrieve one identifier thousands of times. Using the same data does not give these operations the same capacity requirements.

## Slide 3

Here is a complete, small calculation that shows why the average alone can hide a problem. We have twenty invented request durations. Eighteen requests take twenty milliseconds, one takes five hundred, and one takes one thousand. These numbers are a teaching example. They are not measurements from a cloud service.

The multiplication of the list repeats the value twenty eighteen times. We append the two slower observations and then sort the list. Adding all durations gives eighteen hundred sixty milliseconds. Dividing by twenty gives a mean of ninety-three milliseconds.

Now consider the ninety-fifth percentile using the nearest-rank convention shown here. Multiply twenty by zero point ninety-five to obtain nineteen. The ceiling operation selects rank nineteen. Python counts list positions from zero, so the expression subtracts one before indexing the sorted list. Position eighteen contains five hundred milliseconds.

The average therefore says ninety-three milliseconds while the nearest-rank p95 says five hundred milliseconds. Neither calculation contradicts the other. They describe different features of the same observations. The slowest observation is still one thousand milliseconds.

Percentile implementations can use different conventions, particularly with small samples. State the convention when reproducing a calculation. Twenty synthetic requests cannot establish a service-level objective or a reliable production benchmark, but they make the distinction between an average and a slow tail concrete.

## Slide 4

Several changes can address capacity pressure, and each changes a different part of the system. Query and index tuning can reduce unnecessary work. If a query examines many irrelevant records, adding machines might postpone the problem while preserving an inefficient access pattern. We still check the answer and the index's effect on writes.

Scaling up gives one node more resources, such as memory or CPU. It can be a reasonable operational choice when the bottleneck fits those resources. It also has a cost and an eventual limit.

A cache can avoid recomputing or rereading a result. Read replicas can serve suitable reads away from another member. Both require a decision about freshness. An old product description and an old account balance can have very different consequences.

Partitioning divides a table or collection according to a rule. Partitioning within a database can help a query skip irrelevant portions or make retention easier. That arrangement does not automatically distribute execution across independent machines.

Sharding places portions across nodes and adds routing, balancing, and recovery responsibilities. We should be able to name the measured pressure that makes those responsibilities worthwhile.

For our seventy-five records, tuning or simply retaining a small, understandable design is a stronger starting point than building a distributed deployment. We study distribution so that we can recognize a future need and explain its tradeoffs.

## Slide 5

Replication and sharding describe different placement decisions. A replica set maintains copies of the same logical data. If our seventy-five-record collection lives on a three-member replica set, each data-bearing member maintains that logical collection. Replication supports availability and recovery from some member failures, subject to the configuration and the operation's durability guarantees.

Sharding divides ownership of the collection. In the balanced illustration here, three shards each own about twenty-five of the seventy-five records. The collection still has seventy-five logical records. We did not create three unrelated catalogs. A router makes the distributed collection available through a common interface.

Each shard can itself use replication. In that arrangement, replicas of the first shard maintain its assigned portion, replicas of the second shard maintain the second portion, and so on. Dividing ownership does not remove the need to protect each portion from a member failure.

The equal split in the table is an illustration. Actual placement depends on keys, sizes, ranges, and balancing behavior. Equal record counts also do not establish equal work. One shard might own records that receive almost all requests, or records whose documents are much larger.

This distinction prevents a common mistake: counting replicas as if they each added an independent share of write capacity for the same data. Copies and distributed ownership have different operational consequences.

Sources:
https://www.mongodb.com/docs/manual/sharding/

## Slide 6

This diagram separates the roles inside a sharded MongoDB cluster. The application connects through mongos, the query router. The router uses the cluster's metadata to determine which shards are relevant to an operation. The shards hold portions of the application data. Each shard's replica set protects that shard's portion through replication.

The config server replica set maintains cluster metadata, including information about the distribution of data. That metadata allows routing to follow the current placement rather than requiring application code to hard-code a machine for every record. Config servers have a different role from the shards that store the application collection.

Consider an exact lookup that includes an appropriate shard-key value. The router can use that value and the distribution metadata to target the relevant location. A query whose filter lacks the information needed for targeting can require work on multiple shards. The application may receive one result even though several servers participated in producing it.

This diagram explains architecture. We are not deploying these components in our lab. Atlas Free does not provide a sharded cluster for this exercise. Our Python experiment models a small part of placement so that we can reason about it without paying for infrastructure or confusing a simulation with a deployment.

Keep the roles distinct as we continue: the router routes, the metadata describes placement, and the shards hold the distributed data.

Sources:
https://www.mongodb.com/docs/manual/sharding/
https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/

## Slide 7

Our source is the CISA Known Exploited Vulnerabilities catalog. This classroom fixture selects seventy-five records from a catalog version dated July tenth, twenty twenty-six. The retrieval record is dated July thirteenth. A catalog version and a retrieval time describe different events: when the source version identifies itself and when we obtained our copy.

The slide shows selected fields from the first example record. The CVE identifier gives us a stable identifier to match on repeat imports. Vendor and product are descriptive labels. The dateAdded field describes inclusion in this catalog. It does not tell us the moment somebody first discovered the weakness, first exploited it, or installed vulnerable software.

The cwes field is a list. A record can therefore carry more than one weakness identifier without inventing a delimiter inside a single label. We will preserve that list when we choose a database representation.

Seventy-five records are enough to make our code and calculations inspectable. They are not a random sample, and they do not represent the current complete catalog. A count of vendor labels in this subset does not measure a vendor's overall security quality or the number of affected computers.

We will keep the source metadata with the fixture so that another person can understand which observations produced our classroom results.

Sources:
https://github.com/cisagov/kev-data
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 8

JSON parsing establishes that the text follows JSON syntax. It does not establish that an identifier is present, that a date is possible, or that a field uses the type our model expects. The notebook checks those conditions before opening an import path.

A required text field must contain nonempty text. An identifier must have the CVE form used by this source. Dates must parse as calendar dates and must use the canonical year-month-day representation. February thirtieth fails because the date is impossible. A compact string such as twenty twenty-six zero two zero one fails our representation check even if a library can interpret it.

Duplicate identifiers require a decision about which record is authoritative. Silently keeping whichever appears last could conceal a source conflict. The notebook therefore stops instead of choosing on our behalf.

The CWE field must be a list. An empty list stays empty. It does not justify inventing a weakness value or claiming that the vulnerability has no weakness.

Finally, the fixture includes a vendor label with a trailing space. The notebook reports it and preserves it. Trimming may be a useful later transformation, but it changes exact-value grouping. We would document and test that transformation rather than quietly changing the evidence. Data quality work often means making assumptions explicit before a write succeeds.

## Slide 9

Cardinality and frequency describe different properties of a candidate key. Cardinality counts distinct values. Frequency counts how often values repeat. This small ticket example makes both quantities visible without requiring a database.

Suppose eight tickets use two statuses. Six are open and two are resolved. The status field has cardinality two. Its most frequent value appears six times, which is seventy-five percent of the records. If placement depends only on status, all six open tickets share the same key value. Adding machines cannot make those identical values become distinct.

Now give each ticket a different identifier. The identifier field has cardinality eight, and each value appears once. Its largest record share is one eighth, or twelve point five percent. That gives us a finer-grained way to identify and place records.

However, a unique identifier does not prove that requests will spread evenly. A particular ticket could be the subject of nearly every lookup. The stored records would have perfect identifier uniqueness while the request workload remained concentrated.

That is why we distinguish record frequency from request frequency. Our notebook measures the records in a fixture. It has no production request log. We can calculate a candidate's properties and identify risks, but we cannot infer real user demand from uniqueness alone. Keep that boundary in mind when writing your recommendation.

## Slide 10

These measurements come from the actual seventy-five-record teaching snapshot. The CVE identifier has seventy-five distinct values. Its largest value count is one, giving a largest share of one point three three percent after rounding. That makes it useful for identifying one record and matching a repeat import.

The dateAdded field has thirty-eight distinct values. The most repeated date appears eight times, or ten point six seven percent. Those dates can support a time-oriented question, but repeated dates and the order of new arrivals matter for placement.

Vendor has forty-two distinct labels. Microsoft appears sixteen times, making the largest share twenty-one point three three percent. Combining vendor and product increases the distinct count to fifty-six and reduces the largest repeated pair to four records in this fixture.

A compound candidate can divide some groups more finely, but more distinct combinations do not automatically make it the correct shard key. We still need to know which predicates the application supplies and which records receive writes or reads together.

These percentages are descriptive statistics for this selected source. They are not response times or utilization measurements. There is no evidence here that our classroom database has a production bottleneck. In your lab, compare the identifier and date using two measurements, then connect the measurements to a specific query rather than selecting the largest number automatically.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 11

A ranged rule places nearby key values together. We can illustrate that behavior by sorting our records by dateAdded. The oldest sixty records establish three boundaries. We then hold those boundaries fixed and treat the newest fifteen as later writes.

The boundaries in this particular fixture are April twenty-second, May twentieth, and June first of twenty twenty-six. Bucket zero contains dates before the first boundary. Bucket one starts at the first boundary and ends before the second. Bucket two starts at the second and ends before the third. Bucket three begins on June first and includes later dates.

The notebook uses bisect_right to count how many boundaries a date has reached or passed. Because the dates use a fixed year-month-day representation, their string order agrees with their calendar order. The earlier validation makes that assumption explicit.

All fifteen later records land in bucket three. This shows how an advancing time key can concentrate new writes in the current upper range while older records remain elsewhere.

We deliberately omit balancing and migration from this experiment. Real MongoDB distribution can change as ranges move. Also, our ordering is a teaching construction from catalog dates, not an observation of production arrival times. The experiment isolates a mechanism: fixed date ranges and increasing dates can put later work in one range. It does not measure the performance of an actual cluster.

## Slide 12

Both series in this chart use the same fifteen later records. The gray bars show their placement under the fixed date ranges. All fifteen fall into bucket three. The green bars show placement after hashing each CVE identifier and taking the remainder after division by four.

The hash rule produces three records in bucket zero, three in bucket one, six in bucket two, and three in bucket three. Adding either series gives fifteen. That sum matters because an apparent improvement in distribution would be meaningless if the comparison silently dropped some records.

Hashing changes the placement rule. It does not promise a perfectly equal split. With only fifteen records, a three-three-six-three result is entirely plausible. We also lose the simple relationship between a nearby calendar date and a nearby placement range.

Our code uses SHA-256 and four teaching buckets. MongoDB uses its own hashing and range-management behavior. This chart is therefore a transparent, reproducible illustration rather than a reconstruction of MongoDB's internal routing algorithm.

No latency, throughput, document size, or balancing cost appears in the chart. We can conclude that the two rules placed this selected set differently. We cannot conclude that the green rule makes every query faster. The next slides separate the properties that hashing changes from the properties it preserves, and then connect placement to the query we actually need to answer.

Sources:
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 13

Hashing is deterministic. The same input gives the same output under the same algorithm. This short Python example encodes the word Microsoft, computes its SHA-256 hexadecimal digest, converts that digest into an integer, and takes the remainder after division by four. The result is bucket one.

Repeat the calculation sixteen times with the same string, and it still gives bucket one sixteen times. Hashing does not turn repeated values into unique values. If we used vendor alone as the candidate, all sixteen Microsoft records would share the same hashed vendor value in our simulation.

The notebook instead hashes CVE identifiers, which are distinct in the checked fixture. That changes the inputs to the placement function and explains why the later-record comparison can spread those inputs across buckets.

This distinction helps us evaluate a proposed fix. If the problem is a highly repeated field value, simply adding the word hashed to the design does not divide that value. A different candidate or a justified compound key may change the granularity, but it also changes query-targeting requirements.

We are using the hash as a placement function here. We are not using it to encrypt the source data, hide a vendor name, or authenticate a record. A hash function can participate in different systems, and the purpose in this example is the deterministic mapping from an identifier to a teaching bucket.

## Slide 14

Suppose a future version of this collection used a hashed CVE identifier as its shard key. An exact equality filter on that identifier gives the router the key value needed to target its location. That is a useful fit for a lookup whose main question is about one known vulnerability.

A filter that supplies only a vendor label does not supply that CVE key. The same is true of a filter that supplies only a date window. The system can still answer those questions, but the chosen shard key does not narrow them in the same way. Work may need to reach multiple shards.

A local index and shard targeting solve related but distinct problems. An index on vendor can reduce the records examined within a shard. That does not automatically tell the router which shards contain every relevant vendor record.

Counting all records by vendor naturally needs information from across the collection. A distributed aggregation can be appropriate for that whole-collection question. We should avoid treating every multi-shard operation as a mistake.

The useful design question is how our frequent operations match the key and what work those operations require. A candidate that supports exact-ID lookups well can be a weaker fit for date-range access. Our lab recommendation names that tradeoff rather than treating cardinality as a universal ranking.

Sources:
https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/
https://www.mongodb.com/docs/manual/core/hashed-sharding/

## Slide 15

A storage projection is useful when its assumptions remain visible. This example begins with one hundred mebibytes of retained data, adds twenty mebibytes per day, and looks thirty days ahead. We first multiply twenty by thirty to obtain six hundred mebibytes of additional retained data. Adding the initial hundred gives seven hundred.

We then apply an assumed overhead multiplier of two, producing fourteen hundred mebibytes. That multiplier is part of this teaching scenario. It is not a MongoDB or Supabase billing formula, and it does not establish the size of indexes, replicas, backups, or temporary processing space in a real deployment.

The order of operations reflects the model. We project retained data first and apply the chosen multiplier to that total. A different retention policy changes the projection. If records expire after seven days, adding thirty days of arrivals without subtracting departures would overstate retained data. If document sizes grow, a constant daily estimate may understate it.

Units also matter. A mebibyte contains one million forty-eight thousand five hundred seventy-six bytes. A megabyte contains one million bytes. A provider quota and a local size report may use different units.

For a real plan, we would measure representative record and index sizes, specify retention, and compare estimates with observed growth. The equation makes those assumptions discussable and revisable.

## Slide 16

You will now work individually in Notebook 06. Use the embedded snapshot so that your results refer to the same source version as the worked examples. Sections one and two inspect the source, check the selected fields, measure candidate keys, and compare the two placement rules.

Read the source and stored values as you run the cells. The code is part of the lesson. You do not need to create a sharded cluster, purchase a service, or configure a database account for this part.

Concentrate your comparison on CVE identifier and dateAdded. Use two numbers the notebook displays. For example, you can compare their distinct counts and largest-value shares. Then connect that comparison to the grouped question you want to answer. An exact identifier and a date window supply different information to a placement rule.

Also state whether this seventy-five-record classroom database needs sharding. Your answer should distinguish the measured size of this exercise from a hypothetical future workload. A recommendation to keep the design small can be well supported when it explains the current need and what would trigger reconsideration.

Keep the notebook for Day 2. You can note your reasoning in its submission area, but there is no separate Day 1 submission. We will add the import, repeat-run test, changed query, and short handoff to this same notebook during the second meeting.

## Slide 17

Our second meeting starts with a program that runs more than once. Yesterday's import created records. Today's import encounters records that may already exist. The intended effect of that second run belongs in the design, because retries and scheduled refreshes are ordinary parts of operating a data system.

We will use a stable CVE identifier to recognize a logical record. The load will update the selected values when that identifier already exists and insert when it does not. With the same unchanged source, repeating the load should leave the same logical records and values.

We will also inspect what the database actually contains. A successful connection establishes a network and authentication result. An import count tells us something about cardinality. A query result and a comparison with a known source record give us additional, different checks.

SQLite lets everyone run the complete example without a remote database. If you choose Atlas or PostgreSQL, you will additionally cross a network boundary and handle a database credential. Those paths should remain understandable rather than hiding the connection inside a large helper function.

The final written piece is a short handoff inside the notebook. It explains your question, evidence, repeat behavior, and limitation to a hypothetical colleague. It remains individual work, and it does not add a second submission or require you to form a team.

## Slide 18

The TARGET variable chooses the database path. Leave it as sqlite for the simplest route. Python includes the SQLite driver, and this notebook creates an in-memory database inside its own process. Once the notebook is open, that path needs no database account or package download.

The atlas choice uses PyMongo to connect to a MongoDB Atlas project. It needs a database user and a network rule that allows the notebook runtime's address. The postgres choice uses Psycopg to connect to PostgreSQL, including a Supabase project through the suitable connection endpoint.

Choose one target for the required work. Trying a second is optional. You do not receive a more complete repeat-run test merely by connecting to more providers.

The setup cell creates unique practice names and initializes connections. Run it once for a practice run. Then repeat the selected import cell against that existing target. If you recreate an empty database before each import, the second run never encounters the first run's records, so it does not test the behavior we care about.

The notebook prevents starting another setup while the current run remains open. To switch targets, run cleanup and then begin the section again. This keeps the lifecycle visible and reduces the chance of abandoning practice objects or connections while experimenting with another database.

## Slide 19

The source uses JSON, but each database path still needs a representation decision. The CVE identifier becomes a text primary key in the two SQL paths. In MongoDB, the collection has a unique index on cveID. That business identifier is separate from MongoDB's automatically supplied document identifier.

The dates describe calendar days without a time of day. SQLite stores their canonical year-month-day text. MongoDB keeps the same strings in this lesson. PostgreSQL uses its date type. A different application might require timestamps and time zones, but adding midnight here would imply information that our selected date field does not provide.

The CWE list crosses the boundary in three ways. SQLite receives serialized JSON text. MongoDB receives a native array. PostgreSQL receives a jsonb array. We preserve the list structure instead of joining its entries into a comma-separated label that would require another parsing convention later.

When we verify a known record, the code converts the SQL date objects and the SQLite JSON text back into the source representation. Otherwise, a date object and an equivalent date string could compare as different Python values even when they represent the same calendar day.

These conversions are small examples of data modeling in integration work. A field's name alone does not establish its type, meaning, or round-trip behavior. We make those decisions visible and check them.

## Slide 20

Atlas evaluates the network address of the client that connects to the database. In Colab, the Python process runs on a remote notebook machine. That machine can have a different public address from the laptop running your browser.

The notebook asks an IPv4 lookup service for the runtime's public address and prints it with a slash thirty-two suffix. In this context, that suffix selects one IPv4 address. Add that address to your Atlas IP access list, preferably with an expiration when the dashboard offers one. Wait for the rule to become active, then return to the notebook's confirmation prompt.

The browser's Add Current IP control may identify your laptop instead. Adding only that address can leave Colab unable to connect. If Colab replaces the runtime, check its address again rather than assuming yesterday's rule still applies.

The screenshot is a redacted Atlas overview captured in August. It locates Connect and Database and Network Access. It does not show a newly verified connection from your notebook. Connect and Drivers provide the Python connection-string format. Use a database user's credentials, not the password you use to sign into the Atlas website.

Keep the credential inside the hidden prompt. Do not paste it into a code cell, screenshot, or submission. After class, remove the temporary runtime rule. Closing Python does not remove that provider-side permission.

Sources:
https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 21

This excerpt shows the actual connection decision instead of hiding it in a function. MongoClient receives the URI from the hidden prompt. TLS is enabled, and tlsInsecure remains false so that the connection does not bypass certificate and hostname checks.

The server API configuration requests the stable API behavior used by our example. The timeout options bound server selection and individual operations rather than leaving an unsuccessful connection attempt waiting indefinitely. The value ten thousand is in milliseconds.

Creating a client object is not the same as proving a connection. PyMongo can initialize a client before completing the work needed for an operation. The ping command therefore gives us an explicit request whose success demonstrates that the client can communicate with the deployment.

A ping still does not create our dataset or prove that its values are correct. Those are later operations with their own checks.

The complete notebook cell validates the URI form, catches a failed connection, closes a failed client, and clears the temporary URI variable. The connected client still holds the authentication state it needs until cleanup closes it. Clearing a variable is not a substitute for protecting a credential.

If the connection fails, check the database user, percent-encoded password, active runtime IP rule, cluster availability, DNS, and TLS configuration. Disabling TLS checks would weaken the connection without explaining the cause.

Sources:
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/server-selection/

## Slide 22

Supabase provides a PostgreSQL database as well as other application services. This notebook uses a PostgreSQL connection, so it needs the database password and the exact connection details from the project's Connect panel. A Supabase website login and an API key have different roles.

For a notebook network that cannot reach the direct IPv6 endpoint, select the shared session pooler connection. That endpoint supports IPv4. Copy the exact pooler username shown for your project rather than guessing it from an example. The screenshot locates the Connect button, but it does not show the pooler dialog itself.

Transport encryption and server identity verification are related but distinct. The notebook requires an encrypted SSL mode. Require provides encryption. Verify-full additionally checks the certificate and hostname when configured with the provider's certificate authority. We do not solve an unreachable IPv6 address by disabling encryption, because those settings address different layers of the connection.

The code creates a uniquely named practice schema so that our table does not collide with an existing project table. It clears the temporary connection URL after the attempt and keeps the connection available for the following cells.

If a connection fails, separate the likely layers: endpoint and network reachability, database credentials, project availability, transport configuration, and permission to create the practice schema. The SQLite route remains a complete way to finish the required learning if a cloud account is unavailable.

Sources:
https://supabase.com/docs/guides/database/connecting-to-postgres
https://www.postgresql.org/docs/current/libpq-ssl.html

## Slide 23

This code reads one known record after the PostgreSQL import. The outer transaction block gives the operations a clear transaction boundary. The cursor sends commands and reads their results.

The first command chooses the practice schema for this transaction. A schema is a namespace for database objects. SET LOCAL limits the search-path change to the current transaction, so the setting does not silently persist as the notebook moves between activities.

Notice two different substitution mechanisms. The schema name enters the command through sql.Identifier. That mechanism quotes a database identifier. The CVE identifier in the WHERE condition enters through a percent-s placeholder and a separate parameter tuple. It is a data value, not a table or column name.

The comma after known_id creates a one-element Python tuple. Without it, parentheses alone do not make a tuple. The driver receives that tuple separately from the SQL text and handles the value representation.

Fetchone returns the selected row or None when no row matches. Our complete verification checks for a missing result before interpreting its fields.

Do not replace this pattern with a string that inserts arbitrary input directly into SQL. Also do not try to use a value placeholder to choose the schema or column. Identifiers and values occupy different positions in SQL syntax, and the driver gives us different tools for each.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html
https://www.psycopg.org/psycopg3/docs/basic/params.html

## Slide 24

The first import starts with an empty practice table or collection and ends with seventy-five records. That confirms the count for a first load. It does not yet tell us what a repeat will do.

For the second test, keep the same database, table or collection, and source records. Run only the selected import cell again. This time the count begins at seventy-five and ends at seventy-five. The import encounters existing identifiers and applies its conflict behavior rather than creating another seventy-five logical records.

The last row shows a misleading alternative. If we reset setup before every attempt, every attempt starts from zero. The program might look repeatable because it produces seventy-five records each time, but we have not exercised a collision with previous output. We have repeatedly tested a fresh database.

Count equality alone is also incomplete. A program could change a title, replace the wrong record, or store a malformed list while leaving the total unchanged. That is why the notebook compares selected stored values with the source and independently checks the grouped query result.

For the unchanged source in this exercise, idempotent behavior means that repeating the load leaves the same logical records and values. It does not mean no code runs or no database operations occur. It also does not promise to retain historical versions or remove records absent from a future source.

## Slide 25

This is the MongoDB repeat-import loop. Each iteration uses the current record's CVE identifier in the match condition. Replace_one replaces the matched document with the selected source record. Upsert set to true allows an insertion when no document matches that identifier.

The collection's unique index on cveID enforces one document per business identifier. Without a stable match and an appropriate uniqueness rule, a retry can create another logical copy even though MongoDB gives every document its own different internal identifier.

Replacement is a deliberate choice for this disposable import collection. The selected source fields are authoritative for these records, so replacing them can repair a previously changed value. If the collection also held application-owned annotations, replacing the whole document could remove those annotations. That different application would need a different update design or a separate place for annotations.

This loop only visits identifiers present in the selected source. It does not remove an older database record merely because a later source omits it. It also overwrites selected values rather than creating a history table or event log. Those are separate requirements that we would have to implement intentionally.

Run the unchanged source twice against the same practice collection. Then inspect the result. The stable identifier explains the matching behavior, while the query and value comparisons tell us whether the stored data matches our intended outcome.

Sources:
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/

## Slide 26

Atomicity and idempotency answer different questions. Atomicity defines which changes succeed together. Idempotency describes the effect of repeating an operation. A useful import can have repeat behavior without making every write part of one all-or-nothing unit.

In the SQL paths, the notebook places the batch inside a transaction. Suppose the fourth row violates a required constraint. The transaction rolls back its earlier writes instead of committing the first three and leaving the batch halfway applied. Work committed before this transaction remains outside that rollback boundary.

The MongoDB loop uses separate replace_one calls. Each document replacement is atomic for that document. If the fourth call fails, the first three completed replacements remain. This example does not wrap all seventy-five documents in a multi-document transaction.

A retry with the same checked source can match the stable identifiers and finish the import. The retry still needs verification, and it is not a complete production retry policy. A changing source, concurrent writers, authorization failure, or permanent malformed record can require additional decisions.

MongoDB does support transactions in suitable deployments. We are describing the behavior of the code on the previous slide, not a claim that MongoDB cannot offer a larger transaction boundary. In operational work, identify the actual unit of success in the program you run rather than assuming a database product name determines it.

Sources:
https://www.psycopg.org/psycopg3/docs/basic/transactions.html
https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 27

Suppose an imported vulnerability title changes to the wrong text. The collection or table still contains seventy-five records. The known CVE identifier still exists. The vendor counts can still match because the modified field is the title rather than the vendor.

Those checks pass while the record remains wrong. The final row adds a different check: compare every selected field of one known record with the source. That comparison fails and exposes the value difference.

The notebook chooses a known identifier from the checked source, retrieves its stored record, and normalizes representation differences such as PostgreSQL date objects and SQLite JSON text. It then compares the eight selected fields. For MongoDB, it excludes the database-generated internal identifier because that field is not part of the selected source comparison.

Rerunning the unchanged import repairs the selected record when the source remains authoritative. We can then rerun verification to see that the values agree. A passing result after repair is more informative when we understand which earlier check would have missed the error.

This check still has a boundary. One known record does not prove all records and all omitted fields are correct. The grouped comparison adds coverage for the selected grouping, but it does not establish security, backup readiness, or production capacity. Our explanation should name what each check covers without turning a small successful test into a universal claim.

## Slide 28

These two result tables answer different questions using the same selected catalog entries. The left table groups by vendor label. Microsoft appears sixteen times and Cisco seven times. The right table groups by product label. Catalyst SD-WAN Manager and Windows each appear four times.

The unit being counted is a selected catalog entry. These numbers do not count installations, customers, exploit attempts, or compromised machines. A product with several catalog entries contributes several records to its group. That distinction belongs in any written interpretation of the result.

The code sorts groups by descending count and breaks ties by the label. A defined tie order helps us compare the database result with an independently computed result from the source. Without an explicit tie rule, two correct groupings might display equal-count rows in different orders.

The quoted SimpleHelp vendor label includes a trailing space. We use the quotation marks on the slide to make that space visible. The stored label itself remains the source text. The product label SimpleHelp does not have that same trailing space in the displayed product group.

For your change, run the vendor grouping first, change GROUP_FIELD to product, and rerun the cell. Explain one displayed row using its new unit of grouping. The question should change along with the code, rather than continuing to call the output a vendor result.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 29

Changing a grouping column is different from supplying a search value. The GROUP_FIELD variable selects one of two allowed source fields. The mapping translates that choice into the corresponding SQL column name. VendorProject maps to vendor_project, while product keeps the same spelling.

The complete cell rejects any choice outside those two entries. The PostgreSQL path then uses sql.Identifier to quote the selected column name. The SQLite path constructs SQL from the same restricted mapping. We would not place unrestricted input into that formatted SQL string.

A percent-s placeholder binds a value. For example, it can supply the CVE identifier in a WHERE comparison. It cannot turn a value into a column name in a GROUP BY clause. Quoting a name and binding a value are separate responsibilities because the SQL parser gives them different meanings.

This is also a useful interface design. The notebook exposes one small, intentional decision that students can change without rewriting the connection and import code. We can inspect exactly which behavior that decision affects.

The Atlas path makes a corresponding field expression, such as dollar-product, for its aggregation pipeline. The syntax differs, but the question remains the same. After the change, the notebook computes the expected grouping directly from the source records and compares it with the database output, including the tie order.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html

## Slide 30

Complete the second part of the lab in the notebook you started during the first meeting. Choose one database target. Run its setup once, then run its import cell twice without creating a new target between attempts. Keep the before-and-after result so that you can explain what the second import actually encountered.

Run the known-record verification and the vendor grouping. Then change GROUP_FIELD to product and run the grouping again. Read one row as a sentence about the selected records. The notebook's independent source comparison should agree with the database result.

In the submission area, write a short handoff as if a colleague will maintain this small import tomorrow. Explain your question, two measurements relevant to the key comparison, the repeat-run result, and one limitation. Use the evidence already in your notebook. You do not need to paste every output into the prose or create a separate document.

The colleague is the audience for your writing, not a required partner. Work individually and submit one completed notebook in Brightspace. There is no additional report, screenshot, matrix, or repository for this lab.

Run cleanup when finished and remove any accidentally recorded credential before submitting. The final-project discussion uses the project's existing assignment. This lab supplies reusable skills and ideas without adding another set of final-project deliverables.

## Slide 31

Cleanup is part of the program's behavior. It should remove the practice objects we created without treating an entire existing cloud project as disposable.

For SQLite, closing the connection discards this in-memory database. For Atlas, the cleanup cell drops only kev_sample in this run's uniquely named database and then closes the client. An unrelated collection in that database remains. The temporary IP rule is a separate provider-side setting, so remove that rule in the dashboard after you finish.

For PostgreSQL, the cell drops the practice table and tries to remove the generated schema only when it is empty. It does not use CASCADE to remove other objects. If another table remains there, the schema stays rather than destroying that unrelated work. The connection then closes.

Closing a client does not pause or delete a hosted service. It also does not remove an Atlas network rule. Those operations belong to different layers of the system. If you changed other provider settings while connecting, review and reverse only the temporary changes you actually made.

The selected data is public and the practice names are unique, but that does not justify broad cleanup commands. The habit transfers to professional work: identify what your process owns, remove that scope, and distinguish deleting data from revoking access and stopping infrastructure. Our notebook makes those boundaries visible instead of hiding them behind a generic reset button.

## Slide 32

Here is a way to describe this work in an interview without overstating it. I built a small repeatable import from a documented public source. I compared candidate distribution keys, ran the same import twice, and checked a grouped result and selected stored values. I can explain what I measured and why a small fixture does not prove production scalability.

Adapt that account to the path you actually ran. If you used SQLite, say that you implemented and checked the local path and studied the cloud connection alternatives. If you connected to Atlas or PostgreSQL, name the network and credential decisions you handled. Do not claim a sharded deployment because you ran a four-bucket Python simulation.

A useful follow-up explanation identifies the stable key, the transaction boundary, and a failure your checks can detect. For example, matching the row count can miss an incorrect title, while the known-record comparison can expose it. That is more specific than saying that the import worked.

For your project, discuss one source, one important query, and a measured condition that would justify a capacity change. Keep the existing final-project requirements as the source for deliverables.

Next week, we will extend these ideas to an application that uses more than one store. Stable identifiers, repeat behavior, and explicit verification will help us diagnose why two copies can disagree and how to repair them without creating another inconsistency.

## License

Original course prose is licensed under CC BY 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
