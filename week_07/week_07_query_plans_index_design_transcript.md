# Week 7: Midterm Explanation and Preliminary Research - Spoken Transcript

## Slide 1

Welcome, everyone. This is our only meeting this week, and it has two halves. For the first forty-five minutes, I am going to take you through the midterm project one part at a time. For each part, you will see what the starter file already does for you, the small piece you add, the result you should expect, and where that result goes in your README. Then you will have about fifty minutes to work in a Colab notebook that prepares you for the index part of the midterm. In the last five minutes, you will save that notebook, share it with me, and submit its link in Brightspace.

If you have a laptop open, open the Week 7 README on GitHub. It links the midterm instructions, which put the whole midterm on one page: every part, step by step, with the results you should expect. It also links the SQL starter and the README template. If anything I say today sounds different from the written assignment, the written assignment is the rule, and I want you to ask me about it.

## Slide 2

Here is the whole midterm in one sentence. You will run a small PostgreSQL database safely, prove what happened with real query results, and explain those results in your own words.

The database is Metro Support, the ticket system we have used all semester, with users, tickets, and ticket events. You do not build an application, find a new dataset, or give a presentation.

The project has five parts. In Part 1, you check that the data loaded correctly, and you explain three rules that protect it. In Part 2, you change one ticket inside a transaction and roll that change back, and then you make a different change and commit it. In Part 3, you explain a blocking incident from our Week 5 lab. In Part 4, you test one improvement, and the recommended improvement is an index. In Part 5, after next week's lesson on backups, you write a plan for recovering this database.

This is an individual project worth thirty percent of your course grade. You submit two files, midterm.sql and README.md, together in one ZIP file, by the deadline posted in Brightspace.

## Slide 3

This slide explains the workload, so it is worth reading carefully. The starter file does a lot of the work for you, on purpose.

Read down the middle column. The starter already creates all three tables, loads all of the data, and counts the rows. It already contains the complete rollback example for Part 2 and the complete index experiment for Part 4. The Week 5 notebook already contains the blocking example for Part 3.

Now read down the right column. In SQL, you write two small things. The first is a join that shows each ticket with the name of the person who requested it. The second is a commit example that looks almost exactly like the supplied rollback example. On the recommended route, that is all the new SQL you write.

Everything else you add goes into your README. You record the results you actually saw, and you explain them. You explain three integrity rules, the blocking incident, and what the index did or did not change. After Week 8, you add the recovery plan.

So most of your grade comes from careful observation and clear explanation, not from writing a lot of code. A small project with accurate results and clear writing can earn full credit.

## Slide 4

You submit exactly two files, and each one has a different job.

The file midterm.sql is the record of what you ran. Start by saving the starter as midterm.sql. By the end, it holds the supplied setup and count query, your requester join, the rollback example, your commit example, and the index experiment. Tests that are supposed to fail are optional. If you write one, such as inserting a duplicate email, keep it commented out, so the whole file can still run from top to bottom.

The file README.md is the record of what happened and why. Start by saving the template as README.md. It already has a heading for every part, with a prompt in square brackets under each heading. Replace every prompt with your own results and explanations, and do not leave any square-bracket prompts behind.

When you finish, put both files into one ZIP and upload that ZIP in Brightspace. Do not put a password, a connection string, or an API key in either file. When the README asks about your environment, describe it in words, for example, my Supabase practice project, followed by the PostgreSQL version number.

## Slide 5

Before you run anything, here are four rules that keep your work safe.

First, run the starter only in your personal practice database. Section 1 begins by dropping the midterm_metro schema with CASCADE. That deletes everything inside midterm_metro, plus anything elsewhere that depends on it, and then rebuilds the schema from scratch.

Second, run Section 1 once. After that, highlight one section and run only that section.

Third, do not rerun Section 1 partway through the project. If you do, ticket 1004 goes back to low, and the index you created disappears. If you ever need a clean start, rerun Section 1 and then repeat the later sections in order.

Fourth, keep each transaction together. Highlight everything from its first SELECT through its last SELECT and run it as one block.

Now look at the box on the right. The Supabase SQL Editor may show only the result of the last statement in a run. For a transaction block, that hides the value inside the transaction, and you need that value for your README. The fix is a short Colab helper called run_sql, which is printed at the end of the midterm instructions. It prints every result in order. A psql session does the same thing.

