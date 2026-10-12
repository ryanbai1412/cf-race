from rlib import *

CONSTRAINTS = "five integers s, v1, v2, t1, t2 in 1..1000."
UNIQUENESS = "One of three fixed outcomes."
STATEMENT = "Reviewed full statement: compare 2*t + s*v per participant."


def validate(inp):
    nums(exact_tokens(inp, 5), 1, 1000)


def solve(inp):
    s, v1, v2, t1, t2 = map(int, inp.split())
    a, b = 2 * t1 + s * v1, 2 * t2 + s * v2
    return "First" if a < b else "Second" if b < a else "Friendship"


def extra():
    return [("boundary", "all ones draw", "1 1 1 1 1\n"), ("adversarial", "faster typist loses to ping", "1 1 2 1000 1\n"),
            ("maxSize", "all maximum draw", "1000 1000 1000 1000 1000\n"), ("adversarial", "ping offsets exactly cancel", "2 1 2 2 1\n")]
