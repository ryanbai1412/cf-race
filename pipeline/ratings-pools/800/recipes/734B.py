from rlib import *

CONSTRAINTS = "four integers k2, k3, k5, k6 in 0..5*10^6."
UNIQUENESS = "Unique maximum."
STATEMENT = "Reviewed full statement: greedily build 256 then 32."


def validate(inp):
    nums(exact_tokens(inp, 4), 0, 5 * 10 ** 6)


def solve(inp):
    k2, k3, k5, k6 = map(int, inp.split())
    t = min(k2, k5, k6)
    return str(256 * t + 32 * min(k3, k2 - t))


def extra():
    return [("boundary", "all zero", "0 0 0 0\n"), ("boundary", "only 32", "1 1 0 0\n"),
            ("adversarial", "prefer 256 over 32 when 2s scarce", "1 1 1 1\n"),
            ("maxSize", "all maximum (1.28e9 near 32-bit limit)", "5000000 5000000 5000000 5000000\n"),
            ("maxSize", "max twos and threes, no 5s", "5000000 5000000 0 5000000\n")]
