# Week 13: Capacity, Sharding, and Python Integration - Spoken Transcript

## Slide 1

Welcome to Week 13. The case is in the two lines on the slide. A public dataset becomes a database, and the next import arrives tomorrow. That second line is the whole week.

Picture a colleague who asks you to build a small catalog app. The first import works. Tomorrow the source publishes an update, and your colleague runs the same program again. Now what? If the program just appends every row, you get duplicates. If it wipes the database and reloads, it can erase something somebody else added. Neither should happen by accident. So before we write any import, we need to know how to identify a record, where the data came from, and what a second run is supposed to do.

Our data is a historical subset of CISA's Known Exploited Vulnerabilities catalog. We are reading records about vulnerabilities. We are not downloading vulnerable software or testing anybody's system. And the same decisions apply to transit data, museum collections, or product catalogs.

Day 1 is about measuring key choices and running a small distribution experiment in Python. Day 2 is a repeatable import with a checked result. SQLite gives everyone a working path. Atlas and PostgreSQL are optional. On our calendar this is Thanksgiving week, so if we only have one meeting, we do the core of both parts together, with SQLite. Either way, it all goes into one individual notebook, with no separate report.

## Slide 2

Before anybody says the word sharding, we need a workload we can actually describe. Look at the four rows on the slide.

Latency is how long one request takes. A lookup that starts now and finishes eighty milliseconds later has a latency of eighty milliseconds. Throughput is how much work finishes in an interval, like requests per second. Why keep them apart? Because a system can push a lot of requests per second while some individual users still wait a long time. Those are different complaints with different fixes.

The working set is the data and index pages the workload touches again and again. That is what needs to stay close at hand to be fast. A huge archive can have a tiny working set, and a small database can keep the disk busy if its common queries touch pages all over the place. You only learn that by watching the actual access pattern, not by checking the total size.

The growth horizon is how far ahead you are projecting. Planning for tomorrow and planning for a year need different assumptions about retention and incoming data.

Now read the line at the bottom. Our catalog could feed a daily report and an interactive lookup. The report scans lots of records once a day. The lookup might fetch one ID thousands of times. Same records, completely different capacity needs. The size of the database tells you none of that.

## Slide 3

Here is why I never trust an average by itself. This is a complete little Python calculation, and the numbers are invented on purpose. Read the note under the code: it is a synthetic twenty-request trace, not a measurement of Atlas, Supabase, or our dataset.

The second line builds the list. Twenty times eighteen means eighteen requests at twenty milliseconds, then one at five hundred and one at one thousand. We sort it. Add everything up and you get eighteen hundred sixty milliseconds. Divide by twenty, and the mean is ninety-three milliseconds. Sounds fine.

Now the ninety-fifth percentile, using nearest rank. Twenty times zero point nine five is nineteen, and the ceiling keeps it at rank nineteen. Python counts from zero, so the code subtracts one and reads position eighteen of the sorted list. Five hundred milliseconds.

Run it, and it prints ninety-three point zero and five hundred. Same data, two very different stories. The average says everything is quick. The p95 says one request in twenty waits half a second. And the slowest request took a full second. That slow tail is what people actually complain about, and the mean smoothed it away.

Two cautions. Percentile conventions differ, especially with small samples, so always say which one you used. And twenty fake requests cannot set a service-level objective. They just make the difference between an average and a tail concrete.

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

Second row. Three shards with a balanced split. Now each shard owns about twenty-five of the seventy-five. That is division of ownership, not copying. The collection still has seventy-five logical records. We did not make three separate catalogs. A router presents the pieces as one collection.

Third row, and people forget this one. Each shard has its own replicas. Splitting the data does not remove the need to protect each piece from a member failure. The first shard's replicas copy the first shard's portion, and so on.

Now read the warning under the table. The even split is an illustration, not a guarantee. Real placement depends on keys, sizes, ranges, and balancing. And equal record counts do not mean equal work. One shard might own the records that get almost every request.

The mistake this slide prevents is counting replicas as extra write capacity for the same data. Three copies of the same records are protection, not three times the room to write them.

Sources:
https://www.mongodb.com/docs/manual/sharding/

## Slide 6

Here is what is actually inside a sharded MongoDB cluster. Follow the boxes from the top.

