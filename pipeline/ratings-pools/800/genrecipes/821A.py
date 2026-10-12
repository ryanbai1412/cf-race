from rlib import *

CONSTRAINTS = "n in 1..50; n x n grid of integers in 1..10^5."
UNIQUENESS = "Decision problem; we emit 'Yes'/'No' (case-insensitive token per statement)."
STATEMENT = "Reviewed full statement: every non-1 cell equals a row element plus a column element."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 50)
    need(len(ls) == n + 1, "n rows")
    for l in ls[1:]:
        r = l.split(" ")
        need(len(r) == n, "n columns")
        nums(r, 1, 100000)


def solve(inp):
    t = list(map(int, inp.split()))
    n = t[0]; g = [t[1 + i * n:1 + (i + 1) * n] for i in range(n)]
    rows = [set(r) for r in g]
    for x in range(n):
        for y in range(n):
            v = g[x][y]
            if v != 1 and not any(v - g[k][y] in rows[x] for k in range(n)):
                return "No"
    return "Yes"


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 50), 50])
    hi = rng.choice([2, 3, 10, 100000])
    g = [[rng.randint(1, hi) for _ in range(n)] for _ in range(n)]
    if rng.random() < 0.5:
        g = [[1] * n for _ in range(n)]
        for _ in range(rng.randint(0, n * n)):
            x, y = rng.randrange(n), rng.randrange(n)
            s, k = rng.randrange(n), rng.randrange(n)
            if s != y and k != x and g[x][s] + g[k][y] <= 100000:
                g[x][y] = g[x][s] + g[k][y]
    return f"{n}\n" + "".join(joined(r) + "\n" for r in g)


def extra():
    return [("boundary", "single non-1 cell uses itself only", "1\n2\n"), ("adversarial", "needs same-cell row and column pairing", "2\n1 2\n1 1\n"),
            ("maxSize", "50x50 all ones", "50\n" + ("1 " * 49 + "1\n") * 50)]
