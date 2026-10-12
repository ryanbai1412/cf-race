from rlib import *

CONSTRAINTS = "n in 1..100; n rows of n characters from '.C'."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: pairs of chocolates sharing a row or a column."


def validate(inp):
    ls = lines(inp)
    n = num(ls[0], 1, 100)
    need(len(ls) == n + 1, "n rows")
    for r in ls[1:]:
        word(r, ".C", n, n)


def solve(inp):
    g = lines(inp)[1:]
    c = lambda k: k * (k - 1) // 2
    return str(sum(c(r.count("C")) for r in g) + sum(c(col.count("C")) for col in zip(*g)))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100]); p = rng.random()
    return f"{n}\n" + "\n".join("".join("C" if rng.random() < p else "." for _ in range(n)) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "1x1 chocolate", "1\nC\n"), ("adversarial", "diagonal shares nothing", "3\nC..\n.C.\n..C\n"),
            ("maxSize", "100x100 full", "100\n" + "\n".join(["C" * 100] * 100) + "\n")]
