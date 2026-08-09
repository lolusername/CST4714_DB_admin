# Lab: Turn Related CSV Tables Into Two JSON Designs

## Purpose

Represent the same relational facts in two valid JSON shapes and defend their
different read, write, growth, and duplication tradeoffs.

This is individual work completed in class. Do not run SQL or MQL. Submit one
Markdown file.

## 1. Inspect the Facts and Create the File

Open the three files in [`datasets/metro_support`](../datasets/metro_support/):
`users.csv`, `tickets.csv`, and `ticket_events.csv`.

In GitHub, select **Add file**, then **Create new file**. Name it
`week_09/week_09_json_models.md`. In the file, identify:

- the primary identifier in each CSV;
- the columns that connect one file to another;
- which relationship can grow without a clear bound; and
- one fact that should have a single authoritative owner.

## 2. Write Two Strict JSON Designs

Use ticket 1003 and its related rows. Include enough fields to preserve the
requester, assignment, status, and three events.

### Design A: Referenced

Write separate JSON arrays for users, tickets, and events. Use identifiers to
connect them. Use only strict JSON: double quotes, no comments, no trailing commas,
and timestamps represented consistently as strings.

### Design B: Embedded or Hybrid

Write one ticket document that embeds some related data. You decide whether to
embed requester details, all events, a bounded recent-event list, or a historical
snapshot plus references.

Both designs may be valid. They must represent the same underlying facts.

Validate each JSON block by pasting only the JSON into this small Colab or Python
check:

```python
import json
json.loads('''PASTE ONE JSON ARRAY OR OBJECT HERE''')
print("Valid JSON")
```

Remove the pasted JSON and any private content from the temporary checker when
finished.

## 3. Defend the Difference

Below the examples, write one compact comparison:

- one read Design A makes direct;
- one read Design B makes direct;
- one update that is harder in each design;
- one duplicated or growing value;
- one validation rule both designs need; and
- which design you would choose for a ticket page that shows the five latest
  events while retaining years of history.

There is more than one defensible answer. Your evidence must match the shapes you
actually wrote.

## Atlas Safety Check

Before submitting, confirm that your Atlas environment uses a free cluster and a
separate database user, and that no password, URI, private host, or access token
appears in the file. Atlas setup is not a separate deliverable.

## Submit One Thing

Commit `week_09_json_models.md` and submit its URL in Brightspace.
