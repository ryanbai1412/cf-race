from rlib import *

CONSTRAINTS = "two integers a, b in 1..100."
UNIQUENESS = "Two counts are unique."
STATEMENT = "Reviewed full statement: min(a,b) and |a-b|//2."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 100)


def solve(inp):
    a, b = map(int, inp.split())
    return joined([min(a, b), abs(a - b) // 2])


def extra():
    return [("boundary", "1 1", "1 1\n"), ("boundary", "1 2", "1 2\n"), ("adversarial", "1 100", "1 100\n"),
            ("maxSize", "100 100", "100 100\n"), ("maxSize", "100 1", "100 1\n")]
