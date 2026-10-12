from rlib import *

CONSTRAINTS = "n in 1..100, then a correct binary string of length n (no leading zeros unless '0')."
UNIQUENESS = "Minimum string is unique."
STATEMENT = "Reviewed full statement: '0' stays; otherwise '1' followed by all zeros."


def validate(inp):
    t = exact_tokens(inp, 2)
    n = num(t[0], 1, 100)
    word(t[1], "01", n, n)
    need(t[1] == "0" or t[1][0] == "1", "correct string")


def solve(inp):
    s = inp.split()[1]
    return s if s == "0" else "1" + "0" * s.count("0")


def extra():
    return [("boundary", "single 0", "1\n0\n"), ("boundary", "single 1", "1\n1\n"),
            ("maxSize", "n=100 1 then 99 zeros", "100\n1" + "0" * 99 + "\n"), ("maxSize", "n=100 alternating", "100\n" + "10" * 50 + "\n")]
