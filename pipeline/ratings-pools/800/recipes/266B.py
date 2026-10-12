from rlib import *

CONSTRAINTS = "n, t in 1..50; string of n characters over B/G."
UNIQUENESS = "Simultaneous swaps make the result deterministic."
STATEMENT = "Reviewed full statement: each second every BG pair swaps simultaneously."


def validate(inp):
    t = exact_tokens(inp, 3)
    n = num(t[0], 1, 50); num(t[1], 1, 50)
    word(t[2], "BG", n, n)


def solve(inp):
    _, t, s = inp.split()
    s = list(s)
    for _ in range(int(t)):
        i = 0
        while i < len(s) - 1:
            if s[i] == "B" and s[i + 1] == "G":
                s[i], s[i + 1] = "G", "B"
                i += 2
            else:
                i += 1
    return "".join(s)


def extra():
    return [("boundary", "n=1", "1 50\nB\n"), ("boundary", "n=2 single swap", "2 1\nBG\n"),
            ("adversarial", "BBG chain: girl moves one step per second, not two", "3 1\nBBG\n"),
            ("adversarial", "BGBG simultaneous swaps", "4 1\nBGBG\n"),
            ("maxSize", "n=50 t=50 boys then girls", "50 50\n" + "B" * 25 + "G" * 25 + "\n"),
            ("maxSize", "n=50 t=7 alternating", "50 7\n" + "BG" * 25 + "\n")]
