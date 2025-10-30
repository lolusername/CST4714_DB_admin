// Relational to document modeling lab for Week 10.
(async () => {
  const activeDb = db.getName();
  print(`\n🚀 Week 10 Relational → Document Lab`);
  print(`Using database: ${activeDb}\n`);

  const customersRel = [
    { customerId: 'C1001', firstName: 'Riya', lastName: 'Singh', loyaltyTier: 'Gold', email: 'riya@example.com' },
    { customerId: 'C1002', firstName: 'Emilio', lastName: 'Rojas', loyaltyTier: 'Silver', email: 'emilio@example.net' },
    { customerId: 'C1003', firstName: 'Mei', lastName: 'Tanaka', loyaltyTier: 'Platinum', email: 'mei@example.org' }
  ];

  const ordersRel = [
    { orderId: 'O9001', customerId: 'C1001', orderDate: ISODate('2025-02-14T18:32:00Z'), channel: 'web', status: 'fulfilled' },
    { orderId: 'O9002', customerId: 'C1001', orderDate: ISODate('2025-03-02T11:05:00Z'), channel: 'mobile', status: 'pending' },
    { orderId: 'O9003', customerId: 'C1002', orderDate: ISODate('2025-02-28T21:18:00Z'), channel: 'store', status: 'fulfilled' }
  ];

  const orderItemsRel = [
    { orderId: 'O9001', sku: 'BK-101', title: 'Atlas Schema Design', quantity: NumberInt(1), unitPrice: 29.99 },
    { orderId: 'O9001', sku: 'BK-305', title: 'NoSQL Field Guide', quantity: NumberInt(2), unitPrice: 18.5 },
    { orderId: 'O9002', sku: 'AUD-205', title: 'MongoDB Journeys Podcast', quantity: NumberInt(1), unitPrice: 12.0 },
    { orderId: 'O9002', sku: 'EBK-110', title: 'Document Modeling Workbook', quantity: NumberInt(1), unitPrice: 22.5 },
    { orderId: 'O9003', sku: 'BK-305', title: 'NoSQL Field Guide', quantity: NumberInt(1), unitPrice: 18.5 },
    { orderId: 'O9003', sku: 'EBK-220', title: 'Polyglot Persistence Patterns', quantity: NumberInt(1), unitPrice: 24.0 }
  ];

  const orderItemsByOrder = orderItemsRel.reduce((grouped, item) => {
    if (!grouped[item.orderId]) grouped[item.orderId] = [];
    grouped[item.orderId].push({ ...item, lineTotal: +(item.quantity * item.unitPrice).toFixed(2) });
    return grouped;
  }, {});

  const ordersByCustomer = ordersRel.reduce((grouped, order) => {
    if (!grouped[order.customerId]) grouped[order.customerId] = [];
    const items = orderItemsByOrder[order.orderId] || [];
    const subtotal = items.reduce((acc, item) => acc + item.lineTotal, 0);
    const totalQuantity = items.reduce((acc, item) => acc + item.quantity.valueOf(), 0);
    grouped[order.customerId].push({
      orderId: order.orderId,
      channel: order.channel,
      status: order.status,
      orderDate: order.orderDate,
      items,
      metrics: {
        subtotal,
        totalQuantity: NumberInt(totalQuantity)
      }
    });
    return grouped;
  }, {});

  const embeddedCustomers = customersRel.map((customer) => ({
    _id: customer.customerId,
    profile: {
      firstName: customer.firstName,
      lastName: customer.lastName,
      email: customer.email,
      loyaltyTier: customer.loyaltyTier
    },
    orders: (ordersByCustomer[customer.customerId] || []).sort((a, b) => b.orderDate - a.orderDate),
    schemaVersion: NumberInt(1)
  }));

  const referencedOrders = ordersRel.map((order) => ({
    _id: order.orderId,
    customerId: order.customerId,
    orderDate: order.orderDate,
    channel: order.channel,
    status: order.status,
    items: orderItemsByOrder[order.orderId] || [],
    metrics: {
      subtotal: (orderItemsByOrder[order.orderId] || []).reduce((acc, item) => acc + item.lineTotal, 0)
    }
  }));

  const collectionsToReset = ['customers', 'orders_unfolded'];
  collectionsToReset.forEach((name) => {
    if (db.getCollectionNames().includes(name)) {
      db.getCollection(name).drop();
      print(`Dropped existing collection: ${name}`);
    }
  });

  db.createCollection('customers', {
    validator: {
      $jsonSchema: {
        bsonType: 'object',
        required: ['_id', 'profile', 'orders', 'schemaVersion'],
        properties: {
          _id: { bsonType: 'string' },
          schemaVersion: { bsonType: 'int', minimum: 1 },
          profile: {
            bsonType: 'object',
            required: ['firstName', 'lastName', 'email', 'loyaltyTier'],
            properties: {
              firstName: { bsonType: 'string', minLength: 1 },
              lastName: { bsonType: 'string', minLength: 1 },
              email: { bsonType: 'string', pattern: '^.+@.+\\..+$' },
              loyaltyTier: { enum: ['Silver', 'Gold', 'Platinum'] }
            }
          },
          orders: {
            bsonType: 'array',
            items: {
              bsonType: 'object',
              required: ['orderId', 'orderDate', 'items', 'metrics'],
              properties: {
                orderId: { bsonType: 'string' },
                orderDate: { bsonType: 'date' },
                channel: { enum: ['web', 'mobile', 'store'] },
                status: { enum: ['pending', 'fulfilled', 'canceled'] },
                items: {
                  bsonType: 'array',
                  minItems: 1,
                  items: {
                    bsonType: 'object',
                    required: ['sku', 'quantity', 'unitPrice', 'lineTotal'],
                    properties: {
                      sku: { bsonType: 'string' },
                      title: { bsonType: 'string' },
                      quantity: { bsonType: 'int', minimum: 1 },
                      unitPrice: { bsonType: 'double', minimum: 0 },
                      lineTotal: { bsonType: 'double', minimum: 0 }
                    }
                  }
                },
                metrics: {
                  bsonType: 'object',
                  required: ['subtotal', 'totalQuantity'],
                  properties: {
                    subtotal: { bsonType: 'double', minimum: 0 },
                    totalQuantity: { bsonType: 'int', minimum: 1 }
                  }
                }
              }
            }
          }
        }
      }
    }
  });

  db.customers.insertMany(embeddedCustomers);
  print(`Inserted ${embeddedCustomers.length} embedded customer documents.`);

  db.createCollection('orders_unfolded');
  db.orders_unfolded.insertMany(referencedOrders);
  db.orders_unfolded.createIndexes([
    { key: { customerId: 1, orderDate: -1 }, name: 'customer_date' },
    { key: { status: 1 }, name: 'status_idx' }
  ]);
  print(`Inserted ${referencedOrders.length} referenced order documents.\n`);

  print('🔎 Sample embedded customer:');
  printjson(db.customers.findOne({}, { projection: { orders: { $slice: 1 } } }));

  print('\n📊 Top customers (last 45 days) via embedded pipeline:');
  db.customers.aggregate([
    { $unwind: '$orders' },
    { $match: { 'orders.orderDate': { $gte: ISODate('2025-01-15T00:00:00Z') } } },
    { $group: { _id: '$profile.email', totalSpent: { $sum: '$orders.metrics.subtotal' }, orderCount: { $sum: 1 } } },
    { $sort: { totalSpent: -1 } },
    { $limit: 5 }
  ]).forEach((doc) => printjson(doc));

  print('\n🔄 Rebuild relational view with $lookup:');
  db.orders_unfolded.aggregate([
    { $match: { status: 'fulfilled' } },
    {
      $lookup: {
        from: 'customers',
        localField: 'customerId',
        foreignField: '_id',
        as: 'customer'
      }
    },
    { $unwind: '$customer' },
    {
      $project: {
        _id: 0,
        orderId: 1,
        orderDate: 1,
        customerEmail: '$customer.profile.email',
        loyaltyTier: '$customer.profile.loyaltyTier',
        subtotal: '$metrics.subtotal'
      }
    },
    { $sort: { orderDate: -1 } }
  ]).forEach((doc) => printjson(doc));

  print('\n✅ Lab complete. Customize the arrays to mirror your relational workload and rerun to compare strategies.\n');
})();