The application does not talk to the shards directly. It connects to mongos, the query router. Why put a router in the middle? So the application never has to know which machine holds which record. The router figures that out, sends the work where it needs to go, and merges the answers.

How does it figure it out? The config servers. They hold the cluster metadata, including how the data is currently distributed. Because placement is described there, it can change without anybody rewriting application code. That is a different job from the shards, which store the application's data.

Then Shard A and Shard B. Each holds a portion of the data, and each one is a replica set protecting its own portion.

Read the line at the bottom, because it ties this to the rest of the day. The shard key decides distribution, and it decides whether a query can be sent to a limited set of shards. An exact lookup that includes the shard key value can be targeted. A query without that information may need work on several shards, and the application still sees one result.

We are not deploying any of this. Atlas Free does not give us a sharded cluster for this exercise. Our Python experiment models a small piece of placement instead, so we can reason about it without paying for anything.

Sources:
https://www.mongodb.com/docs/manual/sharding/
https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/

## Slide 7

Now our actual data. This is the CISA Known Exploited Vulnerabilities catalog. Our classroom fixture has seventy-five records selected from the catalog version dated July 10, 2026, and we retrieved it on July 13, 2026. Notice those are two different dates. One is when the source says its version was published. The other is when we got our copy. Keep both, because they answer different questions.

Look at the record on the left. The cveID, CVE-2026-56291, is a stable identifier. That is what will let us recognize the same record the next time we import. Vendor and product, Balbooa and Forms, are descriptive labels. And dateAdded is the date this record entered the catalog. It is not when someone discovered the weakness, exploited it, or installed the software. Field names can tempt you into claims the data does not support.

The cwes field is a list, in square brackets. One vulnerability can carry more than one weakness identifier, and a list holds that without inventing a comma convention inside a string. We will keep it a list in every database.

Read the note at the bottom. Seventy-five records are enough to check every calculation by hand. They are not a random sample, and they are not the current catalog. A vendor count in this subset says nothing about a vendor's overall security or how many computers are affected.

Sources:
https://github.com/cisagov/kev-data
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 8

A JSON file that parses is not the same as data you can trust. Parsing only proves the text follows JSON syntax. It does not prove an ID is present, a date is real, or a field has the type your model expects. So the notebook runs the checks in this table before it opens any import path. Let's go down the left column.

A missing vendor, ID, or required text field stops the import before anything loads. IDs also have to look like CVE identifiers.

February 30, 2026 fails because that day does not exist. The compact form, 20260201, fails too, even though a library could probably guess what it means. Why reject it? Because we want one canonical year-month-day form, and later our date ordering depends on it.

A repeated CVE identifier stops everything. Which record is the real one? If the code silently kept whichever came last, it would hide a conflict in the source. So the notebook makes us decide.

If cwes arrives as text instead of a list, that is rejected. And an empty list stays empty. We do not invent a weakness to fill it.

Last row. One vendor label is SimpleHelp with a trailing space. The notebook shows you the space and keeps the label as the source wrote it. Trimming might be right later, but it changes grouping, so we would document and test it, not do it quietly.

## Slide 9

Before we measure the real dataset, here is a tiny made-up one, because two ideas get confused all the time. Cardinality counts how many distinct values a field has. Frequency counts how often each value repeats.

Look at the first row. Eight tickets, six open and two resolved. The status field has cardinality two. Its most common value, open, covers six of eight records, seventy-five percent. Now imagine we place records by status. All six open tickets have the same key, so they land together. Adding machines cannot help, because you cannot split identical values.

Second row. Give each ticket its own ID. Cardinality eight, and each value appears once, so the largest share is one in eight, twelve point five percent. That is a much finer way to spread records.

But read the line in the middle of the slide. A unique ID distributes records finely, but one ID can still receive most reads. Suppose everyone keeps opening the same ticket. The stored records are perfectly spread, and the traffic is all on one.

That is the line at the bottom. Record frequency and request frequency are different measurements. Our notebook measures records in a fixture. We have no production request log. So we can describe a candidate key's properties and its risks, but we cannot say anything about real user demand from uniqueness alone. Keep that boundary in mind when you write your recommendation.

## Slide 10

Now the real measurements, from the seventy-five-record snapshot. Four candidate keys. Read across each row.

cveID has seventy-five distinct values, each appearing once, so the largest share is one point three three percent. That makes it the right field for identifying one record and matching it on a repeat import.

