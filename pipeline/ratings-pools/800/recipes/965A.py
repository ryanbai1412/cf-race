from rlib import *

CONSTRAINTS = "four integers k, n, s, p in 1..10^4."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: ceil(k*ceil(n/s)/p)."


def validate(inp):
    nums(exact_tokens(inp, 4), 1, 10 ** 4)


def solve(inp):
    k, n, s, p = map(int, inp.split())
    return str(-(-k * -(-n // s) // p))


def extra():
    return [("boundary", "all ones", "1 1 1 1\n"), ("maxSize", "k=n=10^4 s=p=1 (1e8)", "10000 10000 1 1\n"),
            ("adversarial", "per-person rounding matters", "10000 1 10000 10000\n")]
