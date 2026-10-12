from rlib import *

CONSTRAINTS = "two integers n, k in 1..10^12."
UNIQUENESS = "Maximizing winners fixes d = (n//2)//(k+1) uniquely."
STATEMENT = "Reviewed full statement: d, k*d, n - (k+1)*d."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 10 ** 12)


def solve(inp):
    n, k = map(int, inp.split())
    d = n // 2 // (k + 1)
    return joined([d, k * d, n - (k + 1) * d])


def extra():
    return [("boundary", "n=1 -> no winners", "1 1\n"), ("adversarial", "k huge -> 0 winners", "1000000000000 1000000000000\n"),
            ("maxSize", "n=10^12 k=1", "1000000000000 1\n"), ("maxSize", "n=10^12 k=499999999999", "1000000000000 499999999999\n")]