dateAdded has thirty-eight distinct values. The most common date appears eight times, ten point six seven percent. Dates are good for time questions, but repeated dates, and the fact that new dates keep arriving, matter for placement. That is the next slide.

vendorProject has forty-two distinct labels, and the biggest, Microsoft, appears sixteen times, twenty-one point three three percent. Combine vendor and product and you get fifty-six distinct pairs, and the largest pair repeats only four times, five point three three percent.

So do we just pick whichever has the most distinct values? No. More distinct combinations do not make a correct shard key. What matters is which values your queries supply and which records get read or written together.

One practical note for the lab. Your notebook prints the distinct count, a ratio, and the largest value share. The largest value count column is on this slide to make the percentages concrete, so do not go looking for it in your output.

And read the note at the bottom. These numbers describe this selected dataset. They are not traffic or latency, and nothing here shows a bottleneck.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 11

Now a small experiment about time-based keys. A ranged rule keeps nearby key values together. That sounds good, and it is good for date-window queries. Watch what it does to new writes.

We sort the records by dateAdded. The oldest sixty records set the boundaries, and then we freeze them. The newest fifteen play the role of later writes arriving into those fixed ranges.

The boundaries in this fixture are April 22, May 20, and June 1, 2026. Read the table. Bucket zero is before April 22. Bucket one is April 22 through May 19. Bucket two is May 20 through May 31. Bucket three is June 1 onward, with no upper end.

The notebook uses bisect_right, which counts how many boundaries a date has reached or passed. That works on plain strings only because every date is in the canonical year-month-day form, so string order matches calendar order. That is why the checks on slide 8 rejected compact dates.

Now the last line in the box. All fifteen later records land in bucket three. Of course they do. Dates keep increasing, and the top range is the only open-ended one. In a real cluster, that pattern puts the new writes in one place while the older ranges sit quiet.

What we left out on purpose is balancing and migration. Real MongoDB moves ranges around. And our ordering comes from catalog dates, not real arrival times. This isolates one mechanism. It is not a cluster benchmark.

## Slide 12

Same fifteen later records, two placement rules, side by side.

The gray bars are the fixed date ranges from the last slide. All fifteen sit in bucket three. The green bars are the hash rule. We hash each CVE identifier with SHA-256 and take the remainder after dividing by four. Look at the green bars: three in bucket zero, three in bucket one, six in bucket two, three in bucket three.

Do a quick check with me. Three plus three plus six plus three is fifteen. The gray series is fifteen too. Why bother adding them up? Because a comparison that silently dropped records could look like better distribution for a bad reason. Always check that both sides account for every row.

Notice that hashing did not produce a perfect split. Six in one bucket and three in the others is completely normal with only fifteen records. And we gave something up. Under the hash rule, two dates next to each other on the calendar no longer land next to each other.

Read the scope note above the chart. This is our own SHA-256 with four teaching buckets. MongoDB has its own hashing and range management, so this is a transparent illustration, not a copy of MongoDB's internals. There is no latency, size, or balancing cost in this chart. We can say the two rules placed these records differently. We cannot say the green rule makes every query faster.

Sources:
course/notebooks/06_public_data_capacity_integration.ipynb

## Slide 13

Here is a property of hashing that people forget when they say "just hash it." Hashing is deterministic. Same input, same algorithm, same output, every time.

Read the code. We take the string Microsoft, encode it to bytes, compute its SHA-256 digest in hexadecimal, turn that into an integer, and take the remainder after dividing by four. Run it, and it prints one. Bucket one.

Now run it again. Still one. Run it sixteen times, once for each Microsoft record in our fixture, and you get bucket one sixteen times. Hashing does not turn repeated values into different values. If vendor were our key, all sixteen Microsoft records would land together, hashed or not.

So why did the previous slide spread out? Read the last line on the slide. The notebook hashes CVE identifiers, not vendor labels, and the identifiers are all distinct. Distinct inputs are what give the hash something to spread.

This is how you evaluate a proposed fix. If the problem is one heavily repeated value, putting the word hashed in front of the design does nothing to it. A different key, or a justified compound key, changes the granularity, but it also changes which queries can be targeted.

One last thing. We are using the hash only as a placement function, a deterministic mapping from an identifier to a bucket. It is not encryption, it does not hide the vendor name, and it does not authenticate anything.

