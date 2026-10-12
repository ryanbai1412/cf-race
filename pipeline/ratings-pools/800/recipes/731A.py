from rlib import *

CONSTRAINTS = "one nonempty lowercase string of length <= 100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: wheel starts at 'a', sum of min circular distances."


def validate(inp):
    word(exact_tokens(inp, 1)[0], LOWER, 1, 100)


def solve(inp):
    cur, total = 0, 0
    for c in inp.split()[0]:
        d = abs(ord(c) - 97 - cur)
        total += min(d, 26 - d)
        cur = ord(c) - 97
    return str(total)


def extra():
    return [("boundary", "single a -> 0", "a\n"), ("boundary", "single n (distance 13)", "n\n"),
            ("adversarial", "wrap a->z->a", "zaz\n"), ("maxSize", "100 alternating a/n", "an" * 50 + "\n")]
