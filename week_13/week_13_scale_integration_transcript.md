# Week 13: Capacity, Sharding, and Python Integration - Spoken Transcript

The transcript follows the slide order and includes source references.

## Slide 1

Welcome to Week 13, Tuesday November 24, 2026. Thanksgiving closes the Thursday meeting. We have one hundred minutes and one notebook submission. Week 12 was November 17 and 19; the separate recovery lesson remains a Week 12 resource.

A public dataset becomes a database. The next import arrives tomorrow. Suppose a colleague runs the same import again: will the records double, or will the program recognize the records already there? Today we will answer that with evidence from real MongoDB Atlas.

Start before the terminology. A document is one record with named fields. Our records describe vulnerabilities in CISA's historical Known Exploited Vulnerabilities catalog. Colab runs Python on a remote computer, PyMongo carries requests, and Atlas stores documents. A collection holds the documents in a database.

Open Notebook 06 and save your own Drive copy. Use Cells 01, 02a with USE_LIVE_FEED False, 02b, and 03–08; then 10, 11 twice, 14, and 15. Skip the optional SQLite and PostgreSQL cells. Setup comes before the twenty-minute individual lab. In that lab you change the grouped question and write a five-to-seven-sentence handoff. Submit one viewable Colab link in Brightspace.

Teaching route: 0–10 minutes slides 1 and 7; 10–25 slides 8, 5, 9, 10, and 12; 25–50 slides 19, 21, and 22; 50–65 slides 27, 25, 26, 29, and 30; 65–85 slide 32; 85–100 slides 16, 33, and 34. Use the remaining slides for optional reference.

## Slide 2

Before anybody says the word sharding, we need a workload we can actually describe. Look at the four rows on the slide.

Latency is how long one request takes. A lookup that starts now and finishes eighty milliseconds later has a latency of eighty milliseconds. Throughput is how much work finishes in an interval, like requests per second. Why keep them apart? Because a system can push a lot of requests per second while some individual users still wait a long time. Those are different complaints with different fixes.

The working set is the data and index pages the workload touches again and again. That is what needs to stay close at hand to be fast. A huge archive can have a tiny working set, and a small database can keep the disk busy if its common queries touch pages all over the place. Measure the actual access pattern to find out.

The growth horizon is how far ahead you are projecting. Planning for tomorrow and planning for a year need different assumptions about retention and incoming data.

Now read the line at the bottom. Our catalog could feed a daily report and an interactive lookup. The report scans lots of records once a day. The lookup might fetch one ID thousands of times. Same records, completely different capacity needs. The size of the database tells you none of that.

## Slide 3

Here is why I never trust an average by itself. This is a complete little Python calculation, and the numbers are invented on purpose. This is a synthetic twenty-request trace.

The second line builds the list. Twenty times eighteen means eighteen requests at twenty milliseconds, then one at five hundred and one at one thousand. We sort it. Add everything up and you get eighteen hundred sixty milliseconds. Divide by twenty, and the mean is ninety-three milliseconds. Sounds fine.

Now the ninety-fifth percentile, using nearest rank. Twenty times zero point nine five is nineteen, and the ceiling keeps it at rank nineteen. Python counts from zero, so the code subtracts one and reads position eighteen of the sorted list. Five hundred milliseconds.

Run it, and it prints ninety-three point zero and five hundred. Same data, two very different stories. The average says everything is quick. The p95 says one request in twenty waits half a second. And the slowest request took a full second. That slow tail is what people actually complain about, and the mean smoothed it away.

Two cautions. Percentile conventions differ, especially with small samples, so always say which one you used. These twenty example requests show how a few long waits affect the 95th percentile.

## Slide 4

When a database gets slow, people jump straight to bigger hardware or more machines. This table is here to slow that reflex down. Each option relieves a different pressure, and each leaves a decision behind. Read across each row.

Tuning a query or an index removes work the database never needed to do. If a query examines thousands of irrelevant rows, adding machines just spreads the waste around. You still have to check that the answer is right and what the index costs on writes.

Scaling up gives one node more CPU or memory. That is often the sensible move, but it costs money and it has a ceiling.