## Slide 14

Now we connect placement to queries. Suppose a future version of this collection used a hashed cveID as its shard key. Go down the left column, and for each query ask: can the router tell where to go?

Exact cveID equality. Yes. The filter carries the key value, so the router can target the relevant shard. That is a great fit if the main job is looking up one known vulnerability.

Only vendorProject equals Microsoft. The filter does not contain the shard key, so the router cannot narrow it down. The same goes for only a dateAdded window. The database can still answer both, but the work may have to go to several shards.

Count every record by vendor. That question needs the whole collection by definition, so going to several shards is not a mistake. It is just what the question costs. Not every multi-shard operation is a design failure.

Read the first line under the table, because it trips people up. A local index on vendor can reduce the work inside each shard. It does not tell the router which shards to skip. Indexing and targeting solve related but different problems.

So the design question is not which key has the biggest number. It is how our frequent operations match the key. A key that is excellent for exact-ID lookups can be weak for date ranges. In your lab recommendation, name that tradeoff.

Sources:
https://www.mongodb.com/docs/manual/core/sharding-choose-a-shard-key/
https://www.mongodb.com/docs/manual/core/hashed-sharding/

## Slide 15

Capacity planning also means projecting storage, and a projection is only useful if you can see its assumptions. They are all in this table.

We start with one hundred mebibytes retained. We add twenty mebibytes a day. We look thirty days ahead. Twenty times thirty is six hundred. Add the starting hundred, and we have seven hundred. Then we apply an assumed overhead multiplier of two, and we get the equation on the slide: fourteen hundred mebibytes.

Read the line under the equation. The multiplier is an assumption for this scenario. It is not a MongoDB or Supabase billing rule, and it does not tell you the real size of indexes, replicas, backups, or temporary space.

Why write it out this way? Because every piece is something someone can question. If records expire after seven days, adding thirty days of arrivals and never subtracting departures overstates what you keep. If documents get bigger over time, a constant twenty a day understates it. Change the retention policy and the whole projection changes.

Units matter too. A mebibyte is 1,048,576 bytes. A megabyte is 1,000,000 bytes. A provider's quota and your local size report may not use the same one.

For a real plan, you would measure actual record and index sizes, set the retention policy, and compare your estimate with observed growth. The equation just makes the assumptions visible enough to argue about and revise.

## Slide 16

Time for Part 1 of the lab. Work individually in Notebook 06, and start from the embedded snapshot. Why the snapshot and not the live feed? Because then your numbers match the ones on these slides, and we can check each other's results.

Run Sections 1 and 2. They inspect the source, check the fields, measure the candidate keys, and run the range and hash comparison. Read the cells as you go. The code is part of the lesson, not a black box.

Then focus on two candidates: cveID and dateAdded. Use two numbers the notebook actually displays, for example the distinct counts and the largest value shares. Then tie them to a grouped question you want to answer, like which vendors appear most often in this subset. An exact identifier and a date window give a placement rule very different information.

Second question: does this seventy-five-record database need sharding? A well-supported no is a perfectly good answer, as long as you say what measured change would make you reconsider.

You do not need a paid cluster, a sharded deployment, or a database account for any of this. Read the box at the bottom. Save the notebook, because Part 2 continues in the same file, and there is no separate Day 1 submission. If we are doing both parts in one meeting this week, go straight on to Section 3 when you finish.

## Slide 17

Day 2 starts with the two lines on the slide. The import ran yesterday, and today it runs again. That second run is not an edge case. Retries and scheduled refreshes are an ordinary part of running any data system, so what the second run does has to be designed, not discovered.

Our design uses the stable CVE identifier to recognize a record. If that identifier is already in the database, the load updates the selected values. If it is not, the load inserts it. Run the same unchanged source again, and you should end up with the same logical records and the same values.

Now read the second box. A query and a value comparison tell us what was actually stored. Here is why that wording matters. A successful connection only proves the network and the login worked. An import count only tells you how many rows there are. Neither tells you the values are right. So we will query the database and compare a known record with the source.

SQLite runs the whole example with no remote database. If you pick Atlas or PostgreSQL, you also cross a network boundary and handle a credential, and we will look at that code directly instead of hiding it in a helper.

The written part is a short handoff in the notebook, explaining your work to an imagined colleague. It is still individual work, and still one submission.

## Slide 18

