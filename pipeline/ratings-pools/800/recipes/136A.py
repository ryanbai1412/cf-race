from rlib import *

CONSTRAINTS = "n in 1..100, then a permutation p_1..p_n of 1..n."
UNIQUENESS = "Inverse permutation is unique."
STATEMENT = "Reviewed full statement: friend p_i gave to i; output for each i who gave to i (inverse permutation)."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100)
    need(len(t) == n + 1, "n values")
    need(sorted(nums(t[1:], 1, n)) == list(range(1, n + 1)), "permutation")


def solve(inp):
    t = list(map(int, inp.split()))
    n, p = t[0], t[1:]
    inv = [0] * n
    for i, v in enumerate(p, 1):
        inv[v - 1] = i
    return joined(inv)


def extra():
    r = rng(136)
    p = list(range(1, 101)); r.shuffle(p)
    return [("boundary", "n=1", "1\n1\n"), ("boundary", "n=2 swap", "2\n2 1\n"),
            ("adversarial", "3-cycle where inverse differs from p", "3\n2 3 1\n"),
            ("maxSize", "random permutation n=100", "100\n" + joined(p) + "\n"),
            ("maxSize", "reversed n=100", "100\n" + joined(range(100, 0, -1)) + "\n")]
