from math import gcd
from rlib import *

CONSTRAINTS = "a single integer n with 3 <= n <= 1000."
UNIQUENESS = "Maximum proper irreducible fraction is unique."
STATEMENT = "Reviewed full statement: largest a < n-a with gcd(a, n-a) = 1."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 3, 1000)


def solve(inp):
    n = int(inp.split()[0])
    a = max(a for a in range(1, n) if a < n - a and gcd(a, n - a) == 1)
    return joined([a, n - a])


def extra():
    return [("boundary", "n=3", "3\n"), ("adversarial", "n=12 needs 5 7", "12\n"), ("maxSize", "n=1000", "1000\n"), ("maxSize", "n=999", "999\n")]
