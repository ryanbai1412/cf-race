from rlib import *

CONSTRAINTS = "n, x in 1..1000; n integers with |a_i| <= x."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: ceil(|sum| / x) more cards."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n x")
    n, x = num(p[0], 1, 1000), num(p[1], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n cards")
    nums(a, -x, x)


def solve(inp):
    t = list(map(int, inp.split()))
    s = abs(sum(t[2:])); x = t[1]
    return str((s + x - 1) // x)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 1000), 1000]); x = rng.choice([1, rng.randint(1, 1000), 1000])
    lo = rng.choice([-x, 0])
    return f"{n} {x}\n" + joined(rng.randint(lo, x) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "sum already zero", "2 5\n-5 5\n"), ("adversarial", "exact multiple of x", "3 4\n4 4 -4\n"),
            ("maxSize", "n=1000 all -1000", "1000 1000\n" + joined([-1000] * 1000) + "\n")]
