from rlib import *

CONSTRAINTS = "n, k with 1 <= k <= n <= 50; then n non-increasing scores in 0..100."
UNIQUENESS = "Advancer count is a unique integer."
STATEMENT = "Reviewed full statement: count scores >= a_k and > 0."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 50); k = num(t[1], 1, n)
    need(len(t) == n + 2, "n scores")
    a = nums(t[2:], 0, 100)
    need(all(a[i] >= a[i + 1] for i in range(n - 1)), "non-increasing")


def solve(inp):
    t = list(map(int, inp.split()))
    k, a = t[1], t[2:]
    return str(sum(1 for x in a if x >= a[k - 1] and x > 0))


def extra():
    return [("boundary", "n=k=1 zero score", "1 1\n0\n"), ("boundary", "n=k=1 positive", "1 1\n5\n"),
            ("adversarial", "ties extend past k", "5 2\n9 7 7 7 1\n"), ("adversarial", "k-th score zero, positives only", "5 4\n3 2 0 0 0\n"),
            ("maxSize", "n=50 k=50 all 100", "50 50\n" + joined([100] * 50) + "\n"),
            ("maxSize", "n=50 k=25 decreasing", "50 25\n" + joined(range(100, 50, -1)) + "\n")]
