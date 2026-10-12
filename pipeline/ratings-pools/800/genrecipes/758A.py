from rlib import *

CONSTRAINTS = "n in 1..100; a_i in 0..10^6."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: sum of (max - a_i)."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, 0, 10 ** 6)


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    return str(max(a) * len(a) - sum(a))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 100), 100])
    return f"{n}\n" + joined(rng.randint(0, rng.choice([0, 5, 10 ** 6])) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single citizen", "1\n0\n"), ("adversarial", "one rich citizen", "4\n0 0 0 1000000\n"),
            ("maxSize", "n=100 widest gap", "100\n" + joined([10 ** 6] + [0] * 99) + "\n")]