A cache or read replicas take repeated reads off the main server. The decision there is staleness. An old product description is harmless. An old account balance is not.

Partitioning inside one database splits a table by a rule, so queries can skip irrelevant parts, or old data can be retired easily. It does not, by itself, spread work across machines.

Sharding does spread data across nodes, and it hands you routing, balancing, and recovery as new jobs. You should be able to name the measured pressure that is worth taking those jobs on.

Read the line at the bottom. For our seventy-five records, the honest answer is tuning, or just keeping the design small. We study distribution so we can recognize the day it is actually needed.

## Slide 5

Two words that get mixed up constantly: replication and sharding. They are different placement decisions, and the table shows our seventy-five-record collection placed three ways.

First row. One replica set with three members. Every member keeps the same logical seventy-five records. These are copies. Why have copies? Availability. If one member fails, another can take over, depending on the configuration and the durability the operation asked for.

Second row. Three shards with a balanced split. Now each shard owns about twenty-five of the seventy-five. Each shard owns a portion of the records. The collection still has seventy-five logical records. A router presents the pieces as one collection.

Look at the third row. Each shard has its own replicas. The first shard's replicas copy the first shard's portion, and so on.

Now read the warning under the table. The example shows an even split. Real placement depends on keys, sizes, ranges, and balancing. Now consider which records receive the most requests. One shard might own the records that get almost every request.

The mistake this slide prevents is counting replicas as extra write capacity for the same data. Three replicas hold copies of the same records to support availability.

Sources:
https://www.mongodb.com/docs/manual/sharding/

## Slide 6

Here is what is actually inside a sharded MongoDB cluster. Follow the boxes from the top.

 It connects to mongos, the query router. The router figures that out, sends the work where it needs to go, and merges the answers.

How does it figure it out? The config servers. They hold the cluster metadata, including how the data is currently distributed. Because placement is described there, it can change without anybody rewriting application code. That is a different job from the shards, which store the application's data.

Then Shard A and Shard B. Each holds a portion of the data, and each one is a replica set protecting its own portion.

Read the line at the bottom, because it ties this to the rest of the day. The shard key decides distribution, and it decides whether a query can be sent to a limited set of shards. An exact lookup that includes the shard key value can be targeted. A query without that information may need work on several shards, and the application still sees one result.

In Cell 07, Python models how each key distributes our sample across four buckets.

Sources:
https://www.mongodb.com/docs/manual/sharding/
https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/

## Slide 7

Now our actual data. This is the CISA Known Exploited Vulnerabilities catalog. Our classroom fixture has seventy-five records selected from the catalog version dated July 10, 2026, and we retrieved it on July 13, 2026. Notice those are two different dates. One is when the source says its version was published. The other is when we got our copy. Keep both, because they answer different questions.

Look at the record on the left. The cveID, CVE-2026-56291, is a stable identifier. That is what will let us recognize the same record the next time we import. Vendor and product, Balbooa and Forms, are descriptive labels. And dateAdded is the date this record entered the catalog.

The cwes field is a list, in square brackets. One vulnerability can carry more than one weakness identifier, and a list holds that without inventing a comma convention inside a string. We will keep it a list in every database.

Read the note at the bottom. Seventy-five records are enough to check every calculation by hand. The snapshot preserves the first 75 entries in catalog order. A vendor count in this subset says nothing about a vendor's overall security or how many computers are affected.

Sources:
https://github.com/cisagov/kev-data
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 8

Validate the parsed JSON before loading it. Check that each ID is present, each date is valid, and each field has the expected type. So the notebook runs the checks in this table before it opens any import path. Let's go down the left column.

A missing vendor, ID, or required text field stops the import before anything loads. IDs also have to look like CVE identifiers.

February 30, 2026 fails because that day does not exist. The compact form, 20260201, fails too, even though a library could probably guess what it means. Why reject it? Because we want one canonical year-month-day form, and later our date ordering depends on it.

A repeated CVE identifier stops everything. Which record is the real one? If the code silently kept whichever came last, it would hide a conflict in the source. So the notebook makes us decide.

If cwes arrives as text instead of a list, that is rejected. And an empty list stays empty.

