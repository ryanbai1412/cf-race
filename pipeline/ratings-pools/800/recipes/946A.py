from rlib import *

CONSTRAINTS = "n in 1..100, n integers in -100..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: sum of absolute values."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100)
    need(len(t) == n + 1, "n values")
    nums(t[1:], -100, 100)


def solve(inp):
    return str(sum(abs(int(x)) for x in inp.split()[1:]))


def extra():
    return [("boundary", "single zero", "1\n0\n"), ("adversarial", "all negative", "3\n-1 -100 -5\n"),
            ("maxSize", "n=100 all -100", "100\n" + joined([-100] * 100) + "\n")]
