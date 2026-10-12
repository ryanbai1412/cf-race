from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^15."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: f(n) = n/2 if even else -(n+1)/2."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 15)


def solve(inp):
    n = int(inp.split()[0])
    return str(n // 2 if n % 2 == 0 else -(n + 1) // 2)


def extra():
    return [("boundary", "n=1 -> -1", "1\n"), ("boundary", "n=2 -> 1", "2\n"),
            ("adversarial", "odd near 2^31 (overflow in 32-bit)", "2147483649\n"),
            ("maxSize", "maximum n=10^15", "1000000000000000\n"), ("maxSize", "odd maximum 10^15-1", "999999999999999\n")]