One variable controls the database path: TARGET. Look at the three rows.

sqlite is the default, and the simplest. Python already includes the SQLite driver, and the notebook builds an in-memory database inside its own process. Nothing to sign up for, nothing to download.

atlas uses PyMongo to connect to your MongoDB Atlas project. It needs a database user and an IP rule that lets the notebook runtime in. We will see why on slide 20.

postgres uses Psycopg to connect to PostgreSQL, including your Supabase project through the right connection endpoint.

You need exactly one. Connecting to a second provider does not make your repeat-run test any more complete. It is the same test.

Now the line at the bottom, which is the most important instruction of the day. Run setup once. Then repeat the import cell. Why? The setup cell creates the practice names and the connection. If you rerun setup before each import, you get a fresh, empty target every time, and the second import never meets the first import's records. You would be testing a first import twice.

And if you want to try another target, clean up this run first. The notebook actually stops you from starting another setup while one is still open. That keeps you from leaving practice objects and open connections scattered across services.

## Slide 19

The source is JSON, but every database still needs a decision about how to store each field. Read the table row by row.

cveID becomes a text primary key in SQLite and PostgreSQL. In MongoDB, we create a unique index on cveID. Why not just use MongoDB's own document identifier? Because MongoDB generates that one, and ours is the business identifier from the source. A repeat import has to match on the identifier the source gives us.

dateAdded is a calendar day with no time. SQLite stores the year-month-day text. MongoDB keeps the same string in this lesson. PostgreSQL uses a real date type. What we do not do is turn it into a timestamp at midnight. That would invent a time of day the source never gave us. That is the first line under the table.

cwes is the list. SQLite gets it as JSON text. MongoDB gets a real array. PostgreSQL gets a jsonb array. In every case it stays a list. We never glue the entries into a comma-separated label that someone has to parse later.

Then the last lines. When we verify, we convert back. A PostgreSQL date object and the string 2026-07-10 are different Python values, even though they mean the same day. So the check converts dates and JSON text back to the source form first, and only then compares. A field's name alone never tells you its type or how it round-trips.

## Slide 20

If you choose Atlas, this is the step that trips everyone up. Atlas checks the network address of whatever connects to it. In Colab, your Python code is not running on your laptop. It runs on a remote notebook machine, and that machine has a different public address from the laptop running your browser.

So the notebook looks up its own runtime's public IPv4 address and prints it with slash thirty-two on the end. Slash thirty-two means exactly one address. Add that to your Atlas IP access list, with an expiration if the dashboard offers one. Wait until the rule is active. Then go back and answer the notebook's confirmation prompt.

Read the note at the bottom. The Add Current IP button adds the browser's address, which is your laptop. Use that alone, and Colab still cannot connect. And if Colab gives you a new runtime, check the address again. Yesterday's rule may not match.

The screenshot is a redacted Atlas interface from August 25, 2026. It shows you where Connect, Database, and Network Access are. It is not proof of a connection from your notebook. Under Connect, then Drivers, you get the Python URI format. Use a database user's password, not your Atlas website password.

Keep that credential in the hidden prompt, never in a code cell, screenshot, or submission. And after class, delete the runtime rule. Closing Python does not remove it.

Sources:
https://www.mongodb.com/docs/atlas/security/ip-access-list/

## Slide 21

Here is the actual connection code, shown in the open instead of buried in a helper. Read it line by line.

MongoClient gets atlas_uri, which came from the hidden prompt. tls equals True turns on encryption. tlsInsecure equals False keeps the certificate and hostname checks on. Why spell that out? Because the classic shortcut when a connection fails is to turn those checks off, and then you have an encrypted connection to a server you never verified.

server_api asks for the stable API, version one, in strict mode. The two timeouts, serverSelectionTimeoutMS and timeoutMS, are both ten thousand milliseconds, which is ten seconds. Without them, a bad connection attempt can just hang, and you never find out why.

Then the last line, ping. Creating a client object does not prove anything, because PyMongo can create a client before it ever talks to a server. The ping is a real request. If it succeeds, the client can reach the deployment.

Read the box at the bottom. A ping does not load or verify a dataset. That comes later, with its own checks. The full cell also validates the URI, closes a failed client, and clears the URI variable.

