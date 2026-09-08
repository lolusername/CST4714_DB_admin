# Lab 1: What Does a Confirmation Promise?

A resident submits a request and sees a confirmation. The next read shows nothing.
Did the database lose the request, is a copy behind, or did the client fail to
learn whether the write succeeded? Those possibilities need different responses.

Work individually in class. Submit one Brightspace text response. You will reason
from the supplied cases, not stop or reconfigure an Atlas cluster.

## 1. Choose a Read and Write Policy

Our teaching replica set has three voting, data-bearing members: primary A and
secondaries B and C. A can communicate with B, while C is isolated.

Worked example: an hourly category dashboard can tolerate some delay. Reading
from an eligible secondary may reduce work on the primary, but the dashboard must
show when its data was refreshed. Replication delay is not a fixed maximum, and a
secondary preference by itself does not guarantee a particular staleness bound.

Now recommend a policy for a resident's **confirmation and immediate ticket
page**. Use [Chapter 12](../../textbook/module_12_reliability.md) to choose:

- how many members should acknowledge the write;
- where the next read should go, which read concern it should use, and how a
  causal session connects it to the preceding write; and
- what the application should do if the write times out before confirmation.

Explain your choices using A, B, and C. A majority is two here. A timeout does not
necessarily mean the write failed: a stable request ID and a status check can
prevent an accidental duplicate submission. Reading an unrelated session from
an arbitrary secondary does not promise read-your-writes.

## 2. Decide Whether the Recovery Plan Is Enough

The usable logical export represents the complete dataset as of 14:00. At 14:17
someone accidentally deletes the collection. A rehearsal takes eight minutes from starting the restore
to passing its application checks. There are no exports or event logs after 14:00.

The stated target is **at most five minutes of lost work** and **service restored
within ten minutes of the incident**.

Explain whether this plan meets each target. Use the actual times. Separate
restore execution from the time needed to detect the failure, find the artifact,
and authorize the repair. A second replica follows the deletion; it is not the
missing historical copy.

End with two or three sentences proposing a safer *free-tier* classroom recovery
plan and acknowledging what it cannot guarantee. You do not need to purchase a
feature or perform a failover.

**Submit:** one text response with your confirmation policy and recovery analysis.
Use precise reasons rather than a large matrix. During project work, reuse the
same reasoning for one important write in your project; the
[final project](../../assignments/final_project.md) remains its sole requirements
document.
