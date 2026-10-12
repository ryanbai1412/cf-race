from rlib import *

CONSTRAINTS = "two lines s, t over RGB, each of length 1..50; Liss never moves past the end of s."
UNIQUENESS = "Final position is deterministic."
STATEMENT = "Reviewed full statement: move forward when instruction color equals current stone color."


def run(s, t):
    p = 0
    for c in t:
        if s[p] == c:
            p += 1
            need(p < len(s), "moves out of sequence")
    return p + 1


def validate(inp):
    s, t = exact_tokens(inp, 2)
    word(s, "RGB", 1, 50); word(t, "RGB", 1, 50)
    run(s, t)


def solve(inp):
    s, t = inp.split()
    return str(run(s, t))


def extra():
    return [("boundary", "single stone, non-matching instruction", "R\nG\n"), ("boundary", "reaches last stone exactly", "RG\nR\n"),
            ("adversarial", "instructions matching later stones only", "RGB\nBBBGGG\n"),
            ("maxSize", "length 50 all moves along s", "RGB" * 16 + "RR\n" + ("RGB" * 16 + "R")[:49] + "B\n"),
            ("maxSize", "length 50 no moves", "R" * 50 + "\n" + "G" * 50 + "\n")]
