from rlib import *

CONSTRAINTS = "n in 1..10, k in 1..240."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max i <= n with 5*i(i+1)/2 + k <= 240."


def validate(inp):
    n, k = exact_tokens(inp, 2)
    num(n, 1, 10); num(k, 1, 240)


def solve(inp):
    n, k = map(int, inp.split())
    return str(max(i for i in range(n + 1) if 5 * i * (i + 1) // 2 + k <= 240))


def extra():
    return [("boundary", "k=240 none", "10 240\n"), ("boundary", "n=1 k=1", "1 1\n"), ("adversarial", "exact fit 225+15", "9 15\n"),
            ("maxSize", "n=10 k=1 (needs 275 > 239)", "10 1\n")]
