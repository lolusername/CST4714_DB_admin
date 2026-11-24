# Industry/Career Connection: Discord: access patterns and hot partitions

Discord's 2023 engineering account describes message-storage growth, hot partitions, a data-service layer, and migration from Cassandra to ScyllaDB. Its workload is not our CISA catalog and its design is not a MongoDB recommendation. The useful comparison is methodological: measure the distribution and access pattern before selecting infrastructure, and verify a migration rather than trusting row counts alone. A data engineer should report the import key, repeat behavior, field checks, and remaining limits. Our 75-record subset provides no evidence that it needs sharding.

[Read the company’s own account](https://discord.com/blog/how-discord-stores-trillions-of-messages).

## Use the case in this lesson

Distinguish the company’s published situation from our classroom model. Explain one design choice and one piece of evidence you would carry into database work. This reading supports the existing activity and adds no separate submission.
