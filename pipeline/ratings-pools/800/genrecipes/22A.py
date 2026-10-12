from rlib import *

CONSTRAINTS = "n in 1..100, n integers with |a_i| <= 100."
UNIQUENESS = "Second smallest distinct value or NO is unique."
STATEMENT = "Reviewed full statement: smallest element strictly greater than the minimum."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 100)
    need(len(t) == n + 1, "n values")
    nums(t[1:], -100, 100)


def solve(inp):
    v = sorted(set(map(int, inp.split()[1:])))
    return str(v[1]) if len(v) > 1 else "NO"


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 100), 100])
    span = rng.choice([0, 1, 3, 100])
    base = rng.randint(-100, 100 - span)
    return f"{n}\n" + joined(rng.randint(base, base + span) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1\n5\n"), ("boundary", "all equal", "3\n-100 -100 -100\n"),
            ("adversarial", "duplicated minimum", "4\n1 1 2 2\n"),
            ("maxSize", "n=100 full range", "100\n" + joined([-100 + 2 * i for i in range(100)]) + "\n")]
