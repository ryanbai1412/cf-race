from rlib import *

CONSTRAINTS = "two integers n, m with 2 <= n < m <= 50, n prime."
UNIQUENESS = "Decision problem: YES/NO."
STATEMENT = "Reviewed full statement: YES iff m is the next prime after n."


def prime(x):
    return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))


def validate(inp):
    n, m = nums(exact_tokens(inp, 2), 2, 50)
    need(n < m and prime(n), "n prime and n < m")


def solve(inp):
    n, m = map(int, inp.split())
    nxt = n + 1
    while not prime(nxt):
        nxt += 1
    return yn(nxt == m)


def extra():
    return [("boundary", "smallest pair 2 3", "2 3\n"), ("boundary", "2 4", "2 4\n"),
            ("adversarial", "m prime but skips 43: 41 47", "41 47\n"), ("adversarial", "47 49 composite", "47 49\n"),
            ("maxSize", "47 50 maximum m", "47 50\n")]
