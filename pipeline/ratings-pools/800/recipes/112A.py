from rlib import *

CONSTRAINTS = "two strings of equal length 1..100 of upper/lowercase Latin letters."
UNIQUENESS = "Comparison result -1/0/1 is unique."
STATEMENT = "Reviewed full statement: case-insensitive lexicographic comparison."


def validate(inp):
    a, b = exact_tokens(inp, 2)
    word(a, LETTERS, 1, 100); word(b, LETTERS, 1, 100)
    need(len(a) == len(b), "equal lengths")


def solve(inp):
    a, b = (x.lower() for x in inp.split())
    return "-1" if a < b else "1" if a > b else "0"


def extra():
    r = rng(112)
    a = "".join(r.choice(LETTERS) for _ in range(100))
    return [("boundary", "single equal letters different case", "a\nA\n"), ("boundary", "single letters less", "a\nB\n"),
            ("adversarial", "uppercase Z vs lowercase a: ASCII order would mislead", "Z\na\n"),
            ("maxSize", "length 100 equal ignoring case", f"{a}\n{a.swapcase()}\n"),
            ("maxSize", "length 100 differ at last char", "a" * 99 + "b\n" + "A" * 100 + "\n")]
