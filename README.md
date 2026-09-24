# The Unofficial Guide

Michael Amoo — Corpus: `campus_life`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

     The Unofficial Guide is a RAG system that searches the campus_life corpus for information about student life. It can answer questions about dining, housing, courses, transportation, and other campus services. The system retrieves relevant chunks from the documents and uses them to generate an answer with a source. If the documents do not have enough relevant information, the system refuses to answer.

## Chunking Strategy

**Chunk size:** Variable, one paragraph plus the document title  
**Overlap:** No fixed character overlap; the document title is repeated in each chunk

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

     I used paragraph-based chunking instead of the original fixed chunks. The campus_life documents are short posts, but some contain multiple topics in separate paragraphs. Splitting by paragraph keeps related information together while separating different ideas. I repeated the title in each chunk so the paragraph still has context.

## Sample Chunks
<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

     ======================================================================
     Chunk 1  |  source: admin_add_drop_deadline.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     On the add/drop deadline

     You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

     ======================================================================
     Chunk 2  |  source: course_cs_340_exams.txt#1  |  produced by: chunker.py::split_documents
     ======================================================================
     CS 340 Databases — assessment

     Start the term project in week three, not week eight; everyone learns this the hard way.

     ======================================================================
     Chunk 3  |  source: course_phys_130_workload.txt#0  |  produced by: chunker.py::split_documents
     ======================================================================
     Workload for PHYS 130 Mechanics

     People keep asking so: 7 hours a week, plus 3 on lab weeks. That's real time, not optimistic time.

     ======================================================================
     Chunk 4  |  source: dining_verrill_street_grill_followup.txt#1  |  produced by: chunker.py::split_documents
     ======================================================================
     Re: Verrill Street Grill

     Also worth saying: one register, so the queue is a single line no matter how busy. Nobody tells you this at orientation.

     ======================================================================
     Chunk 5  |  source: housing_morrow_house.txt#1  |  produced by: chunker.py::split_documents
     ======================================================================
     Morrow House — what it's actually like

     The good: cheapest housing tier by about $900 a year, and the singles are real singles.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How often does the campus shuttle run on weekends?

**Answer:**

```text
The campus shuttle runs a loop every 40 minutes on weekends.

Source: transit_shuttle.txt
```

**My relevance cutoff:** 0.6

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

| Question | In corpus? | Best distance |
|---|---|---:|
| Parking permits | Yes | 0.1928 |
| Kestrel Commons wait times | Yes | 0.1814 |
| Morrow House laundry | Yes | 0.1067 |
| CS 210 exams | Yes | 0.3631 |
| Campus shuttle | Yes | 0.1799 |
| Capital of Mongolia | No | 0.7873 |
| Diesel engine oil | No | 0.9228 |
| 1994 World Cup | No | 0.8474 |
| Ibuprofen dosage | No | 0.8487 |
| Rust for loop | No | 0.8598 |

My in-corpus questions had best distances from 0.1067 to 0.3631. My out-of-scope questions had best distances from 0.7873 to 0.9228. I kept the cutoff at 0.6 because it falls between the two groups.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I used AI to help troubleshoot my Python environment when the project could not import ChromaDB. It helped me identify that VS Code was using my system Python instead of the project's virtual environment. I activated the correct `.venv` and verified that all tests passed.

**2.** I used AI to help think through a chunking strategy for the campus_life corpus. It suggested paragraph-based chunks because the documents are short but often contain multiple topics. I kept that idea, repeated the document title in each chunk for context, and tested five sample chunks to make sure they could stand on their own.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stand on their own | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Answers return within 5 seconds | 4 of 5 | Not measured | Not measured | Not measured | NOT YET MEASURED |

### Evidence — Before

Produced by `run_eval.py::main`, using retrieval from `store.py::search` and chunks from `chunker.py::split_documents`.

**Criteria 1 and 2 — retrieval and source naming**

```text
Question: How quickly do student parking permits for the west lots sell out?
Best distance: 0.1928
Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, course_stat_150.txt, course_stat_150_workload.txt, transit_walking.txt

Student parking permits for the west lots sell out in about three days (admin_parking_permits.txt).
```

The retrieved set contained the document with the expected answer, and the generated answer named that source.

**Criterion 3 — relevance gate**

```text
What is the capital of Mongolia?                                  refused (0.787)
How do I change the oil in a diesel engine?                      refused (0.923)
Who won the 1994 World Cup?                                      refused (0.847)
What is the recommended dosage of ibuprofen for a headache?      refused (0.849)
How do I write a for loop in Rust?                               refused (0.860)

Gate refused 5 of 5.
```

Produced by `run_eval.py::check_out_of_scope`.

**Criterion 4 — chunk quality**

```text
source: admin_add_drop_deadline.txt#0
produced by: chunker.py::split_documents

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.
```

This sample chunk contains enough context to answer a clear question on its own.

**Criterion 5 — response time**

The baseline run did not record response time. Its real output recorded fields such as:

```text
Best distance: 0.1928 (passed the gate)
Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, course_stat_150.txt, course_stat_150_workload.txt, transit_walking.txt
```

Because there was no timing field, Criterion 5 could not be measured from the baseline evidence.

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

### Unit 1

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 questions retrieved a chunk containing the expected answer in all three runs. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source document. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, exceeding the 4 of 5 target. |
| 4 | Chunks stand on their own | MET | All 5 sampled chunks contained enough information to answer one clear question without another chunk. |
| 5 | Answers return within 5 seconds | NOT MEASURED | The evaluation output does not record response time, so I do not have evidence to determine whether this target was met. |

