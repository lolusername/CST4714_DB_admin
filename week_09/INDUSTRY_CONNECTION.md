# Industry / Career Connection: Discord: data shape followed a read pattern

**Primary source:** [Discord engineering account, March 2023](https://discord.com/blog/how-discord-stores-trillions-of-messages). External content retains its own terms.

## What the organization reported

Discord describes partitioning messages by channel and time bucket, handling hot partitions, and changing its database and data-service architecture as message traffic grew. The article documents one system’s workload; it does not choose MongoDB for our class.

## Connection to this lesson

Begin with the application’s read and growth patterns. A ticket page and years of history may need different access paths; embedding all future events in one document is not automatically the right design.

We apply the company's example to the Metro Support design below.

## A short application

For ticket 1003, preserve the three supplied events in both designs. Then describe a later design for a latest-two-events preview while retaining the complete history and one authoritative current requester name.

Use this as a two-minute worked lecture example or optional review. It adds no submission, new account, or required reading beyond the weekly assignment.

**Career connection — Data engineer / backend engineer:** Explain where each fact lives, how it is read, and what must happen when it changes or grows.
