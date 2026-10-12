import re
from rlib import *

CONSTRAINTS = "n in 1..200; second line is exactly n chars of letters in single-space separated words."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max count of capital letters in a word."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 2, "two lines")
    n = num(ls[0], 1, 200)
    need(len(ls[1]) == n and re.fullmatch(r"[A-Za-z]+( [A-Za-z]+)*", ls[1]) is not None, "single-space words of length n")


def solve(inp):
    return str(max(sum(c.isupper() for c in w) for w in lines(inp)[1].split(" ")))


def extra():
    t = " ".join(["A" * 99, "b" * 100])
    return [("boundary", "n=1 lowercase", "1\na\n"), ("boundary", "n=1 capital", "1\nZ\n"),
            ("adversarial", "max in later word, many words", "11\naB CD efGHi\n"),
            ("maxSize", "n=200 single word all capitals", "200\n" + "Q" * 200 + "\n"), ("maxSize", "n=200 two words", f"200\n{t}\n")]
