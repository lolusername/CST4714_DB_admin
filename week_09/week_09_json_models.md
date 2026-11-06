# Lab: One Ticket, Two JSON Designs

## 1. Two JSON Designs

**Referenced Design**
```json
{
  "users": [
    {
      "user_id": 103,
      "display_name": "Requester 103"
    },
    {
      "user_id": 201,
      "display_name": "Agent 201"
    }
  ],
  "tickets": [
    {
      "ticket_id": 1003,
      "subject": "Low water pressure",
      "status": "resolved",
      "requester_id": 103,
      "assignee_id": 201
    }
  ],
  "events": [
    {
      "event_id": 5005,
      "ticket_id": 1003,
      "event_type": "created",
      "event_at": "2026-02-03T12:05:00Z"
    },
    {
      "event_id": 5006,
      "ticket_id": 1003,
      "event_type": "status_changed",
      "event_at": "2026-02-03T14:25:00Z"
    },
    {
      "event_id": 5007,
      "ticket_id": 1003,
      "event_type": "status_changed",
      "event_at": "2026-02-03T19:40:00Z"
    }
  ]
}

Embedded or Hybrid Design

{
  "ticket_id": 1003,
  "subject": "Low water pressure",
  "status": "resolved",
  "requester": {
    "user_id": 103,
    "display_name": "Requester 103"
  },
  "assignee": {
    "user_id": 201,
    "display_name": "Agent 201"
  },
  "events": [
    {
      "event_id": 5005,
      "event_type": "created",
      "event_at": "2026-02-03T12:05:00Z"
    },
    {
      "event_id": 5006,
      "event_type": "status_changed",
      "event_at": "2026-02-03T14:25:00Z"
    },
    {
      "event_id": 5007,
      "event_type": "status_changed",
      "event_at": "2026-02-03T19:40:00Z"
    }
  ]
}

2. Tradeoffs
Read: In the referenced design, opening an application ticket 1003 requires three separate lookups from three separate arrays (or collections): finding the details of the ticket from the tickets array, matching the IDs 103 and 201 in the users array to find the display names, and searching the events array for all of the items matching ticket_id: 1003. In the embedded design, opening the application finds all of this the ticket details, the requester name, and the event history in one read by only the single ticket document.

Change: A change to the display name requires updating only one document in the users collection in the referenced design. Updating the same display name in the embedded design is more efficient because only a single record in the embedded document needs to be updated. The embedded design requires the application to find and update each of the long-term historical tickets that contain the embedded requester name. Meanwhile the embedded design's events array could become so long over the years that it becomes too costly to retrieve and update or it may even run into document size limits.
