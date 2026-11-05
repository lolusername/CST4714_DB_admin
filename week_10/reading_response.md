# Week 10 Day 2 | Chapter 10 reading response

**Part B of Lab 2.** Read the assigned sections on printed pages **116–120** of [Operating Cloud Databases, Chapter 10](../Operating_Cloud_Databases.pdf#page=116). Begin at **Single-Document Atomicity Shapes Modeling** and continue through **More Than One Model Can Be Valid**. In particular, look at the latest-two query in **A Complete Referenced Page** and the discussion in **Growth and the Cost of a Convenient Preview**. The chapter works with ticket 1001. Your decision is about ticket 1003.

## Write to the developer

A resident opens ticket **1003**. The page should show the **latest two events, newest first**, while the service keeps all history. Staff need one place to correct the resident's current contact information. Imagine this ticket eventually has **50,000 events**. The [Week 9 event rows](../week_09/materials/datasets/metro_support/ticket_events.csv) contain the current history. Find ticket 1003's rows and use their timestamps to decide what appears on the page.

In **150–220 words**, recommend where the ticket, events, and current contact details should live. Address these questions in connected prose:

1. Which two event IDs should appear, in what order, and how would your design retrieve them while retaining the older event?
2. Where would a staff member make a contact correction? As history grows, what read, write, or consistency cost does your choice create?
3. Name one Chapter 10 section and use a specific idea from it to justify your decision. Connect that idea to one result from today's insert or filter practice. Name a field, value, or count you actually observed. If access failed and you traced the result by hand, identify it as a prediction.

You can defend a referenced, embedded, or hybrid design. Explain what happens for this workload. For example, a limit on a query controls the number of documents displayed; decide separately where the complete history lives.

## Submit

Paste **Part A — Lab record** from the [lab handout](lab_02_document_model.md) and **Part B — Chapter 10 response** into one Brightspace text entry. Use the reading section's title in your paragraph so your reader can find the passage. A complete response uses the event rows as evidence, identifies who owns current contact data, and explains one cost of the design.
