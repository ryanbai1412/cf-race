from rlib import *

CONSTRAINTS = "n in 1..20, n integers in 1..25; per-muscle totals have a unique maximum (guaranteed)."
UNIQUENESS = "Statement guarantees unambiguous answer; validator enforces a strict maximum."
STATEMENT = "Reviewed full statement: cyclic chest/biceps/back totals, print the muscle with largest total."


def totals(a):
    s = [0, 0, 0]
    for i, x in enumerate(a):
        s[i % 3] += x
    return s


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 20)
    need(len(t) == n + 1, "n values")
    s = totals(nums(t[1:], 1, 25))
    need(s.count(max(s)) == 1, "unambiguous maximum")


def solve(inp):
    t = list(map(int, inp.split()))
    s = totals(t[1:])
    return ("chest", "biceps", "back")[s.index(max(s))]


def extra():
    return [("boundary", "n=1 chest", "1\n1\n"), ("boundary", "n=2 biceps larger", "2\n1 2\n"),
            ("adversarial", "back wins by one", "6\n10 10 11 1 1 1\n"),
            ("adversarial", "chest accumulates over cycles", "7\n5 9 9 5 1 1 5\n"),
            ("maxSize", "n=20 max values, biceps total reduced by final 1", "20\n" + joined([25] * 19 + [1]) + "\n")]
