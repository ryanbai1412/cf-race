from rlib import *

CONSTRAINTS = "n in 1..1000; a_i in 1..10^6."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: optimal play leaves the lower median, sorted[(n-1)//2]."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, 1, 10 ** 6)


def solve(inp):
    a = sorted(map(int, inp.split()[1:]))
    return str(a[(len(a) - 1) // 2])


def gen(rng):
    n = rng.choice([1, 2, 3, rng.randint(1, 1000), 1000])
    return f"{n}\n" + joined(rng.randint(1, rng.choice([3, 10 ** 6])) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "single number", "1\n1000000\n"), ("adversarial", "even n lower median", "4\n4 1 3 2\n"),
            ("maxSize", "n=1000", "1000\n" + joined(10 ** 6 - i * 997 for i in range(1000)) + "\n")]
