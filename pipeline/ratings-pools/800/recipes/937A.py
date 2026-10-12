from rlib import *

CONSTRAINTS = "n in 1..100, n scores in 0..600, at least one nonzero."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: number of distinct nonzero scores."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100)
    need(len(t) == n + 1, "n scores")
    need(any(nums(t[1:], 0, 600)), "nonzero present")


def solve(inp):
    return str(len(set(inp.split()[1:]) - {"0"}))


def extra():
    return [("boundary", "n=1", "1\n600\n"), ("adversarial", "zeros and duplicates", "6\n0 3 0 3 2 0\n"),
            ("maxSize", "n=100 all distinct", "100\n" + joined(range(501, 601)) + "\n")]
