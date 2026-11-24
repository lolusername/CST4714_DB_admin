# Industry / Career Connection: Mattermost: a query plan explained the work

**Primary source:** [Mattermost engineering account, May 2024](https://mattermost.com/blog/making-a-postgres-query-1000-times-faster/). External content retains its own terms.

## What the organization reported

Mattermost investigated a slow PostgreSQL query used in large message-indexing jobs. Its engineers compared plans and changed how the query expressed a boundary condition. The company measured the speedup on its workload.

## Connection to this lesson

A performance claim needs the same intended answer, measured work, and a stated environment. Our CSV inspection predicts results; PostgreSQL EXPLAIN supplies plan evidence later.

Use the case to examine how the permission would work in Metro Support.

## A short application

Keep the newest-open-ticket query unchanged before and after adding an index. Compare ordered IDs, scan and sort work, buffers when available, and index size. A sequential scan on twelve rows can be reasonable.

Use this as a two-minute worked lecture example or optional review. It adds no submission, new account, or required reading beyond the weekly assignment.

**Career connection — Database engineer / performance engineer:** Turn a vague complaint into a hypothesis, a reproducible query, and evidence that could disprove the hypothesis.
