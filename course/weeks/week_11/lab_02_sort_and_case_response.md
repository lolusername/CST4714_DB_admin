# Lab 2: Sort Performance and Inventory Case Response

Connect a guided query-plan exercise to a real application design case and write a
short workplace-ready recommendation.

This is individual work completed in class. Submit one Brightspace text response.

## 1. Test a Sort Index

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

**Submit:** in one Brightspace text submission, paste the redacted lab completion image and
the response. Do not create or upload a Markdown file.
