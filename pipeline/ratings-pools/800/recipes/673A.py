from rlib import *

CONSTRAINTS = "n in 1..90, then strictly increasing t_i in 1..90."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: watch until first gap of 15 boring minutes, capped at 90."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 90)
    need(len(t) == n + 1, "n values")
    v = nums(t[1:], 1, 90)
    need(all(v[i] < v[i + 1] for i in range(n - 1)), "increasing")


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    prev = 0
    for x in t:
        if x - prev > 15:
            return str(prev + 15)
        prev = x
    return str(min(90, prev + 15))


def extra():
    return [("boundary", "single minute 1", "1\n1\n"), ("boundary", "single minute 16 (first gap 15 boring)", "1\n16\n"),
            ("adversarial", "gap exactly 15 boring then stop", "2\n15 31\n"),
            ("adversarial", "last interesting 75 -> 90", "5\n15 30 45 60 75\n"),
            ("maxSize", "all 90 minutes", "90\n" + joined(range(1, 91)) + "\n")]
