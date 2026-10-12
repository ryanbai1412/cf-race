from rlib import *

CONSTRAINTS = "a1..a4 in 0..10^4; s of length 1..10^5 over digits 1-4."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: sum of a_c over characters of s."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    a = ls[0].split(" ")
    need(len(a) == 4, "four costs")
    nums(a, 0, 10000)
    word(ls[1], "1234", 1, 100000)


def solve(inp):
    ls = lines(inp)
    a = list(map(int, ls[0].split()))
    return str(sum(a[int(c) - 1] for c in ls[1]))


def gen(rng):
    a = [rng.choice([0, rng.randint(0, 10000), 10000]) for _ in range(4)]
    L = rng.choice([1, rng.randint(1, 100), rng.randint(1, 5000)] * 8 + [100000])
    return joined(a) + "\n" + "".join(rng.choice("1234") for _ in range(L)) + "\n"


def extra():
    return [("boundary", "zero costs", "0 0 0 0\n1234\n"), ("adversarial", "only strip 4", "1 2 3 4\n4444\n"),
            ("maxSize", "10^5 squares at max cost", "10000 10000 10000 10000\n" + "1234" * 25000 + "\n")]
