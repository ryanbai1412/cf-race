from rlib import *

CONSTRAINTS = "four integers n1, n2, k1, k2 in 1..50."
UNIQUENESS = "Winner is unique under optimal play."
STATEMENT = "Reviewed full statement: First wins iff n1 > n2 (k irrelevant)."


def validate(inp):
    nums(exact_tokens(inp, 4), 1, 50)


def solve(inp):
    n1, n2, _, _ = map(int, inp.split())
    return "First" if n1 > n2 else "Second"


def extra():
    return [("boundary", "all ones", "1 1 1 1\n"), ("boundary", "n1=2 n2=1", "2 1 1 1\n"),
            ("adversarial", "equal boxes, huge k1", "50 50 50 1\n"), ("maxSize", "all maximum", "50 50 50 50\n"),
            ("adversarial", "n1 one larger, small k", "50 49 1 50\n")]
