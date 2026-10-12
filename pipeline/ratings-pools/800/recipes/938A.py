from rlib import *

CONSTRAINTS = "n in 1..100, then a lowercase word of exactly n letters."
UNIQUENESS = "Correction result is deterministic."
STATEMENT = "Reviewed full statement: vowels aeiouy; drop any vowel preceded by a kept vowel."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 100)
    word(t[1], LOWER, n, n)


def solve(inp):
    out = []
    for c in inp.split()[1]:
        if not (out and out[-1] in "aeiouy" and c in "aeiouy"):
            out.append(c)
    return "".join(out)


def extra():
    return [("boundary", "n=1", "1\na\n"), ("adversarial", "y counts as vowel", "4\nyaya\n"),
            ("maxSize", "100 vowels collapse to one", "100\n" + "aeiouy" * 16 + "aeio\n"), ("maxSize", "100 consonants", "100\n" + "b" * 100 + "\n")]
