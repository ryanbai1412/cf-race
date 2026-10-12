from rlib import *

CONSTRAINTS = "one line of eight integers n, k, l, c, d, p, nl, np each in 1..1000."
UNIQUENESS = "Toast count is a unique integer."
STATEMENT = "Reviewed full statement: min(k*l//nl, c*d, p//np) // n."


def validate(inp):
    nums(exact_tokens(inp, 8), 1, 1000)


def solve(inp):
    n, k, l, c, d, p, nl, np = map(int, inp.split())
    return str(min(k * l // nl, c * d, p // np) // n)


def extra():
    return [("boundary", "all ones", "1 1 1 1 1 1 1 1\n"), ("boundary", "all maximum", "1000 1000 1000 1000 1000 1000 1000 1000\n"),
            ("adversarial", "drink limiting, zero toasts", "1000 1 1 1000 1000 1000 1000 1\n"),
            ("adversarial", "lime limiting", "2 1000 1000 1 3 1000 1 1\n"),
            ("maxSize", "large products, salt limiting", "3 1000 1000 1000 1000 999 1 2\n")]
