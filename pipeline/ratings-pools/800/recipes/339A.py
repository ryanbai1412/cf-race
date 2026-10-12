import re
from rlib import *

CONSTRAINTS = "one nonempty string of length <= 100: summands 1/2/3 separated by '+'."
UNIQUENESS = "Sorted sum string is unique."
STATEMENT = "Reviewed full statement: print the summands sorted non-decreasing joined by '+'."


def validate(inp):
    s = exact_tokens(inp, 1)[0]
    need(len(s) <= 100 and re.fullmatch(r"[123](\+[123])*", s) is not None, "correct sum")


def solve(inp):
    return "+".join(sorted(inp.split()[0].split("+")))


def extra():
    r = rng(339)
    return [("boundary", "single summand", "2\n"), ("boundary", "already sorted", "1+1+3\n"),
            ("adversarial", "reverse sorted", "3+2+1\n"),
            ("maxSize", "99 characters (50 summands) random", "+".join(r.choice("123") for _ in range(50)) + "\n"),
            ("maxSize", "50 threes", "+".join(["3"] * 50) + "\n")]