## Slide 6

Part 1 starts with Section 1 of the starter. When it finishes, its last result is a small table of counts. You should see eight users, twelve tickets, and twenty-one ticket events, exactly as on the left of this slide. If you see different numbers, rerun Section 1 before you go any further.

Next, you write the requester join. In the starter, find the TODO comment that asks for a query joining tickets to their requesters, and replace that comment with your query. The code on the right shows the shape. You select the ticket ID from tickets and the display name from users. The only part left blank is the join condition. Every ticket has a requester_id column, and its value matches a user_id in the users table. Write that match on the ON line. Use the full table names, midterm_metro.tickets and midterm_metro.users, as the starter asks.

When your join is correct, it returns exactly twelve rows, one for each ticket. The first row is ticket 1001 with Requester 101, and the last row is ticket 1012 with Requester 104. If you get any number other than twelve, look at your join condition again.

Record both results in the Database checks section of your README: the three counts, and a short statement of what your join returned.

## Slide 7

The second half of Part 1 is explanation. In your README, you name three integrity controls that already exist in the starter, say which column each one protects, and explain what bad data each one prevents. You do not design new tables or invent new constraints.

The word non-key matters here. A primary key and a foreign key are both keys, so they do not count toward your three. The table on this slide shows the three kinds of control the assignment points to, and the starter has all three. NOT NULL appears on many columns. UNIQUE appears on the email column of users. And the tickets table has a CHECK rule that compares two dates.

The simplest approach is to explain one of each. The box at the bottom shows one complete answer. NOT NULL on tickets.subject rejects a ticket whose subject is missing, meaning NULL. Without it, a ticket could enter the queue with no recorded problem. Notice its three pieces: the control, the column, and the bad data it stops.

Write the other two in your own words. For UNIQUE, ask yourself which duplicate it blocks and why that duplicate would cause trouble. For the CHECK rule, read the condition carefully and ask which impossible pair of dates it rejects.

## Slide 8

Part 2 uses ticket 1004, which starts with priority low.

On the left is Section 2A, the supplied rollback example, and you run all six statements together. The first SELECT shows the value before the transaction. BEGIN starts the transaction, and the UPDATE changes the priority to high. The second SELECT shows the value inside the transaction. ROLLBACK cancels the change, and the last SELECT shows the value after. You should see low, then high, then low.

Section 2B is yours to write, and it follows the same pattern. Copy the six statements, change high to medium, and change ROLLBACK to COMMIT. This time, you should see low, then medium, then medium.

Those six values go into the Transactions table in your README, laid out exactly like the table on this slide. Then explain the difference in a few sentences. Inside a transaction, your own session can already see its change. ROLLBACK throws the change away, so the row returns to low. COMMIT makes the change permanent, so medium remains.

Run 2A before 2B. If you run them in the other order, your values will be different, and that is fine as long as you record and explain what you actually saw. When you finish Part 2, leave medium in place, because your recovery checks expect it.

## Slide 9

Part 3 goes back to the Week 5 blocking lab. You do not add anything to midterm.sql for this part. Everything goes into the Blocking section of your README.

First, choose your evidence source, and write it on the Evidence source line. If you run the Week 5 notebook again, write my live run. If you use the results you saved in Week 5, write my saved Week 5 run. If you cannot connect, the notebook has a supplied trace near the end, and you write supplied trace analysis. All three paths are graded with the same criteria, as long as your label is honest.

Then record the six things listed on the left: the diagnostic SQL, which is the query on pg_stat_activity that calls pg_blocking_pids; the blocked session's PID; the blocking session's PID; the row involved; the action that released the block; and the final values of that row.

The box on the right shows how to read the diagnostic output. The blocked session is the one waiting, so its wait_event_type is Lock. Its blocking_pids column lists the PID of the session it is waiting for, and that session is the blocker. Finish by explaining the final row: which change survived, which change did not, and why.

One warning. The Week 5 notebook uses a table called lock_lab, and its ticket 1004 starts at medium and open, not low and new. Take your values from the notebook, not from the midterm database.

## Slide 10

Part 4 is the recommended improvement, and the starter already contains every statement you need. The query asks for the newest open tickets, newest first.

