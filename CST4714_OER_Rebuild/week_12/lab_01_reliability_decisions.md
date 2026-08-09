# Lab 1: Match Expectations to Replica and Recovery Decisions

## Purpose

Turn vague reliability language into testable promises for reads, writes,
partitions, and destructive changes.

This is individual work completed in class. Submit one Markdown file.

## Scenario

Metro Support has four expectations:

1. after a resident receives ticket confirmation, one member failure should not
   silently erase the confirmed ticket;
2. the resident should immediately see the ticket they just submitted;
3. an hourly analytics dashboard may be slightly stale; and
4. an accidental collection deletion must be recoverable without a paid Atlas
   backup feature.

## 1. Build the Decision Matrix

Create `week_12_reliability_decision.md`. For every expectation, identify:

- operation and user impact;
- write concern, read preference, or read concern decision where relevant;
- mechanism that supports the expectation;
- one failure or timeout behavior;
- verification evidence; and
- one limitation.

Use current Atlas Free documentation to confirm which topology and test controls
are available. Record the page and date checked.

## 2. Analyze One Partition

Assume the primary can communicate with only one secondary, while the third member
is isolated. Explain:

- whether a voting majority remains on the two-member side;
- what a majority-acknowledged write is asking for;
- why the isolated side cannot simply accept independent primary writes while also
  preserving one current copy; and
- what a client may observe during election and server selection.

Do not label the product permanently "CP" or "AP." Describe the operation during
this partition.

## 3. Add the Final-Project Workload Checkpoint

End the same file with one paragraph naming your tentative final-project scenario,
platform path, two important reads, one important write, and one failure or
recovery concern. The [canonical final project](../final_project.md) remains the
only source of final requirements.

## Submit One Thing

Submit `week_12_reliability_decision.md`. It contains the matrix, partition
analysis, and one workload paragraph in one artifact.
