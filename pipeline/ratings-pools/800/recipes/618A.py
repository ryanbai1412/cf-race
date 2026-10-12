from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^5."
UNIQUENESS = "Final row is deterministic."
STATEMENT = "Reviewed full statement: output (bit index + 1) of each set bit of n from high to low."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 5)


def solve(inp):
    n = int(inp.split()[0])
    return joined(i + 1 for i in range(n.bit_length() - 1, -1, -1) if n >> i & 1)


def simulate(n):
    row = []
    for _ in range(n):
        row.append(1)
        while len(row) > 1 and row[-1] == row[-2]:
            v = row.pop(); row[-1] = v + 1
    return joined(row)


def extra():
    for n in range(1, 300):
        assert solve(str(n)) == simulate(n)
    return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("adversarial", "n=2^16 single slime", "65536\n"),
            ("adversarial", "n=2^16-1 many slimes", "65535\n"), ("maxSize", "n=10^5", "100000\n"), ("maxSize", "n=99999", "99999\n")]
