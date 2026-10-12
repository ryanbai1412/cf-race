from rlib import *

CONSTRAINTS = "n in 1..1000; a_i in 1..1000."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: interior elements strictly above or below both neighbours."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, 1, 1000)


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    return str(sum((a[i] - a[i - 1]) * (a[i] - a[i + 1]) > 0 for i in range(1, len(a) - 1)))


def gen(rng):
    n = rng.choice([1, 2, 3, rng.randint(1, 1000), 1000])
    return f"{n}\n" + joined(rng.randint(1, rng.choice([2, 3, 1000])) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1\n7\n"), ("adversarial", "plateaus are not extrema", "5\n1 2 2 1 1\n"),
            ("maxSize", "n=1000 zigzag", "1000\n" + joined([1, 1000] * 500) + "\n")]
