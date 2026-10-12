from math import factorial
from rlib import *

CONSTRAINTS = "A, B in 1..10^9 with min(A, B) <= 12."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: min(A,B)!."


def validate(inp):
    a, b = nums(exact_tokens(inp, 2), 1, 10 ** 9)
    need(min(a, b) <= 12, "min <= 12")


def solve(inp):
    return str(factorial(min(map(int, inp.split()))))


def extra():
    return [("boundary", "1 1", "1 1\n"), ("maxSize", "12 and 10^9", "1000000000 12\n"), ("adversarial", "13 12 (13! overflows int)", "13 12\n")]