Last row. One vendor label is SimpleHelp with a trailing space. The notebook shows you the space and keeps the label as the source wrote it. Trimming changes the grouping, so document and test that choice.

## Slide 9

Before we measure the real dataset, here is a tiny made-up one, because two ideas get confused all the time. Cardinality counts how many distinct values a field has. Frequency counts how often each value repeats.

Look at the first row. Eight tickets, six open and two resolved. The status field has cardinality two. Its most common value, open, covers six of eight records, seventy-five percent. Now imagine we place records by status. All six open tickets have the same key, so they land together. Adding machines cannot help, because you cannot split identical values.

Second row. Give each ticket its own ID. Cardinality eight, and each value appears once, so the largest share is one in eight, twelve point five percent. That is a much finer way to spread records.

But read the line in the middle of the slide. A unique ID distributes records finely, but one ID can still receive most reads. Suppose everyone keeps opening the same ticket. The stored records are perfectly spread, and the traffic is all on one.

That is the line at the bottom. Record frequency and request frequency are different measurements. This fixture tells us how often a value appears in the stored records. To find the busiest keys, we would also need a request log.

## Slide 10

Now the real measurements, from the seventy-five-record snapshot. Four candidate keys. Read across each row.

cveID has seventy-five distinct values, each appearing once, so the largest share is one point three three percent. That makes it the right field for identifying one record and matching it on a repeat import.

dateAdded has thirty-eight distinct values. The most common date appears eight times, ten point six seven percent. Dates are good for time questions, but repeated dates, and the fact that new dates keep arriving, matter for placement. That is the next slide.

vendorProject has forty-two distinct labels, and the biggest, Microsoft, appears sixteen times, twenty-one point three three percent. Combine vendor and product and you get fifty-six distinct pairs, and the largest pair repeats only four times, five point three three percent.

So do we just pick whichever has the most distinct values? No. More distinct combinations do not make a correct shard key. What matters is which values your queries supply and which records get read or written together.

One practical note for the lab. Your notebook prints the distinct count, a ratio, and the largest value share. The largest value count column is on this slide to make the percentages concrete, so do not go looking for it in your output.

And read the note at the bottom. These numbers describe this selected dataset.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 11

Now a small experiment about time-based keys. A ranged rule keeps nearby key values together. That sounds good, and it is good for date-window queries. Watch what it does to new writes.

We sort the records by dateAdded. The oldest sixty records set the boundaries, and then we freeze them. The newest fifteen play the role of later writes arriving into those fixed ranges.

The boundaries in this fixture are April 22, May 20, and June 1, 2026. Read the table. Bucket zero is before April 22. Bucket one is April 22 through May 19. Bucket two is May 20 through May 31. Bucket three is June 1 onward, with no upper end.

The notebook uses bisect_right, which counts how many boundaries a date has reached or passed. That works on plain strings only because every date is in the canonical year-month-day form, so string order matches calendar order. That is why the checks on slide 8 rejected compact dates.

Now the last line in the box. All fifteen later records land in bucket three. Of course they do. Dates keep increasing, and the top range is the only open-ended one. In a real cluster, that pattern puts the new writes in one place while the older ranges sit quiet.

What we left out on purpose is balancing and migration. Real MongoDB moves ranges around. We order these records by the dates in the catalog. This isolates one mechanism.

## Slide 12

Same fifteen later records, two placement rules, side by side.

The gray bars are the fixed date ranges from the last slide. All fifteen sit in bucket three. The green bars are the hash rule. We hash each CVE identifier with SHA-256 and take the remainder after dividing by four. Look at the green bars: three in bucket zero, three in bucket one, six in bucket two, three in bucket three.

Do a quick check with me. Three plus three plus six plus three is fifteen. The gray series is fifteen too. Why bother adding them up? Because a comparison that silently dropped records could look like better distribution for a bad reason. Always check that both sides account for every row.

Run Cell 07a for one ID, then Cell 07 for the 15 arrivals. One bucket received six of the fifteen records. Each of the other three buckets received three. And we gave something up. Under the hash rule, two dates next to each other on the calendar no longer land next to each other.

