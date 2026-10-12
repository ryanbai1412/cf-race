from rlib import *

CONSTRAINTS = "n in 1..10^5; a_i in -10^5..10^5."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: number of distinct nonzero values."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, -100000, 100000)


def solve(inp):
    return str(len(set(int(x) for x in inp.split()[1:]) - {0}))


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 3000)])
    hi = rng.choice([0, 1, 5, 100000])
    return f"{n}\n" + joined(rng.randint(-hi, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "already zero", "1\n0\n"), ("adversarial", "negatives distinct from positives", "4\n1 -1 0 1\n"),
            ("maxSize", "n=10^5 all distinct", "100000\n" + joined(list(range(-50000, 0)) + list(range(1, 50001))) + "\n")]
