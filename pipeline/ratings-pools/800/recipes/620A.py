from rlib import *

CONSTRAINTS = "two lines each with two integers in [-10^9, 10^9]."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: Chebyshev distance."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    for l in ls:
        p = l.split(" ")
        need(len(p) == 2, "pair")
        nums(p, -10 ** 9, 10 ** 9)


def solve(inp):
    a, b, c, d = map(int, inp.split())
    return str(max(abs(a - c), abs(b - d)))


def extra():
    return [("boundary", "same point", "0 0\n0 0\n"), ("adversarial", "x dominates", "0 0\n5 -3\n"),
            ("maxSize", "opposite corners distance 2e9 (overflow 32-bit)", "-1000000000 -1000000000\n1000000000 1000000000\n"),
            ("maxSize", "y dominates large", "1000000000 -1000000000\n999999999 1000000000\n")]
