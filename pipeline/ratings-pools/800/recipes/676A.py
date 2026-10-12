from rlib import *

CONSTRAINTS = "n in 2..100, then a permutation of 1..n."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: move 1 or n to an end with exactly one swap."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 2, 100)
    need(len(t) == n + 1 and sorted(nums(t[1:], 1, n)) == list(range(1, n + 1)), "permutation")


def solve(inp):
    t = list(map(int, inp.split()))
    n, a = t[0], t[1:]
    i, j = a.index(1), a.index(n)
    return str(max(i, j, n - 1 - i, n - 1 - j))


def extra():
    r = rng(676)
    p = list(range(1, 101)); r.shuffle(p)
    return [("boundary", "n=2", "2\n1 2\n"), ("boundary", "n=2 reversed", "2\n2 1\n"),
            ("adversarial", "both extremes in middle", "5\n2 1 5 3 4\n"),
            ("maxSize", "random n=100", "100\n" + joined(p) + "\n"), ("maxSize", "identity n=100", "100\n" + joined(range(1, 101)) + "\n")]
