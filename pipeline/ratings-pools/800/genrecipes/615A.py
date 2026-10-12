from rlib import *

CONSTRAINTS = "n, m in 1..100; each button line: x in 0..m then x bulb numbers in 1..m."
UNIQUENESS = "Decision problem."
STATEMENT = "Reviewed full statement: union of button bulbs covers 1..m."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 100), num(p[1], 1, 100)
    need(len(ls) == n + 1, "n buttons")
    for l in ls[1:]:
        a = l.split(" ")
        x = num(a[0], 0, m)
        need(len(a) == x + 1, "x bulbs")
        nums(a[1:], 1, m)


def solve(inp):
    ls = lines(inp)
    m = int(ls[0].split()[1]); got = set()
    for l in ls[1:]:
        got.update(l.split()[1:])
    return yn(len(got) == m)


def gen(rng):
    n, m = rng.choice([1, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    rows = []
    for _ in range(n):
        b = [rng.randint(1, m) for _ in range(rng.randint(0, m))]
        rows.append(" ".join(map(str, [len(b)] + b)))
    return f"{n} {m}\n" + "\n".join(rows) + "\n"


def extra():
    return [("boundary", "empty button", "1 1\n0\n"), ("adversarial", "repeated bulb misses bulb m", "2 3\n3 1 1 2\n1 2\n"),
            ("maxSize", "100 buttons x 100 bulbs", "100 100\n" + "\n".join(["100 " + joined(range(1, 101))] * 100) + "\n")]
