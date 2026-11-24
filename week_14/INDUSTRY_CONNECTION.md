# Industry/Career Connection: Netflix: changes and snapshots must agree

Netflix's 2019 DBLog account explains propagating committed database changes and combining log processing with chunks of a table dump. Keeping downstream stores current requires controlling the interaction between past snapshot rows and newer changes. Our transaction/outbox and version-guard example is a smaller teaching model, not Netflix's implementation. A platform engineer should identify the authoritative source, replay behavior, and reconciliation evidence before calling a derived view repaired.

[Read the company’s own account](https://netflixtechblog.com/dblog-a-generic-change-data-capture-framework-69351fb9099b).

## Use the case in this lesson

Distinguish the company’s published situation from our classroom model. Explain one design choice and one piece of evidence you would carry into database work. This reading supports the existing activity and adds no separate submission.
