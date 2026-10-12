from rlib import *

CONSTRAINTS = "a single integer n with 2 <= n <= 10^5."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count l in 1..n-1 with l | n."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 2, 10 ** 5)


def solve(inp):
    n = int(inp.split()[0])
    return str(sum(n % l == 0 for l in range(1, n)))


def extra():
    return [("boundary", "n=2", "2\n"), ("adversarial", "prime 99991", "99991\n"), ("maxSize", "n=10^5", "100000\n"), ("adversarial", "highly composite 83160", "83160\n")]
