"""
The scorer.

`run_eval.py` imports `judge` from this file and calls it once per run. It
decides the one thing the eval script deliberately won't: whether an answer was
right.

The first version of this was a substring test:

    return expects.lower().strip() in answer.lower()

That is a fine place to start and a bad place to stop. It only ever says yes
when the model happens to phrase things the way questions.py does, so it fails
answers that are correct:

    expects "20 to 25 minutes"  answer "Wait times run about 20-25 minutes."
    expects "Tuesday or Wednesday morning"
                                answer "Tuesday and Wednesday mornings are best."

Both of those are right and both score as failures, which makes the eval report
a measure of phrasing rather than of the system. So this version keeps the
substring test as a fast path and falls back to rapidfuzz for the near misses.
"""

import re
import unicodedata

from rapidfuzz import fuzz

import gate

# How close a fuzzy match has to be, 0-100. 85 is tight enough that a different
# fact doesn't slip through and loose enough to survive punctuation, plurals,
# and an inserted "about". If you move it, move it because you read run output
# and disagreed with a verdict, and write down which one in criteria.md.
THRESHOLD = 85

# "three days" and "3 days" are the same answer. Only the small numbers are
# worth mapping - nobody writes "forty" in a corpus about shuttle schedules,
# and the ones that matter here are all under thirteen.
NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12",
}


def normalize(text: str) -> str:
    """Flatten the differences that aren't differences.

    Unicode dashes become plain ones, punctuation becomes space, spelled-out
    small numbers become digits, and the whole thing goes to lowercase with
    single spaces. This is what both sides of every comparison below run
    through, so "20-25 minutes." and "20 to 25 minutes" start out closer than
    they look.
    """
    text = unicodedata.normalize("NFKD", text or "")
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    words = [NUMBER_WORDS.get(w, w) for w in text.split()]
    return " ".join(words)


def numbers_in(text: str) -> set[str]:
    """Every number in the string, after normalize() has spelled them as digits."""
    return set(re.findall(r"\d+", normalize(text)))


def judge(question, expects, answer, results) -> bool:
    """Did this answer contain what we said a correct answer would contain?

    `question` and `results` come along because run_eval.py passes them and
    because a later version might want them - judging against the retrieved
    chunks rather than against a phrase is the obvious next step. This version
    only looks at `expects` and `answer`.
    """
    if not expects or not expects.strip():
        return False

    # A refusal is never a correct answer to a question we expected an answer
    # to. It's the right behavior for the out-of-scope list, but run_eval.py
    # checks those separately, through the gate.
    if gate.REFUSAL.lower() in (answer or "").lower():
        return False

    want = normalize(expects)
    got = normalize(answer)
    if not want or not got:
        return False

    # Fast path: the original substring test, now immune to punctuation and
    # "three" vs "3". Most correct answers land here.
    if want in got:
        return True

    # Guard the fuzzy path against the failure it's most prone to. "40 minutes"
    # and "20 minutes" are 90% identical as strings and are different answers,
    # so if we asked for a number, the answer has to contain at least one of
    # the numbers we asked for. One, not all: an answer of "about 20 minutes"
    # to an expected "20 to 25 minutes" is a judgment call, and this leaves
    # that call to the score below instead of failing it outright.
    wanted_numbers = numbers_in(expects)
    if wanted_numbers and not (wanted_numbers & numbers_in(answer)):
        return False

    # partial_ratio finds the best-matching window of the answer, which is what
    # "the answer contains this phrase somewhere" means once you allow for
    # small edits. partial_token_sort_ratio does the same after sorting words,
    # which is what catches "Tuesday and Wednesday mornings" against
    # "Tuesday or Wednesday morning".
    score = max(
        fuzz.partial_ratio(want, got),
        fuzz.partial_token_sort_ratio(want, got),
    )
    return score >= THRESHOLD


if __name__ == "__main__":
    # Cases worth keeping honest. Each one is a phrasing that showed up in a
    # run log, or a wrong answer that a looser scorer would have let through.
    CASES = [
        ("three days", "West lot permits usually sell out within three days.", True),
        ("three days", "They sell out in about 3 days.", True),
        ("20 to 25 minutes", "Wait times run about 20-25 minutes at peak.", True),
        ("20 to 25 minutes", "Expect a 5 minute wait.", False),
        ("40 minutes", "The weekend shuttle runs every 20 minutes.", False),
        ("40 minutes", "On weekends it comes every 40 minutes.", True),
        (
            "Tuesday or Wednesday morning",
            "Tuesday and Wednesday mornings are the quietest.",
            True,
        ),
        ("midterms", "Both midterms are curved; the final is not.", True),
        ("midterms", "The final exam is curved.", False),
        ("midterms", gate.REFUSAL, False),
    ]

    failures = 0
    for expects, answer, want in CASES:
        got = judge("", expects, answer, [])
        if got != want:
            failures += 1
        mark = "ok  " if got == want else "BAD "
        print(f"{mark} expects={expects!r:32} -> {got}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} as expected")
