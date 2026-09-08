# Week 10 Day 2 In-Class Response
## Event-Driven Inventory Platform Case Study (MongoDB Video)

## Activity Type
Short individual Day 2 response tied to the MongoDB data modeling week

## Purpose
This assignment asks you to watch a MongoDB beginner case-study video about building an event-driven inventory platform and explain the design choices in your own words.

The goal is not to memorize buzzwords.
The goal is to watch MongoDB modeling decisions happen in context:
- workload first,
- relationships second,
- modeling tradeoffs third.

That is more useful than treating embedding and referencing as abstract rules with no application behind them.
This response belongs on Day 2, after the MongoDB University modeling labs.
That timing lets students connect the official beginner material to a more realistic application design story.

## Assigned Video
Watch this video:
- [MongoDB beginner inventory case-study video](https://www.youtube.com/watch?v=1XeG3VDtdsA&list=PL4WbxRsNWc_Z2O2zq3syRit8b83M923QP&index=13)

Use the exact video above.

## Why This Video
MongoDB's official data modeling docs emphasize:
- identify the application's workload,
- map relationships,
- choose a document structure based on how the application uses data.

That makes a case-study video useful because you can see modeling choices made in a realistic application setting instead of as isolated definitions.
It is a better follow-up than a generic tutorial because it shows MongoDB decisions in the middle of a concrete application design.

## Optional MongoDB Context
If you want a short official reference before or after watching:
- Data Modeling: https://www.mongodb.com/docs/manual/data-modeling/
- Schema Validation: https://www.mongodb.com/docs/manual/core/schema-validation/
- Indexes: https://www.mongodb.com/docs/manual/indexes/

## Submission Format
Create `week10_inventory_video_response.md` and answer all prompts.

Requirements:
- 250-400 words total
- full sentences
- refer to at least two specific timestamps from the video
- make an argument, not just a summary

You may organize the response as short paragraphs or clearly labeled sections.

## Prompts

### Prompt 1
What problem is the inventory platform trying to solve, and why does an event-driven design make sense for that kind of system?

Focus on:
- what kinds of changes or events the platform needs to react to,
- why simple one-table thinking would be too narrow,
- what makes the workload feel like a real application instead of a toy example.

### Prompt 2
Describe one MongoDB data modeling decision that seems important in the case study.

You may discuss:
- embedding,
- referencing,
- document boundaries,
- denormalization,
- event records,
- or how the design supports a common read pattern.

Do not just say what MongoDB can do.
Explain why that choice helps this specific platform.

### Prompt 3
If you were designing this inventory platform, where would you be most likely to embed related data, and where would you keep references instead?

Your answer must name:
- one thing you would probably embed,
- one thing you would probably reference,
- and the workload reason for each choice.

### Prompt 4
Name one database administration or operations concern that still matters in this system, even if MongoDB makes the data model feel flexible.

Examples:
- schema validation,
- indexing,
- duplicate or inconsistent data,
- event ordering,
- write amplification,
- monitoring and performance,
- or keeping one source of truth clear.

Explain why that concern matters in a real platform.


Use at least two timestamp citations in your response.


## Evaluation (Participation / 10)
- 4 pts: all prompts are addressed
- 3 pts: timestamps are used correctly
- 3 pts: response explains tradeoffs clearly instead of only summarizing the video
