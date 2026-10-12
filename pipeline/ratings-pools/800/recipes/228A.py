from rlib import *

CONSTRAINTS = "four integers s1..s4 in 1..10^9."
UNIQUENESS = "Minimum purchase is a unique integer."
STATEMENT = "Reviewed full statement: 4 minus number of distinct colors."


def validate(inp):
    nums(exact_tokens(inp, 4), 1, 10 ** 9)


def solve(inp):
    return str(4 - len(set(inp.split())))


def extra():
    return [("boundary", "all equal minimum", "1 1 1 1\n"), ("boundary", "all distinct", "1 2 3 4\n"),
            ("adversarial", "two pairs", "1000000000 7 7 1000000000\n"),
            ("maxSize", "all maximum", "1000000000 1000000000 1000000000 1000000000\n")]
