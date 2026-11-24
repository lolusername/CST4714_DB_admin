# Industry / Career Connection

## GitHub: observable, controllable schema migration

GitHub introduced gh-ost for online MySQL schema migrations. It copies data into a changed table while following ongoing changes, and provides controls for observing and pausing the migration. [GitHub engineering · August 1, 2016](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/).

## Why this belongs in the lesson

A database engineer makes change testable and recoverable. Our small PostgreSQL rehearsal teaches that habit; gh-ost’s MySQL mechanism is different. In the classroom, apply the same diagnostic steps to the ticket example.

Read the worked course example first, then use this case for a three-minute connection to professional work. No additional submission is required.

## Teaching explanation

A database in use keeps receiving writes while its structure needs to change. GitHub built gh-ost for that production problem in MySQL. Their article explains copying into a changed table, following ongoing changes, and giving operators controls over progress and cutover. GitHub used gh-ost for MySQL. Our migration uses PostgreSQL. What transfers is the engineering question: how do I know the change is safe, and where can I stop if the evidence is wrong? Our rehearsal and verification queries are a small, explicit answer to that question.

The original prose here is CC BY-NC-SA 4.0. The linked company article retains its own license.
