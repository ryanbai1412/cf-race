from rlib import *

CONSTRAINTS = "a single integer x with 1 <= x <= 10^6."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: ceil(x/5)."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 6)


def solve(inp):
    return str(-(-int(inp.split()[0]) // 5))


def extra():
    return [("boundary", "x=1", "1\n"), ("boundary", "x=5", "5\n"), ("adversarial", "x=6", "6\n"),
            ("maxSize", "x=10^6", "1000000\n"), ("maxSize", "x=999999", "999999\n")]