In Section 4A, run the SELECT by itself and write down the ticket IDs in order. Then run the EXPLAIN statement by itself and save its output. Running them one at a time matters, because the editor may show only the last result.

In Section 4B, create the index once. If PostgreSQL reports that the index already exists, it was created earlier, maybe before your baseline. Unless you are sure Section 4A ran first, run the DROP INDEX line from the starter's comments and repeat 4A, 4B, and 4C.

In Section 4C, run the same SELECT and the same EXPLAIN again, and then run the size query.

The table shows what I measured on PostgreSQL 16. The IDs are 1011, 1007, and 1001, both before and after. The plan says Seq Scan on tickets both times. The index is 16384 bytes, which is 16 kilobytes. Your timings and cost numbers will be different, and that is expected.

One detail confuses many people. After you create the index, the cost numbers in the plan may drop, even though the plan still says Seq Scan. Building the index also updated PostgreSQL's estimate of how many rows the table holds. A different estimate is not a different plan. Compare the scan type, such as Seq Scan, Index Scan, or Bitmap Heap Scan.

## Slide 11

Many of you will see the same plan before and after the index, and you may think you did something wrong. You did not. An unchanged plan is a correct result for this database, and an honest explanation of it can earn full credit.

Here is why it happens. All twelve tickets fit on a single eight-kilobyte page. To use the index, PostgreSQL would read index pages and then still read the table page. Reading the one table page directly is cheaper, so the planner chooses a sequential scan. An index like this one is designed for a much larger table, where reading every row would be slow.

The list on the right is what your One improvement section covers. First, the problem the index is meant to solve, which is finding the newest open tickets quickly as the table grows. Second, whether your plan changed, quoting the scan line from each plan. Third, whether the result stayed the same, comparing the ordered IDs. Fourth, one cost of keeping the index, such as the storage it uses or the extra work on every insert and on any update that changes an indexed column. Fifth, the short recommendation the starter asks for: keep the index or drop it, and why.

Do not add fake rows or change planner settings to force an index scan. The assignment does not allow it.

If you prefer a different improvement, you may choose one alternative from class instead: a least-privilege grant, a row-level security test, or a safe schema change. Complete one improvement only.

## Slide 12

Part 5 waits until after next week, when we cover backup and restore. I am showing it now so you can see the whole project.

The recovery plan is one section of your README, about a page at most, and it covers the six items on the left. The source is your practice database and the midterm_metro schema. The backup is a logical export, like the pg_dump command we use in Week 8, limited to the midterm_metro schema and saved as a file such as midterm_metro.dump. The template calls that file the artifact, so name it. The destination is a separate, empty database, on a server with the same or a newer PostgreSQL version. Never restore over the source, because then you are not testing anything. The restore uses pg_restore into that separate database. The checks are at least three, each with an expected result. The table on the right lists four good ones: the counts of eight, twelve, and twenty-one; twelve tickets joined to requesters; ticket 1004 still at medium; and the index still present. The limits describe what the backup leaves out, such as roles, permissions, other schemas, and Supabase settings.

On the Status line, write proposed plan unless you actually performed the restore. Running the restore is optional. What matters is being clear about which checks you planned and which results you actually observed.

## Slide 13

This table maps the README template to the five parts, so you always know where a result belongs.

Run order comes first. Explain how someone else would run your midterm.sql from the beginning, in which order to run the sections, and what the reset in Section 1 deletes. Imagine a classmate following your instructions without being able to ask you anything.

Database checks holds Part 1: your counts, your join result, and your three controls. Transactions holds Part 2: the table of six values, followed by your explanation. Blocking holds Part 3: your evidence label, the diagnostic SQL, the two PIDs, the row, what released the block, and the final values. One improvement holds Part 4: the ordered IDs, the plan lines, the index size, and your explanation. Recovery plan holds Part 5, which you add after Week 8.

References and assistance comes last. Name the starter, the notebooks, any documentation you used, and any assistance you received. Then say what you changed and what you observed yourself.

At the very top of the README, fill in your name, your section, and your environment. To find your PostgreSQL version, run SELECT version, and copy the version number. Describe the environment in words, without any credentials.

## Slide 14

The rubric rewards honesty about evidence, so this slide applies to every part of the project.

