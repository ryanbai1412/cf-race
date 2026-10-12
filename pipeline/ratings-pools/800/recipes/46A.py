from rlib import *

CONSTRAINTS = "a single integer n with 2 <= n <= 100."
UNIQUENESS = "The throw sequence is deterministic, so the n-1 numbers are unique."
STATEMENT = "Reviewed full statement: throw i moves ball i positions forward around circle of n kids starting at 1."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 2, 100)


def solve(inp):
    n = int(inp.split()[0])
    cur, out = 0, []
    for i in range(1, n):
        cur = (cur + i) % n
        out.append(cur + 1)
    return joined(out)


def extra():
    return [("boundary", "minimum n=2", "2\n"), ("boundary", "n=3", "3\n"),
            ("adversarial", "n=64 power of two, many wraps", "64\n"), ("maxSize", "maximum n=100", "100\n"),
            ("maxSize", "n=99", "99\n")]
