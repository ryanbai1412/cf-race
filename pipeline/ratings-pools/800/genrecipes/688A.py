from rlib import *

CONSTRAINTS = "n, d in 1..100; d lines of n characters from '01'."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: longest run of days where some opponent is absent ('0' present in the line)."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n d")
    n, d = num(p[0], 1, 100), num(p[1], 1, 100)
    need(len(ls) == d + 1, "d days")
    for s in ls[1:]:
        word(s, "01", n, n)


def solve(inp):
    best = cur = 0
    for s in lines(inp)[1:]:
        cur = cur + 1 if "0" in s else 0
        best = max(best, cur)
    return str(best)


def gen(rng):
    n, d = rng.choice([1, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    p = rng.choice([0.0, 0.01, 0.5, 0.99, 1.0])
    return f"{n} {d}\n" + "".join("".join("1" if rng.random() < p else "0" for _ in range(n)) + "\n" for _ in range(d))


def extra():
    return [("boundary", "single all-present day", "1 1\n1\n"), ("adversarial", "best run at the end", "2 4\n00\n11\n01\n10\n"),
            ("maxSize", "100x100 alternating", "100 100\n" + "".join(("1" * 100 if i % 7 == 0 else "1" * 99 + "0") + "\n" for i in range(100)))]
