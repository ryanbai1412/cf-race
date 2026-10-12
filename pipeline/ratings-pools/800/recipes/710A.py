from rlib import *

CONSTRAINTS = "one token 'cd' with c in a..h and d in 1..8."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: count king moves staying on the board."


def validate(inp):
    s = exact_tokens(inp, 1)[0]
    need(len(s) == 2 and s[0] in "abcdefgh" and s[1] in "12345678", "position")


def solve(inp):
    s = inp.split()[0]
    x, y = ord(s[0]) - 97, int(s[1]) - 1
    return str(sum(0 <= x + dx < 8 and 0 <= y + dy < 8 for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy))


def extra():
    return [("boundary", "corner a1", "a1\n"), ("boundary", "corner h8", "h8\n"), ("adversarial", "edge a5", "a5\n"),
            ("maxSize", "center d4", "d4\n")]
