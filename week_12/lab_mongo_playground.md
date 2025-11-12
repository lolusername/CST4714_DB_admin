# Mongo Playground Mini-Sprint (Week 12)

## Purpose
Give students a quick, browser-friendly lab that reinforces CRUD fluency, aggregation basics, and schema/index reasoning while connecting back to CAP trade-offs.

## Setup
1. Open [mongoplayground.com](https://mongoplayground.com/).
2. Set the database name to `labWeek12`.
3. Copy the contents of `week_12/lab_mongo_playground.js` into the editor.
4. Run the file once to seed the `orders` collection; then rerun individual sections as needed.

## Activities
- **A1 — Filtering + Projection**  
  Predict the result of Query 1 before running it. Why does the projection hide `_id` but keep nested customer names?
- **A2 — Array Matching**  
  Inspect the documents returned by Query 2. How does MongoDB treat multiple matching `lineItems`?
- **A3 — Aggregation Warm-Up**  
  Run Query 3 and interpret the `$group` output. Which tier would you target with a promotion, and what index would support this query best (apply ESR)?
- **A4 — Thoughtful Updates**  
  Execute Query 4. Why is `$addToSet` safer than `$push` for the `tags` array? What write concern would you set in production for status changes?
- **A5 — TTL Scenario**  
  Discuss the final printed prompt. Which timestamp would you convert into a TTL index for short-lived carts? How would TTL influence availability vs consistency during failures?

## Reflection (Exit Ticket)
Submit 4–5 sentences covering:
1. The Playground query that revealed the biggest insight for you and why.
2. One schema or indexing change you would make before deploying this dataset.
3. How CAP considerations (consistency vs availability) affect the way you expose order status to users.
