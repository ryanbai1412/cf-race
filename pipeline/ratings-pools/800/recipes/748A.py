from rlib import *

CONSTRAINTS = "n, m in 1..10^4, k in 1..2nm."
UNIQUENESS = "Place is uniquely determined."
STATEMENT = "Reviewed full statement: lane = (k-1)//(2m)+1, desk = ((k-1)%(2m))//2+1, side L if k odd."


def validate(inp):
    n, m, k = exact_tokens(inp, 3)
    n = num(n, 1, 10 ** 4); m = num(m, 1, 10 ** 4); num(k, 1, 2 * n * m)


def solve(inp):
    n, m, k = map(int, inp.split())
    return f"{(k - 1) // (2 * m) + 1} {(k - 1) % (2 * m) // 2 + 1} {'L' if k % 2 else 'R'}"


def extra():
    return [("boundary", "1 1 1", "1 1 1\n"), ("boundary", "1 1 2", "1 1 2\n"),
            ("adversarial", "last place of a lane", "3 4 8\n"),
            ("maxSize", "max n, m, last place 2e8", "10000 10000 200000000\n"), ("maxSize", "max n, m, middle", "10000 10000 123456789\n")]
