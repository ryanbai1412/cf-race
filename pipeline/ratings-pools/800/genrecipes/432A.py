from rlib import *

CONSTRAINTS = "n in 1..2000; k in 1..5; y_i in 0..5."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: floor(count of y_i + k <= 5 over 3)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n k")
    n, _ = num(p[0], 1, 2000), num(p[1], 1, 5)
    y = ls[1].split(" ")
    need(len(y) == n, "n values")
    nums(y, 0, 5)


def solve(inp):
    t = list(map(int, inp.split()))
    k = t[1]
    return str(sum(y + k <= 5 for y in t[2:]) // 3)


def gen(rng):
    n = rng.choice([1, 2, 3, rng.randint(1, 2000), 2000]); k = rng.randint(1, 5)
    return f"{n} {k}\n" + joined(rng.randint(0, 5) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "exactly three at the limit", "3 5\n0 0 0\n"), ("adversarial", "y + k = 6 excluded", "3 1\n5 4 4\n"),
            ("maxSize", "n=2000 all eligible", "2000 1\n" + joined([0] * 2000) + "\n")]
