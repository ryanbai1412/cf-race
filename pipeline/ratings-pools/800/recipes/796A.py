from rlib import *

CONSTRAINTS = "n in 2..100, m in 1..n, k in 1..100; n prices in 0..100 with a_m = 0 and some 0 < a_i <= k."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: min 10*|i-m| over buyable affordable houses."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 2, 100); m = num(t[1], 1, n); k = num(t[2], 1, 100)
    need(len(t) == n + 3, "n prices")
    a = nums(t[3:], 0, 100)
    need(a[m - 1] == 0 and any(0 < x <= k for x in a), "guarantees")


def solve(inp):
    t = list(map(int, inp.split()))
    n, m, k, a = t[0], t[1], t[2], t[3:]
    return str(min(10 * abs(i + 1 - m) for i in range(n) if 0 < a[i] <= k))


def extra():
    return [("boundary", "n=2 adjacent", "2 1 1\n0 1\n"), ("boundary", "n=2 girl at right", "2 2 100\n100 0\n"),
            ("adversarial", "cheap far house, expensive near", "5 3 10\n5 50 0 50 1\n"),
            ("maxSize", "n=100 only house 100 affordable from 1", "100 1 1\n0" + " 0" * 98 + " 1\n"),
            ("maxSize", "n=100 all price 100 with k=100", "100 50 100\n" + joined([100] * 49 + [0] + [100] * 50) + "\n")]