If it fails, go through the layers: the database user, a percent-encoded password, the active runtime IP rule, the cluster being up, DNS, and TLS. Do not fix it by disabling TLS checks. That weakens the connection and explains nothing.

Sources:
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/security/tls/
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/connect/connection-options/server-selection/

## Slide 22

If you pick postgres with Supabase, this is where you get the connection details. Read the box at the top right: Connect, then Session pooler.

Why the session pooler? A notebook network like Colab may not be able to reach the direct IPv6 endpoint. The shared session pooler supports IPv4, so it works from the notebook. Copy the exact pooler username shown for your project. Do not guess it from an example.

The middle box is the one people confuse. You need the database password. Not the password you use to sign into the Supabase website, and not an API key. Those are different credentials for different jobs.

Now the SSL box. sslmode equals require gives you encryption. verify-full also checks that the server is who it claims to be, when you configure it with the provider's certificate authority. Those are different layers. If the IPv6 address is unreachable, turning off encryption does not help, because encryption was never the problem.

The screenshot is a redacted overview from August 25, 2026. It shows where Connect is, not the dialog itself.

The code makes a uniquely named practice schema, so your table does not collide with a real one, and it clears the connection URL after the attempt. If it fails, check network reachability, credentials, project availability, the SSL settings, and permission to create the schema. And SQLite is always there to finish the required work.

Sources:
https://supabase.com/docs/guides/database/connecting-to-postgres
https://www.postgresql.org/docs/current/libpq-ssl.html

## Slide 23

After the PostgreSQL import, this code reads one known record back. Two things get substituted into SQL here, and they use two different tools. That is the point of the slide.

The outer with block opens a transaction. Inside it, a cursor sends commands and reads results.

The first execute sets the search path to our practice schema. SET LOCAL means the change lasts only until this transaction ends, so it cannot quietly leak into the next thing the notebook does. Look at how the schema name gets in: sql.Identifier. A schema name is an identifier, and Identifier quotes it correctly as a name.

The second execute is the read. The CVE ID goes in through percent s, and the actual value travels separately, in the tuple. That is a value, not a name, so it is bound as a parameter. The driver sends it apart from the SQL text, so it can never be read as SQL code.

Look at the comma after known_id. That comma is what makes it a one-element tuple. Parentheses alone do not.

fetchone returns the row, or None if nothing matched. The full verification checks for None before reading any fields.

Two rules to take away. Never paste input straight into a SQL string. And never try to use percent s for a schema or column name. Names and values sit in different places in SQL, and the driver gives you a different tool for each.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html
https://www.psycopg.org/psycopg3/docs/basic/params.html

## Slide 24

This table is the repeat-run test, and only one row of it is the real test. Read all three.

Row one, the first import. The practice table or collection starts at zero and ends at seventy-five. Good, but that only tells us the first load worked. It says nothing about the second.

Row two. Same source, same target, and we run only the import cell again. Seventy-five before, seventy-five after. The import ran into seventy-five existing identifiers and applied its conflict behavior instead of adding seventy-five more. That is the test.

Row three is the trap. If you reset setup before every import, every run starts at zero and ends at seventy-five. That looks repeatable. But you never made the program collide with its own earlier output. You just tested a fresh database twice. That is why the box at the bottom says only the second row counts.

Then read the last line. Equal counts can hide changes. A program could overwrite a title with the wrong text, replace the wrong record, or store a broken list, and the total would still be seventy-five. So the notebook also compares stored values with the source and checks the grouped query independently.

For our unchanged source, idempotent means running it again leaves the same logical records and values. It does not mean no work happens. It does not keep history, and it does not delete records a future source leaves out.

## Slide 25

Here is the MongoDB version of the repeat import. Read the loop. For each record, replace_one looks for a document whose cveID matches this record's cveID. If it finds one, it replaces it with the source record. upsert equals True means that if nothing matches, it inserts the record instead. Match or insert, in one call.

Why does this survive a rerun? Because the match is on the business identifier, and a unique index on cveID enforces one document per identifier. Without that stable match, a retry would create a second copy, and MongoDB would happily give it its own new internal identifier. Two documents, one vulnerability.

The SQL paths do the same thing in SQL. Their import uses INSERT with ON CONFLICT on cve_id DO UPDATE, setting each column from excluded, which is the row that was just proposed. Same idea: match on the identifier, and update instead of duplicating.

