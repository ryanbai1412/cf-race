from rlib import *

CONSTRAINTS = "a single integer n with 2 <= n <= 2*10^18."
UNIQUENESS = "Always 25."
STATEMENT = "Reviewed full statement: last two digits of 5^n for n >= 2 are 25."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 2, 2 * 10 ** 18)


def solve(inp):
    return str(pow(5, int(inp.split()[0]), 100)).zfill(2)


def extra():
    return [("boundary", "n=2", "2\n"), ("maxSize", "n=2*10^18", "2000000000000000000\n"), ("adversarial", "n=3", "3\n")]
