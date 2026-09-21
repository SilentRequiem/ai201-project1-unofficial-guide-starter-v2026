# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Because the CS 210 exams question is a different topic from the other four. It uses course-specific information instead of campus location or service information, so I think the system may have a harder time retrieving the correct chunk. That is why I chose 4 out of 5 instead of 5 out of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
It is important to know where every result came from, even if the answer is incorrect or unrelated. Having a source for every answer makes it easier to check whether the system is actually using the documents.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I chose 4 out of 5 because I want the system to reject most unrelated questions while keeping the cutoff somewhat loose so relevant questions are less likely to be rejected.

---

## 4. Something about your chunks

If you printed 5 chunks, what would make you say “these chunks are good”?


**Why this target:**

Out of 5 sample chunks, at least 4 should be able to answer one clear question without needing another chunk.

> **Revised in unit 2:** Out of 5 sample chunks, at least 4 should be able to answer one clear question without needing another chunk.
>
> **Why revised:** My original Criterion 4 was written as a question instead of a measurable target. I revised it so another person could test it consistently.
>
> **Why this target:** I chose 4 out of 5 because most chunks should stand on their own, while still allowing one chunk to be less clear if information is split between topics or paragraphs.

---

## 5. Your choice

For at least 4 of my 5 test questions, the system should return a complete answer within 5 seconds.


**Why this target:**

I chose 5 seconds because the system needs time to retrieve the relevant chunks and generate an answer, but I still want the response to feel fast for the user.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
