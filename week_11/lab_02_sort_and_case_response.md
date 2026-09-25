# Lab 2: Sort Performance and Inventory Case Response

[Open in GitHub](https://github.com/lolusername/CST4714_DB_admin/blob/main/week_11/lab_02_sort_and_case_response.md)

Connect a guided sort-performance exercise to a real application design case and write a
short workplace-ready recommendation.

This is individual work completed in class. Submit one Brightspace text response.

## 1. Improve a Sort

Complete [Improving Performance of $sort stages (Lab Only)](https://learn.mongodb.com/courses/improving-performance-of-sort-stages-lab-only).

Keep one redacted completion screen showing the exact lab title and completion
status or score. This external student lab is not the course example the
instructor live-coded.

If the external lab is unavailable, use Chapter 11's **Explain Shows Plan and
Execution Work** section and compare these explicitly illustrative results for
the same query returning the newest 20 open tickets:

| Plan | Returned | Documents examined | Keys examined | Blocking sort |
|---|---:|---:|---:|---|
| A: collection scan | 20 | 10,000 | 0 | yes |
| B: compatible index scan and fetch | 20 | 20 | 20 | no |

Explain why B does less search/sort work and one cost of keeping its index.
These numbers are a teaching case, not your measured runtime. Put that short
comparison in place of the completion image and label the fallback.

## 2. Explain an Inventory Design Decision

Watch [Building an Event-Driven Inventory Platform: A Case Study](https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13).

While watching, record one modeling decision, one workload/access pattern, and one
operational risk or tradeoff. Do not summarize the entire video.

Write 200-300 words in Brightspace using this structure:

- **Decision:** identify the most consequential database design decision in the case.
- **Specific example:** connect one moment from the video to embedding,
  referencing, event data, aggregation, validation, or index behavior from class.
- **Tradeoff:** explain what the decision makes harder or riskier.
- **Career connection:** write one sentence describing how you would communicate
  the decision to a developer or operations teammate.

Distinguish what the presenter actually demonstrates from a change you would
propose. For example, an index you recommend is not automatically an index shown
in the video. A timestamp or identifiable scene makes your example easy to locate.

**If the video is unavailable:** use this course-authored fictional case instead
and label your response "Written case fallback." Do not describe it as something
shown in the video.

A small retailer keeps one inventory document per product and store location.
The shopping page reads that document to display available stock. Orders live in
a separate collection and reference the product and location IDs. When a sale
occurs, the order service sends an event with a unique event ID. A background
worker receives the event and updates the inventory quantity. Delivery can be
delayed or retried: for a short period the shopping page can show an old quantity,
and a repeated event must not subtract the same sale twice. The retailer wants
fast stock lookups and a history of changes it can investigate.

Use the same four-part, 200-300-word response. For the specific example, cite a
fact from this written case instead of a video timestamp. Explain one benefit
and one operational risk of the design; distinguish a proposed improvement from
what the case already specifies. This replaces the video response, not adds to it.

**Submit:** in one Brightspace text submission, paste the redacted lab completion image and
the response. Do not create or upload a Markdown file.
