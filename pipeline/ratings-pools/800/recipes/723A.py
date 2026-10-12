from rlib import *

CONSTRAINTS = "three distinct integers in 1..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max - min."


def validate(inp):
    v = nums(exact_tokens(inp, 3), 1, 100)
    need(len(set(v)) == 3, "distinct")


def solve(inp):
    v = list(map(int, inp.split()))
    return str(max(v) - min(v))


def extra():
    return [("boundary", "1 2 3", "1 2 3\n"), ("adversarial", "unsorted extremes", "100 50 1\n"), ("maxSize", "1 100 99", "1 100 99\n")]
