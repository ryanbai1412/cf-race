from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 1000."
UNIQUENESS = "Name is fully determined."
STATEMENT = "Reviewed full statement: 'O' at Fibonacci positions, 'o' elsewhere."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 1000)


def solve(inp):
    n = int(inp.split()[0])
    fib, a, b = set(), 1, 1
    while a <= n:
        fib.add(a); a, b = b, a + b
    return "".join("O" if i in fib else "o" for i in range(1, n + 1))


def extra():
    return [("boundary", "n=1", "1\n"), ("adversarial", "n=4 (4 not Fibonacci)", "4\n"), ("maxSize", "n=1000", "1000\n"), ("maxSize", "n=987 Fibonacci end", "987\n")]