Read the scope note above the chart. This is our own SHA-256 with four teaching buckets. Python assigns the example buckets. MongoDB uses its own hashing and range management. Read the chart as a count of the records each bucket receives under the two rules.

Sources:
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 13

Here is a property of hashing that people forget when they say "just hash it." Hashing is deterministic. Same input, same algorithm, same output, every time.

Read the code. We take the string Microsoft, encode it to bytes, compute its SHA-256 digest in hexadecimal, turn that into an integer, and take the remainder after dividing by four. Run it, and it prints one. Bucket one.

Now run it again. Still one. Run it sixteen times, once for each Microsoft record in our fixture, and you get bucket one sixteen times. Each repetition gives the same result. If vendor were our key, all sixteen Microsoft records would land together, hashed or not.

So why did the previous slide spread out? Read the last line on the slide. The notebook hashes each distinct CVE ID. Distinct inputs are what give the hash something to spread.

This is how you evaluate a proposed fix. If the problem is one heavily repeated value, putting the word hashed in front of the design does nothing to it. A different key, or a justified compound key, changes the granularity, but it also changes which queries can be targeted.

One last thing. We are using the hash only as a placement function, a deterministic mapping from an identifier to a bucket.

## Slide 14

Now we connect placement to queries. Suppose a future version of this collection used a hashed cveID as its shard key. Go down the left column, and for each query ask: can the router tell where to go?

Exact cveID equality. Yes. The filter carries the key value, so the router can target the relevant shard. That is a great fit if the main job is looking up one known vulnerability.

Only vendorProject equals Microsoft. The filter does not contain the shard key, so the router cannot narrow it down. The same goes for only a dateAdded window. The database can still answer both, but the work may have to go to several shards.

Count every record by vendor. This query needs data from every shard.

Read the first line under the table, because it trips people up. A local index on vendor can reduce the work inside each shard. The router uses the shard key to choose which shards to contact. Indexing and targeting solve related but different problems.

Choose a key that suits the queries people run most often. A key that is excellent for exact-ID lookups can be weak for date ranges. In your lab recommendation, name that tradeoff.

Sources:
https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/
https://www.mongodb.com/docs/manual/core/hashed-sharding/

## Slide 15

Capacity planning also means projecting storage, and a projection is only useful if you can see its assumptions. They are all in this table.

We start with one hundred mebibytes retained. We add twenty mebibytes a day. We look thirty days ahead. Twenty times thirty is six hundred. Add the starting hundred, and we have seven hundred. Then we apply an assumed overhead multiplier of two, and we get the equation on the slide: fourteen hundred mebibytes.

Read the line under the equation. The multiplier is an assumption for this scenario. Estimate space for indexes, replicas, backups, and temporary files from provider settings and workload measurements.

Why write it out this way? Because every piece is something someone can question. If records expire after seven days, adding thirty days of arrivals and never subtracting departures overstates what you keep. If documents get bigger over time, a constant twenty a day understates it. Change the retention policy and the whole projection changes.

Units matter too. A mebibyte is 1,048,576 bytes. A megabyte is 1,000,000 bytes. A provider's quota and your local size report may not use the same one.

For a real plan, you would measure actual record and index sizes, set the retention policy, and compare your estimate with observed growth. The equation just makes the assumptions visible enough to argue about and revise.

## Slide 16

Discord's 2023 engineering account describes message-storage growth, hot partitions, a data-service layer, and migration from Cassandra to ScyllaDB. Measure distribution and access patterns before selecting infrastructure, then verify the migrated values against the source. A data engineer should report the import key, repeat behavior, field checks, and remaining limits.

For this class, connect the case to the experiment already on the screen. Use this case to interpret your own measurements. Keep classroom results separate from the company’s production system.

Source: https://discord.com/blog/how-discord-stores-trillions-of-messages

## Slide 17

Use the guided inspection to prepare for the lab. In this single Thanksgiving-week meeting, Cells 03–07 prepare the import we will run today.

