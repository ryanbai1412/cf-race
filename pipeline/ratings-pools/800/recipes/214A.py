from rlib import *

CONSTRAINTS = "two integers n, m in 1..1000."
UNIQUENESS = "Count of pairs is a unique integer."
STATEMENT = "Reviewed full statement (system image: a^2 + b = n, a + b^2 = m, a, b >= 0, confirmed by samples)."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 1000)


def solve(inp):
    n, m = map(int, inp.split())
    return str(sum(1 for a in range(0, 1001) for b in range(0, 1001) if a * a + b == n and a + b * b == m))


def extra():
    return [("boundary", "n=m=1 two solutions (0,1),(1,0)", "1 1\n"), ("boundary", "maximum n=m=1000", "1000 1000\n"),
            ("adversarial", "no solution", "2 2\n"), ("adversarial", "single solution a=3, b=0", "9 3\n"),
            ("maxSize", "n=1000 m=1 (a large, b small)", "1000 1\n")]
