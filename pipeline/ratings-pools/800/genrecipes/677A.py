from rlib import *

CONSTRAINTS = "n, h in 1..1000; heights in 1..2h."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: width 2 if height > h else 1."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n h")
    n, h = num(p[0], 1, 1000), num(p[1], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n heights")
    nums(a, 1, 2 * h)


def solve(inp):
    t = list(map(int, inp.split()))
    return str(sum(2 if a > t[1] else 1 for a in t[2:]))


def gen(rng):
    n, h = rng.choice([1, rng.randint(1, 1000), 1000]), rng.choice([1, rng.randint(1, 1000), 1000])
    return f"{n} {h}\n" + joined(rng.choice([h, h + 1, rng.randint(1, 2 * h)]) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "height equals h", "1 1\n1\n"), ("adversarial", "h and h+1", "2 5\n5 6\n"),
            ("maxSize", "n=1000 all 2h", "1000 1000\n" + joined([2000] * 1000) + "\n")]