Keep the retained historical snapshot so the counts match the slides. Cell 06 measures distinct values and repeated values. Compare cveID and dateAdded using the displayed measurements. Cell 07 then places the same records into four teaching buckets under two simplified rules. Run the simulation in Python. The exact slide 12 result is fifteen later records in the last date bucket and three, three, six, three under the displayed hash rule.

Explain how the candidate key would distribute writes and help the router find records. Keep this evidence in the same saved notebook. Continue directly to the Atlas connection; the twenty-minute individual lab comes after guided setup, import, and verification.

## Slide 18

We now move from measuring the source to importing it. Continue with the next part of the class. A scheduled refresh or retry must have an intentional result.

We match each record by its stable cveID. If that value already exists, replace its source fields; if it does not, insert it. Repeating the unchanged source should leave the same logical records and values. That property is idempotency: repeating an operation has the same final effect as doing it once, for the stated input and conditions.

Our required path uses real Atlas. We will import twice into the same collection, compare all seventy-five documents and their field types with the source, and check the grouped result independently. SQLite and PostgreSQL remain available for later practice.

## Slide 19

Cell 08 sets TARGET to atlas for today's required lesson. Python runs in Colab; MongoDB runs in Atlas; PyMongo is the driver that sends the requests between them. SQLite and PostgreSQL remain optional reference paths in this notebook.

Run Cell 08 once. It chooses the database cst4714_week13 and a collection name beginning kev_ followed by twelve random hexadecimal characters. The database is fixed so your database user only needs readWrite on that teaching database. The collection name isolates your run.

Then run Cell 10 to connect. Run Cell 11 twice without rerunning Cell 08 or changing collection names. If every import starts with a fresh collection, the second import never meets the first import's records. Keep the same collection on the second import to test repeat behavior.

Use an existing Free cluster and a database user prepared before class. Authenticate Python with a database user. If access is blocked, label the instructor's demonstrated evidence as observed and complete the same notebook when you can connect.

## Slide 20

The source is JSON, but every database still needs a decision about how to store each field. Read the table row by row.

cveID becomes a text primary key in SQLite and PostgreSQL. In MongoDB, we create a unique index on cveID. The catalog provides the CVE ID before MongoDB creates a document. A repeat import has to match on the identifier the source gives us.

dateAdded is a calendar day with no time. SQLite stores the year-month-day text. MongoDB keeps the same string in this lesson. PostgreSQL uses a real date type.

cwes is the list. SQLite gets it as JSON text. MongoDB gets a real array. PostgreSQL gets a jsonb array. In every case it stays a list. We never glue the entries into a comma-separated label that someone has to parse later.

Then the last lines. When we verify, we convert back. A PostgreSQL date object and the string 2026-07-10 are different Python values, even though they mean the same day. So the check converts dates and JSON text back to the source form first, and only then compares. A field's name alone never tells you its type or how it round-trips.

## Slide 21

Run Cell 10 after Cell 08. Atlas checks the address of the computer making the request. Colab's Python runs on a remote computer. Its network address can therefore be different.

Cell 10 prints that runtime's public IPv4 address with slash thirty-two. That means one address. Add this temporary entry to Atlas Network Access, choose a short expiration when available, wait for it to become active, and return to the notebook's confirmation prompt. Use the /32 address printed by Colab to allow this runtime. A new runtime may need a new entry.

Get the Python Drivers URI from your own Free cluster. Use a database user with readWrite on cst4714_week13. Put the completed URI in a Colab Secret named MONGODB_URI or the hidden prompt. Never paste it into a saved code cell, screenshot, or notebook output.

The redacted screenshot shows the Atlas interface on August 25. The code's ping and later write/read are our evidence. Remove the temporary runtime rule from Atlas when you finish.

Source: https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 22

This is an excerpt of Cell 10, after the hidden URI input. MongoClient creates the driver client. TLS encrypts the connection; keeping tlsInsecure False preserves the certificate and hostname checks that help identify the server. Do not disable those checks to work around a connection error.

The stable API setting requests version one. The two ten-thousand-millisecond settings bound server selection and client operations to about ten seconds each; the pause for your input and package setup take additional time.

Ping sends a request to the server. After ping, the full cell selects the fixed teaching database and this run's collection, checks that it is empty, and creates a unique cveID index. Cell 11 writes the records.

