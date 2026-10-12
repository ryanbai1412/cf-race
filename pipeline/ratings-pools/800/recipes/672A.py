from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 1000."
UNIQUENESS = "Unique digit."
STATEMENT = "Reviewed full statement: n-th digit of concatenation 123456789101112..."

DIGITS_STR = "".join(map(str, range(1, 1000)))


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 1000)


def solve(inp):
    return DIGITS_STR[int(inp.split()[0]) - 1]


def extra():
    return [("boundary", "n=1", "1\n"), ("boundary", "n=9 last single digit", "9\n"), ("adversarial", "n=10 first of '10'", "10\n"),
            ("adversarial", "n=190 first of '100'", "190\n"), ("maxSize", "n=1000", "1000\n")]
