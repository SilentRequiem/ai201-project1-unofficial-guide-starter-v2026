"""
The scorer.

`run_eval.py` imports `judge` from this file and calls it once per run. It
decides the one thing the eval script deliberately won't: whether an answer was
right.

The first version of this was a substring test:

    return expects.lower().strip() in answer.lower()

That is a fine place to start and a bad place to stop. It only says yes when
the model happens to phrase things the way questions.py does, so it fails
answers that are correct:

    expects "20 to 25 minutes"  answer "Wait times run about 20-25 minutes."
    expects "Tuesday or Wednesday morning"
                                answer "Tuesday and Wednesday mornings are best."

Both of those are right and both score as failures, which makes the eval report
a measure of phrasing rather than of the system. So this version keeps the
substring test as a fast path and uses rapidfuzz for the near misses.

The rule underneath, once you strip the machinery out: an answer is correct
when everything `expects` asks for shows up in it, allowing for punctuation,
plurals, and a different word order.
"""

import re
import unicodedata

from rapidfuzz import fuzz, process

import gate

# How close two strings have to be to count as the same thing, 0-100. 85 is
# tight enough that "midterms" doesn't match "final" and loose enough that
# "morning" matches "mornings". If you move it, move it because you read a run
# log and disagreed with a verdict, and write down which one in criteria.md.
THRESHOLD = 85

# "three days" and "3 days" are the same answer. Only the small numbers are
# worth mapping - the ones that show up in a corpus about shuttle schedules and
# laundry rooms are all under thirteen.
NUMBER_WORDS = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "ten": "10", "eleven": "11", "twelve": "12",
}

# Words that carry no fact. "20 to 25 minutes" and "20-25 minutes" are the same
# claim; the only difference is the "to", and holding the answer to it is how
# the substring version got things wrong.
FILLER = {
    "a", "an", "the", "and", "or", "to", "of", "at", "in", "on", "for",
    "is", "are", "about", "around", "roughly", "approximately",
}


def normalize(text: str) -> str:
    """Flatten the differences that aren't differences.

    Unicode dashes and quotes become plain ones, punctuation becomes space,
    spelled-out small numbers become digits, and the whole thing ends up
    lowercase with single spaces. Both sides of every comparison below go
    through this, so "20-25 minutes." and "20 to 25 minutes" start out much
    closer than they look.
    """
    text = unicodedata.normalize("NFKD", text or "")
    text = text.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(NUMBER_WORDS.get(w, w) for w in text.split())


def content_words(text: str) -> list[str]:
    """The normalized words that actually carry the claim."""
    return [w for w in normalize(text).split() if w not in FILLER]


def numbers_in(text: str) -> set[str]:
    """Every number in the string, after normalize() has spelled them as digits."""
    return set(re.findall(r"\d+", normalize(text)))


def judge(question, expects, answer, results) -> bool:
    """Did this answer contain what we said a correct answer would contain?

    `question` and `results` come along because run_eval.py passes them and
    because a later version may want them - judging against the retrieved
    chunks instead of against a phrase is the obvious next step. This version
    looks only at `expects` and `answer`.
    """
    if not expects or not expects.strip():
        return False

    # A refusal is never a correct answer to a question we expected an answer
    # to. It's the right behavior for the out-of-scope list, but run_eval.py
    # puts those through the gate separately and never gets here with one.
    if gate.REFUSAL.lower() in (answer or "").lower():
        return False

    want, got = normalize(expects), normalize(answer)
    if not want or not got:
        return False

    # Fast path: the original substring test, now immune to punctuation and to
    # "three" vs "3". Most correct answers land here.
    if want in got:
        return True

    # Guard the fuzzy paths against the mistake they're most prone to.
    # "40 minutes" and "20 minutes" are 90% identical as strings and are
    # different answers, so if we asked for a number, the answer has to contain
    # at least one number we asked for. At least one, not all: an answer of
    # "about 20 minutes" against an expected "20 to 25 minutes" is a judgment
    # call, and the checks below get to make it rather than failing outright.
    wanted_numbers = numbers_in(expects)
    if wanted_numbers and not (wanted_numbers & numbers_in(answer)):
        return False

    # partial_ratio scores the best-matching window of the answer, which is
    # what "the answer contains this phrase somewhere" means once small edits
    # are allowed. It catches answers that quote the phrase almost verbatim.
    if fuzz.partial_ratio(want, got) >= THRESHOLD:
        return True

    # Otherwise, ask for every content word separately. This is the check that
    # handles a reworded answer - "Tuesday and Wednesday mornings are best"
    # against "Tuesday or Wednesday morning" - where no single window of the
    # answer lines up with the phrase but every piece of it is present.
    wanted = content_words(expects)
    if not wanted:
        return False
    answer_words = got.split()
    return all(
        process.extractOne(word, answer_words, scorer=fuzz.ratio)[1] >= THRESHOLD
        for word in wanted
    )


if __name__ == "__main__":
    # Cases worth keeping honest. Each one is either a phrasing that turned up
    # in a run log, or a wrong answer a looser scorer would have let through.
    CASES = [
        ("three days", "West lot permits usually sell out within three days.", True),
        ("three days", "They sell out in about 3 days.", True),
        ("three days", "Permits are gone by the end of the first week.", False),
        ("20 to 25 minutes", "Wait times run about 20-25 minutes at peak.", True),
        ("20 to 25 minutes", "Expect a 5 minute wait.", False),
        ("40 minutes", "The weekend shuttle runs every 20 minutes.", False),
        ("40 minutes", "On weekends it comes every 40 minutes.", True),
        (
            "Tuesday or Wednesday morning",
            "Tuesday and Wednesday mornings are the quietest.",
            True,
        ),
        (
            "Tuesday or Wednesday morning",
            "Sunday evening is the quietest time for laundry.",
            False,
        ),
        ("midterms", "Both midterms are curved; the final is not.", True),
        ("midterms", "Only the midterm is curved.", True),
        ("midterms", "The final exam is curved.", False),
        ("midterms", gate.REFUSAL, False),
        ("midterms", "", False),
    ]

    failures = 0
    for expects, answer, want in CASES:
        got = judge("", expects, answer, [])
        if got != want:
            failures += 1
        print(f"{'ok  ' if got == want else 'BAD '} expects={expects!r:32} -> {got}")
    print(f"\n{len(CASES) - failures}/{len(CASES)} as expected")
