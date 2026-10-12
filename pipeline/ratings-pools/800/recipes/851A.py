from rlib import *

CONSTRAINTS = "n in 1..10^9, k in 1..n, t in 1..n+k-1."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: t if t<=k, k if t<=n, else n+k-t."


def validate(inp):
    n, k, t = exact_tokens(inp, 3)
    n = num(n, 1, 10 ** 9); k = num(k, 1, n); num(t, 1, n + k - 1)


def solve(inp):
    n, k, t = map(int, inp.split())
    return str(t if t <= k else k if t <= n else n + k - t)


def extra():
    return [("boundary", "n=k=t=1", "1 1 1\n"), ("adversarial", "t = n exactly", "10 5 10\n"), ("adversarial", "t = n+1", "10 5 11\n"),
            ("maxSize", "max values, last moment", "1000000000 1000000000 1999999999\n"), ("maxSize", "max n, k=1", "1000000000 1 500000000\n")]
