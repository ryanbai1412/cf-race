from rlib import *

CONSTRAINTS = "One non-empty word of 1..1000 English letters."
UNIQUENESS = "Unique string."
STATEMENT = "Reviewed full statement: uppercase the first letter only."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 1, "one line")
    word(ls[0], LETTERS, 1, 1000)


def solve(inp):
    w = lines(inp)[0]
    return w[0].upper() + w[1:]


def gen(rng):
    L = rng.choice([1, 2, rng.randint(1, 1000), 1000])
    return "".join(rng.choice(LETTERS) for _ in range(L)) + "\n"


def extra():
    return [("boundary", "single lowercase letter", "a\n"), ("boundary", "single uppercase letter", "Z\n"),
            ("adversarial", "only first letter changes", "aBCDEF\n"), ("maxSize", "1000 letters", "q" * 1000 + "\n")]
