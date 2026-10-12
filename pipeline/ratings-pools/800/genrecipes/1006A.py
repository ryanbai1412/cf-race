from rlib import *

CONSTRAINTS = "n in 1..1000; a_i in 1..10^9."
UNIQUENESS = "Unique array."
STATEMENT = "Reviewed full statement: even values become value-1, odd unchanged."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 1000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, 1, 10 ** 9)


def solve(inp):
    return " ".join(str(x - (x % 2 == 0)) for x in map(int, inp.split()[1:]))


def gen(rng):
    n = rng.choice([1, rng.randint(1, 1000), 1000])
    return f"{n}\n" + joined(rng.choice([1, 2, 10 ** 9, 10 ** 9 - 1, rng.randint(1, 10 ** 9)]) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "smallest values", "2\n1 2\n"), ("adversarial", "max even/odd", "2\n1000000000 999999999\n"),
            ("maxSize", "n=1000", "1000\n" + joined(10 ** 9 - i for i in range(1000)) + "\n")]
