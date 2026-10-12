from rlib import *

CONSTRAINTS = "two integers a, b in 1..6."
UNIQUENESS = "Three counts are unique."
STATEMENT = "Reviewed full statement: count die faces where |a-x| < |b-x|, ==, >."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 6)


def solve(inp):
    a, b = map(int, inp.split())
    w = sum(abs(a - x) < abs(b - x) for x in range(1, 7))
    d = sum(abs(a - x) == abs(b - x) for x in range(1, 7))
    return joined([w, d, 6 - w - d])


def extra():
    return [("boundary", "a=b=1 all draws", "1 1\n"), ("boundary", "1 6", "1 6\n"),
            ("adversarial", "adjacent numbers no draw", "3 4\n"), ("adversarial", "even gap draw at 4", "6 2\n"),
            ("maxSize", "a=b=6", "6 6\n")]
