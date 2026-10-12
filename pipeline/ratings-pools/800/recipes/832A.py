from rlib import *

CONSTRAINTS = "1 <= k <= n <= 10^18."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: YES iff (n//k) is odd."


def validate(inp):
    n, k = nums(exact_tokens(inp, 2), 1, 10 ** 18)
    need(k <= n, "k <= n")


def solve(inp):
    n, k = map(int, inp.split())
    return yn(n // k % 2 == 1)


def extra():
    return [("boundary", "1 1", "1 1\n"), ("boundary", "2 1", "2 1\n"), ("maxSize", "10^18 1 even", "1000000000000000000 1\n"),
            ("maxSize", "10^18 3", "1000000000000000000 3\n"), ("adversarial", "k = n", "999999999999999999 999999999999999999\n")]
