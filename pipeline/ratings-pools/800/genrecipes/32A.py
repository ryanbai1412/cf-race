from bisect import bisect_left, bisect_right
from rlib import *

CONSTRAINTS = "n in 1..1000; d in 1..10^9; n heights in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: ordered pairs i != j with |a_i - a_j| <= d."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n d")
    n, _ = num(p[0], 1, 1000), num(p[1], 1, 10 ** 9)
    a = ls[1].split(" ")
    need(len(a) == n, "n heights")
    nums(a, 1, 10 ** 9)


def solve(inp):
    t = list(map(int, inp.split()))
    d = t[1]; a = sorted(t[2:])
    return str(sum(bisect_right(a, x + d) - bisect_left(a, x - d) - 1 for x in a))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 1000), 1000])
    hi = rng.choice([5, 1000, 10 ** 9])
    d = rng.choice([1, rng.randint(1, hi), 10 ** 9])
    return f"{n} {d}\n" + joined(rng.randint(1, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1 1\n5\n"), ("adversarial", "difference exactly d counts", "2 3\n1 4\n"),
            ("maxSize", "n=1000 all pairs at max d", "1000 1000000000\n" + joined([10 ** 9] * 500 + [1] * 500) + "\n")]
