from rlib import *

CONSTRAINTS = "n in 1..10^5; each line is 01 or 10."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count groups = 1 + number of orientation changes."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100000)
    need(len(ls) == n + 1, "n magnets")
    need(all(s in ("01", "10") for s in ls[1:]), "01 or 10")


def solve(inp):
    m = lines(inp)[1:]
    return str(1 + sum(a != b for a, b in zip(m, m[1:])))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 3000)] * 6 + [100000])
    flip = rng.random()
    cur, out = rng.choice(("01", "10")), []
    for _ in range(n):
        out.append(cur)
        if rng.random() < flip:
            cur = "10" if cur == "01" else "01"
    return f"{n}\n" + "\n".join(out) + "\n"


def extra():
    return [("boundary", "single magnet", "1\n10\n"), ("adversarial", "alternating every magnet", "4\n01\n10\n01\n10\n"),
            ("maxSize", "n=10^5 alternating", "100000\n" + "\n".join("01" if i % 2 else "10" for i in range(100000)) + "\n")]
