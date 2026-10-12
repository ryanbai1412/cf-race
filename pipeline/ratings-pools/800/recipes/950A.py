from rlib import *

CONSTRAINTS = "three integers l, r, a in 0..100."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: 2*min(l+a, r+a, (l+r+a)//2)."


def validate(inp):
    nums(exact_tokens(inp, 3), 0, 100)


def solve(inp):
    l, r, a = map(int, inp.split())
    return str(2 * min(l + a, r + a, (l + r + a) // 2))


def extra():
    return [("boundary", "all zero", "0 0 0\n"), ("adversarial", "odd ambidexters left over", "1 0 2\n"),
            ("maxSize", "all 100", "100 100 100\n"), ("adversarial", "only ambidexters odd", "0 0 99\n")]
