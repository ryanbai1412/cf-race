import re
from rlib import *

CONSTRAINTS = "n in 1..100, then a string of n characters over B/W."
UNIQUENESS = "The encryption is unique."
STATEMENT = "Reviewed full statement: count and list lengths of maximal B runs."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 100)
    word(t[1], "BW", n, n)


def solve(inp):
    runs = [len(m) for m in re.findall(r"B+", inp.split()[1])]
    return "\n".join([str(len(runs))] + ([joined(runs)] if runs else []))


def extra():
    return [("boundary", "n=1 white -> 0 groups", "1\nW\n"), ("boundary", "n=1 black", "1\nB\n"),
            ("adversarial", "runs at both ends", "7\nBBWWBWB\n"),
            ("maxSize", "n=100 alternating 50 groups", "100\n" + "BW" * 50 + "\n"), ("maxSize", "n=100 all black", "100\n" + "B" * 100 + "\n")]
