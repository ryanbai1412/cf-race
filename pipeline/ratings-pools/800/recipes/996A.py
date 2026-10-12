from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: greedy over 100,20,10,5,1 (canonical system)."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 9)


def solve(inp):
    n = int(inp.split()[0]); c = 0
    for d in (100, 20, 10, 5, 1):
        c += n // d; n %= d
    return str(c)


def extra():
    return [("boundary", "n=1", "1\n"), ("adversarial", "n=39", "39\n"), ("maxSize", "n=10^9", "1000000000\n"), ("maxSize", "n=999999999", "999999999\n")]
