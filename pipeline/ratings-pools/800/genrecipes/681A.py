from rlib import *

CONSTRAINTS = "n in 1..100; distinct handles of 1..10 chars from letters, digits, '_' and '-'; before/after in -4000..4000."
UNIQUENESS = "Decision problem."
STATEMENT = "Reviewed full statement: YES iff some outscored participant had before >= 2400 and after > before."

HANDLE = LETTERS + DIGITS + "_-"


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n participants")
    names = set()
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 3, "name before after")
        word(p[0], HANDLE, 1, 10)
        num(p[1], -4000, 4000); num(p[2], -4000, 4000)
        names.add(p[0])
    need(len(names) == n, "distinct handles")


def solve(inp):
    for l in lines(inp)[1:]:
        _, b, a = l.split()
        if int(b) >= 2400 and int(a) > int(b):
            return "YES"
    return "NO"


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    names = set()
    while len(names) < n:
        names.add("".join(rng.choice(HANDLE) for _ in range(rng.randint(1, 10))))
    rows = []
    for s in sorted(names):
        b = rng.choice([2399, 2400, rng.randint(-4000, 4000)])
        rows.append(f"{s} {b} {rng.choice([b, b + 1, b - 1, rng.randint(-4000, 4000)]) if -4000 < b < 4000 else b}")
    return f"{n}\n" + "\n".join(rows) + "\n"


def extra():
    return [("boundary", "exactly 2400 rising", "1\n_ 2400 2401\n"), ("adversarial", "2399 rising and 2400 unchanged", "2\na-1 2399 2500\nB_2 2400 2400\n"),
            ("maxSize", "100 participants, red but falling", "100\n" + "\n".join(f"h{i:03d}-x_ 4000 3999" for i in range(100)) + "\n")]
