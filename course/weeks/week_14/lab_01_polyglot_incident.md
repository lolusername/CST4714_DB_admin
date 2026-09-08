# Lab: Why Does the Resident See the Wrong Status?

The staff dashboard says a request is resolved. The resident's page says it is
open. Diagnose the disagreement, then try duplicate and delayed events in a
small executable model.

Work individually in class. No cloud account is needed. Submit one Brightspace
text response.

## 1. Follow the Failure

PostgreSQL owns ticket status. One transaction changes the ticket and creates an
outbox event. A relay publishes that event, and a consumer updates the MongoDB
copy used by the resident page.

```text
PostgreSQL ticket:
ticket_id=1008 status=resolved source_version=17 updated_at=14:03:12Z

Outbox event:
event_id=evt-1008-17 aggregate_id=1008 source_version=17
created_at=14:03:12Z published_at=14:03:13Z

Consumer log:
14:03:13Z received evt-1008-17
14:03:13Z timeout writing projection
14:03:14Z queued retry evt-1008-17
14:04:00Z retry worker paused: expired database credential

MongoDB projection read at 14:04:05Z:
ticket_id=1008 status=open source_version=16
```

The timeout alone would not prove whether a write occurred. The later read
establishes that this projection is still behind. The received-event log also
shows that this event reached the consumer; the outbox timestamp alone would
not establish every downstream action.

Identify where progress stopped and choose the first repair. Explain why
changing the authoritative PostgreSQL status back to `open` would be a mistake.
No production credentials need to be changed for this paper incident.

## 2. Try Duplicate and Out-of-Order Delivery

Paste this Python example into a blank [Colab](https://colab.research.google.com/)
notebook. It uses dictionaries to model the decision, not a real MongoDB server.

```python
projection = {"ticket_id": 1008, "status": "open", "source_version": 16}
deliveries = [
    {"event_id": "evt-1008-17", "status": "resolved", "source_version": 17},
    {"event_id": "evt-1008-17", "status": "resolved", "source_version": 17},
    {"event_id": "evt-1008-16", "status": "open", "source_version": 16},
    {"event_id": "evt-1008-18", "status": "closed", "source_version": 18},
]

for event in deliveries:
    if event["source_version"] <= projection["source_version"]:
        print("Ignore old or duplicate event:", event["event_id"])
    else:
        projection["status"] = event["status"]
        projection["source_version"] = event["source_version"]
        projection["last_event_id"] = event["event_id"]
        print("Apply:", event["event_id"])
    print("Resident now sees:", projection["status"], projection["source_version"])
```

Predict which deliveries apply before running. Then move version 16 to the **end**
of the list and rerun from the first line. The final state should remain
`closed`, version 18. Temporarily replace the condition with `if False:` to
simulate a consumer that accepts every event. Observe the incorrect regression,
then restore the version guard.

This model assumes one ordered version sequence **per ticket** and events that
contain the complete projected state. If events only contain changes such as
"increment by one," skipping versions can lose effects. Concurrent production
consumers also need an atomic comparison-and-update; a separate Python read and
write would race. We will discuss that boundary in class.

**Submit:** one short incident update stating the user impact, observed failure,
repair, and the duplicate/delayed-event behavior you tested. Include the final
state from the broken run and the repaired run. Name one broader check before
declaring the incident resolved, such as other queued tickets or consumer lag.
No separate timeline, five-check matrix, notebook attachment, or second report
is required.
