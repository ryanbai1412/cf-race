from rlib import *

CONSTRAINTS = "k, l, m, n in 1..10 and d in 1..10^5, each on its own line."
UNIQUENESS = "Count is a unique integer."
STATEMENT = "Reviewed full statement: count i in 1..d divisible by any of k, l, m, n."


def validate(inp):
    ls = lines(inp)
    need(len(ls) == 5, "five lines")
    for l in ls[:4]:
        num(l, 1, 10)
    num(ls[4], 1, 10 ** 5)


def solve(inp):
    k, l, m, n, d = map(int, inp.split())
    return str(sum(1 for i in range(1, d + 1) if i % k == 0 or i % l == 0 or i % m == 0 or i % n == 0))


def extra():
    return [("boundary", "d=1 all divisors 10", "10\n10\n10\n10\n1\n"), ("boundary", "k=1 d=1", "1\n2\n3\n4\n1\n"),
            ("adversarial", "coprime divisors inclusion-exclusion", "2\n3\n5\n7\n100000\n"),
            ("adversarial", "all equal divisors", "7\n7\n7\n7\n99999\n"),
            ("maxSize", "maximum d with large divisors", "10\n9\n8\n7\n100000\n")]
