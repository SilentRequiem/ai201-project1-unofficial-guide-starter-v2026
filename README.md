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

**3.** In Unit 2, I used Claude Enterprise to challenge my planned hybrid-search improvement. Claude pointed out that replacing cosine distances with fused BM25/vector scores could break my 0.6 relevance gate. I changed the design so BM25 only reranks the same five semantic candidates while preserving their original cosine distances. I then tested the change against the full evaluation and confirmed that the gate still refused all five out-of-scope questions.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---


---

# Unit 2

## Run Log — Before

Baseline evidence: `results/run_2026-09-23_1852.md`, produced by `run_eval.py::main` with retrieval from `store.py::search` and chunks from `chunker.py::split_documents`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stand on their own | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Answers return within 5 seconds | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

### Evidence — Before

**Criteria 1 and 2 — retrieval and source naming**

```text
Question: Which CS 210 exams are curved?
Best distance: 0.3631 (passed the gate)
Sources retrieved: course_cs_210.txt, course_cs_210_exams.txt, course_cs_340.txt, course_cs_340_exams.txt

According to the document `course_cs_210_exams.txt`, the midterms are curved, but the final is not.
```

Across the baseline run, all five in-scope questions were answered correctly in all three passes and every generated answer named a source.

**Criterion 3 — relevance gate**

```text
What is the capital of Mongolia?                             refused (0.787)
How do I change the oil in a diesel engine?                 refused (0.923)
Who won the 1994 World Cup?                                 refused (0.847)
What is the recommended dosage of ibuprofen for a headache? refused (0.849)
How do I write a for loop in Rust?                          refused (0.860)

Gate refused 5 of 5.
```

Produced by `run_eval.py::check_out_of_scope`.

**Criterion 4 — chunk quality**

The five sample chunks produced by `chunker.py::split_documents` are shown in the Unit 1 **Sample Chunks** section above. All five contained enough context to answer one clear question without another chunk.

**Criterion 5 — response time**

```text
Parking permits:      4.14s, 0.86s, 0.65s
Kestrel Commons:      0.67s, 0.71s, 0.61s
Morrow House laundry: 0.56s, 0.61s, 0.61s
CS 210 exams:         0.60s, 0.64s, 0.72s
Campus shuttle:       0.58s, 0.57s, 0.70s
```

All 15 measured baseline responses completed within 5 seconds.

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunks contain the answer | MET | All 5 test questions retrieved at least one chunk containing the expected answer in all three runs, exceeding my target of 4 of 5. |
| 2 | Every answer names a source | MET | All 15 generated answers named at least one source document, meeting my target of every answer naming a source. |
| 3 | Gate stops out-of-corpus questions | MET | The relevance gate refused all 5 out-of-scope questions, exceeding my target of at least 4 of 5. |
| 4 | Chunks stand on their own | MET | All 5 sample chunks contained enough information to answer one clear question without needing another chunk, exceeding my target of 4 of 5. |
| 5 | Answers return within 5 seconds | MET | All 15 baseline answers completed within 5 seconds, meeting my target of at least 4 of 5 questions finishing within 5 seconds. |

## Diagnoses

None of my five criteria were missed in the baseline evaluation. However, Criterion 1 was too forgiving because it only required the correct answer to appear somewhere in the top five retrieved chunks.

The CS 210 question exposed a retrieval-ranking weakness even though the criterion still passed. Before my improvement, semantic retrieval ranked `course_cs_340_exams.txt` first and `course_cs_340.txt` second. The correct `course_cs_210_exams.txt` result did not appear until rank 3.

The stage involved was retrieval. `store.py::search` ranked chunks using semantic similarity from the embedding model, so documents about CS courses and exams could be close in embedding space even when their exact course numbers differed. The retriever did not separately reward the exact identifier `CS 210`.

If I wrote Criterion 1 again, I would tighten it so that for at least 4 of my 5 questions, the top-ranked retrieved chunk must contain the answer instead of allowing the answer anywhere in the top five.

## The Improvement

**What I changed:** I added BM25 keyword reranking after semantic retrieval. Chroma still chooses the top five semantic candidates, then BM25 reranks those same five chunks using exact words and numbers from the question. I kept each result's original cosine distance so the relevance gate could continue using the same 0.6 cutoff.

**Why I picked it:** The CS 210 question showed that semantic similarity alone could rank CS 340 material above the exact course requested. BM25 gives exact terms such as `CS 210` more influence without changing the candidate set or replacing the semantic distance used by the gate.

### CS 210 Retrieval — Before

```text
1. course_cs_340_exams.txt   distance 0.3631
2. course_cs_340.txt         distance 0.4126
3. course_cs_210_exams.txt   distance 0.4138
4. course_cs_210_exams.txt   distance 0.4211
5. course_cs_210.txt         distance 0.4242
```

### CS 210 Retrieval — After

```text
1. course_cs_210_exams.txt   distance 0.4138
2. course_cs_340_exams.txt   distance 0.3631
3. course_cs_210_exams.txt   distance 0.4211
4. course_cs_340.txt         distance 0.4126
5. course_cs_210.txt         distance 0.4242
```

The candidate chunks and semantic distances stayed the same, but the exact CS 210 assessment document moved from rank 3 to rank 1.

### Run Log — After

After-improvement evidence: `results/run_2026-09-23_2006_after_bm25.md`, produced by `run_eval.py::main`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 2. Every answer names a source | 5 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 4. Chunks stand on their own | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |
| 5. Answers return within 5 seconds | 4 of 5 | 5 of 5 | 5 of 5 | 5 of 5 | MET |

### Evidence — After

```text
Parking permits:      pass/pass/pass — 3.25s, 0.46s, 0.60s
Kestrel Commons:      pass/pass/pass — 0.73s, 0.68s, 0.81s
Morrow House laundry: pass/pass/pass — 0.73s, 0.58s, 0.63s
CS 210 exams:         pass/pass/pass — 0.72s, 0.62s, 0.63s
Campus shuttle:       pass/pass/pass — 0.76s, 0.52s, 0.64s

Gate refused 5 of 5 out-of-scope questions.
```

**Did it help?**

Yes, but the improvement is visible in retrieval quality rather than the overall pass rate. The system already met all five acceptance criteria before the change, so the before and after criterion totals stayed the same. However, the CS 210 question improved from having a CS 340 document ranked first to having the correct `course_cs_210_exams.txt` document ranked first. The relevance gate also continued refusing all 5 out-of-scope questions, so the reranking did not break that behavior.

## What's Still Broken

None of my five acceptance criteria were missed after the improvement. The specific CS 210 ranking problem improved, but CS 340 chunks can still appear in the top five because BM25 only reranks the semantic candidates instead of removing semantically similar distractors. The reranker also cannot recover a useful chunk that semantic retrieval failed to include in the original top five. I stopped here because this unit asks for one measured improvement rather than several changes at once.

## What I'd Do Differently

I would make Criterion 1 stricter. Requiring the answer to appear anywhere in the top five let the CS 210 retrieval problem pass unnoticed. Next time I would require the top-ranked result to contain the answer for at least 4 of the 5 test questions so ranking quality is measured directly.