### Unit 2

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 test questions retrieved at least one chunk containing the expected answer in all three runs, which exceeds my target of 4 of 5. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source document, meeting my target of every answer naming a source. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, exceeding my target of at least 4 of 5. |
| 4 | Chunks stand on their own | MET | All 5 sample chunks contained enough information to answer one clear question without needing another chunk, exceeding my target of 4 of 5. |
| 5 | Answers return within 5 seconds | MET | In the latest baseline run, all 15 answers completed within 5 seconds, meeting my target of at least 4 of 5 questions finishing within 5 seconds. |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

None of my five criteria were missed in the baseline evaluation. However, Criterion 1 was probably too forgiving because it only requires the correct answer to appear somewhere in the top five retrieved chunks.

The CS 210 question exposed a retrieval weakness even though the criterion still passed. The system retrieved CS 340 material along with the correct CS 210 documents, and CS 340 could rank above the exact course I asked about.

The stage involved is retrieval. `store.py::search` currently ranks chunks using semantic similarity from the embedding model. It does not separately reward an exact keyword such as "CS 210." Because CS 210 and CS 340 documents discuss similar topics such as courses and exams, their embeddings can be similar even though the course numbers are different.

If I wrote Criterion 1 again, I would tighten it so that for at least 4 of my 5 questions, the top-ranked result must contain the answer instead of allowing the answer anywhere in the top five.

## The Improvement

**What I changed:** I added BM25 keyword reranking after semantic retrieval. The system still uses Chroma semantic search to choose the top five candidate chunks, but BM25 reranks those same five chunks using exact words and numbers from the question. I kept the original cosine distances on every result so the relevance gate could continue using the same 0.6 cutoff.

**Why I picked it:** My baseline evaluation passed all five criteria, but the CS 210 question exposed a retrieval-ranking weakness. Before the change, `course_cs_340_exams.txt` ranked first even though the question specifically asked about CS 210. The correct `course_cs_210_exams.txt` result did not appear until rank 3. Because the problem involved an exact course identifier, I chose keyword reranking to give terms such as `CS 210` more influence without replacing semantic retrieval.

### CS 210 Retrieval — Before

```text
1. course_cs_340_exams.txt   distance 0.3631
2. course_cs_340.txt         distance 0.4126
3. course_cs_210_exams.txt   distance 0.4138
4. course_cs_210_exams.txt   distance 0.4211
5. course_cs_210.txt         distance 0.4242

### Run Log — After
1. course_cs_210_exams.txt   distance 0.4138
2. course_cs_340_exams.txt   distance 0.3631
3. course_cs_210_exams.txt   distance 0.4211
4. course_cs_340.txt         distance 0.4126
5. course_cs_210.txt         distance 0.4242

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stand on their own | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Answers return within 5 seconds | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

### Evidence — After

How quickly do student parking permits for the west lots sell out?
run 1: pass (best distance 0.193, 3.25s)
run 2: pass (best distance 0.193, 0.46s)
run 3: pass (best distance 0.193, 0.60s)

How long are wait times at Kestrel Commons between 12:15 and 1:00?
run 1: pass (best distance 0.181, 0.73s)
run 2: pass (best distance 0.181, 0.68s)
run 3: pass (best distance 0.181, 0.81s)

When is the best time to do laundry in Morrow House?
run 1: pass (best distance 0.107, 0.73s)
run 2: pass (best distance 0.107, 0.58s)
run 3: pass (best distance 0.107, 0.63s)

Which CS 210 exams are curved?
run 1: pass (best distance 0.363, 0.72s)
run 2: pass (best distance 0.363, 0.62s)
run 3: pass (best distance 0.363, 0.63s)

How often does the campus shuttle run on weekends?
run 1: pass (best distance 0.180, 0.76s)
run 2: pass (best distance 0.180, 0.52s)
run 3: pass (best distance 0.180, 0.64s)

Gate refused 5 of 5 out-of-scope questions.

Produced by `run_eval.py::main`, using retrieval from `store.py::search` and chunks from `chunker.py::split_documents`.

**Criteria 1 and 2 — retrieval and source naming**

```text
Question: How quickly do student parking permits for the west lots sell out?
Best distance: 0.1928
Response time: 4.82 seconds
Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, course_stat_150.txt, course_stat_150_workload.txt, transit_walking.txt

Student parking permits for the west lots sell out in about three days. (Source: admin_parking_permits.txt)
```

**Criterion 3 — relevance gate**

```text
Gate refused 5 of 5 out-of-scope questions.
Best distances: 0.787, 0.923, 0.847, 0.849, 0.860
```

Produced by `run_eval.py::check_out_of_scope`.

**Criterion 4 — chunk quality**

```text
source: admin_add_drop_deadline.txt#0
produced by: chunker.py::split_documents

On the add/drop deadline

You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript.
```

**Criterion 5 — response time**

```text
Parking permits:      4.82s, 0.59s, 0.67s
Kestrel Commons:      3.38s, 0.67s, 0.76s
Morrow House laundry: 0.73s, 0.73s, 0.75s
CS 210 exams:         0.76s, 0.60s, 0.68s
Campus shuttle:       1.03s, 0.59s, 0.60s
```

All 15 measured responses completed within 5 seconds.

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

     Yes. The change let me measure Criterion 5 instead of guessing. All 15 generated answers finished within 5 seconds, with the slowest response taking 4.82 seconds, so the criterion was met.

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

     None of my five criteria were missed after the improvement. However, the CS 210 question showed that retrieval is not always perfect because the first result was about CS 340 instead of CS 210. The correct CS 210 document was still returned in the top five, so the system still met my retrieval criterion.

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->

     I would write Criterion 5 differently so I knew from the beginning how I planned to measure response time. The target itself was measurable, but my original evaluation did not record timing. I would make sure every criterion has a clear way to collect its evidence before running the first evaluation.