# Teacher Cheat Sheet (Week 7 NoSQL Bridge Lab)
## Research-Based Guide for "If You Designed a Database System Today"

Use this as the instructor rationale and facilitation guide for the Week 7 NoSQL bridge lab.

The student-facing lab is:
- `lab_nosql_design_studio.md`

This guide explains:
- why the lab is structured the way it is,
- which pedagogy choices come from STEM and CS education research,
- what strong student responses should sound like,
- where to intervene during discussion.

---

## 1) Positioning Script
"We are not using this lab to replace SQL with buzzwords. We are using it to reason historically and architecturally. Strong database designers ask what problems SQL solved well, what new pressures changed the design space, and what responsibilities remain no matter which data model we choose."

---

## 2) Pedagogy Basis

### Active learning over passive lecture
Freeman et al. meta-analyzed 225 undergraduate STEM studies and found that active learning increased exam performance and lowered failure rates relative to traditional lecture.

Classroom implication:
- make students generate, classify, compare, and defend ideas,
- do not spend the whole bridge as a mini-history lecture.

### Interactive and constructive work beats passive reception
Chi and Wylie argue in the ICAP framework that engagement modes can be ordered from passive to active to constructive to interactive, with stronger learning expected as learners generate and co-construct ideas.

Classroom implication:
- start with individual thinking,
- move to pair comparison,
- then move to partner design,
- then close with instructor-led synthesis.

### Retrieval practice improves later retention
Roediger and Karpicke found that testing is not only assessment; retrieval itself improves later retention more than additional study on delayed tests.

Classroom implication:
- begin with a silent warm-up from memory,
- end with an individual exit ticket from memory,
- do not let students only reread definitions.

### Peer instruction in CS works best with instructor debrief
Zingaro and Porter showed that in introductory computing, peer discussion helps, but peer discussion plus instructor intervention produces larger gains, especially on harder questions. ACM's SIGCSE coverage of the multi-institutional peer-instruction study also highlights acceptance across seven diverse institutions and practical "do's and don'ts."

Classroom implication:
- let students discuss first,
- then do not skip the whole-class synthesis,
- reserve instructor time for the hardest conceptual tradeoff questions.

---

## 3) What the Lab Is Really Teaching
This lab is not mainly about MongoDB commands.

It is teaching:
1. historical reasoning:
- why NoSQL re-emerged.
2. comparative reasoning:
- what SQL-era systems got right.
3. workload reasoning:
- why different workloads invite different data models.
4. DBA continuity:
- why validation, indexing, backup, security, and observability still matter.

If students leave saying "NoSQL is newer," the lab failed.
If students leave saying "the right model depends on the workload, and the admin burden never disappears," the lab worked.

---

## 4) Why the Steps Are Ordered This Way

### Step 1: Silent retrieval
Purpose:
- surface prior knowledge from Weeks 1-7,
- make students commit to an answer before group influence,
- create a memory event that improves retention.

Instructor move:
- keep this silent and short,
- do not rescue too early.

### Step 2: Keep / Change / Why table
Purpose:
- force compare-and-contrast reasoning,
- prevent students from treating SQL and NoSQL as all-or-nothing camps,
- make them articulate reasons rather than labels.

Instructor move:
- ask "Why keep this?" and "Why change this?" until the answer names a workload or tradeoff.

### Step 3: Workload cards and partner design card
Purpose:
- shift from abstract history into concrete database-fit decisions,
- introduce the idea that different NoSQL families solve different dominant problems.

Instructor move:
- if a group picks a family too quickly, ask what query shape drove the decision.

### Step 4: Share-out and exit ticket
Purpose:
- close with retrieval and synthesis,
- make each student own a position independently of the group,
- keep the whole activity completable in one class meeting.

Instructor move:
- collect this even if the design cards stay informal.

---

