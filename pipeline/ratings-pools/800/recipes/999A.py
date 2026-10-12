from rlib import *

CONSTRAINTS = "n, k in 1..100, then n difficulties in 1..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: solvable prefix plus suffix, capped at n."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100); num(t[1], 1, 100)
    need(len(t) == n + 2, "n values")
    nums(t[2:], 1, 100)


def solve(inp):
    t = list(map(int, inp.split()))
    n, k, a = t[0], t[1], t[2:]
    i = 0
    while i < n and a[i] <= k:
        i += 1
    if i == n:
        return str(n)
    j = n - 1
    while a[j] <= k:
        j -= 1
    return str(i + n - 1 - j)


def extra():
    return [("boundary", "n=1 solvable", "1 1\n1\n"), ("boundary", "n=1 unsolvable", "1 1\n2\n"),
            ("adversarial", "both ends", "5 3\n1 4 4 4 2\n"), ("maxSize", "n=100 all solvable", "100 100\n" + joined([100] * 100) + "\n")]
