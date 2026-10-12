from math import gcd
from rlib import *

CONSTRAINTS = "three integers n, m, z in 1..10^4."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count multiples of lcm(n, m) up to z."


def validate(inp):
    nums(exact_tokens(inp, 3), 1, 10 ** 4)


def solve(inp):
    n, m, z = map(int, inp.split())
    return str(z // (n * m // gcd(n, m)))


def extra():
    return [("boundary", "all ones", "1 1 1\n"), ("adversarial", "lcm exceeds z", "9999 10000 10000\n"),
            ("maxSize", "n=m=1 z=10^4", "1 1 10000\n"), ("adversarial", "non-coprime 4 6 z=10000", "4 6 10000\n")]