An observed result is something you saw in your own output. Write it as a plain fact, with the values, like the example on the left: my rollback test showed low before, high inside the transaction, and low after ROLLBACK.

A prediction, or a proposal, is something you expect but did not run. Label it clearly, like the example on the right: I predict that a restored copy will contain twelve tickets; I have not run this restore. That sentence is completely acceptable in a recovery plan marked proposed plan.

Three situations come up often. First, if you used the supplied blocking trace, those PIDs came from the notebook, not from your run, so say so. Second, if a step failed, write what failed and what you tried. A clear account of a failure is worth far more than a result you did not actually see. Third, copy values directly from your own output, not from these slides or the instructions. Your timings and cost numbers will not match mine, and they should not.

Today's Colab notebook asks for the same distinction, so you will practice it in the second half of class.

## Slide 15

Here is the rubric, out of one hundred points, with the evidence that earns each area.

Twenty-five points are for a reproducible schema and data integrity. The evidence is the setup running, the counts of eight, twelve, and twenty-one, the twelve-row join, and three controls explained.

Twenty-five points are for transactions and blocking. The evidence is the six observed values with an explanation, and a blocking record that matches its evidence and is labeled honestly.

Twenty points are for one improvement. The evidence is a reason for the change, relevant before and after checks, and one tradeoff. On the index route, that means the ordered IDs, the plan lines, the index size, and one cost. A faster time or an index scan is not required.

Fifteen points are for recovery readiness. The evidence is a plan with a separate destination and at least three meaningful checks with expected results.

The last fifteen points are for documentation and communication. Someone else should be able to follow your two files without asking you questions. Your results should be easy to find, every template prompt should be replaced, and there should be no secrets anywhere.

As the assignment says, a small working project with clear explanations is enough.

## Slide 16

These are the mistakes I expect to see most often, so you can avoid them.

Rerunning Section 1 partway through the project. It resets ticket 1004 and deletes the index. Run it once, then work section by section.

Splitting a transaction across separate runs. Keep BEGIN and its COMMIT or ROLLBACK in the same run, along with the SELECT statements around them.

Recording only the last result the editor showed. If you see only the final value, use the Colab helper from the instructions or psql to see the value inside the transaction.

Copying the expected values instead of your own output. The expected values are there so you can check your work, not replace it.

Calling the supplied trace a live run. Label it supplied trace analysis.

Adding fake rows or changing planner settings to force an index scan. An honest sequential scan is a good answer.

Pasting a password or a connection string into a file. Describe your environment in words instead.

Leaving square-bracket prompts from the template in your README.

And finally, submitting the Colab notebook instead of the midterm files. Today's notebook is classwork. The midterm is midterm.sql and README.md in one ZIP.

## Slide 17

Here is the timeline. Today you learn the project and do the preliminary research in Colab. In the first meeting next week, we do the backup and restore lab, which gives you everything you need for Part 5. The second meeting next week is a midterm clinic. Bring one concrete question and one part of the project that already works, and we will use the rubric to find your most valuable next step. The deadline for the ZIP with midterm.sql and README.md is posted in Brightspace.

A good order is to finish Parts 1 and 2 first, because they are short and they set up the data for everything else. Then do Part 3 from your Week 5 work and Part 4 with the index experiment. Write Part 5 after the backup lab.

Now I will take your questions about any part of the midterm. When we finish, open the Week 7 README and click the Open in Colab button, so you are ready to start the lab.

## Slide 18

Now for the research lab, which takes the rest of class except the last five minutes.

Open the Week 7 README and click Open in Colab. Then choose File, Save a copy in Drive, and rename your copy Lastname_Week07_Research, using your own last name. You need no Supabase login, no password, and no installation. The notebook runs Python on data that is already inside it. Near the top, it shows the query from Part 4 of the midterm, the one that lists the newest open tickets. Everything you do today is about that query.

The lab has four steps, shown on these cards: inspect the data for about ten minutes, read two short sources for about ten minutes, write for about twenty-five minutes, and check your work for about five minutes. I will put each step on the screen when it is time, so you always know what to do next.

This writing gives you a head start on Part 4 of your README. Keep in mind that Python results describe the data. They do not show how PostgreSQL will run the query.

## Slide 19