Replacing the whole document is a deliberate choice here. This is a disposable import collection, and the source is authoritative, so a replace even repairs a value someone changed. But if an application stored its own notes on these documents, a full replace would erase them. That application would need a different update design.

Read the line at the bottom. This loop only touches IDs that are in the source. It does not delete a record a later source drops, and it does not keep earlier versions. Those are separate requirements you would build on purpose.

Sources:
https://www.mongodb.com/docs/languages/python/pymongo-driver/current/crud/replace/

## Slide 26

Two words that sound similar and answer different questions. Read the box at the bottom. Atomicity defines which changes succeed together. Idempotency defines what happens when you repeat the operation. A good import can have one without the other.

The table asks a question: something fails on the fourth write, so what happens to the first three?

In the SQL paths, the notebook wraps the batch in a transaction. Say the fourth row breaks a constraint. The transaction rolls back, and the first three writes go with it. You never get a half-applied batch. Anything committed before that transaction is outside the rollback, of course.

The MongoDB loop is different. Each replace_one is its own write, and each one is atomic for its one document. If the fourth call fails, the first three replacements are already done, and they stay. This code does not wrap the seventy-five documents in one transaction.

Is that a disaster? Look at the third row. Rerun the unchanged source, and the stable IDs let the import match what is already there and finish the rest. That is idempotency doing its job. You still verify afterward, and a real retry policy would need more thought about changing sources, other writers, or a record that is permanently malformed.

And to be fair, MongoDB does support transactions in suitable deployments. This is about the code on the previous slide, not the product. Always find the real unit of success in the program you actually run.

Sources:
https://www.psycopg.org/psycopg3/docs/basic/transactions.html
https://www.mongodb.com/docs/manual/core/write-operations-atomicity/

## Slide 27

This slide is about checks that pass while the data is wrong. Picture this. Somebody changes the title of our known record, CVE-2026-56291, the first record in the source, to the wrong text. There is no notebook cell that does this for you. It is a scenario to reason through. Now run our checks down the table.

Record count is seventy-five. Pass. Nothing was added or removed. The known CVE identifier exists. Pass. Vendor counts match. Pass, because we changed the title, not the vendor.

Three passes, and the record is still wrong. That is the danger of checking only totals and existence.

The last row catches it. The notebook takes the known identifier from the checked source, pulls the stored record, and compares all eight selected fields. Before comparing, it normalizes representation, like PostgreSQL date objects and SQLite JSON text. For MongoDB, it leaves out the generated internal identifier, which is not part of the source. Now the title differs, and the check fails.

How do we fix it? Rerun the unchanged import. The source is authoritative, so the upsert puts the correct title back. Then rerun verification and watch it pass.

But read the last line on the slide. This compares that one known record. If a different record's title had changed, this check would miss it. One known record does not prove every untested field is correct, and the grouping check covers only the grouping.

## Slide 28

Two grouped results from the same selected records, answering two different questions. Look at the left table first, grouped by vendor label: Microsoft sixteen, Cisco seven, SimpleHelp with a trailing space three, Ubiquiti three, Adobe two. Now the right table, grouped by product label: Catalyst SD-WAN Manager four, Windows four, Defender three, SimpleHelp three, UniFi OS three.

Be careful about what the number counts. It counts selected catalog entries. Not installations, not customers, not exploit attempts, not compromised machines. Windows four means four entries in this subset have the product label Windows. That is all it means, and your write-up should say so.

Now look at the ties. Windows and Catalyst SD-WAN Manager both have four. Which comes first? The code sorts by count, highest first, and breaks ties by the label. Why define that? Because the notebook compares the database result with a result it computes straight from the source. Without a fixed tie order, two correct answers could print equal rows in different orders and look like a mismatch.

The quotation marks around the vendor SimpleHelp are there to show you the trailing space. The stored label is exactly what the source wrote. The product label SimpleHelp does not have that space.

In the lab, run the vendor grouping first, change GROUP_FIELD to product, rerun, and explain one row in terms of products. The question changes along with the code.

Sources:
course/datasets/cisa_kev_sample/kev_sample.json

## Slide 29

So how does changing GROUP_FIELD actually reach the SQL? This slide answers that, and it connects back to slide 23.

Read the code. GROUP_FIELD is set to product. allowed_columns is a small dictionary with exactly two entries. vendorProject maps to the column vendor_project, and product maps to product. The next line looks up the column name. The full cell rejects any choice outside those two entries, so a misspelling or something malicious stops right there. Only those two names can ever reach the SQL.

