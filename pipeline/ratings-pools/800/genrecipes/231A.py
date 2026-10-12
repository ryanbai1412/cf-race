from rlib import *

CONSTRAINTS = "n in 1..1000; n lines of three 0/1 integers."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count lines with at least two ones."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 1000)
    need(len(ls) == n + 1, "n lines")
    for l in ls[1:]:
        p = l.split(" ")
        need(len(p) == 3, "three values")
        nums(p, 0, 1)


def solve(inp):
    t = list(map(int, inp.split()))[1:]
    return str(sum(sum(t[i:i + 3]) >= 2 for i in range(0, len(t), 3)))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 1000), 1000])
    return f"{n}\n" + "\n".join(joined(rng.randint(0, 1) for _ in range(3)) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single all-zero line", "1\n0 0 0\n"), ("adversarial", "exactly one sure each", "3\n1 0 0\n0 1 0\n0 0 1\n"),
            ("maxSize", "n=1000 all sure", "1000\n" + "1 1 1\n" * 1000)]
