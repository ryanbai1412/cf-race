from rlib import *

CONSTRAINTS = "n in 2..100, s in 1..1000, then n mug volumes in 1..10."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: n-1 friends pour n-1 mugs; YES iff sum minus largest mug <= s."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 2, 100); num(t[1], 1, 1000)
    need(len(t) == n + 2, "n volumes")
    nums(t[2:], 1, 10)


def solve(inp):
    t = list(map(int, inp.split()))
    s, a = t[1], t[2:]
    return yn(sum(a) - max(a) <= s)


def extra():
    return [("boundary", "n=2 exact fit", "2 1\n1 10\n"), ("boundary", "n=2 overflow", "2 1\n2 2\n"),
            ("adversarial", "sum minus max equals s exactly", "4 15\n5 5 5 10\n"),
            ("maxSize", "n=100 all 10, s=990 exact", "100 990\n" + joined([10] * 100) + "\n"),
            ("maxSize", "n=100 all 10, s=989", "100 989\n" + joined([10] * 100) + "\n")]
