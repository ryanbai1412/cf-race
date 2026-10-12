from rlib import *

CONSTRAINTS = "n in 1..2000; a_i in 1..2000."
UNIQUENESS = "Unique positions."
STATEMENT = "Reviewed full statement: position = 1 + number of strictly higher ratings."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 2000)
    a = ls[1].split(" ")
    need(len(a) == n, "n ratings")
    nums(a, 1, 2000)


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    return " ".join(str(1 + sum(b > x for b in a)) for x in a)


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), rng.randint(1, 2000), 2000])
    hi = rng.choice([1, 3, 2000])
    return f"{n}\n" + joined(rng.randint(1, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single student", "1\n2000\n"), ("adversarial", "ties share positions", "4\n2 2 1 3\n"),
            ("maxSize", "n=2000 distinct", "2000\n" + joined(range(1, 2001)) + "\n")]
