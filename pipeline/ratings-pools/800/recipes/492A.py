from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^4."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: maximal h with sum of first h triangular numbers <= n."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 4)


def solve(inp):
    n = int(inp.split()[0])
    h = used = 0
    while used + (h + 1) * (h + 2) // 2 <= n:
        h += 1
        used += h * (h + 1) // 2
    return str(h)


def extra():
    return [("boundary", "n=1", "1\n"), ("boundary", "n=3 one below level two (needs 4)", "3\n"),
            ("adversarial", "exact tetrahedral 220 -> 10", "220\n"), ("adversarial", "219 -> 9", "219\n"),
            ("maxSize", "maximum n=10000", "10000\n")]
