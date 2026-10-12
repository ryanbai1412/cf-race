from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^9."
UNIQUENESS = "Winner is unique."
STATEMENT = "Reviewed full statement: Mahmoud wins iff n even."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 9)


def solve(inp):
    return "Mahmoud" if int(inp.split()[0]) % 2 == 0 else "Ehab"


def extra():
    return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("maxSize", "n=10^9", "1000000000\n"), ("maxSize", "n=999999999", "999999999\n"), ("adversarial", "n=3 odd small", "3\n")]
