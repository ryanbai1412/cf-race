import re
from rlib import *

CONSTRAINTS = "One line of length <= 1000: '{', comma+space separated lowercase letters (possibly none), '}'."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: number of distinct letters in the set."
SHAPE = re.compile(r"\{(?:[a-z](?:, [a-z])*)?\}\Z")


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 1 and len(ls[0]) <= 1000 and SHAPE.match(ls[0]) is not None, "set format")


def solve(inp):
    return str(len({c for c in inp if c.islower()}))


def gen(rng):
    k = rng.choice([0, 1, rng.randint(0, 30), 333])
    alpha = LOWER[:rng.randint(1, 26)]
    return "{" + ", ".join(rng.choice(alpha) for _ in range(k)) + "}\n"


def extra():
    return [("boundary", "empty set", "{}\n"), ("adversarial", "one letter repeated", "{b, b, b, b}\n"),
            ("maxSize", "length 999 with all letters", "{" + ", ".join(LOWER[i % 26] for i in range(333)) + "}\n")]