The collection requests majority writes and majority reads from the primary. If a write times out, inspect and verify the collection before deciding what happened; the stable-key import can be retried.

If setup fails, check the database user and role, completed Drivers URI, active runtime rule, deployment readiness, DNS name lookup, and TLS secure connection. Do not display the secret while diagnosing. The cell closes a failed client and displays the error category.

Sources: https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/ ; https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/server-selection/

## Slide 23

Optional reference: skip this slide in the required Thanksgiving-week route.

If you pick postgres with Supabase, this is where you get the connection details. Read the box at the top right: Connect, then Session pooler.

Why the session pooler? A notebook network like Colab may not be able to reach the direct IPv6 endpoint. The shared session pooler supports IPv4, so it works from the notebook. Copy the exact pooler username shown for your project. Do not guess it from an example.

The middle box is the one people confuse. You need the database password. Use the database user's password. Those are different credentials for different jobs.

Now the SSL box. sslmode equals require gives you encryption. verify-full also checks that the server is who it claims to be, when you configure it with the provider's certificate authority. Those are different layers. If the IPv6 address is unreachable, turning off encryption does not help, because encryption was never the problem.

The screenshot is a redacted overview from August 25, 2026. The image marks the Connect button.

The code makes a uniquely named practice schema, so your table does not collide with a real one, and it clears the connection URL after the attempt. If it fails, check network reachability, credentials, project availability, the SSL settings, and permission to create the schema. SQLite is available for later practice.

Sources:
https://supabase.com/docs/guides/database/connecting-to-postgres
https://www.postgresql.org/docs/current/libpq-ssl.html

## Slide 24

Optional reference: skip this slide in the required Thanksgiving-week route.

After the PostgreSQL import, this code reads one known record back. Two things get substituted into SQL here, and they use two different tools. That is the point of the slide.

The outer with block opens a transaction. Inside it, a cursor sends commands and reads results.

The first execute sets the search path to our practice schema. SET LOCAL means the change lasts only until this transaction ends, so it cannot quietly leak into the next thing the notebook does. Look at how the schema name gets in: sql.Identifier. A schema name is an identifier, and Identifier quotes it correctly as a name.

The second execute is the read. The CVE ID goes in through percent s, and the actual value travels separately, in the tuple. Bind the ID as a parameter. The driver sends it apart from the SQL text, so it can never be read as SQL code.

Look at the comma after known_id. That comma is what makes it a one-element tuple. Parentheses alone do not.

fetchone returns the row, or None if nothing matched. The full verification checks for None before reading any fields.

Two rules to take away. Never paste input straight into a SQL string. And never try to use percent s for a schema or column name. Names and values sit in different places in SQL, and the driver gives you a different tool for each.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html
https://www.psycopg.org/psycopg3/docs/basic/params.html

## Slide 25

This table is the repeat-run test, and only one row of it is the real test. Read all three.

Row one, the first import. The practice table or collection starts at zero and ends at seventy-five. Good, but that only tells us the first load worked. It says nothing about the second.

Row two. Same source, same target, and we run only the import cell again. Seventy-five before, seventy-five after. The second import matched the seventy-five existing identifiers. That is the test.

Row three is the trap. If you reset setup before every import, every run starts at zero and ends at seventy-five. That looks repeatable. But you never made the program collide with its own earlier output. You just tested a fresh database twice. That is why the box at the bottom says only the second row counts.

Then read the last line. Equal counts can hide changes. A program could overwrite a title with the wrong text, replace the wrong record, or store a broken list, and the total would still be seventy-five. So the notebook also compares stored values with the source and checks the grouped query independently.

For our unchanged source, idempotent means running it again leaves the same logical records and values.

## Slide 26

This retained diagram shows the evidence we want: zero records, then seventy-five after the first import, then seventy-five after the second import. For today's Atlas path, run Cell 08 once, connect in Cell 10, and run Cell 11 twice in the same collection. The stable source field is cveID. The small SQL cve_id label in the diagram is only the optional SQL paths' name for that same identifier; Atlas keeps cveID.

