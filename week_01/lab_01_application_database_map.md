# Week 1 In-Class Lab: Application to Data Map

## Instructions

1. Choose one application you use (for example, music playlist, ticket tracker, or task list).
2. Name the 4–6 things the app needs to remember.
3. Write 3 question prompts this app must answer from its data.
4. Trace one action from user click to stored data in 4 steps:
   - client
   - API or backend logic
   - database management layer
   - stored data model

Use short, plain text. Keep your submission to one markdown file.

## Deliverable

Submit the repository URL to this file.

## Example Format

- **App**: Music playlist app
- **Data entities**: users, playlists, tracks, playlist_items
- **Question 1**: What tracks are currently in playlist 42?
- **Trace**: client -> API endpoint -> PostgreSQL/MongoDB command -> playlist_items row/document
