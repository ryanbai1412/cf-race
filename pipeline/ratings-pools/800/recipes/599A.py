from rlib import *

CONSTRAINTS = "three integers d1, d2, d3 in 1..10^8."
UNIQUENESS = "Minimum distance is unique."
STATEMENT = "Reviewed full statement: min(d1+d2+d3, 2(d1+d2), 2(d1+d3), 2(d2+d3))."


def validate(inp):
    nums(exact_tokens(inp, 3), 1, 10 ** 8)


def solve(inp):
    a, b, c = map(int, inp.split())
    return str(min(a + b + c, 2 * (a + b), 2 * (a + c), 2 * (b + c)))


def extra():
    return [("boundary", "all ones", "1 1 1\n"), ("adversarial", "long shop road, go home between", "1 1 100000000\n"),
            ("adversarial", "long d2, go via shop 1", "1 100000000 1\n"),
            ("maxSize", "all 10^8 (sum 3e8 exceeds nothing but 2*(a+b) 4e8 > 2^31)", "100000000 100000000 100000000\n"),
            ("maxSize", "near max with d3 cheap", "100000000 99999999 1\n")]
