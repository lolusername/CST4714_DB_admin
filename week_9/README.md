# Week 9 – MongoDB Philosophy & CAP Trade-offs

## Student Materials
- `mongodb_cap_nosql.pptx` — slide deck outlining the CAP theorem, NoSQL model comparisons, and Atlas workflow screenshots.
- `mongodb_cap_lab.ipynb` — hands-on notebook for exploring consistency trade-offs with `pymongo`.
- `sample_mongodb_script.js` — reference automation script for seeding a collection, creating indexes, and running an aggregation with `mongosh --file`.

## Before Class
1. Make sure you can log into [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) with a project ready for the lab.
2. Install `mongosh` and confirm you can connect using your Atlas SRV connection string.
3. (Optional) Bring a laptop with Python 3.9+, `pandas`, `matplotlib`, and `pymongo` installed for the notebook exercise.

## In-Class Flow
1. **CAP Theorem Refresher:** Capture notes on how Consistency, Availability, and Partition tolerance trade-offs affect distributed databases you already know.
2. **NoSQL Model Tour:** Observe quick demos of Redis (key-value), MongoDB (document), Cassandra (column-family), and Neo4j (graph). Record one use case and sample query from each.
3. **Atlas Walkthrough:** Follow the live cluster creation steps. When prompted, create your own database user and whitelist your IP.
4. **Automation Demo:** Watch `sample_mongodb_script.js` run via `mongosh --file ...` so you can adapt it for your project data.
5. **Notebook Lab:** Use `mongodb_cap_lab.ipynb` to toggle read/write concerns, capture latency observations, and discuss why workloads may choose different settings.

## After Class Tasks
1. Export `mongodb_cap_lab.ipynb` to PDF with your observations and submit it to the LMS.
2. Fork `sample_mongodb_script.js`, adjust the schema validation, and rerun it against your own Atlas cluster; document any issues you hit.
3. Review the MongoDB University module on schema patterns to prepare for the Week 10 indexing deep dive.

## Helpful Commands
```bash
# Run the automation script (replace placeholders)
mongosh "mongodb+srv://<cluster>/<database>" --username <user> --file week_9/sample_mongodb_script.js

# Optional: install notebook dependencies from inside Jupyter
%pip install pymongo matplotlib pandas
```

## External Resources
- MongoDB University: [Schema Design Patterns & Anti-Patterns](https://learn.mongodb.com/learn/course/schema-design-patterns-and-antipatterns/schema-design-patterns-and-anti-patterns/apply-schema-design-patterns)
- MongoDB Manual: [Read Concern](https://www.mongodb.com/docs/manual/reference/read-concern/), [Write Concern](https://www.mongodb.com/docs/manual/reference/write-concern/)
- Redis Docs: [Data Types Overview](https://redis.io/docs/latest/develop/data-types/)
- Apache Cassandra: [Data Modeling Guide](https://cassandra.apache.org/doc/latest/cassandra/data_modeling/)
- Neo4j: [Cypher Query Language Basics](https://neo4j.com/docs/getting-started/current/cypher-intro/)