The first import inserts seventy-five documents. The repeated import inserts zero and matches seventy-five existing identifiers. Read the modified counter from your own output. In our real local MongoDB test it reported seventy-five on the repeat even though the complete selected values and types matched. Idempotency here means rerunning the import preserves the same logical records and values. Preserve both count pairs in the printed history.

Then Cell 14 compares every selected value and type of all seventy-five stored documents with the checked source. Cell 15 checks the grouping against a separate Python count.

## Slide 27

Here is the MongoDB version of the repeat import. Read the loop. For each record, replace_one looks for a document whose cveID matches this record's cveID. If it finds one, it replaces it with the source record. upsert equals True means that if nothing matches, it inserts the record instead. Match or insert, in one call.

Why does this survive a rerun? Because the match is on the business identifier, and a unique index on cveID enforces one document per identifier. Without that stable match, a retry would create a second copy, and MongoDB would happily give it its own new internal identifier. Two documents, one vulnerability.

The SQL paths do the same thing in SQL. Their import uses INSERT with ON CONFLICT on cve_id DO UPDATE, setting each column from excluded, which is the row that was just proposed. Match on the identifier and update the existing record.

Replacing the whole document is a deliberate choice here. This is a disposable import collection, and the source is authoritative, so a replace even repairs a value someone changed. But if an application stored its own notes on these documents, a full replace would erase them. That application would need a different update design.

Read the line at the bottom. This loop only touches IDs that are in the source.

Sources:
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/

## Slide 28

Two words that sound similar and answer different questions. Read the box at the bottom. Atomicity defines which changes succeed together. Idempotency defines what happens when you repeat the operation. A good import can have one without the other.

The table asks a question: something fails on the fourth write, so what happens to the first three?

In the SQL paths, the notebook wraps the batch in a transaction. Say the fourth row breaks a constraint. The transaction rolls back, and the first three writes go with it. You never get a half-applied batch. Anything committed before that transaction is outside the rollback, of course.

The MongoDB loop is different. Each replace_one is its own write, and each one is atomic for its one document. If the fourth call fails, the first three replacements are already done, and they stay.

Is that a disaster? Look at the third row. Rerun the unchanged source, and the stable IDs let the import match what is already there and finish the rest. That is idempotency doing its job. You still verify afterward, and a real retry policy would need more thought about changing sources, other writers, or a record that is permanently malformed.

And to be fair, MongoDB does support transactions in suitable deployments. Trace the code on the previous slide. Always find the real unit of success in the program you actually run.

Sources:
https://www.psycopg.org/psycopg3/docs/basic/transactions.html
https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 29

Trace the hypothetical change in the example. Suppose somebody changes only the vulnerability title of the first source record. The collection still has seventy-five documents. That CVE ID still exists. Vendor totals still match. All three checks can pass while a title is wrong.

Cell 14 independently reads back every document, leaving out only MongoDB's generated _id, sorts by cveID, and compares the result with the checked source. It also checks the seven string fields and the cwes array of strings. The known first record is printed separately so you can inspect a concrete example. Cell 14 checks all seventy-five stored records against their sources.

This model stores each calendar date as a YYYY-MM-DD string. Store cwes as a list.

Rerunning the unchanged import would repair source-controlled values, because the source is authoritative for this disposable collection. The passing check confirms the imported records and types match this snapshot.

## Slide 30

Two grouped results from the same selected records, answering two different questions. Look at the left table first, grouped by vendor label: Microsoft sixteen, Cisco seven, SimpleHelp with a trailing space three, Ubiquiti three, Adobe two. Now the right table, grouped by product label: Catalyst SD-WAN Manager four, Windows four, Defender three, SimpleHelp three, UniFi OS three.

Be careful about what the number counts. It counts selected catalog entries. Windows four means four entries in this subset have the product label Windows. That is all it means, and your write-up should say so.

Now look at the ties. Windows and Catalyst SD-WAN Manager both have four. Which comes first? The code sorts by count, highest first, and breaks ties by the label. Why define that? Because the notebook compares the database result with a result it computes straight from the source. Without a fixed tie order, two correct answers could print equal rows in different orders and look like a mismatch.

