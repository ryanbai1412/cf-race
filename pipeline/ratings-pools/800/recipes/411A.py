from rlib import *

ALPHA = LETTERS + DIGITS + "!?.,_"
CONSTRAINTS = "one nonempty line of at most 100 chars from letters, digits and !?.,_"
UNIQUENESS = "Exactly one of two fixed messages."
STATEMENT = "Reviewed full statement: length >= 5 and contains uppercase, lowercase and digit."


def validate(inp):
    word(exact_tokens(inp, 1)[0], ALPHA, 1, 100)


def solve(inp):
    s = inp.split()[0]
    ok = len(s) >= 5 and any(c.isupper() for c in s) and any(c.islower() for c in s) and any(c.isdigit() for c in s)
    return "Correct" if ok else "Too weak"


def extra():
    return [("boundary", "single char", "a\n"), ("boundary", "length exactly 5 complete", "aB1!_\n"),
            ("adversarial", "length 4 with all classes", "aB1?\n"), ("adversarial", "no digit, symbols", "abcDE.,!?\n"),
            ("maxSize", "length 100 punctuation plus one of each class at end", "_" * 97 + "aZ9\n"),
            ("maxSize", "length 100 missing uppercase", "a1" * 50 + "\n")]
