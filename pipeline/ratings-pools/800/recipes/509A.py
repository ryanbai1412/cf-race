from math import comb
from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max is a[n][n] = C(2n-2, n-1)."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10)


def solve(inp):
    n = int(inp.split()[0])
    return str(comb(2 * n - 2, n - 1))


def extra():
    return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("maxSize", "n=10", "10\n"), ("adversarial", "n=7", "7\n")]
