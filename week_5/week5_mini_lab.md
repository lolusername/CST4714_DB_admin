# Week 5 Mini Lab — Quick Normalization Drill

Use this short in-class activity to warm students up before the full wellness lab. Everything happens in the `public` schema and should take ~20 minutes.

---

## Scenario
A student club stores merchandise orders in a single spreadsheet. You’ll recreate the spreadsheet, spot problems, and refactor it into two small tables.

Raw columns:
- order_id, order_date
- customer_name, customer_email
- item_name, category
- unit_price, quantity
- line_total

Issues to notice:
- Customer contact info repeats across rows.
- Line totals can drift away from `unit_price * quantity`.
- Categories repeat for each line even though they only depend on the item.

---

## Step 1 — Load the raw data
Run this SQL in Supabase (public schema):

```sql
DROP TABLE IF EXISTS club_merch_raw;

CREATE TABLE club_merch_raw (
    order_id      integer,
    order_date    date,
    customer_name text,
    customer_email text,
    item_name     text,
    category      text,
    unit_price    numeric(6,2),
    quantity      integer,
    line_total    numeric(8,2)
);

INSERT INTO club_merch_raw VALUES
    (2001, '2024-03-15', 'Alex Rivera',  'alex@example.edu', 'Hoodie',   'Apparel',      35.00, 2, 70.00),
    (2001, '2024-03-15', 'Alex Rivera',  'alex@example.edu', 'Sticker',  'Accessories',   3.00, 4, 12.00),
    (2002, '2024-03-16', 'Britt Chen',   'britt@example.edu','Bottle',   'Accessories',  18.00, 1, 18.00),
    (2003, '2024-03-16', 'Casey Morgan', 'casey@example.edu','Hoodie',   'Apparel',      35.00, 1, 40.00), -- line_total error on purpose
    (2003, '2024-03-16', 'Casey Morgan', 'casey@example.edu','Notebook', 'Stationery',    6.00, 3, 18.00);

-- Quick anomaly checks
SELECT order_id, SUM(unit_price * quantity) AS computed_total,
       SUM(line_total) AS stored_total
FROM club_merch_raw
GROUP BY order_id;

SELECT customer_email, COUNT(*) AS rows_per_customer
FROM club_merch_raw
GROUP BY customer_email;
```

Ask students: What dependencies do you see? Which columns depend on the order, which depend on the item, and which depend on the customer?

---

## Step 2 — Design the fix
Work together to identify three target tables:
1. `club_customers(customer_email PRIMARY KEY, customer_name)`
2. `club_items(item_name PRIMARY KEY, category, unit_price)`
3. `club_orders(order_id, order_date)` plus a bridge table `club_order_lines(order_id, item_name, quantity)`

Have students sketch the ERD on the board (customers → order lines ← items, orders → order lines).

---

## Step 3 — Build the normalized tables
Provide this starter code and ask students to fill in the blanks:

```sql
DROP TABLE IF EXISTS club_order_lines;
DROP TABLE IF EXISTS club_orders;
DROP TABLE IF EXISTS club_items;
DROP TABLE IF EXISTS club_customers;

CREATE TABLE club_customers (
    customer_email text PRIMARY KEY,
    customer_name  text NOT NULL
);

CREATE TABLE club_items (
    item_name  text PRIMARY KEY,
    category   text NOT NULL,
    unit_price numeric(6,2) NOT NULL
);

CREATE TABLE club_orders (
    order_id   integer PRIMARY KEY,
    order_date date NOT NULL
);

CREATE TABLE club_order_lines (
    order_id   integer REFERENCES club_orders(order_id),
    item_name  text REFERENCES club_items(item_name),
    quantity   integer NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, item_name)
);
```

Prompt students to populate the tables using `INSERT ... SELECT DISTINCT` from `club_merch_raw`.

---

## Step 4 — Verify everything works
Together, run these checks:

```sql
-- Distinct customers (no duplicates expected)
SELECT * FROM club_customers;

-- Compare stored vs. computed totals using the normalized tables
SELECT o.order_id,
       SUM(li.quantity * i.unit_price) AS computed_total
FROM club_orders o
JOIN club_order_lines li ON li.order_id = o.order_id
JOIN club_items i ON i.item_name = li.item_name
GROUP BY o.order_id
ORDER BY o.order_id;
```

Discuss: How did the normalization remove the incorrect line total for order 2003? What business rules does each table enforce?

---

## Wrap-Up
- Revisit functional dependencies identified in Step 1 and confirm each table now respects them.
- Ask students how they would extend this model (e.g., tracking fulfillment status or payment method) without breaking normalization.
- Transition into the full wellness lab, emphasizing that the workflow is identical—just more tables and data.
