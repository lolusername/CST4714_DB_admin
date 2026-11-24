# Industry / Career Connection

## Cloudflare: SQL powers device-status reports

Cloudflare described using TimescaleDB, built on PostgreSQL, for Zero Trust device analytics. Its example filters an account, a device, and a time range before grouping status records. [Cloudflare engineering · July 8, 2025](https://blog.cloudflare.com/timescaledb-art/).

## Why this belongs in the lesson

A reporting query has to define its population and row meaning. Analysts and data engineers inspect those choices before trusting a count or optimizing it. In the classroom, apply the same diagnostic steps to the ticket example.

Read the worked course example first, then use this case for a three-minute connection to professional work. No additional submission is required.

## Teaching explanation

Cloudflare’s engineering article includes a real reporting query. It filters to an account, a device, and a time range, then groups device-state records by hour and status. You can recognize the same SQL ideas we are learning: choose rows, group them, and count the resulting groups. Their storage and traffic are much larger than our fixture. Apply the company's measurement method to the classroom query. The useful connection is that a report’s filters and grouping have a meaning before they have a speed. A data engineer needs both a correct count and an explanation of what it counts.

The original prose here is CC BY-NC-SA 4.0. The linked company article retains its own license.
