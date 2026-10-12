from collections import Counter
from rlib import *

CONSTRAINTS = "five integers t_i in 1..100."
UNIQUENESS = "Unique minimum sum."
STATEMENT = "Reviewed full statement: optionally discard 2 or 3 equal cards once."


def validate(inp):
    nums(exact_tokens(inp, 5), 1, 100)


def solve(inp):
    t = list(map(int, inp.split()))
    best = 0
    for v, c in Counter(t).items():
        if c >= 2:
            best = max(best, v * min(c, 3))
    return str(sum(t) - best)


def extra():
    return [("boundary", "all ones (discard three)", "1 1 1 1 1\n"), ("boundary", "all distinct", "1 2 3 4 5\n"),
            ("adversarial", "pair of larger value beats triple of smaller", "7 7 3 3 3\n"),
            ("adversarial", "triple 3 beats pair 4", "4 4 3 3 3\n"),
            ("maxSize", "all maximum", "100 100 100 100 100\n")]