## 5) High-Value Questions To Ask During the Lab
- What problem did SQL solve that you would definitely keep?
- What modern pressure makes you want to change the design?
- Is your answer about a workload, or is it just a product preference?
- What administrative problem still exists in your redesigned system?
- If your data model is more flexible, how will you stop schema drift?
- If your system scales out, what new consistency or coordination issue appears?

---

## 6) Strong Answer Shapes

### If students choose "still primarily relational"
Strong reasons:
- many joins,
- strong cross-entity integrity,
- broad reporting,
- stable schema,
- transactional correctness across many entities.

Weak reason:
- "SQL is normal so I trust it."

### If students choose "document"
Strong reasons:
- nested object-shaped data,
- read-together aggregates,
- evolving attributes,
- fewer joins for the dominant workflow.

Weak reason:
- "documents are easier because there is no schema."

### If students choose "key-value"
Strong reasons:
- known-key lookups,
- low-latency session or token retrieval,
- simple access pattern.

Weak reason:
- "it is faster than everything else."

### If students choose "graph"
Strong reasons:
- traversal-heavy questions,
- multi-hop relationship analysis,
- recommendations or fraud networks.

Weak reason:
- "it looks advanced."

### If students choose "column-family"
Strong reasons:
- wide sparse data,
- heavy write volume,
- time-windowed access patterns.

Weak reason:
- "it stores many columns."

---

## 7) Misconceptions To Correct Immediately
- "NoSQL means no schema."
- "If I designed a database today, I would not keep transactions."
- "Horizontal scaling removes the need for careful modeling."
- "MongoDB or NoSQL is automatically better because it is newer."
- "Different database families are just different brand names."

Preferred correction line:
"The modern design question is not old versus new. It is which guarantees and data shapes best fit the workload."

---

## 8) Compressed Flow
Recommended sequence:
1. Step 1 warm-up + pair check
2. Step 2 partner design card
3. Step 3 share-out + exit ticket

If class time is especially tight:
- cut the pair discussion shorter,
- keep only very short pair share-outs,
- do not remove the exit ticket.

If students are especially talkative:
- shorten oral share-outs, not retrieval or exit ticket.

## 9) Submission Logistics
For the shared artifact, keep grading simple:
- one partner submits the design card for the pair,
- the submitter must include both names at the top,
- use a line like `Submitted by: Name A | Partner: Name B`.

Each student should still complete an individual exit ticket.

---

## 10) Suggested Debrief Close
"SQL did not fail. It solved durable problems so well that many of its ideas still survive in newer systems. What changed is that different workloads made different tradeoffs worth making. That is why DBAs need model literacy, not just product familiarity."

---

## 11) Core References
- Freeman et al., "Active learning increases student performance in science, engineering, and mathematics" (PNAS, 2014): [https://pubmed.ncbi.nlm.nih.gov/24821756/](https://pubmed.ncbi.nlm.nih.gov/24821756/)
- Chi and Wylie, "The ICAP Framework: Linking Cognitive Engagement to Active Learning Outcomes" (Educational Psychologist, 2014 PDF): [https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf](https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf)
- Roediger and Karpicke, "Test-enhanced learning: taking memory tests improves long-term retention" (Psychological Science, 2006): [https://pubmed.ncbi.nlm.nih.gov/16507066/](https://pubmed.ncbi.nlm.nih.gov/16507066/)
- Zingaro and Porter, "Peer Instruction in computing: The value of instructor intervention" (Computers & Education, 2014): [https://www.sciencedirect.com/science/article/pii/S0360131513002777](https://www.sciencedirect.com/science/article/pii/S0360131513002777)
- ACM SIGCSE 2016 summary of "A Multi-institutional Study of Peer Instruction in Introductory Computing": [https://www.acm.org/media-center/2016/february/sigcse-2016](https://www.acm.org/media-center/2016/february/sigcse-2016)
- Peer Instruction for Computer Science research page: [https://peerinstruction4cs.com/latest-research](https://peerinstruction4cs.com/latest-research)
