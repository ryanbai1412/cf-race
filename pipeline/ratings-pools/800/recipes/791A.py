from rlib import *

CONSTRAINTS = "1 <= a <= b <= 10."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: years until 3^y a > 2^y b."


def validate(inp):
    a, b = nums(exact_tokens(inp, 2), 1, 10)
    need(a <= b, "a <= b")


def solve(inp):
    a, b = map(int, inp.split())
    y = 0
    while a <= b:
        a, b, y = a * 3, b * 2, y + 1
    return str(y)


def extra():
    return [("boundary", "1 1", "1 1\n"), ("maxSize", "1 10 worst case", "1 10\n"), ("adversarial", "10 10", "10 10\n")]
