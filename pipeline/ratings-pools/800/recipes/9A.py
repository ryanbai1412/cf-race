from math import gcd
from rlib import *

CONSTRAINTS = "two die results Y and W, each an integer in 1..6."
UNIQUENESS = "Irreducible fraction A/B (with 1/1 for certainty) is a unique string."
STATEMENT = "Reviewed full statement: Dot wins ties, probability Dot rolls >= max(Y, W) as reduced fraction."


def validate(inp):
    nums(exact_tokens(inp, 2), 1, 6)


def solve(inp):
    y, w = map(int, inp.split())
    a, b = 7 - max(y, w), 6
    g = gcd(a, b)
    return f"{a // g}/{b // g}"


def extra():
    return [("boundary", "both minimum: answer 1/1", "1 1\n"), ("boundary", "both maximum: answer 1/6", "6 6\n"),
            ("adversarial", "reduction to 1/2 (max=4)", "4 2\n"), ("adversarial", "reduction to 2/3 (max=3)", "1 3\n"),
            ("maxSize", "one die at maximum 6", "2 6\n")]
