from rlib import *

CONSTRAINTS = "n, m in 1..1000; c_i, a_j in 1..1000."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: scan games; buy with the first bill when bill >= cost, which then disappears."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 3, "three lines")
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 1000), num(p[1], 1, 1000)
    c, a = ls[1].split(" "), ls[2].split(" ")
    need(len(c) == n and len(a) == m, "lengths")
    nums(c, 1, 1000); nums(a, 1, 1000)


def solve(inp):
    _, c, a = lines(inp)
    a = list(map(int, a.split())); j = 0
    for x in map(int, c.split()):
        if j < len(a) and a[j] >= x:
            j += 1
    return str(j)


def gen(rng):
    n, m = rng.choice([1, rng.randint(1, 1000), 1000]), rng.choice([1, rng.randint(1, 1000), 1000])
    hi = rng.choice([2, 1000])
    return f"{n} {m}\n" + joined(rng.randint(1, hi) for _ in range(n)) + "\n" + joined(rng.randint(1, hi) for _ in range(m)) + "\n"


def extra():
    return [("boundary", "single exact bill", "1 1\n5\n5\n"), ("adversarial", "more bills than games", "2 5\n1 1\n1000 1000 1000 1000 1000\n"),
            ("maxSize", "n=m=1000", "1000 1000\n" + joined([1000] * 1000) + "\n" + joined([1000] * 1000) + "\n")]
