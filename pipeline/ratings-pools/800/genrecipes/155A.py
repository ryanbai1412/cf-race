from rlib import *

CONSTRAINTS = "n in 1..1000; n integers in 0..10000."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count strict new maxima or minima after the first contest."


def validate(inp):
    t = toks(inp)
    n = num(t[0], 1, 1000)
    need(len(t) == n + 1, "n points")
    nums(t[1:], 0, 10000)


def solve(inp):
    v = list(map(int, inp.split()[1:]))
    lo = hi = v[0]; c = 0
    for x in v[1:]:
        if x > hi or x < lo:
            c += 1
        lo, hi = min(lo, x), max(hi, x)
    return str(c)


def gen(rng):
    n = rng.choice([1, 2, rng.randint(1, 1000), 1000])
    hi = rng.choice([0, 1, 10, 10000])
    return f"{n}\n" + joined(rng.randint(0, hi) for _ in range(n)) + "\n"


def extra():
    return [("boundary", "n=1", "1\n10000\n"), ("adversarial", "equal values are not amazing", "4\n5 5 5 5\n"),
            ("maxSize", "n=1000 strictly increasing", "1000\n" + joined(range(0, 10000, 10)) + "\n")]
