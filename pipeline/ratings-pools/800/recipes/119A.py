from math import gcd
from rlib import *

CONSTRAINTS = "three integers a, b, n with 1 <= a, b, n <= 100."
UNIQUENESS = "Winner 0/1 is deterministic."
STATEMENT = "Reviewed full statement: alternate taking gcd(own number, pile); player unable to take loses; Simon (0) starts."


def validate(inp):
    nums(exact_tokens(inp, 3), 1, 100)


def solve(inp):
    a, b, n = map(int, inp.split())
    turn = 0
    while True:
        g = gcd((a, b)[turn], n)
        if g > n:
            return str(1 - turn)
        n -= g
        turn ^= 1
        if n == 0:
            return str(1 - turn)


def extra():
    return [("boundary", "all ones", "1 1 1\n"), ("boundary", "minimum pile, large numbers", "100 100 1\n"),
            ("adversarial", "Simon empties pile at once", "100 1 100\n"), ("maxSize", "all maximum", "100 100 100\n"),
            ("maxSize", "long game a=1 b=1 n=100", "1 1 100\n")]
