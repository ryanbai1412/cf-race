from rlib import *

CONSTRAINTS = "two integers n, k in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: (n//k + 1) * k."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 10 ** 9)


def solve(inp):
    n, k = map(int, inp.split())
    return str((n // k + 1) * k)


def extra():
    return [("boundary", "1 1", "1 1\n"), ("adversarial", "n divisible by k", "10 5\n"),
            ("maxSize", "n=10^9 k=10^9 -> 2e9 (32-bit overflow)", "1000000000 1000000000\n"),
            ("maxSize", "n=10^9 k=1", "1000000000 1\n"), ("adversarial", "k > n", "5 1000000000\n")]