Step one is inspecting the data, for about ten minutes. Run the code cells from the top. The first output gives you three counts, and they go in the first row of your observation table.

The next cell lists tickets with one status, newest first. Run it with the status set to open, and write down the ticket IDs in order. Then change the status to new, run it again, and write down that list too. Record the first list before you change anything, because the second run replaces the output.

Then inspect one ticket. Ticket 1004 is already filled in, and you may switch to another ID you saw. Record its status and its requester.

Two details trip people up. A blank assignee means nobody has been assigned yet; every ticket still has a requester. And MAX_ROWS is a ceiling of twenty, not a promise that twenty tickets match.

## Slide 20

Step two is reading, for about ten minutes. If your observation table is not finished, finish it first, then open the two PostgreSQL documentation pages linked in the notebook. Read only the parts shown on this slide.

On the first page, Indexes Introduction, read the opening example through the paragraph that begins, Once an index is created. Then read the final paragraph, about keeping an index synchronized with its table. Skip the discussion of operator classes.

On the second page, Indexes and ORDER BY, read the first three paragraphs, through the discussion of ORDER BY with LIMIT. The later examples are optional.

As you read, look for the three things at the bottom of the slide: what an index might let PostgreSQL avoid, why PostgreSQL might still choose another plan, and what extra work an index adds. Keep both links, because your writing uses them.

## Slide 21

Step three is writing, and it takes about twenty-five minutes. You write between one hundred eighty and two hundred fifty words in total, spread across the three response cells, A, B, and C. The table shows what each one needs.

Cell A, about fifty to seventy words, says what the query at the top of the notebook must return. Use two specific observations from your notebook, and explain why LIMIT 20 can return fewer than twenty rows in this dataset.

Cell B, about eighty to one hundred ten words, explains how an index could help the filter or the ordering, and names one cost. Use one idea from each source and keep both links. Then explain why finding an index definition online does not prove that this small database will run faster.

Cell C, about fifty to seventy words, describes one before-and-after test you will run in PostgreSQL for the midterm: what stays the same, which results and plan evidence you will compare, and what would make you keep or reconsider the index. Label your expected outcome as a prediction, and finish with one question you still need answered.

Write in your own words. To edit a response cell, double-click it.

## Slide 22

Step four is checking your work, for about five minutes before you submit. Go down the checklist on the left.

Every row of your observation table should come from your own outputs. Cells A, B, and C should hold your writing in place of the prompts, between one hundred eighty and two hundred fifty words in total. Both source links should still be there. Every observation you wrote should match an output above it, and your expected test result should be labeled as a prediction. If a cell failed to run, say so, and label any supplied example you used. Never invent an observation.

The box on the right shows what I look for: accurate observations, a connection between the two sources and this dataset, a test that compares the same query and results, and a clear line between what you observed and what you predict.

## Slide 23

We have five minutes left, so it is time to save and submit.

First, run every cell one more time, and then choose File, Save, so your outputs and your writing are stored in your Drive copy. Second, click Share and give me viewer access. Third, copy the link. Fourth, paste that link into today's classwork assignment in Brightspace.

Make sure you submit the link to your own saved copy, Lastname_Week07_Research. The link to the starter notebook on GitHub or in Colab does not contain your work. You do not need to upload a file or take screenshots.

Before you go, keep the two submissions separate in your mind. Today's notebook is classwork, and you submit its link now. The midterm is midterm.sql and README.md in one ZIP, due on the date in Brightspace. Next week, we cover backup and restore, and then we hold the midterm clinic. Bring one question and one working part of your project. Thank you, everyone, and I will see you next week.

## Slide 24

These short animations go with this week's reading. Students can watch them before class to preview the mechanisms, or afterwards to review: When does an index help? (1:44); Reading a query plan (0:55); Selectivity: why a Seq Scan can beat an index (1:07); How a B-tree index finds rows (0:58); Composite indexes: column order matters (1:08); Testing an index hypothesis (1:03). Each video is silent with on-screen captions and a subtitle file, and is linked from the Week 7 README. The diagrams are schematic illustrations, not benchmarks.

## License

Original course prose is licensed under CC BY-NC-SA 4.0. Source-specific notices control adapted material and external images. The transcript and the PowerPoint notes contain the same spoken script.
