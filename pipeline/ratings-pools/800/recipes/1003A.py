from collections import Counter
from rlib import *

CONSTRAINTS = "n in 1..100, n values in 1..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: maximum multiplicity."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100)
    need(len(t) == n + 1, "n values")
    nums(t[1:], 1, 100)


def solve(inp):
    return str(max(Counter(inp.split()[1:]).values()))


def extra():
    return [("boundary", "n=1", "1\n1\n"), ("maxSize", "n=100 all same", "100\n" + joined([7] * 100) + "\n"),
            ("adversarial", "multiplicity tie", "6\n1 2 1 2 3 4\n")]
