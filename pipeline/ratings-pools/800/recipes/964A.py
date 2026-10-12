from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: number of distinct weights is n//2 + 1."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 9)


def solve(inp):
    return str(int(inp.split()[0]) // 2 + 1)


def extra():
    return [("boundary", "n=1", "1\n"), ("maxSize", "n=10^9", "1000000000\n"), ("adversarial", "n=3", "3\n")]
