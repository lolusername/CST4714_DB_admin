# Industry / Career Connection

## Cloudflare: reports depend on the aggregation level

Cloudflare described moving HTTP analytics into ClickHouse, with aggregated tables supporting reports over request logs. Different report measures required different aggregation choices. [Cloudflare engineering · March 6, 2018](https://blog.cloudflare.com/http-analytics-for-6m-requests-per-second-using-clickhouse/).

## Why this belongs in the lesson

An analytics engineer checks what each stored or returned row represents. Our ticket/event example exposes that same counting problem before any tuning. In the classroom, apply the same diagnostic steps to the ticket example.

Read the worked course example first, then use this case for a three-minute connection to professional work. No additional submission is required.

## Teaching explanation

Cloudflare’s HTTP analytics article explains a pipeline from request logs into analytical tables and reports. Those tables are useful because they summarize the data at a chosen level, but the level still matters: a summary row is not automatically one request, and different measures do not all combine in the same way. Our direct join produced ticket-event pairs. We had to name that meaning before correcting the count. That is an analytics-engineering skill, even though we use PostgreSQL and the case uses ClickHouse. The company measured its own workload at this scale.

The original prose here is CC BY-NC-SA 4.0. The linked company article retains its own license.
