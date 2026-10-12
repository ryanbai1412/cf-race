from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^6."
UNIQUENESS = "Closest divisor pair with a <= b is unique."
STATEMENT = "Reviewed full statement: largest divisor a <= sqrt(n), b = n/a."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 6)


def solve(inp):
    n = int(inp.split()[0])
    a = max(d for d in range(1, int(n ** 0.5) + 2) if n % d == 0 and d * d <= n)
    return joined([a, n // a])


def extra():
    return [("boundary", "n=1", "1\n"), ("adversarial", "large prime 999983", "999983\n"),
            ("maxSize", "n=10^6 square", "1000000\n"), ("adversarial", "n=999999", "999999\n")]
