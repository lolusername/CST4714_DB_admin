# Lab 1: Build a Responsibility and Evidence Map

## Purpose

Create your first reproducible course artifact while learning how to separate a
managed provider's responsibilities from your own.

This is individual work completed in class. Do not include passwords, keys,
connection strings, or real personal data.

## 1. Create the Artifact in GitHub

1. Sign in to GitHub and open the repository you will use for course practice.
2. Select **Add file**, then **Create new file**.
3. Name the file `week_01/responsibility_map.md`. Typing the slash creates the
   folder in GitHub's online editor.
4. Paste the template below and replace every bracketed prompt.

```markdown
# Managed Database Responsibility Map

## Scenario
[Choose one: a user cannot connect; a query is slow; a record is visible to the
wrong user; or a deleted record must be recovered.]

## Separate the Layers
| Layer | What might be wrong? | What evidence would I collect? |
|---|---|---|
| application or browser | [write here] | [write here] |
| identity or network | [write here] | [write here] |
| database service | [write here] | [write here] |
| query or data | [write here] | [write here] |

## Shared Responsibility
Provider responsibility: [one specific responsibility]

My responsibility: [one specific responsibility]

## Verification
One check that would support my conclusion: [write here]

One thing that check would not prove: [write here]

## Credential Safety
One value that must never appear in this artifact: [write here]
```

5. Use the **Preview** tab to check the headings and table.
6. Commit the file with the message `Add managed database responsibility map`.

## 2. Strengthen One Claim

Choose either Supabase or MongoDB Atlas. Open its official documentation and add
one sentence below your responsibility map that begins:

> According to the current platform documentation, ...

Link the exact page. Your sentence must distinguish a documented feature from
something you are assuming.

Useful starting points:

- Supabase architecture: <https://supabase.com/docs/guides/getting-started/architecture>
- MongoDB Atlas documentation: <https://www.mongodb.com/docs/atlas/>

## 3. Submit One Thing

Open the committed file, copy its GitHub URL, and submit that one URL in
Brightspace.

Before submitting, check that:

- all bracketed prompts are replaced;
- the scenario is analyzed across at least four layers;
- provider and customer responsibilities are both specific;
- verification includes a limitation; and
- no credential or private value appears.
