from rlib import *

CONSTRAINTS = "k, w in 1..1000, n in 0..10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: max(0, k*w*(w+1)/2 - n)."


def validate(inp):
    k, n, w = exact_tokens(inp, 3)
    num(k, 1, 1000); num(n, 0, 10 ** 9); num(w, 1, 1000)


def solve(inp):
    k, n, w = map(int, inp.split())
    return str(max(0, k * w * (w + 1) // 2 - n))


def extra():
    return [("boundary", "n=0", "1 0 1\n"), ("boundary", "exactly enough", "3 6 2\n"),
            ("adversarial", "lots of money", "1 1000000000 1000\n"),
            ("maxSize", "k=w=1000 n=0 (500500000)", "1000 0 1000\n"), ("maxSize", "k=w=1000 n=10^9", "1000 1000000000 1000\n")]
