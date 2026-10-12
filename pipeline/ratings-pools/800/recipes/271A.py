from rlib import *

CONSTRAINTS = "a single integer y with 1000 <= y <= 9000."
UNIQUENESS = "Minimum year is unique."
STATEMENT = "Reviewed full statement: smallest year > y with distinct digits."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1000, 9000)


def solve(inp):
    y = int(inp.split()[0]) + 1
    while len(set(str(y))) != 4:
        y += 1
    return str(y)


def extra():
    return [("boundary", "minimum y=1000", "1000\n"), ("boundary", "maximum y=9000", "9000\n"),
            ("adversarial", "1987 -> 2013 long gap", "1987\n"), ("adversarial", "8888", "8888\n"),
            ("maxSize", "8999 crosses thousand", "8999\n")]
