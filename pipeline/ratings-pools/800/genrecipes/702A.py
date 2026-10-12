from rlib import *

CONSTRAINTS = "n in 1..10^5; a_i in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: longest strictly increasing contiguous subarray."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 100000)
    a = ls[1].split(" ")
    need(len(a) == n, "n values")
    nums(a, 1, 10 ** 9)


def solve(inp):
    a = list(map(int, inp.split()))[1:]
    best = cur = 1
    for i in range(1, len(a)):
        cur = cur + 1 if a[i] > a[i - 1] else 1
        best = max(best, cur)
    return str(best)


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), rng.randint(1, 3000)])
    hi = rng.choice([1, 3, 10 ** 9])
    return f"{n}\n" + joined(rng.randint(1, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1\n5\n"), ("adversarial", "equal neighbours break runs", "5\n1 2 2 3 4\n"),
            ("maxSize", "n=10^5 strictly increasing", "100000\n" + joined(range(1, 100001)) + "\n")]
