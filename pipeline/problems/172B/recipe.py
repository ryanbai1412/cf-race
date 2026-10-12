from genlib import *  # noqa: F401,F403

CHECKER = "Single integer period; unique, exact token comparison."
STATEMENT = "Legend defines the period, input (1<=m<=1e5, 0<=a,b<=1000, 0<=r0<m), output present."


def solve(s):
    a, b, m, r = ints(s)
    first = {}
    i = 0
    while r not in first:
        first[r] = i
        r = (a * r + b) % m
        i += 1
    return f"{i - first[r]}\n"


def rand(g, mhi):
    m = g.randint(1, mhi)
    return fmt([g.randint(0, 1000), g.randint(0, 1000), m, g.randint(0, m - 1)])


def cases(g):
    out = [("boundary", "m=1", fmt([0, 0, 1, 0])), ("boundary", "a=b=0 constant zero", fmt([0, 0, 7, 3])),
           ("boundary", "a=1 b=0 fixed point", fmt([1, 0, 100000, 99999])),
           ("adversarial", "full period a=1 b=1 m=1e5", fmt([1, 1, 100000, 0])),
           ("adversarial", "long pre-period (a=0)", fmt([0, 5, 100000, 99999])),
           ("adversarial", "a=1000 b=1000 m=99991 prime", fmt([1000, 1000, 99991, 1])),
           ("maxSize", "m=1e5 a=1 b=999 (gcd-limited cycle)", fmt([1, 999, 100000, 12345])),
           ("maxSize", "m=1e5 a=1 b=7", fmt([1, 7, 100000, 1]))]
    out += fill(g, lambda g: rand(g, 50), 60, reason="small m")
    out += fill(g, lambda g: rand(g, 100000), 40, reason="random m up to 1e5")
    out += fill(g, lambda g: fmt([1, g.randint(1, 1000), 100000, g.randint(0, 99999)]), 6, reason="a=1 long cycles")
    return out
