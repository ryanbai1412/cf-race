from rlib import *

CONSTRAINTS = "n, m in 1..100; n rows of m space-separated colors from CMYWGB."
UNIQUENESS = "Fixed word."
STATEMENT = "Reviewed full statement: #Color if any C/M/Y pixel else #Black&White."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 100), num(p[1], 1, 100)
    need(len(ls) == n + 1, "n rows")
    for l in ls[1:]:
        r = l.split(" ")
        need(len(r) == m and all(c in ("C", "M", "Y", "W", "G", "B") for c in r), "row")


def solve(inp):
    return "#Color" if any(c in "CMY" for c in inp.split()[2:]) else "#Black&White"


def gen(rng):
    n, m = rng.choice([1, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    g = [[rng.choice("WGB") for _ in range(m)] for _ in range(n)]
    if rng.random() < 0.5:
        g[rng.randrange(n)][rng.randrange(m)] = rng.choice("CMY")
    return f"{n} {m}\n" + "".join(" ".join(r) + "\n" for r in g)


def extra():
    return [("boundary", "single black pixel", "1 1\nB\n"), ("adversarial", "single yellow among greys", "2 2\nG G\nG Y\n"),
            ("maxSize", "100x100 grey", "100 100\n" + ("G " * 99 + "G\n") * 100)]
