# Lab: One Ticket, Two JSON Designs

A ticket page needs a requester's name, the ticket's status, and its event
history. Those facts can be represented in more than one sensible JSON shape.
Design two alternatives and explain which read each makes convenient.

Work individually in class in a text editor. Do not run SQL or MQL. No Atlas
account or database connection is needed. Submit one Markdown file in Brightspace.

## 1. Read the Rows and Write Two Designs

Open the three CSV files in the
[Metro Support dataset](../../datasets/metro_support/README.md).
The files are [users.csv](../../datasets/metro_support/users.csv),
[tickets.csv](../../datasets/metro_support/tickets.csv), and
[ticket_events.csv](../../datasets/metro_support/ticket_events.csv).
Use only **ticket 1003**, requester **103**, assignee **201**, and events
**5005, 5006, 5007**. Ignore other rows for this exercise.

Here is a small JSON example using a different ticket:

```json
{
  "ticket_id": 1004,
  "subject": "Broken bench slat",
  "status": "new",
  "requester_id": 104,
  "assignee_id": null
}
```

The number 104 identifies another record; the object does not contain that
person's name. Also notice that `null` is not quoted.

In `week_09_json_models.md`, write two fenced `json` blocks. Each block must
contain one complete JSON object:

- **Referenced design:** put `users`, `tickets`, and `events` arrays in the
  object. Connect their records by IDs, like the CSVs.
- **Embedded or hybrid design:** put useful related information inside the
  ticket document, such as the requester's name and an events array. You may
  retain IDs for facts stored elsewhere.

Keep the ticket's ID, subject, status, requester and assignee IDs and display
names, and the three events' IDs, types, and timestamps. The event columns are
`event_id`, `event_type`, and `event_at`. Other columns can be omitted. Both
designs must preserve those same facts. Dates remain strings in this JSON
exercise. Chapter 9 and slides 24-26 demonstrate the method with ticket 1001,
not your assigned ticket.

Use double quotes for strings and field names, balanced braces/brackets, no
comments inside JSON, and no trailing commas. Formatting and indentation should
make the nesting readable. A GitHub commit saves text; it does not prove valid JSON.

## 2. Explain One Tradeoff

Below your designs, explain these two situations in a short paragraph:

**Read:** the application opens ticket 1003 and shows its requester and events.
Where does it find those facts in each design?

**Change:** the requester changes their display name, and the ticket accumulates
years of events. Which information would need updating, and which part could
grow too large?

Choose a design for a page showing only the five latest events while retaining
the complete history. You may propose bounded embedding plus a separate history
collection. Explain your choice; there is no single required document shape.

**Submit:** `week_09_json_models.md` with two JSON examples and your paragraph.
This is one file, not an Atlas configuration task or a second written assignment.

**Using GitHub's editor:** in your own repository, choose **Add file > Create new
file**, enter the filename, write the Markdown and JSON blocks, use **Preview**,
then **Commit changes**. Download the file for the Brightspace submission.
[GitHub's file-creation guide](https://docs.github.com/en/repositories/working-with-files/managing-files/creating-new-files)
shows the interface.
