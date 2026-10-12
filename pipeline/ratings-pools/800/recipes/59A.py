from rlib import *

CONSTRAINTS = "one word of 1..100 upper/lowercase Latin letters."
UNIQUENESS = "The corrected word is deterministic."
STATEMENT = "Reviewed full statement: uppercase iff strictly more uppercase letters, else lowercase (ties lowercase)."


def validate(inp):
    word(exact_tokens(inp, 1)[0], LETTERS, 1, 100)


def solve(inp):
    s = inp.split()[0]
    up = sum(c.isupper() for c in s)
    return s.upper() if up > len(s) - up else s.lower()


def extra():
    return [("boundary", "single uppercase", "A\n"), ("boundary", "single lowercase", "z\n"),
            ("adversarial", "exact tie -> lowercase", "aBcD\n"),
            ("adversarial", "one more uppercase", "aBC\n"),
            ("maxSize", "100 letters tie 50/50", "Ab" * 50 + "\n"), ("maxSize", "100 letters 51 uppercase", "A" * 51 + "b" * 49 + "\n")]
