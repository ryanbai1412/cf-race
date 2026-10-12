from rlib import *

CONSTRAINTS = "n in 2..100, then n heights in 1..100."
UNIQUENESS = "Minimum swap count is a unique integer."
STATEMENT = "Reviewed full statement: move first maximum to front and last minimum to back with adjacent swaps."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 2, 100)
    need(len(t) == n + 1, "n heights")
    nums(t[1:], 1, 100)


def solve(inp):
    t = list(map(int, inp.split()))
    n, a = t[0], t[1:]
    i = a.index(max(a))
    j = n - 1 - a[::-1].index(min(a))
    return str(i + (n - 1 - j) - (1 if i > j else 0))


def extra():
    r = rng(144)
    return [("boundary", "n=2 already correct", "2\n2 1\n"), ("boundary", "n=2 reversed", "2\n1 2\n"),
            ("boundary", "all equal heights", "5\n7 7 7 7 7\n"),
            ("adversarial", "max after min: crossing saves a swap", "4\n3 1 4 2\n"),
            ("adversarial", "duplicate maxima and minima pick nearest", "6\n1 5 1 5 1 5\n"),
            ("maxSize", "n=100 sorted increasing (worst case)", "100\n" + joined(range(1, 101)) + "\n"),
            ("maxSize", "n=100 random", "100\n" + joined(r.randint(1, 100) for _ in range(100)) + "\n")]
