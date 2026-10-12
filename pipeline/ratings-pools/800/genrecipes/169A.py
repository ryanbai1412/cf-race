from rlib import *

CONSTRAINTS = "n in 2..2000; a, b >= 1 with a + b = n; n values in 1..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: h_sorted[b] - h_sorted[b-1] (0-indexed)."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 2, 2000); a = num(t[1], 1, n); b = num(t[2], 1, n)
    need(a + b == n and len(t) == n + 3, "a+b=n, n values")
    nums(t[3:], 1, 10 ** 9)


def solve(inp):
    t = list(map(int, inp.split()))
    b = t[2]; h = sorted(t[3:])
    return str(h[b] - h[b - 1])


def gen(rng):
    n = rng.choice([2, rng.randint(2, 2000), 2000])
    a = rng.randint(1, n - 1)
    hi = rng.choice([1, 5, 10 ** 9])
    return f"{n} {a} {n - a}\n" + joined(rng.randint(1, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=2 equal", "2 1 1\n5 5\n"), ("boundary", "n=2 extremes", "2 1 1\n1 1000000000\n"),
            ("adversarial", "split inside duplicates", "4 2 2\n3 3 3 3\n"),
            ("maxSize", "n=2000 distinct", "2000 1000 1000\n" + joined(range(1, 2001)) + "\n")]
