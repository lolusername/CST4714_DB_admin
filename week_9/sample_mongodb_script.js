// Week 9 automation demo for mongosh
// CLI usage:
//   mongosh "mongodb+srv://<cluster>/<database>" --username <user> --file week_9/sample_mongodb_script.js
//
// MongoDB VS Code Playground usage:
//   Ensure you connected to the Atlas cluster in the left sidebar, update the `use('<db>')` line below, then Run.

// If you are using Playgrounds, uncomment and set your database explicitly:
// use('<database-name>');

const activeDb = db; // mongosh injects the currently selected database here.
const databaseName = activeDb.getName();
const connection = activeDb.getMongo();
print(`Connected to ${connection} | Database: ${databaseName}`);

const collectionName = "cap_lab_sessions";

try {
  const collectionExists =
    activeDb.getCollectionInfos({ name: collectionName }).length > 0;

  if (collectionExists) {
    print(`Dropping existing collection: ${collectionName}`);
    activeDb.getCollection(collectionName).drop();
  }

  const validator = {
    $jsonSchema: {
      bsonType: "object",
      required: ["sessionId", "status", "topics", "lastUpdated"],
      properties: {
        sessionId: {
          bsonType: "string",
          description: "Unique identifier for the run",
        },
        status: {
          enum: ["draft", "running", "complete"],
          description: "Simple lifecycle marker",
        },
        topics: {
          bsonType: "array",
          minItems: 1,
          items: { bsonType: "string" },
          description: "CAP or NoSQL concepts touched in the run",
        },
        metrics: {
          bsonType: "object",
          properties: {
            latencyMs: { bsonType: "double" },
            staleReads: { bsonType: "int" },
          },
        },
        lastUpdated: { bsonType: "date" },
      },
    },
  };

  print(`Creating collection ${collectionName} with schema validation...`);
  activeDb.createCollection(collectionName, {
    validator,
    validationLevel: "moderate",
  });

  const collection = activeDb.getCollection(collectionName);
  const now = new Date();
  collection.insertMany([
    {
      sessionId: "week9-lab-a",
      status: "complete",
      topics: ["CAP", "readConcern"],
      metrics: { latencyMs: 18.4, staleReads: 0 },
      lastUpdated: now,
    },
    {
      sessionId: "week9-lab-b",
      status: "running",
      topics: ["writeConcern", "schema"],
      metrics: { latencyMs: 26.1, staleReads: 1 },
      lastUpdated: now,
    },
  ]);
  print(`Seeded ${collection.countDocuments({})} documents.`);

  print("Creating compound index on { status: 1, lastUpdated: -1 }...");
  collection.createIndex({ status: 1, lastUpdated: -1 });

  print("Aggregation summary (average latency by status):");
  collection
    .aggregate([
      {
        $group: {
          _id: "$status",
          avgLatency: { $avg: "$metrics.latencyMs" },
          runs: { $sum: 1 },
        },
      },
      { $sort: { avgLatency: 1 } },
    ])
    .forEach((doc) => printjson(doc));

  print("Demo complete. Remember to rotate credentials when sharing scripts.");
} catch (error) {
  print("Script failed:");
  printjson(error);
  throw error;
}
