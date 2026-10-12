from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 500."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: is n = k(k+1)/2 for some k >= 1."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 500)


def solve(inp):
    n = int(inp.split()[0])
    return yn(any(k * (k + 1) // 2 == n for k in range(1, 40)))


def extra():
    return [("boundary", "minimum n=1 (triangular)", "1\n"), ("boundary", "n=2 not triangular", "2\n"),
            ("adversarial", "largest triangular <=500 is 496", "496\n"), ("adversarial", "495 just below triangular", "495\n"),
            ("maxSize", "maximum n=500", "500\n")]
