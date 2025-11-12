/**
 * Mongo Playground Mini-Sprint — Seed + Practice Queries
 * Copy this file into mongoplayground.com (or mongosh) and run it top-to-bottom,
 * or execute each section individually as you discuss results in class.
 */

db = db.getSiblingDB("labWeek12");
const orders = db.orders;

// Reset the collection so each student starts from the same snapshot.
orders.drop();

orders.insertMany([
  {
    _id: 1001,
    customer: { name: "Chai & Co", tier: "gold" },
    status: "shipped",
    total: 180,
    placedAt: ISODate("2024-10-01T12:10:00Z"),
    lineItems: [
      { sku: "sensor-100", qty: 2, price: 60 },
      { sku: "gateway-01", qty: 1, price: 60 }
    ],
    tags: ["iot", "priority"]
  },
  {
    _id: 1002,
    customer: { name: "Byte Bazaar", tier: "silver" },
    status: "processing",
    total: 92,
    placedAt: ISODate("2024-10-03T09:45:00Z"),
    lineItems: [
      { sku: "sensor-100", qty: 1, price: 60 },
      { sku: "panel-05", qty: 4, price: 8 }
    ],
    tags: ["retail"]
  },
  {
    _id: 1003,
    customer: { name: "Loft Labs", tier: "gold" },
    status: "pending",
    total: 240,
    placedAt: ISODate("2024-10-03T15:20:00Z"),
    lineItems: [
      { sku: "gateway-01", qty: 2, price: 60 },
      { sku: "panel-05", qty: 10, price: 8 }
    ],
    tags: ["lab", "priority"]
  },
  {
    _id: 1004,
    customer: { name: "Nova Retail", tier: "bronze" },
    status: "shipped",
    total: 58,
    placedAt: ISODate("2024-10-05T11:00:00Z"),
    lineItems: [
      { sku: "panel-05", qty: 6, price: 8 },
      { sku: "sensor-200", qty: 1, price: 10 }
    ],
    tags: ["retail"]
  }
]);

print("\nQuery 1 — Gold-tier orders over $150 (projection demo)");
orders
  .find(
    { "customer.tier": "gold", total: { $gt: 150 } },
    { _id: 0, "customer.name": 1, total: 1, status: 1 }
  )
  .forEach(doc => printjson(doc));

print("\nQuery 2 — Orders containing sensor-100 (array match)");
orders.find({ "lineItems.sku": "sensor-100" }).forEach(doc => printjson(doc));

print("\nQuery 3 — Average order total by customer tier (aggregation)");
orders
  .aggregate([
    { $group: { _id: "$customer.tier", avgTotal: { $avg: "$total" }, orders: { $sum: 1 } } },
    { $sort: { avgTotal: -1 } }
  ])
  .forEach(doc => printjson(doc));

print("\nQuery 4 — Update order 1002 status and tags");
const updateResult = orders.updateOne(
  { _id: 1002 },
  { $set: { status: "shipped" }, $addToSet: { tags: "priority" } }
);
printjson(updateResult);
print("\nUpdated order 1002:");
printjson(orders.findOne({ _id: 1002 }));

print("\nTTL Thought Exercise (no-op)");
print(
  "If orders were short-lived carts, consider adding an expiresAt field and creating a TTL index:\n" +
    'db.orders.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 1800 })\n' +
    "Discuss which field (createdAt? placedAt?) you would repurpose and what CAP trade-off TTL would reinforce."
);
