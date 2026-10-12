from rlib import *

CONSTRAINTS = "a1 a2 a3 in 0..100; b1 b2 b3 in 0..100; n in 1..100, one group per line."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: ceil(sum a/5) + ceil(sum b/10) <= n."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    a, b = ls[0].split(" "), ls[1].split(" ")
    need(len(a) == 3 and len(b) == 3, "three per line")
    nums(a, 0, 100); nums(b, 0, 100); num(ls[2], 1, 100)


def solve(inp):
    t = list(map(int, inp.split()))
    return yn(-(-sum(t[:3]) // 5) + -(-sum(t[3:6]) // 10) <= t[6])


def extra():
    return [("boundary", "everything zero", "0 0 0\n0 0 0\n1\n"), ("boundary", "one cup one medal one shelf", "1 0 0\n0 0 1\n1\n"),
            ("adversarial", "exact fit 5 cups and 10 medals on 2 shelves", "2 2 1\n5 5 0\n2\n"),
            ("maxSize", "all maximum, needs 60+30=90 shelves", "100 100 100\n100 100 100\n100\n"),
            ("maxSize", "all maximum cups, 89 shelves", "100 100 100\n100 100 100\n89\n")]
