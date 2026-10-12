from rlib import *

CONSTRAINTS = "two integers n, m with 1 <= n <= 50, 1 <= m <= 10^4."
UNIQUENESS = "Simulation result is a unique integer."
STATEMENT = "Reviewed full statement: walrus i gets i chips cyclically 1..n until fewer chips than needed; print leftover."


def validate(inp):
    n, m = exact_tokens(inp, 2)
    num(n, 1, 50); num(m, 1, 10 ** 4)


def solve(inp):
    n, m = map(int, inp.split())
    i = 1
    while m >= i:
        m -= i
        i = i % n + 1
    return str(m)


def extra():
    return [("boundary", "n=1 m=1 -> 0", "1 1\n"), ("boundary", "n=50 m=1", "50 1\n"),
            ("adversarial", "exact full cycle sum 1..4 = 10", "4 10\n"), ("maxSize", "n=50 m=10000", "50 10000\n"),
            ("maxSize", "n=1 m=10000 -> 0", "1 10000\n")]