Then, in the PostgreSQL path, sql.Identifier quotes the chosen column as a name. The SQLite path builds its SQL from the same restricted mapping. Either way, no free text is pasted into a command.

Why not just use percent s, like we did for the CVE ID? Read the last line. A percent s placeholder binds a value. It can say "where cve_id equals this." It cannot say "group by this column," because the SQL parser treats names and values as different things.

This is also good interface design. You get one small decision you can change without touching the connection or import code.

On the Atlas path, the same choice becomes a field expression, dollar product, in the aggregation pipeline. Different syntax, same question. After the change, the notebook computes the expected grouping directly from the source and compares it with the database output, tie order included.

Sources:
https://www.psycopg.org/psycopg3/docs/api/sql.html

## Slide 30

Here is Part 2 of the lab, in the same notebook as Part 1.

Choose one target. Run its setup once. Then run its import cell twice, without rerunning setup in between. Keep the before and after counts, because that is your repeat-run evidence. Run the known-record verification and the vendor grouping. Then change GROUP_FIELD from vendorProject to product, rerun, and read one of the new rows as a sentence about the selected records. The notebook's own source comparison should agree with the database.

Then write the handoff, as if a colleague will maintain this small import tomorrow. The slide names four things: your question, two key measurements, the repeat-run result, and a limitation. The lab asks for two more, so include them: one verification result, and the changed product row as your concrete example. Add a text cell under the Submission Record heading and write it there. Use the evidence already in your notebook. You do not need to paste every output again.

The colleague is your audience, not a partner. Work individually and submit one completed notebook, 06_public_data_capacity_integration.ipynb, in Brightspace. Read the bottom box: no separate report, screenshot, matrix, or repository is required.

Before you submit, run cleanup, remove any temporary Atlas rule, and make sure no credential is saved in any cell or output.

## Slide 31

Cleanup is part of the program, not an afterthought. The rule is simple: remove what this run created, and nothing else. Read the table one row at a time.

SQLite. Closing the connection throws away the in-memory database. There is nothing else to do.

Atlas. The cleanup cell drops only this run's kev_sample collection, in this run's uniquely named database, and closes the client. Any unrelated collection stays. Then look at the third column. The temporary slash thirty-two runtime rule is a provider-side setting. The notebook cannot remove it. You do that in the Atlas dashboard.

PostgreSQL. The cell drops kev_sample, then tries to drop the practice schema only if it is empty. It deliberately does not use CASCADE. If some other table is in there, the schema stays, because destroying work we did not create is far worse than leaving an empty schema behind. Then the connection closes. And if you changed any provider-side access settings, review those yourself.

Now read the note at the bottom. Closing a client does not pause a hosted database, and it does not remove an Atlas network rule. Deleting data, revoking access, and stopping infrastructure are different operations at different layers.

Our data is public and our names are unique, but that is no excuse for broad cleanup commands. The professional habit is to know exactly what your process owns, and remove exactly that.

## Slide 32

Let's finish with how you would describe this work, say in an interview, without overstating it. The paragraph on the slide is a model. I built a small, repeatable import from a documented public source. I compared distribution keys, tested the same import twice, and checked both a query result and stored record values. I can explain which behavior I ran and which scaling claims this small dataset cannot support.

Make it true for you. If you ran SQLite, say you built and checked the local path and studied the cloud connections. If you connected to Atlas or PostgreSQL, name the network and credential decisions you handled. And do not claim a sharded deployment because you ran a four-bucket Python simulation.

A strong follow-up names the stable key, the transaction boundary, and a failure your checks can catch. For example, the row count missed a wrong title, and the known-record comparison found it. That beats saying the import worked.

For your project, look at the second box: one source, one important query, and a measured reason that would justify a capacity change. This week also has a checkpoint in the existing final-project assignment: your model, your seed data, and your first two queries. Record your progress and next step in your project package. It is not a separate submission.

Next week, an application with more than one store. Stable identifiers, repeat behavior, and verification will help us figure out why two copies disagree and how to repair them safely.

## Slide 33

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: Capacity: measure before you scale (1:17); Shard keys: distribution and targeting (1:37); A repeatable Python import (1:28). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 13 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