The quotation marks around the vendor SimpleHelp are there to show you the trailing space. The stored label is exactly what the source wrote. The product label SimpleHelp does not have that space.

In the lab, run the vendor grouping first, change GROUP_FIELD to product, rerun, and explain one row in terms of products. The question changes along with the code.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 31

Optional reference: skip this slide in the required Thanksgiving-week route.

So how does changing GROUP_FIELD actually reach the SQL? This slide answers that, and it connects back to slide 24.

Read the code. GROUP_FIELD is set to product. allowed_columns is a small dictionary with exactly two entries. vendorProject maps to the column vendor_project, and product maps to product. The next line looks up the column name. The full cell rejects any choice outside those two entries, so a misspelling or something malicious stops right there. Only those two names can ever reach the SQL.

Then, in the PostgreSQL path, sql.Identifier quotes the chosen column as a name. The SQLite path builds its SQL from the same restricted mapping.

Why not just use percent s, like we did for the CVE ID? Read the last line. A percent s placeholder binds a value. It can say "where cve_id equals this." It cannot say "group by this column," because the SQL parser treats names and values as different things.

This is also good interface design. You get one small decision you can change without touching the connection or import code.

On the Atlas path, the same choice becomes a field expression, dollar product, in the aggregation pipeline. Different syntax, same question. After the change, the notebook computes the expected grouping directly from the source and compares it with the database output, tie order included.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html

## Slide 32

This is the twenty-minute individual lab, after the guided Atlas connection, both imports, full verification, and vendor query. Stay in the same notebook and collection. In Cell 15, change GROUP_FIELD from vendorProject to product, run that cell, and confirm that the five groups match the independently counted source. Do not rerun Cell 08 and do not switch providers.

Read one row as a sentence. Windows appears in four entries in the selected catalog sample. The same seventy-five records now answer a different question.

Write five to seven sentences in Submission Record. Include the historical source and your question, the CVE-ID and date measurements, the same-collection repeat result, one changed product row, independent verification, and a limitation. Write the handoff using the evidence saved in your notebook.

Save your own Drive copy with code, outputs, and the handoff. Give the instructor viewer access and submit that viewable Colab sharing link in Brightspace. If you only observed the instructor's real Atlas demonstration, label that honestly and finish the same notebook under the existing deadline.

Retain evidence before any optional cleanup. The final cleanup cell defaults to off so it cannot erase the collection while you are still querying it.

## Slide 33

Cleanup is optional after both grouped queries, verification, and the saved handoff. Cell 16 starts with RUN_CLEANUP False. Leaving it there keeps your practice collection for now. Do not run cleanup before completing the evidence.

If you deliberately set it True, the Atlas branch removes only the named kev_ collection created by this run from cst4714_week13, then closes the client. The temporary runtime slash-thirty-two rule is separate; remove it in Atlas when no longer needed or let its intended expiration end it.

The other table rows describe optional SQLite and PostgreSQL paths. SQLite closes its in-memory database. PostgreSQL removes its practice table and only removes the schema if it is empty; no CASCADE is used.

Deleting practice data, closing a driver, revoking network access, and stopping hosted infrastructure are different actions. Closing a client does not pause the service or remove a network rule. Save your notebook outputs first and remove only objects you can identify as belonging to your own run.

## Slide 34

Here is a precise way to describe the work: I imported a documented historical source into real Atlas, used a stable identifier to repeat the import without duplicating records, and checked stored values, types, and a grouped result against the source.

Make the claim match what you actually did. If you only observed the instructor's Atlas run, say so. The four-bucket Python simulation shows how the two keys distribute incoming records. Seventy-five records do not establish that this workload needs sharding.

For the existing final project, discuss one source, one important query, and evidence that would justify a capacity change. Keep the requirements and deadlines on the existing project page.

The next week examines applications with more than one data store. Stable identifiers, repeat behavior, and verification will help us explain why stored copies disagree. Today ends with one saved, viewable Colab link.

## Slide 35

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Capacity: measure before you scale (1:17); Shard keys: distribution and targeting (1:37); A repeatable Python import (1:28). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 13 README. The diagrams illustrate the design.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
