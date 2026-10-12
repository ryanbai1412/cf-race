from rlib import *

CONSTRAINTS = "n, m in 1..100; n lines of 2m window states 0/1 separated by single spaces."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: flats (window pairs 2j-1, 2j) with at least one light."


def validate(inp):
    ls = lines(inp)
    p = ls[0].split(" ")
    need(len(p) == 2, "n m")
    n, m = num(p[0], 1, 100), num(p[1], 1, 100)
    need(len(ls) == n + 1, "n floors")
    for l in ls[1:]:
        w = l.split(" ")
        need(len(w) == 2 * m, "2m windows")
        nums(w, 0, 1)


def solve(inp):
    total = 0
    for l in lines(inp)[1:]:
        w = l.split()
        total += sum(w[i] == "1" or w[i + 1] == "1" for i in range(0, len(w), 2))
    return str(total)


def gen(rng):
    n, m = rng.choice([1, rng.randint(1, 100), 100]), rng.choice([1, rng.randint(1, 100), 100])
    p = rng.random()
    return f"{n} {m}\n" + "\n".join(joined(int(rng.random() < p) for _ in range(2 * m)) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "1x1 dark", "1 1\n0 0\n"), ("adversarial", "only second window of each flat lit", "1 3\n0 1 0 1 0 1\n"),
            ("maxSize", "100x100 all lit", "100 100\n" + "\n".join([joined([1] * 200)] * 100) + "\n")]
