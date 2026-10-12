from rlib import *

CONSTRAINTS = "n, m in 1..100; n rows of exactly m digits."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: each row single colour, adjacent rows differ."


def validate(inp):
    ls = lines(inp)
    n, m = ls[0].split(" ")
    n, m = num(n, 1, 100), num(m, 1, 100)
    need(len(ls) == n + 1, "n rows")
    for r in ls[1:]:
        word(r, DIGITS, m, m)


def solve(inp):
    rows = lines(inp)[1:]
    return yn(all(len(set(r)) == 1 for r in rows) and all(a[0] != b[0] for a, b in zip(rows, rows[1:])))


def gen(rng):
    n, m = rng.choice([1, 2, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    rows, prev = [], None
    for _ in range(n):
        c = rng.choice([d for d in DIGITS if d != prev])
        rows.append(c * m)
        prev = c
    kind = rng.randint(0, 2)
    if kind == 1 and n > 1:
        i = rng.randint(1, n - 1)
        rows[i] = rows[i - 1]
    elif kind == 2:
        i = rng.randrange(n); j = rng.randrange(m)
        rows[i] = rows[i][:j] + rng.choice([d for d in DIGITS if d != rows[i][j]]) + rows[i][j + 1:]
    return f"{n} {m}\n" + "\n".join(rows) + "\n"


def extra():
    return [("boundary", "1x1", "1 1\n0\n"), ("boundary", "two equal rows", "2 1\n5\n5\n"),
            ("adversarial", "one bad cell at the last column", "3 4\n1111\n2222\n1112\n"),
            ("maxSize", "100x100 alternating 0/1 rows", "100 100\n" + "\n".join(("0" if i % 2 else "1") * 100 for i in range(100)) + "\n")]
