from rlib import *

CONSTRAINTS = "two integers 1 <= a <= b <= 10^100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: a if a == b else 1."


def validate(inp):
    a, b = exact_tokens(inp, 2)
    x = num(a, 1, 10 ** 100); y = num(b, 1, 10 ** 100)
    need(x <= y, "a <= b")


def solve(inp):
    a, b = inp.split()
    return a if int(a) == int(b) else "1"


def extra():
    g = "1" + "0" * 100
    return [("boundary", "1 1", "1 1\n"), ("boundary", "googol googol", f"{g} {g}\n"),
            ("adversarial", "consecutive huge numbers", f"{'9' * 100} {g}\n"), ("maxSize", "1 to googol", f"1 {g}\n")]
